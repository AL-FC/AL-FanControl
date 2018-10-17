from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import abc


class UserInterfaceBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update(self):
        """Update user interface according to the given state."""
        raise NotImplementedError()
