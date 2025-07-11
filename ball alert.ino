// === Ball Tracking Alert System Using Ultrasonic Sensor + Buzzer ===
// Author: Sajid TP

#define TRIG_PIN 9
#define ECHO_PIN 10
#define BUZZER_PIN 3

long duration;
int distance;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
}

void loop() {
  // Clear trigger pin
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Send 10 microsecond pulse
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Read echo pulse
  duration = pulseIn(ECHO_PIN, HIGH);

  // Calculate distance (cm)
  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // If object (ball) is closer than 15cm, alert
  if (distance < 15) {
    tone(BUZZER_PIN, 1000); // buzzer on
    delay(200);
    noTone(BUZZER_PIN);     // buzzer off
    delay(200);
  } else {
    noTone(BUZZER_PIN);
  }

  delay(300); // slight delay between readings
}
