#include <SoftPWM.h>

int pin_pwm = 5;
int pin_pulse = 6;
int pwm_value = 64;
int target_rpm = 2000;

void setup()
{
  Serial.begin(9600);
  pinMode(pin_pulse, INPUT);
  digitalWrite(pin_pulse,HIGH);
  
  SoftPWMBegin();
  SoftPWMSet(pin_pwm, 0);
  SoftPWMSetFadeTime(pin_pwm, 100, 100);
  SoftPWMSet(pin_pwm, pwm_value);
}

void loop()
{
  unsigned long pulseDuration = pulseIn(pin_pulse, LOW);
  Serial.print("Duration: ");
  Serial.print(pulseDuration);
  Serial.print(" ");

  double frequency = 1000000/pulseDuration;
  Serial.print("Frequency:");
  Serial.print(frequency);
  Serial.print(" ");
  
  double rpm = frequency/2*60;
  Serial.print("RPM:");
  Serial.print(rpm);
  Serial.print(" ");
  
  if (rpm > target_rpm + 0.03 * target_rpm) {
    pwm_value = pwm_value + 10;
  }
  if (pwm_value > 254) {
    pwm_value = 254;
  }

  if (rpm < target_rpm - 0.03 * target_rpm) {
    pwm_value = pwm_value - 10;
  }
  
  if (pwm_value < 1) {
    pwm_value = 1;
  }

  Serial.print("PWM:");
  Serial.print(pwm_value);
  Serial.println();

  SoftPWMSet(pin_pwm, pwm_value);
}
