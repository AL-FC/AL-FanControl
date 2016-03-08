int outputPin = 45;
int analogPin = 0;
int val = 0;
int val2 = 0;

void setup(){
 TCCR5A = B00100011; // Fast PWM
 TCCR5B = B11001; //no prescalering
 OCR5A = 639; //count to 639 (16MHz/(640-1)=25 kHz)
 OCR5B = 315; //set PWM to 50%
 pinMode(outputPin, OUTPUT); //set outputPin(45) to output
}  
void loop(){
  val = analogRead(analogPin); //read potentiometer value
  val2 = val / 1023 * 639; //adjust val2 to <0;639>
  OCR5B = val; //set PWM value
}
