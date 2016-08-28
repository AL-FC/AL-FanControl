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
    fans = [GPU, None, None, None, Case, Case, CPU, Case]
    chips = [radeon, None, None, None, it8718, it8718, k10temp, it8718]
    features = [temp1, None, None, None, temp1, temp2, temp1, temp3]
    ambients = [25, None, None, None, 25, 25, 15, 25]
    limits = [90, None, None, None, 80, 80, 70, 80]
