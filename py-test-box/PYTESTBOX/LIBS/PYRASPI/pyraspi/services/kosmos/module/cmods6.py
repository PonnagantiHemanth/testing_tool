#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.cmods6
:brief: Kosmos CMODS6 Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2021/11/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntFlag
from enum import unique

from pyraspi.services.kosmos.module.dac import Dac
from pyraspi.services.kosmos.module.module import ModuleBaseClass
from pyraspi.services.kosmos.module.module import ModuleSettings
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SWM
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SWM_WRITE_ARRAY_PART_1
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SWM_WRITE_ARRAY_PART_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_SWM_WRITE_JOB_DESCRIPTOR
from pyraspi.services.kosmos.protocol.generated.messages import swm_job_descriptor_t
from pyraspi.services.kosmos.protocol.generated.messages import swm_reg_map_msg_t
from pyraspi.services.kosmos.protocol.generated.messages import swm_reg_map_t
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class Cmods6(object):
    """
    Kosmos CMODS6 Module class (auxiliary FPGA dedicated to analog & power supply functions)
    """
    @unique
    class CHANNEL(IntFlag):
        """
        CHANNEL
        """
        BATTERY = 1
        USB = 2
    # end class CHANNEL

    ALL_CHANNELS = CHANNEL(CHANNEL.BATTERY | CHANNEL.USB)

    def __init__(self):
        self.job_desc = swm_job_descriptor_t()
        self.reg_map = swm_reg_map_t()
    # end def __init__

    def reset_all(self):
        """
        Reset both channel (Battery & USB):
         - DAC: reset Output Voltage, Current Sink & Source, Serie Resistance
         - Relays: disable output voltage connection
        """
        self.enable_output_voltage(channels=self.ALL_CHANNELS, enable=False)
        self.reset_dac(channels=self.ALL_CHANNELS)
    # end def reset_all

    def reset_dac(self, channels):
        """
        DAC: reset Output Voltage, Sink & Source Currents, Serie Resistance.

        :param channels: channel(s) to set
        :type channels: ``Cmods6.CHANNEL``
        """
        self.assert_channel_valid(channels)
        if self.CHANNEL.BATTERY in channels:
            self.reg_map.dac_vbat = Dac.cmd_reset()
            self.job_desc.bit.dac_v_bat_enable = 1
        # end if
        if self.CHANNEL.USB in channels:
            self.reg_map.dac_vusb = Dac.cmd_reset()
            self.job_desc.bit.dac_v_usb_enable = 1
        # end if
    # end def reset_dac

    def set_output_voltage(self, channels, voltage):
        """
        DAC: Set Output Voltage.

        :param channels: channel(s) to set
        :type channels: ``Cmods6.CHANNEL``
        :param voltage: Output Voltage to be set (Volt)
        :type voltage: ``float``
        """
        self.assert_channel_valid(channels)
        if self.CHANNEL.BATTERY in channels:
            self.reg_map.dac_vbat = Dac.cmd_set_output_voltage(voltage)
            self.job_desc.bit.dac_v_bat_enable = 1
        # end if
        if self.CHANNEL.USB in channels:
            self.reg_map.dac_vusb = Dac.cmd_set_output_voltage(voltage)
            self.job_desc.bit.dac_v_usb_enable = 1
        # end if
    # end def set_output_voltage

    def set_sink_current(self, channels, current):
        """
        DAC: Set Sink Current.

        :param channels: channel(s) to set
        :type channels: ``Cmods6.CHANNEL``
        :param current: Sink Current to be set (Ampere)
        :type current: ``float``
        """
        self.assert_channel_valid(channels)
        if self.CHANNEL.BATTERY in channels:
            self.reg_map.dac_vbat = Dac.cmd_set_sink_current(current)
            self.job_desc.bit.dac_v_bat_enable = 1
        # end if
        if self.CHANNEL.USB in channels:
            self.reg_map.dac_vusb = Dac.cmd_set_sink_current(current)
            self.job_desc.bit.dac_v_usb_enable = 1
        # end if
    # end def set_sink_current

    def set_source_current(self, channels, current):
        """
        DAC: Set Source Current.

        :param channels: channel(s) to set
        :type channels: ``Cmods6.CHANNEL``
        :param current: Source Current to be set (Ampere)
        :type current: ``float``
        """
        self.assert_channel_valid(channels)
        if self.CHANNEL.BATTERY in channels:
            self.reg_map.dac_vbat = Dac.cmd_set_source_current(current)
            self.job_desc.bit.dac_v_bat_enable = 1
        # end if
        if self.CHANNEL.USB in channels:
            self.reg_map.dac_vusb = Dac.cmd_set_source_current(current)
            self.job_desc.bit.dac_v_usb_enable = 1
        # end if
    # end def set_source_current

    def set_serie_resistance(self, channels, resistance):
        """
        DAC: Set Serie Resistance.

        :param channels: channel(s) to set
        :type channels: ``Cmods6.CHANNEL``
        :param resistance: Serie Resistance to be set (Ohm)
        :type resistance: ``float``
        """
        self.assert_channel_valid(channels)
        if self.CHANNEL.BATTERY in channels:
            self.reg_map.dac_vbat = Dac.cmd_set_serie_resistance(resistance)
            self.job_desc.bit.dac_v_bat_enable = 1
        # end if
        if self.CHANNEL.USB in channels:
            self.reg_map.dac_vusb = Dac.cmd_set_serie_resistance(resistance)
            self.job_desc.bit.dac_v_usb_enable = 1
        # end if
    # end def set_serie_resistance

    def enable_output_voltage(self, channels, enable):
        """
        RELAY: Enable/Disable Output Voltage connection to DUT

        :param channels: channel(s) to set
        :type channels: ``Cmods6.CHANNEL``
        :param enable: Enable or Disable connection
        :type enable: ``bool or int``
        """
        self.assert_channel_valid(channels)
        if self.CHANNEL.BATTERY in channels:
            self.reg_map.shifter_bat.bit.relay_1 = 1 if enable else 0
            self.job_desc.bit.shifter_bat_enable = 1
        # end if
        if self.CHANNEL.USB in channels:
            self.reg_map.shifter_usb.bit.relay_1 = 1 if enable else 0
            self.job_desc.bit.shifter_usb_enable = 1
        # end if
    # end def enable_output_voltage

    def enable_voltage_feedback(self, channels, enable):
        """
        RELAY: Enable/Disable Voltage Feedback connection from DUT

        :param channels: channel(s) to set
        :type channels: ``Cmods6.CHANNEL``
        :param enable: Enable or Disable connection
        :type enable: ``bool or int``
        """
        self.assert_channel_valid(channels)
        if self.CHANNEL.BATTERY in channels:
            self.reg_map.shifter_bat.bit.relay_2 = 1 if enable else 0
            self.job_desc.bit.shifter_bat_enable = 1
        # end if
        if self.CHANNEL.USB in channels:
            self.reg_map.shifter_usb.bit.relay_2 = 1 if enable else 0
            self.job_desc.bit.shifter_usb_enable = 1
        # end if
    # end def enable_voltage_feedback

    def enable_current_sink(self, enable):
        """
        RELAY: Enable/Disable Current Sink

        :param enable: Enable or Disable connection
        :type enable: ``bool or int``
        """
        self.reg_map.shifter_bat.bit.relay_3 = 1 if enable else 0
        self.job_desc.bit.shifter_bat_enable = 1
    # end def enable_current_sink

    def set_current_sink_channel(self, channel):
        """
        RELAY: Select which channel the Current Sink will be connected to.

        :param channel: channel to set, either BATTERY or USB.
        :type channel: ``Cmods6.CHANNEL``

        :raise ``AssertionError``: if channel value is not either BATTERY or USB.
        """
        assert channel in [self.CHANNEL.BATTERY, self.CHANNEL.USB], f'Invalid channel value {channel}.'
        self.reg_map.shifter_usb.bit.relay_3 = 1 if (channel is self.CHANNEL.BATTERY) else 0
        self.job_desc.bit.shifter_usb_enable = 1
    # end def set_current_sink_channel

    @classmethod
    def is_channel_valid(cls, channel):
        """
        Test if channel value is valid. Refer to ``Cmods6.CHANNEL` IntFlag enum.

        :param channel: channel to test
        :type channel: ``Cmods6.CHANNEL or int``

        :return: True if channel is valid, False otherwise.
        :rtype: ``bool``
        """
        return (not channel & ~cls.ALL_CHANNELS) and (channel & cls.ALL_CHANNELS)
    # end def is_channel_valid

    @classmethod
    def assert_channel_valid(cls, channel):
        """
        Assertion Test for channel value.

        :param channel: channel to test
        :type channel: ``Cmods6.CHANNEL or int``

        :raise ``AssertionError``: if channel value is not valid. Refer to ``Cmods6.CHANNEL` IntFlag enum.
        """
        assert cls.is_channel_valid(channel), f'Invalid channel value {channel}.'
    # end def assert_channel_valid

    def __str__(self):
        """
        Return human-readable string representation of Job descriptor and SWM registers.

        :return: string representation of Job descriptor and SWM registers.
        :rtype: ``str``
        """
        return self.swm_to_str(self.job_desc, self.reg_map)
    # end def __str__

    @staticmethod
    def swm_to_str(job_desc, reg_map):
        """
        Return human-readable string representation of Job descriptor and SWM registers.

        :param job_desc: SWM Job Description
        :type job_desc: ``swm_job_descriptor_t``
        :param reg_map: SWM Register Map
        :type reg_map: ``swm_reg_map_t``

        :return: string representation of Job descriptor and SWM registers.
        :rtype: ``str``
        """
        str_out = f'{"JOB DESC":12}: {job_desc.reg:#010x}\n'
        if job_desc.bit.dac_v_bat_enable:
            str_out += f'{"DAC VBAT":12}: {reg_map.dac_vbat.reg:#010x}\n'
        # end if
        if job_desc.bit.dac_v_usb_enable:
            str_out += f'{"DAC VUSB":12}: {reg_map.dac_vusb.reg:#010x}\n'
        # end if
        if job_desc.bit.shifter_usb_enable:
            str_out += f'{"SHIFTER USB":12}: {reg_map.shifter_usb.reg:#06x}\n'
        # end if
        if job_desc.bit.shifter_bat_enable:
            str_out += f'{"SHIFTER BAT":12}: {reg_map.shifter_bat.reg:#06x}\n'
        # end if
        if job_desc.bit.pga_adc_vbat_enable:
            str_out += f'{"PGA ADC VBAT":12}: {reg_map.pga_adc_vbat.reg[0]:#010x} {reg_map.pga_adc_vbat.reg[1]:#010x}\n'
        # end if
        if job_desc.bit.reserved_4_15:
            str_out += f'{"PGA ADC IBAT":12}: {reg_map.pga_adc_ibat.reg[0]:#010x} {reg_map.pga_adc_ibat.reg[1]:#010x}\n'
            str_out += f'{"PGA ADC VUSB":12}: {reg_map.pga_adc_vusb.reg[0]:#010x} {reg_map.pga_adc_vusb.reg[1]:#010x}\n'
            str_out += f'{"PGA ADC IUSB":12}: {reg_map.pga_adc_iusb.reg[0]:#010x} {reg_map.pga_adc_iusb.reg[1]:#010x}\n'
        # end if
        if job_desc.bit.reserved_20_29:
            str_out += f'{"RESERVED REG12":12} {reg_map.reg_12_reserved.reg:#010x}\n'
            str_out += f'{"RESERVED REG13":12} {reg_map.reg_13_reserved.reg:#010x}\n'
        # end if
        if job_desc.bit.bat_ntc_value_enable:
            str_out += f'{"NTC POT":12} {reg_map.ntc_pot.reg:#010x}\n'
        # end if
        return str_out
    # end def swm_to_str
