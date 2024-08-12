#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.recovery.business
:brief: Receiver for device recovery business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/02/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.receiver.recovery.recovery import ReceiverForDeviceRecoveryTestCase
from pytestbox.shared.base.recoveryutils import DisconnectMethod

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverForDeviceRecoveryBusinessTestCase(ReceiverForDeviceRecoveryTestCase):
    """
    Validate ``ReceiverForDeviceRecovery`` business test cases
    """

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Business')
    @services('Debugger')
    def test_complete_business_dfu_restart(self):
        """
        Receiver with recovery device business case: Discover, Connect, then perform DFU, finishing with DFU.Restart
        function
        """
        self._complete_business(disconnect_method=DisconnectMethod.DFU_RESTART, perform_dfu=True)

        self.testCaseChecked("BUS_DEV_RECVONR_0001")
    # end def test_complete_business_dfu_restart

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Business')
    @services('Debugger')
    def test_complete_business_c1_unpairing(self):
        """
        Receiver with recovery device business case: Discover, Connect, then Disconnect using
        PerformDevicePairingAndUnpairing.ConnectDevices = Unpairing (0x03)
        """
        self._complete_business(disconnect_method=DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING)

        self.testCaseChecked("BUS_DEV_RECVONR_0002")
    # end def test_complete_business_c1_unpairing

    @features('DeviceRecovery')
    @features('BLEProProtocol')
    @level('Business')
    @services('Debugger')
    def test_complete_business_device_off_on(self):
        """
        Receiver with recovery device business case: Discover, Connect, then Disconnect using device power supply
        off/on function
        """
        self._complete_business(disconnect_method=DisconnectMethod.DEVICE_OFF_ON)

        self.testCaseChecked("BUS_DEV_RECVONR_0003")
    # end def test_complete_business_device_off_on
# end class ReceiverForDeviceRecoveryBusinessTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
