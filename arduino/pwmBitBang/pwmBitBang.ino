// pins to which the fans are connected physically
// connector index  0  1  2  3   4   5   6   7
const int NUMBER_OF_PINS = 8;
const int PINS_PWM[] = {2, 6, 9, 4, A3, 15, 10, A1};
const int PINS_PULSE[] = {3, 7, 8, 5, A2, 14, 16, A0};

void setup() {
  // initialize serial connection
  Serial.begin(300);
  
  for (int i = 0; i < NUMBER_OF_PINS; i++) {
    pinMode(PINS_PULSE[i], INPUT);
    digitalWrite(PINS_PULSE[i],HIGH);
    pinMode(PINS_PWM[i], OUTPUT);
  }
}

int loop_count = 0;
int values[] = {127, 127, 127, 127, 127, 127, 127, 127};

void loop() {
  run_pwm();
  return;
  
  // get message from serial console
  String message = "";
  while (Serial.available())
    message.concat((char) Serial.read());
  if (message == "")
    return;

  for (int i = 0; i < NUMBER_OF_PINS; i++) {
    values[i] = message.substring(0, message.indexOf(';')).toInt();
  }

  
  loop_count++;
  if (loop_count % 10000 == 0) {
    Serial.println("testtesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttesttest");
    Serial.println(values[0], DEC);
  }
}

void run_pwm () {
  for (int i = 0; i < NUMBER_OF_PINS; i++) {
    digitalWrite(i, HIGH);
  }

  delayMicroseconds(128);

  for (int duty = 0; duty < 255; duty++) {
    for (int i = 0; i < NUMBER_OF_PINS; i++) {
      if(1) { //duty == values[i]) {
        digitalWrite(i, LOW);
      }
    }
    delayMicroseconds(1);
  }
}
