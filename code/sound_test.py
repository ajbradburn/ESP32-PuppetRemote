from machine import I2C, Pin, I2S

def emptyFunction():
    return

# Start Servo Config
# Connect to the PCA9685 servo driver.
i2c = I2C(0, scl=3, sda=8)
ser = emptyFunction()
#print('Safety Print') # CRITICALLY IMPORTANT. This print statement enables I2S to work properly. Some combination of the i2c assignment, and then a variable assignemtn afterwards makes the I2S sound terrible. Simply printing the variable resolves the issue...
# End Servo

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

def playAudio(file):
    print(file)
    #try:
    if True:
        # Open the file and seek data.
        wav_file = file
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

playAudio('snake.wav')

audio_out.deinit()
