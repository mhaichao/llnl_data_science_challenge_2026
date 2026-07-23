"""Environment-backed settings that never expose secret values."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated runtime configuration for local and Cloud Run environments."""

    app_env: str = "development"
    cors_allowed_origins: str = "http://localhost:3000"
    gcp_project_id: str | None = None
    gcs_bucket_name: str | None = None
    demo_mode: bool = True
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def cors_origins(self) -> tuple[str, ...]:
        """Return normalized configured origins without allowing a wildcard."""
        origins = tuple(
            origin.strip()
            for origin in self.cors_allowed_origins.split(",")
            if origin.strip()
        )
        return origins or ("http://localhost:3000",)


@lru_cache
def get_settings() -> Settings:
    """Return one immutable-by-convention settings instance per process."""
    return Settings()
