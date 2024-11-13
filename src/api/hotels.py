from typing import Any
from fastapi import Body, Query, APIRouter
from sqlalchemy import insert, select

from api.dependences import PaginationDep
from models.hotels import HotelsOrm
from schemas.hotels import Hotel, HotelPatch

from db import async_session_maker, engine

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get(
    "",
    summary="Получить информацию об отеле",
    description="Получить информацию об отеле по его id или названию",
)
async def get_hotel(
    pgntn: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
):

    per_page = pgntn.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        if title:
            query = query.filter(HotelsOrm.title.like(f"%{title}%"))
        if location:
            query = query.filter(HotelsOrm.location.like(f"%{location}%"))
        query = query.limit(per_page).offset(per_page * (pgntn.page - 1))

        result = await session.execute(query)

        hotels = result.scalars().all()
        [print(f"{hotel.id}\t{hotel.title}\t{hotel.location}") for hotel in hotels]
        return hotels


@router.post("/", summary="Добавить отель в список")
async def create_hotel(
    hotel_data: Hotel = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи1",
                "value": {
                    "title": "Атрия",
                    "location": "Адлерский район, улица Мира, д.44 а, Сочи",
                },
            },
            "2": {
                "summary": "Сочи2",
                "value": {
                    "title": "Радуга-Престиж",
                    "location": "Краснодарский край, г. Сочи, ул. Пирогова, д. 2/3",
                },
            },
            "3": {
                "summary": "Дубай1",
                "value": {
                    "title": "Отель Al Khoory Executive Hotel",
                    "location": "Al Wasl Area, Dubai, Дубай",
                },
            },
            "4": {
                "summary": "Дубай2",
                "value": {
                    "title": "Holiday Inn Express Dubai Internet City an IHG Hotel",
                    "location": "Knowledge Village Pob 282647, Дубай",
                },
            },
        }
    )
):

    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(
            add_hotel_stmt.compile(bind=engine, compile_kwargs={"literal_binds": True})
        )
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Обновление информации об отеле",
    description="Обновление информации об отеле",
)
def modify_hotel(hotel_id: int, hotel_data: Hotel):
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
def modify_hotel(hotel_id: int, hotel_data: HotelPatch):
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
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [h for h in hotels if h["id"] != hotel_id]
    return {"status": "OK"}
