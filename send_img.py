from picamera2 import Picamera2
from libcamera import controls
from time import sleep
import os
picam2 = Picamera2()
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=1 -d /dev/v4l-subdev0")
print("Setting HDR to ON")
picam2.start(show_preview=True)
#picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous, "AfSpeed": controls.AfSpeedEnum.Fast})
picam2.capture_files("images/HDRfastfocus{:d}.jpg", num_files=80)
sleep(30)
picam2.stop_preview()
picam2.stop()
print("Setting HDR to OFF")
os.system("v4l2-ctl --set-ctrl wide_dynamic_range=0 -d /dev/v4l-subdev0")
