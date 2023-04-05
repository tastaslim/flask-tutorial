import os
from flask import Flask
from flask_smorest import Api
from config import db
from middleware import register_jwt_middleware, apply_rate_limiter
from resources import StoreBlueprint, TagBlueprint, ItemBlueprint, UserBlueprint
# from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    load_dotenv()
    with app.app_context():
        app.config["API_TITLE"] = "Stores REST API"
        app.config["API_VERSION"] = "v1"
        app.config["OPENAPI_VERSION"] = "3.0.0"
        app.config["OPENAPI_URL_PREFIX"] = "/"
        app.config["OPENAPI_SWAGGER_UI_PATH"] = f"{os.getenv('API_VERSION')}/swagger"
        app.config[
            "OPENAPI_SWAGGER_UI_URL"
        ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
        app.config['API_SPEC_OPTIONS'] = {
            'security': [{"bearerAuth": []}, { "apiKey" : []}],
            'components': {
                "securitySchemes":
                {
                    "bearerAuth": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "Authorization",
                        "bearerFormat": "JWT",
                        "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
                    },
                    "apiKey":{
                        "type": "apiKey",
                        "in": "header",
                        "name": "x-api-key",
                        "description": "Enter your API KEY",
                    }
                }
            }
        }

        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('POSTGRES_DB_URL')
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["PROPAGATE_EXCEPTIONS"] = True

        app.config['SECRET_KEY'] = "POWER_FULL_SECRET_KEY"
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

        db.init_app(app)
        # app.config.from_object()
        migrate = Migrate()
        migrate.init_app(app, db)
        # csrf = CSRFProtect()
        # csrf.init_app(app)

        api = Api(app)
        # Store it in Some safe place
        # app.config['WTF_CSRF_SECRET_KEY'] = "CSRF_SECRET_KEY"

        register_jwt_middleware(app)
        apply_rate_limiter(app)
        api.register_blueprint(ItemBlueprint)
        api.register_blueprint(StoreBlueprint)
        api.register_blueprint(TagBlueprint)
        api.register_blueprint(UserBlueprint)
    
    @app.errorhandler(404)
    def not_found(e):
        return {
            "status": "Not Found",
            "code": 404, 
            "message" : "The resource doesn't exist"
        }
    
    @app.errorhandler(500)
    def internal_error(e):
        print(e)
        return {
            "status": "Internal Server Error",
            "code": 500, 
            "message" : e.message
        }

    return app
