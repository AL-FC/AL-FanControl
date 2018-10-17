from __future__ import print_function

from config.configuration import Configuration
from microbar.microbar import MicroBar
from model.state import State
from ui.ui_abc import UserInterfaceBase

class SingleLineInterface(UserInterfaceBase):

    def update(self):
        microbars = [MicroBar(minimum=0, maximum=1)
                     for _ in Configuration().limits]
        out = ''
        out += 'Thermal Load: '
        for (fan, headroom, microbar) in zip(Configuration().fans, State().headrooms, microbars):
            try:
                load = str(round(1 - headroom, 2))[1:4].ljust(3, '0')
                bar = microbar.get_bar(value=1 - headroom)

                out += fan + ' '
                out += load + ' '
                out += bar + ' '
            except TypeError:
                pass

        print(out, end='\r')
