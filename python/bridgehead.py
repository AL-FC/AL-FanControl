"""Python side of the Python to Arduino bridge."""

from __future__ import print_function

from multiprocessing import Process, Queue

import serial

from temperatures import get_temps
from util import (format_fans, format_names, format_ports, format_pwms,
                  format_rpms, format_temps, format_tmps,
                  IncompleteMessageError, parse_rpms, pwms_to_message)


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

    while True:
        # TODO calculate conversation starter

        ports = list(range(0, 8))
        fans = ['CPU', 'Case', 'Case', None, 'GPU', None, None, None]
        pwms = [90, 180, 180, None, 180, None, None, None]

        queue_write.put(pwms_to_message(pwms=pwms))

        try:
            message = queue_read.get()
        except KeyboardInterrupt:
            break

        rpms = parse_rpms(message=message)

        temps = get_temps()

        print(format_fans(fans=fans))
        print(format_ports(ports=ports))
        print(format_pwms(pwms=pwms))
        print(format_rpms(rpms=rpms))
        print(format_temps(temps=temps))
        print()

        # TODO calculate response

    reader_t.terminate()
    writer_t.terminate()


if __name__ == '__main__':
    main()
