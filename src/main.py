from typing import Any
from fastapi import FastAPI, Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Dubai"},
]


@app.get("/hotels")
def get_hotels(
    id: int,
    title: str = Query(description="Название отеля"),
) -> list[dict[str, Any]]:
    return [h for h in hotels if h["title"] == title and h["id"] == id]


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int) -> dict[str, str]:
    global hotels
    hotels = [h for h in hotels if h["id"] != hotel_id]
    return {"status": "OK"}


@app.get("/")
def func() -> list[dict[str, Any]]:
    return hotels


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
