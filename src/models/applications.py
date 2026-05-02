from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey, func
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.students import StudentModel


class ApplicationModel(BaseModel):
    __tablename__ = "applications"

    id_application: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id_student", ondelete="CASCADE"), nullable=False)
    corpus: Mapped[str] = mapped_column(String(1), nullable=False)
    preferred_floor: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # Relationships
    student: Mapped["StudentModel"] = relationship(back_populates="applications")