from app.ble.models import BleAdvertisementEvent
from app.rules.conditions import event_matches_conditions


def test_rule_matches_address_and_rssi():
    event = BleAdvertisementEvent(device_address="AA:BB", rssi=-60, local_name="Band")
    assert event_matches_conditions(event, {"device_address": "AA:BB", "rssi_gt": -70})


def test_rule_rejects_weak_rssi():
    event = BleAdvertisementEvent(device_address="AA:BB", rssi=-90, local_name="Band")
    assert not event_matches_conditions(event, {"device_address": "AA:BB", "rssi_gt": -70})
