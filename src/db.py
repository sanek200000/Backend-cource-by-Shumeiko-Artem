from sqlalchemy.ext.asyncio import create_async_engine

from conf import settings


engine = create_async_engine(settings.DB_URL)


## Пример использования
# import asyncio
# from sqlalchemy import text
# async def func():
#    async with engine.begin() as conn:
#        res = await conn.execute(text("select version()"))
#        print(res.fetchone())


# asyncio.run(func())
