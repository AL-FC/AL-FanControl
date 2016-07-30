#! python
"""Hello."""

import sensors


def get_temps(chips, features):  # pragma: no cover
    """Get temperatures from lmsensors."""

    chips_detected = _get_detected_chips()

    temps = _get_temperatures(chips=chips,
                              features=features,
                              chips_detected=chips_detected)
    return temps


def _get_detected_chips():  # pragma: no cover
    sensors.cleanup()
    sensors.init()

    chips_detected = list(sensors.iter_detected_chips())

    return chips_detected


def _get_temperatures(chips, features, chips_detected):
    temps = [None] * max(len(chips), len(features))

    for chip in chips_detected:
        chip_prefix = to_str(chip.prefix)

        if chip_prefix not in chips:
            # this chip was not requested, so ignore
            continue

        for feature in chip:
            feature_name = to_str(feature.name)

            if feature_name not in features:
                # this feature was not requested, so ignore
                continue

            for start_index in range(len(features)):
                try:
                    index = _get_index(chips=chips, chip=chip,
                                       features=features,
                                       feature=feature,
                                       start_index=start_index)
                except (NoSuchChipError, NoSuchFeatureError,
                        ChipFeatureMismatchError):
                    continue

                # fill in list with temperature value
                temps[index] = feature.get_value()

    return temps


def _get_index(chips, chip, features, feature, start_index):
    feature_name = to_str(feature.name)
    chip_prefix = to_str(chip.prefix)

    try:
        chip_index = chips[start_index:].index(chip_prefix)
    except ValueError:
        raise NoSuchChipError(
            'The requested chip %s does not appear beyond this point: %s' %
            (chip_prefix, chips[start_index:]))

    try:
        feature_index = features[start_index:].index(feature_name)
    except ValueError:
        raise NoSuchFeatureError(
            'The requested feature %s does not appear beyond this point: %s' %
            (feature_name, features[start_index:]))

    if feature_index != chip_index:
        raise ChipFeatureMismatchError(
            'The sensor %s does not belong to the chip %s.' %
            (feature_name, chip_prefix))

    index = start_index + feature_index

    return index


class NoSuchChipError(BaseException):
    pass


class NoSuchFeatureError(BaseException):
    pass


class ChipFeatureMismatchError(BaseException):
    pass


def to_str(bytes_or_string):
    try:
        string = bytes_or_string.decode()
    except AttributeError:
        # prefix was str
        string = bytes_or_string

    return string
