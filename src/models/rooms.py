from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class RoomModel(BaseModel):
    __tablename__ = "rooms"
    id_room: Mapped[int] = mapped_column(primary_key=True)
    floor: Mapped[int]
    number: Mapped[int]
    qty_person: Mapped[int]
    who: Mapped[str] = mapped_column(String(1))
    corpus: Mapped[str] = mapped_column(String(1))
    status: Mapped[str] = mapped_column(String(1))