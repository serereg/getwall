"""Services module."""

from aioredis import Redis

EXPIRATION_TIME = 10


class Service:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def set(self, key, value) -> None:
        await self._redis.set(key, value, ex=EXPIRATION_TIME)

    async def get(self, key) -> str:
        return await self._redis.get(key)
