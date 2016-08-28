
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from fancontrol.config.configuration import Configuration
from fancontrol.ui.cli_util import (format_ambients, format_fans,
                                    format_headrooms, format_limits,
                                    format_ports, format_pwms, format_pwms_new,
                                    format_rpms, format_temps)


class CommandLineInterface(object):

    def __init__(self, controller):
        self.controller = controller

    def update(self):
        """
        Update the command line interface to the latest controller state.
        """

        # print configuration
        print(format_fans(fans=Configuration.fans))
        print(format_ports(ports=Configuration.ports))
        print(format_ambients(ambients=Configuration.ambients))
        print(format_limits(limits=Configuration.limits))

        # print runtime state
        print(format_pwms(pwms=self.controller.pwms))
        print(format_rpms(rpms=self.controller.rpms))
        print(format_temps(temps=self.controller.temps))
        print(format_headrooms(headrooms=self.controller.headrooms))
        print(format_pwms_new(pwms_new=self.controller.pwms))
        print()
