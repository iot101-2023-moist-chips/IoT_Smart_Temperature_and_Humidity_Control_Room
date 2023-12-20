#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Arduino.h>

#define             M_IN1 12
#define             M_IN2 13

int motorA_vector = 1;    // 모터의 회전방향이 반대일 시 0을 1로 

const char*         ssid ="갤럭시탭";
const char*         password = "54958735";
const char*         mqttServer = "44.216.90.150";
const int           mqttPort = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
void callback(char* topic, byte* payload, unsigned int length);

void setup() {
    Serial.begin(115200);
    pinMode(M_IN1, OUTPUT);
    pinMode(M_IN2, OUTPUT);
    WiFi.mode(WIFI_STA); 
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("Connected to the WiFi network");
    client.setServer(mqttServer, mqttPort);
    client.setCallback(callback);
 
    while (!client.connected()) {
        Serial.println("Connecting to MQTT...");
 
        if (client.connect("ESP8266_term_linear")) {
            Serial.println("connected");  
        } else {
            Serial.print("failed with state "); 
            Serial.println(client.state());
            delay(2000);
        }
    }
    client.subscribe("id/ikarosoo/linear/cmd");
    digitalWrite(M_IN1, motorA_vector);    // IN1번에 LOW(motorA_vector가 0이면 HIGH)  
    digitalWrite(M_IN2, !motorA_vector);    // IN2번에 LOW(motorA_vector가 0이면 HIGH) 
}

void loop() {
    client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
 
    char msgBuffer[20];
    if(!strcmp(topic, "id/ikarosoo/linear/cmd")) {
        int i;
        for(i = 0; i < (int)length; i++) {
            msgBuffer[i] = payload[i];
        } 
        msgBuffer[i] = '\0';
        Serial.printf("\n%s -> %s", topic, msgBuffer);
        if(!strcmp(msgBuffer, "on")) {
          digitalWrite(M_IN1, motorA_vector);    // IN1번에 HIGH(motorA_vector가 0이면 LOW) 
          digitalWrite(M_IN2, !motorA_vector);   // IN2번에 LOW(motorA_vector가 0이면 HIGH) 
          } else if(!strcmp(msgBuffer, "off")) {
          digitalWrite(M_IN1, !motorA_vector);   // IN1번에 LOW(motorA_vector가 0이면 HIGH)  
          digitalWrite(M_IN2, motorA_vector);    // IN2번에 HIGH(motorA_vector가 0이면 LOW) 
          delay(10);
        }
    }
}
