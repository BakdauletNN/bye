from fastapi import APIRouter, Body
from schemas.auth_s import Auth, Register
from a


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
async def login(input: Auth):
    return {"acces_token": "fake-jwt-token", "token_type":"bearer"}


@router.post("/register")
def rgs(all_info: Register):
    pass