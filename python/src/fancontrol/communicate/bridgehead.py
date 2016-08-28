"""Python side of the Python to Arduino bridge."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from contextlib import contextmanager
from multiprocessing import Process, Queue

import serial

from communicate.bridgehead_util import message_to_rpms, pwms_to_message


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
    del tty, baudrate

    queue_read = Queue(maxsize=1)
    reader_t = Process(target=_reader, args=([console, queue_read]))
    reader_t.start()

    queue_write = Queue(maxsize=1)
    writer_t = Process(target=_writer, args=([console, queue_write]))
    writer_t.start()

    def bridgehead(pwms):
        queue_write.put(pwms_to_message(pwms=pwms))

        message = queue_read.get()
        rpms = message_to_rpms(message=message)
        return rpms

    yield bridgehead

    reader_t.terminate()
    writer_t.terminate()
