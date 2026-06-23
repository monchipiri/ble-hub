from datetime import datetime
from pydantic import BaseModel


class DeviceOut(BaseModel):
    id: int
    address: str
    name: str | None
    device_type: str | None
    notes: str | None
    last_rssi: int | None
    last_seen_at: datetime | None

    model_config = {"from_attributes": True}
