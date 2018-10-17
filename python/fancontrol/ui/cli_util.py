from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

RJUST = 12


def format_fans(fans):
    return format_line(prefix='fans'.rjust(RJUST), values=fans)


def format_rpms(rpms):
    return format_line(prefix='rpms'.rjust(RJUST), values=rpms)


def format_pwms(pwms):
    return format_line(prefix='pwms'.rjust(RJUST), values=pwms)


def format_tmps(tmps):
    return format_line(prefix='temps'.rjust(RJUST), values=tmps)


def format_names(names):
    return format_line(prefix='names'.rjust(RJUST), values=names)


def format_ports(ports):
    return format_line(prefix='ports'.rjust(RJUST), values=ports)


def format_temps(temps):
    return format_line(prefix='temps'.rjust(RJUST), values=temps)


def format_ambients(ambients):
    return format_line(prefix='ambients'.rjust(RJUST), values=ambients)


def format_limits(limits):
    return format_line(prefix='limits'.rjust(RJUST), values=limits)


def format_buffers(buffers):
    return format_line(prefix='buffers'.rjust(RJUST), values=buffers)


def format_headrooms(headrooms):
    return format_line(prefix='headrooms'.rjust(RJUST), values=headrooms)


def format_directions(directions):
    return format_line(prefix='directions'.rjust(RJUST), values=directions)


def format_differences(differences):
    return format_line(prefix='differences'.rjust(RJUST), values=differences)


def format_pwms_new(pwms_new):
    return format_line(prefix='new pwms'.rjust(RJUST), values=pwms_new)


def format_line(prefix, values):
    line = ''
    line += prefix
    line += ': '
    line += '['
    for value in values:
        try:
            if value >= 1:
                value = int(round(value, 0))
            if 1 > value != 0:
                value = str(value)[1:4].ljust(3, '0')
        except TypeError:
            # value is None
            pass

        value = str(value) if value is not None else ''
        line += value.rjust(6)
        line += ', '
    line = line[:-len(', ')]
    line += ']'

    return line
