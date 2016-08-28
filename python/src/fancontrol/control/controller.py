"""
The actual fan controller.

Sets the fan power level according to the cooling needs.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from fancontrol.config.configuration import Configuration
from fancontrol.control.controller_util import get_headrooms, get_pwms
from fancontrol.sense.temperatures import get_temps


class Controller(object):

    def __init__(self):
        self.pwms = [169, None, None, None, 167, 181, 196, 176]  # at idle
        self.rpms = [None, None, None, None, None, None, None, None]
        self.temps = [None, None, None, None, None, None, None, None]
        self.headrooms = [None, None, None, None, None, None, None, None]

    def control(self, rpms):
        self.rpms = rpms
        # TODO adjust pwms to rpms

        self.temps = get_temps(chips=Configuration.chips,
                               features=Configuration.features)

        self.headrooms = get_headrooms(
            temps=self.temps,
            limits=Configuration.limits,
            ambients=Configuration.ambients)

        # TODO reintroduce hysteresis to avoid oscillating

        self.pwms = get_pwms(self.headrooms)
