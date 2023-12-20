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
    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'html.parser')
    airTable = soup.find_all("div", class_="card card_dust")

    for air in airTable:
        today = air.find_all("span", class_="value _cnPm10Value")
        for data in today:
            dust = data.text
    
    client.publish(topic, dust)
    
    time.sleep(10)

client.loop_forever()