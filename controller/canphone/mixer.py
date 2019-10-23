import alsaaudio
import subprocess

# documentation for alsa: https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html

# implementing class capable of toggle between speak (speaker on , mic off) 
# and listen mode (speaker off, mic on)
# initial stet is mute for both

OUTPUTNAME = "Speaker"
INPUTNAME = "Mic"
CARDNAME = "Device"

#f*ck*ng patch for not working alsamixer
shell_cmd_mic_on = "amixer -c 1 sset Mic unmute cap"
shell_cmd_mic_off = "amixer -c 1 sset Mic mute nocap"

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

    def muteMic(self):
        subprocess.run(shell_cmd_mic_off.split(" "))

    def unMuteMic(self):
        subprocess.run(shell_cmd_mic_on.split(" "))

    def speak(self):
        self.mixOut.setmute(True)
        self.unMuteMic()
    
    def listen(self):
        self.mixOut.setmute(False)
        self.muteMic()

    def mute(self):
        self.mixOut.setmute(True)
        self.muteMic()
