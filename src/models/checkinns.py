from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime
from datetime import datetime


class CheckinsModel(BaseModel):
    __tablename__ = "checkins"
    id_checkin: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int]
    room_id: Mapped[int]
    checkin_date: Mapped[datetime] = mapped_column(DateTime)
    checkout_date: Mapped[datetime] = mapped_column(DateTime)