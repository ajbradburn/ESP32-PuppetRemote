import network
import espnow

import ubinascii
print('Mac address for this device in byte and Hex format?')                                                                                                 
print(network.WLAN().config('mac'))
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        print(host, msg)
        if msg == b'end':
            break
