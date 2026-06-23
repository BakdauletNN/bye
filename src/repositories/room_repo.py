from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.rooms import RoomModel


class RoomRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, room_id: int) -> Optional[RoomModel]:
        result = await self.session.execute(
            select(RoomModel).where(RoomModel.id_room == room_id)
        )
        return result.scalars().first()

    async def create(self, data: dict) -> RoomModel:
        room = RoomModel(**data, status="a")
        self.session.add(room)
        await self.session.commit()
        await self.session.refresh(room)
        return room

    async def get_available(
        self,
        page: int,
        per_page: int,
        corpus: Optional[str] = None,
        who: Optional[str] = None,
        floor: Optional[int] = None,
    ) -> list[RoomModel]:
        query = select(RoomModel).where(RoomModel.status == "a")
        if corpus:
            query = query.where(RoomModel.corpus == corpus)
        if who:
            query = query.where(RoomModel.who == who)
        if floor:
            query = query.where(RoomModel.floor == floor)
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, room_id: int, data: dict) -> Optional[RoomModel]:
        room = await self.get_by_id(room_id)
        if not room:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(room, key, value)
        await self.session.commit()
        await self.session.refresh(room)
        return room

    async def delete(self, room_id: int) -> bool:
        room = await self.get_by_id(room_id)
        if not room:
            return False
        await self.session.delete(room)
        await self.session.commit()
        return True
