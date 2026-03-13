import asyncio
import aiohttp
import json
import time
import logging
from typing import Any, Dict, Optional

from aiortc import (
    MediaStreamTrack,
    RTCConfiguration,
    RTCIceServer,
    RTCPeerConnection,
    RTCSessionDescription,
)

from audio_distributor import AudioDistributor

logger = logging.getLogger("local_peer")


class LocalPeer:
    """
    Minimal WebRTC client to connect microphone track to OpenAI Realtime
    and receive remote audio + events via data channel.
    """

    def __init__(self, api_key: str, prompt_payload: dict):
        self.api_key = api_key
        self.prompt_payload = prompt_payload
        self.pc: Optional[RTCPeerConnection] = None
        self.mic_track: Optional[MediaStreamTrack] = None
        self.session_id: Optional[str] = None
        self.ephemeral_key: Optional[str] = None
        self.data_channel = None
        self.remote_audio_distributor: Optional[AudioDistributor] = None
        self._events: asyncio.Queue[Dict[str, Any]] = asyncio.Queue()
        self._last_input_committed_at: Optional[float] = None
        self._last_item_added_at: Optional[float] = None
        self._last_latency_input_to_item: Optional[float] = None
        self._last_latency_item_to_output_started: Optional[float] = None

    async def create_session(self):
        payload = self.prompt_payload
        url = "https://api.openai.com/v1/realtime/sessions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        logger.info("requesting session from openai")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    raise RuntimeError(
                        f"Could not create session: {resp.status}, {text}"
                    )
                data = await resp.json()
        self.session_id = data.get("id")
        self.ephemeral_key = data.get("client_secret", {}).get("value")
        if self.session_id is None or self.ephemeral_key is None:
            raise RuntimeError("Session creation did not return session_id or key")
        logger.info("Session created: id=%s", self.session_id)

    async def setup_peer(
        self, add_audio: bool = False, input_track: MediaStreamTrack = None
    ):
        ice_servers = [RTCIceServer(urls=["stun:stun.l.google.com:19302"])]
        config = RTCConfiguration(iceServers=ice_servers)
        self.pc = RTCPeerConnection(configuration=config)
        self.mic_track = input_track

        @self.pc.on("iceconnectionstatechange")
        def on_iceconnectionstatechange():
            logger.info("ICE connection state: %s", self.pc.iceConnectionState)

        @self.pc.on("icecandidate")
        def on_icecandidate(event):
            if event.candidate:
                logger.debug("Local ICE candidate: %s", event.candidate)
            else:
                logger.info("ICE gathering complete")

        @self.pc.on("connectionstatechange")
        def on_connectionstatechange():
            logger.info("Connection state: %s", self.pc.connectionState)

        @self.pc.on("track")
        async def on_track(track: MediaStreamTrack):
            logger.info("Got remote track: %s", track.kind)
            if track.kind == "audio":
                self.remote_audio_distributor = AudioDistributor(track)
                await self.remote_audio_distributor.start()
                logger.info("Remote audio distributor started")

        self.data_channel = self.pc.createDataChannel("oai-events")
        
        @self.data_channel.on("open")
        def on_datachannel_open():
            logger.info("DataChannel opened")
        
        @self.data_channel.on("close")
        def on_datachannel_close():
            logger.warning("DataChannel closed")

        @self.data_channel.on("message")
        def on_our_channel_message(msg):
            try:
                data = json.loads(msg)
            except Exception:
                data = None
            now = time.time()
            if isinstance(data, dict):
                etype = data.get("type")
                if etype == "input_audio_buffer.committed":
                    self._last_input_committed_at = now
                    self._last_item_added_at = None
                elif etype == "conversation.item.added":
                    self._last_item_added_at = now
                    if self._last_input_committed_at is not None:
                        latency = now - self._last_input_committed_at
                        self._last_latency_input_to_item = latency
                        logger.info("Latency committed→item: %.3fs", latency)
                elif etype == "output_audio_buffer.started":
                    if self._last_item_added_at is not None:
                        latency2 = now - self._last_item_added_at
                        self._last_latency_item_to_output_started = latency2
                        logger.info("Latency item→output_start: %.3fs", latency2)
            payload = data if data is not None else {"raw": msg}
            asyncio.create_task(self._events.put(payload))

        if add_audio:
            self.pc.addTrack(input_track)

        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        logger.info("Local SDP offer created")

    async def send_offer(self):
        if self.pc is None or self.pc.localDescription is None:
            raise RuntimeError("PeerConnection or localDescription not ready")
        
        model = self.prompt_payload.get("model", "gpt-4o-realtime-preview")
        url = f"https://api.openai.com/v1/realtime?model={model}"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                data=self.pc.localDescription.sdp,
                headers={
                    "Authorization": f"Bearer {self.ephemeral_key}",
                    "Content-Type": "application/sdp",
                    "OpenAI-Beta": "realtime=v1",
                },
            ) as response:
                text = await response.text()
                if response.status not in (200, 201):
                    raise RuntimeError(f"Offer post failed: {response.status}, {text}")
                if text is None or text == "":
                    raise RuntimeError("Answer SDP missing from response")
                answer = RTCSessionDescription(sdp=text, type="answer")
                await self.pc.setRemoteDescription(answer)
        logger.info("Remote SDP answer set")

    async def start(self, add_audio: bool = False, input_track: MediaStreamTrack = None):
        # 1. First create session (get ephemeral key)
        await self.create_session()
        
        # 2. Setup WebRTC peer
        await self.setup_peer(add_audio=add_audio, input_track=input_track)
        
        logger.info("WebRTC setup complete, ready to connect")
        asyncio.create_task(self.monitor_audio_stall_and_track())
    
    async def _wait_for_datachannel(self, timeout: float = 10.0):
        start = time.time()
        while time.time() - start < timeout:
            if self.data_channel and self.data_channel.readyState == "open":
                logger.info("DataChannel is open")
                return
            await asyncio.sleep(0.1)
        raise RuntimeError("DataChannel did not open in time")
    
    async def _configure_session(self):
        if not self.data_channel or self.data_channel.readyState != "open":
            logger.warning("DataChannel not open, skipping session config")
            return
        
        # Send session.update event to configure the session
        config_event = {
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",
                "instructions": "You are a helpful assistant. Please respond naturally and conversationally.",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "input_audio_transcription": {
                    "model": "whisper-1"
                },
                "turn_detection": {
                    "type": "server_vad",
                    "threshold": 0.5,
                    "prefix_padding_ms": 300,
                    "silence_duration_ms": 500
                },
                "temperature": 0.8
            }
        }
        
        self.data_channel.send(json.dumps(config_event))
        logger.info("Session configuration sent")

    async def stop(self):
        if self.mic_track and hasattr(self.mic_track, "stop"):
            self.mic_track.stop()
        if self.pc:
            await self.pc.close()

    def peer_is_ready(self) -> bool:
        return self.data_channel is not None

    def send_text_sync(self, text: str, role: str = "user", call_id: str = None):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running():
            # schedule on the existing loop
            asyncio.create_task(self.send_text(text=text, role=role, call_id=call_id))
        else:
            asyncio.run(self.send_text(text=text, role=role, call_id=call_id))

    async def send_text(self, text: str, role: str = "user", call_id: str = None):
        if not self.data_channel:
            raise RuntimeError("Data channel not ready")
        event = {"type": "conversation.item.create", "item": {}}
        if call_id:
            event["item"]["call_id"] = str(call_id)
            event["item"]["output"] = str(text)
            event["item"]["type"] = "function_call_output"
        else:
            event["item"]["content"] = [{"type": "input_text", "text": str(text)}]
            event["item"]["type"] = "message"
            event["item"]["role"] = role
        self.data_channel.send(json.dumps(event))
        self.data_channel.send(json.dumps({"type": "response.create"}))

    async def recv_event(self, timeout: Optional[float] = None) -> Dict[str, Any]:
        if timeout is None:
            return await self._events.get()
        return await asyncio.wait_for(self._events.get(), timeout=timeout)

    async def monitor_audio_stall_and_track(self):
        last_bytes_sent = 0
        while True:
            if not self.pc:
                await asyncio.sleep(2)
                continue
            output: str = ""
            stats = await self.pc.getStats()
            for report in stats.values():
                if report.type == "outbound-rtp" and report.kind == "audio":
                    if report.bytesSent == last_bytes_sent:
                        output += "⚠️ No new audio bytes sent — possible stall\n"
                    else:
                        output += f"✅ Audio bytes sent: {report.bytesSent}\n"
                    last_bytes_sent = report.bytesSent % 1000000
                elif report.type == "remote-inbound-rtp" and report.kind == "audio":
                    rtt = report.roundTripTime
                    output += f"RTT: {rtt} s\n"
            if output:
                logger.info(output.strip())
            await asyncio.sleep(2)
