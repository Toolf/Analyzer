from marshmallow import Schema, post_load, fields

from domain.location import Location


class LocationSchema(Schema):
    longitude = fields.Number()
    latitude = fields.Number()

    @post_load
    def to_domain(self, data, **kwargs):
        return Location(**data)
