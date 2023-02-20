from marshmallow import Schema, fields

from domain.road_type import RoadType


class RoadTypeSchema(Schema):
    road_type = fields.Enum(RoadType, by_value=True)
