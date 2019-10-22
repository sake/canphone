from .mqtt import MqttController, EventType
from .mixer import CanMixer
from .hwcontrols import PhoneControls, CanState, PttState
import json
import logging
from enum import Enum, auto
import threading


log = logging.getLogger("canphone")


class PhoneState(Enum):
    INIT = auto()
    WAITING = auto()
    CALLING = auto()
    ESTABLISHED = auto()
    ACCEPTING = auto()
    RINGING = auto()
    HEARING = auto()
    SPEAKING = auto()


class CanController:

    def __init__(self):
        self.state = PhoneState.INIT
        self.mqtt = MqttController()
        self.mixer = CanMixer()
        self.hw = PhoneControls(self.__pttCallback__, self.__canCallback__)
        self.lock = threading.Lock()

        # register callback
        self.mqtt.setCallback(self.__phoneCallback__)

    def start(self):
        self.mixer.mute()
        self.mqtt.connect(self.waitingState, "localhost")

    def stop(self):
        self.mqtt.disconnect()
        self.mixer.mute
        self.hw.stopBlinking()
        
    def dial(self, phoneNumber: str):
        msgObj = {"command": "dial", "params": phoneNumber}
        msgStr = json.dumps(msgObj)
        self.mqtt.send_command(msgStr)

    def dialMainContact(self):
        msgObj = {"command": "dialcontact"}
        msgStr = json.dumps(msgObj)
        self.mqtt.send_command(msgStr)

    def acceptCall(self):
        msgObj = {"command": "accept"}
        msgStr = json.dumps(msgObj)
        self.mqtt.send_command(msgStr)

    def hangupCall(self):
        msgObj = {"command": "hangup"}
        msgStr = json.dumps(msgObj)
        self.mqtt.send_command(msgStr)


    # Callbacks interacting with the softphone

    def __phoneCallback__(self, evt: EventType, msg):
        self.lock.acquire()
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
        self.lock.release()

    # Peripheral callbacks

    def __canCallback__(self, canStatus):
        self.lock.acquire()
        if canStatus == CanState.LIFTED:
            if self.state == PhoneState.WAITING:
                self.callingState()
            elif self.state == PhoneState.RINGING:
                self.acceptingState()
        elif canStatus == CanState.HUNGUP:
            if self.state in { PhoneState.CALLING, PhoneState.ESTABLISHED, PhoneState.HEARING, PhoneState.SPEAKING }:
                self.waitingState()
        self.lock.release()

    def __pttCallback__(self, pttStatus):
        self.lock.acquire()
        if self.state is PhoneState.HEARING:
            if pttStatus == PttState.PRESSED:
                self.speakingState()
        elif self.state is PhoneState.SPEAKING:
            if pttStatus == PttState.RELEASED:
                self.hearingState()
        self.lock.release()


    # statemachine

    def waitingState(self):
        log.debug("Waiting entered.")
        self.state = PhoneState.WAITING
        self.mixer.mute()
        self.hw.startBlinking() # wait blink
        self.hangupCall()

    def callingState(self):
        log.debug("Calling entered.")
        self.state = PhoneState.CALLING
        self.hw.startBlinking() # calling blink
        self.dialMainContact()

    def acceptingState(self):
        log.debug("Accepting entered.")
        self.state = PhoneState.ACCEPTING
        self.acceptCall()

    def establishedState(self):
        log.debug("Established entered.")
        self.state = PhoneState.ESTABLISHED
        self.hearingState()

    def ringingState(self):
        log.debug("Ringing entered.")
        self.state = PhoneState.RINGING
        self.hw.startBlinking() # ringing blink
    
    def hearingState(self):
        log.debug("Hearing entered.")
        self.state = PhoneState.HEARING
        self.mixer.listen()
        self.hw.stopBlinking()
        # TODO: set led

    def speakingState(self):
        log.debug("Speaking entered.")
        self.state = PhoneState.SPEAKING
        self.mixer.speak()
        # TODO: set led
