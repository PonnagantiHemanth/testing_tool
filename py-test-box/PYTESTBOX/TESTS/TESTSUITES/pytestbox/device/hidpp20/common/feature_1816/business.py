#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1816.business
:brief: HID++ 2.0 BLEPro pre-pairing business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleproprepairingutils import BleProPrePairingTestUtils
from pytestbox.device.hidpp20.common.feature_1816.bleproprepaing import BleProPrePairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Christophe Roquebert"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BleProPrePairingBusinessTestCase(BleProPrePairingTestCase):
    """
    Validate Device BLE Pro Pre-pairing Business TestCases
    """

    @features('Feature1816')
    @level('Business', 'SmokeTests')
    def test_device_prepairing_sequence(self):
        """
        Validate device Pre-pairing sequence Business Case

        To set the prepairing data, the requested sequence is :
        - prepairing_management (Start)
        - set the mandatory pairing data (set_LTK, set_prepairing_data (remoteAddress))
        - set the optional pairing data (set_IRK, set_CSRK, set_prepairing_data, ??)
        - check for the response of the check commands
        - prepairing_management (Store)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence")
        LogHelper.log_check(self, "Check pre-pairing response")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index)

        self.testCaseChecked("BUS_1816_0001")
    # end def test_device_prepairing_sequence
# end class BleProPrePairingBusinessTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
