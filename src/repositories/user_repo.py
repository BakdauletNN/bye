from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.users import UserModel


# Search online: "Repository pattern SQLAlchemy Python"
class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalars().first()

    async def get_by_student_id(self, student_id: int) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.student_id == student_id)
        )
        return result.scalars().first()

    async def create(
        self,
        username: str,
        password_hash: str,
        student_id: int,
        role: str = "student",
    ) -> UserModel:
        user = UserModel(
            username=username,
            password_hash=password_hash,
            student_id=student_id,
            role=role,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
