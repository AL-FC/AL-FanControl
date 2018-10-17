from __future__ import (absolute_import, division, print_function,
                        unicode_literals)


class Configuration(object):

    # aliases for better readibility
    CPU = 'CPU'
    GPU = 'GPU'
    Case = 'Case'
    k10temp = 'k10temp'
    radeon = 'radeon'
    it8718 = 'it8718'
    temp1 = 'temp1'
    temp2 = 'temp2'
    temp3 = 'temp3'

    # ToDo: Read this from a config file
    ports = [0, 1, 2, 3, 4, 5, 6, 7]
    fans = [CPU, CPU, CPU, GPU, Case, Case, Case, GPU]
    chips = [k10temp, k10temp, k10temp, radeon, it8718, it8718, it8718, radeon]
    features = [temp1, temp1, temp1, temp1, temp3, temp3, temp3, temp1]
    ambients = [0, 0, 0, 25, 25, 25, 25, 25]
    limits = [55, 55, 55, 90, 75, 75, 75, 90]
