#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.small_services.robustness
:brief: Validate Gatt small services Robustness test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/01/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import queue

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.logiconstants import LogitechVendorUuid
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesFactory
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import choices
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceApplicationTestCase
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------

_AUTHOR = "Sylvana Ieri"

STRING_TO_CUT = "a 23 byte string to cut"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
def _extract_matching_handle(application_gatt_table, bootloader_blepp_characteristic_handle):
    """
    helper method to extract the element of the gatt table with the same handle as
    the bootloader blepp characteristic
    :param application_gatt_table: the gatt table that will be iterated
    :type application_gatt_table: ``list``
    :param bootloader_blepp_characteristic_handle: handle of reference to be matched with
    :type bootloader_blepp_characteristic_handle: ``int``
    :return: the characteristic declaration of the gatt table that match the handle and the service containing it.
        or None for both in all situations
    :rtype: ``tuple[BleAttribute|None,BleService|None]``
    """
    for service in application_gatt_table:
        if service.handle == bootloader_blepp_characteristic_handle:
            return None, None
        # end if
        for characteristic in service.characteristics:
            if characteristic.handle == bootloader_blepp_characteristic_handle:
                return None, None
            elif characteristic.declaration.handle == bootloader_blepp_characteristic_handle:
                return characteristic.declaration, service
            # end if
            for descriptor in characteristic.descriptors:
                if descriptor.handle == bootloader_blepp_characteristic_handle:
                    return None, None
                # end if
            # end for
        # end for
    # end for
    return None, None
# end def _extract_matching_handle

