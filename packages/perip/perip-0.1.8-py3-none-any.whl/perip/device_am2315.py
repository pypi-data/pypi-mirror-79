from aosong import am2315
import time, json
from .comm import Comm

r = Comm(host='ec2-75-101-199-232.compute-1.amazonaws.com',
         port=7599,
         password='p525f81fc5bf9a369922112084c158114e3978bc3042d9a76172a8508c7cd26ce')

sensor = am2315.Sensor()

def get_data():
    while True:
        tuple_data = sensor.data()
        j = {
            "humidity":tuple_data[0],
            "c":tuple_data[1],
            "f":tuple_data[2]
        }
        r.set_key('data',json.dumps(j))
        # r.set('data', json.dumps(j))
        print(j)
        time.sleep(2.00)