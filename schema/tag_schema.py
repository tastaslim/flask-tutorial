from schema import ItemSchema
from marshmallow import Schema, fields

from schema.schemas import PlainItemSchema, PlainStoreSchema, PlainTagSchema


class TagSchema(PlainTagSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)


class TagAndItemSchema(Schema):
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
    message = fields.Str()
