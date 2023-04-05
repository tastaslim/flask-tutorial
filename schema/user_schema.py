from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True, require=False)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)
