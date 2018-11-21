import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera 
import time 
import cv2  
import numpy as np 
import camconfig #my input file

def run():
    print('running DetectCharlie.py')
    #### TREAT DISPENSING FUNCTIONS ###
    ## PIN OUTPUT STUFF ##
    litePIN=16 #light pin
    dispPIN = 21 #dispense pin
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(dispPIN, GPIO.OUT)
    GPIO.setup(litePIN, GPIO.OUT)

    ## DISPENSE FUNCTION ##
    def dispenseTreat(secs):
            GPIO.output(litePIN, True)
            time.sleep(.5)  #wait for assistant to finish response
            GPIO.output(dispPIN, True)
            time.sleep(secs)  #time alotted for treat dispensing
            GPIO.output(dispPIN, False)
            time.sleep(5)
            GPIO.output(litePIN,False)
    ## LED ON FUNCTION ##
    def turnOnLED():
            GPIO.output(litePIN, True)
            time.sleep(.5)
            GPIO.output(litePIN, False)

    #Initialize camera & grab reference to the raw camera capture
    camera = PiCamera()

    #Camera settings
    camera.resolution = camconfig.imgSize
    camera.framerate = camconfig.fps #Rpi exclusive
    camera.rotation = camconfig.rot
    camera.brightness = camconfig.brightness
    camera.contrast = camconfig.contrast
    rawCapture = PiRGBArray(camera, size=camconfig.imgSize)

    #allow camera warmup
    time.sleep(camconfig.camera_warmup_time) #Rpi Exclusive

    #Load openCV xml of object to detect
    cascade = cv2.CascadeClassifier('dog.xml')

    tInitial = 0
    tTarget = 0
    reset = False
    tRecord = time.time() + camconfig.recording_time # 30 seconds of recording

    # capture frames from the camera
    camera.start_preview()
    time.sleep(1)
    print('recording started: charliedetected.h264')
    camera.start_recording('charliedetected.h264')

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        print('current time: ' + str(time.time()))
        print('rRecord time: ' + str(tRecord))
        if reset == True: #While True:
            print('Resetting timers')
            tTarget = 0
            tInitial = 0
            startTime = time.time()
            reset = False

        # grab the raw NumPy array representing the image,
        #then initialize the timestamp & occupied/unoccupied text
        image = frame.array
        faces = cascade.detectMultiScale(image,camconfig.scaleFactor,camconfig.minNeighbors)
        
        #checks if faces is not empty
        if np.array(faces).any(): 
            flagSpotted = True
            for (x,y,w,h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        else:
            flagSpotted = False
        
        #when first spot happens
        if flagSpotted and tInitial ==0:
            #winsound.Beep(frequency+50,duration)
            tInitial = time.time()
            tTarget = time.time()+camconfig.detect_time
            print('Charlie spotted for first time')
        
        #if spotted during time defined by tTarget
        if flagSpotted and tInitial !=0 and time.time()< tTarget:
            #winsound.Beep(frequency,duration)
            print(str(time.time()-tInitial)+' oh! I think that was him again!')
        
        #if continuously spotted for longer than tTarget
        if flagSpotted and tInitial != 0 and time.time() > tTarget:
            print(str(time.time()-tInitial) + ' yup, thats charlie alright! ')
            charlie_pic_filename = 'charliespic.jpg'
            camera.capture(charlie_pic_filename)
##            charlie_pic_filename.close()
            turnOnLED()
            dispenseTreat(.1)
            reset = True
        
        elif not flagSpotted and tInitial !=0 and time.time()>tTarget:
            print(str(time.time()-tInitial)+' nope, that wasnt charlie')
            reset = True
        
        
        #show the frame
        cv2.imshow("Frame", image)

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key is pressed, break from the loop
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
        # if the esc key is pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        # stop recording if time greater than tRecord
        if time.time() > tRecord:
            print('recording stopped')
            camera.stop_recording()
            camera.stop_preview()
            camera.close()
            cv2.destroyAllWindows()
            break
    print('Detecting Charlie Completed')
