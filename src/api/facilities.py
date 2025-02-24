from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache


from api.dependences import DB_DEP
from schemas.facilities import FacilitiesAdd
from services.facilities import FacilityService
from tasks.tasks import test_task
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
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
