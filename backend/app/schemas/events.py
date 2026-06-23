from datetime import datetime
from pydantic import BaseModel


class EventOut(BaseModel):
    id: int
    source: str
    device_address: str | None
    local_name: str | None
    rssi: int | None
    service_uuids: list
    manufacturer_data: dict
    payload: dict
    created_at: datetime

    model_config = {"from_attributes": True}
