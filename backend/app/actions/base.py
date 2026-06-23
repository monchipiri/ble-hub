from typing import Protocol
from app.ble.models import BleAdvertisementEvent


class ActionHandler(Protocol):
    async def execute(self, event: BleAdvertisementEvent, params: dict) -> None: ...
