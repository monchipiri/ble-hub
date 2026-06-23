from app.ble.parsers import parse_advertisement

def test_parse_advertisement():
    raw={'address':'AA:BB:CC','rssi':-60}
    parsed=parse_advertisement(raw)
    assert parsed['device_mac']=='AA:BB:CC'
