import asyncio
from aiortc import MediaStreamTrack
from av import AudioFrame
import logging

logger = logging.getLogger("audio_distributor")


class AudioDistributor:
    """
    Fan-out audio frames from a single MediaStreamTrack to multiple subscribers.
    Each subscriber gets an asyncio.Queue of AudioFrame objects.
    """

    def __init__(self, source_track: MediaStreamTrack, queue_size: int = 10):
        self.source_track = source_track
        self.subscribers: list[asyncio.Queue] = []
        self.queue_size = queue_size
        self._task = None
        self._stopped = asyncio.Event()

    def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue[AudioFrame] = asyncio.Queue(maxsize=self.queue_size)
        self.subscribers.append(q)
        return q

    async def start(self):
        if self._task is not None:
            return
        self._stopped.clear()
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        self._stopped.set()
        if self._task:
            await self._task
        for q in self.subscribers:
            q.put_nowait(None)

    async def _run(self):
        try:
            while not self._stopped.is_set():
                frame = await self.source_track.recv()
                for q in list(self.subscribers):
                    try:
                        q.put_nowait(frame)
                    except asyncio.QueueFull:
                        pass
        except Exception as e:
            logger.error("audio distributor stopped: %s", e)
        finally:
            self._stopped.set()
