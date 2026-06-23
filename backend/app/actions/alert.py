import logging
from app.ble.models import BleAdvertisementEvent

logger = logging.getLogger(__name__)


class AlertAction:
    async def execute(self, event: BleAdvertisementEvent, params: dict) -> None:
        logger.warning("alert=%s address=%s rssi=%s", params.get("message", "BLE alert"), event.device_address, event.rssi)
