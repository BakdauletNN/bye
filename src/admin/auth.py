from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.dependencies import require_admin
from src.database.database import get_session
from src.repositories.perm_repo import PermRepo

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/me")
async def admin_profile(current_user=Depends(require_admin)):
    return {
        "user_id": current_user.id_user,
        "username": current_user.username,
        "role": current_user.role,
    }


@router.get("/user-role/{user_id}")
async def admin_get_user_role(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user=Depends(require_admin),
):
    role = await PermRepo(session).get_user_role(user_id)
    if role is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "role": role}