#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.adda
:brief: Kosmos ADDA (PODS ADC & DAC) Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/05/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyraspi.services.kosmos.module.module import ModuleBaseClass
from pyraspi.services.kosmos.module.module import ModuleSettings
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_ALL
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_OUTPUT_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_0
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_1
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_2
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_ADDA
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_ADDA_ADC_READ
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_ADDA_DAC_WRITE
from pyraspi.services.kosmos.protocol.generated.messages import adda_sel_e__enumvalues
from pyraspi.services.kosmos.protocol.python.messageframe import MessageFrame


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AddaModule(ModuleBaseClass):
    """
    Kosmos ADDA (PODS ADC & DAC) module class.
    """

    def __init__(self):
        module_settings = ModuleSettings(
            name=r'PODS ADDA',
            instance_id=None,  # Module is a singleton
            optional=False,
            msg_id=MSG_ID_ADDA
        )
        super().__init__(module_settings=module_settings)
    # end def __init__

    def _read_adc(self):
        """
        Get PODS ADC raw measurements from remote.

        :return: PODS ADC multi-channel measurements (raw)
        :rtype: ``adda_adc_msg_t``
        """
        # Send request and get reply
        return self.dt.fpga_transport.send_control_message(msg_id=self.settings.msg_id,
                                                           msg_cmd=MSG_ID_ADDA_ADC_READ).adc
    # end def _read_adc

    def read_adc(self):
        """
        Return PODS ADC measurement from remote, expressed in Volts.

        :return: PODS ADC multi-channel measurements in Volts
        :rtype: ``list[float]``
        """
        raw = self._read_adc()
        return list(map(self.convert_adc_data_to_volt, raw))
    # end def read_adc

    def _write_dac(self, data, dac_sel, channels):
        """
        Send PODS DAC raw codes to remote.

        If channel is `ADDA_DAC_CH_ALL`, then only one `data` value need to be passed.
        Otherwise, `data` must be an array of length equal to the number of DAC channel selected.

        :param data: array of raw value per DAC channel, or one value for all channels
        :type data: ``list[int] or int``
        :param dac_sel: DAC selection (DAC 0, 1 or 2), refer to `adda_sel_e__enumvalues`
        :type dac_sel: ``adda_sel_e or int``
        :param channels: DAC channel selection (bitfield), refer to `adda_dac_channels_e__enumvalues`
        :type channels: ``adda_dac_channels_e or int``

        :raise ``AssertionError``: if an input parameter is invalid
        """
        if not isinstance(data, list):
            data = [data]
        # end if

        # Sanity check
        assert ADDA_DAC_CH_ALL <= channels <= ((1 << ADDA_DAC_OUTPUT_COUNT) - 1), \
            f'DAC channels field is out-of-range: {channels:#04x}.'
        if channels == ADDA_DAC_CH_ALL:
            assert len(data) == 1, \
                'When all DAC channels are selected together, only one common data entry can be passed in parameter.'
        else:
            assert len(data) == bin(channels).count('1'), \
                'The number of set bits in DAC channels field does not match the number of data entries.'
        # end if
        for k, v in enumerate(data):
            assert isinstance(v, int), f'DAC data[{k}] must be an integer, got {type(v)}.'
            assert 0 <= v <= 0xFFFF, f'DAC data[{k}] is out-of-range: {v:#06x}.'
        # end for
        assert dac_sel in [ADDA_SEL_DAC_0, ADDA_SEL_DAC_1, ADDA_SEL_DAC_2], f' DAC selection is invalid: {dac_sel}.'

        # Create request
        tx_frame = MessageFrame()
        tx_frame.frame.id = self.settings.msg_id
        tx_frame.frame.cmd = MSG_ID_ADDA_DAC_WRITE
        tx_frame.frame.payload.adda_dac.dac_sel = dac_sel
        tx_frame.frame.payload.adda_dac.channels = channels
        if channels == ADDA_DAC_CH_ALL:
            tx_frame.frame.payload.adda_dac.values[0] = data[0]
        else:
            data_it = iter(data)
            for idx in range(ADDA_DAC_OUTPUT_COUNT):
                if channels & (1 << idx):
                    tx_frame.frame.payload.adda_dac.values[idx] = next(data_it)
                # end if
            # end for
        # end if

        # Send request and get reply
        txrx_frames = self.dt.fpga_transport.send_control_message_list([tx_frame])

        # TODO: check reply status
    # end def _write_dac

    def write_dac(self, volts, dac_sel, channels=ADDA_DAC_CH_ALL):
        """
        Set PODS DAC output voltages, per channels.

        If channel is `ADDA_DAC_CH_ALL`, then only one `volts` value need to be passed.
        Otherwise, `volts` must be an array of length equal to the number of DAC channel selected.

        :param volts: array of voltage values per DAC channel, or one value for all channels
        :type volts: ``list[float] or float``
        :param dac_sel: DAC selection (DAC 0, 1 or 2), refer to `adda_sel_e__enumvalues`
        :type dac_sel: ``adda_sel_e or int``
        :param channels: DAC channel selection (bitfield), refer to `adda_dac_channels_e__enumvalues` - OPTIONAL
        :type channels: ``adda_dac_channels_e or int``
        """
        if not isinstance(volts, list):
            volts = [volts]
        # end if

        data = list(map(self.convert_volt_to_dac_data, volts, [dac_sel] * len(volts)))
        self._write_dac(data=data, dac_sel=dac_sel, channels=channels)
    # end def write_dac

    @staticmethod
    def convert_adc_data_to_volt(data):
        """
        Convert ADC data code to volts.

        Context:
            ADC is wired for pseudo-differential measurements.
            Each ADC negative input channel is set to a fixed 2.5V voltage.
            Full scale is 5V, with 16-bit resolution.

            From ADS131A04 datasheet, section 9.5.1.5.1, page 40:
                The 16 bits of data per channel are sent in binary two's complement format, MSB first.
                The size of one code (LSB) is calculated using Equation 8:
                    1 LSB = (2 x V_REF / Gain) / 2^16 = FS / 2^15

        :param data: raw ADC value
        :type data: ``int or ctypes.c_int16``

        :return: ADC Voltage
        :rtype: ``float``
        """
        v_fs = 4.  # Full scale voltage
        v_common = 2.5  # half of 5V from MAX6350
        v_in = (data * v_fs) / 0x8000  # data * FS/2^15
        return v_in + v_common
    # end def convert_adc_data_to_volt

    @staticmethod
    def convert_volt_to_dac_data(volt, dac_sel):
        """
        Convert volts to DAC data code.

        Context:
            VREF = 5V

            DAC 0: PIO input thresholds
            DAC 1: PIO output levels
            DAC 2: LED-SPY input thresholds

            [DAC 1]
                Input resistor divider: 1 (none)
                Output resistor divider: 1 (none)
                DACREF2 = VREF = 5V
                dac1_data = 0xFFFF * (volt / 5)
                          = volt * 13107

            [DAC 0 & DAC 2]
                Input resistor divider: 9.9 kOhm / 15 kOhm
                Output resistor divider: 100 kOhm / 151 kOhm
                DACREF1 = DACREF3 = VREF * 15/(15+9.9) = VREF * 0.6 = 3 V
                dac0_data = 0xFFFF * (volt / (VREF * 15/(15+9.9))) * (151/(100+151))
                          = 0xFFFF * (volt / 3) * (151/(100+151))
                          = volt * 13141.812749

        :param volt: Desired DAC output voltage
        :type volt: ``float``
        :param dac_sel: DAC selection (DAC 0, 1 or 2), refer to `adda_sel_e__enumvalues`
        :type dac_sel: ``adda_sel_e or int``

        :return: DAC data code, matching the desired voltage for the selected DAC
        :rtype: ``int``

        :raise ``AssertionError``: multiple source of error:
         - Invalid DAC selection
         - Out-of-bounds voltage
        """
        assert dac_sel in [ADDA_SEL_DAC_0, ADDA_SEL_DAC_1, ADDA_SEL_DAC_2], f' DAC selection is invalid: {dac_sel}.'
        if dac_sel == ADDA_SEL_DAC_1:
            assert 0 <= volt <= 5, f'DAC voltage for {adda_sel_e__enumvalues[dac_sel]} is out-of-range: {volt}.'
            return round(volt * 13107)
        else:
            assert 0 <= volt <= 3, f'DAC voltage for {adda_sel_e__enumvalues[dac_sel]} is out-of-range: {volt}.'
            return round(volt * 13141.812749)
        # end if
    # end def convert_volt_to_dac_data
# end class AddaModule


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
