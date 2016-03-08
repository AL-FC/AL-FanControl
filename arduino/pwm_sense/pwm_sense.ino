int pin_pulse = 10;
int pin_pwm = A0;

void setup() {
  Serial.begin(9600);
  pinMode(pin_pulse, INPUT);
  pinMode(pin_pwm, OUTPUT);
  digitalWrite(pin_pulse,HIGH);
}

void loop() {
  unsigned long pulseDuration = pulseIn(pin_pulse, LOW);
  double frequency = 1000000/pulseDuration;
  
  // Serial.print("pulse duration:");
  // Serial.println(pulseDuration);
  
  // Serial.print("time for full rev. (microsec.):");
  // Serial.println(pulseDuration*2);
  // Serial.print("freq. (Hz):");
  // Serial.println(frequency/2);
  Serial.print("RPM:");
  Serial.println(frequency/2*60);
  
  if (frequency/2*60 > 5200){
    analogWrite(pin_pwm, 255);
  } else {
    analogWrite(pin_pwm, 128);
  }
  delay(1000);
}
