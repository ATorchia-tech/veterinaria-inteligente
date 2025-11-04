from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite:///./app.db"
    weather_api_base: str | None = None
    weather_api_key: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
