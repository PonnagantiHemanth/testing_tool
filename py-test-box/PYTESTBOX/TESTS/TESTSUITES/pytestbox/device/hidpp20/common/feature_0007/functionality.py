#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0007.functionality
:brief: HID++ 2.0 DeviceFriendlyName functionality test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/10/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesFactory
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesFactory
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils as Utils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname import DeviceFriendlyNameTestCase
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pytransport.ble.bleconstants import BleAdvertisingDataType


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceFriendlyNameFunctionalityTestCase(DeviceFriendlyNameTestCase):
    """
    Validates DeviceFriendlyName functionality test cases
    """
    @features('Feature0007')
    @level('Functionality')
    def test_get_friendly_name_index_valid_range(self):
        """
        Validates GetFriendlyName Functionality case
        """
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        for byte_index in range(0, int(Numeral(response.name_len))):
            response = Utils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(self, byte_index=byte_index)
            if response is None or len(response) <= 0:
                break
            # end if
        # end for
        self.testCaseChecked("FUN_0007_0001", _AUTHOR)
    # end def test_get_friendly_name_index_valid_range

    @features('Feature0007')
    @level('Functionality')
    def test_get_default_friendly_name_index_valid_range(self):
        """
        Validates GetDefaultFriendlyName Functionality case sequence
        """
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        for byte_index in range(0, int(Numeral(response.default_name_len))):
            response = Utils.GetDefaultFriendlyNameHelper.HIDppHelper.get_default_friendly_name(
                    self, byte_index=byte_index)
            if response is None or len(response) <= 0:
                break
            # end if
        # end for
        self.testCaseChecked("FUN_0007_0002", _AUTHOR)
    # end def test_get_default_friendly_name_index_valid_range

    @features('Feature0007')
    @level('Functionality')
    def test_set_friendly_name_index_valid_range(self):
        """
        Validates SetFriendlyName index valid range
        """
        self.post_requisite_reload_nvs = True
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop to write test name starting at different index")
        # --------------------------------------------------------------------------------------------------------------
        for byte_index in range(0, int(Numeral(response.name_max_len))):
            Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(
                    self, byte_index=byte_index, name_chunk=self.test_name_chunk)
        # end for
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        received_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)
        expected_name = HexList((self.test_name_chunk[0:1] * int(Numeral(response.name_len))).encode()).toString()
        Utils.GetFriendlyNameHelper.MessageChecker.check_name_match(self, received_name, expected_name)
        self.testCaseChecked("FUN_0007_0003", _AUTHOR)
    # end def test_set_friendly_name_index_valid_range

    @features('Feature0007')
    @level('Functionality')
    def test_set_friendly_name_extra_truncated(self):
        """
        Validates SetFriendlyName properly truncates the extra padding
        """
        self.post_requisite_reload_nvs = True
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        d, q = divmod(int(Numeral(response.name_max_len)), self.name_chunk_length)
        expected_name = f"{self.test_name_chunk * d}{self.test_name_chunk[0:q]}"
        for byte_index in range(0, d):
            Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(
                    self, byte_index=byte_index * self.name_chunk_length, name_chunk=self.test_name_chunk)
        # end for
        if d == 0:
            byte_index = 0
        else:
            byte_index = d * self.name_chunk_length
        # end if
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(
                self, byte_index=byte_index, name_chunk=self.test_name_chunk)
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        received_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)
        Utils.GetFriendlyNameHelper.MessageChecker.check_name_match(self, received_name, expected_name)
        self.testCaseChecked("FUN_0007_0004", _AUTHOR)
    # end def test_set_friendly_name_extra_truncated

    @features('Feature0007')
    @level('Functionality')
    def test_set_friendly_name_length(self):
        """
        Validates SetFriendlyName interface
        """
        self.post_requisite_reload_nvs = True
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(self, byte_index=0, name_chunk=self.test_name_chunk)
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        received_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)
        Utils.GetFriendlyNameHelper.MessageChecker.check_length(
                self, int(Numeral(response.name_len)), len(received_name))
        Utils.GetFriendlyNameHelper.MessageChecker.check_name_match(self, received_name, self.test_name_chunk)
        self.testCaseChecked("FUN_0007_0005", _AUTHOR)
    # end def test_set_friendly_name_length

    @features('Feature0007')
    @level('Functionality')
    @services('PowerSupply')
    def test_set_friendly_name_available_after_reset_by_power_emulator(self):
        """
        Validates SetFriendlyName data available after reset
        """
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        self.post_requisite_reload_nvs = True
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(self, byte_index=0, name_chunk=self.test_name_chunk)
        # ------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # ------------------------------------------
        self.reset(LinkEnablerInfo.HID_PP_MASK, hardware_reset=True, recover_time_needed=True)
        sleep(2)
        friendly_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(self, byte_index=0)
        Utils.GetFriendlyNameHelper.MessageChecker.check_name_match(self, friendly_name, self.test_name_chunk)
        self.testCaseChecked("FUN_0007_0006", _AUTHOR)
    # end def test_set_friendly_name_available_after_reset_by_power_emulator

    @features('Feature0007')
    @features('Feature1802')
    @level('Functionality')
    def test_set_friendly_name_available_after_reset_by_feature_1802(self):
        """
        Validates SetFriendlyName data available after reset
        """
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        self.post_requisite_reload_nvs = True
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(self, byte_index=0, name_chunk=self.test_name_chunk)
        # ------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # ------------------------------------------
        DeviceTestUtils.ResetHelper.hidpp_reset(self)

        friendly_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(self, byte_index=0)
        Utils.GetFriendlyNameHelper.MessageChecker.check_length(self, len(friendly_name), len(self.test_name_chunk))
        Utils.GetFriendlyNameHelper.MessageChecker.check_name_match(self, friendly_name, self.test_name_chunk)
        self.testCaseChecked("FUN_0007_0006", _AUTHOR)
    # end def test_set_friendly_name_available_after_reset_by_feature_1802

    @features('Feature0007')
    @level('Functionality')
    def test_set_friendly_name_validation(self):
        """
        Validates SetFriendlyName interface
        """
        self.post_requisite_reload_nvs = True
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        default_friendly_name = Utils.GetDefaultFriendlyNameHelper.HIDppHelper.get_full_name(
                self, response.default_name_len)
        Utils.GetDefaultFriendlyNameHelper.MessageChecker.check_default_name_length(
                self, response.default_name_len, default_friendly_name)
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(self, byte_index=0, name_chunk=self.test_name_chunk)
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        received_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)
        Utils.GetFriendlyNameHelper.MessageChecker.check_name_match(self, received_name, self.test_name_chunk)
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        Utils.GetFriendlyNameHelper.MessageChecker.check_length(
                self, int(Numeral(response.name_len)), len(self.test_name_chunk))
        self.testCaseChecked("FUN_0007_0007", _AUTHOR)
    # end def test_set_friendly_name_validation

    @features('Feature0007')
    @level('Functionality')
    def test_friendly_name_validation_with_device_name(self):
        """
        Validates SetFriendlyName does not affect GetDeviceName
        """
        device_name_count_before = to_int(
            DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name_count(test_case=self).device_name_count)
        device_name_before = ascii_converter(
            DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name(test_case=self, char_index=0).device_name)

        self.post_requisite_reload_nvs = True
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(self, byte_index=0, name_chunk=self.test_name_chunk)
        friendly_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(self, byte_index=0)
        device_name_count_after = to_int(
            DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name_count(test_case=self).device_name_count)
        device_name_after = ascii_converter(
            DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name(test_case=self, char_index=0).device_name)

        Utils.SetFriendlyNameHelper.MessageChecker.check_equal_value(
                self, device_name_count_before, device_name_count_after)
        Utils.SetFriendlyNameHelper.MessageChecker.check_equal_value(
                self, device_name_before, device_name_after)
        Utils.SetFriendlyNameHelper.MessageChecker.check_equal_value(self, friendly_name, self.test_name_chunk)
        self.testCaseChecked("FUN_0007_0008", _AUTHOR)
    # end def test_friendly_name_validation_with_device_name

    @features('Feature0007')
    @features('Feature1806')
    @level('Functionality')
    def test_friendly_name_with_set_device_properties(self):
        """
        Validates SetDevicesProperties affect GetDeviceFriendlyName
        """
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x1806)")
        # --------------------------------------------------------------
        feature_1806_index, feature_1806, _, _ = Utils.HIDppHelper.get_parameters(
            test_case=self,
            feature_id=ConfigurableDeviceProperties.FEATURE_ID,
            factory=ConfigurableDevicePropertiesFactory)

        # ----------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setDeviceProperties (0x1806) request to set BLE_LONG_NAME")
        # ----------------------------------------------------------------------------------------
        property_data = HexList.fromString(self.test_name_chunk)[0:10]
        report = feature_1806.set_device_properties_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=feature_1806_index,
                property_id=feature_1806.property_id.BLE_LONG_NAME,
                flag=1,
                sub_data_index=0,
                property_data=property_data)
        ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=feature_1806.set_device_properties_response_cls
        )

        report = feature_1806.get_device_properties_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=feature_1806_index,
                property_id=feature_1806.property_id.BLE_LONG_NAME,
                flag=1,
                sub_data_index=0)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=feature_1806.get_device_properties_response_cls)

        expected_data = property_data
        expected_data.addPadding(response.LEN.PROPERTY_DATA // 8, fromLeft=False)
        Utils.GetFriendlyNameHelper.MessageChecker.check_equal_value(self, response.property_data, expected_data)
        self.testCaseChecked("FUN_0007_0009", _AUTHOR)
    # end def test_friendly_name_with_set_device_properties

    @features('Feature0007')
    @features('Feature1807')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
    @level('Functionality')
    def test_friendly_name_with_write_property(self):
        """
        Validate 0x1807 - Configurable Properties writeProperty affects GetDeviceFriendlyName
        """
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        feature_1807_index, feature_1807, _, _ = Utils.HIDppHelper.get_parameters(
            test_case=self,
            feature_id=ConfigurableProperties.FEATURE_ID,
            factory=ConfigurablePropertiesFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write BLE_GAP_APP_NAME")
        # --------------------------------------------------------------------------------------------------------------
        test_data = HexList.fromString(self.test_name_chunk[0:10])
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self,
                                                                    ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Device Friendly Name")
        # --------------------------------------------------------------------------------------------------------------
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        received_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Friendly Name matches data written to BLE_GAP_APP_NAME property")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=test_data.toString(),
                         obtained=received_name,
                         msg="Friendly Name should match the data written to BLE_GAP_APP_NAME property")

        self.testCaseChecked("FUN_0007_0009", _AUTHOR)
    # end def test_friendly_name_with_write_property

    @features('Feature0007')
    @features('RcvBLEEnumeration')
    @features('RcvWithDevice')
    @level('Functionality')
    def test_ble_pro_device_name_api(self):
        """
        Validate read BLE Pro device name (B5 6n)
        """
        # ------------------------------------------------------------------
        LogHelper.log_step(self, "Test Loop over BLE Pro Device Name parts")
        # ------------------------------------------------------------------
        device_name_resps = []
        for part in NonVolatilePairingInformation.BleProDeviceNamePart:
            # ---------------------------------------------------------------
            LogHelper.log_step(self, "Send Read BLE Pro device name request")
            # ---------------------------------------------------------------
            device_name_req = GetBLEProDeviceDeviceNameRequest(
                    NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN,
                    part)

            device_name_resp = ChannelUtils.send(
                test_case=self,
                report=device_name_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                response_class_type=GetBLEProDeviceDeviceNameResponse)

            # ------------------------------------------------
            LogHelper.log_check(self, "Check response fields")
            # ------------------------------------------------
            checks = EnumerationTestUtils.BLEProDeviceNameResponseChecker.get_default_check_map(self)
            checks["device_name_part"] = (
                    EnumerationTestUtils.BLEProDeviceNameResponseChecker.check_device_name_part, part)
            EnumerationTestUtils.BLEProDeviceNameResponseChecker.check_fields(
                    self, device_name_resp, GetBLEProDeviceDeviceNameResponse, checks)

            device_name_resps.append(device_name_resp)
        # end for

        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        received_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)

        # --------------------------------------------
        LogHelper.log_check(self, "Check Device Name")
        # --------------------------------------------
        EnumerationTestUtils.check_device_name(self, device_name_resps, received_name)

        self.testCaseChecked("FUN_0007_0010", _AUTHOR)
    # end def test_ble_pro_device_name_api

    @features('Feature0007')
    @features('BLEProtocol')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_get_friendly_name_same_complete_local_name_scan_response(self):
        """
        Verify that the scan response in application mode and unpaired have the same complete local name than the
        name gotten with the feature 0x0007
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get full name using the feature 0x0007')
        # ---------------------------------------------------------------------------
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        received_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)

        self._verify_complete_local_name(
            expected_name=received_name,
            fail_message="The complete local name differs from the one gotten with the feature 0x0007")

        self.testCaseChecked("FUN_0007_0011", "Stanislas Cottard")
    # end def test_get_friendly_name_same_complete_local_name_scan_response

    @features('Feature0007')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
    @features('BLEProtocol')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_set_friendly_name_change_complete_local_name_scan_response(self):
        """
        Verify that the scan response in application mode and unpaired have the complete local name change when
        changing the name with the feature 0x0007
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set name using the feature 0x0007')
        # ---------------------------------------------------------------------------
        # Length of the name from 0x1807 properties if any, else from 0x0007 settings
        name_len = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(
            self, ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
        # Sanity check
        assert name_len > 0, \
            f"BLE_GAP_APP_NAME property should be superior to 0, current BLE_GAP_APP_NAME length ({name_len}) is not"

        self.post_requisite_reload_nvs = True
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(
            self, byte_index=0, name_chunk=self.test_name_chunk[:name_len])

        self._verify_complete_local_name(
            expected_name=self.test_name_chunk[:name_len],
            fail_message="The complete local name differs from the set with the feature 0x0007")

        self.testCaseChecked("FUN_0007_0012", "Stanislas Cottard")
    # end def test_set_friendly_name_change_complete_local_name_scan_response

    def _verify_complete_local_name(self, expected_name, fail_message):
        """
        Change host, scan for the device and verify the complete local name in the scan response.

        :param expected_name: Expected value of the complete local name
        :type expected_name: ``str``
        :param fail_message: Message to give to the assert method if it fails
        :type fail_message: ``str``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter pairing mode')
        # ---------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.button_stimuli_emulator.enter_pairing_mode()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Scan until current device is found (max 2s)")
        # ---------------------------------------------------------------------------
        current_device = BleProtocolTestUtils.scan_for_current_device(
            test_case=self, scan_timeout=2, send_scan_request=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the complete local name in the scan response is the same "
                                  "as the one gotten with the feature 0x0007")
        # ---------------------------------------------------------------------------
        complete_local_name = current_device.scan_response[0].records[
                                          BleAdvertisingDataType.COMPLETE_LOCAL_NAME]
        complete_local_name = HexList(complete_local_name).toString()
        self.assertEqual(obtained=complete_local_name,
                         expected=expected_name,
                         msg=fail_message)
    # end def _verify_complete_local_name
# end class DeviceFriendlyNameFunctionalityTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
