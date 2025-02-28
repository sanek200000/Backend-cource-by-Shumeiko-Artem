from datetime import date
from asyncpg import PostgresSyntaxError, UniqueViolationError
from fastapi import Body, HTTPException, Query, APIRouter
from fastapi_cache.decorator import cache

from api.dependences import DB_DEP, PaginationDep
from exceptions import (
    DateToEaelierDateFromException,
    DateToEaelierDateFromHTTPException,
    HotelAlradyExistHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    NoDataHTTPException,
)
from schemas.hotels import HotelAdd, HotelPatch
from services.hotels import HotelService
from utils.openapi_examples import HotelsOE

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", summary="Получение список отелей")
@cache(expire=10)
async def get_hotel_by_id(db: DB_DEP):
    return await HotelService(db).get_all_hotels()


@router.get("/filter", summary="Список отелей по фильтру")
@cache(expire=10)
async def get_hotel(
    pagination: PaginationDep,
    db: DB_DEP,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Адрес отеля"),
    date_from: date = Query(example="2024-11-01"),
    date_to: date = Query(example="2024-11-08"),
):

    try:
        return await HotelService(db).get_filtred_by_time(
            pagination,
            title,
            location,
            date_from,
            date_to,
        )
    except DateToEaelierDateFromException as ex:
        raise DateToEaelierDateFromHTTPException


@router.post("", summary="Добавить отель в список")
async def create_hotel(
    db: DB_DEP,
    hotel_data: HotelAdd = Body(openapi_examples=HotelsOE.create),
):
    try:
        hotel = await HotelService(db).create_hotel(hotel_data)
    except UniqueViolationError:
        raise HotelAlradyExistHTTPException
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Обновление информации об отеле",
    description="Обновление информации об отеле",
)
async def modify_hotel(db: DB_DEP, hotel_id: int, hotel_data: HotelAdd):
    try:
        await HotelService(db).put_hotel(hotel_id, hotel_data)
    except UniqueViolationError:
        raise HotelAlradyExistHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление информации об отеле",
    description="Частичное обновление информации об отеле",
)
async def edit_hotel(db: DB_DEP, hotel_id: int, hotel_data: HotelPatch):
    try:
        await HotelService(db).patch_hotel(hotel_id, hotel_data)
    except UniqueViolationError:
        raise HotelAlradyExistHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except PostgresSyntaxError:
        raise NoDataHTTPException
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление информации об отеле из БД",
    description="Удаление информации об отеле из БД",
)
async def delete_hotel(db: DB_DEP, hotel_id: int):
    try:
        await HotelService(db).delete_hotel(hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}
