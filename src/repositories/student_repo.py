from typing import Optional
from sqlalchemy import select
from src.models.students import StudentModel


class StudentRepo:
    def __init__(self, session):
        self.session = session

    async def get_by_id(self, student_id: int) -> Optional[StudentModel]:
        stmt = select(StudentModel).where(StudentModel.id_student == student_id)
        result = await self.session.execute(stmt)
        return result.scalars().first()
 