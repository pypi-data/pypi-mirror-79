from .comm import Comm
import time, sys
import RPi.GPIO as GPIO

db = Comm(host='ec2-75-101-199-232.compute-1.amazonaws.com',
         port=7599,
         password='p525f81fc5bf9a369922112084c158114e3978bc3042d9a76172a8508c7cd26ce')

GPIO.setmode(GPIO.BCM)
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

def logit(message):
    print(message)
    sys.stdout.flush()

def blink():
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        db.set_key("led_state", "high")
        print(db.get_value_by_key("led_state"))
        time.sleep(2)

        GPIO.output(LED_PIN, GPIO.LOW)
        db.set_key("led_state", "high")
        print(db.get_value_by_key("led_state"))
        time.sleep(2)