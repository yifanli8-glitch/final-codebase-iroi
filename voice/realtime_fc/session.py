"""
RealtimeFCSession – Realtime API session with function calling.

Replaces the old record→Whisper→RAG→TTS loop with:
  Realtime audio stream → model decides tool calls → local execution → voice reply

Reuses existing infrastructure:
  - LocalPeer            (voice/local_peer.py)        – WebRTC + DataChannel
  - MicrophoneStreamArecord (voice/mic_stream_arecord.py) – arecord mic input
  - RAGRetriever         (voice/rag_retriever.py)     – embedding search
"""

import asyncio
import json
import os
import re
import sys
import threading
import time
from difflib import SequenceMatcher
from typing import List, Optional

from PyQt6.QtCore import QObject, pyqtSignal

# Ensure the voice/ directory is importable
_VOICE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _VOICE_DIR not in sys.path:
    sys.path.insert(0, _VOICE_DIR)

from local_peer import LocalPeer  # noqa: E402
from mic_stream_arecord import MicrophoneStreamArecord  # noqa: E402

from .tools import ALL_TOOLS, FC_INSTRUCTIONS, execute_image_analysis, execute_rag


class RealtimeFCSession(QObject):
    """
    Manages a single Realtime API session with function-calling tools.

    Signals (connect from UI thread):
        speech_recognized(str) – user's transcribed speech
        response_ready(str)    – model's text transcript (audio plays via WebRTC)
        error_occurred(str)    – fatal error
    """

    speech_recognized = pyqtSignal(str)
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    listening_changed = pyqtSignal(bool)  # True = mic open, False = mic muted

    def __init__(
        self,
        api_key: str,
        device_name: str,
        rag_retriever=None,
        instructions: str = "",
        use_tts_playback: bool = False,
    ):
        super().__init__()
        self.api_key = api_key
        self.device_name = device_name
        self.rag_retriever = rag_retriever
        self.instructions = instructions or FC_INSTRUCTIONS
        self.use_tts_playback = use_tts_playback

        self.pending_image_path: Optional[str] = None
        self.active = False
        self._item_ids: List[str] = []
        self._max_items = 20

        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._peer: Optional[LocalPeer] = None
        self._mic: Optional[MicrophoneStreamArecord] = None
        self._thread: Optional[threading.Thread] = None
        self._playback_task: Optional[asyncio.Task] = None
        self._response_active = False
        self._last_ai_text = ""
        self._last_ai_text_ts = 0.0
        self._echo_guard_window_sec = 6.0
        self._echo_guard_similarity = 0.9
        self._tts_playback_done = False
        self._response_done = False

    # ── public API ───────────────────────────────────────────────────────

    def start(self):
        """Start the session in a background thread."""
        if self.active:
            return
        self.active = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the session (safe to call from any thread)."""
        self.active = False
        if self._loop and self._peer:
            try:
                fut = asyncio.run_coroutine_threadsafe(
                    self._cleanup(), self._loop
                )
                fut.result(timeout=3)
            except Exception:
                pass
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=2)
        self._thread = None

    def unmute_mic(self):
        """Call when TTS playback has finished (use_tts_playback mode)."""
        if self._mic:
            self._mic.muted = False
        self.listening_changed.emit(True)

    def notify_tts_playback_finished(self):
        """Called by UI after local TTS playback (and delay) completes."""
        self._tts_playback_done = True
        if self._loop:
            self._loop.call_soon_threadsafe(self._try_unmute_tts_mode)
        else:
            self._try_unmute_tts_mode()

    def notify_image_uploaded(self, image_path: str):
        """Tell the session that the student uploaded a new image."""
        self.pending_image_path = image_path
        if self._loop and self._peer:
            asyncio.run_coroutine_threadsafe(
                self._inject_image_notification(), self._loop
            )

    # ── background thread entry ──────────────────────────────────────────

    def _run(self):
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._session())
        except Exception as e:
            print(f"❌ [FC Session] {e}")
            self.error_occurred.emit(str(e))
        finally:
            self._loop.close()
            self._loop = None
            self.active = False

    # ── core session ─────────────────────────────────────────────────────

    async def _session(self):
        try:
            await self._session_inner()
        finally:
            await self._cleanup()

    async def _session_inner(self):
        self._item_ids.clear()

        # ── 1. Build prompt payload (session creation endpoint) ────────
        # NOTE: tools/tool_choice must NOT be here — the session creation
        # endpoint rejects unknown fields. They are sent later via
        # session.update over the DataChannel.
        prompt_payload = {
            "model": "gpt-4o-realtime-preview",
            "modalities": ["text", "audio"],
            "voice": "alloy",
            "instructions": self.instructions,
            "input_audio_format": "pcm16",
            "output_audio_format": "pcm16",
            "input_audio_transcription": {"model": "whisper-1", "language": "en"},
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.3,
                "prefix_padding_ms": 300,
                "silence_duration_ms": 700,
            },
            "temperature": 0.8,
        }

        # ── 2. Microphone track ─────────────────────────────────────────
        self._mic = MicrophoneStreamArecord(
            mic_settings={
                "rate": 48000,
                "channels": 1,
                "chunk_size": 1024,
                "input_gain": 15.0,
                "minimum_volume": 0.0,
            },
            device_name=self.device_name,
            audio_stream=None,
        )

        # ── 3. WebRTC peer ──────────────────────────────────────────────
        self._peer = LocalPeer(
            api_key=self.api_key, prompt_payload=prompt_payload
        )
        await self._peer.start(add_audio=True, input_track=self._mic)
        await self._peer.send_offer()
        dc = await self._wait_dc(timeout=15)

        # ── 4. session.update (tools + config) ──────────────────────────
        dc.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "modalities": ["text", "audio"],
                        "voice": "alloy",
                        "instructions": self.instructions,
                        "input_audio_format": "pcm16",
                        "output_audio_format": "pcm16",
                        "input_audio_transcription": {"model": "whisper-1", "language": "en"},
                        "turn_detection": {
                            "type": "server_vad",
                            "threshold": 0.3,
                            "prefix_padding_ms": 300,
                            "silence_duration_ms": 700,
                        },
                        "tools": ALL_TOOLS,
                        "tool_choice": "required",
                    },
                }
            )
        )

        print("✅ [FC Session] Started (tools: search_knowledge_base, analyze_image)")

        # ── 5. Trigger initial greeting (skip tool calls for this one) ──
        dc.send(
            json.dumps(
                {
                    "type": "response.create",
                    "response": {
                        "modalities": ["text", "audio"],
                        "instructions": "Greet the student briefly in English, e.g. 'Hi! How can I help you today?'",
                        "tool_choice": "none",
                    },
                }
            )
        )

        # ── 6. Speaker output (skip if TTS playback; else consume WebRTC audio) ─
        if not self.use_tts_playback:
            self._playback_task = asyncio.create_task(self._play_remote_audio())

        # ── 7. Event loop ───────────────────────────────────────────────
        transcript_buf: List[str] = []
        pending_fc: List[dict] = []
        last_activity = time.time()

        while self.active:
            # read next event
            try:
                ev = await asyncio.wait_for(
                    self._peer.recv_event(timeout=1.0), timeout=2.0
                )
            except asyncio.TimeoutError:
                if time.time() - last_activity > 600:
                    print("[FC Session] 10-min silence timeout")
                    break
                continue
            except Exception as e:
                print(f"❌ [FC Session] Event error: {e}")
                break

            if not isinstance(ev, dict):
                continue

            etype = ev.get("type", "")

            # ── User speech transcript ──────────────────────────────────
            if etype == "conversation.item.input_audio_transcription.completed":
                text = (ev.get("transcript") or "").strip()
                if text:
                    if self._is_echo_transcript(text):
                        print(f"🛑 [EchoGuard] Dropped possible self-echo: {text[:120]}")
                    else:
                        print(f"👤 [User] {text}")
                        self.speech_recognized.emit(text)
                last_activity = time.time()

            # ── AI audio transcript (streaming) ─────────────────────────
            elif etype == "response.audio_transcript.delta":
                delta = ev.get("delta", "")
                if delta:
                    transcript_buf.append(delta)

            elif etype == "response.audio_transcript.done":
                if transcript_buf:
                    ai_text = "".join(transcript_buf).strip()
                    transcript_buf.clear()
                    if ai_text:
                        print(f"🤖 [AI] {ai_text}")
                        self._last_ai_text = ai_text
                        self._last_ai_text_ts = time.time()
                        self.response_ready.emit(ai_text)
                last_activity = time.time()

            # ── Function call arguments ready ───────────────────────────
            elif etype == "response.function_call_arguments.done":
                pending_fc.append(ev)

            # ── Track conversation items for pruning ─────────────────────
            elif etype == "conversation.item.created":
                item_id = ev.get("item", {}).get("id")
                if item_id:
                    self._item_ids.append(item_id)

            # ── Response finished → execute any pending function calls ──
            elif etype == "response.done":
                if pending_fc:
                    self._response_done = False
                    await self._handle_function_calls(pending_fc)
                    pending_fc.clear()
                else:
                    self._response_active = False
                    self._response_done = True
                    self._try_unmute_tts_mode()
                self._prune_old_items()
                last_activity = time.time()

            # ── Mute mic immediately when AI starts responding ──────────
            elif etype == "response.created":
                self._response_active = True
                self._response_done = False
                self._tts_playback_done = False
                if self._mic and not self._mic.muted:
                    self._mic.muted = True
                    self.listening_changed.emit(False)

            # ── Session config acknowledged ─────────────────────────────
            elif etype == "session.updated":
                tools = ev.get("session", {}).get("tools", [])
                names = [t.get("name", "?") for t in tools]
                print(f"✅ [FC] Config accepted (tools: {', '.join(names)})")

            elif etype == "error":
                msg = ev.get("error", {}).get("message", str(ev))
                print(f"⚠️ [FC] Server error: {msg}")

    # ── conversation pruning ─────────────────────────────────────────────

    def _prune_old_items(self):
        """Delete oldest conversation items when history exceeds _max_items."""
        dc = self._peer.data_channel if self._peer else None
        if not dc or dc.readyState != "open":
            return
        while len(self._item_ids) > self._max_items:
            old_id = self._item_ids.pop(0)
            dc.send(json.dumps({"type": "conversation.item.delete", "item_id": old_id}))

    def _normalize_text(self, text: str) -> str:
        text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
        return " ".join(text.split())

    def _is_echo_transcript(self, user_text: str) -> bool:
        """Filter likely self-echo transcripts in realtime_tts mode."""
        if not self.use_tts_playback:
            return False
        if not self._last_ai_text:
            return False
        if time.time() - self._last_ai_text_ts > self._echo_guard_window_sec:
            return False

        u = self._normalize_text(user_text)
        a = self._normalize_text(self._last_ai_text)
        if not u or not a:
            return False

        # Fast path for obvious replay.
        if len(u) >= 20 and (u in a or a in u):
            return True

        return SequenceMatcher(None, u, a).ratio() >= self._echo_guard_similarity

    def _try_unmute_tts_mode(self):
        """Unmute only when both TTS and model response are finished."""
        if not self.use_tts_playback:
            return
        if not self._tts_playback_done or not self._response_done or self._response_active:
            return
        if self._mic and self._mic.muted:
            self._mic.muted = False
            self.listening_changed.emit(True)

    # ── function call handling ───────────────────────────────────────────

    async def _handle_function_calls(self, calls: List[dict]):
        """Execute all pending function calls, send results, then ONE response.create."""
        dc = self._peer.data_channel if self._peer else None
        if not dc or dc.readyState != "open":
            return

        loop = asyncio.get_event_loop()

        for ev in calls:
            call_id = ev.get("call_id", "")
            name = ev.get("name", "")
            item_id = ev.get("item_id", "")
            args_str = ev.get("arguments", "{}")

            print(f"🔧 [FC] {name}({args_str[:120]})")

            try:
                args = json.loads(args_str)
            except json.JSONDecodeError:
                args = {}

            if name == "search_knowledge_base":
                result = await loop.run_in_executor(
                    None, execute_rag, args.get("query", ""), self.rag_retriever
                )
            elif name == "analyze_image":
                result = await loop.run_in_executor(
                    None,
                    execute_image_analysis,
                    args.get("question", "Analyze this image"),
                    self.pending_image_path,
                    self.api_key,
                )
            else:
                result = f"Unknown tool: {name}"

            print(f"🔧 [FC] Result ({len(result)} chars)")

            create_ev = {
                "type": "conversation.item.create",
                "item": {
                    "type": "function_call_output",
                    "call_id": call_id,
                    "output": result,
                },
            }
            if item_id:
                create_ev["previous_item_id"] = item_id

            dc.send(json.dumps(create_ev))

        # Generate answer using the tool results — skip further tool calls
        dc.send(json.dumps({
            "type": "response.create",
            "response": {"tool_choice": "none"},
        }))

    # ── speaker output ──────────────────────────────────────────────────

    async def _play_remote_audio(self):
        """Subscribe to remote audio distributor and play via aplay."""
        import subprocess

        from av import AudioResampler

        # Wait for the remote audio track to arrive
        for _ in range(100):
            if not self.active:
                return
            if self._peer and self._peer.remote_audio_distributor:
                break
            await asyncio.sleep(0.1)
        else:
            print("⚠️ [FC] No remote audio track received")
            return

        import queue as queue_module
        import numpy as np

        q = self._peer.remote_audio_distributor.subscribe()
        RATE = 48000
        resampler = AudioResampler(format="s16", layout="mono", rate=RATE)
        play_queue = queue_module.Queue(maxsize=60)
        proc = None
        last_speech = 0.0

        def playback_writer():
            nonlocal proc
            while self.active:
                try:
                    pcm = play_queue.get(timeout=0.5)
                except queue_module.Empty:
                    continue
                if pcm is None:
                    break
                if proc is None:
                    proc = subprocess.Popen(
                        [
                            "aplay", "-D", "plughw:1,0",
                            "-f", "S16_LE", "-r", str(RATE),
                            "-c", "1", "-t", "raw", "-q",
                            "-B", "400000",
                        ],
                        stdin=subprocess.PIPE,
                    )
                    print(f"🔊 [FC] Speaker: {RATE}Hz mono (aplay plughw:1,0, 400ms buf)")
                try:
                    proc.stdin.write(pcm)
                except BrokenPipeError:
                    break

        writer_thread = threading.Thread(target=playback_writer, daemon=True)
        writer_thread.start()

        try:
            while self.active:
                try:
                    frame = await asyncio.wait_for(q.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                if frame is None:
                    play_queue.put(None)
                    break
                for converted in resampler.resample(frame):
                    pcm = bytes(converted.planes[0])
                    level = np.abs(np.frombuffer(pcm, dtype=np.int16)).mean()
                    if level > 200:
                        last_speech = time.time()
                    elif (
                        last_speech > 0
                        and not self._response_active
                        and self._mic
                        and self._mic.muted
                        and time.time() - last_speech > 0.8
                    ):
                        self._mic.muted = False
                        self.listening_changed.emit(True)
                        print(f"🔈 [FC] Mic unmuted ({time.time()-last_speech:.1f}s silence)")
                    try:
                        play_queue.put_nowait(pcm)
                    except queue_module.Full:
                        pass
            play_queue.put(None)
        except asyncio.CancelledError:
            play_queue.put(None)
        except Exception as e:
            print(f"❌ [FC] Playback error: {e}")
            play_queue.put(None)
        finally:
            try:
                play_queue.put(None)
            except Exception:
                pass
            if writer_thread.is_alive():
                writer_thread.join(timeout=3)
            if proc:
                try:
                    proc.stdin.close()
                except Exception:
                    pass
                proc.wait(timeout=2)

    # ── helpers ──────────────────────────────────────────────────────────

    async def _inject_image_notification(self):
        """Insert a user-text item so the model knows an image was uploaded."""
        dc = self._peer.data_channel if self._peer else None
        if not dc or dc.readyState != "open":
            return
        dc.send(
            json.dumps(
                {
                    "type": "conversation.item.create",
                    "item": {
                        "type": "message",
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "I just uploaded a lab diagram image. "
                                    "First, briefly confirm you received the image "
                                    "and ask what I want to know about it, then wait "
                                    "for my question."
                                ),
                            }
                        ],
                    },
                }
            )
        )
        dc.send(json.dumps({"type": "response.create"}))

    async def _wait_dc(self, timeout: float = 15) -> object:
        """Wait for the DataChannel to reach 'open' state."""
        t0 = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - t0 < timeout:
            dc = self._peer.data_channel if self._peer else None
            if dc and dc.readyState == "open":
                return dc
            await asyncio.sleep(0.5)
        raise RuntimeError("DataChannel did not open within timeout")

    async def _cleanup(self):
        self.active = False
        if self._playback_task and not self._playback_task.done():
            self._playback_task.cancel()
            try:
                await self._playback_task
            except (asyncio.CancelledError, Exception):
                pass
            self._playback_task = None
        if self._peer:
            await self._peer.stop()
            self._peer = None
        if self._mic and hasattr(self._mic, "stop"):
            try:
                self._mic.stop()
            except Exception:
                pass
            self._mic = None
        print("[FC Session] Stopped")
