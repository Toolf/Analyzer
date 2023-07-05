from enum import Enum
from sqlalchemy import (
    Column,
    Enum as SQLAlchemyEnum,
    Float,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from ..db import Base

from domain.road_type import RoadType
from domain.analyzed_data import AnalyzedData
from domain.accelerometer import Accelerometer
from domain.location import Location


class AnalyzedDataModel(Base):
    __tablename__ = "analyzed_data"

    id = Column(Integer, primary_key=True)
    accelerometer_id = Column(Integer, ForeignKey("accelerometer.id"))
    location_id = Column(Integer, ForeignKey("location.id"))
    time = Column(DateTime)
    road_type = Column(SQLAlchemyEnum(RoadType))

    accelerometer = relationship("AccelerometerModel")
    location = relationship("LocationModel")

    @classmethod
    def from_dataclass(cls, analyzed_data: AnalyzedData) -> "AnalyzedDataModel":
        return cls(
            time=analyzed_data.time,
            road_type=analyzed_data.road_type,
            accelerometer=AccelerometerModel.from_dataclass(
                analyzed_data.accelerometer
            ),
            location=LocationModel.from_dataclass(analyzed_data.location),
        )


class LocationModel(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    longitude = Column(Float)
    latitude = Column(Float)

    @classmethod
    def from_dataclass(cls, location: Location) -> "LocationModel":
        return cls(longitude=location.longitude, latitude=location.latitude)


class AccelerometerModel(Base):
    __tablename__ = "accelerometer"

    id = Column(Integer, primary_key=True)
    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)

    @classmethod
    def from_dataclass(cls, accelerometer: Accelerometer) -> "AccelerometerModel":
        return cls(x=accelerometer.x, y=accelerometer.y, z=accelerometer.z)
