from fastapi import APIRouter, Depends, HTTPException
from src.schemas.apl_s import ApplicationCreate, ApplicationResponse, ApplicationStatusUpdate
from src.repositories.apl_repo import ApplicationRepo
from src.database.database import get_session
from src.core.dependencies import PgnDepds, require_manager, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter(prefix="/applications", tags=["Applications"])


# Search online: "FastAPI post create resource SQLAlchemy"
@router.post("/", response_model=ApplicationResponse)
async def create_application(
    data: ApplicationCreate,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    app = await ApplicationRepo(session).create(
        student_id=current_user.student_id,
        corpus=data.corpus,
        preferred_floor=data.preferred_floor,
    )
    return app


@router.get("/my", response_model=List[ApplicationResponse])
async def my_applications(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await ApplicationRepo(session).get_by_student(current_user.student_id)


@router.get("/", response_model=List[ApplicationResponse], dependencies=[Depends(require_manager)])
async def get_all_applications(pgt: PgnDepds, session: AsyncSession = Depends(get_session)):
    apps, _ = await ApplicationRepo(session).get_all(pgt.page, pgt.per_page)
    return apps


@router.patch("/{app_id}/status", response_model=ApplicationResponse, dependencies=[Depends(require_manager)])
async def update_status(
    app_id: int,
    data: ApplicationStatusUpdate,
    session: AsyncSession = Depends(get_session),
):
    if data.status not in ("pending", "approved", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status")
    app = await ApplicationRepo(session).update_status(app_id, data.status)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app
