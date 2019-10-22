import threading
from gpiozero import LED, Button, Device, Pin
from gpiozero.pins.mock import MockFactory
from signal import pause
from time import sleep
from enum import Enum, auto


#Device.pin_factory = MockFactory()


class CanState(Enum):
    LIFTED = auto()
    HUNGUP = auto()

class PttState(Enum):
    PRESSED = auto()
    RELEASED = auto()

class PhoneControls:
    def __init__(self,  callbPush, callbHang, led = LED(17), pushToTalkButton = Device.pin_factory.pin(18), hangUpButton = Device.pin_factory.pin(19), isItBlinking = False):
        # define properties
        self.led = led
        self.isItBlinking = isItBlinking
        self.pushToTalkButton = pushToTalkButton
        self.hangUpButton = hangUpButton
        # configure hardware
        self.__configPinHandler__(pushToTalkButton, self.__pttCallback__)
        self.__configPinHandler__(hangUpButton, self.__canCallback__)
        self.cbCan = callbHang
        self.cbPtt = callbPush

    def __configPinHandler__(self, button: Pin, cb):
        button.edges = "both"
        button.input_with_pull("up")
        button.bounce = 250
        button.when_changed = cb

    def __canCallback__(self, ticks, state):
        # TODO: convert state
        if state == 1:
            enumState = CanState.HUNGUP
        else:
            enumState = CanState.LIFTED
        self.cbCan(enumState)

    def __pttCallback__(self, ticks, state):
        # TODO: convert state
        if state == 1:
            enumState = PttState.PRESSED
        else:
            enumState = PttState.RELEASED
        self.cbCan(enumState)

    def startBlinking(self):
        self.blinkThread = threading.Thread(target=self.__blinking__)

    def stopBlinking(self):
        if self.blinkThread != None:
            self.blinkThread._stop()
            self.blinkThread = None

    def __blinking__(self):
        while True:
            self.led.on
            sleep(1) 
            self.led.off
            sleep(1)
