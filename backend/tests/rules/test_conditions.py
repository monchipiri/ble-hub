from app.rules.conditions import matches

def test_rssi_match():
    event={'rssi':-60}
    condition={'rssi_gt':-70}
    assert matches(event, condition)
