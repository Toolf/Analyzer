import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage

from schema.aggregated_data_schema import AggregatedDataSchema
from schema.analyzed_data_schema import AnalyzedDataSchema
from domain.aggregated_data import AggregatedData
from domain.analyzed_data import AnalyzedData
from analyzer import Analyzer
from config import config


analyzer = Analyzer()


def on_message(client, userdata, message: MQTTMessage):
    # print(
    #     "Received message | topic: {}, qos: {}, retain: {}, payload:{}"
    #     .format(
    #         message.topic,
    #         message.qos,
    #         message.retain,
    #         message.payload.decode('utf-8')
    #     )
    # )
    # == Take json data ==
    jsonData = message.payload.decode('utf-8')
    # == Convert json to object ==
    data: AggregatedData = AggregatedDataSchema().loads(jsonData)
    # == Analyze data ==
    roadType = analyzer.analyze(data)
    # == Publish analyzed data ==
    # prepare result
    res = AnalyzedData(
        accelerometer=data.accelerometer,
        location=data.location,
        time=data.time,
        road_type=roadType
    )
    # convert object to json
    json_res = AnalyzedDataSchema().dumps(res)
    # publish
    publish_result = client.publish(config.analyzed_topic, json_res)
    status = publish_result[0]
    if status == 0:
        pass
        # print(f"Send `{json_res}` to topic `{config.analyzed_topic}`")
    else:
        print(f"Failed to send message to topic {config.analyzed_topic}")


client = mqtt.Client()
client.connect(config.broker, config.port)
client.subscribe(config.aggregator_topic)
client.on_message = on_message
client.loop_forever()
