from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, func
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.rooms import RoomModel
    from src.models.students import StudentModel


class CheckinsModel(BaseModel):
    __tablename__ = "checkins"

    id_checkin: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id_student", ondelete="CASCADE"), nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id_room", ondelete="RESTRICT"), nullable=False
    )
    checkin_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    checkout_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    # Relationships
    student: Mapped["StudentModel"] = relationship(back_populates="checkins")
    room: Mapped["RoomModel"] = relationship(back_populates="checkins")
