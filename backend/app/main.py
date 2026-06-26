from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import beacon, devices, events, health, rules
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización
    await init_db()

    yield

    # Aquí en el futuro podremos cerrar conexiones,
    # workers, beacon, etc.


app = FastAPI(
    title="BLE Hub API",
    description="Backend para gestión de dispositivos BLE, reglas y balizas.",
    version="0.1.0",
    lifespan=lifespan,
)

# --------------------------------------------------------------------
# CORS
# --------------------------------------------------------------------
# Durante el desarrollo dejamos acceso libre.
# En producción se restringirá únicamente al frontend autorizado.
# --------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------------------------
# API
# --------------------------------------------------------------------

app.include_router(health.router, tags=["Health"])
app.include_router(devices.router, prefix="/devices", tags=["Devices"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(rules.router, prefix="/rules", tags=["Rules"])
app.include_router(beacon.router, prefix="/beacon", tags=["Beacon"])
