from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from datetime import datetime, timedelta
from src.schemas.auth_s import Auth, Register, TokenResponse, UserResponse, RecoveryRequest
from src.repositories.user_repo import UserRepo
from src.repositories.student_repo import StudentRepo
from src.database.database import get_session
from src.core.config import stgs
from src.core.dependencies import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Search online: "passlib bcrypt password hashing Python"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(username: str) -> str:
    # Search online: "PyJWT create token encode Python"
    expire = datetime.now() + timedelta(minutes=stgs.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"username": username, "exp": expire}
    return jwt.encode(payload, stgs.SECRET_KEY, algorithm=stgs.HASH__ALG0)


@router.post("/login", response_model=TokenResponse)
async def login(auth_data: Auth, session: AsyncSession = Depends(get_session)):
    user = await UserRepo(session).get_by_username(auth_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        valid = pwd_context.verify(auth_data.password, user.password_hash)
    except UnknownHashError:
        raise HTTPException(
            status_code=500,
            detail="Stored password hash is invalid. Recreate the user with a proper bcrypt hash.",
        )
    if not valid:
        raise HTTPException(status_code=401, detail="Incorrect password")
    token = create_access_token(user.username)
    return TokenResponse(access_token=token)


@router.post("/register")
async def register(user_data: Register, session: AsyncSession = Depends(get_session)):
    # Search online: "FastAPI register user SQLAlchemy async"
    user_repo = UserRepo(session)
    student_repo = StudentRepo(session)

    student = await student_repo.get_by_id(user_data.id_std)
    if not student:
        raise HTTPException(status_code=400, detail="Student with this ID not found")

    if await user_repo.get_by_student_id(user_data.id_std):
        raise HTTPException(status_code=400, detail="This student is already registered")

    if await user_repo.get_by_username(user_data.email):
        raise HTTPException(status_code=400, detail="This email is already registered")

    hashed = pwd_context.hash(user_data.password)
    await user_repo.create(username=user_data.email, password_hash=hashed, student_id=user_data.id_std)
    return {"status": "registered successfully"}


@router.get("/me", response_model=UserResponse)
async def me(current_user=Depends(get_current_user)):
    # Search online: "FastAPI get current user Depends"
    return UserResponse(
        user_id=current_user.id_user,
        username=current_user.username,
        role=current_user.role,
        student_id=current_user.student_id,
    )


@router.post("/recovery")
async def recovery(email_data: RecoveryRequest):
    # Search online: "FastAPI send email SMTP"
    return {"message": f"Recovery email sent to {email_data.email}"}
