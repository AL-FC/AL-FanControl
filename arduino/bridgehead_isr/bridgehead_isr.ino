volatile int pwm_value = 128;

// ugly bootstrapping here.
// assume we were run just now when we really were not.
volatile int lastrun = micros();

// convention: use only microseconds

int calls[100];
volatile int index = 0;


void isr( ){
  int now = micros();
  calls[index] = now;
  index++;
  
  //int now = micros();
  //int runtime = now - lastrun;
  //int cycletime = 40; // 1 / 25 kHz = 40 microseconds
  //int timestep = runtime % cycletime;
  //
  //if (timestep > 255)
  //  lastrun = micros();

}


void setup() {
attachInterrupt(digitalPinToInterrupt(0), isr, CHANGE);
attachInterrupt(digitalPinToInterrupt(1), isr, CHANGE);
//real pin: attachInterrupt(digitalPinToInterrupt(2), isr);
//real pin: attachInterrupt(digitalPinToInterrupt(3), isr);
//real pin: attachInterrupt(digitalPinToInterrupt(7), isr);
}

void loop() {

}
