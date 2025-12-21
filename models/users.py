from pydantic import BaseModel, Field
from enum import Enum


class UserRole(str, Enum):
    guest = "guest"
    admin = "admin"


class UserRegister(BaseModel):
    first_name: str = Field(..., example="Ivan")
    last_name: str = Field(..., example="Ivanov")
    phone: str = Field(..., example="+79998887766")
    email: str = Field(..., example="ivan@example.com")
    password: str = Field(..., example="strong_password")
    role: UserRole = UserRole.guest

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "phone": "+79998887766",
                "email": "ivan@example.com",
                "password": "strong_password",
                "role": "guest"
            }
        }


class UserLogin(BaseModel):
    email: str = Field(..., example="ivan@example.com")
    password: str = Field(..., example="strong_password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "ivan@example.com",
                "password": "strong_password"
            }
        }


class UserInDB(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str
    password: str
    role: UserRole


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str
    role: UserRole

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Ivan",
                "last_name": "Ivanov",
                "phone": "+79998887766",
                "email": "ivan@example.com",
                "role": "guest"
            }
        }
