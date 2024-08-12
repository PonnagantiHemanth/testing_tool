#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package:    pyraspi.services.ina226
:brief:      Tests for Raspi ina226 Control Class
:author:     fred.chen
:date:       2019/6/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import TestCase
from unittest import skipIf
from time import sleep
import sys
if sys.platform == 'linux':
    from pyraspi.services.daemon import Daemon
    from pyraspi.services.ina226 import INA226
    from pyraspi.services.ina226 import ina226_averages_t
    from pyraspi.services.ina226 import ina226_busConvTime_t
    from pyraspi.services.ina226 import ina226_shuntConvTime_t
    from pyraspi.services.ina226 import ina226_mode_t
# end if

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


@skipIf(sys.platform != 'linux', 'Support test on Raspi only!')
@skipIf(Daemon.is_host_kosmos(),
        'Support test on Raspberry Pi NOT configured for KOSMOS project (legacy test environment)!')
class INA226TestCase(TestCase):
    """
    Test ina226 Class
    """

    R_SHUNT = 0.5
    VERBOSE = False

    # @skipIf(Raspi.discover_ina226() is False, 'INA226 not found')
    def test_INA226GetId(self):
        """
        Test INA226 Manufacture ID and Die ID
        """
        if INA226.discover() is False:
            self.skipTest('INA226 is not present!')
        else:
            ina226 = INA226.get_instance()
            ina226.configure(avg=ina226_averages_t['INA226_AVERAGES_16'],
                             busConvTime=ina226_busConvTime_t['INA226_BUS_CONV_TIME_8244US'],
                             shuntConvTime=ina226_shuntConvTime_t['INA226_SHUNT_CONV_TIME_8244US'],
                             mode=ina226_mode_t['INA226_MODE_SHUNT_BUS_CONT'])
            ina226.calibrate(rShuntValue=self.R_SHUNT, iMaxExcepted=0.16)
            sleep(2)
            self.assertEqual(0x5449, ina226.get_manufacturer_id())
            self.assertEqual(0x2260, ina226.get_die_id())
        # end if
    # end def test_INA226GetId

    def test_INA226(self):
        """
        Test INA226 Class
        """
        if INA226.discover() is False:
            self.skipTest('INA226 is not present!')
        else:
            ina226 = INA226.get_instance()
            ina226.configure(avg=ina226_averages_t['INA226_AVERAGES_16'],
                             busConvTime=ina226_busConvTime_t['INA226_BUS_CONV_TIME_8244US'],
                             shuntConvTime=ina226_shuntConvTime_t['INA226_SHUNT_CONV_TIME_8244US'],
                             mode=ina226_mode_t['INA226_MODE_SHUNT_BUS_CONT'])
            ina226.calibrate(rShuntValue=self.R_SHUNT, iMaxExcepted=0.16)

            sleep(2)

            if self.VERBOSE:
                print('Measure current 10 times per 500ms...')
                for x in range(10):
                    print(f'Current: {round(ina226.read_shunt_current() * 1000, 6)} mA')
                    sleep(0.5)
                # end for
            # end if

            self.assertEqual(self.R_SHUNT, ina226.rShunt)
        # end if
    # end def test_INA226

# end class INA226TestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
