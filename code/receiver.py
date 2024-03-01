import network
import espnow

import ubinascii
print('Device MAC Address:')
print(network.WLAN().config('mac'))
print(ubinascii.hexlify(network.WLAN().config('mac'),':').decode())

from machine import I2C, Pin, I2S, SDCard
import servo
import time
#from uos import mount
import uos
from os import listdir
from time import sleep


# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
#sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

# Start Servo Config
# Connect to the PCA9685 servo driver.
i2c = I2C(0, scl=3, sda=8)
ser = servo.Servos(i2c, address=0x40)
# End Servo

# Start Motor Config
# Configure the forward and reverse pins.
mf = Pin(9, Pin.OUT) # Motor Forward
mb = Pin(10, Pin.OUT) # Motor Backward
# End Motor

'''
# Start Sound Config
# Configure the I2S connection to the Max98357A audio amplifier.
#sample_rate_in_hz = 44100
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
    ibuf=1024
    )

# Start SD Card
# Connect to the SD card reader via SPI.
sd = SDCard(slot=3, sck=Pin(14), mosi=Pin(13), miso=Pin(12), cs=Pin(15))
mount(sd, "/sd")
#print(os.listdir("/sd"))

####
# Open the file and seek data.
wav_file = '/sd/{}'.format('snake.wav')
wav = open(wav_file,'rb')
pos = wav.seek(44) 

# Allocate audio buffer.
#   memoryview used to reduce heap allocation in while loop
wav_samples = bytearray(1024)
wav_samples_mv = memoryview(wav_samples)
audio_out.shift

# Play Audio File
while True:
    num_read = wav.readinto(wav_samples_mv)
    if num_read == 0:
        break
    num_written = 0
    # Increase the volume.
    #I2S.shift(buf=wav_samples_mv, bits=16, shift=1)
    while num_written < num_read:
        num_written += audio_out.write(wav_samples_mv[num_written:num_read])
wav.close()
'''
bck_pin = Pin(5)                                                                                                                                             
ws_pin = Pin(6)  
sdout_pin = Pin(4)

# channelformat settings:
#     mono WAV:  channelformat=I2S.ONLY_LEFT
audio_out = I2S(
    1, 
    sck=bck_pin, ws=ws_pin, sd=sdout_pin, 
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO, 
    rate=44100,
    ibuf=1024
    )

sd = SDCard(slot=3, sck=Pin(14), mosi=Pin(13), miso=Pin(12), cs=Pin(15))
uos.mount(sd, "/sd")

wav_file = '/sd/{}'.format('snake.wav')
wav = open(wav_file,'rb')
pos = wav.seek(44) 
wav_samples = bytearray(1024)
wav_samples_mv = memoryview(wav_samples)
audio_out.shift

while True:
    num_read = wav.readinto(wav_samples_mv)
    if num_read == 0:
        break
    num_written = 0
    # Increase the volume.
    #I2S.shift(buf=wav_samples_mv, bits=16, shift=1)
    while num_written < num_read:
        num_written += audio_out.write(wav_samples_mv[num_written:num_read])
####

def blink():
    ser.position(0, 180)
    sleep(1)
    ser.position(0, 0)

def servoTest():
    ser.position(0, 720)
    sleep(1)
    ser.position(0, 0)
    
def flap():
    mf.value(1)
    sleep(1)
    mf.value(0)
    mb.value(1)
    sleep(1)
    mb.value(0)

def playAudio(file):
    print(file)
    #try:
    if True:
        # Open the file and seek data.
        wav_file = '/sd/{}'.format(file)
        wav = open(wav_file,'rb')
        pos = wav.seek(44) 

        # Allocate audio buffer.
        #   memoryview used to reduce heap allocation in while loop
        wav_samples = bytearray(1024)
        wav_samples_mv = memoryview(wav_samples)
        audio_out.shift

        # Play Audio File
        while True:
            num_read = wav.readinto(wav_samples_mv)
            if num_read == 0:
                break
            num_written = 0
            # Increase the volume.
            #I2S.shift(buf=wav_samples_mv, bits=16, shift=1)
            while num_written < num_read:
                num_written += audio_out.write(wav_samples_mv[num_written:num_read])
        wav.close()
    #except (KeyboardInterrupt, Exception) as e:
    #    print('caught exception {} {}'.format(type(e).__name__, e))

# Application Loop
while True:
    host, msg = e.recv()
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
            servoTest()
        elif msg == b'10':
            print('No action assigned to command 10')

umount("/sd")
sd.deinit()
audio_out.deinit()
