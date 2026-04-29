from src.database.database import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Column, Boolean


class UserModel(BaseModel):
    __tablename__ = "users"
    id_user: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int]
    username: Mapped[str]
    password_hash = Column(String(255), nullable=False)
    role: Mapped[str]
    is_registered: Mapped[bool]
    
    