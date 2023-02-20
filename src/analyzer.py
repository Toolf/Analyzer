from domain.aggregated_data import AggregatedData
from domain.road_type import RoadType


class Analyzer:
    def analyze(self, data: AggregatedData) -> RoadType:
        if abs(data.accelerometer.z) > 16000:
            return RoadType.LargePits
        elif abs(data.accelerometer.z) > 12000:
            return RoadType.SmallPits
        elif abs(data.accelerometer.z) > 8000:
            return RoadType.Curb
        else:
            return RoadType.Nice
