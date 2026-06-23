from enum import Enum
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Optional


class Corpus(str, Enum):
    A = "A"
    B = "B"


class Gender(str, Enum):
    MALE = "m"
    FEMALE = "f"


class RoomStatus(str, Enum):
    AVAILABLE = "a"
    OCCUPIED = "o"
    MAINTENANCE = "m"


class RoomCreate(BaseModel):
    floor: int = Field(..., ge=1, le=4)
    number: int = Field(..., ge=100, le=499)
    qty_person: int = Field(default=4, ge=1, le=8)
    who: Gender
    corpus: Corpus

    @model_validator(mode="after")
    def check_floor_matches_number(self) -> "RoomCreate":
        if self.number // 100 != self.floor:
            raise ValueError(f"Room number must start with floor digit: {self.floor}XX")
        return self


class RoomResponse(BaseModel):
    id_room: int
    dormitory_id: int
    floor: int
    number: int
    qty_person: int
    who: Gender
    corpus: Corpus
    status: RoomStatus

    #Source:"Pydantic v2 from_attributes ORM mode"
    model_config = ConfigDict(from_attributes=True)


class RoomUpdate(BaseModel):
    floor: Optional[int] = Field(None, ge=1, le=4)
    number: Optional[int] = Field(None, ge=100, le=499)
    who: Optional[Gender] = None
    status: Optional[RoomStatus] = None