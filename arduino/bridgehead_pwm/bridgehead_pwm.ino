/*
                Fast PWM Test

Demostrates the generation of high speed PWM
using timers 1 and 4
There are two pieces of code:

One for pins 9, 10 and 11 using TIMER 1
with frequencies up to 62kHz

Other for pins 5 and 6 using TIMER 4
with frequencies up to 187kHz

*/

int pin_pulse = 7;


/**********************************************************
   Fast PWM on pins 9,10,11 (TIMER 1)
   
   Do not use analogWrite to pins 9, 10 or 11 if using 
   this functions as they use the same timer.
   
   Those functions will probably conflict with the 
   servo library.
   
   Uses 5 PWM frequencies between 61Hz and 62.5kHz
   
**********************************************************/

// Frequency modes for TIMER1
#define PWM62k   1   // 62500 Hz
#define PWM8k    2   //  7812 Hz
#define PWM1k    3   //   976 Hz
#define PWM244   4   //   244 Hz
#define PWM61    5   //    61 Hz

// Direct PWM change variables
// OCR = output compare register
#define PWM9   OCR1A
#define PWM10  OCR1B
#define PWM11  OCR1C

// Configure the PWM clock
// The argument is one of the 5 previously defined modes
void pwm91011configure(int mode) {
  // Configure DDRB
  // DDRB is the Port B Data Direction Register.
  DDRB |= 1 << 5;  // Set port B pin 5 (Arduino 9) to output mode
  DDRB |= 1 << 6;  // Set port B pin 6 (Arduino 10) to output mode
  DDRB |= 1 << 7;  // Set port B pin 7 (Arduino 11) to output mode

  // Configure TCCR1A
  //  00 : Channel A disabled D9
  //  00 : Channel B disabled D10
  //  00 : Channel C disabled D11
  //  01 : Fast PWM 8 bit
  // TCCR1A is the Timer/Counter1 Control Register A.
  TCCR1A = 1;      // Set prescaler to 1, to increment at 16 MHz
  TCCR1A |= 0x80;  // Activate channel 5
  TCCR1A |= 0x20;  // Activate channel 6
  TCCR1A |= 0x08;  // Activate channel 7

  // Configure TCCR1B
  // TCCR1B is the Timer/Counter 1 Control Register B.
  // Clock mode and Fast PWM 8 bit
  TCCR1B = mode | 0x08;

  // Configure TCCR1C
  // TCCR1C is the Timer/Counter 1 Control Register C.
  TCCR1C = 0;      // Stop timer/counter channel c
}

/**********************************************************
   Fast PWM on pins 5, 6 (High Speed TIMER 4)
   
   Do not use analogWrite to pins 5 or 6 if using 
   this functions as they use the same timer.
   
   Those functions will conflict with the 
   MSTIMER2 library.

   Uses 7 PWM frequencies between 2930Hz and 187.5kHz
   
   Timer 4 uses a PLL as input so that its clock frequency
   can be up to 96MHz on standard Arduino Leonardo.
   We limit imput frequency to 48MHz to generate 187.5kHz PWM
   If needed, we can double that up to 375kHz

**********************************************************/

// Frequency modes for TIMER4
#define PWM187k 1   // 187500 Hz
#define PWM94k  2   //  93750 Hz
#define PWM47k  3   //  46875 Hz
#define PWM23k  4   //  23437 Hz
#define PWM12k  5   //  11719 Hz
#define PWM6k   6   //   5859 Hz
#define PWM3k   7   //   2930 Hz

// Direct PWM change variables
#define PWM5 OCR4A
#define PWM6 OCR4D

// Configure the PWM clock
// The argument is one of the 7 previously defined modes
void pwm_5_6_configure(int mode) {
  // TCCR4A configuration
  TCCR4A |= 0x42; // Activate the complementary channel A (Arduino pin 5)
 
  // TCCR4B configuration
  TCCR4B = mode;
  
  // TCCR4C configuration
  TCCR4C |= 0x09;  // Activate channel C

  // TCCR4D configuration
  TCCR4D = 0;      // operate in PWM mode

  OCR4C = 255;     // Terminal count for Timer 4 PWM
  
  // Configure Port C
  DDRC |= 1 << 6;  // Set port C pin 6 (Arduino 5) to output mode
  DDRD |= 1 << 7;  // Set port D pin 7 (Arduino 6) to output mode
 
  // PLL Configuration
  // Use 96MHz / 2 = 48MHz
  PLLFRQ = (PLLFRQ & 0xCF)|0x30;
  // PLLFRQ = (PLLFRQ & 0xCF)|0x10; // Will double all frequencies
}

