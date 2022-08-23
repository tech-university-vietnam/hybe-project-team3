from pydantic import BaseSettings


class Settings(BaseSettings):
    SECRET: str = "hype-secrect"

    class Config:

        env_file = "./env"