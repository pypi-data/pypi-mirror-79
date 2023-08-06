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
    logit("high")
    GPIO.output(LED_PIN, GPIO.HIGH)
    time.sleep(2)
    logit("low")
    GPIO.output(LED_PIN, GPIO.LOW)


if __name__ == '__main__':
    try:
        while True:
            time.sleep(2)
            blink()
    except:
        logit("Bye!")
        GPIO.cleanup()