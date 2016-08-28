"""
AL-FanControl

Control PC fans on an application level.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from communicate.bridgehead import Bridgehead
from config.configuration import Configuration
from control.controller import Controller
from ui.cli import CommandLineInterface

SCALING_FACTOR = 0.05  # usually in (0.01, 0.1)


def main():
    controller = Controller()
    cli = CommandLineInterface(controller)

    with Bridgehead(tty='/dev/ttyACM0', baudrate=9600) as bridgehead:
        rpms = [None] * len(Configuration.fans)
        while True:
            controller.control(rpms)
            cli.update()

            try:
                rpms = bridgehead(pwms=controller.pwms)
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    main()
