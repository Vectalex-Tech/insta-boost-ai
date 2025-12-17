from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "dev"
    PUBLIC_BASE_URL: str = "http://localhost:8000"
    CORS_ORIGINS: str = "http://localhost:3000"

    DATABASE_URL: str
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/1"

    UPLOAD_DIR: str = "/data/uploads"
    RENDER_DIR: str = "/data/renders"

    OPENAI_API_KEY: str = ""

    META_APP_ID: str = ""
    META_APP_SECRET: str = ""
    META_REDIRECT_URI: str = ""
    META_API_VERSION: str = "v21.0"

    META_USER_ACCESS_TOKEN: str = ""
    META_PAGE_ID: str = ""
    META_IG_USER_ID: str = ""

    def cors_list(self) -> List[str]:
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]

settings = Settings()
