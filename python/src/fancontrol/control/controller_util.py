from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


def get_headrooms(temps, limits, ambients):
    return [
        _get_headroom(ambient=ambient, limit=limit, temp=temp)
        for temp, limit, ambient in zip(temps, limits, ambients)
    ]


def _get_headroom(ambient, limit, temp):
    """
    Calculate the thermal headroom.

    The thermal headroom is the remaining fraction of the temperature range.
    Return None, if any temperature is none.
    """
    if None in [ambient, limit, temp]:
        return None

    return (1 - ((temp - ambient) / (limit - ambient)))


def get_pwms(headrooms):
    return [
        _get_pwm(headroom=headroom)
        for headroom in headrooms
    ]


def _get_pwm(headroom):
    if headroom is None:
        return None

    return _clip_pwm(round(255 * headroom, 0))


def _clip_pwm(pwm):
    return _clip(pwm, 0, 255)


def _clip(value, minimum, maximum):
    if None in [value, minimum, maximum]:
        return None

    return sorted([minimum, value, maximum])[1]
