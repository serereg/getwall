from typing import AsyncIterator

from aioredis import Redis, from_url


async def init_redis_pool(host: str, password: str) -> AsyncIterator[Redis]:
    session = from_url(
        f"redis://{host}", password=password, encoding="utf-8", decode_responses=True
    )
    yield session
    session.close()
    await session.wait_closed()
