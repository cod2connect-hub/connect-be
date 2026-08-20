"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Connect Backend"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str = ""
    database_url_migrator: str = ""
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    sendgrid_api_key: str = ""
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    cloudflare_api_token: str = ""
    s3_endpoint_url: str = ""
    s3_bucket: str = "platform-media"
    s3_access_key: str = ""
    s3_secret_key: str = ""


settings = Settings()
