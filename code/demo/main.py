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

# End Servo
# Start Motor

mf = machine.Pin(9, machine.Pin.OUT) # Motor Forward
mb = machine.Pin(10, machine.Pin.OUT) # Motor Backward

mf.value(1)
time.sleep(1)
mf.value(0)
mb.value(1)
time.sleep(1)
mb.value(0)
time.sleep(4)

# End Motor
# Start Sound
 
from machine import I2S
from machine import SDCard
from machine import Pin
import uos

#======= USER CONFIGURATION =======
#WAV_FILE = 'chimes.wav'
WAV_FILE = 'snake.wav'
#WAV_FILE = 'infinity.wav'
#WAV_FILE = 'chimes-22050.wav'
SAMPLE_RATE_IN_HZ = 44100
#======= USER CONFIGURATION =======

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
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=1024
    )

# configure SD card:
# See [docs](https://docs.micropython.org/en/latest/library/machine.SDCard.html#esp32) for
# recommended pins depending on the chosen slot.
#   slot=2 configures SD card to use the SPI3 controller (VSPI), DMA channel = 2
#   slot=3 configures SD card to use the SPI2 controller (HSPI), DMA channel = 1
sd = SDCard(slot=3, sck=Pin(14), mosi=Pin(13), miso=Pin(12), cs=Pin(15))
print(sd)
uos.mount(sd, "/sd")
import os
print(os.listdir("/sd"))
wav_file = '/sd/{}'.format(WAV_FILE)
wav = open(wav_file,'rb')

# advance to first byte of Data section in WAV file
pos = wav.seek(44) 

# allocate sample arrays
#   memoryview used to reduce heap allocation in while loop
wav_samples = bytearray(1024)
wav_samples_mv = memoryview(wav_samples)
audio_out.shift

print('Starting')
# continuously read audio samples from the WAV file 
# and write them to an I2S DAC
while True:
    num_read = wav.readinto(wav_samples_mv)
    if num_read == 0:
        break
    num_written = 0
    # Increase the volume.
    #I2S.shift(buf=wav_samples_mv, bits=16, shift=1)
    while num_written < num_read:
        num_written += audio_out.write(wav_samples_mv[num_written:num_read])
#try:
#except (KeyboardInterrupt, Exception) as e:
#    print('caught exception {} {}'.format(type(e).__name__, e))


'''
while True:
    try:
        num_read = wav.readinto(wav_samples_mv)
        num_written = 0
#        # end of WAV file?
        if num_read == 0:
#            # advance to first byte of Data section
            pos = wav.seek(44) 
        else:
#            # loop until all samples are written to the I2S peripheral
            while num_written < num_read:
                num_written += audio_out.write(wav_samples_mv[num_written:num_read])
    except (KeyboardInterrupt, Exception) as e:
        print('caught exception {} {}'.format(type(e).__name__, e))
        break
'''
    
wav.close()
uos.umount("/sd")
sd.deinit()
audio_out.deinit()
print('Done')
