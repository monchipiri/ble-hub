from fastapi import APIRouter, Query
from sqlalchemy import desc, select

from app.db.models import RuleTrigger
from app.db.session import AsyncSessionLocal

router = APIRouter(prefix="/rule-triggers")


@router.get("")
async def list_rule_triggers(limit: int = Query(default=100, ge=1, le=500)):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(RuleTrigger)
            .order_by(desc(RuleTrigger.created_at))
            .limit(limit)
        )

        triggers = result.scalars().all()

        return [
            {
                "id": trigger.id,
                "rule_id": trigger.rule_id,
                "rule_name": trigger.rule_name,
                "device_address": trigger.device_address,
                "local_name": trigger.local_name,
                "rssi": trigger.rssi,
                "actions": trigger.actions,
                "payload": trigger.payload,
                "created_at": trigger.created_at,
            }
            for trigger in triggers
        ]
