from typing import Any
from fastapi import Body, FastAPI, Query

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "best hotel in Sochi"},
    {"id": 2, "title": "Dubai", "name": "best hotel in Dubai"},
]


@app.get(
    "/",
    summary="Получить список всех отелей",
    description="Получить список всех отелей",
)
def func() -> list[dict[str, Any]]:
    return hotels


@app.get(
    "/hotels",
    summary="Получить информацию об отеле",
    description="Получить информацию об отеле по его id или названию",
)
def get_hotels(
    id: int,
    title: str = Query(description="Название отеля"),
) -> list[dict[str, Any]]:
    return [h for h in hotels if h["title"] == title and h["id"] == id]


@app.post("/hotels", summary="Добавить отель в список")
def create_hotel(title: str = Body(embed=True)) -> dict[str, str]:
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1, "title": title})
    return {"status": "OK"}


@app.put(
    "/hotels/{hotel_id}",
    summary="Обновление информации об отеле",
    description="Обновление информации об отеле",
)
def modify_hotel(
    hotel_id: int,
    title: str = Body(description="Название отеля"),
    name: str = Body(description="Наименование отеля"),
) -> dict[str, str]:
    if name == "" or title == "":
        return {"status": "not OK"}

    global hotels
    hotel = [h for h in hotels if h["id"] == hotel_id][0]
    hotel["title"] = title
    hotel["name"] = name
    return {"status": "OK"}


@app.patch(
    "/hotels/{hotel_id}",
    summary="Частичное обновление информации об отеле",
    description="Частичное обновление информации об отеле",
)
def modify_hotel(
    hotel_id: int,
    title: str | None = Body(default=None, description="Название отеля"),
    name: str | None = Body(default=None, description="Наименование отеля"),
) -> dict[str, str]:
    global hotels
    hotel = [h for h in hotels if h["id"] == hotel_id][0]
    if title and title != "":
        hotel["title"] = title
    if name and name != "":
        hotel["name"] = name
    return {"status": "OK"}


@app.delete(
    "/hotels/{hotel_id}",
    summary="Удаление информации об отеле из БД",
    description="Удаление информации об отеле из БД",
)
def delete_hotel(hotel_id: int) -> dict[str, str]:
    global hotels
    hotels = [h for h in hotels if h["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True, host="0.0.0.0")
