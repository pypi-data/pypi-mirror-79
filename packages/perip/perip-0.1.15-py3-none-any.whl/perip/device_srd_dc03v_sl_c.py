import time, sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

class Relay:
    def __init__(self, db):
        self.db = db

    def logit(message):
        print(message)
        sys.stdout.flush()

    def blink(self, loop_count=2, sleep=1.0):
        count = 0
        while count <= loop_count:
            GPIO.output(LED_PIN, GPIO.HIGH)
            self.db.set_key("led_state", "high")
            print(self.db.get_value_by_key("led_state"))
            time.sleep(sleep)

            GPIO.output(LED_PIN, GPIO.LOW)
            self.db.set_key("led_state", "low")
            print(self.db.get_value_by_key("led_state"))
            time.sleep(sleep)

            count += 1