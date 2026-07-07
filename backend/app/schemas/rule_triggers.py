from datetime import datetime

from pydantic import BaseModel


class RuleTriggerOut(BaseModel):
    id: int
    rule_id: int
    rule_name: str
    device_address: str | None
    local_name: str | None
    rssi: int | None
    actions: list[dict]
    payload: dict
    created_at: datetime

    model_config = {"from_attributes": True}
