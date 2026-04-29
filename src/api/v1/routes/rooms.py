from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from src.schemas.rooms_s import *
from src.core.dependencies import Pagination


router = APIRouter(prefix="/rooms", tags=["Rooms"])



@router.post("/add", response_model=RoomResponse)
async def create_room(room: RoomCreate, whois = Depends()):
    # TODO: Проверить статус, если админ сохранить в БД
    pass


@router.get("/{id_room}", response_model=RoomResponse)
async def get_room_info(id_room: int):
    # TODO: Проверить статус, если админ отдавать результат
    pass


@router.get("/available/", response_model=List[RoomResponse])
async def get_available_rooms(
    pgt: Pagination,
    corpus: Optional[Corpus] = Query(None),
    who: Optional[Gender] = Query(None),
    floor: Optional[int] = Query(None, ge=1, le=5)
):
    ans = []
    if pgt.page and pgt.per_page:
        return ans[pgt.per_page*(pgt.page-1):][:pgt.per_page]
    pass


@router.patch("/{id_room}", response_model=RoomResponse)
async def update_room(id_room: int, room_update: RoomUpdate):
    # TODO: Проверить статус, если админ изменить в БД
    pass


@router.delete("/{id_room}")
async def delete_room(id_room: int):
    # TODO: Проверить статус, если админ удалить из БД
    pass