from fastapi import APIRouter, HTTPException, status
from typing import List
from models.rooms import RoomCreate, RoomUpdate, RoomInDB, RoomOut

router = APIRouter(prefix="/rooms", tags=["Rooms"])

rooms_db: list[RoomInDB] = []
room_id_counter = 1


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_room(data: RoomCreate):
    global room_id_counter

    for room in rooms_db:
        if room.room_number == data.room_number and room.floor == data.floor:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room already exists on this floor"
            )

    new_room = RoomInDB(
        id=room_id_counter,
        **data.dict()
    )

    rooms_db.append(new_room)
    room_id_counter += 1

    return {
        "message": "Room created successfully"
    }


@router.get("/", response_model=List[RoomOut])
def get_all_rooms():
    return rooms_db


@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int):
    for room in rooms_db:
        if room.id == room_id:
            return room

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )


@router.put("/{room_id}")
def update_room(room_id: int, data: RoomUpdate):
    for room in rooms_db:
        if room.id == room_id:
            if data.price_per_night is not None:
                room.price_per_night = data.price_per_night
            if data.area is not None:
                room.area = data.area
            if data.description is not None:
                room.description = data.description

            return {
                "message": "Room updated successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )


@router.delete("/{room_id}")
def delete_room(room_id: int):
    for index, room in enumerate(rooms_db):
        if room.id == room_id:
            rooms_db.pop(index)
            return {
                "message": "Room deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Room not found"
    )
