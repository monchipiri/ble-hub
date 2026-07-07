from collections.abc import Mapping
from typing import Any

from app.ble.models import BleAdvertisementEvent


def _event_value(event: BleAdvertisementEvent | Mapping[str, Any], key: str) -> Any:
    if isinstance(event, Mapping):
        if key == "device_address":
            return event.get("device_address") or event.get("device_mac")
        return event.get(key)
    return getattr(event, key)


def _condition_int(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def event_matches_conditions(event: BleAdvertisementEvent | Mapping[str, Any], conditions: dict) -> bool:
    address = conditions.get("device_address") or conditions.get("device_mac")
    event_address = _event_value(event, "device_address")
    if address and (event_address or "").lower() != str(address).lower():
        return False

    local_name_contains = conditions.get("local_name_contains")
    if local_name_contains:
        local_name = _event_value(event, "local_name")
        if not local_name or str(local_name_contains).lower() not in str(local_name).lower():
            return False

    rssi_gt = conditions.get("rssi_gt")
    if rssi_gt is not None:
        threshold = _condition_int(rssi_gt)
        event_rssi = _event_value(event, "rssi")
        if threshold is None or event_rssi is None or event_rssi <= threshold:
            return False

    rssi_lt = conditions.get("rssi_lt")
    if rssi_lt is not None:
        threshold = _condition_int(rssi_lt)
        event_rssi = _event_value(event, "rssi")
        if threshold is None or event_rssi is None or event_rssi >= threshold:
            return False

    service_uuid = conditions.get("service_uuid")
    if service_uuid:
        service_uuids = _event_value(event, "service_uuids") or []
        if str(service_uuid).lower() not in [str(uuid).lower() for uuid in service_uuids]:
            return False

    return True


def matches(event: BleAdvertisementEvent | Mapping[str, Any], conditions: dict) -> bool:
    return event_matches_conditions(event, conditions)
