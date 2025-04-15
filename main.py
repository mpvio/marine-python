from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import session, VesselDB, VesselCreate, VesselUpdate
from sqlalchemy import func

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
async def create_vessel(vesselCreate: VesselCreate):
    vessel = VesselDB(**vesselCreate.model_dump())
    session.add(vessel)
    session.commit()
    session.refresh(vessel)
    return vessel

#READ (LIST)
@myApp.get("/")
async def get_vessels():
    query = session.query(VesselDB)
    return query.all()

#READ ID
@myApp.get("/{id}")
async def get_vessel(id: int):
    vessel = session.query(VesselDB).filter(VesselDB.id == id).first()
    if not vessel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vessel with id {id} not found."
        )
    else:
        return vessel

#READ NAME
@myApp.get("/name/{name}")
async def get_vessels_by_name(name: str):
    vessels = session.query(VesselDB).filter(func.lower(VesselDB.name) == func.lower(name)).all()
    return vessels

#UPDATE
@myApp.put("/update/{id}")
async def update_vessel(
    id: int,
    updates: VesselUpdate):
    vessel = session.query(VesselDB).filter(VesselDB.id == id).first()
    if not vessel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vessel with id {id} not found."
        )
    else:
        changes = False
        for field, value in updates.model_dump(exclude_unset=True).items():
            if hasattr(vessel, field) and getattr(vessel, field) != value:
                setattr(vessel, field, value)
                changes = True
        if changes:
            session.commit()
            session.refresh(vessel)
        return vessel
    
#DELETE
@myApp.delete("/delete/{id}")
async def delete_vessel(id: int):
    vessel = session.query(VesselDB).filter(VesselDB.id == id).first()
    if vessel:
        # Create copy of vessel data
        vessel_data = {
            "id": vessel.id,
            "name": vessel.name,
            "latitude": vessel.latitude,
            "longitude": vessel.longitude
        }
        session.delete(vessel)
        session.commit()
        return VesselDB(**vessel_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vessel with id {id} not found."
        )