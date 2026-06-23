from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from app.ble.models import BleAdvertisementEvent


def parse_advertisement(device: BLEDevice, data: AdvertisementData) -> BleAdvertisementEvent:
    manufacturer_data = {
        str(company_id): value.hex() for company_id, value in data.manufacturer_data.items()
    }
    return BleAdvertisementEvent(
        device_address=device.address,
        local_name=data.local_name or device.name,
        rssi=data.rssi,
        service_uuids=list(data.service_uuids or []),
        manufacturer_data=manufacturer_data,
        payload={
            "tx_power": data.tx_power,
            "platform_data": [str(item) for item in data.platform_data],
        },
    )
