import logging
import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client: redis.Redis = None

    async def connect(self):
        logging.info(f"Начинаю подключение к Redis host={self.host} port={self.port}")
        self.client = redis.Redis(host=self.host, port=self.port)
        logging.info(f"Подключился к Redis host={self.host} port={self.port}")

    async def set(self, key: str, value: str, expire: int = None):
        await self.client.set(name=key, value=value, ex=expire)

    async def get(self, key):
        return await self.client.get(key)

    async def delete(self, key):
        await self.client.delete(key)

    async def close(self):
        if self.client:
            await self.client.close()
