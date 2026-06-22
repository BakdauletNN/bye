from pydantic import BaseModel, ConfigDict, EmailStr


class User(BaseModel):
    id: int
    email: str
    password_hash: str
    model_config = ConfigDict(from_attributes=True)


class Auth(BaseModel):
    username: str 
    password: str


class Register(BaseModel):
    name: str
    id_std: int
    email: EmailStr
    password: str 


class UserResponse(BaseModel):
    user_id: int
    email: str
    role: str
    name: str


class RecoveryRequest(BaseModel):
    email: EmailStr


class UserWithHashPass(User):
    hash_password: str