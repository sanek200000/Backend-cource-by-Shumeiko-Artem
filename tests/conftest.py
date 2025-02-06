import json
import os
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from typing import AsyncGenerator, Generator
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy.ext.asyncio import create_async_engine

from api.dependences import get_db
from main import app
from conf import SETTINGS
from db import ASYNC_SESSION_MAKER_NULL_POOL, Base, engine_null_pool
from models import *
from schemas.facilities import FacilitiesAdd
from schemas.hotels import HotelAdd
from schemas.rooms import RoomAdd
from utils.db_manager import DBManager


meta = Base.metadata
USER_DATA = {"name": "user", "email": "sdfsf@fdsf.ru", "password": "111"}


@pytest.fixture(scope="session", autouse=True)
async def async_main() -> None:
    assert SETTINGS.MODE == "TEST"


async def get_db_nullpool() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=ASYNC_SESSION_MAKER_NULL_POOL) as db:
        yield db


@pytest.fixture(scope="function")
async def db(async_main) -> AsyncGenerator[DBManager, None]:
    async for db in get_db_nullpool():
        yield db


app.dependency_overrides[get_db] = get_db_nullpool


@pytest.fixture(scope="session")
async def ac(async_main) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


def load_mock_data(filename: str) -> list[dict]:
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


@pytest.fixture(scope="session", autouse=True)
async def setup_database(async_main) -> None:
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)

    hotels_data = load_mock_data("mock_hotels.json")
    rooms_data = load_mock_data("mock_rooms.json")
    facilities_data = load_mock_data("mock_facilitieas.json")

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels_data]
    rooms = [RoomAdd.model_validate(room) for room in rooms_data]
    facilities = [
        FacilitiesAdd.model_validate(facility) for facility in facilities_data
    ]

    async with DBManager(ASYNC_SESSION_MAKER_NULL_POOL) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.facilities.add_bulk(facilities)
        await db_.commit()


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    response = await ac.post(url="/auth/register", json=USER_DATA)

    assert response.status_code == 200


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database, ac):
    response = await ac.post(url="/auth/register", json=USER_DATA)

    assert response.status_code == 200


@pytest.fixture(scope="session")
async def login_user(register_user, ac):
    response = await ac.post(url="/auth/login", json=USER_DATA)

    assert response.status_code == 200
    assert ac.cookies.get("access_tocken")

    yield ac
