from .comm import Comm
from .device_am2315 import TempRh
from .device_srd_dc03v_sl_c import Relay

db = Comm(host='ec2-75-101-199-232.compute-1.amazonaws.com',
         port=7599,
         password='p525f81fc5bf9a369922112084c158114e3978bc3042d9a76172a8508c7cd26ce')

tempRh = TempRh(db)
relay = Relay(db)

while True:
    temp_rh = tempRh.get_data()
    relay.blink(5)
    print(temp_rh)