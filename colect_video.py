from picamera2 import Picamera2
from picamera2 import H264Encoder
import time

# Define constants
FRAMES_PER_SECOND = 20
DURATION_SECONDS = 7
OUTPUT_FILE = 'video.h264'

# Calculate the total number of frames to capture
total_frames = FRAMES_PER_SECOND * DURATION_SECONDS

# Initialize the PiCamera
with Picamera2() as camera:
    # Set camera resolution
    print("Colecting")
    camera.resolution = (640, 480)

    # Start recording to a file
    camera.start_recording(H264Encoder(),output=OUTPUT_FILE)

    # Capture frames for the specified duration
    start_time = time.time()
    for i in range(total_frames):
        # Wait for the next frame
        camera.wait_recording(1 / FRAMES_PER_SECOND)

    # Stop recording
    camera.stop_recording()

# Output file path
print(f"Video saved as: {OUTPUT_FILE}")

