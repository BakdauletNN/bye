from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Body


class Auth(BaseModel):
    input_data: OAuth2PasswordRequestForm = Body(embed=True)


class Register(BaseModel):
    name: str= Body(embed=True),
    surname:str= Body(embed=True)
    id_std: int= Body(embed=True)
    location: str= Body(embed=True)
    course: int= Body(embed=True)
