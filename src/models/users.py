from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.students import StudentModel

class UserModel(BaseModel):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id_student", ondelete="CASCADE"), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, server_default="student")
    is_registered: Mapped[bool] = mapped_column(nullable=False, server_default="true")

    # Relationships
    student: Mapped["StudentModel"] = relationship(back_populates="user")
    


