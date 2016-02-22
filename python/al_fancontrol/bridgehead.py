"""Python side of the Python to Arduino bridge."""

from __future__ import division, print_function

from multiprocessing import Process, Queue

import serial
from temperatures import get_temps
from util import (clip_pwm, format_ambients, format_buffers, format_decisions,
                  format_differences, format_directions, format_fans,
                  format_hysteresises, format_limits, format_names,
                  format_percentages, format_ports, format_pwms,
                  format_pwms_new, format_rpms, format_temps, format_tmps,
                  message_to_rpms, pwms_to_message, signum)

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
    pwms = [128, 128, 128, None, 45, None, 128, 128]  # at idle
    ports = [0, 1, 2, 3, 4, 5, 6, 7]
    fans = ['CPU', 'Case', 'Case', None, 'GPU', None, 'Test', 'Test']
    chips = ['k10temp', 'it8718', 'it8718', None, 'radeon', None, 'it8718',
             'it8718']
    features = ['temp1', 'temp2', 'temp1', None, 'temp1', None, 'temp1',
                'temp3']
    ambients = [25, 30, 30, None, 30, None, 25, 25]
    limits = [60, 70, 70, None, 80, None, 60, 60]
    hysteresises = [3, 3, 3, None, 3, None, 3, 3]

    console = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    queue_read = Queue(maxsize=1)
    queue_write = Queue(maxsize=1)

    reader_t = Process(target=_reader, args=([console, queue_read]))
    reader_t.start()
    writer_t = Process(target=_writer, args=([console, queue_write]))
    writer_t.start()

    while True:
        queue_write.put(pwms_to_message(pwms=pwms))

        try:
            message = queue_read.get()
        except KeyboardInterrupt:
            break
        rpms = message_to_rpms(message=message)

        temps = [
            temp if temp is not None else None
            for temp in get_temps(chips=chips,
                                  features=features)
        ]

        decisions = [
            abs(limit - temp) > hysteresis
            if None not in [limit, temp, hysteresis] else None
            for (limit, temp, hysteresis) in zip(limits, temps, hysteresises)
        ]

        percentages = [
            100 * ((temp - ambient) / (limit - ambient))
            if None not in [temp, limit] else None
            for temp, limit, ambient in zip(temps, limits, ambients)
        ]

        pwms_new = [clip_pwm(255 - 255 * percentage / 100)
                    if percentage is not None else None
                    for percentage in percentages]

        print(format_fans(fans=fans))
        print(format_ports(ports=ports))
        print(format_pwms(pwms=pwms))
        print(format_rpms(rpms=rpms))
        print(format_temps(temps=temps))
        print(format_ambients(ambients=ambients))
        print(format_limits(limits=limits))
        print(format_hysteresises(hysteresises=hysteresises))
        print(format_decisions(decisions=decisions))
        print(format_percentages(percentages=percentages))
        print(format_pwms_new(pwms_new=pwms_new))
        print()

        pwms = pwms_new

    reader_t.terminate()
    writer_t.terminate()


if __name__ == '__main__':
    main()
