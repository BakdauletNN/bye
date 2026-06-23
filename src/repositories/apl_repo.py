from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.applications import ApplicationModel


class ApplicationRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, student_id: int, corpus: str, preferred_floor: int) -> ApplicationModel:
        app = ApplicationModel(
            student_id=student_id,
            corpus=corpus,
            preferred_floor=preferred_floor,
            status="pending",
        )
        self.session.add(app)
        await self.session.commit()
        await self.session.refresh(app)
        return app

    async def get_all(self, page: int, per_page: int) -> tuple[list[ApplicationModel], int]:
        offset = (page - 1) * per_page
        result = await self.session.execute(
            select(ApplicationModel).offset(offset).limit(per_page)
        )
        apps = result.scalars().all()
        count = await self.session.execute(select(func.count()).select_from(ApplicationModel))
        total = count.scalar()
        return apps, total

    async def get_by_id(self, app_id: int) -> Optional[ApplicationModel]:
        result = await self.session.execute(
            select(ApplicationModel).where(ApplicationModel.id_application == app_id)
        )
        return result.scalars().first()

    async def update_status(self, app_id: int, status: str) -> Optional[ApplicationModel]:
        app = await self.get_by_id(app_id)
        if not app:
            return None
        app.status = status
        await self.session.commit()
        await self.session.refresh(app)
        return app

    async def get_by_student(self, student_id: int) -> list[ApplicationModel]:
        result = await self.session.execute(
            select(ApplicationModel).where(ApplicationModel.student_id == student_id)
        )
        return result.scalars().all()
