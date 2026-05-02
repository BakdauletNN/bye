from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.rooms import RoomModel



class DormitoriesModel(BaseModel):
    __tablename__ = "dormitories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    # Relationships
    rooms: Mapped[list["RoomModel"]] = relationship(back_populates="dormitory")