void setup() {
  // Configure Timer 1 (Pins 9, 10 and 11)
  // It will operate at 8 kHz
  // Valid options are: 
  //      PWM62k, PWM8k, PWM1k, PWM244 and PWM61
  // This works with Arctic Cooling AF12 und Noctua NF-F12.
  pwm91011configure(PWM8k);

  // Configure Timer 4 (Pins 5 and 6)
  // It will operate at 23 kHz
  // Valid options are:
  //     PWM187k, PWM94k, PWM47k, PWM23k, PWM12k, PWM6k and PWM3k
  pwm_5_6_configure(PWM23k);

  Serial.begin(9600);

  pinMode(pin_pulse, INPUT_PULLUP);
}

int min_int(int one, int other) {
  if (one < other)
    return one;
  return other;
}

int max_int(int one, int other) {
  if (one > other)
    return one;
  return other;
}

int rpm_target = 200;
int pwm_value = 40;
int pwm_min = 28;
int pwm_max = 255;
bool upwards = true;

/*
 * free air
 * PWM - RPM - ticking
 *   0 - off/restart
 *   1 - off/restart
 *   2 - off/restart
 *   3 - off/restart
 *   4 - off/restart
 *   5 - off/restart
 *   6 - off/restart
 *   7 - off/restart
 *   8 - off/restart
 *   9 - off/restart
 *  10 - off/restart
 *  11 - off/restart
 *  12 - off/restart
 *  13 - off/restart
 *  14 - off/restart
 *  15 - off/restart
 *  16 - off/restart
 *  17 - off/restart
 *  18 - off/restart
 *  19 - off/restart
 *  20 - off/restart
 *  21 - off/restart
 *  22 - off/restart
 *  23 - off/restart
 *  24 - off/restart
 *  25 - off/restart
 *  26 - off/restart
 *  27 - off/restart
 *  28 -  120
 *  32 -  180 - faint
 *  40 -  240 - yes
 *  48 -  360 - yes
 *  64 -  480 - yes
 *  96 -  840 - yes
 * 128 - 1140 - yes
 * 130 - 1140 - yes
 * 135 - 1140 - yes
 * 138 - 1200 - yes
 * 140 - 1200 - yes
 * 150 - 1320 - faint
 * 153 - 1320 - faint
 * 155 - 1380 - no
 * 160 - 1380 - no
 * 256 - off - no
 */

void loop() {
  unsigned long pulseDuration = pulseIn(pin_pulse, LOW);
  double frequency = 1000000 / pulseDuration;
  int rpm_current = (int) frequency / 4 * 60;
  Serial.print("RPM:");
  Serial.println(rpm_current);

  // target rpm
/*
  if (rpm_current < rpm_target - 1.5 / 255.0 * rpm_target)
    pwm_value = min_int(pwm_value + 1, 255);
  if (rpm_current > rpm_target + 1.5 / 255.0 * rpm_target)
    pwm_value = max_int(pwm_value - 1, 0);
*/


  // sweep rpm
  if (pwm_value == pwm_min)
    upwards = true;
  if (pwm_value == pwm_max)
    upwards = false;
  if (upwards)
    pwm_value = pwm_value + 1;
  else
    pwm_value = pwm_value - 1;

  // Those fast macros require a previous configuration
  // of the channels using the pwmSet9 and pwmSet6
  // functions
  // PWMn macros are fast to execute
  PWM5 = 255 - pwm_value;
  PWM6 = pwm_value;
  PWM9 = pwm_value;
  PWM10 = pwm_value;
  PWM11 = pwm_value; // TODO there is no pin 11 on the leonardo clones, I am using

  Serial.print("PWM:");
  Serial.println(pwm_value, DEC);

  // Small delay
  delay(100);
}

