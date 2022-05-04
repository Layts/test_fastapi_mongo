from pydantic import BaseSettings


class Settings(BaseSettings):
    db_name: str = "test"

    class Config:
        env_file = ".env"


settings = Settings(_env_file='conf.env')
