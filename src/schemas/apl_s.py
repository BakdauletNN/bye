from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ApplicationCreate(BaseModel):
    corpus: str
    preferred_floor: int


class ApplicationResponse(BaseModel):
    id_application: int
    student_id: int
    corpus: str
    preferred_floor: int
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ApplicationStatusUpdate(BaseModel):
    status: str  # pending / approved / rejected
