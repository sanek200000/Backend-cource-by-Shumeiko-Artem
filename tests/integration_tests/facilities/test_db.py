from schemas.facilities import FacilitiesAdd


async def test_add_facility(db):
    data = FacilitiesAdd(title="Bar")
    await db.facilities.add(data)
    await db.commit()
