import logging
from app.ble.models import BleAdvertisementEvent

logger = logging.getLogger(__name__)


class LogActivityAction:
    async def execute(self, event: BleAdvertisementEvent, params: dict) -> None:
        activity = params.get("activity", "ble_event")
        logger.info("activity=%s address=%s rssi=%s", activity, event.device_address, event.rssi)
