from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
def apply_rate_limiter(app):
    Limiter(key_func = get_remote_address, app=app, default_limits=["50/minute"], storage_uri="redis://localhost:6379", storage_options={})
    @app.errorhandler(429)
    def rate_limit_handler(e):
        return { "code" : 429, "message" : "You have exceeded your rate-limit. Please try after some time."}
    