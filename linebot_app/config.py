from functools import lru_cache
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class APISettings(BaseSettings):
    title: str = "VoiceTube Search"
    description: str = "Search API of VoiceTube"
    version: str = "1.0.0"
    docs_url: Optional[str] = None
    redoc_url: Optional[str] = None

    class Config:
        env_file = ".env"


class APPSettings(BaseSettings):
    project: str
    db_host: str
    db_port: str
    db_database: str
    db_username: str
    db_password: str
    datascientist_domain: str
    auth_domain: str
    vta_domain: str
    line_channel_access_token: str
    line_channel_secret: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_api_settings() -> APISettings:
    return APISettings()


@lru_cache()
def get_app_settings() -> APPSettings:
    return APPSettings()
