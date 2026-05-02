from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from sqlalchemy import DateTime, func
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.applications import ApplicationModel
    from src.models.checkinns import CheckinsModel
    from src.models.users import UserModel


class StudentModel(BaseModel):
    __tablename__ = "students"

    id_student: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)
    course: Mapped[int] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relationships with other tables in Database
    user: Mapped["UserModel"] = relationship(back_populates="student", uselist=False)
    applications: Mapped[list["ApplicationModel"]] = relationship(back_populates="student")
    checkins: Mapped[list["CheckinsModel"]] = relationship(back_populates="student")