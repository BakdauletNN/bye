from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.students import StudentModel


class StudentRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, student_id: int) -> Optional[StudentModel]:
        result = await self.session.execute(
            select(StudentModel).where(StudentModel.id_student == student_id)
        )
        return result.scalars().first()

    async def get_all(self, page: int, per_page: int) -> tuple[list[StudentModel], int]:
        offset = (page - 1) * per_page
        result = await self.session.execute(
            select(StudentModel).offset(offset).limit(per_page)
        )
        students = result.scalars().all()
        count = await self.session.execute(select(func.count()).select_from(StudentModel))
        total = count.scalar()
        return students, total

    async def create(self, data: dict) -> StudentModel:
        student = StudentModel(**data)
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    async def update(self, student_id: int, data: dict) -> Optional[StudentModel]:
        student = await self.get_by_id(student_id)
        if not student:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(student, key, value)
        await self.session.commit()
        await self.session.refresh(student)
        return student

    async def delete(self, student_id: int) -> bool:
        student = await self.get_by_id(student_id)
        if not student:
            return False
        await self.session.delete(student)
        await self.session.commit()
        return True
