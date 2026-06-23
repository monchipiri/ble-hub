import logging
from sqlalchemy import select
from app.actions.alert import AlertAction
from app.actions.log_activity import LogActivityAction
from app.actions.webhook import WebhookAction
from app.ble.models import BleAdvertisementEvent
from app.db.models import Rule
from app.db.session import AsyncSessionLocal
from app.rules.conditions import event_matches_conditions
from app.services.activity_service import store_ble_event

logger = logging.getLogger(__name__)

ACTION_REGISTRY = {
    "log_activity": LogActivityAction(),
    "database_log": LogActivityAction(),
    "alert": AlertAction(),
    "webhook": WebhookAction(),
}


async def dispatch_ble_event(event: BleAdvertisementEvent) -> None:
    async with AsyncSessionLocal() as session:
        await store_ble_event(session, event)
        rules = (await session.execute(select(Rule).where(Rule.enabled.is_(True)))).scalars().all()

    for rule in rules:
        if not event_matches_conditions(event, rule.conditions):
            continue
        logger.info("rule matched id=%s name=%s", rule.id, rule.name)
        for action in rule.actions:
            action_type = action.get("type")
            params = action.get("params", {})
            handler = ACTION_REGISTRY.get(action_type)
            if not handler:
                logger.warning("unknown action type=%s", action_type)
                continue
            await handler.execute(event, params)
