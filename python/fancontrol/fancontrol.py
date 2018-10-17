"""
AL-FanControl
             Control PC fans on an application level.

Usage:
  fancontrol.py [--ui=<ui>]
  fancontrol.py (-h | --help)
  fancontrol.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --ui=<ui>     User interface in [sli, tui, nui] [default: sli].
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from docopt import docopt

from communicate.bridgehead import Bridgehead
from config.configuration import Configuration
from control.controller import Controller
from model.state import State
from ui.cli import CommandLineInterface
from ui.sli import SingleLineInterface
from version import __version__

SCALING_FACTOR = 0.05  # usually in (0.01, 0.1)


def _get_user_interface(ui):
    if ui == 'cli':
        user_interface = CommandLineInterface()
    if ui == 'sli':
        user_interface = SingleLineInterface()

    try:
        return user_interface
    except UnboundLocalError:
        print('Error: Command line parameter "--ui" was not valid.')
        exit()


def main(user_interface):
    controller = Controller()
    user_interface = _get_user_interface(ui=user_interface)
    ttys = ['/dev/ttyACM0', '/dev/ttyACM1', '/dev/ttyACM2', '/dev/ttyACM3']
    with Bridgehead(ttys=ttys, baudrate=9600) as bridgehead:
        rpms = [None] * len(Configuration.fans)
        while True:
            controller.control(rpms)

            user_interface.update()

            try:
                rpms = bridgehead(pwms=State().pwms)
            except KeyboardInterrupt:
                break


if __name__ == '__main__':
    arguments = docopt(__doc__, version='AL-FanControl %s' % __version__)
    _ui = arguments['--ui']
    main(user_interface=_ui)
