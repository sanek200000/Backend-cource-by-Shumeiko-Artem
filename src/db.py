from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from conf import settings


engine = create_async_engine(settings.DB_URL)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

ASYNC_SESSION_MAKER = async_sessionmaker(bind=engine, expire_on_commit=False)
ASYNC_SESSION_MAKER_NULL_POOL = async_sessionmaker(
    bind=engine_null_pool,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


## Пример использования
# import asyncio
# from sqlalchemy import text
# async def func():
#    async with engine.begin() as conn:
#        res = await conn.execute(text("select version()"))
#        print(res.fetchone())


# asyncio.run(func())
