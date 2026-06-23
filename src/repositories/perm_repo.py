from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users import UserModel


class PermRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_role(self, user_id: int) -> Optional[str]:
        result = await self.session.execute(
            select(UserModel.role).where(UserModel.id_user == user_id)
        )
        row = result.first()
        return row[0] if row else None

    async def user_has_role(self, user_id: int, role: str) -> bool:
        return (await self.get_user_role(user_id)) == role
