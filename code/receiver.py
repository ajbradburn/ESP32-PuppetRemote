import network
import espnow

import ubinascii
print('Device MAC Address:')
print(network.WLAN().config('mac'))
print(ubinascii.hexlify(network.WLAN().config('mac'),':').decode())

from machine import I2C, Pin, I2S, SDCard, Timer
from servo import Servos
import time
from uos import mount, umount
from os import listdir
from time import ticks_ms, ticks_diff
from math import fabs

# Start ESP NOW
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)

e = espnow.ESPNow()
e.active(True)
# End ESP NOW

# Start Servo Config
# Connect to the PCA9685 servo driver.
servo_disable_time = None

i2c = I2C(0, scl=3, sda=8)
ser = Servos(i2c, address=0x40)
ser.position(0, 0)
print(ser) # CRITICALLY IMPORTANT. This print statement enables I2S to work properly. Some combination of the i2c assignment, and then a variable assignemtn afterwards makes the I2S sound terrible. Simply printing the variable resolves the issue...
# End Servo

# Start Motor Config
# Configure the forward and reverse pins.
motor_disable_time = None

mf = Pin(9, Pin.OUT) # Motor Forward
mb = Pin(10, Pin.OUT) # Motor Backward
# End Motor

# Start Sound Config
current_file = None
BUFFER_SIZE = 10000

# Configure the I2S connection to the Max98357A audio amplifier.
bclk = Pin(5) # Clock Pin
lrc = Pin(6) # Channel Select Pin
din = Pin(4) # Data Pin

audio_out = I2S(
    1, 
    sck=bclk, ws=lrc, sd=din, 
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO, 
    rate=44100,
    ibuf=BUFFER_SIZE
    )

# Start SD Card
# Connect to the SD card reader via SPI.
sd = SDCard(slot=3, sck=Pin(14), mosi=Pin(13), miso=Pin(12), cs=Pin(15))
mount(sd, "/sd")
#print(os.listdir("/sd"))

def blink():
    global servo_disable_time
    if servo_disable_time == None:
        servo_disable_time = ticks_ms() + 1000
        ser.position(0, 180)
    else:
        servo_disable_time = None
        ser.position(0, 0)

def flap():
    print('Flap Called')

    global motor_disable_time
    if motor_disable_time == None:
        motor_disable_time = ticks_ms() + 1000
        mf.value(1)
        print('Starting Flap')
    elif mf.value():
        motor_disable_time = ticks_ms() + 1000
        mf.value(0)
        mb.value(1)
        print('Reversing Flap')
    elif mb.value():
        motor_disable_time = None
        mb.value(0)
        print('Done Flapping')
    else:
        print('Already flapping.')

def i2s_callback(arg):
    global current_file
    global BUFFER_SIZE
    wav_samples = bytearray(BUFFER_SIZE)
    wav_samples_mv = memoryview(wav_samples)
    num_read = current_file.readinto(wav_samples_mv)
    if num_read == 0:
        audio_out.irq(None)
        current_file.close()
        current_file = None
    else:
        audio_out.write(wav_samples_mv[:num_read])

def playAudio(file):
    global current_file
    global BUFFER_SIZE
    # If the audio file has a value, we are going to abort, and let it finish.
    if current_file != None:
        return

    # Open the file and seek data.
    wav_file = '/sd/{}'.format(file)
    current_file = open(wav_file,'rb')
    pos = current_file.seek(44) 

    # Allocate audio buffer.
    #   memoryview used to reduce heap allocation in while loop
    wav_samples = bytearray(BUFFER_SIZE)
    wav_samples_mv = memoryview(wav_samples)
    #audio_out.shift
    num_read = current_file.readinto(wav_samples_mv)
    audio_out.irq(i2s_callback)
    audio_out.write(wav_samples_mv[:num_read])

def upkeep():
    # The servo needs a time to call a return to 0.
    if servo_disable_time != None:
        if servo_disable_time < ticks_ms():
            blink()

    # The motor needs a time to disable.
    if motor_disable_time != None:
        if motor_disable_time < ticks_ms():
            print('Callign Flap')
            flap()

# Application Loop
while True:
    upkeep()

    host, msg = e.recv(0)
    if msg:             # msg == None if timeout in recv()
        #print(host, msg)
        command = msg.decode('utf-8')
        if msg == b'8':
            print('Play Audio')
            playAudio('snake.wav')
        elif msg == b'3':
            print('Blink')
            blink()
        elif msg == b'46':
            print('Flap Wings')
            flap()
        elif msg == b'9':
            print('No action assigned to command 9.')
        elif msg == b'10':
            print('No action assigned to command 10')

umount("/sd")
sd.deinit()
audio_out.deinit()
