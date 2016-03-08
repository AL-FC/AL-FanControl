#include <SoftPWM.h>

// GPU, CPU, Case
int pins_pwm[] = {2, 6, 9};
int pins_pulse[] = {3, 7, 8};

// gaming
int values_pwm[] = {114, 130, 108};
int rpm_targets[] = {3000, 1500, 3000};

// leisure
// int values_pwm[] = {192, 64, 160};
// int rpm_targets[] = {2000, 2000, 2500};

void setup()
{
  Serial.begin(19200);
  SoftPWMBegin();
  
  for (int i = 0; i < 3; i++) {
    pinMode(pins_pulse[i], INPUT);
    digitalWrite(pins_pulse[i],HIGH);
    
    SoftPWMSetFadeTime(pins_pwm[i], 100, 100);
    SoftPWMSet(pins_pwm[i], values_pwm[i]);
  }
}

void loop()
{
  for (int i = 0; i < 3; i++) {
    unsigned long pulseDuration = pulseIn(pins_pulse[i], LOW);
    //Serial.print("Duration: ");
    //Serial.print(pulseDuration);
    //Serial.print(" ");
  
    double frequency = 1000000/pulseDuration;
    //Serial.print("Frequency:");
    //Serial.print(frequency);
    //Serial.print(" ");
    
    int rpm = frequency/2*60;
    Serial.print("RPM:");
    Serial.print(rpm);
    Serial.print(" ");
    
    if (rpm > rpm_targets[i] + 0.03 * rpm_targets[i]) {
      values_pwm[i] = values_pwm[i] + 1;
    }
    if (values_pwm[i] > 254) {
      values_pwm[i] = 254;
    }
  
    if (rpm < rpm_targets[i] - 0.03 * rpm_targets[i]) {
      values_pwm[i] = values_pwm[i] - 1;
    }
    if (values_pwm[i] < 1) {
      values_pwm[i] = 1;
    }
  
    Serial.print("PWM:");
    Serial.print(values_pwm[i]);
    Serial.print(" ");
    
    SoftPWMSet(pins_pwm[i], values_pwm[i]);
  }
  Serial.println();
}

