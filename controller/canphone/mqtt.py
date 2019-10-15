from paho.mqtt.client import Client, MQTTMessage, MQTT_ERR_SUCCESS
import logging
import json
from json import JSONDecodeError
from enum import Enum, auto
from typing import Dict, Callable, Optional
import threading


log = logging.getLogger("canphone")


class EventType(Enum):
    REGISTER_OK = auto()
    CALL_RINGING = auto()
    CALL_ESTABLISHED = auto()
    CALL_CLOSED = auto()
    CALL_INCOMING = auto()

EventCallback = Callable[[EventType, Dict], None]

class MqttController:
    def __init__(self):
        self.client = Client()
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.evtCallback: Optional[EventCallback] = None

    def connect(self, connectCallback, host, port=1883, keepalive=60):
        log.info("Trying to connect MQTT client.")
        self.connectCallback = connectCallback
        self.client.connect(host, port, keepalive)
        self.client.loop_start()

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def setCallback(self, callback: EventCallback):
        self.evtCallback = callback

    def delCallback(self):
        self.evtCallback = None

    def __on_connect(self, client, userdata, flags, rc):
        log.info("MQTT client connected, registering subscriptions.")
        self.client.subscribe("/baresip/event")
        self.connectCallback()

    def __on_message(self, client, userdata, msg: MQTTMessage):
        log.info("MQTT message received for path=%s.", msg.topic)
        log.debug("payload=%s", msg.payload)

        # parse message
        try:
            msgObj = json.loads(msg.payload)
            evtType = EventType[msgObj["type"]]

            # notify respective callback
            cb = self.evtCallback
            if cb is not None:
                log.debug("Calling event callback in a thread.")
                t = threading.Thread(target=lambda: cb(evtType, msgObj))
                t.start()
            else:
                log.debug("No callback registered.")
        except JSONDecodeError:
            log.error("Received invalid JSON message.")
        except KeyError:
            log.warn("Received unhandled type code or type code is missing.")

    def send_command(self, msg):
        log.debug("Trying to send message %s to phone.", msg)
        info = self.client.publish("/baresip/command/", msg)
        log.debug("Waiting for publish")
        log.debug(info.rc)
        info.wait_for_publish()
        if info.rc != MQTT_ERR_SUCCESS:
            log.error("Failed to publish message")
        else:
            log.debug("Message sent successfully.")
