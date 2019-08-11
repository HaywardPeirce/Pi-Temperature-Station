sudo apt-get install git wget python-pip python python-usb python-setuptools -y

sudo echo 'dtoverlay=w1-gpio' >> /boot/config.txt

cd /home/pi/
wget https://github.com/padelt/temper-python/archive/v1.5.3.tar.gz
tar xzf v1.5.3.tar.gz
mv temper-python-1.5.3 temper-python
cd temper-python
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
sudo python setup.py install

sudo cp etc/99-tempsensor.rules /etc/udev/rules.d/

sudo echo 'usbhid.quirks=0x0c45:0x7401:0x4' >> /boot/cmdline.txt

cd /home/pi/Pi-Temperature-Station/

sudo pip install virtualenv
virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
sudo pip install -r requirements.txt

cp config.ini.example config.ini


sudo chmod +x thermometer.py
sudo cp thermoservice.service /etc/systemd/system/thermoservice.service
sudo systemctl start thermoservice.service

sudo reboot