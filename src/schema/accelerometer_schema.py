from marshmallow import Schema, post_load, fields

from domain.accelerometer import Accelerometer


class AccelerometerSchema(Schema):
    x = fields.Int()
    y = fields.Int()
    z = fields.Int()

    @post_load
    def to_domain(self, data, **kwargs):
        return Accelerometer(**data)
