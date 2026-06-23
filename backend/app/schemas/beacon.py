from pydantic import BaseModel, Field


class BeaconStartRequest(BaseModel):
    payload: dict = Field(default_factory=dict)
