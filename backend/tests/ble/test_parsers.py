from types import SimpleNamespace

from app.ble.parsers import parse_advertisement


def test_parse_advertisement():
    device = SimpleNamespace(address="AA:BB:CC", name="Tracker")
    data = SimpleNamespace(
        local_name=None,
        rssi=-60,
        service_uuids=["180f"],
        manufacturer_data={76: b"\x01\x02"},
        tx_power=-12,
        platform_data=("raw",),
    )

    parsed = parse_advertisement(device, data)

    assert parsed.device_address == "AA:BB:CC"
    assert parsed.local_name == "Tracker"
    assert parsed.rssi == -60
    assert parsed.service_uuids == ["180f"]
    assert parsed.manufacturer_data == {"76": "0102"}
