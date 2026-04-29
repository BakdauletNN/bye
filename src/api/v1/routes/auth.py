from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from src.schemas.auth_s import Auth, Register, UserResponse, RecoveryRequest


router = APIRouter(prefix="/auth", tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login", response_model=dict)
async def login(auth_data: Auth):
    # TODO: проверить логин/пароль в БД
    if auth_data.username != "student@example.com" or auth_data.password != "password":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {
        "access_token": "fake-jwt-token-123", 
        "token_type": "bearer",
        "expires_in": 3600
    }



@router.post("/recovery")
async def recovery_with_email(email_data: RecoveryRequest):
    # TODO: отправить письмо на email_data.email
    return {
        "message": "Recovery email sent",
        "email": email_data.email
    }


@router.post("/register", response_model=UserResponse)
async def register(user_data: Register):
    # TODO: сохранить в БД
    return UserResponse(
        user_id=user_data.id_std,
        email=user_data.email,
        role="student",
        name=f"{user_data.name} {user_data.surname}"
    )


@router.get("/me", response_model=UserResponse)
async def me(token: str = Depends(oauth2_scheme)):
    # TODO: декодировать JWT и получить user
    if token != "fake-jwt-token-123":
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return UserResponse(
        user_id=123,
        email="student@example.com",
        role="student",
        name="John Doe"
    )