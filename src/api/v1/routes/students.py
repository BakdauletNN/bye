from fastapi import APIRouter, Query, Depends, HTTPException
from typing import List, Optional
from src.schemas.student_s import StudentCreate, StudentResponse, StudentUpdate
from src.core.dependencies import PgnDepds, require_admin
from src.repositories.student_repo import StudentRepo
from src.database.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=List[StudentResponse])
async def list_students(
    pgt: PgnDepds,
    session: AsyncSession = Depends(get_session),
):
    students, _ = await StudentRepo(session).get_all(pgt.page, pgt.per_page)
    return students


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)):
    student = await StudentRepo(session).get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.post("/add", response_model=StudentResponse, dependencies=[Depends(require_admin)])
async def create_student(student_data: StudentCreate, session: AsyncSession = Depends(get_session)):
    student = await StudentRepo(session).create(student_data.model_dump())
    return student


@router.patch("/{student_id}", response_model=StudentResponse, dependencies=[Depends(require_admin)])
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    session: AsyncSession = Depends(get_session),
):
    student = await StudentRepo(session).update(student_id, student_data.model_dump(exclude_none=True))
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.delete("/{student_id}", dependencies=[Depends(require_admin)])
async def delete_student(student_id: int, session: AsyncSession = Depends(get_session)):
    deleted = await StudentRepo(session).delete(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"status": "deleted"}
