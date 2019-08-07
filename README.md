# Pi-Temperature-Station

A Raspberry Pi-based temperature sensing station. The setup uses 2 DS18B20 digital temperature sensor modules and one USB TEMPer sensor. The data is then fed to Grafana

### Resources

The basic code for the temperature sensing python script was found here: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

The drivers for the TEMPer sensor were found here: https://github.com/padelt/temper-python

### Installation

Clone this repo into the Pi home directory

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

- Follow the [TEMPer-python](https://github.com/padelt/temper-python) installation instructions
- Install the required python libraries: `pip install -r requirements.txt`
- Place the thermoservice.service file in /etc/systemd/system
- Change the permissions for the `thermometer.py` file: `sudo chmod +x thermometer.py`
- Reboot the Pi
