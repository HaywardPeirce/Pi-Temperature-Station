# Pi-Temperature-Station

A Raspberry Pi-based temperature sensing station. The setup uses 2 DS18B20 digital temperature sensor modules and one USB TEMPer sensor. The data is then fed to Grafana

### Resources

The basic code for the temperature sensing python script was found here: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview

The drivers for the TEMPer sensor were found here: https://github.com/padelt/temper-python

[Adafruit.io installation instructions for ds18b20 temperature sensing](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/ds18b20#add-onewire-support)

### Installation

Clone this repo into the Pi home directory

Run `sudo bash setup.sh`

Edit the `config.ini` file to indicate the IP address of the influxdb server, the port, and which database you wish to have the data added to

Reboot