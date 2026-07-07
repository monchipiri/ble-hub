import json
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BLE Hub"
    app_env: str = "dev"
    database_url: str = "sqlite+aiosqlite:///./blehub.db"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    ble_scan_adapter: str = "hci0"
    ble_advertise_adapter: str = "hci1"
    ble_scan_rssi_min: int = -95

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> object:
        if not isinstance(value, str):
            return value

        raw_value = value.strip()
        if raw_value == "*":
            return ["*"]

        if raw_value.startswith("["):
            return json.loads(raw_value)

        return [origin.strip() for origin in raw_value.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
