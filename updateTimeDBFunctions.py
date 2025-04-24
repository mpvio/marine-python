from time import time
from fastapi import HTTPException, status
from models import session, UpdateTimeDB
from config import settings

async def update_time(current_time: float = None):
    if not current_time: current_time = time()
    try:
        update = session.query(UpdateTimeDB).filter(UpdateTimeDB.id == settings.TIME_RECORD_ID).first()
        if not update:
            # if record has not yet been created, create record with fixed ID (currently 1)
            update = UpdateTimeDB(id = settings.TIME_RECORD_ID, updateTime = current_time)
            session.add(update)
        else: 
            #else update record with current time
            update.updateTime = current_time
        session.commit()
        session.refresh(update)
        return update
    except ValueError as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e))
    except:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create time record")
    
async def get_time():
    # get update record with fixed id (currently 1)
    update = session.query(UpdateTimeDB).filter(UpdateTimeDB.id == settings.TIME_RECORD_ID).first()
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Update time not found.")
    else:
        return update.updateTime
    
async def get_time_records():
    return session.query(UpdateTimeDB).all()