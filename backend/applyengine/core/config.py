from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _get_env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


def _get_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    return int(raw) if raw and raw.strip() else default


@dataclass(frozen=True, slots=True)
class Settings:
    app_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_base_url: str = "http://localhost:8000"
    frontend_base_url: str = "http://localhost:3000"
    jwt_secret: str = "<JWT_SECRET>"
    jwt_audience: str = "applyengine-api"
    jwt_issuer: str = "applyengine"
    access_token_ttl_minutes: int = 30
    refresh_token_ttl_minutes: int = 10080
    database_url: str = "postgresql+asyncpg://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>"
    redis_url: str = "redis://localhost:6379/0"

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings(
        app_env=_get_env("APP_ENV", "development"),
        api_host=_get_env("API_HOST", "0.0.0.0"),
        api_port=_get_int("API_PORT", 8000),
        api_base_url=_get_env("API_BASE_URL", "http://localhost:8000"),
        frontend_base_url=_get_env("FRONTEND_BASE_URL", "http://localhost:3000"),
        jwt_secret=_get_env("JWT_SECRET", "<JWT_SECRET>"),
        jwt_audience=_get_env("JWT_AUDIENCE", "applyengine-api"),
        jwt_issuer=_get_env("JWT_ISSUER", "applyengine"),
        access_token_ttl_minutes=_get_int("ACCESS_TOKEN_TTL_MINUTES", 30),
        refresh_token_ttl_minutes=_get_int("REFRESH_TOKEN_TTL_MINUTES", 10080),
        database_url=_get_env(
            "DATABASE_URL", "postgresql+asyncpg://<DB_USER>:<DB_PASSWORD>@localhost:5432/<DB_NAME>"
        ),
        redis_url=_get_env("REDIS_URL", "redis://localhost:6379/0"),
    )

