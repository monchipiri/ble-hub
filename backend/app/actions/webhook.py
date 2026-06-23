import logging
from app.ble.models import BleAdvertisementEvent

logger = logging.getLogger(__name__)


class WebhookAction:
    async def execute(self, event: BleAdvertisementEvent, params: dict) -> None:
        # MVP placeholder. Later: use httpx.AsyncClient with retries and timeouts.
        logger.info("webhook placeholder url=%s event=%s", params.get("url"), event.model_dump())
