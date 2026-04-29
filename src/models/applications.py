from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime


class ApplicationModel(BaseModel):
    __tablename__ = "applications"
    id_application: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int]
    corpus: Mapped[str] = mapped_column(String(1))
    preferred_floor: Mapped[int]
    status: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

