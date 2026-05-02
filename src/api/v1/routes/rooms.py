from fastapi import APIRouter, Query, Depends, HTTPException
from typing import List, Optional
from src.schemas.rooms_s import *
from src.core.dependencies import Pagination
from src.models.rooms import RoomModel
from src.database.database import async_ses_mkr, engine
from sqlalchemy import insert, select, update, delete


router = APIRouter(prefix="/rooms", tags=["Rooms"])



@router.post("/add", response_model=RoomResponse)
async def create_room(room_data: RoomCreate, whois = Depends()):

    # TODO: Проверить статус, если админ сохранить в БД
    async with async_ses_mkr() as session:
        rooom_add_stmt = insert(RoomModel).values(**room_data.model_dump())
        print(rooom_add_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(rooom_add_stmt)
        await session.commit()
        pass


@router.get("/available/", response_model=List[RoomResponse])
async def get_available_rooms(
    pgt: Pagination,
    corpus: Optional[Corpus] = Query(None),
    who: Optional[Gender] = Query(None),
    floor: Optional[int] = Query(None, ge=1, le=2)
):
    ans = []
    if pgt.page and pgt.per_page:
        return ans[pgt.per_page*(pgt.page-1):][:pgt.per_page]
    pass


@router.get("/{id_room}")
async def get_room_info(id_room_input:int):
    #check tole for admin, if not admin return info about room

    async with async_ses_mkr() as session:
        query = select(RoomModel).where(RoomModel.id_room == id_room_input)
        result = await session.execute(query)
        room = result.scalars().first()
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        return RoomResponse(
            id_room=room.id_room,
            floor=room.floor,
            number=room.number,
            qty_person=room.qty_person,
            who=room.who,
            corpus=room.corpus,
            status=RoomStatus(room.status)
        )


@router.patch("/{id_room}", response_model=RoomResponse)
async def update_room(id_room: int, room_update: RoomUpdate):
    # TODO: Проверить статус, если админ изменить в БД
    pass


@router.delete("/{id_room}")
async def delete_room(id_room: int):
    # TODO: Проверить статус, если админ удалить из БД
    pass