from fastapi import APIRouter, Query, Depends, HTTPException
from typing import List, Optional
from src.schemas.rooms_s import RoomCreate, RoomResponse, RoomUpdate, RoomStatus, Corpus, Gender
from src.core.dependencies import PgnDepds, require_admin, get_current_user
from src.repositories.room_repo import RoomRepo
from src.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/available/", response_model=List[RoomResponse])
async def get_available_rooms(
    pgt: PgnDepds,
    corpus: Optional[Corpus] = Query(None),
    who: Optional[Gender] = Query(None),
    floor: Optional[int] = Query(None, ge=1, le=4),
    session: AsyncSession = Depends(get_session),
):
    repo = RoomRepo(session)
    rooms = await repo.get_available(
        page=pgt.page,
        per_page=pgt.per_page,
        corpus=corpus.value if corpus else None,
        who=who.value if who else None,
        floor=floor,
    )
    return rooms


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int, session: AsyncSession = Depends(get_session)):
    room = await RoomRepo(session).get_by_id(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.post("/add", response_model=RoomResponse, dependencies=[Depends(require_admin)])
async def create_room(room_data: RoomCreate, session: AsyncSession = Depends(get_session)):
    # Search online: "FastAPI dependencies protect route admin"
    data = room_data.model_dump()
    data["dormitory_id"] = 1 if data["corpus"] == "A" else 2  # A→1, B→2
    room = await RoomRepo(session).create(data)
    return room


@router.patch("/{room_id}", response_model=RoomResponse, dependencies=[Depends(require_admin)])
async def update_room(room_id: int, room_update: RoomUpdate, session: AsyncSession = Depends(get_session)):
    data = room_update.model_dump(exclude_none=True)
    room = await RoomRepo(session).update(room_id, data)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.delete("/{room_id}", dependencies=[Depends(require_admin)])
async def delete_room(room_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await RoomRepo(session).delete(room_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"status": "deleted"}
