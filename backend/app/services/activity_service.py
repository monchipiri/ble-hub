from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.ble.models import BleAdvertisementEvent
from app.db.models import BleEvent, Device


async def store_ble_event(session: AsyncSession, event: BleAdvertisementEvent) -> BleEvent:
    now = datetime.now(timezone.utc)

    db_event = BleEvent(
        source=event.source,
        device_address=event.device_address,
        local_name=event.local_name,
        rssi=event.rssi,
        service_uuids=event.service_uuids,
        manufacturer_data=event.manufacturer_data,
        payload=event.payload,
        created_at=now,
    )
    session.add(db_event)

    if not event.device_address:
        return db_event

    result = await session.execute(select(Device).where(Device.address == event.device_address))
    device = result.scalar_one_or_none()

    if device is None:
        session.add(
            Device(
                address=event.device_address,
                name=event.local_name,
                last_rssi=event.rssi,
                last_seen_at=now,
                created_at=now,
            )
        )
    else:
        if event.local_name:
            device.name = event.local_name
        device.last_rssi = event.rssi
        device.last_seen_at = now

    return db_event
