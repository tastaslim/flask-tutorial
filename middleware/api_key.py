from functools import wraps
from flask import request
def verify_api_key():
    def _verify_api_key(function_on_which_middleware_is_applied):
        @wraps(function_on_which_middleware_is_applied)
        def __verify_api_key(*args, **kwargs):
            if not request.headers.get('x-api-key') or request.headers.get('x-api-key') != '1234567890':
                return {"message": "API Key is either Invalid or Missing", "error": "INVALID_OR_MISSING_KEY", "code" : 400}
            result = function_on_which_middleware_is_applied(*args, **kwargs)
            return result
        return __verify_api_key
    return _verify_api_key
