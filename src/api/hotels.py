from fastapi import Body, Query, APIRouter

from api.dependences import DB_DEP, PaginationDep
from schemas.hotels import HotelAdd, HotelPatch

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/{hotel_id}", summary="Получение информыции об отеле по его id")
async def get_hotel_by_id(db: DB_DEP, hotel_id: int):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.get(
    "",
    summary="Получить информацию об отеле",
    description="Получить информацию об отеле по его id или названию",
)
async def get_hotel(
    pgntn: PaginationDep,
    db: DB_DEP,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
):
    per_page = pgntn.per_page or 5

    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pgntn.page - 1),
    )


@router.post("/", summary="Добавить отель в список")
async def create_hotel(
    db: DB_DEP,
    hotel_data: HotelAdd = Body(
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
    ),
):

    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Обновление информации об отеле",
    description="Обновление информации об отеле",
)
async def modify_hotel(db: DB_DEP, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление информации об отеле",
    description="Частичное обновление информации об отеле",
)
async def modify_hotel(db: DB_DEP, hotel_id: int, hotel_data: HotelPatch):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление информации об отеле из БД",
    description="Удаление информации об отеле из БД",
)
async def delete_hotel(db: DB_DEP, hotel_id: int):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "OK"}
