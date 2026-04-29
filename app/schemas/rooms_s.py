from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Optional


class Corpus(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Gender(str, Enum):
    MALE = "m"
    FEMALE = "f"


class RoomStatus(str, Enum):
    AVAILABLE = "a"
    OCCUPIED = "o"
    MAINTENANCE = "m"


class RoomCreate(BaseModel): 
    floor: int = Field(..., ge=1, le=5)
    number: int = Field(..., ge=100, le=599)
    qty_person: int = Field(default=4, ge=1, le=4)
    who: Gender
    corpus: Corpus

    @model_validator(mode='after')
    def check_floor_matches_number(self) -> 'RoomCreate':
        if self.number // 100 != self.floor:
            raise ValueError(
                f"Enter between {self.floor}01-{self.floor}99"
            )
        return self


class RoomResponse(BaseModel): 
    id_room: int 
    floor: int
    number: int
    qty_person: int
    who: Gender
    corpus: Corpus
    status: RoomStatus = RoomStatus.AVAILABLE


class RoomUpdate(BaseModel):
    floor: Optional[int] = Field(None, ge=1, le=5)
    number: Optional[int] = Field(None, ge=100, le=599)
    who: Optional[Gender] = None
    status: Optional[RoomStatus] = None