from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"

    # Database (Neon)
    database_url: str
    database_url_direct: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Resend
    resend_api_key: str = ""
    resend_from_email: str = "Payment Platform <notifications@example.com>"

    # Security
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    admin_session_expire_minutes: int = 480
    encryption_key: str

    # Dashboard admin (CORS)
    admin_dashboard_origin: str = "http://localhost:3000"

    # Yellow Card
    yellowcard_base_url: str = "https://sandbox.api.yellowcard.io"
    yellowcard_api_key: str = ""
    yellowcard_api_secret: str = ""

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
