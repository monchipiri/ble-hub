from app.ble.models import BleAdvertisementEvent


def event_matches_conditions(event: BleAdvertisementEvent, conditions: dict) -> bool:
    address = conditions.get("device_address") or conditions.get("device_mac")
    if address and (event.device_address or "").lower() != str(address).lower():
        return False

    local_name_contains = conditions.get("local_name_contains")
    if local_name_contains:
        if not event.local_name or str(local_name_contains).lower() not in event.local_name.lower():
            return False

    rssi_gt = conditions.get("rssi_gt")
    if rssi_gt is not None:
        if event.rssi is None or event.rssi <= int(rssi_gt):
            return False

    rssi_lt = conditions.get("rssi_lt")
    if rssi_lt is not None:
        if event.rssi is None or event.rssi >= int(rssi_lt):
            return False

    service_uuid = conditions.get("service_uuid")
    if service_uuid:
        if str(service_uuid).lower() not in [uuid.lower() for uuid in event.service_uuids]:
            return False

    return True
