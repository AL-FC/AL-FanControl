void setup() {
  // pinMode(17, OUTPUT);  // pin 17 is connected to the serial busy led on the arduino pro micro
  pinMode(8, OUTPUT);
  
  // initialize timer1
  noInterrupts();
  TCCR1A = 0;
  TCNT1  = 0;
  // 512 = 24 - 48 µs
  // 384 = 16 - 32 µs
  // 256 = 12 - 24 µs
  // 128 =  6 - 12 µs
  //  64 =  3 -  6 µs
  //  48 =  2 -  4 µs
  //  40 =  1 -  2 µs
  //  36 =  0.8 - 1.6
  OCR1A = 1024;            // compare match register 16MHz/64/25kHz
  TCCR1B = 0;
  TCCR1B |= (1 << WGM12);   // CTC mode
  //TCCR1B |= (1 << CS12);    // 256 prescaler
  //TCCR1B |= (1 << CS11) | (1 << CS10); // 64 prescaler
  //TCCR1B |= (1 << CS11);    // 8 prescaler
  TCCR1B |= (1 << CS10);    // 1 prescaler
  TIMSK1 |= (1 << OCIE1A);  // enable timer compare interrupt
  interrupts();             // enable all interrupts

  Serial.begin(2400);
}

// volatile long times[2] = {0, 0};
// volatile int index = 0;
// volatile bool alive = false;
volatile int cycles = 0;

volatile int duty = 128;

// timer compare interrupt service routine
ISR(TIMER1_COMPA_vect) {
  // toggle LED pin

  //times[index] = micros();
  //index = (index + 1) % 2;

  //alive = true;

  // for 384
  // cycles = (cycles + 1) % 32767;
  // PORTB = (cycles > 16384 << PB0);    // pin 17 == Port B 0 == PB0

  // for 1024
  int freq = 8192;
  cycles = (cycles + 1) % freq;
  //PORTB = ((cycles > (freq / 255 * duty)) << PB0);    // pin 17 == Port B 0 == PB0
  PORTB = ((cycles / freq) > (duty / 255) << PB4);    // pin 17 == Port B 0 == PB0
}

unsigned long previousMillis = 0;
const long interval = 2000;           // interval at which to blink (milliseconds)

const int duties [] = {228, 160, 64, 128, 32, 192};
int index = 0;

void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    Serial.println(".");

    //long duration = times[0] - times[1];
    //if (duration < 0)
    //  duration = -duration;
    //Serial.println(duration, DEC);

    //Serial.println(alive, BIN);
    //alive = false;

    duty = duties[index];
    index = (index + 1) % 5;
  }
}

