from fastapi import APIRouter, Depends
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import BleEvent
from app.db.session import AsyncSessionLocal
from app.schemas.events import EventOut

router = APIRouter(prefix="/events", tags=["events"])


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("", response_model=list[EventOut])
async def list_events(limit: int = 100, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(BleEvent).order_by(desc(BleEvent.created_at)).limit(limit))
    return result.scalars().all()
