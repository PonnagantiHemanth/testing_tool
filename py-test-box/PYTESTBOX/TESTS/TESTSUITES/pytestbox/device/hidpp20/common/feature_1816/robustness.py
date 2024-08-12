#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1816.robustness
:brief: HID++ 2.0 BLEPro pre-pairing robustness test suite
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
class BleProPrePairingRobustnessTestCase(BleProPrePairingTestCase):
    """
    Validate Device BLE Pro pre-pairing Robustness TestCases
    """
    @features('Feature1816')
    @level('Robustness')
    def test_delete_called_twice(self):
        """
        Check calling twice the Delete request do not raise any HID++ error code
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the mandatory part of the Device Pre-pairing sequence including the "
                                         "last 'Store' requests")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send the prepairing_management request with prepairing_slot=0 and "
                                 "prepairing_management_control='Delete'")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.delete_pre_pairing_slot(self, self.feature_1816, self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Resend the prepairing_management request with prepairing_slot=0 and "
                                 "prepairing_management_control='Delete'")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.delete_pre_pairing_slot(self, self.feature_1816, self.feature_1816_index)

        self.testCaseChecked("ROB_1816_0001")
    # end def test_delete_called_twice
# end class BleProPrePairingRobustnessTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
