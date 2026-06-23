from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.checkinns import CheckinsModel
from datetime import datetime


class CheckinRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, student_id: int, room_id: int) -> CheckinsModel:
        checkin = CheckinsModel(student_id=student_id, room_id=room_id)
        self.session.add(checkin)
        await self.session.commit()
        await self.session.refresh(checkin)
        return checkin

    async def get_active_by_student(self, student_id: int) -> Optional[CheckinsModel]:
        result = await self.session.execute(
            select(CheckinsModel).where(
                CheckinsModel.student_id == student_id,
                CheckinsModel.checkout_date.is_(None),
            )
        )
        return result.scalars().first()

    async def checkout(self, checkin_id: int) -> Optional[CheckinsModel]:
        result = await self.session.execute(
            select(CheckinsModel).where(CheckinsModel.id_checkin == checkin_id)
        )
        checkin = result.scalars().first()
        if not checkin:
            return None
        checkin.checkout_date = datetime.now()
        await self.session.commit()
        await self.session.refresh(checkin)
        return checkin

    async def get_all_active(self) -> list[CheckinsModel]:
        result = await self.session.execute(
            select(CheckinsModel).where(CheckinsModel.checkout_date.is_(None))
        )
        return result.scalars().all()
