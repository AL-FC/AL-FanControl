"""
The actual fan controller.

Sets the fan power level according to the cooling needs.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from config.configuration import Configuration
from control.controller_util import get_headrooms, get_pwms
from model.state import State
from sense.temperatures import get_temps


class Controller(object):

    def control(self, rpms):
        # TODO adjust pwms to rpms

        temperatures = get_temps()

        headrooms = get_headrooms(temperatures=temperatures)

        pwms = get_pwms(headrooms=headrooms)

        State().update(headrooms=headrooms, pwms=pwms, rpms=rpms,
                       temperatures=temperatures)
