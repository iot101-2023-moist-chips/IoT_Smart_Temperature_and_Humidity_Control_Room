import sys
import paho.mqtt.client as mqtt
import time
from bs4 import BeautifulSoup
import requests

topic = "id/ikarosoo/Crawling/Temp_Out"
server = "44.216.90.150"

client = mqtt.Client()
client.connect(server, 1883, 60)

URL = "https://rp5.ru/%EC%8B%9C%ED%9D%A5%EC%9D%98_%EB%82%A0%EC%94%A8"  #온도 
while(1):
    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'html.parser')

    temperature_data = soup.find("div", {"id" : "ArchTemp"})

    Temp_Out = temperature_data.find("span", {"class" : "t_0"}).text

    client.publish(topic, Temp_Out[:-3])

    print(Temp_Out[:-3])

client.loop_forever()