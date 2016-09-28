
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from config.configuration import Configuration
from model.state import State
from ui.cli_util import (format_ambients, format_fans, format_headrooms,
                         format_limits, format_ports, format_pwms,
                         format_pwms_new, format_rpms, format_temps)
from ui.ui_abc import UserInterfaceBase


class CommandLineInterface(UserInterfaceBase):

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
        print(format_pwms(pwms=State().pwms))
        print(format_rpms(rpms=State().rpms))
        print(format_temps(temps=State().temperatures))
        print(format_headrooms(headrooms=State().headrooms))
        print()
