import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage
import signal
import time
from sqlalchemy.orm import sessionmaker

from schema.aggregated_data_schema import AggregatedDataSchema
from schema.analyzed_data_schema import AnalyzedDataSchema
from domain.aggregated_data import AggregatedData
from domain.analyzed_data import AnalyzedData
from repository.model.analyzed_data_model import AnalyzedDataModel
from repository.db import engine, Base, is_connected_to_db
from analyzer import Analyzer
from config import config


while not is_connected_to_db():
    print("Waiting for the database...")
    time.sleep(5)


# Create database session
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

analyzer = Analyzer()


def on_message(client, userdata, message: MQTTMessage):
    # Extract JSON data
    jsonData = message.payload.decode("utf-8")

    # Convert JSON to object
    data: AggregatedData = AggregatedDataSchema().loads(jsonData)

    # Analyze data
    roadType = analyzer.analyze(data)

    # Prepare result
    res = AnalyzedData(
        accelerometer=data.accelerometer,
        location=data.location,
        time=data.time,
        road_type=roadType,
    )

    # Save analyzed data to database
    try:
        analyzed_data_model = AnalyzedDataModel.from_dataclass(res)
        session.add(analyzed_data_model)
        session.commit()
    except Exception as e:
        print(f"Failed to save analyzed data to the database:", e)
        return

    # Convert object to JSON
    json_res = AnalyzedDataSchema().dumps(res)

    # Publish analyzed data
    publish_result = client.publish(config.analyzed_topic, json_res)
    status = publish_result[0]

    if status == 0:
        pass
    else:
        print(f"Failed to send message to topic {config.analyzed_topic}")


# Create MQTT client
client = mqtt.Client()
client.connect(config.broker, config.port)
client.subscribe(config.aggregator_topic)
client.on_message = on_message


# Docker stop handler
def exit_gracefully():
    client.loop_stop()
    session.close()
    exit(0)


# Set up signal handler for graceful exit
signal.signal(signal.SIGTERM, exit_gracefully)


# Start MQTT client loop
client.loop_forever()
