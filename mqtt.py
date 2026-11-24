import json
from datetime import datetime

import paho.mqtt.client as paho

from consts import MQTT_HOST, MQTT_PORT, MQTT_TOPIC

client = paho.Client(paho.CallbackAPIVersion.VERSION2)


def connect():
    client.connect_async(MQTT_HOST, MQTT_PORT)
    client.loop_start()  # thread réseau en tâche de fond, gère la reconnexion


def publish(text):
    payload = {"text": text, "timestamp": datetime.now().astimezone().isoformat()}
    client.publish(MQTT_TOPIC, json.dumps(payload, ensure_ascii=False), qos=1)
