from datetime import date
from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache

from api.dependences import DB_DEP, PaginationDep
from schemas.hotels import HotelAdd, HotelPatch
from utils.openapi_examples import HotelsOE

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/", summary="Получение список отелей")
@router.get("", summary="Получение список отелей")
@cache(expire=10)
async def get_hotel_by_id(db: DB_DEP):
    return await db.hotels.get_all()


@router.get("/{hotel_id}", summary="Получить информацию об отеле")
@cache(expire=10)
async def get_hotel(
    pgntn: PaginationDep,
    db: DB_DEP,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date = Query(example="2024-11-01"),
    date_to: date = Query(example="2024-11-08"),
):
    per_page = pgntn.per_page or 5

    return await db.hotels.get_filtred_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pgntn.page - 1),
    )


@router.post("/", summary="Добавить отель в список")
async def create_hotel(
    db: DB_DEP,
    hotel_data: HotelAdd = Body(openapi_examples=HotelsOE.create),
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
async def edit_hotel(db: DB_DEP, hotel_id: int, hotel_data: HotelPatch):
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
