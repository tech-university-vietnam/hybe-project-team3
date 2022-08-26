import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET: str

    class Config:
        env_file = os.path.join(os.getcwd(), '.env')
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    settings = Settings()
    return settings
