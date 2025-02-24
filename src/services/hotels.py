from datetime import date

from fastapi import HTTPException
from api.dependences import PaginationDep
from exceptions import (
    DateToEaelierDateFromException,
    HotelNotFoundException,
    ObjictNotFoundException,
)
from schemas.hotels import HotelAdd, HotelPatch
from services.base import BaseService


class HotelService(BaseService):

    async def get_filtred_by_time(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date,
    ):

        per_page = pagination.per_page or 5

        return await self.db.hotels.get_filtred_by_time(
            date_from=date_from,
            date_to=date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_all_hotels(self):
        return await self.db.hotels.get_all()

    async def create_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def put_hotel(self, id: int, data: HotelAdd):
        await self.db.hotels.edit(data, id=id)
        await self.db.commit()

    async def patch_hotel(self, id: int, data: HotelPatch):
        await self.db.hotels.edit(data, exclude_unset=True, id=id)
        await self.db.commit()

    async def delete_hotel(self, id: int):
        await self.db.hotels.delete(id=id)
        await self.db.commit()

    async def get_hotel_with_check(self, id: int):
        """Checking the existence of a hotel by its `id`

        Args:
            id (int): hotel id

        Raises:
            HotelNotFoundException: Hotel with this `id` not found
        """
        try:
            await self.db.hotels.get_one(id=id)
        except ObjictNotFoundException:
            raise HotelNotFoundException
