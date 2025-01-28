from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.auth import router as router_auth
from api.hotels import router as router_hotels
from api.rooms import router as router_rooms
from api.bookings import router as router_bookings
from api.facilities import router as router_facilities
from utils.openapi_examples import AuthOE

from init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте
    await redis_manager.connect()

    yield

    # При выключении/перезагрузке
    await redis_manager.close()


# никогда на dev ветке не пиши этот атрибут `docs_url=None`
app = FastAPI(lifespan=lifespan)
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
