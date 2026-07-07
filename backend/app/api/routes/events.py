from fastapi import APIRouter, Depends, Query
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import BleEvent
from app.db.session import get_session
from app.schemas.events import EventOut

router = APIRouter(prefix="/events", tags=["events"])


@router.get("", response_model=list[EventOut])
async def list_events(
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(BleEvent).order_by(desc(BleEvent.created_at)).limit(limit))
    return result.scalars().all()
