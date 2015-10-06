// fancontrol.ino
//
// Intentionally left simple and stupid so that all intelligent code can reside on the host side.

#include <SoftPWM.h>

// pins to which the fans are connected physically
int PINS_PWM[] = {2, 6, 9};
int PINS_PULSE[] = {3, 7, 8};

void setup() {
  // init serial
  Serial.begin(9600);
  
  // init pwm
  SoftPWMBegin();
  for (int i = 0; i < 3; i++) {
    pinMode(PINS_PULSE[i], INPUT);
    digitalWrite(PINS_PULSE[i],HIGH);
    
    SoftPWMSetFadeTime(PINS_PWM[i], 100, 100);
    SoftPWMSet(PINS_PWM[i], 0);
  }
}

void loop() {
  // get message from serial console
  String message = "";
  while (Serial.available())
    message.concat((char) Serial.read());
  if (message == "")
    return;

  // iterate fans, collect pulse durations
  String pulseDurations = ":";
  for (int i = 0; i != 3; i++) {
    // parse value left of a ';' and set according fan
    SoftPWMSet(PINS_PWM[i], message.substring(0, message.indexOf(';')).toInt());
    
    // strip part left of a ';' from message
    message = message.substring(message.indexOf(';') + 1);

    // respond with pulse durations
    pulseDurations = pulseDurations + String(pulseIn(PINS_PULSE[i], LOW)) + ";";
    
    // if there is no further ';' in the message, parse and set the rest of it
    if (message.indexOf(';') == -1)
      SoftPWMSet(PINS_PWM[i], message.toInt());
  }
  Serial.println(pulseDurations);
}

