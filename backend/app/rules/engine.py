from collections.abc import Mapping
from typing import Any

from app.ble.models import BleAdvertisementEvent
from app.rules.conditions import event_matches_conditions


def evaluate_rule(event: BleAdvertisementEvent | Mapping[str, Any], rule: Mapping[str, Any]) -> bool:
    conditions = rule.get("conditions", {})
    if not isinstance(conditions, dict):
        return False
    return event_matches_conditions(event, conditions)
