from pydantic import BaseModel, Field
from typing import Optional


class RoomBase(BaseModel):
    room_number: int = Field(..., example=101)
    floor: int = Field(..., example=1)
    price_per_night: float = Field(..., example=4500.0)
    area: float = Field(..., example=28.5)
    description: Optional[str] = Field(
        None, example="Comfortable room with a double bed"
    )


class RoomCreate(RoomBase):
    class Config:
        json_schema_extra = {
            "example": {
                "room_number": 101,
                "floor": 1,
                "price_per_night": 4500.0,
                "area": 28.5,
                "description": "Comfortable room with a double bed"
            }
        }


class RoomUpdate(BaseModel):
    price_per_night: Optional[float] = Field(None, example=4800.0)
    area: Optional[float] = Field(None, example=30.0)
    description: Optional[str] = Field(
        None, example="Updated description"
    )


class RoomInDB(RoomBase):
    id: int


class RoomOut(RoomInDB):
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "room_number": 101,
                "floor": 1,
                "price_per_night": 4500.0,
                "area": 28.5,
                "description": "Comfortable room with a double bed"
            }
        }
