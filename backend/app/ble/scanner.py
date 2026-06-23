import asyncio
import logging
import time

from bleak import BleakScanner

from app.ble.models import BleAdvertisementEvent
from app.ble.parsers import parse_advertisement
from app.core.config import get_settings
from app.services.event_dispatcher import dispatch_ble_event

logger = logging.getLogger(__name__)


class BleScannerService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._scanner: BleakScanner | None = None
        self._queue: asyncio.Queue[BleAdvertisementEvent] = asyncio.Queue(maxsize=1000)
        self._worker_task: asyncio.Task | None = None

        # Evita guardar decenas de anuncios BLE iguales por segundo.
        # Guarda como máximo 1 evento por dispositivo cada X segundos.
        self._last_seen_by_device: dict[str, float] = {}
        self._dedupe_seconds = 5

    async def start(self) -> None:
        logger.info("starting BLE scanner adapter=%s", self.settings.ble_scan_adapter)

        self._worker_task = asyncio.create_task(self._worker())

        def detection_callback(device, advertisement_data) -> None:
            event = parse_advertisement(device, advertisement_data)

            if event.rssi is not None and event.rssi < self.settings.ble_scan_rssi_min:
                return

            now = time.monotonic()
            last_seen = self._last_seen_by_device.get(event.device_address)

            if last_seen is not None and now - last_seen < self._dedupe_seconds:
                return

            self._last_seen_by_device[event.device_address] = now

            try:
                self._queue.put_nowait(event)
            except asyncio.QueueFull:
                logger.warning(
                    "BLE event queue full; dropping event device=%s",
                    event.device_address,
                )

        self._scanner = BleakScanner(
            detection_callback=detection_callback,
            adapter=self.settings.ble_scan_adapter,
        )

        await self._scanner.start()

    async def stop(self) -> None:
        if self._scanner:
            await self._scanner.stop()
            logger.info("BLE scanner stopped")

        if self._worker_task:
            self._worker_task.cancel()

    async def run_forever(self) -> None:
        await self.start()
        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            await self.stop()

    async def _worker(self) -> None:
        while True:
            event = await self._queue.get()
            try:
                await dispatch_ble_event(event)
            except Exception:
                logger.exception(
                    "error processing BLE event device=%s",
                    event.device_address,
                )
            finally:
                self._queue.task_done()
