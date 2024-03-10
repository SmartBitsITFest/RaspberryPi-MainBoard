from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from threading import Condition
from libcamera import controls
from gtts import gTTS
import asyncio
import playsound
import websockets
import io
import os
import RPi.GPIO as GPIO
from time import sleep
import speech_recognition as sr


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()




def play_sound(text):
    tts = gTTS(text, lang='en')
    filename = "tmp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

async def send_frames(websocket,mode=b'BARC'):
    try:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                modf_frame =mode+frame    
                
                await websocket.send(modf_frame)
    except Exception as e:
        print("Error! Frames",e)

def is_on(bt):
    return GPIO.input(bt)
    
    
    
    
def check_mode(b1,b2,mode,seconds=1 ,percent=0.75,last_saved=False, last_good=False):
    count_b1 = 0
    count_b2 = 0
    play_sound('beep')
    for i in range(int(seconds*10)):
        count_b1 += int(is_on(b1))
        count_b2 += int(is_on(b2))
        sleep(0.1)
    if count_b1 >= seconds*percent and count_b2 >= seconds*percent and last_good: # open microphon
        r = sr.Recognizer()
        speech = sr.Microphone()
        play_sound("What you want to find about the product?")
        with speech as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source,10,3)
            play_sound("Procesing your message")
            try:
                recog = r.recognize_sphinx(audio, language = 'en-US')
                play_sound("You said: " + recog)
                """
                here call for lama with recog, to ask for more infomation that is wansted 
                last_good is the name of the last susscesful detected barcode
                response = await websocket.recv() - response for llama
                """
            except sr.UnknownValueError:
                print("Recognition could not understand audio")
    elif count_b1 >= seconds*percent: # change mode
        if mode == b'BARC':
            mode = b'EXPD'
            play_sound('Mode changed to expiration date')
        else:
            mode = b'REBB' # calculate expiratin and back to barcode
            play_sound('Calculating expiration date for provided images, and swiching back to barcode. This may take more that one minute. Processing')
    elif count_b2 >= seconds*percent: # save data in db, ask for reteta
        if last_saved:
            play_sound('Generate receipies with the products saved until now')
            mode = b'RECP'
        else:
            play_sound('Saving product.')
            mode = b'SAVE'
        last_saved = not last_saved
        print('b2')
    sleep(0.1)
    return mode, last_saved

picam2 = Picamera2()
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 10.0})

picam2.configure(picam2.create_video_configuration())
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

GPIO.setmode(GPIO.BOARD)


async def main():
    b1 = 16
    b2 = 18
    GPIO.setup(b1, GPIO.IN)
    GPIO.setup(b2, GPIO.IN)
    mode = b'BARC'
    last_saved = False
    good_barc = False
    async with websockets.connect('ws://85.120.206.111:8001/ws') as websocket:
        while True:
            await send_frames(websocket,mode)
            response = await websocket.recv()
            if 'notBar' in response: #nobarcode found, need update, I don't know how it named
                good_barc = False
            else:
                good_barc = response
                play_sound(response)
            if mode == b'SAVE' or mode == b'RECP' or mode == b'REBB':
                mode = b'BARC'
            if is_on(b1) or is_on(b2) or good_barc:
                mode, last_saved = check_mode(b1,b2,mode,last_saved)
            print(response)
asyncio.get_event_loop().run_until_complete(main())  

