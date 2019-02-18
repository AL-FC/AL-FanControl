// fancontrol.ino
//
// Intentionally kept simple and stupid so that all intelligent code can reside on the host side.

#include <SoftPWM.h>

// Pins to which the fans are connected physically
// Connector index  0   1   2   3   4   5   6   7
int PINS_PWM[]   = {2,  6,  9,  4, A3, 15, 10, A1};
int PINS_PULSE[] = {3,  7,  8,  5, A2, 14, 16, A0};

void setup() {
    // Initialize serial connection
    Serial.begin(9600);

    // Initialize pulse pins
    for (int i = 0; i < 8; i++)     
        pinMode(PINS_PULSE[i], INPUT_PULLUP);

    // Initialize SoftPWM library
    SoftPWMBegin(SOFTPWM_INVERTED);
    SoftPWMSetFadeTime(ALL, 0, 0);

    // Send 30 % as a start up pulse
    int pwms[8] = {77, 77, 77, 77, 77, 77, 77, 77};
    setPwms(pwms);
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
    for (int i = 0; i < 8; i++)
        SoftPWMSet(PINS_PWM[i], pwms[i]);
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
}
