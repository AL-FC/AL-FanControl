from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from config.configuration import Configuration


def get_headrooms(temperatures):
    """
    Calculate the thermal headroom for each sensor.

    Thermal headroom is the remaining fraction of the temperature range.
    List entry will be None, if any temperature for its sensor is none.
    """
    limits = Configuration.limits
    ambients = Configuration.ambients

    return [
        _get_headroom(ambient=ambient, limit=limit, temp=temp)
        for temp, limit, ambient in zip(temperatures, limits, ambients)
    ]


def _get_headroom(ambient, limit, temp):
    if None in [ambient, limit, temp]:
        return None

    return 1 - ((temp - ambient) / (limit - ambient))


def get_pwms(headrooms):
    """
    Calculate pwm value for each fan.

    PWM value is proportional to the given headroom and limited to [0, 255].
    List entry will be None, if its headroom is None.
    """
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
