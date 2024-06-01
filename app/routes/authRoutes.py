from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dto.userObjects import LoginUserBody, UserBody
from models.userModel import User
from config.database import get_db
from sqlalchemy.orm import Session
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

router = APIRouter(tags=["Authentication"])

@router.post("/register")
def register(user: UserBody, db: Session = Depends(get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"])
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(
      username = user.username,
      email = user.email,
      password = hashed_password,
      created_at = datetime.now(),
      updated_at = datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": "success",
        "data": new_user
    }
    

@router.post("/login")
def login(user: LoginUserBody, db: Session = Depends(get_db)):
    pwd_context = CryptContext(schemes=["bcrypt"])
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not pwd_context.verify(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    payload = {
        "email": user.email,
        "exp": datetime.now() + timedelta(hours=1)
    }

    token = jwt.encode(payload, 'SECRET', algorithm='HS256')

    return {
        "status": "success",
        "token": token
    }

@router.post("/verify")
def verify():
    return "Verify"