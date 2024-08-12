#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.recovery.business
:brief: Device recovery business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.device.recovery.recovery import DeviceRecoveryTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceRecoveryBusinessTestCase(DeviceRecoveryTestCase):
    """
    Validate ``DeviceRecovery`` business test cases
    """

    @features('DeviceRecovery')
    @level('Business')
    @services('Debugger')
    def test_complete_recovery_dfu_business_no_pairing(self):
        """
        Validate the business case without pairing of the DFU process in recovery mode
        """
        self._complete_dfu_business(pairing=False)

        self.testCaseChecked("BUS_DEV_RECV_0001#1")
    # end def test_complete_recovery_dfu_business_no_pairing

    @features('DeviceRecovery')
    @features('Feature00D0SoftDevice')
    @level('Business')
    @services('Debugger')
    def test_complete_recovery_soft_device_dfu_business_no_pairing(self):
        """
        Validate the business case without pairing of the soft device DFU process in recovery mode
        """
        self._complete_dfu_business(pairing=False, soft_device=True)

        self.testCaseChecked("BUS_DEV_RECV_0001#2")
    # end def test_complete_recovery_soft_device_dfu_business_no_pairing
# end class DeviceRecoveryBusinessTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
