import sys
import paho.mqtt.client as mqtt
import time

topic1 = "id/ikarosoo/sensor/evt/temperature"
topic2 = "id/ikarosoo/sensor/evt/humidity"
topic3 = "id/ikarosoo/Crawling/dust"
topic4 = "id/ikarosoo/Crawling/Temp_Out"
server = "44.216.90.150"

received_temperature = False
received_humidity = False
received_dust = False
received_Temp_Out = False
temperature = 0
humidity = 0
dust = 0
Temp_Out = 0

count = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with RC : " + str(rc))
    client.subscribe(topic1)
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.subscribe(topic4)

def on_message(client, userdata, msg):
    global count
    global received_temperature, received_humidity, received_dust, received_Temp_Out, temperature, humidity, dust, Temp_Out
    
    if topic1 == msg.topic:
        temperature = float(msg.payload.decode('utf-8'))
        received_temperature = True
        
    if topic2 == msg.topic:
        humidity = float(msg.payload.decode('utf-8'))
        received_humidity = True

    if topic3 == msg.topic:
       dust = float(msg.payload.decode('utf-8'))
       received_dust = True
    
    if topic4 == msg.topic:
       Temp_Out = float(msg.payload.decode('utf-8'))
       received_dust = True
       
    if received_temperature and received_humidity and received_dust and received_Temp_Out:
        print("Temperature :", temperature)
        print("Humidity :", humidity)
        print("Dust :", dust)
        print("Temp_Out : ", Temp_Out)
        
        # Reset flags for the next set of messages
        received_temperature = False
        received_humidity = False
        received_dust = False
        received_Temp_Out = False
        
    print("Temperature :", temperature)
    print("Humidity :", humidity)
    print("Dust :", dust)
    print("Temp_Out : ", Temp_Out)
    
    # 미세먼지 나쁨
    if dust > 80:
        client.publish("id/ikarosoo/linear/cmd", "off")
        count = 0
        print("미세먼지 나빠")

    # 미세먼지 좋음
    else:
        print("미세먼지 좋아")
        # 방 습도가 낮다
        if humidity < 50:
            client.publish("id/ikarosoo/linear/cmd", "off")
            client.publish("id/ikarosoo/humidiffer/cmd", "on")
            count = 0
            print("습도 낮아")
        # 방 습도가 높다
        else:
            if abs(temperature - Temp_Out) > 8:
                client.publish("id/ikarosoo/linear/cmd", "off")
                count = 0
                print("너무 온도 차이 커")
            else:
                if count >= 5 and count < 10:
                    client.publish("id/ikarosoo/linear/cmd", "off")
                    time.sleep(2)
                    count += 1
                    print("닫기")
                elif count == 10:
                    time.sleep(2)
                    count = 0
                    print("리셋")
                else:
                    client.publish("id/ikarosoo/linear/cmd", "on")
                    time.sleep(2)
                    count += 1
                    print("오픈")

client = mqtt.Client()
client.connect(server, 1883, 60)
client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
