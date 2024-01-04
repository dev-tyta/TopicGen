from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "TopicGen API"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = ["*"]

    model_config = SettingsConfigDict(gcase_sensitive=True)


settings = Settings()
