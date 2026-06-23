from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone

from app.db.models import BleEvent, Device


async def store_ble_event(session, event) -> None:
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

    stmt = insert(Device).values(
        address=event.device_address,
        name=event.local_name,
        last_rssi=event.rssi,
        last_seen_at=now,
        created_at=now,
    ).on_conflict_do_update(
        index_elements=["address"],
        set_={
            "name": event.local_name,
            "last_rssi": event.rssi,
            "last_seen_at": now,
        },
    )

    await session.execute(stmt)
    await session.commit()
