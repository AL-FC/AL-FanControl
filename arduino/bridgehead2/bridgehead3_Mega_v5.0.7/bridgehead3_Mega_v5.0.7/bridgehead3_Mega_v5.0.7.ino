//                   FAN_{  15,   7,   6,   5,   4,   3,   2,   1,   0,   8,   9,  10,  11,  12,  13,  14}
const int PINS_PULSE[] = { A14,  21,  20,  19,  18,  17,  16,  15,  14,  A0,  A2,  A4,  A6,  A8, A10, A12};
//                    Log{ INF;0.50;0.49; INF;0.48;0.47;0.44;0.47;0.47;0.47;0.43; INF;0.47;0.48; INF;0.48}
//            Pulse works{  No, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes}
const int PINS_PWM[] =   {   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  45,  46,  44};
//            PWM   works{  No, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes, Yes}
const int MICROSECONDS_IN_ONE_SECOND = 1000000;

void setup() {
    const int PWM_FREQUENCY_TARGET = 24000;

    // The base frequency for pins 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 44, 45, and 46 is 31250 Hz
    // Allowed divisors are always 1 and 8; we don't need to worry about the rest for PWM fans.
    // So set a pin's PWM frequency of each clock to 31250 Hz / 1 = 31250 Hz ~ 125 % of 25000 Hz
    // TCCR3B
    setPwmFrequency( 2, 1);
    setPwmFrequency( 3, 1);
    setPwmFrequency( 5, 1);
    // TCCR4B
    setPwmFrequency( 6, 1);
    setPwmFrequency( 7, 1);
    setPwmFrequency( 8, 1);
    // TCCR2B
    setPwmFrequency( 9, 1);
    setPwmFrequency(10, 1);
    // TCCR1B
    setPwmFrequency(11, 1);
    setPwmFrequency(12, 1);
    // TCCR5B
    setPwmFrequency(44, 1);
    setPwmFrequency(45, 1);
    setPwmFrequency(46, 1);

    // The base frequency for pins 4, and 13 is 62500 Hz
    // Allowed divisors are always 1 and 8; we don't need to worry about the rest for PWM fans.
    // Set pin 4's PWM frequency of their clock to 62500 / 8 = 7813 Hz ~ 31 % of 25000 Hz
    // Set pin 13's PWM frequency of their clock to 62500 / 8 = 7813 Hz ~ 31 % of 25000 Hz
    // TCCR0B
    setPwmFrequency(4, 8);
    setPwmFrequency(13, 8);

    // space out fan speeds a bit to avoid some resonance
    int pwms[16] = {46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61};

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
    //Serial.begin(SERIAL_BD_RATE);

    // Sending data to the host seems to mess up the timing.
    // So don't do that to preserve that last timer for PWM, too.
    //Serial.println("");
    //Serial.println("Setup done");
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
    //Serial.println(pulseDurations);
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

            // Sending data to the host seems to mess up the timing.
            // So don't do that to preserve that last timer for PWM, too.
            // logPulseIntervals();
        }
    } else {
        // We got a message this time.
        if (LAST_MESSAGE == message) {
            // This message was repeated by the host.
            // So log the pulse intervals.

            // Sending data to the host seems to mess up the timing.
            // So don't do that to preserve that last timer for PWM, too.
            // logPulseIntervals();            
        } else {
            // This message was new.
            // So update the last message.
            LAST_MESSAGE = message;
            // Also update the PWMs and the log pulse intervals.
            setPwms(messageToPwms(message));
            // Sending data to the host seems to mess up the timing.
            // So don't do that to preserve that last timer for PWM, too.
            // logPulseIntervals();
        }
    }

    // Sending data to the host seems to mess up the timing.
    // So don't do that to preserve that last timer for PWM, too.
    //Serial.println(".");
}

void setPwmFrequency(int pin, int divisor) {
    /**
     * Divides a given PWM pin frequency by a divisor.
     *
     * The resulting frequency is equal to the base frequency divided by
     * the given divisor:
     *   - Base frequencies:
     *      o The base frequency for pins 3, 9, 10, and 11 is 31250 Hz.
     *      o The base frequency for pins 5 and 6 is 62500 Hz.
     *   - Divisors:
     *      o The divisors available on pins 5, 6, 9 and 10 are: 1, 8, 64,
     *        256, and 1024.
     *      o The divisors available on pins 3 and 11 are: 1, 8, 32, 64,
     *        128, 256, and 1024.
     *
     * PWM frequencies are tied together in pairs of pins. If one in a
     * pair is changed, the other is also changed to match:
     *   - Pins 5 and 6 are paired on timer0
     *   - Pins 9 and 10 are paired on timer1
     *   - Pins 3 and 11 are paired on timer2
     *
     * Note that this function will have side effects on anything else
     * that uses timers:
     *   - Changes on pins 3, 5, 6, or 11 may cause the delay() and
     *     millis() functions to stop working. Other timing-related
     *     functions may also be affected.
     *   - Changes on pins 9 or 10 will cause the Servo library to function
     *     incorrectly.
     *
     * Thanks to macegr of the Arduino forums for his documentation of the
     * PWM frequency divisors. His post can be viewed at:
     *   https://forum.arduino.cc/index.php?topic=16612#msg121031
     */

    byte mode;

    if(pin == 1) {
      // TODO Do Bit-Bang/software PWM
      // at pin == 1 / Arduino D1 / Board FAN_15
      return;
    }

    //    FAN_5       FAN_11
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

    //     FAN_9       FAN_10
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

    //    FAN_0        FAN_8
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

    //    FAN_7       FAN_6       FAN_4
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

    //    FAN_3       FAN_2       FAN_1
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

    //    FAN_14       FAN_12       FAN_13
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
