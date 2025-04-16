from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./vesselData.db"
    LAST_UPDATE_FILE: str = "last_update.txt"
    CREATED: str = "created"
    CHANGED: str = "changed"
    UNCHANGED: str = "unchanged"
    DELETED: str = "deleted"
    NOTFOUND: str = "not found"

settings = Settings()