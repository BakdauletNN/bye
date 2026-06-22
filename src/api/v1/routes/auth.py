from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from src.schemas.auth_s import Auth, Register, UserResponse, RecoveryRequest
from src.repositories.user_repo import UserRepo
from src.repositories.student_repo import StudentRepo
from src.database.database import async_ses_mkr
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.core.config import settings as stgs
import jwt



router = APIRouter(prefix="/auth", tags=["Authentication"], )
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_acces_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=stgs.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encode_jwt = jwt.encode(to_encode, stgs.SECRET_KEY, algorithm=stgs.HASH__ALG0)
    return encode_jwt


def verify_pass(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/login", response_model=dict)
async def login(auth_data: Auth):
    hashed_pswd = pwd_context.hash(auth_data.password)
    new_user_data = Auth(username=auth_data.username, password=hashed_pswd)
    async with async_ses_mkr() as session:
        user = await UserRepo(session).get_by_username(auth_data.username)
        if not user:
            raise HTTPException("User not found", status_code=404)
        if not verify_pass(auth_data.password, user.password_hash):
            raise HTTPException("Incorrect password", status_code=400)
                
        acces_token = create_acces_token({"user_id": user.username})
        return {"access_token": acces_token, "token_type": "bearer"}



@router.post("/recovery")
async def recovery_with_email(email_data: RecoveryRequest):
    # TODO: отправить письмо на email_data.email
    return {
        "message": "Recovery email sent",
        "email": email_data.email
    }



@router.post("/register", response_model=UserResponse)
async def register(user_data: Register):
    hashed_pswd = pwd_context.hash(user_data.password)
    ok = False
    async with async_ses_mkr() as session:
        student_repo = StudentRepo(session)
        user_repo = UserRepo(session)
        student = await student_repo.get_by_id(user_data.id_std)
        if not student:
            raise HTTPException(
                status_code=400,
                detail="Student with this ID was not found"
            )

        existing_user_by_id = await user_repo.get_by_student_id(user_data.id_std)
        if existing_user_by_id:
            raise HTTPException(
                status_code=400,
                detail="This student is already registered",
            )
        existing_by_mail = await user_repo.get_by_username(user_data.email)
        if existing_by_mail:
            raise HTTPException(
                status_code=400,
                detail="This email is already registered",
            )
        else:
            await user_repo.create(
                username=user_data.email,
                password_hash=hashed_pswd,
                student_id=user_data.id_std,
            )
            ok = True
        

    return {"status":"registred successfully" if ok else "registration failed"}


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