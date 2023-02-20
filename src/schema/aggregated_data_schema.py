from marshmallow import Schema, post_load, fields
from schema.accelerometer_schema import AccelerometerSchema
from schema.location_schema import LocationSchema

from domain.aggregated_data import AggregatedData


class AggregatedDataSchema(Schema):
    accelerometer = fields.Nested(AccelerometerSchema)
    location = fields.Nested(LocationSchema)
    time = fields.DateTime('iso')

    @post_load
    def to_domain(self, data, **kwargs):
        return AggregatedData(**data)
