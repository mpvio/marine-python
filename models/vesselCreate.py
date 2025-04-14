from pydantic import BaseModel

class VesselCreate(BaseModel):
    name: str
    latitude: float
    longitude: float