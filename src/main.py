from fastapi import FastAPI

from api.auth import router as router_auth
from api.hotels import router as router_hotels
from api.rooms import router as router_rooms

app = FastAPI()
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
