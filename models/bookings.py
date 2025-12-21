from pydantic import BaseModel, Field
from enum import Enum
from datetime import date


class BookingStatus(str, Enum):
    active = "ACTIVE"
    cancelled = "CANCELLED"


class BookingCreate(BaseModel):
    user_id: int = Field(..., example=1)
    room_id: int = Field(..., example=2)
    start_date: date = Field(..., example="2025-05-10")
    end_date: date = Field(..., example="2025-05-15")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "room_id": 2,
                "start_date": "2025-05-10",
                "end_date": "2025-05-15"
            }
        }


class BookingInDB(BaseModel):
    id: int
    user_id: int
    room_id: int
    start_date: date
    end_date: date
    status: BookingStatus


class BookingOut(BookingInDB):
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "room_id": 2,
                "start_date": "2025-05-10",
                "end_date": "2025-05-15",
                "status": "ACTIVE"
            }
        }
