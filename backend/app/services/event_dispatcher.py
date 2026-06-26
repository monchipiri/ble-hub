import logging
from datetime import datetime, timezone

from sqlalchemy import select

from app.actions import ACTION_REGISTRY
from app.ble.models import BleAdvertisementEvent
from app.db.models import Rule, RuleTrigger
from app.db.session import AsyncSessionLocal
from app.rules.conditions import event_matches_conditions
from app.services.activity_service import store_ble_event

logger = logging.getLogger(__name__)


async def dispatch_ble_event(event: BleAdvertisementEvent) -> None:
    async with AsyncSessionLocal() as session:
        await store_ble_event(session, event)

        result = await session.execute(
            select(Rule).where(Rule.enabled.is_(True))
        )
        rules = result.scalars().all()

        for rule in rules:
            if not event_matches_conditions(event, rule.conditions):
                continue

            logger.warning(
                "RULE TRIGGERED rule=%s device=%s rssi=%s",
                rule.name,
                event.device_address,
                event.rssi,
            )

            trigger = RuleTrigger(
                rule_id=rule.id,
                rule_name=rule.name,
                device_address=event.device_address,
                local_name=event.local_name,
                rssi=event.rssi,
                actions=rule.actions,
                payload={
                    "source": event.source,
                    "service_uuids": event.service_uuids,
                    "manufacturer_data": event.manufacturer_data,
                    "payload": event.payload,
                },
                created_at=datetime.now(timezone.utc),
            )

            session.add(trigger)

            for action_config in rule.actions:
                action_type = action_config.get("type")
                params = action_config.get("params", {})

                action = ACTION_REGISTRY.get(action_type)
                if not action:
                    logger.warning("unknown action type=%s", action_type)
                    continue

                await action.execute(event, params)

        await session.commit()
