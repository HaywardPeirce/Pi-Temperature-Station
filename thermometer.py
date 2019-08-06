#!/usr/bin/env python

import os
import os.path
import glob
import time
from subprocess import *

import configparser
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError, InfluxDBServerError
from requests.exceptions import ConnectionError

config = configparser.ConfigParser()
config.read('config.ini')

delay = float(config['GENERAL']['Delay'])
output = bool(config['GENERAL'].get('Output', fallback=True))
# print(output)

influxAddress = config['INFLUXDB']['Address']
influxPort = float(config['INFLUXDB']['Port'])
influxDatabase = config['INFLUXDB']['Database']
influxUser = config['INFLUXDB'].get('Username', fallback='')
influxPassword = config['INFLUXDB'].get('Password', fallback='')

influx_client = InfluxDBClient(influxAddress, influxPort, influxUser, influxPassword, influxDatabase)

#Read the Adafruit API key in from file /home/pi/apikey.txt.
# file = open('/home/pi/apikey.txt', 'r')
# apikey = file.readline().replace("\n", '')
# file.close()

# # Import library and create instance of REST client.
# from Adafruit_IO import Client
# aio = Client(apikey)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

device_folder = []
device_file = []

base_dir = '/sys/bus/w1/devices/'
device_folder.append(glob.glob(base_dir + '28*')[0])
device_file.append(device_folder[0] + '/w1_slave')
device_folder.append(glob.glob(base_dir + '28*')[1])
device_file.append(device_folder[1] + '/w1_slave')
print('Device File 0:', device_file[0])
print('Device File 1:', device_file[1])

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def get_usb_temp():
    usbtemp_str= run_cmd("temper-poll | grep 'Device'  | awk '{print $3}' | cut -c 1-4")
    #print('usbtemp_str: ', usbtemp_str)
    if usbtemp_str != "":
        usbtemp = float(usbtemp_str) - 8
        return usbtemp
    else: return False

def readTempGPIO(index):
    lines = readRawTempGPIO(index)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = readRawTempGPIO(index)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    else: return False
    
def readRawTempGPIO(index):
    f = open(device_file[index], 'r')
    lines = f.readlines()
    f.close()
    return lines
    
def readTemps(index):
    
    if index != 2:
       temp = readTempGPIO(index)
    else: temp = get_usb_temp()
    
    return temp

def sendInfluxData(json_data):

    if output:
        #print(json_data)
        print(type(json_data))

    try:
        influx_client.write_points(json_data)
    except (InfluxDBClientError, ConnectionError, InfluxDBServerError) as e:
        if hasattr(e, 'code') and e.code == 404:

            print('Database {} Does Not Exist.  Attempting To Create'.format(influxDatabase))

            influx_client.create_database(influxDatabase)
            influx_client.write_points(json_data)

            return

        print('ERROR: Failed To Write To InfluxDB')
        print(e)

    if output:
        print('Written To Influx: {}'.format(json_data))

def main():
        
    checkList = [None, None, None]
    
    tempList = []
    #temps = []
    #data = []
    
    # loop through length of list of devices to check
    for index, temp in enumerate(checkList):
        
        #read in the temp for the entry
        tempTemp = readTemps(index)
        
        #if the temerature was read in (and isn't still null)
        if tempTemp != False:
            print('Sensor ', index, ' temp: ',tempTemp)
            tempList.append(tempTemp)
    
    #Find the average of the temperatures that were read in        
    tempFinal = sum(tempList)/len(tempList)

    # Round `finalTemp` to three decimal places, and retain it as a float
    tempFinal = float('%.3f'%(tempFinal))
    
    #send the temperature to adafruit
    # aio.send('temperature', '%.3f'%tempFinal)
    # value = aio.receive('temperature')
    # print('Received value: {0}'.format(value.value))
    
    #only send the data if there is non-null data to send
    if tempFinal is not None:

        json_body = [{
            "measurement": "housetemps",
            "tags": {
                "location": "livingroom"
            },
            "fields": {
                "temperature": tempFinal
            }
        }]

        sendInfluxData(json_body)

    time.sleep(delay)

if __name__ == '__main__':
    main()