"""Python side of the Python to Arduino bridge."""

from __future__ import division, print_function

from contextlib import contextmanager
from multiprocessing import Process, Queue

import serial


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


@contextmanager
def Bridgehead(tty, baudrate):
    console = serial.Serial(tty, baudrate, timeout=1)

    queue_read = Queue(maxsize=1)
    reader_t = Process(target=_reader, args=([console, queue_read]))
    reader_t.start()

    queue_write = Queue(maxsize=1)
    writer_t = Process(target=_writer, args=([console, queue_write]))
    writer_t.start()

    yield (queue_read, queue_write)

    reader_t.terminate()
    writer_t.terminate()
