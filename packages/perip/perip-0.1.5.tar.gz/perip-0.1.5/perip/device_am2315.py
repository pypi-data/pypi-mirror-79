from aosong import am2315
import time
import redis
from .comm import connect

r = redis.Redis(host='ec2-75-101-199-232.compute-1.amazonaws.com', port=7599, password='p525f81fc5bf9a369922112084c158114e3978bc3042d9a76172a8508c7cd26ce')
sensor = am2315.Sensor()

test = connect()
print(test)

def get_data():
    while True:
        r.set('data', 'hello')
        print(sensor.data())
        time.sleep(2.00)