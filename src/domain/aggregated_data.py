from dataclasses import dataclass

from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.location import Location


@dataclass
class AggregatedData:
    accelerometer: Accelerometer
    location: Location
    time: datetime
