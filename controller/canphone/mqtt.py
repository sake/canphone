from paho.mqtt.client import Client, MQTTMessage, MQTT_ERR_SUCCESS
import logging

log = logging.getLogger("canphone")

class MqttController:
    def __init__(self):
        self.client = Client()
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message

    def connect(self, host, port=1883, keepalive=60):
        log.info("Trying to connect MQTT client.")
        self.client.connect(host, port, keepalive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def __on_connect(self, client, userdata, flags, rc):
        log.info("MQTT client connected, registering subscriptions.")
        self.client.subscribe("/baresip/event")

    def __on_message(self, client, userdata, msg: MQTTMessage):
        log.info("MQTT message received.")
        log.debug("payload=%s", msg.payload)
        

    def send_command(self, msg):
        info = self.client.publish("/baresip/command/", msg)
        info.wait_for_publish()
        if info.rc != MQTT_ERR_SUCCESS:
            log.error("Failed to publish message")
