#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.cccds.business
:brief: Validate BLE CCCDs Business test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/09/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pychannel.logiconstants import LogitechBleConstants
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pylibrary.mcu.nrf52.blesysattrchunks import DeviceBleUserServices
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.ble.base.bleppserviceutils import BleppServiceUtils
from pytestbox.device.ble.cccds.cccds import BleppCccdToggledTestCases
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.blemessage import BleMessage


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Christophe Roquebert"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleppCccdToggledBusinessTestCases(BleppCccdToggledTestCases):
    """
    BLE advertising in pairing mode with no prepairing data Business Test Cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    @features('BLEppCccdToggled')
    @features('BLEProtocol')
    @level('Business', 'SmokeTests')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_cccd_enabled(self):
        """
        Verify the firmware state machine when the BLE++ CCCD is enabled:
         - The DUT shall send notification in BLE++ (active = BLEpp)
         - The DUT shall switch the communication in HID when receiving request on this service
         - The DUT shall switch back in BLE++ when receiving request on this BLE++ service
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the HID++ service')
        LogHelper.log_check(self, 'Check communication in HID is active (cf EVT4: HID request received)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self, device_index=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable BLE++ service CCCD")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        BleppServiceUtils.configure_blepp_cccds(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 0x1D4B notification received first in the BLE++ characteristic "
                                  "(cf EVT1: BLEpp CCCD toggled)")
        # --------------------------------------------------------------------------------------------------------------
        blepp_notification = BleppServiceUtils.get_blepp_notification(test_case=self)
        hid20_blepp_notification = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_notification, current_channel=self.current_channel)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=to_int(hid20_blepp_notification.status),
                         msg='The Status parameter differs from the one expected')

        # ------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the BLE++ CCCD is now enabled")
        # ------------------------------------------------------------------------
        characteristic = BleppServiceUtils.get_blepp_characteristic(test_case=self)
        blepp_cccd_descriptor = self.ble_context.attribute_read(
            ble_context_device=self.ble_context_device_used, attribute=characteristic.get_descriptors(
                descriptor_uuid=BleUuid(value=BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION))[0])
        self.assertEqual(expected=DeviceBleUserServices.CCCD.NOTIFICATION.ENABLED,
                         obtained=to_int(blepp_cccd_descriptor.data[::-1]),
                         msg='The CCCD state differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the BLE++ service')
        # --------------------------------------------------------------------------------------------------------------
        enable_hidden_features_idx = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, EnableHidden.FEATURE_ID)
        set_hidden = SetEnableHiddenFeatures(device_index=0xFF, feature_index=enable_hidden_features_idx,
                                             enable_byte=EnableHidden.ENABLED)
        blepp_response = BleppServiceUtils.write_blepp_characteristic(test_case=self, hidpp_message=set_hidden)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check communication in BLEpp is active (cf EVT3: BLEpp request received)')
        # --------------------------------------------------------------------------------------------------------------
        hid20_blepp_response = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_response, current_channel=self.current_channel)
        self.assertEqual(expected=SetEnableHiddenFeaturesResponse.FUNCTION_INDEX,
                         obtained=to_int(hid20_blepp_response.functionIndex),
                         msg='The Function index parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the HID++ service')
        LogHelper.log_check(self, 'Check communication in HID is active (cf EVT4: HID request received)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self, device_index=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the BLE++ service')
        # --------------------------------------------------------------------------------------------------------------
        blepp_response = BleppServiceUtils.write_blepp_characteristic(test_case=self, hidpp_message=set_hidden)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check communication in BLEpp is active (cf EVT3: BLEpp request received)')
        # --------------------------------------------------------------------------------------------------------------
        hid20_blepp_response = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_response, current_channel=self.current_channel)
        self.assertEqual(expected=SetEnableHiddenFeaturesResponse.FUNCTION_INDEX,
                         obtained=to_int(hid20_blepp_response.functionIndex),
                         msg='The Status parameter differs from the one expected')

        self.testCaseChecked("BUS_BLEPP_CCCD_0001", _AUTHOR)
    # end def test_blepp_cccd_enabled

    @features('BLEppCccdToggled')
    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_cccd_persistent_to_hardware_reset(self):
        """
        Verify the firmware state machine when the BLE++ CCCD is enabled:
         - The DUT shall be in BLE++ after a hardware reboot
         - The DUT shall send any notification in BLE++ (active = BLEpp)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable BLE++ service CCCD")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        BleppServiceUtils.configure_blepp_cccds(test_case=self)

        blepp_notification = BleppServiceUtils.get_blepp_notification(test_case=self)
        hid20_blepp_notification = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_notification, current_channel=self.current_channel)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=to_int(hid20_blepp_notification.status),
                         msg='The Status parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self, delay=2.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Bond to the device")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.ble_context_device_used)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 0x1D4B notification received first in the BLE++ characteristic")
        # --------------------------------------------------------------------------------------------------------------
        blepp_notification = BleppServiceUtils.get_blepp_notification(test_case=self)
        hid20_blepp_notification = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_notification, current_channel=self.current_channel)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=to_int(hid20_blepp_notification.status),
                         msg='The Status parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 0x1004 notification received second in the BLE++ characteristic")
        # --------------------------------------------------------------------------------------------------------------
        blepp_notification = BleppServiceUtils.get_blepp_notification(test_case=self)
        hid20_blepp_notification = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_notification, current_channel=self.current_channel)
        self.assertEqual(expected=UnifiedBattery.ChargingStatus.DISCHARGING,
                         obtained=to_int(hid20_blepp_notification.charging_status),
                         msg='The Charging Status parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the BLE++ service')
        # --------------------------------------------------------------------------------------------------------------
        enable_hidden_features_idx = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, EnableHidden.FEATURE_ID)
        set_hidden = SetEnableHiddenFeatures(device_index=0xFF, feature_index=enable_hidden_features_idx,
                                             enable_byte=EnableHidden.ENABLED)
        BleppServiceUtils.write_blepp_characteristic(test_case=self, hidpp_message=set_hidden)

        self.testCaseChecked("BUS_BLEPP_CCCD_0002", _AUTHOR)
    # end def test_blepp_cccd_persistent_to_hardware_reset

    @features('BLEppCccdToggled')
    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_cccd_persistent_to_disconnection(self):
        """
        Verify the firmware state machine when the BLE++ CCCD is enabled:
         - The DUT shall be in BLE++ after a disconnection / reconnection
         - The DUT shall send any notification in BLE++ (active = BLEpp)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable BLE++ service CCCD")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        BleppServiceUtils.configure_blepp_cccds(test_case=self)

        blepp_notification = BleppServiceUtils.get_blepp_notification(test_case=self)
        hid20_blepp_notification = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_notification, current_channel=self.current_channel)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=to_int(hid20_blepp_notification.status),
                         msg='The Status parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device disconnection")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.disconnect_device(self, ble_context_device=self.ble_context_device_used)
        self.button_stimuli_emulator.user_action()

        LogHelper.log_step(self, "Bond to the device")
        # ----------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.ble_context_device_used)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 0x1D4B notification received first in the BLE++ characteristic")
        # --------------------------------------------------------------------------------------------------------------
        blepp_notification = BleppServiceUtils.get_blepp_notification(test_case=self)
        hid20_blepp_notification = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_notification, current_channel=self.current_channel)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=to_int(hid20_blepp_notification.status),
                         msg='The Status parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the BLE++ service')
        # --------------------------------------------------------------------------------------------------------------
        enable_hidden_features_idx = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, EnableHidden.FEATURE_ID)
        set_hidden = SetEnableHiddenFeatures(device_index=0xFF, feature_index=enable_hidden_features_idx,
                                             enable_byte=EnableHidden.ENABLED)
        BleppServiceUtils.write_blepp_characteristic(test_case=self, hidpp_message=set_hidden)

        self.testCaseChecked("BUS_BLEPP_CCCD_0003", _AUTHOR)
    # end def test_blepp_cccd_persistent_to_disconnection

    @features('BLEppCccdToggled')
    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_cccd_disabled(self):
        """
        Verify the firmware state machine when the BLE++ CCCD is disabled:
         - The DUT shall send notification in HID (active = HID)
         - The DUT shall be in HID after a disconnection / reconnection
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable BLE++ service CCCD")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        BleppServiceUtils.configure_blepp_cccds(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 0x1D4B notification received first in the BLE++ characteristic "
                                  "(cf EVT1: BLEpp CCCD toggled)")
        # --------------------------------------------------------------------------------------------------------------
        blepp_notification = BleppServiceUtils.get_blepp_notification(test_case=self)
        hid20_blepp_notification = BleppServiceUtils.convert_blepp_to_hidpp_message(
            ble_message=blepp_notification, current_channel=self.current_channel)
        self.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                         obtained=to_int(hid20_blepp_notification.status),
                         msg='The Status parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable BLE++ service CCCD")
        # --------------------------------------------------------------------------------------------------------------
        BleppServiceUtils.configure_blepp_cccds(test_case=self, enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the BLE++ service')
        # --------------------------------------------------------------------------------------------------------------
        enable_hidden_features_idx = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, EnableHidden.FEATURE_ID)
        set_hidden = SetEnableHiddenFeatures(device_index=0xFF, feature_index=enable_hidden_features_idx,
                                             enable_byte=EnableHidden.ENABLED)
        message = HexList(set_hidden)[2:]
        message.addPadding(size=LogitechBleConstants.BLEPP_MESSAGE_SIZE, fromLeft=False)
        self.ble_context.characteristic_write(
            ble_context_device=self.ble_context_device_used,
            characteristic=BleppServiceUtils.get_blepp_characteristic(test_case=self), data=BleMessage(data=message))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check communication in BLEpp is inactive')
        # --------------------------------------------------------------------------------------------------------------
        sleep(.5)
        self.assertTrue(expr=BleppServiceUtils.get_blepp_time_stamped_msg_queue(test_case=self).empty(),
                        msg='The BLEpp communication shall be inactive')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check response received through the HID service with device index = 0xFF '
                                  '(cf EVT3: BLEpp request received Notes')
        # --------------------------------------------------------------------------------------------------------------
        set_hidden_response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON,
                                                    class_type=SetEnableHiddenFeaturesResponse)
        self.assertEqual(expected=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         obtained=to_int(set_hidden_response.device_index),
                         msg='The device index parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the HID++ service')
        LogHelper.log_check(self, 'Check communication in HID is active (cf EVT4: HID request received)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self, device_index=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device disconnection")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.disconnect_device(self, ble_context_device=self.ble_context_device_used)
        self.button_stimuli_emulator.user_action()

        LogHelper.log_step(self, "Bond to the device")
        # ----------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.ble_context_device_used)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 0x1D4B notification received through the HID++ service")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(test_case=self)

        self.testCaseChecked("BUS_BLEPP_CCCD_0004", _AUTHOR)
    # end def test_blepp_cccd_disabled

    @features('BLEppCccdToggled')
    @features('BLEProtocol')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_cccd_default(self):
        """
        Verify the default CCCD configuration after a pairing sequence:
         - BLE++ CCCD shall be disabled
         - The DUT shall communicate in HID (active = HID)
         - Any communication on the BLE++ service is forbidden
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the BLE++ service')
        # --------------------------------------------------------------------------------------------------------------
        enable_hidden_features_idx = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, EnableHidden.FEATURE_ID)
        set_hidden = SetEnableHiddenFeatures(device_index=0xFF, feature_index=enable_hidden_features_idx,
                                             enable_byte=EnableHidden.ENABLED)
        message = HexList(set_hidden)[2:]
        message.addPadding(size=LogitechBleConstants.BLEPP_MESSAGE_SIZE, fromLeft=False)
        self.ble_context.characteristic_write(
            ble_context_device=self.ble_context_device_used,
            characteristic=BleppServiceUtils.get_blepp_characteristic(test_case=self), data=BleMessage(data=message))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check communication in BLEpp is inactive (cf EVT3: BLEpp request received -> '
                                  'DEV_ERROR)')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=BleppServiceUtils.get_blepp_time_stamped_msg_queue(test_case=self).empty(),
                        msg='The BLEpp communication shall be inactive')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send the enable hidden Features through the HID++ service')
        LogHelper.log_check(self, 'Check communication in HID is active (cf EVT4: HID request received)')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self, device_index=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device disconnection")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.disconnect_device(self, ble_context_device=self.ble_context_device_used)
        self.button_stimuli_emulator.user_action()

        LogHelper.log_step(self, "Bond to the device")
        # ----------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.ble_context_device_used)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 0x1D4B notification received through the HID++ service")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(test_case=self)

        self.testCaseChecked("BUS_BLEPP_CCCD_0005", _AUTHOR)
    # end def test_blepp_cccd_default
# end class BleppCccdToggledBusinessTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
