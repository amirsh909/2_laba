from fastapi import APIRouter, HTTPException, status
from typing import List
from models.users import UserRegister, UserLogin, UserInDB, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

users_db: list[UserInDB] = []
user_id_counter = 1


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(data: UserRegister):
    global user_id_counter

    for user in users_db:
        if user.email == data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

    new_user = UserInDB(
        id=user_id_counter,
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        email=data.email,
        password=data.password,
        role=data.role
    )

    users_db.append(new_user)
    user_id_counter += 1

    return {
        "message": "User signed up successfully"
    }


@router.post("/login")
def login_user(data: UserLogin):
    for user in users_db:
        if user.email == data.email and user.password == data.password:
            return {
                "message": "User signed in successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password"
    )


@router.get("/", response_model=List[UserOut])
def get_all_users():
    return [UserOut(**user.dict()) for user in users_db]


@router.get("/{email}", response_model=UserOut)
def get_user_by_email(email: str):
    for user in users_db:
        if user.email == email:
            return UserOut(**user.dict())

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

