from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import session, VesselDB, Status
from config import settings

myApp = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000"
]
myApp.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

'''
run with uvicorn main:myApp
test on localhost:8000/docs
'''

#CREATE
@myApp.post("/create")
async def create_vessel(
    name: str, 
    latitude: float, 
    longitude: float
    ):
    vessel = VesselDB(
        name=name, 
        latitude=latitude, 
        longitude=longitude
        )
    session.add(vessel)
    session.commit()
    return Status(vessel.id, settings.CREATED)

#READ (LIST)
@myApp.get("/")
async def get_vessels():
    query = session.query(VesselDB)
    return query.all()

#READ ID
@myApp.get("/{id}")
async def get_vessel(id: int):
    query = session.query(VesselDB).filter(VesselDB.id == id)
    return query.one_or_none()

#UPDATE
@myApp.put("/update/{id}")
async def update_vessel(
    id: int,
    name: str = None,
    latitude: float = None,
    longitude: float = None
    ):
    query = session.query(VesselDB).filter(VesselDB.id == id)
    vessel = query.one_or_none()
    if vessel:
        change = False
        if name: 
            vessel.name = name
            change = True
        if latitude: 
            vessel.latitude = latitude
            change = True
        if longitude: 
            vessel.longitude = longitude
            change = True
        if change:
            session.add(vessel)
            session.commit()
            return Status(id, settings.CHANGED)
        else:
            return Status(id, settings.UNCHANGED)
    else:
        return Status(id, settings.NOTFOUND)
    
#DELETE
@myApp.delete("/delete/{id}")
async def delete_vessel(id: int):
    query = session.query(VesselDB).filter(VesselDB.id == id)
    vessel = query.one_or_none()
    if vessel:
        session.delete(vessel)
        session.commit()
        return Status(id, settings.DELETED)
    else:
        return Status(id, settings.NOTFOUND)