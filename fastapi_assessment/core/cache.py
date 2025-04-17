"""Cache Module.

Description:
- This module provides caching functionality using Redis.

"""

from collections.abc import Awaitable
from typing import Any

import orjson
import redis

from fastapi_assessment.core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
)


def set_cached_data(key: str, value: Any, expire: int = 3600) -> None:
    """Set data in Redis cache.

    :Description:
    - This function sets data in the Redis cache with an expiration time in
    seconds.

    :Args:
    - `key` (str): The key to store the data in the cache. **(Required)**
    - `value` (Any): The data to be cached. **(Required)**
    - `expire` (int): The expiration time in seconds. **(Optional)**

    :Returns:
    - `None`

    """
    redis_client.setex(name=key, time=expire, value=orjson.dumps(value))


def get_cached_data(key: str) -> Any | None:
    """Get data from Redis cache.

    :Description:
    - This function retrieves data from the Redis cache using the provided key.

    :Args:
    - `key` (str): The key to retrieve data from the cache. **(Required)**

    :Returns:
    - `data` (Any | None): The cached data if found, otherwise None.

    """
    data: Awaitable[Any] | Any = redis_client.get(name=key)

    if data:
        return orjson.loads(str(data))

    return None


def delete_cached_data(key: str) -> None:
    """Delete data from Redis cache.

    :Description:
    - This function deletes data from the Redis cache using the provided key.

    :Args:
    - `key` (str): The key to delete data from the cache. **(Required)**

    :Returns:
    - `None`

    """
    redis_client.delete(key)


def clear_cache() -> None:
    """Clear all data from Redis cache.

    :Description:
    - This function clears all data from the Redis cache.

    :Args:
    - `None`

    :Returns:
    - `None`

    """
    redis_client.flushall()
