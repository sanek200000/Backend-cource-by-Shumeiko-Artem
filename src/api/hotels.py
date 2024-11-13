from typing import Any
from fastapi import Body, Query, APIRouter
from sqlalchemy import insert

from api.dependences import PaginationDep
from models.hotels import HotelsOrm
from schemas.hotels import Hotel, HotelPatch

from db import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get(
    "/",
    summary="Получить список всех отелей",
    description="Получить список всех отелей",
)
def get_hotels(pgntn: PaginationDep) -> list[dict[str, Any]]:
    if pgntn.page and pgntn.per_page:
        l = (pgntn.page - 1) * pgntn.per_page
        r = pgntn.page * pgntn.per_page
        result = hotels[l:r]

        if result:
            return result
        return [{"status": "Out of range"}]

    return hotels


@router.get(
    "",
    summary="Получить информацию об отеле",
    description="Получить информацию об отеле по его id или названию",
)
def get_hotel(
    pgntn: PaginationDep,
    id: int | None = Query(None),
    title: str | None = Query(None, description="Название отеля"),
) -> list[dict[str, Any]]:

    hotels_ = list()
    for hotel in hotels:
        if id and hotel["id"] == id:
            hotels_.append(hotel)
        if title and hotel["title"] == title:
            hotels_.append(hotel)

    if pgntn.page and pgntn.per_page:
        return hotels_[pgntn.per_page * (pgntn.page - 1) :][: pgntn.per_page]
    return hotels


@router.post("/", summary="Добавить отель в список")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {"title": "Сочи", "location": "ул. Моря, д.1"},
            },
            "2": {
                "summary": "Дубай",
                "value": {"title": "Дубай", "location": "ул. Абракадабры, д.2"},
            },
        }
    )
) -> dict[str, str]:

    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Обновление информации об отеле",
    description="Обновление информации об отеле",
)
def modify_hotel(hotel_id: int, hotel_data: Hotel) -> dict[str, str]:
    if hotel_data.name == "" or hotel_data.title == "":
        return {"status": "not OK"}

    global hotels
    hotel = [h for h in hotels if h["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление информации об отеле",
    description="Частичное обновление информации об отеле",
)
def modify_hotel(hotel_id: int, hotel_data: HotelPatch) -> dict[str, str]:
    global hotels
    hotel = [h for h in hotels if h["id"] == hotel_id][0]
    if hotel_data.title and hotel_data.title != "":
        hotel["title"] = hotel_data.title
    if hotel_data.name and hotel_data.name != "":
        hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление информации об отеле из БД",
    description="Удаление информации об отеле из БД",
)
def delete_hotel(hotel_id: int) -> dict[str, str]:
    global hotels
    hotels = [h for h in hotels if h["id"] != hotel_id]
    return {"status": "OK"}
