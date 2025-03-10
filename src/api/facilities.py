from asyncpg import UniqueViolationError
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache


from api.dependences import DB_DEP
from exceptions import FacilityAlradyExistHTTPException
from schemas.facilities import FacilitiesAdd
from services.facilities import FacilityService
from utils.openapi_examples import FacilitiesOE

router = APIRouter(prefix="/facilities", tags=["Удобства в номерах"])


@router.get("", summary="Посмотреть список удобств")
@cache(expire=10)
async def get_all_facilities(db: DB_DEP):
    return await FacilityService(db).get_all_facilities()


@router.post("", summary="Добавить вид удобства")
async def create_facility(
    db: DB_DEP,
    facility_data: FacilitiesAdd = Body(openapi_examples=FacilitiesOE.create),
):
    try:
        facility = await FacilityService(db).create_facility(facility_data)
    except UniqueViolationError:
        raise FacilityAlradyExistHTTPException
    return {"status": "OK", "data": facility}
