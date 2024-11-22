from fastapi import APIRouter, Body

from api.dependences import DB_DEP
from schemas.facilities import FacilitiesAdd


router = APIRouter(prefix="/facilities", tags=["Удобства в номерах"])


@router.get("/", summary="Посмотреть список удобств")
async def get_all_facilities(db: DB_DEP):
    return await db.facilities.get_all()


@router.post("/", summary="Добавить вид удобства")
async def create_facility(
    db: DB_DEP,
    facility_data: FacilitiesAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Internet",
                "value": {
                    "title": "WiFi",
                },
            },
            "2": {
                "summary": "Жакузя",
                "value": {
                    "title": "Жакузя",
                },
            },
            "3": {
                "summary": "Туалет",
                "value": {
                    "title": "Туалет",
                },
            },
        }
    ),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    return {"status": "OK", "data": facility}
