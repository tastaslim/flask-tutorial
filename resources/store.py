from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from flask_jwt_extended import jwt_required
from config import db
from models import StoreModel
from schema import StoreSchema


StoreBlueprint = Blueprint(
    "Stores", "stores", description="Operations on stores")


@StoreBlueprint.route("/store/<string:store_id>")
class Store(MethodView):
    @jwt_required()
    @StoreBlueprint.response(200, StoreSchema)
    def get(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            return store
        except Exception as e:
            print(e)
            abort(
                500, message=f"An error occurred while getting the itemId {store_id}")

    @jwt_required()
    @StoreBlueprint.response(204, None)
    def delete(self, store_id):
        try:
            store = StoreModel.query.get_or_404(store_id)
            db.session.delete(store)
            db.session.commit()
            return {"message": "Store deleted"}, 200
        except SQLAlchemyError:
            abort(
                500, message=f"An error occurred deleting the store {store_id}")
        except Exception as e:
            abort(500, message=f"An error occurred {e}")


@StoreBlueprint.route("/store")
class StoreList(MethodView):
    @jwt_required()
    @StoreBlueprint.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @jwt_required()
    @StoreBlueprint.arguments(StoreSchema)
    @StoreBlueprint.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store
