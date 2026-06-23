from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ApplicationCreate(BaseModel):
    corpus: str = Field(..., pattern="^[A-D]$")
    preferred_floor: int = Field(..., ge=1, le=4)


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