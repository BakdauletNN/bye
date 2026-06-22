from typing import Optional
from sqlalchemy import select
from src.models.users import UserModel
from src.schemas.auth_s import User, UserWithHashPass


class UserRepo:

    schema = User
    model = UserModel

    def __init__(self, session):
        self.session = session

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.username == username)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_by_student_id(self, student_id: int) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.student_id == student_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(
        self,
        username: str,
        password_hash: str,
        student_id: int,
        role: str = "student",
        is_registered: bool = True,
    ) -> UserModel:
        user = UserModel(
            username=username,
            password_hash=password_hash,
            student_id=student_id,
            role=role,
            is_registered=is_registered,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def get_user_by_hash_pass(self, email: str) -> Optional[UserWithHashPass]:
        query = select(UserModel).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashPass.model_validate(model)
    