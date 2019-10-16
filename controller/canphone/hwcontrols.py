import thread
from gpiozero import LED, Button
from signal import pause
from time import sleep

led = LED(17)
button = Button(3)
isItBlinking = False

def startBlinking():
    isItBlinking = True

def stopBlinking():
    isItBlinking = False

def blinking():
    while isItBlinking == True:
        led.on
        sleep(1) 
        led.off
        sleep(1) 

def buttonListener():
    while True:
        button.when_pressed = # add function call push to talk
        button.when_released = # add function call end push to talk
        sleep(1)

def main():
    thread.start_new_thread(buttonListener, ())
    thread.start_new_thread(blinking, ())

if __name__ == '__main__':
    main()
