from config.db import db
from config.redis import redis_cache
from config.allowed_urls import pass_api_key_check, pass_jwt_check
"""
args = {
    "host": "<<your host>>",
    "user": "<<your user>>",
    "dbname": "<<your dbname>>",
    "sslcert": "<<path to sslcert>>",
    "sslkey": "<<path to sslkey>>",
    "sslrootcert": "<<path to verification ca chain>>",
    "sslmode": "verify-full"
}
"""
BLOCKLIST = list()
X_API_KEY = '1234567890'