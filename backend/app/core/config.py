from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BLE Hub"
    app_env: str = "dev"
    database_url: str = "postgresql+asyncpg://blehub:blehub_password@localhost:5432/blehub"
    ble_scan_adapter: str = "hci0"
    ble_advertise_adapter: str = "hci1"
    ble_scan_rssi_min: int = -95

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
