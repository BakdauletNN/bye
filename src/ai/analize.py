from fastapi import APIRouter, Depends
from src.database.database import get_session
from src.core.dependencies import require_manager
from src.models.rooms import RoomModel
from src.models.checkinns import CheckinsModel
from src.models.applications import ApplicationModel
from src.models.students import StudentModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

# Search online: "SQLAlchemy aggregate functions count group by async"
router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    dependencies=[Depends(require_manager)],
)


@router.get("/rooms/summary")
async def rooms_summary(session: AsyncSession = Depends(get_session)):
    """Rooms summary: total, available, occupied, maintenance"""
    result = await session.execute(
        select(RoomModel.status, func.count().label("count")).group_by(RoomModel.status)
    )
    rows = result.all()
    mapping = {"a": "available", "o": "occupied", "m": "maintenance"}
    summary = {mapping.get(r.status, r.status): r.count for r in rows}
    total = sum(summary.values())
    return {"total": total, **summary}


@router.get("/rooms/by-corpus")
async def rooms_by_corpus(session: AsyncSession = Depends(get_session)):
    """Load by dormitory building"""
    result = await session.execute(
        select(
            RoomModel.corpus,
            func.count().label("total"),
            func.sum(
                func.cast(RoomModel.status == "o", type_=func.count().type)
            ).label("occupied"),
        ).group_by(RoomModel.corpus)
    )
    rows = result.all()
    return [
        {
            "corpus": r.corpus,
            "total": r.total,
            "occupied": r.occupied or 0,
            "available": r.total - (r.occupied or 0),
        }
        for r in rows
    ]


@router.get("/applications/summary")
async def applications_summary(session: AsyncSession = Depends(get_session)):
    """Applications summary: pending / approved / rejected"""
    result = await session.execute(
        select(ApplicationModel.status, func.count().label("count"))
        .group_by(ApplicationModel.status)
    )
    rows = result.all()
    return {r.status: r.count for r in rows}


@router.get("/checkins/active-count")
async def active_checkins_count(session: AsyncSession = Depends(get_session)):
    """Number of students currently checked in"""
    result = await session.execute(
        select(func.count()).where(CheckinsModel.checkout_date.is_(None))
    )
    count = result.scalar()
    return {"active_checkins": count}


@router.get("/students/by-course")
async def students_by_course(session: AsyncSession = Depends(get_session)):
    """Number of students by course"""
    result = await session.execute(
        select(StudentModel.course, func.count().label("count"))
        .group_by(StudentModel.course)
        .order_by(StudentModel.course)
    )
    rows = result.all()
    return [{"course": r.course, "count": r.count} for r in rows]
