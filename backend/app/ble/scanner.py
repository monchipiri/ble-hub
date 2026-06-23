import asyncio
import logging
from bleak import BleakScanner
from app.ble.parsers import parse_advertisement
from app.core.config import get_settings
from app.services.event_dispatcher import dispatch_ble_event

logger = logging.getLogger(__name__)


class BleScannerService:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._scanner: BleakScanner | None = None

    async def start(self) -> None:
        logger.info("starting BLE scanner adapter=%s", self.settings.ble_scan_adapter)

        async def detection_callback(device, advertisement_data):
            event = parse_advertisement(device, advertisement_data)
            if event.rssi is not None and event.rssi < self.settings.ble_scan_rssi_min:
                return
            await dispatch_ble_event(event)

        self._scanner = BleakScanner(
            detection_callback=detection_callback,
            adapter=self.settings.ble_scan_adapter,
        )
        await self._scanner.start()

    async def stop(self) -> None:
        if self._scanner:
            await self._scanner.stop()
            logger.info("BLE scanner stopped")

    async def run_forever(self) -> None:
        await self.start()
        try:
            while True:
                await asyncio.sleep(3600)
        finally:
            await self.stop()
