#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.adda_test
:brief: Tests for Kosmos ADDA (PODS ADC & DAC) class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/05/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import ctypes
from time import sleep

from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_DAC_CH_ALL
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_1
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@require_kosmos_device(DeviceName.ADDA)
class KosmosAddaTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos ADDA (PODS ADC & DAC) class
    """

    def test_adc_read(self):
        """
        ADC Read test: let 30s to the user to apply voltage and check value in console
        """
        last = []
        time = 0
        max_time = 30
        while time < max_time:
            adc_raw = self.kosmos.adda._read_adc()
            adc_v = list(map(self.kosmos.adda.convert_adc_data_to_volt, adc_raw))
            code_unsigned = ctypes.c_uint16(adc_raw[0]).value
            if last != adc_raw:
                print(f'{code_unsigned:#06x}\t{adc_raw[0]:#06x}\t{adc_v[0]:.5f}')
                last = adc_raw
            # end if
            sleep(0.1)
            time += 0.1
        # end while
    # end def test_adc_read

    def test_dac_write(self):
        """
        DAC ramp-up test.
        """
        dac = ADDA_SEL_DAC_1
        channels = ADDA_DAC_CH_ALL

        self.kosmos.adda.write_dac(volts=0, dac_sel=dac, channels=channels)
        sleep(0.1)

        # Only let the loop been played 5 times
        loop = 0
        max_loop = 5
        while loop < max_loop:
            print(f'Loop {loop+1}/{max_loop}')
            for i in range(0, 0x10000, 0x10):
                volt = 5 * i / 0xFFFF
                self.kosmos.adda.write_dac(volts=volt, dac_sel=dac, channels=channels)

                if not i & 0xff:
                    print(f'{self.kosmos.adda.convert_volt_to_dac_data(volt, dac):#06x}\t{volt:.5f}')
                # end if
            # end for
            loop += 1
        # end while
        # Reset DAC after test
        self.kosmos.adda.write_dac(volts=0, dac_sel=dac, channels=channels)
    # end def test_dac_write

    def test_adc_dac(self):
        """
        DAC-ADC feedback loop test.
        Plug a wire between ADDA_SEL_DAC_1 and ADDA_DAC_CH_ALL (any)
        """
        dac = ADDA_SEL_DAC_1
        channels = ADDA_DAC_CH_ALL

        self.kosmos.adda.write_dac(volts=0, dac_sel=dac, channels=channels)
        sleep(0.1)

        for millivolts in list(range(0, 5000, 10)) + [5000]:
            volts = millivolts/1000
            self.kosmos.adda.write_dac(volts=volts, dac_sel=dac, channels=channels)

            adc_raw = self.kosmos.adda._read_adc()
            adc_v = list(map(self.kosmos.adda.convert_adc_data_to_volt, adc_raw))
            code_unsigned = ctypes.c_uint16(adc_raw[0]).value

            if (not millivolts % 100) or (volts == 5):
                print(f'{self.kosmos.adda.convert_volt_to_dac_data(volts, dac):#06x}\t{volts:.5f}'
                      f'\t{code_unsigned:#06x}\t{adc_raw[0]:+#06x}\t{adc_v[0]:.5f}'
                      f'\t{volts - adc_v[0]:.5f}')
            # end if
        # end for
        sleep(0.1)

        for data in list(range(0, 0x10000, 0x10)) + [0xFFFF]:
            self.kosmos.adda._write_dac(data=data, dac_sel=dac, channels=channels)

            adc_raw = self.kosmos.adda._read_adc()
            adc_v = list(map(self.kosmos.adda.convert_adc_data_to_volt, adc_raw))
            code_unsigned = ctypes.c_uint16(adc_raw[0]).value

            volt = data / (0xFFFF/5)
            if (not data & 0xff) or (data == 0xFFFF):
                print(f'{data:#06x}\t{volt:.5f}'
                      f'\t{code_unsigned:#06x}\t{adc_raw[0]:+#06x}\t{adc_v[0]:.5f}'
                      f'\t{volt - adc_v[0]:.5f}')
            # end if
        # end for
        sleep(0.1)
        self.kosmos.adda.write_dac(volts=0, dac_sel=dac, channels=channels)
    # end def test_adc_dac
# end class KosmosAddaTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
