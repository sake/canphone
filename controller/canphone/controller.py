from .mqtt import MqttController, EventType
import json
import logging
from enum import Enum, auto


log = logging.getLogger("canphone")


class PhoneState(Enum):
    WAITING = auto()
    CALLING = auto()
    ESTABLISHED = auto()
    ACCEPTING = auto()
    RINGING = auto()
    HEARING = auto()
    SPEAKING = auto()


class CanController:

    def __init__(self):
        self.state = PhoneState.WAITING
        self.mqtt = MqttController()
        # register first callback
        self.mqtt.setCallback(self.__phoneCallback__)
        #self.peri.setCallback(self.__waitingForCanPickup__)

    def start(self):
        self.mqtt.connect(self.waitingState, "localhost")

    def stop(self):
        self.mqtt.disconnect()
        #self.peri.stop()
        
    def dial(self, phoneNumber: str):
        msgObj = {"command": "dial", "params": phoneNumber}
        msgStr = json.dumps(msgObj)
        self.mqtt.send_command(msgStr)

    # Callbacks interacting with the softphone

    def __phoneCallback__(self, evt: EventType, msg):
        log.debug("Callback received event=%s", evt)
        if evt is EventType.CALL_CLOSED:
            log.info("Going to waiting state after close message.")
            self.waitingState()
        elif evt is EventType.CALL_INCOMING:
            if self.state is PhoneState.WAITING:
                log.info("Incoming call.")
                self.ringingState()
        elif evt is EventType.CALL_ESTABLISHED:
            if self.state in { PhoneState.CALLING, PhoneState.ACCEPTING }:
                log.info("Establishing incoming call.")
                self.establishedState()

    # Peripheral callbacks

    def __canCallback__(self):
        # send call command
        msgStr = json.dumps({"command": "dialcontact"})
        self.mqtt.send_command(msgStr)

    def __pttCallback__(self):
        if self.state is PhoneState.HEARING:
            self.speakingState()
        elif self.state is PhoneState.SPEAKING:
            self.hearingState()


    # statemachine

    def waitingState(self):
        pass

    def callingState(self):
        pass

    def acceptingState(self):
        self.state = PhoneState.ACCEPTING
        # accept call
        msgObj = {"command": "accept"}
        msgStr = json.dumps(msgObj)
        self.mqtt.send_command(msgStr)

    def establishedState(self):
        pass

    def ringingState(self):
        pass
    
    def hearingState(self):
        pass

    def speakingState(self):
        pass
