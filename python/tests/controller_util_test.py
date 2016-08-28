from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest.case import TestCase

from mock import MagicMock, Mock
from nose.tools import assert_raises

from fancontrol.control.controller_util import (_clip, _clip_pwm,
                                                _get_headroom, _get_pwm,
                                                get_headrooms, get_pwms)


class PublicApiNoneTests(TestCase):

    def test_get_headrooms_None(self):
        ambients = [None] * 3
        temps = [None] * 3
        limits = [None] * 3

        headrooms = get_headrooms(
            ambients=ambients, temps=temps, limits=limits)

        assert headrooms == [None, None, None]

    def test_get_pwms_None(self):
        headrooms = [None] * 3

        pwms = get_pwms(headrooms=headrooms)

        assert isinstance(pwms, type([None, None, None]))


class PrivateApiNoneTests(TestCase):

    def test_get_headroom_None(self):
        ambient = None
        temp = None
        limit = None

        headroom = _get_headroom(
            ambient=ambient, temp=temp, limit=limit)

        assert isinstance(headroom, type(None))

    def test_get_pwm_None(self):
        headroom = None

        pwm = _get_pwm(headroom=headroom)

        assert isinstance(pwm, type(None))

    def test_clip_pwm_None(self):
        pwm = None

        pwm = _clip_pwm(pwm=pwm)

        assert isinstance(pwm, type(None))

    def test_clip_None(self):
        minimum = None
        value = None
        maximum = None

        pwm = _clip(minimum=minimum, value=value, maximum=maximum)

        assert isinstance(pwm, type(None))


class PrivateApiSucceedingTests(TestCase):

    def test_get_headroom_half(self):
        ambient = 20
        temp = 50
        limit = 80

        headroom = _get_headroom(
            ambient=ambient, temp=temp, limit=limit)

        assert headroom == 0.50

    def test_get_headroom_one_quarter(self):
        ambient = 20
        temp = 65
        limit = 80

        headroom = _get_headroom(
            ambient=ambient, temp=temp, limit=limit)

        assert headroom == 0.25

    def test_get_headroom_three_quarter(self):
        ambient = 20
        temp = 35
        limit = 80

        headroom = _get_headroom(
            ambient=ambient, temp=temp, limit=limit)

        assert headroom == 0.75

    def test_get_pwm_middle(self):
        headroom = 0.5

        pwm = _get_pwm(headroom=headroom)

        assert pwm == 128

    def test_get_pwm_zero(self):
        headroom = 0.0

        pwm = _get_pwm(headroom=headroom)

        assert pwm == 0

    def test_get_pwm_full(self):
        headroom = 1.0

        pwm = _get_pwm(headroom=headroom)

        assert pwm == 255
