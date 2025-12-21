from fastapi import FastAPI
import uvicorn

from routes.users import router as users_router
from routes.rooms import router as rooms_router
from routes.bookings import router as bookings_router

app = FastAPI(
    title="Hotel Microservices API",
    description="Educational microservice-based hotel booking system",
    version="1.0"
)


app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(bookings_router)


@app.get("/")
def root():
    return {"message": "Hotel API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
