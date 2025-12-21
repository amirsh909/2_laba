from fastapi import APIRouter, HTTPException, status
from typing import List
from models.bookings import BookingCreate, BookingInDB, BookingOut, BookingStatus

router = APIRouter(prefix="/bookings", tags=["Bookings"])

bookings_db: list[BookingInDB] = []
booking_id_counter = 1


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_booking(data: BookingCreate):
    global booking_id_counter

    # Проверка корректности дат
    if data.start_date >= data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )

    # Проверка доступности номера
    for booking in bookings_db:
        if (
            booking.room_id == data.room_id
            and booking.status == BookingStatus.active
            and not (data.end_date <= booking.start_date or data.start_date >= booking.end_date)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is already booked for selected dates"
            )

    new_booking = BookingInDB(
        id=booking_id_counter,
        user_id=data.user_id,
        room_id=data.room_id,
        start_date=data.start_date,
        end_date=data.end_date,
        status=BookingStatus.active
    )

    bookings_db.append(new_booking)
    booking_id_counter += 1

    return {
        "message": "Booking created successfully"
    }


@router.get("/", response_model=List[BookingOut])
def get_all_bookings():
    return bookings_db


@router.get("/user/{user_id}", response_model=List[BookingOut])
def get_user_bookings(user_id: int):
    user_bookings = [b for b in bookings_db if b.user_id == user_id]

    if not user_bookings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No bookings found for this user"
        )

    return user_bookings


@router.put("/{booking_id}/cancel")
def cancel_booking(booking_id: int):
    for booking in bookings_db:
        if booking.id == booking_id:
            if booking.status == BookingStatus.cancelled:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Booking is already cancelled"
                )

            booking.status = BookingStatus.cancelled
            return {
                "message": "Booking cancelled successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Booking not found"
    )
