from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dto.userObjects import UserBody
from models.userModel import User
from sqlalchemy.orm import Session
from config.database import get_db
from sqlalchemy.orm import Session
from middleware.authentication import verifyAuth

router = APIRouter(tags=["Users"])

@router.get("/{user_email}", dependencies=[Depends(verifyAuth)])
def getUserDetail(user_email: str, db: Session=Depends(get_db)):
    user_detail = db.query(User).filter(User.email == user_email).first()
    if not user_detail:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "status": "success",
        "data": user_detail
    }

@router.get("/")
def getAllUsers(db: Session=Depends(get_db)):
    users = db.query(User).all()
    
    return {
        "status": "success",
        "data": users
    }

@router.put("/{user_id}", dependencies=[Depends(verifyAuth)])
def updateUser(user_id: int, user: UserBody, db: Session=Depends(get_db)):
    existing_user = db.query(User).filter(User.id == user_id).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, val in user.model_dump().items():
        setattr(existing_user, key, val)
    
    db.commit()
    db.refresh(existing_user)

    return {
        "status": "success",
        "message": "data has been updated"
    }