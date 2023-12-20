# -*- coding: UTF-8 -*-
import sys
import paho.mqtt.client as mqtt
import time
from bs4 import BeautifulSoup
import requests

topic = "id/ikarosoo/Crawling/dust"
server = "44.216.90.150"

client = mqtt.Client()
client.connect(server, 1883, 60)

URL = "https://weather.naver.com/air/02390589"  #미세먼지 

while(True):

    dust = 30
    client.publish(topic, dust)
    print(dust)
    time.sleep(2)

client.loop_forever()