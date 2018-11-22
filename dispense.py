import RPi.GPIO as GPIO
import time

# # PIN OUTPUT SETTINGS # #
litePIN=16 #light pin
dispPIN = 21 #dispense pin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(dispPIN, GPIO.OUT)
GPIO.setup(litePIN, GPIO.OUT)

# # DISPENSE FUNCTION # #
def dispenseTreat(secs):
        GPIO.output(litePIN, True)
        GPIO.output(dispPIN, True)
        time.sleep(secs)  #time alotted for treat dispensing
        GPIO.output(dispPIN, False)
        GPIO.output(litePIN,False)

# # LED ON FUNCTION # #
def turnOnLED(secs):
        GPIO.output(litePIN, True)
        time.sleep(secs)
        GPIO.output(litePIN, False)