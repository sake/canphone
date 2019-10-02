 # localhost:1883
 # mosquitto_pub -t /baresip/command/ -m '{"command":"hangup"}'                                                                                                                                                                                                                           ✔  4814  22:08:15
 # mosquitto_pub -t /baresip/command/ -m '{"command":"accept"}'

from .mqtt import MqttController

class CanController:

    def __init__(self):
        self.mqtt = MqttController()

    def start(self):
        self.mqtt.connect("localhost")

    def stop(self):
        self.mqtt.disconnect()
        