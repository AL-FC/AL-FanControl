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
                    index = _get_index(features=features, feature=feature,
                                       chips=chips, chip=chip,
                                       start_index=start_index)
                except ValueError:
                    continue

                # fill in list with temperature value
                if temps[index] is not None:
                    print('alert')

                temps[index] = feature.get_value()

    sensors.cleanup()

    return temps


def _get_index(chips, chip, features, feature, start_index):
    try:
        feature_index = features[start_index:].index(feature.name)
    except ValueError:
        raise ValueError(
            'The requested feature does not appear beyond this point.')

    try:
        chip_index = chips[start_index:].index(chip.prefix)
    except ValueError:
        raise ValueError(
            'The requested chip does not appear beyond this point.')

    if feature_index != chip_index:
        raise ValueError('this sensor does not belong to this chip.')

    index = start_index + feature_index

    return index
