from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from pydantic import EmailStr
from sqlalchemy import DateTime
from datetime import datetime


class StudentModel(BaseModel):
    __tablename__ = "students"
    id_student: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)
    course: Mapped[int]
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

