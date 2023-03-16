import os
from flask import Flask, jsonify
from flask_smorest import Api
from config import DB_URL, db
from middleware import register_jwt_middleware
from resources import StoreBlueprint, TagBlueprint, ItemBlueprint, UserBlueprint
# from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.9"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['API_SPEC_OPTIONS'] = {
        'security': [{"bearerAuth": []}],
        'components': {
            "securitySchemes":
            {
                "bearerAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization",
                    "bearerFormat": "JWT",
                    "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
                }
            }
        }
    }

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or DB_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    app.config['SECRET_KEY'] = "POWER_FULL_SECRET_KEY"
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)
    # csrf = CSRFProtect()
    # csrf.init_app(app)

    api = Api(app)
    # Store it in Some safe place
    # app.config['WTF_CSRF_SECRET_KEY'] = "CSRF_SECRET_KEY"

    register_jwt_middleware(app)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
