from fastapi import Query, Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import get_session
import jwt
from src.core.config import stgs

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# --- Pagination ---
# Search online: "FastAPI Query parameters pagination"
class Pagination(BaseModel):
    page: Annotated[int, Query(1, ge=1)]
    per_page: Annotated[int, Query(10, ge=1, le=50)]


PgnDepds = Annotated[Pagination, Depends()]


# --- DB session as dependency ---
# Search online: "FastAPI dependency injection database session SQLAlchemy"
SessionDep = Annotated[AsyncSession, Depends(get_session)]


# --- Get current user from JWT token ---
# Search online: "FastAPI JWT authentication get current user"
async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    from src.repositories.user_repo import UserRepo
    try:
        payload = jwt.decode(token, stgs.SECRET_KEY, algorithms=[stgs.HASH__ALG0])
        username: str = payload.get("username")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await UserRepo(session).get_by_username(username)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# --- Admin role check ---
# Search online: "FastAPI role based access control RBAC"
async def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# --- Manager or admin role check ---
async def require_manager(current_user=Depends(get_current_user)):
    if current_user.role not in ("admin", "manager"):
        raise HTTPException(status_code=403, detail="Manager access required")
    return current_user


CurrentUser = Annotated[object, Depends(get_current_user)]
AdminUser = Annotated[object, Depends(require_admin)]
ManagerUser = Annotated[object, Depends(require_manager)]
