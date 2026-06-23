from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.ble.models import BleAdvertisementEvent
from app.db.models import BleEvent, Device


async def store_ble_event(session: AsyncSession, event: BleAdvertisementEvent) -> BleEvent:
    db_event = BleEvent(
        source=event.source,
        device_address=event.device_address,
        local_name=event.local_name,
        rssi=event.rssi,
        service_uuids=event.service_uuids,
        manufacturer_data=event.manufacturer_data,
        payload=event.payload,
        created_at=event.created_at,
    )
    session.add(db_event)

    if event.device_address:
        result = await session.execute(select(Device).where(Device.address == event.device_address))
        device = result.scalar_one_or_none()
        now = datetime.now(timezone.utc)
        if device is None:
            device = Device(
                address=event.device_address,
                name=event.local_name,
                last_rssi=event.rssi,
                last_seen_at=now,
            )
            session.add(device)
        else:
            device.name = event.local_name or device.name
            device.last_rssi = event.rssi
            device.last_seen_at = now

    await session.commit()
    await session.refresh(db_event)
    return db_event
