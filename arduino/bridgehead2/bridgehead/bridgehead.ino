/* Demonstrates usage of the PalatisSoftPWM library.
   Fades Arduino pin 13 from PWM value 0 to the highest level and back to 0 again.
*/

#include <PalatisSoftPWM.h>

//Configure Arduino pin as PWM channels

SOFTPWM_DEFINE_PIN2_CHANNEL(0);
//SOFTPWM_DEFINE_PIN3_CHANNEL(1);
SOFTPWM_DEFINE_PIN4_CHANNEL(1);
//SOFTPWM_DEFINE_PIN5_CHANNEL(3);
SOFTPWM_DEFINE_PIN6_CHANNEL(2);
//SOFTPWM_DEFINE_PIN7_CHANNEL(5);
//SOFTPWM_DEFINE_PIN8_CHANNEL(6);
SOFTPWM_DEFINE_PIN9_CHANNEL(3);

SOFTPWM_DEFINE_PIN10_CHANNEL(8);
//SOFTPWM_DEFINE_PIN14_CHANNEL(9);
SOFTPWM_DEFINE_PIN15_CHANNEL(10);
//SOFTPWM_DEFINE_PIN16_CHANNEL(11);

// Arduino Pro Micro onboard LED pin
// SOFTPWM_DEFINE_PIN17_CHANNEL(0);

//SOFTPWM_DEFINE_PINA0_CHANNEL(12);
SOFTPWM_DEFINE_PINA1_CHANNEL(13);
//SOFTPWM_DEFINE_PINA2_CHANNEL(14);
SOFTPWM_DEFINE_PINA3_CHANNEL(15);

SOFTPWM_DEFINE_OBJECT_WITH_PWM_LEVELS(8, 256);

// (ms)The length of time for to go from PWM value 0 to the highest level and back to 0 again. The maximum allowed value is 8388.
const unsigned int fadeDuration = 100;

void setup() {
  // begin with a certain PWM frequency
  PalatisSoftPWM.begin(100);

  Serial.begin(19200);
}

void loop() {
  // fade from PWM value 0 to the highest value
  for (byte value = 0; value < PalatisSoftPWM.PWMlevels() - 1; value++) {
    delayMicroseconds(fadeDuration * 1000UL / PalatisSoftPWM.PWMlevels() / 2);
    for (byte channel = 0; channel < PalatisSoftPWM.size(); channel++) {
      PalatisSoftPWM.set(channel, value);
    }
  }
  // fade back to PWM value 0
  for (int value = PalatisSoftPWM.PWMlevels() - 1; value >= 0; value--) {
    delayMicroseconds(fadeDuration * 1000UL / PalatisSoftPWM.PWMlevels() / 2);
    for (byte channel = 0; channel < PalatisSoftPWM.size(); channel++) {
      PalatisSoftPWM.set(channel, value);
    }
  }

  PalatisSoftPWM.printInterruptLoad();

}
