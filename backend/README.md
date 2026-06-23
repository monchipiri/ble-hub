# BLE Hub Backend MVP

Backend inicial para escuchar anuncios BLE de wearables, normalizar eventos, evaluar reglas configurables y registrar actividad.

## Requisitos Raspberry Pi

- Raspberry Pi OS actualizado
- Python 3.11+
- BlueZ instalado y activo
- 1 o 2 adaptadores Bluetooth, por ejemplo `hci0` para scan y `hci1` para advertising

```bash
sudo apt update
sudo apt install -y bluetooth bluez python3-venv
bluetoothctl list
```

## Instalacion

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

## Ejecutar API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Ejecutar scanner BLE

```bash
python scripts/run_scanner.py
```

## Endpoints iniciales

- `GET /health`
- `GET /events`
- `GET /devices`
- `GET /rules`
- `POST /rules`
- `PATCH /rules/{rule_id}`
- `GET /beacon/status`
- `POST /beacon/start`
- `POST /beacon/stop`

## Nota sobre advertising BLE

El archivo `app/ble/advertiser.py` deja preparado el contrato del servicio. En Raspberry Pi se recomienda implementarlo con BlueZ D-Bus y ejecutarlo como proceso separado usando `hci1`.