# end class Cmods6


class Cmods6Manager(ModuleBaseClass):
    """
    Kosmos CMODS6 FPGA Manager class.
    Handle communication between Python and the Kosmos Hardware.
    """

    def __init__(self):
        module_settings = ModuleSettings(
            name=r'CMODS6',
            instance_id=None,  # Module is a singleton
            optional=False,
            msg_id=MSG_ID_SWM,
        )
        super().__init__(module_settings=module_settings)
        self._max_voltage_limit = {
            Cmods6.CHANNEL.BATTERY: Dac.MAX_VOLTAGE,  # Volts
            Cmods6.CHANNEL.USB: Dac.MAX_VOLTAGE,  # Volts
        }
    # end def __init__

    def send(self, cmods6):
        """
        Write to FPGA SWM registers then trigger the SWM communication.

        :param cmods6: Cmods6 data instance
        :type cmods6: ``Cmods6``
        """
        # Safety checks
        self.assert_safety_checks(cmods6.reg_map)

        # Convert type for array access convenience
        reg_map_msg = swm_reg_map_msg_t.from_buffer(cmods6.reg_map)

        # 1st frame: Register Map (part 1/2)
        tx_frames = []
        tx_frame = MessageFrame()
        tx_frame.frame.id = self.settings.msg_id
        tx_frame.frame.cmd = MSG_ID_SWM_WRITE_ARRAY_PART_1
        tx_frame.frame.payload.raw.dword = reg_map_msg.part.p1
        tx_frames.append(tx_frame)

        # 2nd frame: Register Map (part 2/2)
        tx_frame = MessageFrame()
        tx_frame.frame.id = self.settings.msg_id
        tx_frame.frame.cmd = MSG_ID_SWM_WRITE_ARRAY_PART_2
        tx_frame.frame.payload.raw.dword = reg_map_msg.part.p2
        tx_frames.append(tx_frame)

        # 3rd frame: Job Descriptor
        tx_frame = MessageFrame()
        tx_frame.frame.id = self.settings.msg_id
        tx_frame.frame.cmd = MSG_ID_SWM_WRITE_JOB_DESCRIPTOR
        tx_frame.frame.payload.swm_reg.job_descriptor = cmods6.job_desc
        tx_frames.append(tx_frame)

        # Send datagram and get reply
        txrx_frames = self.dt.fpga_transport.send_control_message_list(tx_frames)

        # Check result
        self.dt.fpga_transport.check_status_message_replies(txrx_frames)
    # end def send

    def read(self):
        """
        Read FPGA SWM registers.
        """
        raise NotImplementedError("Reading from CMODS6 is not implemented in hardware yet")
    # end def read

    def set_max_voltage_limit(self, channels, voltage):
        """
        Set DAC output voltage maximum limit.

        :param channels: channel(s) to set
        :type channels: ``Cmods6.CHANNEL``
        :param voltage: voltage limit, in Volts
        :type voltage: ``float``

        :raise ``AssertionError``: if one of the following conditions is met:
                                    - Limit voltage is out-of-range
                                    - Unknown channel value
        """
        assert 0 <= voltage <= Dac.MAX_VOLTAGE, \
            f'Voltage is out-of-range: {voltage} not in [0, {Dac.MAX_VOLTAGE}]'

        assert Cmods6.CHANNEL.BATTERY in channels or Cmods6.CHANNEL.USB in channels, \
            f'Unknown channel {channels}.'

        if Cmods6.CHANNEL.BATTERY in channels:
            self._max_voltage_limit[Cmods6.CHANNEL.BATTERY] = voltage
        # end if
        if Cmods6.CHANNEL.USB in channels:
            self._max_voltage_limit[Cmods6.CHANNEL.USB] = voltage
        # end if
    # end def set_max_voltage_limit

    def get_max_voltage_limit(self, channel):
        """
        Get DAC output voltage maximum limit.

        :param channel: channel to read
        :type channel: ``Cmods6.CHANNEL``

        :return: DAC output voltage maximum limit of selected channel
        :rtype: ``float``
        """
        return self._max_voltage_limit[channel]
    # end def get_max_voltage_limit

    def safety_checks(self, reg_map):
        """
        Check that:
         - Battery DAC output voltage is below set limit.
         - USB DAC output voltage of is below set limit.

        :param reg_map: RegisterMap instance
        :type reg_map: ``swm_reg_map_t``

        :return: Empty list if all safety checks are passing; List of error strings if:
                  - Battery DAC output voltage module is above set limit
                  - USB DAC output voltage module is above set limit
        :rtype: ``list[str]``
        """
        error_list = []

        # Check Battery DAC output voltage limit
        address = reg_map.dac_vbat.bit.address
        command = reg_map.dac_vbat.bit.command
        voltage_target = Dac.dac_value_to_volt(reg_map.dac_vbat.bit.data)
        voltage_limit = self._max_voltage_limit[Cmods6.CHANNEL.BATTERY]
        if address in [Dac.CHANNEL.A, Dac.CHANNEL.ALL] and \
                Dac.COMMAND.WRITE_INPUT_REG_N <= command <= Dac.COMMAND.WRITE_INPUT_REG_N_AND_UPDATE_N and \
                voltage_target > voltage_limit:
            error_list.append(f'Battery DAC output voltage ({voltage_target:.3f} Volts) '
                              f'is set above limit ({voltage_limit} Volts).')
        # end if

        # Check USB DAC output voltage limit
        address = reg_map.dac_vusb.bit.address
        command = reg_map.dac_vusb.bit.command
        voltage_target = Dac.dac_value_to_volt(reg_map.dac_vusb.bit.data)
        voltage_limit = self._max_voltage_limit[Cmods6.CHANNEL.USB]
        if address in [Dac.CHANNEL.A, Dac.CHANNEL.ALL] and \
                Dac.COMMAND.WRITE_INPUT_REG_N <= command <= Dac.COMMAND.WRITE_INPUT_REG_N_AND_UPDATE_N and \
                voltage_target > voltage_limit:
            error_list.append(f'USB DAC output voltage ({voltage_target:.3f} Volts) '
                              f'is set above limit ({voltage_limit} Volts).')
        # end if

        return error_list
    # end def safety_checks

    def assert_safety_checks(self, reg_map):
        """
        Assertion test wrapper for ``safety_checks()`` method.

        :param reg_map: RegisterMap instance
        :type reg_map: ``swm_reg_map_t``

        :raise ``AssertionError``: CMODS6 safety checks failed, refer to ``safety_checks()`` method.
        """
        error_list = self.safety_checks(reg_map)
        assert not error_list, 'CMODS6 safety checks failed:\n' + '\n'.join(error_list)
    # end def assert_safety_checks
# end class Cmods6Manager

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
