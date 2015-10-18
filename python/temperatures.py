#! python
"""Hello."""

import time

import sensors

TEMP_TYPE = 2
CPU_PREFIX = 'k10temp'


def get_cpu_temp():
    """Get the temperature of the cpu."""
    sensors.init()
    try:
        for chip in sensors.iter_detected_chips():
            if chip.prefix != CPU_PREFIX:
                continue

            # print '%s at %s' % (chip, chip.adapter_name)
            # print(chip.adapter_name, chip.addr, chip.bus, chip.has_wildcards,
            #       chip.path, chip.prefix)

            for feature in chip:
                if feature.type != TEMP_TYPE:
                    continue
                # print '  %s: %.2f' % (feature.label, feature.get_value())
                return feature.get_value()
    finally:
        sensors.cleanup()


def get_temps():
    cpu = get_cpu_temp()
    return [cpu] + [0] * 7


if __name__ == '__main__':
    while True:
        temp = get_cpu_temp()
        print(temp)
        time.sleep(1)
