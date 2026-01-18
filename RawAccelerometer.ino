/*
  Based on the 'simple accelerometer' example
  Sends pure accelerometer output over the serial line
*/

#include <Arduino_LSM9DS1.h>

void setup() {
  Serial.begin(9600);
  IMU.begin();
}

void loop() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    Serial.print(x);
    Serial.print(',');
    Serial.print(y);
    Serial.print(',');
    Serial.println(z);
  }`
}
