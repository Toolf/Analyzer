from dataclasses import dataclass

from datetime import datetime
from domain.road_type import RoadType
from domain.accelerometer import Accelerometer
from domain.location import Location


@dataclass
class AnalyzedData:
    accelerometer: Accelerometer
    location: Location
    time: datetime
    road_type: RoadType
