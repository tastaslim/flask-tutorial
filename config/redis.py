import redis
import os
redis_cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True, encoding="utf-8", password = os.getenv('REDIS_PASSWORD')) # type: ignore