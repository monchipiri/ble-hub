from sqlalchemy import select

from app.ble.models import BleAdvertisementEvent
from app.db.models import BleEvent, Device, Rule, RuleTrigger
from app.db.session import AsyncSessionLocal
from app.services.event_dispatcher import dispatch_ble_event


async def test_dispatch_stores_event_device_and_rule_trigger():
    async with AsyncSessionLocal() as session:
        session.add(
            Rule(
                name="Band nearby",
                enabled=True,
                conditions={"device_address": "AA:BB:CC", "rssi_gt": -70},
                actions=[{"type": "log_activity", "params": {"activity": "nearby"}}],
            )
        )
        await session.commit()

    event = BleAdvertisementEvent(
        device_address="AA:BB:CC",
        local_name="Band",
        rssi=-55,
        service_uuids=["180f"],
    )

    await dispatch_ble_event(event)

    async with AsyncSessionLocal() as session:
        events = (await session.execute(select(BleEvent))).scalars().all()
        devices = (await session.execute(select(Device))).scalars().all()
        triggers = (await session.execute(select(RuleTrigger))).scalars().all()

    assert len(events) == 1
    assert len(devices) == 1
    assert devices[0].address == "AA:BB:CC"
    assert devices[0].last_rssi == -55
    assert len(triggers) == 1
    assert triggers[0].rule_name == "Band nearby"
