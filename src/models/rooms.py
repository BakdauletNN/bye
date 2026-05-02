from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UniqueConstraint, ForeignKey
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.checkinns import CheckinsModel
    from src.models.dormitories import DormitoriesModel


class RoomModel(BaseModel):
    __tablename__ = "rooms"
    __table_args__ = (UniqueConstraint("number", "corpus", name="uq_room_number_corpus"),)

    id_room: Mapped[int] = mapped_column(primary_key=True)
    dormitory_id: Mapped[int] = mapped_column(ForeignKey("dormitories.id", ondelete="RESTRICT"), nullable=False)
    floor: Mapped[int] = mapped_column(nullable=False)
    number: Mapped[int] = mapped_column(nullable=False)
    qty_person: Mapped[int] = mapped_column(nullable=False, server_default="4")
    who: Mapped[str] = mapped_column(String(1), nullable=False)
    corpus: Mapped[str] = mapped_column(String(1), nullable=False)
    status: Mapped[str] = mapped_column(String(1), nullable=False, server_default="a")

    # Relationships
    dormitory: Mapped["DormitoriesModel"] = relationship(back_populates="rooms")
    checkins: Mapped[list["CheckinsModel"]] = relationship(back_populates="room")


