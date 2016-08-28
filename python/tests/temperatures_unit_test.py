"""
Tests for the temperature data source.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from unittest.case import TestCase

from mock import MagicMock, Mock
from nose.tools import assert_raises

from fancontrol.temperatures import (ChipFeatureMismatchError, NoSuchChipError,
                                     NoSuchFeatureError, _get_detected_chips,
                                     _get_index, _get_temperatures)


class GetIndexUnitTests(TestCase):

    def test_get_index(self):
        chips = ['k10temp']
        chip = Mock()
        chip.prefix = 'k10temp'
        features = ['temp1']
        feature = Mock()
        feature.name = 'temp1'
        start_index = 0

        index = _get_index(
            chips, chip, features, feature, start_index)

        assert index == 0

    def test_get_index_no_such_chip_beyond(self):
        chips = ['k10temp']
        chip = Mock()
        chip.prefix = 'k10temp'
        features = ['temp1', 'temp1']
        feature = Mock()
        feature.name = 'temp1'
        start_index = 1

        assert_raises(NoSuchChipError, _get_index,
                      chips, chip, features, feature, start_index)

    def test_get_index_no_such_feature_beyond(self):
        chips = ['k10temp', 'k10temp']
        chip = Mock()
        chip.prefix = 'k10temp'
        features = ['temp1']
        feature = Mock()
        feature.name = 'temp1'
        start_index = 1

        assert_raises(NoSuchFeatureError, _get_index,
                      chips, chip, features, feature, start_index)

    def test_get_index_this_is_not_the_chip_you_are_looking_for(self):
        chips = ['k10temp', 'it8718', 'k10temp']
        chip = Mock()
        chip.prefix = 'k10temp'
        features = ['temp1', 'temp1', 'temp1']
        feature = Mock()
        feature.name = 'temp1'
        start_index = 1

        assert_raises(ChipFeatureMismatchError, _get_index,
                      chips, chip, features, feature, start_index)

    def test_get_index_this_is_not_the_feature_you_are_looking_for(self):
        chips = ['k10temp', 'k10temp', 'it8718', ]
        chip = Mock()
        chip.prefix = 'k10temp'
        features = ['temp1', 'temp2', 'temp1']
        feature = Mock()
        feature.name = 'temp1'
        start_index = 1

        assert_raises(ChipFeatureMismatchError, _get_index,
                      chips, chip, features, feature, start_index)


class GetTemperaturesUnitTests(TestCase):

    def test_get_temperatures_same_sensor_two_fans(self):
        k10temp = MagicMock()
        k10temp.prefix = 'k10temp'
        temp1 = MagicMock()
        temp1.name = 'temp1'
        temp1.get_value.return_value = 42
        k10temp.__iter__.return_value = [temp1]
        chips_detected = [k10temp]

        chips = ['k10temp', 'k10temp']
        features = ['temp1', 'temp1']

        temps = _get_temperatures(chips=chips,
                                  features=features,
                                  chips_detected=chips_detected)

        assert temps[0] == 42
        assert temps[1] == 42

    def test_get_temperatures_chip_not_requested(self):
        k10temp = MagicMock()
        k10temp.prefix = 'k10temp'
        temp1 = MagicMock()
        temp1.name = 'temp1'
        temp1.get_value.return_value = 42
        k10temp.__iter__.return_value = [temp1]
        chips_detected = [k10temp]

        chips = ['it8718', 'it8718']
        features = ['temp1', 'temp1']

        temps = _get_temperatures(chips=chips,
                                  features=features,
                                  chips_detected=chips_detected)

        assert temps[0] is None
        assert temps[1] is None

    def test_get_temperatures_feature_not_requested(self):
        k10temp = MagicMock()
        k10temp.prefix = 'k10temp'
        temp1 = MagicMock()
        temp1.name = 'temp1'
        temp1.get_value.return_value = 42
        k10temp.__iter__.return_value = [temp1]
        chips_detected = [k10temp]

        chips = ['k10temp', 'k10temp']
        features = ['temp2', 'temp2']

        temps = _get_temperatures(chips=chips,
                                  features=features,
                                  chips_detected=chips_detected)

        assert temps[0] is None
        assert temps[1] is None

    def test_get_temperatures_no_such_feature(self):
        k10temp = MagicMock()
        k10temp.prefix = 'k10temp'
        temp1 = MagicMock()
        temp1.name = 'temp1'
        temp1.get_value.return_value = 42
        k10temp.__iter__.return_value = [temp1]
        chips_detected = [k10temp, k10temp]

        chips = ['k10temp', 'k10temp']
        features = ['temp1', 'temp2']

        temps = _get_temperatures(chips=chips,
                                  features=features,
                                  chips_detected=chips_detected)

        assert temps[0] == 42
        assert temps[1] is None

    def test_get_temperatures_no_such_chip(self):
        k10temp = MagicMock()
        k10temp.prefix = 'k10temp'
        temp1 = MagicMock()
        temp1.name = 'temp1'
        temp1.get_value.return_value = 42
        k10temp.__iter__.return_value = [temp1]
        chips_detected = [k10temp, k10temp]

        chips = ['k10temp', 'it8718']
        features = ['temp1', 'temp1']

        temps = _get_temperatures(chips=chips,
                                  features=features,
                                  chips_detected=chips_detected)

        assert temps[0] == 42
        assert temps[1] is None

    def test_get_temperatures_chip_feature_missmatch(self):
        k10temp = MagicMock()
        k10temp.prefix = 'k10temp'
        temp1 = MagicMock()
        temp1.name = 'temp1'
        temp1.get_value.return_value = 42
        k10temp.__iter__.return_value = [temp1]
        chips_detected = [k10temp, k10temp]

        chips = ['k10temp', 'it8718', 'k10temp']
        features = ['temp1', 'temp2', 'temp2']

        temps = _get_temperatures(chips=chips,
                                  features=features,
                                  chips_detected=chips_detected)

        assert temps[0] == 42
        assert temps[1] is None
        assert temps[2] is None
