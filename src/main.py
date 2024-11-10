from fastapi import FastAPI

from hotels import router as router_hotels

app = FastAPI()
app.include_router(router_hotels)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
