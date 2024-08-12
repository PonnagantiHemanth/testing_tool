#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9215.business
:brief: HID++ 2.0 ``Ads1231`` business test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ads1231utils import Ads1231TestUtils
from pytestbox.device.base.brakeforceutils import BrakeForceTestUtils
from pytestbox.device.hidpp20.peripheral.feature_9215.ads1231 import Ads1231TestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Ads1231BusinessTestCase(Ads1231TestCase):
    """
    Validate ``Ads1231`` business test cases
    """

    @features("Feature8134")
    @features("Feature9215")
    @level("Business")
    def test_write_other_nvs_data_business(self):
        """
        Validate ``WriteOtherNvsData`` is able to write max load value
        """
        self.post_requisite_reload_nvs = True
        data = HexList("400000000000000000000000000000")
        data_field_id_zero = HexList("00")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteOtherNvsData request")
        # --------------------------------------------------------------------------------------------------------------
        Ads1231TestUtils.HIDppHelper.write_other_nvs_data(self, data_field_id=data_field_id_zero, data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadOtherNvsData request")
        # --------------------------------------------------------------------------------------------------------------
        response_read_other_nvs_data = Ads1231TestUtils.HIDppHelper.read_other_nvs_data(
            self, data_field_id=data_field_id_zero)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verifying data HIDppHelper.read from ReadOtherNvsData matches values "
                                  "set by WriteOtherNvsData")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=data,
            obtained=response_read_other_nvs_data.data,
            msg=f"The value of max load is not as expected")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetInfo request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrakeForceTestUtils.HIDppHelper.get_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check getInfo response fields")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=HexList(data[0]),
            obtained=response.maximum_kg_load,
            msg=f"The value of max load is not as expected")
        self.testCaseChecked("BUS_9215_0001", _AUTHOR)
    # end def test_write_other_nvs_data_business
# end class Ads1231BusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
