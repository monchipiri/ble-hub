from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import beacon, devices, events, health, rules, rule_triggers
from app.core.config import get_settings
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


settings = get_settings()

app = FastAPI(
    title="BLE Hub API",
    description="Backend para gestión de dispositivos BLE, reglas y balizas.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(devices.router)
app.include_router(events.router)
app.include_router(rules.router)
app.include_router(beacon.router)
app.include_router(rule_triggers.router)
