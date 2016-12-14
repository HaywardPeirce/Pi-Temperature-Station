#!/usr/bin/env python

import os
import os.path
import glob
import time
from subprocess import *

#Read the Adafruit API key in from file /home/pi/apikey.txt.
file = open('/home/pi/apikey.txt', 'r')
apikey = file.readline().replace("\n", '')
file.close()

# Import library and create instance of REST client.
from Adafruit_IO import Client
aio = Client(apikey)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder0 = glob.glob(base_dir + '28*')[0]
device_file0 = device_folder0 + '/w1_slave'
device_folder1 = glob.glob(base_dir + '28*')[1]
device_file1 = device_folder1 + '/w1_slave'
print('Device File 0:', device_file0)
print('Device File 1:', device_file1)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def get_usb_temp():
    usbtemp_str= run_cmd("temper-poll | grep 'Device'  | awk '{print $3}' | cut -c 1-4")
    #print('usbtemp_str: ', usbtemp_str)
    if usbtemp_str != "":
        usbtemp = float(usbtemp_str) - 8
        return usbtemp_str
    else: return False

def read_temp_raw0():
    f = open(device_file0, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_raw1():
    f = open(device_file1, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp0():
    lines = read_temp_raw0()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw0()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    else: return False

def read_temp1():
    lines = read_temp_raw1()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw1()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    else: return False

while True:
        temp0 = read_temp0()
        temp1 = read_temp1()

        temp2 = get_usb_temp()
        
        if temp0 != False:
            print('Sensor 0 temp:',temp0)
            aio.send('temperature', temp0)
            data0 = aio.receive('temperature')
            print('Received value: {0}'.format(data0.value))
        if temp1 != False: 
            print('Sensor 1 temp:',temp1)
            aio.send('temperature-2', temp1)
            data1 = aio.receive('temperature-2')
            print('Received value: {0}'.format(data1.value))
        if temp2 != False:
            print('Sensor 2 temp:',temp2)
            aio.send('temperature-3', temp2)
            data2 = aio.receive('temperature-3')
            print('Received value: {0}'.format(data2.value))
        time.sleep(10)


