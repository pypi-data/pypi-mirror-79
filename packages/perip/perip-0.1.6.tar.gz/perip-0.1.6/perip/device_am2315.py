from aosong import am2315
import time
from .comm import connect

r = connect()
sensor = am2315.Sensor()

def get_data():
    while True:
        r.set('data', 'hello')
        print(sensor.data())
        time.sleep(2.00)