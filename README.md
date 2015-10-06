# FanControl

An application-level fan control for desktop PCs using Python, Arduino and PWM fans.

## Rationale

PC cooling has always been an area of constant change.
In the past,
    ever more power hungry CPUs have lead to
    sophisticated cooling techology.
In combination with more efficient CPUs
    this has enabled smaller and quieter cooling,
    in recent years.
Yet,
    desktop PCs continue to be
    loud at idle and hot under load.
This is an attempt
    at reinventing fan control.
I hope to provoke
    a change in the way we control our fans
    that I feel is long overdue.

Plugging PWM fans into motherboards is a gamble,
    because many built-in fan control do not work properly.
Often PC users are are plagued by
    unnecessary fan noise at idle,
    nervously accelerating fans under short-time load and
    high temperatures at precious hardware.
When swapping
    motherboards, fans or operating systems,
    a previously well-working setup cam misbehave.
Fan controls can be much better and reliable.

FanControl is a hardware platform
    for building better fan controls.
It works around
    the often false abstraction
        of the motherboard
    and replaces it with a sane lower-level layer.
Upon this standardised lower-level operation,
    FanControl provides applications easy access to PWM fans.

This repository contains
    a complete chain of open-sourced parts
    necessary to upgrade
        a common desktop PC
        with a software-defined fan control.
These are
    an schematic
        for the neccessary electronics,
    Arduino code
        for the controller-side
    Python code
        for the host-side.

The electronic plans
    comprise
        a breadboard layout,
        electronic schematic and
        platine layout.
They are provided
        in the Fitzing format
    and
        can be be fabricated even at small volumes.

The electronic are based on an
    Atmel 32u4, which
        has hardware USB support
        and
        is fast enough to do PWM in software.
It handles
    the immediate pwm control
        and
    the fan speed sensing.

The Python code
    is structured in layers
        that can be easily replaced by alternative implementaions.
The application level code
    is free of cruft
        and
    can be extended with custom functionality.
Thermal limits and fan caracteristics
    can be defined
    via configuration files.

## Features

-   reusable
    -   Open Source
    -   Open Hardware
-   reproducable
    -   fully documented
    -   fabricatable via Fritzing
-   compact
    -   requires no 3.5"/5.25" bay
    -   fits in a small space inside the case
-   cheap
    -   < 30 € for 1 unit
-   compatible
    -   uses common USB
-   simple protocol
    -   one message to the controller follows one message to the host
-   universal
    -   up to 8 channels for complex PCs

## Design

-   stand-alone hardware that can safely operate during boot/shutdown
-   small Arduino code that only does what it needs to
-   simple protocol that can be easily implemented on the host
-   virtually direct access to PWM from the application level
-   application logic written in Python for easy reimplmentation

## Dependencies

-   1 free USB port
-   1 free 12 V connector
-   PWM fans
-   Linux
-   Python
-   lm-sensors

## Bill of Materials

-    6 € Arduino-clone
-   10 € board (or a breadboard and good soldering skills)
-   14 € small electronic components
