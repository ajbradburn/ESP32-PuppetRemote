from machine import I2S
from machine import SDCard
from machine import Pin
import uos

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

wav.close()
uos.umount("/sd")
sd.deinit()
audio_out.deinit()
