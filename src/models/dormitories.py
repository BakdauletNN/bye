from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class DormitoriesModel(BaseModel):
    __tablename__ = "dormitories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(2))