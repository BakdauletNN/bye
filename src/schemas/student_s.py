from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class StudentCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., max_length=100)
    gender: str = Field(..., pattern="^[mf]$")  # Pydantic v2: pattern вместо regex
    course: int = Field(..., ge=1, le=6)
    phone: str = Field(..., min_length=6, max_length=20)


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[str] = Field(None, max_length=100)
    gender: Optional[str] = Field(None, pattern="^[mf]$")
    course: Optional[int] = Field(None, ge=1, le=6)
    phone: Optional[str] = Field(None, min_length=6, max_length=20)


class StudentResponse(BaseModel):
    id_student: int
    first_name: str
    last_name: str
    email: str
    gender: str
    course: int
    phone: Optional[str] = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class StudentList(BaseModel):
    total: int
    students: list[StudentResponse]