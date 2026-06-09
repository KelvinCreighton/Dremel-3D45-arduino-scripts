
const int PROBE_PIN = 18;  // Z-MIN signal pin on Arduino Mega

bool lastState = HIGH;

void setup() {
  Serial.begin(9600);
  pinMode(PROBE_PIN, INPUT_PULLUP);  // Internal pull-up keeps pin HIGH when open
  Serial.print("Watching pin D");
  Serial.println(PROBE_PIN);
}

void loop() {
  bool currentState = digitalRead(PROBE_PIN);

  // Only print when state changes (avoids spamming the monitor)
  if (currentState != lastState) {
    delay(20);
    currentState = digitalRead(PROBE_PIN);

    if (currentState == LOW) {
      Serial.println("switch closed");
    } else {
      Serial.println("switch open");
    }

    lastState = currentState;
  }
}
