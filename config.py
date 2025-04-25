from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./vesselData.db"
    TIME_RECORD_ID: int = 1

settings = Settings()