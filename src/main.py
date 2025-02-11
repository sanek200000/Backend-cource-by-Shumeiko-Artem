from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api.auth import router as router_auth
from api.hotels import router as router_hotels
from api.rooms import router as router_rooms
from api.bookings import router as router_bookings
from api.facilities import router as router_facilities
from api.images import router as router_images

from init import redis_manager


logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.client), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
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
app.include_router(router_images)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
