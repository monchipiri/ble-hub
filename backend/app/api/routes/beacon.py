from fastapi import APIRouter
from app.ble.advertiser import BleAdvertiserService
from app.schemas.beacon import BeaconStartRequest

router = APIRouter(prefix="/beacon", tags=["beacon"])
advertiser = BleAdvertiserService()


@router.get("/status")
async def beacon_status():
    return await advertiser.status()


@router.post("/start")
async def beacon_start(payload: BeaconStartRequest):
    await advertiser.start(payload.payload)
    return await advertiser.status()


@router.post("/stop")
async def beacon_stop():
    await advertiser.stop()
    return await advertiser.status()
