#! python
"""Hello."""

import sensors


def get_temps(chips, features):
    """Get temperatures from lmsensors."""
    temps = [None] * max(len(chips), len(features))

    sensors.init()

    for chip in sensors.iter_detected_chips():
        if chip.prefix not in chips:
            continue

        for feature in chip:
            if feature.name not in features:
                continue

            # determine index of the temperature
            index = None
            for start_index in range(len(features)):
                feature_index = features[start_index:].index(feature.name)
                chip_index = chips[start_index:].index(chip.prefix)
                if feature_index == chip_index:
                    index = start_index + feature_index
                    break

            temps[index] = feature.get_value()

    sensors.cleanup()

    return temps
