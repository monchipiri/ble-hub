from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import RuleTrigger
from app.db.session import get_session
from app.schemas.rule_triggers import RuleTriggerOut

router = APIRouter(prefix="/rule-triggers", tags=["rule-triggers"])


@router.get("", response_model=list[RuleTriggerOut])
async def list_rule_triggers(
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(RuleTrigger).order_by(desc(RuleTrigger.created_at)).limit(limit)
    )
    return result.scalars().all()
