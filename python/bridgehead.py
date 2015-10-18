"""Python side of the Python to Arduino bridge."""

from __future__ import print_function

from multiprocessing import Process, Queue

import serial

from temperatures import get_temps
from util import (format_buffers, format_decisions, format_differences,
                  format_directions, format_fans, format_hysteresises,
                  format_limits, format_names, format_ports, format_pwms,
                  format_pwms_new, format_rpms, format_temps, format_tmps,
                  parse_rpms, pwms_to_message, signum)

SCALING_FACTOR = 0.05  # usually in (0.01, 0.1)


def _reader(console, queue_read):
    while True:
        try:
            response = console.readline().decode('ASCII')
        except TypeError:
            pass
        response = response.strip()
        if response != '':
            queue_read.put(response)


def _writer(console, queue_write):
    while True:
        try:
            message = queue_write.get()
        except KeyboardInterrupt:
            break
        console.writelines([message.encode('ASCII')])


def main():
    console = serial.Serial('/dev/ttyACM4', 9600, timeout=1)
    queue_read = Queue(maxsize=1)
    queue_write = Queue(maxsize=1)

    reader_t = Process(target=_reader, args=([console, queue_read]))
    reader_t.start()
    writer_t = Process(target=_writer, args=([console, queue_write]))
    writer_t.start()

    pwms = [255, 255, 255, None, 120, None, None, None]  # at idle

    while True:
        queue_write.put(pwms_to_message(pwms=pwms))

        ports = list(range(0, 8))
        fans = ['CPU', 'Case', 'Case', None, 'GPU', None, None, None]

        try:
            message = queue_read.get()
        except KeyboardInterrupt:
            break
        rpms = parse_rpms(message=message)

        chips = ['k10temp', 'it8718', 'it8718', None, 'radeon', None, None,
                 None]
        features = ['temp1', 'temp1', 'temp3', None, 'temp1', None, None, None]

        temps = [int(round(temp, 0)) if temp is not None else None
                 for temp in get_temps(chips=chips,
                                       features=features)]

        limits = [60, 40, 50, None, 70, None, None, None]

        buffers = [
            limit - temp if limit is not None and temp is not None else None
            for (temp, limit) in zip(temps, limits)
        ]

        hysteresises = [5, 5, 5, None, 5, None, None, None]

        decisions = [
            abs(limit - temp) > hysteresis if
            limit is not None and temp is not None and hysteresis is not None
            else None
            for (limit, temp, hysteresis) in zip(limits, temps, hysteresises)
        ]

        directions = [signum(limit - temp)
                      if limit is not None and temp is not None else None
                      for (limit, temp) in zip(limits, temps)]

        differences = [
            round(pwm * direction * SCALING_FACTOR, 0) if decision else None
            for (pwm, direction, decision) in zip(pwms, directions, decisions)
        ]

        pwms_new = [pwm + difference
                    if pwm is not None and difference is not None else pwm
                    for (pwm, difference) in zip(pwms, differences)]
        pwms_new = [0 if pwm_new < 0 else 255 if pwm_new > 255 else pwm_new
                    for pwm_new in pwms_new]

        print(format_fans(fans=fans))
        print(format_ports(ports=ports))
        print(format_pwms(pwms=pwms))
        print(format_rpms(rpms=rpms))
        print(format_temps(temps=temps))
        print(format_limits(limits=limits))
        print(format_buffers(buffers=buffers))
        print(format_hysteresises(hysteresises=hysteresises))
        print(format_decisions(decisions=decisions))
        print(format_directions(directions=directions))
        print(format_differences(differences=differences))
        print(format_pwms_new(pwms_new=pwms_new))

        pwms = pwms_new

        print()

        # TODO calculate response

    reader_t.terminate()
    writer_t.terminate()


if __name__ == '__main__':
    main()
