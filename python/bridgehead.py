"""Python side of the Python to Arduino bridge."""

from threading import Thread

import serial
from queue import Queue


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
        message = queue_write.get()
        console.writelines([message.encode('ASCII')])


def main():
    console = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    queue_read = Queue(maxsize=1)
    queue_write = Queue(maxsize=1)

    Thread(target=_reader, args=([console, queue_read])).start()
    Thread(target=_writer, args=([console, queue_write])).start()

    while True:
        # TODO calculate conversation starter

        message = '123;123;123'
        queue_write.put(message)

        pulse_durations = queue_read.get()
        print(pulse_durations)

        # TODO calculate response

if __name__ == '__main__':
    main()