class GattSmallServicesRobustnessTestCase(GattSmallServiceApplicationTestCase):
    """
    Gatt small services Robustness test cases
    """

    @features('BLEProtocol')
    @features('Feature0007')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def _test_device_name_change_with_0007_sizes(self):
        """
        TODO : Skipped while issue https://jira.logitech.io/browse/BT-438 is open. Enable when it is resolved.
        Verify the GAP Service Device Name characteristic is changed using feature 0x0007 with several name sizes
        """
        name_base = STRING_TO_CUT
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get Feature 0x0007")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0007_index, self.feature_0007, _, _ = DeviceFriendlyNameTestUtils.HIDppHelper.get_parameters(
            self,
            DeviceFriendlyName.FEATURE_ID,
            DeviceFriendlyNameFactory)

        gap_service = BleUuid(BleUuidStandardService.GENERIC_ACCESS)
        device_name_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Compute a set of lengths between 1 and 14 to test")
        # --------------------------------------------------------------------------------------------------------------
        lengths = choices(range(1, 14), elem_nb=5)
        lengths += 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_name = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=gap_service,
                                                                            characteristic_uuid=device_name_char)[0]

        LogHelper.log_info(self, f"Name read: {original_name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over samples lengths of the name in valid range sampled between 1 and 14:'
                  f'{lengths}%')
        # --------------------------------------------------------------------------------------------------------------
        previous_name = original_name
        for length in lengths:
            new_name_to_set = name_base[:length]
            LogHelper.log_info(self, f"new name to set '{new_name_to_set}', length={length}'")
            DeviceFriendlyNameTestUtils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(
                self, byte_index=0, name_chunk=new_name_to_set)
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
            # --------------------------------------------------------------------------------------------------------------
            new_name_read = BleProtocolTestUtils.read_characteristics_as_string(
                test_case=self, ble_context_device=self.current_ble_device, service_uuid=gap_service, 
                characteristic_uuid=device_name_char)[0]
            LogHelper.log_info(self, f"Name read: {new_name_read}")
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check it's the new name")
            # --------------------------------------------------------------------------------------------------------------
            self.assertNotEqual(
                unexpected=previous_name, obtained=new_name_read,
                msg="Current Name in the GAP service is still the old one after writing with feature 0x0007")
            self.assertEqual(expected=new_name_to_set,
                             obtained=new_name_read,
                             msg="Current Name in the GAP service doesn't match with name set with feature 0x0007")
            previous_name = new_name_to_set
        # end for
        self.testCaseChecked("ROB_BLE_GATT_SSRV_0001", _AUTHOR)
    # end def _test_device_name_change_with_0007_sizes
    
    @features('BLEProtocol')
    @features('Feature1807')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_device_name_change_with_1807_sizes(self):
        """
        Verify the GAP Service Device Name characteristic is changed using feature 0x1807 with several name sizes
        """
        name_base = STRING_TO_CUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get Feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1807_index, self.feature_1807, _, _ = ConfigurablePropertiesTestUtils.HIDppHelper.get_parameters(
            test_case=self,
            feature_id=ConfigurableProperties.FEATURE_ID,
            factory=ConfigurablePropertiesFactory)

        gap_service = BleUuid(BleUuidStandardService.GENERIC_ACCESS)
        device_name_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Compute a set of lengths between 1 and 14 to test")
        # --------------------------------------------------------------------------------------------------------------
        lengths = choices(range(1, 15), elem_nb=5)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_name = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=gap_service,
                                                                            characteristic_uuid=device_name_char)[0]

        LogHelper.log_info(self, f"Name read: {original_name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over samples lengths of the name in valid range sampled between 1 and 14:'
                  f'{lengths}%')
        # --------------------------------------------------------------------------------------------------------------
        previous_name = original_name
        for length in lengths:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Enable manufacturing features")
            # --------------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            new_name_to_set = name_base[:length]
            LogHelper.log_info(self, f"new name to set '{new_name_to_set}', length={length}'")
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Change name with with HID++ feature 0x1807")
            # --------------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.select_property(
                self, ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
            ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, HexList.fromString(new_name_to_set))
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reset device")
            # --------------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ResetHelper.hidpp_reset(self)

            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
            # --------------------------------------------------------------------------------------------------------------
            new_name_read = BleProtocolTestUtils.read_characteristics_as_string(
                test_case=self, ble_context_device=self.current_ble_device, service_uuid=gap_service, 
                characteristic_uuid=device_name_char)[0]
            LogHelper.log_info(self, f"Name read: {new_name_read}")
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check it's the new name")
            # --------------------------------------------------------------------------------------------------------------
            self.assertNotEqual(
                unexpected=previous_name, obtained=new_name_read,
                msg="Current Name in the GAP service is still the old one after writing with feature 0x1807")
            self.assertEqual(expected=new_name_to_set,
                             obtained=new_name_read,
                             msg="Current Name in the GAP service doesn't match with name set with feature 0x1807")
            previous_name = new_name_to_set
        # end for
        self.testCaseChecked("ROB_BLE_GATT_SSRV_0002", _AUTHOR)
    # end def test_device_name_change_with_1807_sizes

    @features('BLEProtocol')
    @features('BootloaderBLESupport')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_hids_handle_conflict(self):
        """
        Verify that the handle of BLEPP characteristic declaration in bootloader doesn't match the handle of a HIDS
        characteristic declaration in application as this causes an issue on MacOs Catalina and Big Sur
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the application GATT table")
        # --------------------------------------------------------------------------------------------------------------
        application_gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Open device in BLE bootloader mode")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=True)
        self.post_requisite_restart_in_main_application = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the bootloader GATT table")
        # --------------------------------------------------------------------------------------------------------------
        bootloader_gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there is no conflict with the bootloader "
                                  "blepp characteristic declaration handle")
        LogHelper.log_info(self, f"application gatt table:\n"
                                 f"{BleProtocolTestUtils.gatt_table_to_string_with_handles(application_gatt_table)}")
        LogHelper.log_info(self, f"bootloader gatt table:\n"
                                 f"{BleProtocolTestUtils.gatt_table_to_string_with_handles(bootloader_gatt_table)}")
        # --------------------------------------------------------------------------------------------------------------
        bootloader_blepp_service = BleProtocolTestUtils.get_service_in_gatt(
            bootloader_gatt_table, BleProtocolTestUtils.build_128_bits_uuid(
                LogitechVendorUuid.BOOTLOADER_SERVICE))
        bootloader_blepp_characteristic = bootloader_blepp_service.characteristics[0]
        bootloader_blepp_characteristic_handle = bootloader_blepp_characteristic.declaration.handle

        # look if matching characteristics is a characteristic declaration
        application_matching_handle, application_matching_service = _extract_matching_handle(
            application_gatt_table, bootloader_blepp_characteristic_handle)

        if application_matching_handle is None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "handle matching is not a characteristic declaration, no conflict possible")
            # ----------------------------------------------------------------------------------------------------------
            return
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "handle matching is a characteristic declaration")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE),
                            obtained=application_matching_service.uuid,
                            msg="The blepp characteristic in bootloader shares its declaration handle with a "
                                "declaration handle in the HIDS service.\n"
                                "This can cause issues with Catalina and Big Sur")

        self.testCaseChecked("ROB_BLE_GATT_SSRV_0003", _AUTHOR)
    # end def test_blepp_hids_handle_conflict

    @features('BLEProtocol')
    @features('Rechargeable')
    @features('USBCharging')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    @services('Rechargeable')
    @services('ChargingWithoutConnection')
    def test_battery_notification_on_charge_event(self):
        battery_service = BleUuid(BleUuidStandardService.BATTERY_SERVICE)
        battery_level_characteristic = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Subscribe to the battery level notification")
        # --------------------------------------------------------------------------------------------------------------
        self._subscribe_characteristic(battery_service, battery_level_characteristic)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Clean battery notification")
        # --------------------------------------------------------------------------------------------------------------
        initial_state_of_charge = 0
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            LogHelper.log_info(self, "Initial notification received with battery level "
                                     f"= {to_int(ble_notification.data)}")
        except queue.Empty:
            pass
        # end try
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start charging the device without change in state of charge")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(self)
        self.post_charge_mode = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check a notification is received")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            state_of_charge = to_int(ble_notification.data)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"State of charge = {state_of_charge}%")
            # ----------------------------------------------------------------------------------------------------------
        except queue.Empty:
            self.fail(msg=f"no notification received when entering charge mode")
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop charging the device without change in state of charge")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.exit_charging_mode(self)
        self.post_charge_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check a notification is received")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            state_of_charge = to_int(ble_notification.data)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"State of charge = {state_of_charge}%")
            # ----------------------------------------------------------------------------------------------------------
        except queue.Empty:
            self.fail(msg=f"No notification received when exiting charge mode")
        # end try
    # end def test_battery_notification_on_charge_event
# end class GattSmallServicesRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
