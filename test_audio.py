import os
from gtts import gTTS
import playsound


def play_sound(text):
    tts = gTTS(text, lang='en')
    filename = "tmp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

play_sound('The quick brown fox jumps over the lazy dog. Chestie Chestie. Thing Thing. Peleme Test Test')
