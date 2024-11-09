from typing import Any
from fastapi import Body, FastAPI, Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "best hotel in Sochi"},
    {"id": 2, "title": "Dubai", "name": "best hotel in Dubai"},
]


@app.get("/")
def func() -> list[dict[str, Any]]:
    return hotels


@app.get("/hotels")
def get_hotels(
    id: int,
    title: str = Query(description="Название отеля"),
) -> list[dict[str, Any]]:
    return [h for h in hotels if h["title"] == title and h["id"] == id]


@app.post("/hotels")
def create_hotel(title: str = Body(embed=True)) -> dict[str, str]:
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title})
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def modify_hotel(
    hotel_id: int,
    title: str | None = Body(description="Название отеля"),
    name: str | None = Body(description="Наименование отеля"),
) -> dict[str, str]:
    if not (name or title) or (name == "" or title == ""):
        return {"status": "not OK"}

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}")
def modify_hotel(
    hotel_id: int,
    title: str | None = Body(description="Название отеля"),
    name: str | None = Body(description="Наименование отеля"),
) -> dict[str, str]:
    if not (name and title) or (name == "" and title == ""):
        return {"status": "not OK"}

    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title and title != "":
                hotel["title"] = title
            if name and name != "":
                hotel["name"] = name
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int) -> dict[str, str]:
    global hotels
    hotels = [h for h in hotels if h["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
