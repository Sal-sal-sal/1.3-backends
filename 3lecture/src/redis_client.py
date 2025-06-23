import redis
import redis.asyncio as aioredis
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Redis client (sync)
redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)

# Asynchronous Redis client (for FastAPI, async tasks)
async def get_async_redis():
    return aioredis.from_url(settings.redis_url, decode_responses=True)

# Test connection (sync)
def test_redis_connection():
    try:
        redis_client.ping()
        logger.info("Redis connection successful")
        return True
    except redis.ConnectionError:
        logger.error("Redis connection failed")
        return False

# Redis utility functions (sync)
def set_value(key: str, value: str, expire: int = None):
    """Set a value in Redis with optional expiration"""
    if expire:
        redis_client.setex(key, expire, value)
    else:
        redis_client.set(key, value)

def get_value(key: str):
    """Get a value from Redis"""
    return redis_client.get(key)

def delete_key(key: str):
    """Delete a key from Redis"""
    return redis_client.delete(key)

def exists(key: str):
    """Check if a key exists in Redis"""
    return redis_client.exists(key)

# Redis utility functions (async)
async def async_set_value(key: str, value: str, expire: int = None):
    """Set a value in Redis asynchronously with optional expiration"""
    redis = await get_async_redis()
    if expire:
        await redis.setex(key, expire, value)
    else:
        await redis.set(key, value)
    await redis.close()

async def async_get_value(key: str):
    """Get a value from Redis asynchronously"""
    redis = await get_async_redis()
    value = await redis.get(key)
    await redis.close()
    return value

async def async_delete_key(key: str):
    """Delete a key from Redis asynchronously"""
    redis = await get_async_redis()
    result = await redis.delete(key)
    await redis.close()
    return result

async def async_exists(key: str):
    """Check if a key exists in Redis asynchronously"""
    redis = await get_async_redis()
    result = await redis.exists(key)
    await redis.close()
    return result