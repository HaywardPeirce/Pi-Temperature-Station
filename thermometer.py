#!/usr/bin/env python

import os
import glob
import time
from subprocess import *

# Import library and create instance of REST client.
from Adafruit_IO import Client
aio = Client('')

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
    usbtemp_str= run_cmd("temper-poll | grep 'Device'  | awk '{print $3}' | cut -c 1-3")
    print('usbtemp_str: ', usbtemp_str)
    if usbtemp_str != "":
        #usbtemp = float(usbtemp_str)
        return usbtemp_str

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

while True:
        temp0 = read_temp0()
        temp1 = read_temp1()

        temp2 = get_usb_temp()

        print('Sensor 0 temp:',temp0)
        print('Sensor 1 temp:',temp1)
        print('Sensor 2 temp:',temp2)
        aio.send('temperature', temp0)
        aio.send('temperature-2', temp1)
        data0 = aio.receive('temperature')
        print('Received value: {0}'.format(data0.value))
        data1 = aio.receive('temperature')
        print('Received value: {0}'.format(data1.value))
        time.sleep(1)
