#include <Servo.h>

Servo probeServo;
int currentAngle = 90;

void setup() {
  Serial.begin(9600);
  probeServo.attach(11);
  probeServo.write(currentAngle);
  Serial.println("Starting at 90. Enter +/- to move (e.g. +10 or -10):");
}

void loop() {
  if (Serial.available() > 0) {
    int delta = Serial.parseInt();
    int newAngle = constrain(currentAngle + delta, 0, 180);
    probeServo.write(newAngle);
    currentAngle = newAngle;
    Serial.print("Position: ");
    Serial.println(currentAngle);
  }
}
