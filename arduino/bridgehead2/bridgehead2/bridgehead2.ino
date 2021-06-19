#include <PalatisSoftPWM.h>

int PINS_PULSE[] = {3, 7, 8, 5, A2, 14, 16, A0};

SOFTPWM_DEFINE_PIN2_CHANNEL(0);
SOFTPWM_DEFINE_PIN6_CHANNEL(1);
SOFTPWM_DEFINE_PIN9_CHANNEL(2);
SOFTPWM_DEFINE_PIN4_CHANNEL(3);
SOFTPWM_DEFINE_PINA3_CHANNEL(4);
SOFTPWM_DEFINE_PIN15_CHANNEL(5);
SOFTPWM_DEFINE_PIN10_CHANNEL(6);
SOFTPWM_DEFINE_PINA1_CHANNEL(7);

const int PWM_CHANNEL_COUNT = 8;
const int PWM_LEVEL_COUNT = 256;
SOFTPWM_DEFINE_OBJECT_WITH_PWM_LEVELS(PWM_CHANNEL_COUNT, PWM_LEVEL_COUNT);

void setup() {
  const int PWM_FREQUENCY = 512;
  PalatisSoftPWM.begin(PWM_FREQUENCY);

  // space out fan speeds a bit to avoid some resonance
  // int pwms[8] = {128, 128, 128, 128, 128, 128, 128, 128};
  // int pwms[8] = {114, 118, 122, 126, 130, 134, 138, 142};

  // space out fan speeds a bit to avoid some resonance
  // int pwms[8] = {96, 96, 96, 96, 96, 96, 96, 96};
  // int pwms[8] = {82, 86, 90, 94, 98, 102, 106, 110};
  int pwms[8] = {38, 40, 42, 44, 46, 48, 50, 52};

  // Shuffle PWM values to load fans randomly
  for (int i = 0; i < 8 - 1; i++) {
      int j = random(0, 8 - i);

      int t = pwms[i];
      pwms[i] = pwms[j];
      pwms[j] = t;
  }

  // Send a start up pulse
  setPwms(pwms);

  // Initialize pulse pins
  for (int i = 0; i < 8; i++)     
      pinMode(PINS_PULSE[i], INPUT_PULLUP);

  const int SERIAL_BD_RATE = 19200;
  Serial.begin(SERIAL_BD_RATE);
}

int* messageToPwms(String message){
    // Caution: Non-reentrant return value.
    static int pwms[8];
  
    int separator_position;
    for (int i = 0; i < 8; i++) {
        // Determine next separator
        separator_position = message.indexOf(';');
        
        // Parse value left of a ';' 
        pwms[i] = message.substring(0, separator_position).toInt();
    
        // Strip part left of a ';' from message
        message = message.substring(separator_position + 1);
    }
    
    return pwms;
}

void logPulseIntervals () {
    String pulseDurations = "";
    
    // Collect pulse durations from all fans into a message
    for (int i = 0; i < 8; i++)
        pulseDurations = pulseDurations + String(pulseIn(PINS_PULSE[i], LOW, 100000)) + ";";

    // Log message to the host via the serial interface
    Serial.println(pulseDurations);
}

void setPwms (int pwms[]) {
    // Set PWM value to each fan
    for (byte channel = 0; channel < PalatisSoftPWM.size(); channel++)
      PalatisSoftPWM.set(
        channel,
        PalatisSoftPWM.PWMlevels() - PalatisSoftPWM.PWMlevels() * pwms[channel] / 256
      );
}

String LAST_MESSAGE = "";
void loop() {
    // Get message from serial console
    String message = "";
    while (Serial.available())
        message.concat((char) Serial.read());

    if (message == "") {
        if (LAST_MESSAGE == "") {
            // We have never gotten a message.
            // So keep waiting for one.
            return;
        } else {
            // We have not gotten a message this time, but last time.
            // So use the last message as our current one.
            message = LAST_MESSAGE;
            // We already know that the current message equals last message.
            // So log the pulse intervals.
            logPulseIntervals();
        }
    } else {
        // We got a message this time.
        if (LAST_MESSAGE == message) {
            // This message was repeated by the host.
            // So log the pulse intervals.
            logPulseIntervals();            
        } else {
            // This message was new.
            // So update the last message.
            LAST_MESSAGE = message;
            // Also update the PWMs and the log pulse intervals.
            setPwms(messageToPwms(message));
            logPulseIntervals();
        }
    }

    // Serial.println("");
    PalatisSoftPWM.printInterruptLoad();
}
