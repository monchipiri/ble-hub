from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.routes import beacon, devices, events, health, rules
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await init_db()
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.include_router(health.router)
app.include_router(devices.router)
app.include_router(events.router)
app.include_router(rules.router)
app.include_router(beacon.router)
