from marshmallow import Schema, fields, validate


class Level8Schema(Schema):
    number = fields.Integer(required=True, validate=validate.Range(min=1, max=1000))


class SecretSchema(Schema):
    secret = fields.String(required=True)
