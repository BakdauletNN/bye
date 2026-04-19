from fastapi import APIRouter, Body
from 
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
async def login(input_data: OAuth2PasswordRequestForm = Body(embed=True)):
    return {"acces_token": "fake-jwt-token", "token_type":"bearer"}


@router.post("/register")
def rgs(name: str= Body(embed=True),
        surname:str= Body(embed=True),
        id_std: int= Body(embed=True),
        location: str= Body(embed=True),
        course: int= Body(embed=True), 
        ):
    
    pass