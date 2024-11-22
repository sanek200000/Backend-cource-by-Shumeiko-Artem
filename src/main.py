from fastapi import FastAPI

from api.auth import router as router_auth
from api.hotels import router as router_hotels
from api.rooms import router as router_rooms
from api.bookings import router as router_bookings
from api.facilities import router as router_facilities

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
