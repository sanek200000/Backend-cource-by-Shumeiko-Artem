import json
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from main import app
from conf import SETTINGS
from db import Base, engine_null_pool
from models import *


meta = Base.metadata
BASE_URL = "http://test"
USER_DATA = {"name": "user", "email": "sdfsf@fdsf.ru", "password": "111"}


def load_mock_data(filename: str) -> list[dict]:
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data


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
        base_url=BASE_URL,
    ) as client:
        response = await client.post(url="/auth/register", json=USER_DATA)

        assert response.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def get_access_token(register_user):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=BASE_URL,
    ) as client:
        response = await client.post(url="/auth/login", json=USER_DATA)

        assert response.status_code == 200

        access_tocken = response.json().get("access_tocken")
        assert access_tocken is not None

        yield access_tocken


@pytest.fixture(scope="session", autouse=True)
async def add_hotels(async_main) -> None:

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=BASE_URL,
    ) as client:

        data = load_mock_data("/src/tests/mock_hotels.json")
        for hotel in data:
            response = await client.post(url="/hotels/", json=hotel)

            assert response.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def add_rooms(get_access_token) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=BASE_URL,
    ) as client:

        data = load_mock_data("/src/tests/mock_rooms.json")
        for room in data:
            hotel_id = room.get("hotel_id")
            response = await client.post(
                url=f"/hotels/{hotel_id}/rooms/",
                json=room,
                headers={"access_tocken": get_access_token},
            )

            assert response.status_code == 200
