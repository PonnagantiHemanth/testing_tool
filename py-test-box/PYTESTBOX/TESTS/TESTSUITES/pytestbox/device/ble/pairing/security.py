#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.pairing.security
:brief: Validate BLE pairing Security test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/09/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.blechannel import BleChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.root import Root
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import LOGITECH_ENCRYPTION_KEY_SIZE
from pytestbox.device.ble.pairing.pairing import PairingTestCases


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Stanislas Cottard"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PairingSecurityTestCases(PairingTestCases):
    """
    BLE pairing security Test Cases
    """

    @features('BLEProtocol')
    @level('Security')
    @services('BleContext')
    @services('Debugger')
    def test_host_with_lesc_128_bits_encryption_key(self):
        """
        Verify that a LE secure connection is used if the host shows the capabilities
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect and bond to the device with LESC capabilities")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.current_device, lesc=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the connection is using LESC with a 128bits encryption key")
        # --------------------------------------------------------------------------------------------------------------
        connection_security_parameters = self.ble_context.get_connection_security_parameters(
            ble_context_device=self.current_device)
        self.assertTrue(expr=connection_security_parameters.encrypted, msg="The connection is not encrypted")
        self.assertTrue(expr=connection_security_parameters.lesc, msg="The connection is not LE Secure Connection")
        self.assertEqual(expected=LOGITECH_ENCRYPTION_KEY_SIZE,
                         obtained=connection_security_parameters.encryption_key_size,
                         msg="The connection does not have the required 128bits encryption key")

        self.testCaseChecked("SEC_BLE_PAIRING_0001", _AUTHOR)
    # end def test_host_with_lesc_128_bits_encryption_key

    @features('BLEProtocol')
    @level('Security')
    @services('BleContext')
    @services('Debugger')
    def test_host_with_legacy_bonding_128_bits_encryption_key(self):
        """
        Verify that a LE secure connection is optional if the host disables this capability
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect and bond to the device without LESC capabilities")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.current_device, lesc=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the connection is using legacy bonding with a 128bits encryption key")
        # --------------------------------------------------------------------------------------------------------------
        connection_security_parameters = self.ble_context.get_connection_security_parameters(
            ble_context_device=self.current_device)
        self.assertTrue(expr=connection_security_parameters.encrypted, msg="The connection is not encrypted")
        self.assertFalse(expr=connection_security_parameters.lesc,
                         msg="The connection is LE Secure Connection while it should be legacy")
        self.assertEqual(expected=LOGITECH_ENCRYPTION_KEY_SIZE,
                         obtained=connection_security_parameters.encryption_key_size,
                         msg="The connection does not have the required 128bits encryption key")

        self.testCaseChecked("SEC_BLE_PAIRING_0002", _AUTHOR)
    # end def test_host_with_legacy_bonding_128_bits_encryption_key

    # TODO: This test is here for now (for intel Evo tests) but should be moved to more appropriated location
    @features('BLEProtocol')
    @features('NoUSB')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @services('Rechargeable')
    def test_ble_connection_continue_after_charging_starts(self):
        """
        Verify that a BLE connection is kept after the USB charging is started
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect and bond to the device")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.current_device)
        self.ble_channel = BleChannel(ble_context=self.ble_context, ble_context_device=self.current_device)
        # Open the channel on the HID packets only for the last part of the test
        self.ble_channel.open()
        ChannelUtils.get_descriptors(test_case=self, channel=self.ble_channel)
        _, root_version = self.current_channel.hid_dispatcher.get_feature_entry_by_index(
            feature_index=Root.FEATURE_INDEX)
        self.ble_channel.hid_dispatcher.add_feature_entry(
            feature_index=Root.FEATURE_INDEX, feature_id=Root.FEATURE_ID, feature_version=root_version)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start device charging")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_turn_off_usb_charging_cable = True
        if self.power_supply_emulator is not None:
            self.power_supply_emulator.recharge(enable=True)
        # end if
        self.device.turn_on_usb_charging_cable()
        # Delay to make sure that the supervision timeout is not triggered
        sleep(4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the connection is still present")
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self.ble_channel.is_device_connected(force_refresh_cache=True),
                        msg="The device is not connected anymore")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send a HID++ request (root feature 0x0000)")
        LogHelper.log_check(self, "Check that a response is received")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=DeviceInformation.FEATURE_ID, channel=self.ble_channel)

        self.testCaseChecked("SEC_BLE_PAIRING_0003", _AUTHOR)
    # end def test_ble_connection_continue_after_charging_starts
# end class PairingSecurityTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
