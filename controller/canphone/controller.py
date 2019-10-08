from .mqtt import MqttController, EventType
import json
import logging


log = logging.getLogger("canphone")


class CanController:

    def __init__(self):
        self.mqtt = MqttController()
        # callback shortcuts
        self.cb1 = lambda evt, msg: self.__waitingForCall__(evt, msg)
        # register first callback
        self.mqtt.setCallback(self.cb1)

    def start(self):
        self.mqtt.connect("localhost")

    def stop(self):
        self.mqtt.disconnect()
        
    def dial(self, phoneNumber: str):
        msgObj = {"command": "dial", "params": phoneNumber}
        msgStr = json.dumps(msgObj)
        self.mqtt.send_command(msgStr)

    # Callbacks interacting with the softphone

    def __waitingForCall__(self, evt: EventType, msg):
        if evt is EventType.CALL_INCOMING:
            log.info("Accepting incoming call.")
            msgObj = {"command": "accept"}
            msgStr = json.dumps(msgObj)
            self.mqtt.send_command(msgStr)
