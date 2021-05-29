const int PINS_PULSE[] = {14, 15, 16, 17, 18, 19, SDA, SCL, A0, A1, A2, A4, A7, A9, A15, A12};
const int PINS_PWM[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 44, 45, 46};
const int MICROSECONDS_IN_ONE_SECOND = 1000000;


void setup() {
    const int PWM_FREQUENCY_TARGET = 24000;

    // The base frequency for pins 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, and 46 is 31250 Hz
    // So set a pin's PWM frequency of each clock to 31250 Hz / 1 = 31250 Hz
    setPwmFrequency( 2, 1);
    setPwmFrequency( 6, 1);
    setPwmFrequency( 9, 1);
    setPwmFrequency(11, 1);
    setPwmFrequency(44, 1);

    // The base frequency for pins 4 and 13 is 62500 Hz
    // Set pin 4's PWM frequency to 62500/8 = 7813 Hz
    setPwmFrequency(4, 2);

    // space out fan speeds a bit to avoid some resonance
    int pwms[16] = {38, 39, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38};

    // Shuffle PWM values to load fans randomly
    for (int i = 0; i < 16 - 1; i++) {
        int j = random(0, 16 - i);

        int t = pwms[i];
        pwms[i] = pwms[j];
        pwms[j] = t;
    }

    // Send a start up pulse
    setPwms(pwms);

    // Initialize pulse pins
    for (int i = 0; i < 16; i++)     
        pinMode(PINS_PULSE[i], INPUT_PULLUP);

    const int SERIAL_BD_RATE = 19200;
    Serial.begin(SERIAL_BD_RATE);
    Serial.write("Setup done");
}

int* messageToPwms(String message) {
    // Caution: Non-reentrant return value.
    static int pwms[16];

    int separator_position;
    for (int i = 0; i < 16; i++) {
        // Determine next separator
        separator_position = message.indexOf(';');
  
        // Parse value left of a ';' 
        pwms[i] = message.substring(0, separator_position).toInt();

        // Strip part left of a ';' from message
        message = message.substring(separator_position + 1);
    }

    return pwms;
}

void logPulseIntervals() {
    String pulseDurations = "";

    // Collect pulse durations from all fans into a message
    for (int i = 0; i < 16; i++)
        pulseDurations = \
            pulseDurations + \
            String(
                float(MICROSECONDS_IN_ONE_SECOND) /
                pulseIn(PINS_PULSE[i], LOW, 200000)
            ) + \
            ";";

    // Log message to the host via the serial interface
    Serial.println(pulseDurations);
}

void setPwms(int pwms[]) {
    // Set PWM value to each fan
    for (byte channel_index = 0; channel_index < 16; channel_index++)
        analogWrite(PINS_PWM[channel_index], pwms[channel_index]);
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

    Serial.println(".");
}

void setPwmFrequency(int pin, int divisor) {
    byte mode;

    if(pin == 4 || pin == 13) {
        switch(divisor) {
            case 1: mode = 0x01; break;
            case 8: mode = 0x02; break;
            case 64: mode = 0x03; break;
            case 256: mode = 0x04; break;
            case 1024: mode = 0x05; break;
            default: return;
        }
        TCCR0B = TCCR0B & B11111000 | mode;
        return;
    }

    if(pin == 11 || pin == 12) {
        switch(divisor) {
            case 1: mode = 0x01; break;
            case 8: mode = 0x02; break;
            case 64: mode = 0x03; break;
            case 256: mode = 0x04; break;
            case 1024: mode = 0x05; break;
            default: return;
        }
        TCCR1B = TCCR1B & B11111000 | mode;
        return;
    }

    if(pin == 9 || pin == 10) {
        switch(divisor) {
            case 1: mode = 0x01; break;
            case 8: mode = 0x02; break;
            case 32: mode = 0x03; break;
            case 64: mode = 0x04; break;
            case 128: mode = 0x05; break;
            case 256: mode = 0x06; break;
            case 1024: mode = 0x07; break;
            default: return;
        }
        TCCR2B = TCCR2B & B11111000 | mode;
        return;
    }

    if(pin == 2 || pin == 3 || pin == 5) {
        switch(divisor) {
            case 1: mode = 0x01; break;
            case 8: mode = 0x02; break;
            case 64: mode = 0x03; break;
            case 256: mode = 0x04; break;
            case 1024: mode = 0x05; break;
            default: return;
        }
        TCCR3B = TCCR3B & B11111000 | mode;
        return;
    }

    if(pin == 6 || pin == 7 || pin == 8) {
        switch(divisor) {
            case 1: mode = 0x01; break;
            case 8: mode = 0x02; break;
            case 64: mode = 0x03; break;
            case 256: mode = 0x04; break;
            case 1024: mode = 0x05; break;
            default: return;
        }
        TCCR4B = TCCR4B & B11111000 | mode;
        return;
    }

    if(pin == 44 || pin == 45 || pin == 46) {
        switch(divisor) {
            case 1: mode = 0x01; break;
            case 8: mode = 0x02; break;
            case 64: mode = 0x03; break;
            case 256: mode = 0x04; break;
            case 1024: mode = 0x05; break;
            default: return;
        }
        TCCR5B = TCCR5B & B11111000 | mode;
        return;
    }
}
