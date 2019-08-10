sudo apt-get install git pip python python-usb python-setuptools -y

sudo echo 'dtoverlay=w1-gpio' >> /boot/config.txt

cd /home/pi/
git clone https://github.com/padelt/temper-python.git
cd temper-python
sudo python setup.py install

sudo cp etc/99-tempsensor.rules /etc/udev/rules.d/

sudo echo 'usbhid.quirks=0x0c45:0x7401:0x4' >> /boot/cmdline.txt

cd /home/pi/Pi-Temperature-Station/

sudo pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
sudo pip install -r requirements.txt

sudo chmod +x thermometer.py
sudo cp thermoservice.service /etc/systemd/system/thermoservice.service

sudo reboot