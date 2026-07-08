import json
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BLE Hub"
    app_env: str = "dev"
    database_url: str = "sqlite+aiosqlite:///./blehub.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    ble_scan_adapter: str = "hci0"
    ble_advertise_adapter: str = "hci1"
    ble_scan_rssi_min: int = -95

    @property
    def cors_origin_list(self) -> list[str]:
        raw_value = self.cors_origins.strip()
        if not raw_value:
            return []
        if raw_value == "*":
            return ["*"]

        if raw_value.startswith("["):
            parsed_value = json.loads(raw_value)
            if not isinstance(parsed_value, list):
                raise ValueError("CORS_ORIGINS JSON value must be a list")
            return [str(origin).strip() for origin in parsed_value if str(origin).strip()]

        return [origin.strip() for origin in raw_value.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
