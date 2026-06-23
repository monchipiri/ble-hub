from pydantic import BaseModel, Field


class RuleCreate(BaseModel):
    name: str
    enabled: bool = True
    conditions: dict = Field(default_factory=dict)
    actions: list[dict] = Field(default_factory=list)


class RulePatch(BaseModel):
    name: str | None = None
    enabled: bool | None = None
    conditions: dict | None = None
    actions: list[dict] | None = None


class RuleOut(BaseModel):
    id: int
    name: str
    enabled: bool
    conditions: dict
    actions: list[dict]

    model_config = {"from_attributes": True}
