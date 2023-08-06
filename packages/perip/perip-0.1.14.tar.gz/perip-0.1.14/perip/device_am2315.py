from aosong import am2315
import time, json

class TempRh:
    def __init__(self, db):
        self.db = db
        self.sensor = am2315.Sensor()

    def get_data(self):
        tuple_data = self.sensor.data()
        j = {
            "humidity": tuple_data[0],
            "c": tuple_data[1],
            "f": tuple_data[2]
        }
        temp_rh = json.dumps(j)
        self.db.set_key('temp_rh', temp_rh)
        return temp_rh