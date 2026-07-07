# BLE Hub

Gateway local para detectar anuncios BLE, normalizar eventos, evaluar reglas y operar un panel web de dispositivos, actividad y baliza.

## Estructura

- `backend/`: API FastAPI, scanner BLE, reglas, acciones y persistencia.
- `frontend/`: panel React/Vite para consultar dispositivos, eventos, reglas, disparos y baliza.

## Arranque local

Backend:

```bash
cd backend
python3 -m venv ../.venv
../.venv/bin/pip install -e ".[dev]"
cp .env.example .env
../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:

```bash
cd frontend
cp .env.example .env
pnpm install
pnpm run dev
```

Abrir `http://localhost:5173`.

## Producción en Raspberry Pi

El backend usa SQLite por defecto para instalación simple. Si prefieres PostgreSQL, cambia `DATABASE_URL` a una URL `postgresql+asyncpg://...` e instala/gestiona la base de datos aparte.

Para el scanner BLE:

```bash
cd backend
../.venv/bin/python scripts/check_adapters.py
../.venv/bin/python scripts/run_scanner.py
```

`app/ble/advertiser.py` mantiene el contrato de advertising. La implementación real de BlueZ D-Bus queda separada para ejecutarse con un adaptador dedicado, por ejemplo `hci1`.
