from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Device
from app.db.session import AsyncSessionLocal
from app.schemas.devices import DeviceOut

router = APIRouter(prefix="/devices", tags=["devices"])


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("", response_model=list[DeviceOut])
async def list_devices(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Device).order_by(Device.last_seen_at.desc().nullslast()))
    return result.scalars().all()
