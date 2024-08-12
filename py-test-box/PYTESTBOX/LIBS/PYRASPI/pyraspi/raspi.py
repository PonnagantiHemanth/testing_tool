#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.raspi
:brief: Raspi Control Class
:author: Fred Chen <fchen7@logitech.com>
:date: 2019/10/21
"""
# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from io import open
from uuid import getnode
from platform import node

from kosmos_daemon.public.hardware import Hardware


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
# Pretty-print error message to be printed when the host is not a RaspberryPi configured for Kosmos.
# In order to quicken debugging, this also prints the hostname and MAC address of the actual host platform.
UNSUPPORTED_SETUP_ERR_MSG = f'Support test on Raspberry Pi configured for KOSMOS project only!\n' \
                            f'Note: current host is hostname={node()}, MAC={getnode():#010x}.'

PI_4_MODEL = 'raspberry pi 4 model b'
PI_5_MODEL = 'raspberry pi 5 model b'


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
def is_kosmos_setup():
    """
    Test if the raspberry PI4 node has been deployed with a Kosmos.

    :return: ``True`` if the setup type provided by the Kosmos daemon API is Kosmos v2, ``False`` otherwise
    :rtype: ``bool``
    """
    kosmos_hardware = Hardware()
    return kosmos_hardware.is_kosmos_v2
# end def is_kosmos_setup


class Raspi(object):
    """
    Raspi service provider
    """
    _is_host_raspberry_pi = None
    _is_host_kosmos = None

    @staticmethod
    def is_host_raspberry_pi():
        """
        Test if the host running this script is a Raspberry Pi (i.e. 4 or 5 models).

        :return: ``True`` if the host is a Raspberry Pi, ``False`` otherwise
        :rtype: ``bool``
        """
        # Returned cached value if present
        if Raspi._is_host_raspberry_pi is not None:
            return Raspi._is_host_raspberry_pi
        # end if
        Raspi._is_host_raspberry_pi = Raspi.is_raspberry_pi(pi4=True, pi5=True)

        return Raspi._is_host_raspberry_pi
    # end def is_host_raspberry_pi

    @staticmethod
    def is_raspberry_pi(pi4=True, pi5=False):
        """
        Test if the host running this script is a Raspberry Pi 4 model, a Raspberry Pi 5 model or one of the two.

        :param pi4: If True, return True if the hardware is a Raspberry Pi model 4B, defaults to True - OPTIONAL
        :type pi4: ``bool``
        :param pi5: If True, return True if the hardware is a Raspberry Pi model 5, defaults to False - OPTIONAL
        :type pi5: ``bool``

        :return: ``True`` if the host is a Raspberry Pi matching the given models, ``False`` otherwise
        :rtype: ``bool``

        :raise ``AssertionError``: At least one model shall be enabled: `rpi4` or `rpi5`
        """
        assert pi4 | pi5, 'At least one model shall be enabled'

        # Check RaspberryPi's model string
        model_list = [PI_4_MODEL] if not pi5 else [PI_5_MODEL] if not pi4 else [PI_4_MODEL, PI_5_MODEL]
        try:
            with open('/sys/firmware/devicetree/base/model', 'r') as m:
                text = m.read().lower()
                return any([x in text for x in model_list])
            # end with
        except FileNotFoundError:
            return False
        # end try
    # end def is_raspberry_pi

    @staticmethod
    def is_raspberry_pi_5():
        """
        Test if the host running this script is a Raspberry Pi 5 model B.

        :return: ``True`` if the host is a Raspberry Pi 5 model B, ``False`` otherwise
        :rtype: ``bool``
        """
        return Raspi.is_raspberry_pi(pi4=False, pi5=True)
    # end def is_raspberry_pi_5

    class PIN:
        """
        Pin allocation

        Note: Pin numbering use GPIO.BOARD notation (Raspberry Pi header numbers),
        not GPIO.BCM notation (Broadcom GPIO 00..nn numbers)
        """
        if is_kosmos_setup():
            # Kosmos Motherboard v2
            STATUS_LED_1 = 38

            # Saturn FPGA
            GLOBAL_GO = 33  # Schematics signal name is "AUX_0"
            GLOBAL_ERROR = 8  # Schematics signal name is "AUX_1"
            AUX_2 = 10
            AUX_3 = 22
            AUX_4 = 16
            AUX_5 = 15
            AUX_6 = 37
            AUX_7 = 32
            AUX_8 = 13  # Schematics signals name is "AUXX"

            # CMODS6 FPGA
            CMOD_0 = 11
            CMOD_1 = 12
            CMOD_2 = 35

            # Misc
            JLINK_IO_SWITCH = None
        else:
            # Power board
            JLINK_IO_SWITCH = 13
            RECHARGEABLE = 15
            VOLTAGE_OUTPUT = 16
            OVER_VOLTAGE_ALERT = 18
            OVER_CURRENT_ALERT = 37

            # C&P Mouse Basic Button Emulator
            LEFT_BUTTON = 11
            RIGHT_BUTTON = 12
            MIDDLE_BUTTON = 29
            BACK = 23
            FORWARD = 24
            EASY_SWITCH_BUTTON = 22
            DPI_CYCLING_BUTTON = 21
            DPI_UP_BUTTON = 31
            DPI_DOWN_BUTTON = 32
            DPI_SHIFT_BUTTON = 33
            CYCLE_THROUGH_ONBOARD_PROFILE = 35
            EMOJI_PANEL = 36
            SMART_SHIFT = 38

            # Gaming mouse
            # Connect mouse button index to the corresponding raspi button index.
            # Ex: The button index of DPI Cycling button is 6 on Garnet. So, shall connect the button to Button_6 = 22,
            #     not connect it the DPI_CYCLING_BUTTON = 21
            BUTTON_1 = 11  # Default function: Left button
            BUTTON_2 = 12  # Default function: Right button
            BUTTON_3 = 29  # Default function: Middle button
            BUTTON_4 = 23  # Default function: Back button
            BUTTON_5 = 24  # Default function: Forward button
            BUTTON_6 = 22
            BUTTON_7 = 21
            BUTTON_8 = 31
            BUTTON_9 = 32
            BUTTON_10 = 33
            BUTTON_11 = 35
            BUTTON_12 = 36
            BUTTON_13 = 38
            BUTTON_14 = 7
            BUTTON_15 = 8
            BUTTON_16 = 10

            # Keyboard Emulator: MT8816 Analog Switch Array
            # 1. Share with mouse GPIOs (11, 12, 22, 29)
            # 2. Occupied GPIOs from SPI0 and SPI1
            # 3. Share with power board GPIO 37
            MT8816_CS_0 = 7
            MT8816_CS_1 = 8
            MT8816_CS_2 = 38
            MT8816_RESET = 10
            MT8816_STROBE = 11
            MT8816_DATA_0 = 12
            MT8816_DATA_1 = 22
            MT8816_DATA_2 = 40
            MT8816_AX_0 = 26
            MT8816_AX_1 = 29
            MT8816_AX_2 = 31
            MT8816_AX_3 = 33
            MT8816_AY_0 = 35
            MT8816_AY_1 = 36
            MT8816_AY_2 = 37

            # Game Mode Slider Emulator
            GAME_MODE_SLIDER = 32
        # end if
    # end class PIN

    if not is_kosmos_setup():
        PRESET_GPIO_LIST = [PIN.BUTTON_1, PIN.BUTTON_2, PIN.BUTTON_3, PIN.BUTTON_4, PIN.BUTTON_5, PIN.BUTTON_6,
                            PIN.BUTTON_7, PIN.BUTTON_8, PIN.BUTTON_9, PIN.BUTTON_10, PIN.BUTTON_11, PIN.BUTTON_12,
                            PIN.BUTTON_13, PIN.BUTTON_14, PIN.BUTTON_15, PIN.BUTTON_16]
    # end if

# end class Raspi

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
