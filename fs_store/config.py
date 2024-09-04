import os

from pydantic_settings import BaseSettings


class GlobalConfig(BaseSettings):
    ENV_STATE: str = os.getenv("ENV_STATE", "local")


class LocalConfig(GlobalConfig):
    BASE_URL = "http://localhost:8000"


class StgConfig(GlobalConfig):
    BASE_URL = "http://localhost:8000"


class ProdConfig(GlobalConfig):
    BASE_URL = "http://localhost:8000"


class FactoryConfig:
    def __init__(self, env_state: str):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "dev":
            return LocalConfig()
        elif self.env_state == "stg":
            return StgConfig()
        elif self.env_state == "prod":
            return ProdConfig()
        raise ValueError(f"Invalid ENV_STATE: {self.env_state}")


settings = FactoryConfig(GlobalConfig().ENV_STATE)()
