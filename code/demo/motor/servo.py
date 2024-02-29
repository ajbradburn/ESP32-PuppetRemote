import machine

i2c = machine.I2C(0, scl=3, sda=8)

import servo
import time

ser = servo.Servos(i2c, address=0x40)
ser.position(0, 90)
time.sleep(1)
ser.position(0, 0)
time.sleep(1)
ser.position(0, 180)
time.sleep(1)
ser.position(0, 0)
ser.release(1)
