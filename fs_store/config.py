import os

from pydantic import BaseModel


class GlobalConfig(BaseModel):
    ENV_STATE: str = os.getenv("ENV_STATE", "local")
    BASE_URL: str = "http://localhost:8000"


class LocalConfig(GlobalConfig):
    pass


class StgConfig(GlobalConfig):
    pass


class ProdConfig(GlobalConfig):
    pass


class FactoryConfig:
    def __init__(self, env_state: str):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "local":
            return LocalConfig()
        elif self.env_state == "stg":
            return StgConfig()
        elif self.env_state == "prod":
            return ProdConfig()
        raise ValueError(f"Invalid ENV_STATE: {self.env_state}")


settings = FactoryConfig(GlobalConfig().ENV_STATE)()
