from aosong import am2315
import time

sensor = am2315.Sensor()

def get_data():
    while True:
        print(sensor.data())
        time.sleep(2.00)