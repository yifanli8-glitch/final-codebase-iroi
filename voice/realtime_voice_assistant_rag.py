#!/usr/bin/env python3
"""
DOGU Voice Assistant - Realtime API + OpenWakeWord + RAG
Combines:
- OpenWakeWord for local wake word detection
- RAG (Retrieval Augmented Generation) with confidence gating
- OpenAI Realtime API for low-latency voice conversation
"""

import os
import sys
import asyncio
import threading
import tempfile
import wave
import time
import numpy as np
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

# Import OpenWakeWord
try:
    from openwakeword import Model
    OWW_AVAILABLE = True
except ImportError:
    OWW_AVAILABLE = False
    print("Warning: openwakeword not installed: pip install openwakeword")

# Import config (try voice/config.py first, then parent config.py)
CONFIG_AVAILABLE = False
OPENAI_API_KEY = None
MIC_DEVICE_NAME = "default"
WAKE_RESPONSE = "Which task do you want me to help with?"

# Try voice/config.py first
try:
    import config as voice_config_module
    if hasattr(voice_config_module, 'OPENAI_API_KEY'):
        OPENAI_API_KEY = voice_config_module.OPENAI_API_KEY
    if hasattr(voice_config_module, 'MIC_DEVICE_NAME'):
        MIC_DEVICE_NAME = voice_config_module.MIC_DEVICE_NAME
    CONFIG_AVAILABLE = True
except ImportError:
    pass

# Try parent config.py if not found
if not CONFIG_AVAILABLE or not OPENAI_API_KEY:
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, parent_dir)
    try:
        import config as parent_config
        if hasattr(parent_config, 'OPENAI_API_KEY'):
            OPENAI_API_KEY = parent_config.OPENAI_API_KEY
        if hasattr(parent_config, 'MIC_DEVICE_NAME'):
            MIC_DEVICE_NAME = parent_config.MIC_DEVICE_NAME
        if hasattr(parent_config, 'WAKE_RESPONSE'):
            WAKE_RESPONSE = parent_config.WAKE_RESPONSE
        CONFIG_AVAILABLE = True
    except ImportError:
        pass

# Add voice directory to path
VOICE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, VOICE_DIR)

# Import Realtime API components
from mic_stream_arecord import MicrophoneStreamArecord
from local_peer import LocalPeer
# Note: voice_config is imported separately for Realtime API settings

# Import RAG components
try:
    from rag_retriever import RAGRetriever
    from rag_config import RAG_SYSTEM_INSTRUCTIONS
    RAG_RETRIEVER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: RAG retriever not available: {e}")
    RAG_RETRIEVER_AVAILABLE = False
    RAG_SYSTEM_INSTRUCTIONS = "You are a helpful assistant.\n\n{context}"


