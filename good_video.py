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


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

picam2 = Picamera2()
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
#picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 10.0})

picam2.configure(picam2.create_video_configuration())
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))


def play_sound(text):
    tts = gTTS(text, lang='en')
    filename = "tmp.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)



image = 'HDRfastfocus2.jpg'
async def send_frames(websocket):
    try:
            with output.condition:
                output.condition.wait()
                frame = output.frame
                await websocket.send(frame)
    except Exception as e:
        print("Error! Frames",e)


async def hello():
	async with websockets.connect('ws://85.120.206.111:8001/ws') as websocket:
		while True:
			await send_frames(websocket)
			response = await websocket.recv()
			print(response)


asyncio.get_event_loop().run_until_complete(hello())
