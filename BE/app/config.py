import os
from functools import lru_cache
from pydantic import BaseSettings


def get_env_file():
    filename = '.'.join(['.env', os.getenv('ENV', 'local')])
    env_filepath = os.path.join(os.getcwd(), filename)

    return env_filepath


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET: str

    class Config:
        env_file = get_env_file()
        print(env_file)
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    settings = Settings()
    return settings
