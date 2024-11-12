from sqlalchemy.ext.asyncio import async_session, create_async_engine

from conf import settings


engine = create_async_engine(settings.DB_URL)

async_session_maker = async_session(bind=engine, expire_on_commit=False)

## Пример использования
# import asyncio
# from sqlalchemy import text
# async def func():
#    async with engine.begin() as conn:
#        res = await conn.execute(text("select version()"))
#        print(res.fetchone())


# asyncio.run(func())
