from time import time
from fastapi import HTTPException, status
from models import session, UpdateTimeDB

async def update_time():
    current_time = time()
    try:
        update = session.query(UpdateTimeDB).filter(UpdateTimeDB.id == 1).first()
        if not update:
            update = UpdateTimeDB(current_time)
            session.add(update)
        else: 
            update.updateTime = current_time
        session.commit()
        session.refresh(update)
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
    update = session.query(UpdateTimeDB).filter(UpdateTimeDB.id == 1).first()
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Update time not found.")
    else:
        return update.updateTime
    
async def get_time_records():
    return session.query(UpdateTimeDB).all()