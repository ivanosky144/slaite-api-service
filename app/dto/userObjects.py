from pydantic import BaseModel

class UserBody(BaseModel):
    username: str
    email: str
    password: str

class LoginUserBody(BaseModel):
    email: str
    password: str