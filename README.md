# Pi-Temperature-Station

A Raspberry Pi-based temperature sensing station. The setup uses 2 DS18B20 digital temperature sensor modules and one USB TEMPer sensor. The data is then fed back to Adafruit.io

### Resources

The basic code for the temperature sensing python script was found here: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

Details about including Adafruit.io were found here: https://github.com/adafruit/io-client-python

The drivers for the TEMPer sensor were found here: https://github.com/padelt/temper-python

Information on how to create an Upstart Service was found here: https://stackoverflow.com/questions/17747605/daemon-vs-upstart-for-python-script

### Installation

Install Upstart
`sudo apt-get install upstart`

Follow the [Adafruit.io installation instructions](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20#add-onewire-support):
- Add `dtoverlay=w1-gpio` to `/boot/config.txt` using `sudo nano /boot/config.txt`
- Reboot
- Run the following the check that the temperature device(s) works:
  
  `sudo modprobe w1-gpio`
  
  `sudo modprobe w1-therm`
  
  `cd /sys/bus/w1/devices`
  
  `ls`
  
  `cd 28-xxxx` (change this to match what serial number pops up)
  
  `cat w1_slave`

- Follow the TEMPer-python installation instructions
- Close this repo into the pi user home directory
- Install the required python libraries: `pip install -r requirements.txt`
- Place the thermoservice.conf file in /etc/init
- Change the permissions for the `thermometer.py` file: `sudo chmod +x thermometer.py`
- Reboot the Pi
