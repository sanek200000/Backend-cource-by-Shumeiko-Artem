from schemas.facilities import FacilitiesAdd
from services.base import BaseService
from tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_all_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, facility_data: FacilitiesAdd):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()

        test_task.delay()

        return facility
