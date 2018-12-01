=======
LzScope
=======

:Author:
   Evgeny P. Kurbatov
:Contact:
   evgeny.p.kurbatov at gmail dot com

:Version: 1.0.0


Git repository: https://bitbucket.org/evgenykurbatov/lzscope



Boards
======


- Amperka Iskra JS

  `General info <http://amperka.ru/product/iskra-js>`_ and `specs <http://wiki.amperka.ru/js:iskra_js>`_ (in Russian).

  Some characteristics:

  - MCU: STM32F405RG 168MHz (32bit ARM cortex M4)
  - Flash-ROM 1MiB, flash-RAM 256KiB, SRAM 192KiB
  - External power: 7-15V (or 3.6-12V if 5V is not needed)
  - Max current: 1000mA for 5V bus, 300mA for 3.3V bus
  - Ports: 26x GPIO, 22x PWM, 3x 12 bit ADC (12 channels), 2x 12 bit DAC
  - Hardware interfaces: 2x SPI, 3x I2C/TWI, 4x UART/Serial, USB FS



Communication protocol
======================


Command list
------------

- ``ADC1`` | ``ADC2``

  Reads a single value from ADC1 or ADC2.

  Returns two-byte integer.

- ``ADC1DMA <frame_length>`` |  ``ADC2DMA <frame_length>``

  Starts reading a sequence of values from ADC1 or ADC2. Every ``frame_length`` values can be read by the host with the '``GET``' command (see below). The reading should be performed before next ``frame_length`` measurements are done.

- ``GET``

  This is a subcommand of ``ADC<n>DMA`` context.

  Returns ``frame_length`` two-byte integers.

- ``RESET``

  This is a subcommand of ``ADC<n>DMA`` context.

  In ``ADC<n>DMA`` context it stops ADC reading sequence. Otherwise does nothing.

  Returns '``OK``'.

- Unknown command.

  Does nothing.


Examples
--------

#. Single ADC conversion.

  ::

    > RESET
    < OK
    > ADC1
    < nn

#. Sequence of ADC conversions.

  ::

    > RESET
    < OK
    > ADC1DMA 8
    > GET
    < nn nn nn nn nn nn nn nn
    > GET
    < nn nn nn nn nn nn nn nn
    ...
    > RESET
    < OK
