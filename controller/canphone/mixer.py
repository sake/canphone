import alsaaudio

# documentation for alsa: https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html

# implement class capable of toggle mute of the speaker and microphone
# initial state of the mixer shall be set to mic mute, speaker not mute

OUTPUTNAME = "Speaker"
INPUTNAME = "Mic"
CARDNAME = "Device"

DEFAULT_VOL_OUT = 70
DEFAULT_VOL_IN = 70

def getCardIndex():
    return alsaaudio.cards().index(CARDNAME)

class canMixer():
    def __init__(self):
        self.Out = alsaaudio.Mixer(OUTPUTNAME, cardindex=getCardIndex())
        self.In = alsaaudio.Mixer(INPUTNAME, cardindex=getCardIndex())
        self.Out.setvolume(DEFAULT_VOL_OUT)
        self.In.setvolume(DEFAULT_VOL_IN)
        self.Out.setmute(False)
        self.In.setmute(True)

def speak():
    canMixer.Out.setmute(True)
    canMixer.In.setmute(False)

def listen():
    canMixer.Out.setmute(False)
    canMixer.In.setmute(True)
try:
    canMixer = canMixer()
except:
    print("Error - card not found")



