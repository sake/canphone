from threading import RLock, Lock, Event, Thread
from gpiozero import RGBLED, Device, Pin, Buzzer
from gpiozero.pins.mock import MockFactory
from signal import pause
from time import sleep
from enum import Enum, auto
import logging

log = logging.getLogger("canphone")

# uncomment to run on PC hardware
#Device.pin_factory = MockFactory()


class CanState(Enum):
    LIFTED = auto()
    HUNGUP = auto()

class PttState(Enum):
    PRESSED = auto()
    RELEASED = auto()


class Color3(Enum):
    RED = (1, 0, 0)
    GREEN = (0, 1, 0)
    BLUE = (0, 0, 1)
    CYAN = (0, 1, 1)
    MAGENTA = (1, 0, 1)
    YELLOW = (1, 1, 0)
    WHITE = (1, 1, 1)
    BLACK = (0, 0, 0)


class PhoneControls:
    def __init__(self,  callbPush, callbHang, ledPins = (17, 27, 22), buzzerPin = 13, pttPin = 18, canPin = 19):
        # define properties
        self.led = RGBLED(ledPins[0], ledPins[1], ledPins[2])
        self.buzzer = Buzzer(buzzerPin, active_high=True)
        self.pttButton = Device.pin_factory.pin(pttPin)
        self.canButton: Pin = Device.pin_factory.pin(canPin)
        # configure hardware
        self.__configPinHandler__(self.pttButton, self.__pttCallback__)
        self.__configPinHandler__(self.canButton, self.__canCallback__)
        self.cbCan = callbHang
        self.cbPtt = callbPush

    def __configPinHandler__(self, button: Pin, cb):
        button.edges = "both"
        button.input_with_pull("up")
        button.bounce = .250
        button.when_changed = cb

    def __canCallback__(self, ticks, state):
        sleep(0.2)
        state = self.canButton.state
        log.debug("Can button state=%d", state)
        if state == 1:
            self.cbCan(CanState.HUNGUP)
        else:
            self.cbCan(CanState.LIFTED)

    def __pttCallback__(self, ticks, state):
        sleep(0.2)
        state = self.pttButton.state
        log.debug("PTT button state=%d", state)
        if state == 1:
            self.cbPtt(PttState.RELEASED)
        else:
            self.cbPtt(PttState.PRESSED)

    def ledOff(self):
        self.led.off()

    def ledOn(self, rgb=(1, 1, 1)):
        self.led.value = rgb

    def startBlinking(self, rgb=(1, 1, 1), off_time=0.5, on_time=0.5):
        self.led.blink(on_time=on_time, off_time=off_time, on_color=rgb, background=True)

    def beep(self):
        self.buzzer.beep(on_time=1, off_time=0.25, background=True)

    def stopBeep(self):
        self.buzzer.off()
