import json
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from main import app
from conf import SETTINGS
from db import Base, engine_null_pool
from models import *


meta = Base.metadata


@pytest.fixture(scope="session", autouse=True)
async def async_main() -> None:
    assert SETTINGS.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)


@pytest.fixture(scope="session", autouse=True)
async def register_user(async_main):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            url="/auth/register",
            json={
                "name": "user",
                "email": "sdfsf@fdsf.ru",
                "password": "111",
            },
        )

        assert response.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def login_user(register_user):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            url="/auth/login",
            json={
                "name": "user",
                "email": "sdfsf@fdsf.ru",
                "password": "111",
            },
        )

        assert response.status_code == 200

        access_tocken = response.json().get("access_tocken")
        assert access_tocken is not None

        yield access_tocken


def load_mock_data(filename: str):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


@pytest.fixture(scope="session", autouse=True)
async def add_hotels(async_main):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        data: list[dict] = load_mock_data("/src/tests/mock_hotels.json")
        for hotel in data:
            response = await client.post(url="/hotels/", json=hotel)

            assert response.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def add_rooms(login_user):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        data: list[dict] = load_mock_data("/src/tests/mock_rooms.json")
        for room in data:
            hotel_id = room.get("hotel_id")
            response = await client.post(
                url=f"/hotels/{hotel_id}/rooms/",
                json=room,
                headers={"access_tocken": login_user},
            )

            assert response.status_code == 200
