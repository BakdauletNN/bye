from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


# Schema for login
class Auth(BaseModel):
    username: str
    password: str


# Schema for registration
class Register(BaseModel):
    id_std: int
    email: EmailStr
    password: str


# Response after login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Current user information (/me)
class UserResponse(BaseModel):
    user_id: int
    username: str
    role: str
    student_id: int
    model_config = ConfigDict(from_attributes=True)


# Internal schema for password hash handling
class UserWithHashPass(BaseModel):
    id_user: int
    username: str
    password_hash: str
    role: str
    student_id: int
    model_config = ConfigDict(from_attributes=True)


# Password recovery request
class RecoveryRequest(BaseModel):
    email: EmailStr
