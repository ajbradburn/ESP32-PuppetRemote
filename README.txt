The goal is to create a remote control for a puppet.

1. Direct communication between two ESP devices via ESP-NOW.
2. Playing sound upon trigger.
3. Control servo to articulate eye lids.
4. Control motor to retract wings.

Implemented with Micropython
https://micropython.org/download/ESP32_GENERIC_S3/

Example Ampy Commands: ampy -p /dev/ttyACM0 -b 115200 put receiver.py main.py

-: Setup Environment
-- THIS --
sudo apt install python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip3 install adafruit-ampy
pip3 install esptool
-- OR --
sudo apt install python3 python3-pip
sudo pip3 install adafruit-ampy --break-system-packages
sudo pip3 install esptool –break-system-packages
-- THEN --
python3 -m esptool --port /dev/ttyACM0 erase_flash
python3 -m esptool --chip esp32s3 --port /dev/ttyACM0 write_flash -z 0 ESP32_GENERIC_S3-SPIRAM_OCT-20240222-v1.22.2.bin
ampy -p /dev/ttyACM0 -b 115200 put receiver.py main.py

To reset: -> Connect via serial port. picocom -b 115200 /dev/ttyACM0 -> At the terminal, type the following:
import machine
machine.reset()
