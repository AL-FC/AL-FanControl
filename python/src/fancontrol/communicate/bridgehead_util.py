"""
Parsers and generators of strings that go on the serial interface.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class IncompleteMessageError(Exception):
    pass


def message_to_rpms(message):
    durations = parse_durations(message=message)
    rpms = [duration2rpm(duration) for duration in durations]
    return rpms


def parse_durations(message):
    # if there is a line break in the message, parse the longest part
    if False and '\r' in message:
        sub_messages = message.split('\r')
        message = ''
        for sub_message in sub_messages:
            if message.count(':') == 0:
                message = sub_message
            if message.count(';') < sub_message.count(';'):
                message = sub_message

    if False and message.count(':') > 1:
        messages = message.split(':')
        if len(messages[0]) > len(messages[1]):
            message = message[0]
        else:
            message = message[1]

    if False and not message.count(";") >= 3:
        raise IncompleteMessageError(message)

    if not message.count(":") >= 1:
        raise IncompleteMessageError(message)

    if False and not message.startswith(':'):
        message = message.split(':')[1]

    message = message.lstrip(':')
    rpms = message.split(';')

    rpms = rpms[:-1] if rpms[-1] == '' else rpms
    return rpms


def duration2rpm(duration):
    duration = int(duration)
    if duration == 0:
        return duration
    rpm = 1000000 / duration / 2 * 60
    rpm = int(rpm)
    return rpm


def pwms_to_message(pwms):
    '''
    pwms = [90, 180, 180, None, 180, None, None, None]
    message = '090;180;180;123;180;123;123;123'
    '''
    pwms = [pwm if pwm is not None else 123 for pwm in pwms]
    pwms = [str(pwm) for pwm in pwms]
    message = ';'.join(pwms)
    return message


def signum(integer):
    if integer < 0:
        return -1
    elif integer > 0:
        return 1
    return 0
