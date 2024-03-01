import network
import espnow

from machine import Pin
from time import sleep, ticks_ms
from math import fabs

# Display the mac address for this device.
import ubinascii
print('Device MAC address:')
print(network.WLAN().config('mac'))
print(ubinascii.hexlify(network.WLAN().config('mac'),':').decode())

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
#sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'4\x85\x18\x90\x85X'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()

'''
e.send(peer, "Starting...")
for i in range(100):
    e.send(peer, str(i)*20, True)
    time.sleep(1)
e.send(peer, b'end')
'''

#pinNumbers = [8, 3, 46, 9, 10, 11, 12, 13]
pinNumbers = [8, 3, 46, 9, 10]

# An array to track the last time a pin was pressed, to act as a form of additional debouncing.
pressed = {}
for p in pinNumbers:
    pressed[p] = ticks_ms()

def transmit(p):
    if fabs(pressed[p] - ticks_ms()) < 500:
        print("Button {} double-pressed.".format(p))
        return
    e.send(peer, "{}".format(p))
    pressed[p] = ticks_ms()
    print("Button {} pressed.".format(p))

pinObjects = {}
pinCallbacks = {}

for p in pinNumbers:
    pinObjects[p] = Pin(p, Pin.IN, Pin.PULL_UP)
    pinCallbacks[p] = eval("lambda p: transmit({})".format(p))
    pinObjects[p].irq(pinCallbacks[p], Pin.IRQ_FALLING)

'''
bS = Pin(8, Pin.IN, Pin.PULL_UP)
bS.irq(lambda p:transmit(8), Pin.IRQ_FALLING)
'''

