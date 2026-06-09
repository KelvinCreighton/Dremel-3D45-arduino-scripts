#include <Servo.h>

// 0 = relative (+10 / -10)
// 1 = absolute (type exact angle)
int mode = 1;

Servo probeServo;
int currentAngle = 95;

void setup() {
  Serial.begin(9600);
  probeServo.attach(11);
  probeServo.write(currentAngle);
  Serial.println("Starting at " + String(currentAngle) + ".");
}

void loop() {
  if (Serial.available() > 0) {
    int input = Serial.parseInt();
    while (Serial.available()) Serial.read(); // drain leftover bytes
    int newAngle;

    if (mode == 0) {
      newAngle = constrain(currentAngle + input, 0, 180);
    } else {
      newAngle = constrain(input, 0, 180);
    }

    probeServo.write(newAngle);
    currentAngle = newAngle;
    Serial.print("Position: ");
    Serial.println(currentAngle);
  }
}
