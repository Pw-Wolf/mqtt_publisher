#!/usr/bin/python3
import re
import subprocess
import uuid
from json import dumps
from random import randint

import paho.mqtt.client as mqtt

from adafruit_dht import DHT22
from board import D22

# This is the Publisher

device_id = hex(uuid.getnode())
ip = "ip"
port = 1883
topic = "test/Topic"

def check_CPU_temp():
	err, msg = subprocess.getstatusoutput('vcgencmd measure_temp')
	if err: return "--"
	m = re.search(r'-?\d\.?\d*', msg)
	return float(m.group())

def room_temp():
	SENSOR_PIN = D22
	dht22 = DHT22(SENSOR_PIN, use_pulseio=False)
	return dht22.temperature, dht22.humidity

if __name__ == "__main__":
	temperature, humidity = room_temp()
	message = {
			"name":"Raspberry Pi 4",
			"cpu_temp":check_CPU_temp(),
			"id":f"{device_id}",
			"multiGraphs": False,
			"sensors" : {"Temp_Graph|-20,60":f"{temperature:.1f}", "Humidity_Text":f"{humidity:.1f}%"}
	}
	client = mqtt.Client()
	client.connect(ip,port,60)
	client.publish(topic, dumps(message));
	client.disconnect();