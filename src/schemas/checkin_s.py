from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class CheckinCreate(BaseModel):
    student_id: int
    room_id: int


class CheckinResponse(BaseModel):
    id_checkin: int
    student_id: int
    room_id: int
    checkin_date: datetime
    checkout_date: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)