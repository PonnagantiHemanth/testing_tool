#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.recovery.interface
:brief: Receiver for device recovery interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/02/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.recovery.recovery import ReceiverForDeviceRecoveryTestCase
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.recoveryutils import RecoveryTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverForDeviceRecoveryInterfaceTestCase(ReceiverForDeviceRecoveryTestCase):
    """
    Validate ``ReceiverForDeviceRecovery`` interface test cases
    """

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Interface')
    @services('Debugger')
    def test_device_recovery_notification_api(self):
        """
        DeviceRecoveryNotification API validation
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify all Device Recovery Notification parts are received')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = RecoveryTestUtils.get_discovered_recovery_device(test_case=self)
        self.assertNotNone(obtained=bluetooth_address,
                           msg="Recovery device wanted not found")

        self.testCaseChecked("INT_DEV_RECVONR_0001")
    # end def test_device_recovery_notification_api
# end class ReceiverForDeviceRecoveryInterfaceTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
