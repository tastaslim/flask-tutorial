from schema.schemas import PlainItemSchema, PlainStoreSchema, PlainTagSchema
from marshmallow import fields


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
