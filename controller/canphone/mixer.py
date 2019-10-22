import alsaaudio

# documentation for alsa: https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html

# implementing class capable of toggle between speak (speaker on , mic off) 
# and listen mode (speaker off, mic on)
# initial stet is mute for both

OUTPUTNAME = "Speaker"
INPUTNAME = "Mic"
CARDNAME = "Device"

DEFAULT_VOL_OUT = 70
DEFAULT_VOL_IN = 70

def getCardIndex(cardName):
    return alsaaudio.cards().index(cardName)

class CanMixer():
    def __init__(self, cardName=CARDNAME, inName=INPUTNAME, outName=OUTPUTNAME, defVolOut=DEFAULT_VOL_OUT, defVolIn=DEFAULT_VOL_IN):
        cardindex=getCardIndex(cardName)
        self.mixOut = alsaaudio.Mixer(outName, cardindex=cardindex)
        self.mixIn = alsaaudio.Mixer(inName, cardindex=cardindex)
        self.mixOut.setvolume(defVolOut)
        self.mixIn.setvolume(defVolIn)
        self.mute()

    def speak(self):
        self.mixOut.setmute(True)
        self.mixIn.setmute(False)
    
    def listen(self):
        self.mixOut.setmute(False)
        self.mixIn.setmute(True)

    def mute(self):
        self.mixOut.setmute(True)
        self.mixIn.setmute(True)
