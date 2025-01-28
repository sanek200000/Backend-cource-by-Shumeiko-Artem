import json
from fastapi import APIRouter, Body

from api.dependences import DB_DEP
from schemas.facilities import FacilitiesAdd
from utils.openapi_examples import FacilitiesOE
from init import redis_manager

router = APIRouter(prefix="/facilities", tags=["Удобства в номерах"])


@router.get("/", summary="Посмотреть список удобств")
async def get_all_facilities(db: DB_DEP):
    facilities_from_cache = await redis_manager.get("facilities")
    print(f"{facilities_from_cache = }")

    if not facilities_from_cache:
        print("ИДУ В БАЗУ")
        facilities = await db.facilities.get_all()
        facilities_schema = [f.model_dump() for f in facilities]
        facilities_json = json.dumps(facilities_schema)
        await redis_manager.set("facilities", facilities_json, 10)

        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)
        return facilities_dicts


@router.post("/", summary="Добавить вид удобства")
async def create_facility(
    db: DB_DEP,
    facility_data: FacilitiesAdd = Body(openapi_examples=FacilitiesOE.create),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}
