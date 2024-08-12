#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.dac_sel
:brief: Kosmos DAC Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/11/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from enum import unique

from pyraspi.services.kosmos.protocol.generated.messages import swm_dac_t


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Dac(object):
    """
    Kosmos DAC Module class
    """
    # LTC2654-H DAC
    DAC_RESOLUTION = 16  # bits
    DAC_MAX_VALUE = (1 << DAC_RESOLUTION) - 1

    # The LTC2654-H DAC has a 2.048V reference that provides a full-scale output of 4.096V
    DAC_OUTPUT_FULL_SCALE = 2.048 * 2  # Volts

    # The external op-amp LT1970 has a 2x gain
    OUTPUT_OPAMP_GAIN = 2

    # Maximum voltage
    MAX_VOLTAGE = OUTPUT_OPAMP_GAIN * DAC_OUTPUT_FULL_SCALE * DAC_MAX_VALUE / (1 << DAC_RESOLUTION)  # Volts

    @unique
    class COMMAND(IntEnum):
        """
        DAC Command that can be executed by the DAC chip itself.
        Refer to LTC2654-H DAC datasheet.
        """
        WRITE_INPUT_REG_N = 0
        UPDATE_INPUT_REG_N = 1
        WRITE_INPUT_REG_N_AND_UPDATE_ALL = 2
        WRITE_INPUT_REG_N_AND_UPDATE_N = 3
        POWER_DOWN_N = 4
        POWER_DOWN_CHIP = 5
        SELECT_INTERNAL_REF = 6
        SELECT_EXTERNAL_REF = 7
        NOP = 0xF  # No Operation
    # end class COMMAND

    @unique
    class CHANNEL(IntEnum):
        """
        DAC channel that can be selected.
        Refer to LTC2654-H DAC datasheet.
        """
        A = 0  # DAC Channel A
        B = 1  # DAC Channel B
        C = 2  # DAC Channel C
        D = 3  # DAC Channel D
        ALL = 0xF  # All DAC channels
    # end class CHANNEL

    @staticmethod
    def volt_to_dac_value(volt):
        """
        Convert Volts to DAC binary representation.

        DAC_VOLT = Gain * Vref * DAC_VALUE / 2^n
                   where DAC_VALUE is the number from 0 to 2^n-1 with n = 16 bits
                   and Vref = 4 * 1.024 V and output Gain is 2x.

        DAC_VOLT = DAC_VALUE * 8.192 / 65536
        DAC_VALUE = DAC_VOLT * 65536 / 8.192

        The maximum DAC_VALUE of 65535 gives the DAC_VOLT = 8.191875 V
        For example, to get 1.000V, it's necessary to set DAC_VALUE = int(65536 * DAC_VOLT / 8.192 V)
                                                                    = int(65536 * 1.0V / 8.192V) = 8000d = 0x1F40

        :param volt: DAC output voltage
        :type volt: ``int or float``

        :return: DAC input binary representation
        :rtype: ``int``

        :raise ``ValueError``: If input is out-of-range. Valid range is [0, 8.191875] Volts.
        """
        if not 0 <= volt <= Dac.MAX_VOLTAGE:
            raise ValueError(f'Voltage is out-of-range: {volt}. '
                             f'Valid range is [0, {Dac.MAX_VOLTAGE}] Volts.')
        # end if

        v_dac = volt / Dac.OUTPUT_OPAMP_GAIN
        return round(v_dac * (1 << Dac.DAC_RESOLUTION) / Dac.DAC_OUTPUT_FULL_SCALE)

    # end def volt_to_dac_value

    @staticmethod
    def dac_value_to_volt(dac_value):
        """
        Convert Volts to DAC binary representation.

        DAC_VOLT = Gain * Vref * DAC_VALUE / 2^n
                   where DAC_VALUE is the number from 0 to 2^n-1 with n = 16 bits
                   and Vref = 4 * 2 * 1.024 V = 8.192 V.

        DAC_VOLT = DAC_VALUE * 8.192 / 65536
        DAC_VALUE = DAC_VOLT * 65536 / 8.192

        The maximum DAC_VALUE of 65535 gives the DAC_VOLT = 8.191875 V
        For example, to get 1.000V, it's necessary to set DAC_VALUE = int(65536 * DAC_VOLT / 8.192 V)
                                                                    = int(65536 * 1.0V / 8.192V) = 8000d = 0x1F40

        :param dac_value: DAC input value. Value must be integer when using float type.
        :type dac_value: ``int or float``

        :return: DAC output voltage
        :rtype: ``float``

        :raise ``TypeError``: If input is not an integer value.
        :raise ``ValueError``: If input is out-of-range. Valid range is [0, 0xFFFF].
        """
        if not (isinstance(dac_value, int) or (isinstance(dac_value, float) and dac_value.is_integer())):
            raise TypeError(f'DAC value must be an integer: type is {type(dac_value).__name__}, value is {dac_value}.')
        # end if

        if not 0 <= dac_value <= Dac.DAC_MAX_VALUE:
            raise ValueError(f'DAC value is out-of-range: {dac_value}. '
                             f'Valid range is [0, {Dac.DAC_MAX_VALUE:#06x}].')
        # end if

        v_dac = Dac.DAC_OUTPUT_FULL_SCALE * dac_value / (1 << Dac.DAC_RESOLUTION)
        return v_dac * Dac.OUTPUT_OPAMP_GAIN
    # end def dac_value_to_volt

    @staticmethod
    def get_dac_cmd(command=COMMAND.WRITE_INPUT_REG_N_AND_UPDATE_ALL, address=None, data=0):
        """
        Get DAC command (generic).

        :param command: DAC command to be executed by the DAC chip itself,
                        defaults to `COMMAND.WRITE_INPUT_REG_N_AND_UPDATE_ALL` - OPTIONAL
        :type command: ``Dac.COMMAND``
        :param address: DAC channel address, defaults to None - OPTIONAL
        :type address: ``Dac.CHANNEL``
        :param data: DAC data, defaults to 0 - OPTIONAL
        :type data: ``int or ctypes.c_uint16``

        :return: DAC register value
        :rtype: ``swm_dac_t``

        :raise ``AssertionError``: Invalid argument type
        """
        assert command in Dac.COMMAND
        assert address in Dac.CHANNEL
        dac_cmd = swm_dac_t()
        dac_cmd.bit.command = command
        dac_cmd.bit.address = address
        dac_cmd.bit.data = data
        return dac_cmd
    # end def get_dac_cmd

    @staticmethod
    def cmd_reset():
        """
        Get DAC command for resetting all the DAC channels

        :return: DAC register value
        :rtype: ``swm_dac_t``
        """
        return Dac.get_dac_cmd(address=Dac.CHANNEL.ALL)
    # end def cmd_reset

    @staticmethod
    def cmd_set_output_voltage(voltage):
        """
        Get DAC command for setting Output Voltage.

        :param voltage: Output Voltage to be set (Volt)
        :type voltage: ``float``

        :return: DAC register value
        :rtype: ``swm_dac_t``
        """
        return Dac.get_dac_cmd(address=Dac.CHANNEL.A, data=Dac.volt_to_dac_value(voltage))
    # end def cmd_set_output_voltage

    @staticmethod
    def cmd_set_sink_current(sink_current):
        """
        Get DAC command for setting Sink Current.

        :param sink_current: Sink Current to be set (Ampere)
        :type sink_current: ``float``

        :return: DAC register value
        :rtype: ``swm_dac_t``
        """
        dac_voltage = sink_current * 1  # FIXME: find coef
        return Dac.get_dac_cmd(address=Dac.CHANNEL.B, data=Dac.volt_to_dac_value(dac_voltage))
    # end def cmd_set_sink_current

    @staticmethod
    def cmd_set_source_current(source_current):
        """
        Get DAC command for setting Source Current.

        :param source_current: Source Current to be set (Ampere)
        :type source_current: ``float``

        :return: DAC register value
        :rtype: ``swm_dac_t``
        """
        dac_voltage = source_current * 1  # FIXME: find coef
        return Dac.get_dac_cmd(address=Dac.CHANNEL.C, data=Dac.volt_to_dac_value(dac_voltage))
    # end def cmd_set_source_current

    @staticmethod
    def cmd_set_serie_resistance(serie_resistance):
        """
        Get DAC command for setting Serie Resistance.

        :param serie_resistance: Serie Resistance to be set (Ohm)
        :type serie_resistance: ``float``

        :return: DAC register value
        :rtype: ``swm_dac_t``
        """
        dac_voltage = serie_resistance * 1  # FIXME: find coef
        return Dac.get_dac_cmd(address=Dac.CHANNEL.D, data=Dac.volt_to_dac_value(dac_voltage))
    # end def cmd_set_serie_resistance
# end class Dac

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
