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
        if chip.prefix not in chips:
            # this chip was not requested, so ignore
            continue

        for feature in chip:
            if feature.name not in features:
                # this feature was not requested, so ignore
                continue

            for start_index in range(len(features)):
                try:
                    index = _get_index(chips=chips, chip=chip,
                                       features=features, feature=feature,
                                       start_index=start_index)
                except (NoSuchChipError, NoSuchFeatureError,
                        ChipFeatureMismatchError):
                    continue

                # fill in list with temperature value
                temps[index] = feature.get_value()

    return temps


def _get_index(chips, chip, features, feature, start_index):
    try:
        chip_index = chips[start_index:].index(chip.prefix)
    except ValueError:
        raise NoSuchChipError(
            'The requested chip %s does not appear beyond this point: %s' %
            (chip.prefix, chips[start_index:]))

    try:
        feature_index = features[start_index:].index(feature.name)
    except ValueError:
        raise NoSuchFeatureError(
            'The requested feature %s does not appear beyond this point: %s' %
            (feature.name, features[start_index:]))

    if feature_index != chip_index:
        raise ChipFeatureMismatchError(
            'The sensor %s does not belong to the chip %s.' %
            (feature.name, chip.prefix))

    index = start_index + feature_index

    return index


class NoSuchChipError(BaseException):
    pass


class NoSuchFeatureError(BaseException):
    pass


class ChipFeatureMismatchError(BaseException):
    pass
