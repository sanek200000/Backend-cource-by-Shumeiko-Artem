from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def func() -> str:
    return "Hello World!!!!!!!!!!"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
