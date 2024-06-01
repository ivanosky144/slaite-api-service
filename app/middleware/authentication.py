from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime

security = HTTPBearer()

def verifyAuth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, 'SECRET', algorithms=['HS256'])
        if payload['exp'] < datetime.timestamp(datetime.now()):
            raise HTTPException(status_code=403, detail="Token has expired")
        return payload

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")