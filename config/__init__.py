import os

from config.db import db

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
# DB_URL = f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PW")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}' if os.getenv(
#     'PYTHON_ENV') == 'LOCAL' else f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PW")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}?sslmode=require&sslcert={os.getenv("CA_CERT")}'
BLOCKLIST = list()
X_API_KEY = '1234567890'
