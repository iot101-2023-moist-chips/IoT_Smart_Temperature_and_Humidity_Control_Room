# -*- coding: UTF-8 -*-
import sys
import paho.mqtt.client as mqtt
import time
from bs4 import BeautifulSoup
import requests

topic1 = "id/ikarosoo/sensor/evt/temperature"
topic2 = "id/ikarosoo/sensor/evt/humidity"
server = "44.216.90.150"

client = mqtt.Client()
client.connect(server, 1883, 60)

while(True):

    temp = -10
    humi = 60
    client.publish(topic1, temp)
    client.publish(topic2, humi)
    print(temp, humi)
    time.sleep(2)

client.loop_forever()