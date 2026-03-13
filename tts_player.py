#!/usr/bin/env python3
import os
import subprocess
import tempfile
import threading
import time
from typing import Optional, Callable

def _load_config():
    d = {
        "api_key": None,
        "voice": "alloy",
        "model": "tts-1",
    }
    try:
        import config
        d["api_key"] = getattr(config, "OPENAI_API_KEY", None)
        d["voice"] = getattr(config, "TTS_VOICE", d["voice"])
        d["model"] = getattr(config, "TTS_MODEL", d["model"])
    except ImportError:
        d["api_key"] = os.environ.get("OPENAI_API_KEY")
    return d

_CONFIG = _load_config()

_ALSA_DEVICE_CACHE = None


def _get_alsa_device() -> str:
    global _ALSA_DEVICE_CACHE
    return _ALSA_DEVICE_CACHE if _ALSA_DEVICE_CACHE is not None else "default"


def _play_file(audio_path: str) -> bool:
    global _ALSA_DEVICE_CACHE
    candidates = [_ALSA_DEVICE_CACHE] if _ALSA_DEVICE_CACHE else ["default", "plughw:1,0", "plughw:0,0", "plughw:2,0"]
    for dev in candidates:
        try:
            if audio_path.endswith(".mp3"):
                cmd = ["mpg123", "-q", "-o", "alsa", "-a", dev, audio_path]
            else:
                cmd = ["aplay", "-q", "-D", dev, audio_path] if dev != "default" else ["aplay", "-q", audio_path]
            r = subprocess.run(cmd, capture_output=True, timeout=120, text=True)
            if r.returncode == 0:
                _ALSA_DEVICE_CACHE = dev
                return True
        except Exception:
            continue
    return False


def _text_to_speech_openai(text: str, voice: str = None, model: str = None) -> Optional[str]:
    api_key = _CONFIG["api_key"]
    if not api_key or not text or not text.strip():
        return None
    voice = voice or _CONFIG["voice"]
    model = model or _CONFIG["model"]
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        ts = int(time.time() * 1000)
        path = os.path.join(tempfile.gettempdir(), f"tts_{ts}.mp3")
        resp = client.audio.speech.create(model=model, voice=voice, input=text.strip())
        resp.stream_to_file(path)
        return path if os.path.isfile(path) and os.path.getsize(path) > 0 else None
    except Exception:
        return None


def _text_to_speech_espeak(text: str) -> Optional[str]:
    if not text or not text.strip():
        return None
    for bin_path in ["/usr/bin/espeak-ng", "/usr/bin/espeak"]:
        if not os.path.isfile(bin_path):
            continue
        try:
            fd, path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            r = subprocess.run(
                [bin_path, "-w", path, "-v", "en", text.strip()],
                capture_output=True,
                timeout=30,
            )
            if r.returncode == 0 and os.path.getsize(path) > 0:
                return path
            if os.path.exists(path):
                os.unlink(path)
        except Exception:
            if os.path.exists(path):
                try:
                    os.unlink(path)
                except OSError:
                    pass
    return None


def speak(text: str, voice: str = None) -> None:
    if not text or not (t := text.strip()):
        return
    path = None
    try:
        path = _text_to_speech_openai(t, voice=voice)
        if path:
            _play_file(path)
            return
        path = _text_to_speech_espeak(t)
        if path:
            _play_file(path)
    finally:
        if path and os.path.exists(path):
            try:
                os.unlink(path)
            except OSError:
                pass


def speak_async(text: str, voice: str = None, on_done: Optional[Callable[[], None]] = None) -> None:
    def _run():
        speak(text, voice=voice)
        if on_done:
            try:
                on_done()
            except Exception:
                pass
    t = threading.Thread(target=_run, daemon=True)
    t.start()
