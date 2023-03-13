from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from config import db
from middleware.api_key import verify_x_api_key
from models import ItemModel
from schema import ItemSchema, ItemUpdateSchema

ItemBlueprint = Blueprint("Items", "items", description="Operations on items")


@ItemBlueprint.route("/item/<string:item_id>")
class Item(MethodView):

    @jwt_required()
    @ItemBlueprint.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    @ItemBlueprint.response(204, None)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @jwt_required()
    @ItemBlueprint.arguments(ItemUpdateSchema)
    @ItemBlueprint.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item


@ItemBlueprint.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @verify_x_api_key
    @ItemBlueprint.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @ItemBlueprint.arguments(ItemSchema)
    @ItemBlueprint.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
