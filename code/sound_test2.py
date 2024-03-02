from machine import I2S, Pin, I2C

def emptyFunction():
    return

i2c = I2C(0, scl=3, sda=8)
ser = emptyFunction()
#print('Safety Print') # CRITICALLY IMPORTANT. This print statement enables I2S to work properly. Some combination of the i2c assignment, and then a variable assignment through a function makes I2S sound terrible. Simply printing anything prevents this.

def i2s_callback(arg):
    num_read = wav.readinto(wav_samples_mv)
    if num_read == 0:
        audio_out.irq()
    else:
        audio_out.write(wav_samples_mv[:num_read])


audio_out = I2S(
    1,
    sck=Pin(5),
    ws=Pin(6),
    sd=Pin(4),
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO,
    rate=44100,
    ibuf=10000,
)

audio_out.irq(i2s_callback)

wav = open('snake.wav', "rb")
wav.seek(44)  # advance to first byte of Data section in WAV file

silence = bytearray(1000)

wav_samples = bytearray(10000)
wav_samples_mv = memoryview(wav_samples)

audio_out.write(silence)
