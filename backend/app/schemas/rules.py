from datetime import datetime

from pydantic import BaseModel, Field


class RuleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    enabled: bool = True
    conditions: dict = Field(default_factory=dict)
    actions: list[dict] = Field(default_factory=list)


class RulePatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    enabled: bool | None = None
    conditions: dict | None = None
    actions: list[dict] | None = None


class RuleOut(BaseModel):
    id: int
    name: str
    enabled: bool
    conditions: dict
    actions: list[dict]
    created_at: datetime

    model_config = {"from_attributes": True}
