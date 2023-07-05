from dataclasses import dataclass
import os


@dataclass
class Config:
    broker: str
    port: int
    aggregator_topic: str
    analyzed_topic: str


def readConfig():
    return Config(
        os.environ.get("MQTT_HOST") or "localhost",
        os.environ.get("MQTT_PORT") or 1883,
        os.environ.get("MQTT_AGGREGATOR_TOPIC") or "aggregator/<aggregator-id>",
        os.environ.get("MQTT_ANALYZED_TOPIC") or "analyzed/<analyzed-id>",
    )


config = readConfig()
