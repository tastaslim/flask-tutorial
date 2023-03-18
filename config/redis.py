import redis
redis_cache = redis.Redis(host='localhost', port=6379, db=0, password="localhost")
