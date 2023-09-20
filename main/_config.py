import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    ENVIRONMENT: str
    LOGGING_LEVEL: int = logging.INFO

    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_ENGINE_OPTIONS: dict = {}
    SQLALCHEMY_ECHO: bool = False
    MYSQL_DEV_ROOT_PASSWORD: str
    MYSQL_DEV_DATABASE: str
    MYSQL_DEV_PORT: int = 3306
    ADMINER_PORT: int = 8080

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file_encoding="utf-8",
    )


environment = os.environ.get("ENVIRONMENT", "local")
config = Config(
    ENVIRONMENT=environment,
    # ".env.{environment}" takes priority over ".env"
    _env_file=[".env", f".env.{environment}"],
)
