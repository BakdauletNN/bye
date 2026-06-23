from fastapi import APIRouter, Depends, HTTPException
from src.schemas.checkin_s import CheckinCreate, CheckinResponse
from src.repositories.checkin_repo import CheckinRepo
from src.repositories.room_repo import RoomRepo
from src.database.database import get_session
from src.core.dependencies import require_manager
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

# Only manager and admin manage check-ins
router = APIRouter(
    prefix="/checkins",
    tags=["Checkins"],
    dependencies=[Depends(require_manager)],
)


@router.post("/", response_model=CheckinResponse)
async def checkin(data: CheckinCreate, session: AsyncSession = Depends(get_session)):
    room = await RoomRepo(session).get_by_id(data.room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if room.status != "a":
        raise HTTPException(status_code=400, detail="Room is not available")

    active = await CheckinRepo(session).get_active_by_student(data.student_id)
    if active:
        raise HTTPException(status_code=400, detail="Student already checked in")

    checkin = await CheckinRepo(session).create(data.student_id, data.room_id)
    await RoomRepo(session).update(data.room_id, {"status": "o"})
    return checkin


@router.post("/{checkin_id}/checkout", response_model=CheckinResponse)
async def checkout(checkin_id: int, session: AsyncSession = Depends(get_session)):
    checkin = await CheckinRepo(session).checkout(checkin_id)
    if not checkin:
        raise HTTPException(status_code=404, detail="Checkin not found")

    await RoomRepo(session).update(checkin.room_id, {"status": "a"})
    return checkin


@router.get("/active", response_model=List[CheckinResponse])
async def get_active_checkins(session: AsyncSession = Depends(get_session)):
    return await CheckinRepo(session).get_all_active()
