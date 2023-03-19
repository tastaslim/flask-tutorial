from functools import wraps
from flask import request
from dotenv import load_dotenv
import os
load_dotenv()

def verify_api_key():
    def _verify_api_key(f):
        @wraps(f)
        def __verify_api_key(*args, **kwargs):
            if not request.headers.get('x-api-key') or request.headers.get('x-api-key') != os.getenv('API_KEY'):
                return {"message": "API Key is either Invalid or Missing", "error": "INVALID_OR_MISSING_KEY", "code" : 400}
            result = f(*args, **kwargs)
            return result
        return __verify_api_key
    return _verify_api_key
