from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class State(object):
    """
    Describe the current state of the observed and influenced system.
    """

    _headrooms = [None, None, None, None, None, None, None, None]
    _pwms = [169, None, None, None, 167, 181, 196, 176]  # at idle
    _rpms = [None, None, None, None, None, None, None, None]
    _temperatures = [None, None, None, None, None, None, None, None]

    _state = {}  # borg pattern: eternal state

    def __new__(cls, *p, **k):
        del p, k

        self = object.__new__(cls)
        self.__dict__ = cls._state
        return self

    def update(self, headrooms, pwms, rpms, temperatures):
        """
        Update the state of the observed and influenced system.
        """
        self._headrooms = headrooms
        self._pwms = pwms
        self._rpms = rpms
        self._temperatures = temperatures

    @property
    def headrooms(self):
        """
        Return the thermal headrooms of the observed and influenced system.
        """
        return self._headrooms

    @property
    def pwms(self):
        """
        Return the PWM values of the controlled fans.
        """
        return self._pwms

    @property
    def rpms(self):
        """
        Return the RPM values of the controlled fans.
        """
        return self._rpms

    @property
    def temperatures(self):
        """
        Return the temperatures of the observed and influenced system.
        """
        return self._temperatures
