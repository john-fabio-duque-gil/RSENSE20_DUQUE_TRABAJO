#include <Arduino.h>
#include "MPU9250.h"
#include <WiFi.h>

// an MPU9250 object with the MPU-9250 sensor on I2C bus 0 with address 0x68
MPU9250 IMU(Wire,0x68);
int status;

const char* ssid       = "iPhone";
const char* password   = "123456789";

const uint16_t port = 8090;
const char * host = "172.20.10.3";


void setup() {

  Serial.begin(115200);
  delay(1000);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());


  while(!Serial) {}

  // start communication with IMU 
  status = IMU.begin();
  if (status < 0) {
    while(1) {}
  }

  //  Frecuencia de muestreo de 10Hz (cada 100ms)
  IMU.setSrd(99);
}


void loop() {

  WiFiClient client;

  while(!client.connect(host, port)){
    Serial.println("Connection to host failed");
    delay(1000);
  }
   
  IMU.readSensor();

  Serial.print(IMU.getAccelX_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getAccelY_mss(),6);
  Serial.print("\t");
  Serial.print(IMU.getAccelZ_mss(),6);
  Serial.print("\t");
  Serial.print(degrees(IMU.getGyroX_rads()),6);
  Serial.print("\t");
  Serial.print(degrees(IMU.getGyroY_rads()),6);
  Serial.print("\t");
  Serial.println(degrees(IMU.getGyroZ_rads()),6);


  client.print("1");
  client.print(IMU.getAccelX_mss(),6);
  client.print("\t");
  client.print(IMU.getAccelY_mss(),6);
  client.print("\t");
  client.print(IMU.getAccelZ_mss(),6);
  client.print("\t");
  client.print(degrees(IMU.getGyroX_rads()),6);
  client.print("\t");
  client.print(degrees(IMU.getGyroY_rads()),6);
  client.print("\t");
  client.print(degrees(IMU.getGyroZ_rads()),6);
  delay(100);
  client.stop();
    
}
