from app.rules.conditions import matches


def test_rssi_match():
    event = {"rssi": -60}
    condition = {"rssi_gt": -70}
    assert matches(event, condition)


def test_invalid_numeric_condition_does_not_match():
    event = {"rssi": -60}
    condition = {"rssi_gt": "near"}
    assert not matches(event, condition)
