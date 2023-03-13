from functools import wraps
from flask import request

from flask_smorest import abort
from config import X_API_KEY


def verify_x_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        API_Key = request.headers.get('x-api-key')
        if not API_Key or API_Key != X_API_KEY:
            abort(400, message=f"Invalid Key")
        return f(API_Key, *args, **kwargs)
    return decorated
