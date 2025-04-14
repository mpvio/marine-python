from pydantic import BaseModel

class VesselUpdate(BaseModel):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None