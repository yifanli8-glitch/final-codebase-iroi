import asyncio
import queue
import threading
import subprocess
import time
from fractions import Fraction
from typing import Optional
import os
import signal

import numpy as np
from aiortc import MediaStreamTrack
from av import AudioFrame


class MicrophoneStreamArecord(MediaStreamTrack):

    kind = "audio"

    def __init__(
        self,
        mic_settings: dict,
        device_name: str = "hw:2,0",
        audio_stream=None,
    ):
        super().__init__()
        self.chunk_size = mic_settings["chunk_size"]
        self.channels = mic_settings["channels"]
        self.rate = mic_settings["rate"]
        self.gain = mic_settings.get("input_gain", 1.0)
        self.mute_threshold = mic_settings.get("minimum_volume", 0.005)
        self.device_name = device_name

        self.audio_stream = audio_stream
        self.muted = False

        self._stop_event = threading.Event()
        self._process = None
        self.q = queue.Queue()
        self._timestamp = 0

        self._start_arecord()
        self._start_audio_thread()

    def _start_arecord(self):
        cmd = [
            'arecord',
            '-D', self.device_name,
            '-f', 'S16_LE',  # 16-bit PCM
            '-r', str(self.rate),
            '-c', str(self.channels),
            '-t', 'raw',
            '--'
        ]
        
        try:
            preexec_fn = os.setsid
        except AttributeError:
            preexec_fn = None

        self._process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            preexec_fn=preexec_fn,
        )
        print(f"✅ arecord ，: {self.device_name}")

    def _start_audio_thread(self):
        def audio_capture():
            bytes_per_chunk = self.chunk_size * self.channels * 2
            
            while not self._stop_event.is_set():
                if self._process is None or self._process.poll() is not None:
                    break
                try:
                    raw_data = self._process.stdout.read(bytes_per_chunk)
                    if not raw_data:
                        break
                    
                    data = self.process_pcm(raw_data)
                    self.q.put(data)
                except Exception as e:
                    print(f"❌ : {e}")
                    break
                time.sleep(0.001)

        threading.Thread(target=audio_capture, daemon=True).start()

    def low_amplitude_mute(self, pcm: np.ndarray, threshold: float = 0.005) -> np.ndarray:
        if len(pcm) == 0:
            return pcm
        pcm_float = pcm.astype(np.float32) / 32768.0
        rms = np.sqrt(np.mean(pcm_float**2))
        if rms < threshold:
            pcm[:] = 0
        return pcm

    def process_pcm(self, raw_data: bytes) -> bytes:
        if self.muted:
            return b"\x00" * len(raw_data)

        pcm = np.frombuffer(raw_data, dtype=np.int16).copy()
        
        pcm = self.low_amplitude_mute(pcm, self.mute_threshold)
        
        pcm = pcm * self.gain
        pcm = np.clip(pcm, -32768, 32767).astype(np.int16)
        
        return pcm.tobytes()

    async def recv(self) -> AudioFrame:
        loop = asyncio.get_running_loop()
        data = await loop.run_in_executor(None, self.q.get)

        frame = AudioFrame(
            format="s16",
            layout="mono" if self.channels == 1 else "stereo",
            samples=self.chunk_size,
        )
        frame.sample_rate = self.rate
        frame.planes[0].update(data)
        frame.pts = self._timestamp
        frame.time_base = Fraction(1, self.rate)
        self._timestamp += self.chunk_size
        return frame

    def stop(self):
        self._stop_event.set()
        
        if self._process is not None:
            try:
                try:
                    os.killpg(os.getpgid(self._process.pid), signal.SIGTERM)
                except:
                    self._process.terminate()
                
                self._process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait()
            except Exception as e:
                print(f"⚠️  arecord : {e}")
            finally:
                self._process = None
        
        print("✅ arecord ")
