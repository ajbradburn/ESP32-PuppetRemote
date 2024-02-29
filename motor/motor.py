import machine

mf = machine.Pin(47, machine.Pin.OUT) # Motor Forward
mb = machine.Pin(48, machine.Pin.OUT) # Motor Backward

import time

mf.value(1)
time.sleep(1)
mf.value(0)
mb.value(1)
time.sleep(1)
mb.value(0)
time.sleep(4)
 