class RealtimeVoiceAssistantRAG(QObject):
    """Voice Assistant with OpenWakeWord + RAG + Realtime API"""
    
    # Qt signals for UI integration
    wake_word_detected = pyqtSignal(str)
    speech_recognized = pyqtSignal(str)
    response_ready = pyqtSignal(str)
    speaking_finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, api_key: str = None, docs_dir: str = None):
        super().__init__()
        
        # API Key
        self.api_key = api_key or OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key == "YOUR_OPENAI_API_KEY" or "API Key" in str(self.api_key):
            print("Warning: Please set OPENAI_API_KEY in config.py")
            self.api_key = None
        else:
            print(f"API Key loaded: {self.api_key[:20]}...")
        
        # Microphone device
        self.device_name = MIC_DEVICE_NAME
        self.wake_response = WAKE_RESPONSE
        
        # OpenWakeWord model
        self.oww_model = None
        if OWW_AVAILABLE:
            self._init_wake_word_model()
        
        # Initialize RAG retriever (NEW: replaces simple document loading)
        self.rag_retriever = None
        if RAG_RETRIEVER_AVAILABLE and self.api_key:
            self.rag_retriever = RAGRetriever(api_key=self.api_key, docs_dir=docs_dir)
        else:
            print("⚠️ RAG retriever not initialized (need API key)")
        
        # Legacy: Keep old docs_context for backward compatibility with Realtime API
        # (Realtime API needs context at session start, can't do retrieval per turn)
        self.docs_context = self._load_documents(docs_dir)
        
        # Image analysis context (for maintaining image memory in Realtime API conversations)
        self.last_image_analysis = ""  # Back-compat: latest image summary (short)
        # New: structured image context blocks to inject into the *current* Realtime session
        # Keep a small rolling window to avoid instructions growing without bound.
        self.image_context_history = []  # list[str]
        self.max_image_contexts = 3
        
        # Realtime API components
        self.local_peer = None
        self.mic_track = None
        self.realtime_loop = None
        self.realtime_thread = None
        
        # State
        self.listening = False
        self.in_conversation = False
        self.audio_transcript_buffer = []
        self.user_transcript_buffer = []

    def clear_image_context(self):
        self.last_image_analysis = ""
        self.image_context_history = []

    def _build_realtime_instructions(self) -> str:
        """Build Realtime session instructions from RAG + image context.
        This is used at session start and for in-session session.update.
        """
        instructions = (
            "You are IROI, a lab teaching assistant robot for a Sensor and Circuit course. "
            "Always respond in English. Be concise and helpful, like a friendly lab TA."
        )

        if self.docs_context:
            instructions += (
                f"\n\nKnowledge base context:\n{self.docs_context[:5000]}"
            )
        # Add structured image context blocks (preferred)
        if self.image_context_history:
            # Keep only the last N blocks to control size
            blocks = self.image_context_history[-self.max_image_contexts :]
            instructions += "\n\n" + "\n\n".join(blocks)
        # Fallback: legacy single summary
        elif self.last_image_analysis:
            instructions += f"\n\n{self.last_image_analysis}"

        return instructions

    def _make_image_context_block(self, analysis_text: str, user_intent: str = "") -> str:
        """Format a structured, injectable image context block for Realtime instructions."""
        ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        analysis_excerpt = (analysis_text or "").strip()
        # Keep excerpt reasonably sized for instructions
        if len(analysis_excerpt) > 1200:
            analysis_excerpt = analysis_excerpt[:1200].rstrip() + "..."

        # Minimal structured template (works even if we don't parse the diagram)
        intent_line = user_intent.strip() if user_intent else "Analyze the uploaded diagram and use it for subsequent answers."
        return (
            "<<<IMAGE_CONTEXT v1>>>\n"
            "You have a user-provided diagram image. Treat the following as the best available description of the image.\n"
            "Use it to answer subsequent questions. If the question depends on details not present here, ask a targeted clarification.\n\n"
            f"Image ID: {ts}\n"
            f"User intent: {intent_line}\n\n"
            "Observations (from the diagram):\n"
            f"- {analysis_excerpt}\n\n"
            "Uncertainties (do NOT assume):\n"
            "- Exact node names/values not explicitly described above\n\n"
            "Answering rules:\n"
            "- Prefer the diagram context above over general assumptions when they conflict.\n"
            "<<<END_IMAGE_CONTEXT>>>"
        )

    def push_realtime_instructions_update(self, reason: str = "image_context"):
        """Update the *current* Realtime session instructions via session.update (no reconnect)."""
        if not self.in_conversation:
            return
        if not self.realtime_loop or not self.local_peer:
            return
        try:
            future = asyncio.run_coroutine_threadsafe(
                self._send_session_update(self._build_realtime_instructions(), reason=reason),
                self.realtime_loop,
            )
            # Best-effort: don't block the UI thread too long
            future.result(timeout=2)
        except Exception as e:
            print(f"Warning: Failed to push session.update ({reason}): {e}")

    async def _send_session_update(self, instructions: str, reason: str = ""):
        """Send a session.update over the existing DataChannel."""
        if not self.local_peer or not self.local_peer.data_channel:
            return
        if getattr(self.local_peer.data_channel, "readyState", None) != "open":
            return
        import json
        config_event = {
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",
                "instructions": instructions,
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {"model": "whisper-1", "language": "en"},
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.3,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 700,
                },
            },
        }
        self.local_peer.data_channel.send(json.dumps(config_event))
        if reason:
            print(f"🖼️ [Image Context] session.update pushed ({reason})")
    
    def _init_wake_word_model(self):
        """Initialize OpenWakeWord model (expects model/eyeroeee.onnx)."""
        try:
            try:
                import openwakeword.utils
                openwakeword.utils.download_models()
                print("✅ [OpenWakeWord] Base models ready")
            except Exception as e:
                print(f"⚠️ [OpenWakeWord] Error downloading base models (may already exist): {e}")
            
            model_dir = os.path.join(os.path.dirname(__file__), "..", "model")
            model_path = os.path.join(model_dir, "eyeroeee.onnx")
            if not os.path.exists(model_path):
                tflite_path = os.path.join(model_dir, "eyeroeee.tflite")
                if os.path.exists(tflite_path):
                    print(f"⚠️ [OpenWakeWord] Wake word model not found: {model_path}")
                    print("   (You have eyeroeee.tflite; OpenWakeWord needs eyeroeee.onnx. Export ONNX and put in model/.)")
                else:
                    print(f"⚠️ [OpenWakeWord] Wake word model not found: {model_path}")
                self.oww_model = None
                return
            self.oww_model = Model(wakeword_models=[model_path], inference_framework="onnx")
            print(f"✅ [OpenWakeWord] Custom model loaded: {model_path}")
        except Exception as e:
            print(f"⚠️ [OpenWakeWord] Failed to load model: {e}")
            import traceback
            traceback.print_exc()
            self.oww_model = None
    
    def _load_documents(self, docs_dir: str = None) -> str:
        """Load RAG documents from docs/."""
        if docs_dir:
            docs_path = Path(docs_dir)
        else:
            docs_path = Path(__file__).parent.parent / "docs"
        
        if not docs_path.exists():
            print(f"Info: Docs directory not found: {docs_path}")
            return ""
        
        documents = []
        for md_file in docs_path.glob("**/*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                documents.append(f"# {md_file.name}\n{content}")
            except Exception as e:
                print(f"Warning: Failed to load {md_file}: {e}")
        
        if documents:
            rag_context = "\n\n---\n\n".join(documents)
            print(f"RAG: Loaded {len(documents)} document(s), {len(rag_context)} chars")
            return rag_context
        return ""
    
    def start_listening(self, audio_mode: bool = True):
        """Start listening for wake word"""
        if self.listening:
            print("Already listening")
            return
        
        if not self.oww_model:
            print("Error: Wake word model not available")
            self.error_occurred.emit("Wake word model not available")
            return
        
        if not self.api_key:
            print("Error: API key not available")
            self.error_occurred.emit("API key not available")
            return
        
        self.listening = True
        
        # Start wake word detection thread
        self.wake_thread = threading.Thread(target=self._wake_word_loop, daemon=True)
        self.wake_thread.start()
    
    def start_conversation_direct(self):
        """
        Start Realtime API conversation directly without wake word detection
        Use this for UI modes where you want immediate conversation (like QA Chat)
        Similar to how run.py works
        """
        if self.in_conversation:
            print("⚠️ Already in conversation")
            return
        
        if not self.api_key:
            print("❌ API key not available")
            self.error_occurred.emit("API key not available")
            return
        
        print("🎙️ [Direct] Starting conversation without wake word...")
        
        # Set conversation flag FIRST
        self.in_conversation = True
        
        # Emit initial response
        self.response_ready.emit(self.wake_response)
        
        # Start Realtime API in separate thread (same as wake word path)
        self.realtime_thread = threading.Thread(
            target=self._run_realtime_api,
            daemon=True
        )
        self.realtime_thread.start()
        print("🎙️ [Direct] Conversation thread started")
    
    def record_audio(self, duration: int = 10, silence_threshold: float = 500) -> str:
        import subprocess
        import wave
        import struct
        
        timestamp = int(time.time() * 1000)
        wav_path = f"/tmp/recording_{timestamp}.wav"
        
        cmd = [
            'arecord',
            '-D', self.device_name,
            '-f', 'S16_LE',
            '-r', '16000',
            '-c', '1',
            '-d', str(duration),
            wav_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )
            return wav_path
        except subprocess.CalledProcessError as e:
            msg = (e.stderr or "").strip()
            print(f"❌ [Record] arecord failed (code {e.returncode}) on {self.device_name}")
            if msg:
                print(f"   stderr: {msg}")
            return None
        except Exception as e:
            print(f"❌ [Record] Unexpected error while recording on {self.device_name}: {e}")
            return None
    
    def _record_user_input(self, duration: int = 10) -> str:
        return self.record_audio(duration=duration) or None
    
    def _passes_energy_filter(
        self,
        pcm_bytes: bytes,
        sample_rate: int,
        rms_threshold: float = 80.0,
        speech_band_ratio_min: float = 0.22,
        band_low_hz: float = 300.0,
        band_high_hz: float = 3400.0,
        _debug: bool = True,
    ) -> bool:
        if len(pcm_bytes) < 2:
            if _debug:
                print("🔇 [EnergyFilter] Skip: too short")
            return False
        samples = np.frombuffer(pcm_bytes, dtype=np.int16)
        if samples.size == 0:
            return False
        rms = np.sqrt(np.mean(samples.astype(np.float64) ** 2))
        if rms < rms_threshold:
            if _debug:
                print(f"🔇 [EnergyFilter] Reject: RMS={rms:.0f} < {rms_threshold}")
            return False
        n = samples.size
        window = np.hanning(n)
        spectrum = np.fft.rfft(samples.astype(np.float64) * window)
        freqs = np.fft.rfftfreq(n, 1.0 / sample_rate)
        power = np.abs(spectrum) ** 2
        power_total = np.sum(power)
        if power_total <= 0:
            return False
        mask = (freqs >= band_low_hz) & (freqs <= band_high_hz)
        power_band = np.sum(power[mask])
        ratio = power_band / power_total
        if ratio < speech_band_ratio_min:
            if _debug:
                print(f"🔇 [EnergyFilter] Reject: speech_band_ratio={ratio:.2f} < {speech_band_ratio_min}")
            return False
        return True

    def _extract_speech_with_vad(self, wav_path: str, min_speech_sec: float = 0.4) -> str:
        try:
            import webrtcvad
        except ImportError:
            return wav_path
        
        try:
            with wave.open(wav_path, 'rb') as wf:
                sr = wf.getframerate()
                nch = wf.getnchannels()
                sample_width = wf.getsampwidth()
                pcm = wf.readframes(wf.getnframes())
            if sr not in (8000, 16000, 32000) or nch != 1 or sample_width != 2:
                return wav_path
        except Exception as e:
            print(f"⚠️ [VAD] Cannot read WAV: {e}")
            return wav_path
        
        frame_duration_ms = 30
        frame_len = int(sr * frame_duration_ms / 1000) * 2  # bytes
        n_frames = len(pcm) // frame_len
        if n_frames == 0:
            return None
        
        vad = webrtcvad.Vad(2)
        speech_frames = []
        for i in range(n_frames):
            start = i * frame_len
            frame = pcm[start:start + frame_len]
            if len(frame) < frame_len:
                break
            if vad.is_speech(frame, sr):
                speech_frames.append(frame)
        
        if not speech_frames:
            print("🔇 [VAD] No speech frames")
            return None
        speech_duration_sec = len(speech_frames) * frame_duration_ms / 1000.0
        if speech_duration_sec < min_speech_sec:
            print(f"🔇 [VAD] Speech too short: {speech_duration_sec:.2f}s < {min_speech_sec}s")
            return None
        
        out_pcm = b''.join(speech_frames)
        if not self._passes_energy_filter(out_pcm, sr):
            return None
        fd, out_path = tempfile.mkstemp(suffix='_vad.wav')
        os.close(fd)
        with wave.open(out_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(out_pcm)
        return out_path
    
    def transcribe_audio(self, audio_path: str, use_vad: bool = True) -> str:
        vad_path = None
        try:
            if use_vad:
                vad_path = self._extract_speech_with_vad(audio_path)
                if vad_path is None:
                    return ""
                path_to_transcribe = vad_path
            else:
                path_to_transcribe = audio_path
            
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            with open(path_to_transcribe, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            
            return (transcript.text or "").strip()
        except Exception as e:
            return ""
        finally:
            if vad_path and vad_path != audio_path and os.path.exists(vad_path):
                try:
                    os.unlink(vad_path)
                except OSError:
                    pass
    
    def text_to_speech(self, text: str) -> str:
        print(f"🔊 [TTS] Converting text to speech ({len(text)} chars)...")
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            timestamp = int(time.time() * 1000)
            audio_path = f"/tmp/tts_{timestamp}.mp3"
            
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            
            response.stream_to_file(audio_path)
            print(f"✅ [TTS] Saved to {audio_path}")
            return audio_path
            
        except Exception as e:
            print(f"❌ [TTS] Error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def play_audio(self, audio_path: str):
        import subprocess
        
        print(f"▶️ [Playback] Playing {audio_path}...")
        
        try:
            if audio_path.endswith('.mp3'):
                cmd = ['mpg123', '-q', audio_path]
            else:
                cmd = ['aplay', '-q', audio_path]
            
            subprocess.run(cmd, check=True, stderr=subprocess.DEVNULL)
            print(f"✅ [Playback] Finished")
            
        except Exception as e:
            print(f"❌ [Playback] Error: {e}")
    
    def chat_with_rag(self, user_message: str, image_paths: list = None):
        """
        Text-based chat with RAG retrieval + confidence gating + optional image analysis
        Used by QA Chat panel for image analysis
        Uses standard GPT-4 Vision API (not Realtime API)
        
        NEW: Implements confidence gating - fail-fast if retrieval confidence is low
        """
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            # ========== STEP 1: Retrieval with Confidence Gating ==========
            retrieval_result = None
            if self.rag_retriever and not image_paths:  # Only use retrieval for text queries
                retrieval_result = self.rag_retriever.retrieve(user_message)
                
                # Check if retrieval failed (low confidence)
                if retrieval_result["status"] == "no_answer":
                    retrieval_result = None
            
            # ========== STEP 2: Prepare LLM Context ==========
            messages = []
            
            # System message with RAG context
            if retrieval_result and retrieval_result["status"] == "success":
                # Use retrieved chunks (HIGH CONFIDENCE PATH)
                retrieved_context = self.rag_retriever.get_context_for_llm(retrieval_result["chunks"])
                system_content = RAG_SYSTEM_INSTRUCTIONS.format(context=retrieved_context)
            elif image_paths:
                system_content = (
                    "You are IROI, a lab teaching assistant robot for a Sensor and Circuit course. "
                    "Always respond in English. Analyze the image and answer concisely."
                )
                if self.docs_context:
                    system_content += f"\n\nKnowledge base context:\n{self.docs_context[:5000]}"
            else:
                system_content = (
                    "You are IROI, a lab teaching assistant robot for a Sensor and Circuit course. "
                    "Always respond in English. Be concise and helpful."
                )
                if self.docs_context:
                    system_content += f"\n\nKnowledge base context:\n{self.docs_context[:5000]}"
            
            messages.append({"role": "system", "content": system_content})
            
            # ========== STEP 3: User Message ==========
            if image_paths:
                import base64
                content = [{"type": "text", "text": user_message}]
                for img_path in image_paths:
                    with open(img_path, "rb") as f:
                        img_data = base64.b64encode(f.read()).decode()
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_data}"}
                    })
                messages.append({"role": "user", "content": content})
            else:
                messages.append({"role": "user", "content": user_message})
            
            # ========== STEP 4: Call LLM ==========
            response = client.chat.completions.create(
                model="gpt-4o" if image_paths else "gpt-4o",  # Use GPT-4o for both text and vision
                messages=messages,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            
            # If this was an image analysis, save a summary for future Realtime API conversations
            if image_paths:
                # Create a concise summary for injection into Realtime API
                summary = f"User uploaded an image. Analysis: {answer[:200]}..."  # First 200 chars
                self.last_image_analysis = summary
                # New: keep a structured block and push session.update to the current Realtime session
                block = self._make_image_context_block(
                    analysis_text=answer,
                    user_intent=user_message,
                )
                self.image_context_history.append(block)
                if len(self.image_context_history) > self.max_image_contexts:
                    self.image_context_history = self.image_context_history[-self.max_image_contexts :]
                self.push_realtime_instructions_update(reason="image_analysis")
            
            return answer
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def stop_listening(self):
        """Stop listening and any active Realtime conversation.
        Must always stop Realtime session when called (e.g. leaving QA Chat or Lab mode),
        even if listening was False (direct conversation started without wake word).
        """
        # Always stop any active Realtime conversation first (e.g. from QA Chat or wake word in Lab flow)
        self.in_conversation = False
        if self.realtime_loop and self.local_peer:
            try:
                future = asyncio.run_coroutine_threadsafe(self._stop_realtime(), self.realtime_loop)
                future.result(timeout=3)  # Wait up to 3 seconds
            except Exception as e:
                print(f"Warning: Error stopping realtime session: {e}")

        if not self.listening:
            return

        print("Stopping voice assistant...")
        self.listening = False

        # Wait for threads to finish
        if hasattr(self, 'wake_thread') and self.wake_thread and self.wake_thread.is_alive():
            self.wake_thread.join(timeout=2)

        if hasattr(self, 'realtime_thread') and self.realtime_thread and self.realtime_thread.is_alive():
            self.realtime_thread.join(timeout=2)

        print("Voice assistant stopped")
    
    def _wake_word_loop(self):
        """Background thread for wake word detection"""
        import subprocess
        
        # Audio parameters for wake word detection
        chunk_size = 1280  # 80ms at 16kHz
        
        try:
            # Start arecord for wake word detection
            cmd = [
                'arecord',
                '-D', self.device_name,
                '-f', 'S16_LE',
                '-r', '16000',  # 16kHz for wake word
                '-c', '1',
                '-t', 'raw',
                '--'
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            
            print(f"Wake word detection started on {self.device_name}")
            
            while self.listening:
                # ⚠️ Check if conversation was started externally (e.g., from UI)
                if self.in_conversation:
                    # print("DEBUG: [Wake loop] Conversation started externally, stopping arecord...")
                    try:
                        process.terminate()
                        process.wait(timeout=1)
                    except:
                        process.kill()
                    # print("DEBUG: [Wake loop] arecord stopped for conversation")
                    
                    # Wait for conversation to finish
                    while self.in_conversation and self.listening:
                        time.sleep(0.5)
                    
                    # Restart arecord
                    if self.listening:
                        # print("DEBUG: [Wake loop] Conversation ended, restarting arecord...")
                        process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        # print("DEBUG: [Wake loop] arecord restarted")
                    continue
                
                # Read audio chunk
                audio_data = process.stdout.read(chunk_size * 2)  # 2 bytes per sample
                if not audio_data:
                    break
                
                # Convert to numpy array
                audio_array = np.frombuffer(audio_data, dtype=np.int16)
                
                # Run wake word detection
                prediction = self.oww_model.predict(audio_array)
                
                # Check for wake word
                for mdl in self.oww_model.prediction_buffer.keys():
                    scores = list(self.oww_model.prediction_buffer[mdl])
                    if scores and scores[-1] > 0.5:
                        print(f"Wake word detected! (score: {scores[-1]:.2f})")
                        
                        self.wake_word_detected.emit("iroi")
                        self.oww_model.prediction_buffer[mdl].clear()
            
            # Cleanup
            try:
                process.terminate()
                process.wait(timeout=2)
            except:
                process.kill()
            print("Wake word detection stopped")
            
        except Exception as e:
            print(f"Wake word detection error: {e}")
            self.error_occurred.emit(f"Wake word error: {e}")
    
    def trigger_conversation(self):
        """
        Public method to trigger conversation (for UI integration)
        This simulates a wake word detection from external code
        """
        if self.in_conversation:
            print("⚠️ Already in conversation")
            return
        
        if not self.listening:
            print("⚠️ Voice assistant not listening, call start_listening() first")
            return
        
        print("🎙️ [External trigger] Starting conversation...")
        # Set flag to trigger conversation
        # The wake word loop will detect this and handle mic properly
        self._start_conversation()
    
    def _start_conversation(self):
        """Start Realtime API conversation (internal)"""
        if self.in_conversation:
            return
        
        self.in_conversation = True
        
        # print("DEBUG: [_start_conversation] Starting conversation...")
        # print(f"DEBUG: [_start_conversation] listening={self.listening}")
        
        # ⚠️ CRITICAL: If wake word detection is running, we need to temporarily pause it
        # to avoid microphone resource conflict with Realtime API
        # Note: The wake word loop will resume after conversation ends
        if self.listening and hasattr(self, 'wake_thread') and self.wake_thread and self.wake_thread.is_alive():
            pass # print("DEBUG: [_start_conversation] Wake word detection is running, will let it handle mic conflict")
            # Wake word loop will stop its arecord when it detects conversation start
        
        # Emit wake response
        self.response_ready.emit(self.wake_response)
        
        # Start Realtime API in separate thread
        self.realtime_thread = threading.Thread(
            target=self._run_realtime_api,
            daemon=True
        )
        self.realtime_thread.start()
        # print("DEBUG: [_start_conversation] Realtime thread started")
    
    def _run_realtime_api(self):
        """Run Realtime API in asyncio event loop"""
        # print("DEBUG: [_run_realtime_api] Creating event loop...")
        # Create new event loop for this thread
        self.realtime_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.realtime_loop)
        
        try:
            # print("DEBUG: [_run_realtime_api] Starting realtime session...")
            self.realtime_loop.run_until_complete(self._realtime_session())
            # print("DEBUG: [_run_realtime_api] Realtime session completed")
        except Exception as e:
            print(f"❌ Realtime API error: {e}")
            import traceback
            traceback.print_exc()
            self.error_occurred.emit(f"Realtime error: {e}")
        finally:
            # print("DEBUG: [_run_realtime_api] Cleaning up...")
            self.realtime_loop.close()
            self.realtime_loop = None
            self.in_conversation = False
            # print("DEBUG: [_run_realtime_api] Cleanup complete")
    
    async def _realtime_session(self):
        """Run Realtime API session"""
        # print("DEBUG: [_realtime_session] Session starting...")
        # Build instructions from RAG + image context
        instructions = self._build_realtime_instructions()
        if self.docs_context:
            print(f"✅ [RAG] Knowledge base added to instructions ({len(self.docs_context[:5000])} chars)")
        else:
            print("⚠️ [RAG] No knowledge base available")
        if self.image_context_history or self.last_image_analysis:
            print("🖼️ [Image Context] Included in Realtime instructions")
        
        # print(f"DEBUG: [_realtime_session] Instructions size: {len(instructions)} chars")
        
        prompt_payload = {
            "model": "gpt-4o-realtime-preview-2024-12-17",
            "modalities": ["text", "audio"],
            "voice": "alloy",
            "instructions": instructions,
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "input_audio_transcription": {
                "model": "whisper-1",
                "language": "en"
            },
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.3,
                "prefix_padding_ms": 300,
                "silence_duration_ms": 700
            },
            "temperature": 0.8
        }
        
        # Create microphone stream
        # print("DEBUG: [_realtime_session] Creating microphone stream...")
        input_settings = {
            "rate": 48000,
            "channels": 1,
            "chunk_size": 1024,
            "input_gain": 15.0,  # Increased gain for better detection
            "minimum_volume": 0.0,
        }
        
        self.mic_track = MicrophoneStreamArecord(
            mic_settings=input_settings,
            device_name=self.device_name,
            audio_stream=None,
        )
        # print("DEBUG: [_realtime_session] Microphone stream created")
        
        # Create LocalPeer
        # print("DEBUG: [_realtime_session] Creating LocalPeer...")
        self.local_peer = LocalPeer(
            api_key=self.api_key,
            prompt_payload=prompt_payload,
        )
        # print("DEBUG: [_realtime_session] LocalPeer created")
        
        # Start connection
        # print("DEBUG: [_realtime_session] Starting connection...")
        await self.local_peer.start(add_audio=True, input_track=self.mic_track)
        # print("DEBUG: [_realtime_session] Sending offer...")
        await self.local_peer.send_offer()
        # print("DEBUG: [_realtime_session] Offer sent")
        
        # Wait for DataChannel
        # print("DEBUG: [_realtime_session] Waiting for DataChannel to open...")
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < 15.0:
            elapsed = asyncio.get_event_loop().time() - start_time
            if self.local_peer.data_channel:
                state = self.local_peer.data_channel.readyState
                # print(f"DEBUG: [_realtime_session] DataChannel state: {state} (elapsed: {elapsed:.1f}s)")
                if state == "open":
                    break
            else:
                pass # print(f"DEBUG: [_realtime_session] DataChannel is None (elapsed: {elapsed:.1f}s)")
            await asyncio.sleep(0.5)
        else:
            error_msg = f"DataChannel failed to open after 15s"
            if self.local_peer.data_channel:
                error_msg += f" (final state: {self.local_peer.data_channel.readyState})"
            else:
                error_msg += " (DataChannel is None)"
            print(f"❌ {error_msg}")
            raise RuntimeError(error_msg)
        
        # print("DEBUG: [_realtime_session] DataChannel is open!")
        
        # Send session configuration
        # print("DEBUG: [_realtime_session] Preparing session config...")
        config_event = {
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",
                "instructions": instructions,
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.3,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 700
                }
            }
        }
        import json
        # print("DEBUG: [_realtime_session] Sending session config...")
        self.local_peer.data_channel.send(json.dumps(config_event))
        # print("DEBUG: [_realtime_session] Session config sent")
        
        print("Realtime API session started")
        # print("DEBUG: [_realtime_session] Resetting buffers...")
        
        # Reset buffers
        self.audio_transcript_buffer = []
        self.user_transcript_buffer = []
        
        # print("DEBUG: [_realtime_session] Buffers reset")
        
        # Event loop
        # print("DEBUG: [_realtime_session] Preparing event loop...")
        conversation_timeout = 600  # 600 seconds (10 minutes) of silence ends conversation
        last_activity = time.time()
        
        print("Event loop started, listening for responses...")
        # print("DEBUG: [_realtime_session] Entering main event loop...")
        
        try:
            loop_iteration = 0
            while self.in_conversation:
                loop_iteration += 1
                # if loop_iteration <= 3:
                #     print(f"DEBUG: [Event loop] Iteration {loop_iteration}")
                try:
                    ev = await asyncio.wait_for(
                        self.local_peer.recv_event(timeout=1.0),
                        timeout=2.0
                    )
                    # if loop_iteration <= 3:
                    #     print(f"DEBUG: [Event loop] Received event")
                    
                    if isinstance(ev, dict):
                        etype = ev.get("type")
                        
                        # User speech transcription
                        if etype == "conversation.item.input_audio_transcription.completed":
                            transcript = ev.get("transcript") or ""
                            if self.user_transcript_buffer:
                                user_text = ''.join(self.user_transcript_buffer).strip()
                                self.user_transcript_buffer.clear()
                            elif transcript:
                                user_text = transcript
                            else:
                                user_text = None
                            
                            if user_text:
                                print(f"[User] {user_text}")
                                self.speech_recognized.emit(user_text)
                            last_activity = time.time()
                        
                        # AI response transcription
                        elif etype == "response.audio_transcript.delta":
                            text = ev.get("delta") or ""
                            if text:
                                self.audio_transcript_buffer.append(text)
                        
                        elif etype == "response.audio_transcript.done":
                            if self.audio_transcript_buffer:
                                ai_text = ''.join(self.audio_transcript_buffer).strip()
                                self.audio_transcript_buffer.clear()
                                print(f"[AI] {ai_text}")
                                self.response_ready.emit(ai_text)
                            last_activity = time.time()
                        
                        # Response completed
                        elif etype == "response.done":
                            self.speaking_finished.emit()
                
                except asyncio.TimeoutError:
                    # if loop_iteration <= 5:
                    #     print(f"DEBUG: [Event loop] Timeout waiting for event (iteration {loop_iteration})")
                    # Check conversation timeout
                    if time.time() - last_activity > conversation_timeout:
                        print("Conversation timeout, returning to wake word detection")
                        break
                except Exception as e:
                    print(f"❌ [Event loop] Exception: {e}")
                    import traceback
                    traceback.print_exc()
                    break
        
        except Exception as e:
            print(f"Event loop error: {e}")
        
        finally:
            # Cleanup
            await self._stop_realtime()
    
    async def _stop_realtime(self):
        """Stop Realtime API session"""
        if self.local_peer:
            await self.local_peer.stop()
            self.local_peer = None
        
        if self.mic_track:
            self.mic_track.stop()
            self.mic_track = None
        
        self.in_conversation = False
        print("Realtime API session stopped")


# Backward compatibility
VoiceAssistantRAG = RealtimeVoiceAssistantRAG
VoiceAssistant = RealtimeVoiceAssistantRAG
