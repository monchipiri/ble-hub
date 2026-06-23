from datetime import datetime, timezone
from pydantic import BaseModel, Field


class BleAdvertisementEvent(BaseModel):
    source: str = "ble_scan"
    device_address: str | None = None
    local_name: str | None = None
    rssi: int | None = None
    service_uuids: list[str] = Field(default_factory=list)
    manufacturer_data: dict[str, str] = Field(default_factory=dict)
    payload: dict = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
