import pytest
from sqlalchemy.ext.asyncio import create_async_engine

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
