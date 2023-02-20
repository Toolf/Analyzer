from marshmallow import Schema, post_load, fields

from schema.road_type_schema import RoadTypeSchema
from schema.accelerometer_schema import AccelerometerSchema
from schema.location_schema import LocationSchema
from domain.analyzed_data import AnalyzedData
from domain.road_type import RoadType


class AnalyzedDataSchema(Schema):
    accelerometer = fields.Nested(AccelerometerSchema)
    location = fields.Nested(LocationSchema)
    time = fields.DateTime('iso')
    road_type = fields.Enum(RoadType, by_value=True)

    @post_load
    def to_domain(self, data, **kwargs):
        return AnalyzedData(**data)
