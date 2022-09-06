import os
from functools import lru_cache
from pydantic import BaseSettings
import os


def get_env_file():
    filename = '.'.join(['.env', os.getenv('ENV', 'local')])
    env_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    print(env_filepath)
    return env_filepath


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET: str

    class Config:
        env_file = get_env_file()
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    settings = Settings()
    return settings
