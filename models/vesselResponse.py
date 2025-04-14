from pydantic import BaseModel

class VesselResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float