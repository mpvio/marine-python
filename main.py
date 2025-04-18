from time import time
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import session, VesselDB, VesselCreate, VesselUpdate
from sqlalchemy import func

myApp = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173"
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
    try:
        vessel = VesselDB(updateTime = time(), **check_vessel(vesselCreate).model_dump())
        session.add(vessel)
        session.commit()
        session.refresh(vessel)
        return vessel
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create vessel")

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
            detail=f"Vessel with id {id} not found.")
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
            detail=f"Vessel with id {id} not found.")
    else:
        changes = False
        try:
            for field, value in check_vessel(updates).model_dump(exclude_unset=True).items():
                if hasattr(vessel, field) and getattr(vessel, field) != value:
                    setattr(vessel, field, value)
                    changes = True
            if changes:
                vessel.updateTime = time()
                session.commit()
                session.refresh(vessel)
            return vessel
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update vessel")

    
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
            "longitude": vessel.longitude,
            "updateTime": vessel.updateTime
        }
        session.delete(vessel)
        session.commit()
        return VesselDB(**vessel_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vessel with id {id} not found.")

#get latest update time from DB
@myApp.get("/latest/")
def get_latest_update():
    subqry = session.query(func.max(VesselDB.updateTime))
    vessel = session.query(VesselDB).filter(VesselDB.updateTime == subqry).first()
    if vessel:
        return vessel.updateTime
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No vessels found.")
  
#helper functions
def check_vessel(vessel: VesselCreate | VesselUpdate):
    if vessel.latitude is not None and not -90 <= vessel.latitude <= 90:
        raise ValueError('Latitude must be between -90 and 90 degrees')
    if vessel.longitude is not None and not -180 <= vessel.longitude <= 180:
        raise ValueError('Longitude must be between -180 and 180 degrees')
    return vessel