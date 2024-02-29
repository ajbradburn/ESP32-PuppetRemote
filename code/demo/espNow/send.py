import network
import espnow
import time

import ubinascii
print('Mac address for this device in byte and Hex format?')
print(network.WLAN().config('mac'))
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

e = espnow.ESPNow()
e.active(True)
peer = b'4\x85\x18\x90\x85X'   # MAC address of peer's wifi interface
e.add_peer(peer)      # Must add_peer() before send()

e.send(peer, "Starting...")
for i in range(100):
    e.send(peer, str(i)*20, True)
    time.sleep(1)
e.send(peer, b'end')
