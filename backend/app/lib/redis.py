from redis import Redis
from core.config import REDIS_PORT, REDIS_HOST


Redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
)
