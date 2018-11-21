from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180
camera.brightness = 62
camera.contrast = 5
camera.start_preview()
sleep(1)
camera.start_recording('mysecondvid.h264')
sleep(10)
camera.stop_recording()
camera.stop_preview()