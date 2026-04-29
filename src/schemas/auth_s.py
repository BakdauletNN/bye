from pydantic import BaseModel, EmailStr


class Auth(BaseModel):
    username: str 
    password: str


class Register(BaseModel):
    name: str
    surname: str
    id_std: int
    email: EmailStr
    location: str
    course: int
    password: str 


class UserResponse(BaseModel):
    user_id: int
    email: str
    role: str
    name: str


class RecoveryRequest(BaseModel):
    email: EmailStr