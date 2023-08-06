from aosong import am2315
import time, json
from .comm import connect

r = connect()
sensor = am2315.Sensor()

def get_data():
    while True:
        tuple_data = sensor.data()
        j = {
            "humidity":tuple_data[0],
            "c":tuple_data[1],
            "f":tuple_data[2]
        }
        r.set('data', json.dumps(j))
        print(j)
        time.sleep(2.00)