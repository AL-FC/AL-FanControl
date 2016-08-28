from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest.case import TestCase

from fancontrol import temperatures


class NoneTests(TestCase):

    def test_get_temps_None_only(self):
        chips = [None]
        features = [None]
        temps = temperatures.get_temps(chips=chips, features=features)

        assert isinstance(temps[0], type(None))

    def test_get_temps_None_multiple(self):
        chips = [None, None]
        features = [None, None]
        temps = temperatures.get_temps(chips=chips, features=features)

        assert isinstance(temps[0], type(None))
        assert isinstance(temps[1], type(None))

    def test_get_temps_None_before(self):
        chips = [None, 'k10temp', 'it8718']
        features = [None, 'temp1', 'temp1']
        temps = temperatures.get_temps(chips=chips, features=features)

        assert isinstance(temps[0], type(None))
        assert type(temps[1]) is float
        assert type(temps[2]) is float

    def test_get_temps_None_between(self):
        chips = ['k10temp', None, 'it8718']
        features = ['temp1', None, 'temp1']
        temps = temperatures.get_temps(chips=chips, features=features)

        assert type(temps[0]) is float
        assert isinstance(temps[1], type(None))
        assert type(temps[2]) is float

    def test_get_temps_None_after(self):
        chips = ['k10temp', 'it8718', None]
        features = ['temp1', 'temp1', None]
        temps = temperatures.get_temps(chips=chips, features=features)

        assert type(temps[0]) is float
        assert type(temps[1]) is float
        assert isinstance(temps[2], type(None))

    def test_get_temps_chip_before(self):
        chips = ['k10temp', None, None]
        features = ['temp1', None, None]
        temps = temperatures.get_temps(chips=chips, features=features)

        assert type(temps[0]) is float
        assert isinstance(temps[1], type(None))
        assert isinstance(temps[2], type(None))

    def test_get_temps_chip_between(self):
        chips = [None, 'k10temp', None]
        features = [None, 'temp1', None]
        temps = temperatures.get_temps(chips=chips, features=features)

        assert isinstance(temps[0], type(None))
        assert type(temps[1]) is float
        assert isinstance(temps[2], type(None))

    def test_get_temps_chip_after(self):
        chips = [None, None, 'k10temp']
        features = [None, None, 'temp1']
        temps = temperatures.get_temps(chips=chips, features=features)

        assert isinstance(temps[0], type(None))
        assert isinstance(temps[1], type(None))
        assert type(temps[2]) is float


class SensorTests(TestCase):

    def test_get_temps_one_chip_multiple_sensors(self):
        chips = ['it8718', 'it8718']
        features = ['temp1', 'temp2']
        temps = temperatures.get_temps(chips=chips, features=features)

        assert type(temps[0]) is float
        assert type(temps[1]) is float

    def test_get_temps_multiple_chips_one_sensor_each(self):
        chips = ['k10temp', 'it8718']
        features = ['temp1', 'temp1']
        temps = temperatures.get_temps(chips=chips, features=features)

        assert type(temps[0]) is float
        assert type(temps[1]) is float

    def test_get_temps_one_chip_one_sensor_multiple_fans(self):
        chips = ['k10temp', 'k10temp']
        features = ['temp1', 'temp1']
        temps = temperatures.get_temps(chips=chips, features=features)

        assert type(temps[0]) is float
        assert type(temps[1]) is float

        assert temps[0] == temps[1]
