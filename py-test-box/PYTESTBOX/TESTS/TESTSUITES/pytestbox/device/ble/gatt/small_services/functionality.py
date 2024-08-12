#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------------------------
# Python Test Box
# --------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.small_services
:brief: Validate Gatt small services Functionality test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2022/07/22
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
from pylibrary.tools.threadutils import QueueEmpty
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceAdvertisingTestCases
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceApplicationTestCase
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytransport.ble.bleconstants import BleAdvertisingDataType
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.transportcontext import TransportContextException

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattSmallServicesApplicationFunctionalityTestCase(GattSmallServiceApplicationTestCase):
    """
    Gatt Small Services Application mode Functionality Test Cases
    """

    @features('BLEProtocol')
    @features('Feature0007')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def _test_device_name_change_with_0007(self):
        """
        skipped while issue https://jira.logitech.io/browse/BT-438 is open
        Verify that the GAP Service Device Name characteristic value is changed using the feature 0x0007
        """

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
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_name = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=gap_service,
                                                                            characteristic_uuid=device_name_char)[0]

        LogHelper.log_info(self, f"Name read: {original_name}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate a different name from the read name")
        # --------------------------------------------------------------------------------------------------------------
        new_name_to_set = original_name.swapcase()
        LogHelper.log_info(self, f"New name to set: {new_name_to_set}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change name with with HID++ feature 0x0007")
        # --------------------------------------------------------------------------------------------------------------
        response = DeviceFriendlyNameTestUtils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(
            self, byte_index=0, name_chunk=new_name_to_set)
        LogHelper.log_info(self, f"SetFriendlyName response: {response}")

        friendly_name = DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(self, byte_index=0)
        LogHelper.log_info(self, f"Name read with 0x0007: {friendly_name}")

        DeviceBaseTestUtils.ResetHelper.hidpp_reset(self)
        self.current_channel.open()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        new_name_read = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=gap_service,
                                                                            characteristic_uuid=device_name_char)[0]

        LogHelper.log_info(self, f"Name read: {new_name_read}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check it's the new name")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=original_name,
                            obtained=new_name_read,
                            msg="Current Name in the GAP service is still the old one after writing with feature 0x0007")
        self.assertEqual(expected=new_name_to_set,
                         obtained=new_name_read,
                         msg="Current Name in the GAP service doesn't match with name set with feature 0x0007")

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0002", _AUTHOR)
    # end def _test_device_name_change_with_0007

    @features('BLEProtocol')
    @features('Feature1807')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_device_name_change_with_1807(self):
        """
        Verify that the GAP Service Device Name characteristic value is changed using the feature 0x1807
        """
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
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_name = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=gap_service,
                                                                            characteristic_uuid=device_name_char)[0]

        LogHelper.log_info(self, f"Name read: {original_name}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate a different name from the read name")
        # --------------------------------------------------------------------------------------------------------------
        new_name_to_set = original_name.swapcase()
        LogHelper.log_info(self, f"New name to set: {new_name_to_set}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change name with with HID++ feature 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self,
                                                                    ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
        ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, HexList.fromString(new_name_to_set))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset device")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        new_name_read = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=gap_service,
                                                                            characteristic_uuid=device_name_char)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check it's the new name")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=original_name,
                            obtained=new_name_read,
                            msg="Current Name in the GAP service is still the old one after writing with feature 0x1807")
        self.assertEqual(expected=new_name_to_set,
                         obtained=new_name_read,
                         msg="Current Name in the GAP service doesn't match with name set with feature 0x1807")

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0003", _AUTHOR)
    # end def test_device_name_change_with_1807

    @features('BLEProtocol')
    @features('Feature0007')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def _test_device_name_characteristic_write(self):
        """
        skipped while issue https://jira.logitech.io/browse/BT-438 is open
        Verify that the GAP Service Device Name characteristic value is not changed when written over through BLE
        """
        gap_service = BleUuid(BleUuidStandardService.GENERIC_ACCESS)
        device_name_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        original_name = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=gap_service,
                                                                            characteristic_uuid=device_name_char)[0]

        LogHelper.log_info(self, f"Name read: {original_name}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate a different name from the read name")
        # --------------------------------------------------------------------------------------------------------------
        new_name_to_set = original_name.swapcase()
        LogHelper.log_info(self, f"New name to set: {new_name_to_set}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write on the Service Device Name characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=gap_service, characteristic_uuid=device_name_char,
                                                  value=HexList.fromString(new_name_to_set))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        new_name_read = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                            ble_context_device=self.current_ble_device,
                                                                            service_uuid=gap_service,
                                                                            characteristic_uuid=device_name_char)[0]

        LogHelper.log_info(self, f"Name read: {new_name_read}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check it's still the original name")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=new_name_to_set,
                            obtained=new_name_read,
                            msg="Current Name in the GAP service is the one that was written and should have been ignored")

        self.assertEqual(expected=original_name,
                         obtained=new_name_read,
                         msg="Current Name in the GAP service doesn't match the original name")

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0004", _AUTHOR)
    # end def _test_device_name_characteristic_write

    @features('BLEProtocol')
    @features('BLEProV2')
    @features('BootloaderBLESupport')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_service_changed_indication(self):
        """
        Verify the service changed indication is sent when switching to bootloader
        """
        generic_attribute_uuid = BleUuid(BleUuidStandardService.GENERIC_ATTRIBUTE)
        service_changed_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.SERVICE_CHANGED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the whole GATT table")
        # --------------------------------------------------------------------------------------------------------------
        application_gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Subscribe to the indication of the Service Changed Characteristic")
        # --------------------------------------------------------------------------------------------------------------

        self._subscribe_characteristic(generic_attribute_uuid,
                                       service_changed_uuid,
                                       application_gatt_table)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch on bootloader and reconnect")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=True)
        self.post_requisite_restart_in_main_application = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the whole GATT table")
        # --------------------------------------------------------------------------------------------------------------
        bootloader_gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check an indication is received on the Service Changed characteristic")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.indications_queues[(generic_attribute_uuid, service_changed_uuid)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
        except queue.Empty:
            self.fail(msg="No indication received in time")
        # end try
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the value in the indication contain the expected range")
        # --------------------------------------------------------------------------------------------------------------

        start_of_affected_range = to_int(ble_notification.data[0:2], little_endian=True)
        end_of_affected_range = to_int(ble_notification.data[2:4], little_endian=True)

        first_two_uuid_application = [service.uuid for service in application_gatt_table[:2]]
        first_two_uuid_bootloader = [service.uuid for service in bootloader_gatt_table[:2]]
        gap_and_gatt = [BleUuid(BleUuidStandardService.GENERIC_ACCESS),
                        BleUuid(BleUuidStandardService.GENERIC_ATTRIBUTE)]

        if first_two_uuid_application == gap_and_gatt and first_two_uuid_bootloader == gap_and_gatt:
            # if Gap and Gatt are the first two handles, the third handle is an acceptable value
            third_handle = bootloader_gatt_table[2].handle
            self.assertIn(start_of_affected_range,
                          [0x0001, third_handle],
                          msg="Start of affected range is not 0x0001 or the first handle after the GAP and GATT"
                              " when GAP and GATT are listed first")
        else:
            # otherwise start of affected range should be 0x0001
            self.assertEqual(expected=0x0001,
                             obtained=start_of_affected_range,
                             msg="Start of affected range is not 0x0001 when GAP and GATT are not listed first")
        # end if

        self.assertIn(member=end_of_affected_range,
                      container=[0xFFFF, bootloader_gatt_table[-1].handle],
                      msg="End of affected range is not 0xFFFF or the last handle of the last service")

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0006", _AUTHOR)
    # end def test_service_changed_indication

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @services('PowerSupply')
    def test_battery_level_notification(self):
        """
        Verify the battery level notification is sent when power diminishes :
        """
        battery_service = BleUuid(BleUuidStandardService.BATTERY_SERVICE)
        battery_level_characteristic = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Subscribe to the notification of the Battery Level characteristic")
        # --------------------------------------------------------------------------------------------------------------
        self._subscribe_characteristic(battery_service, battery_level_characteristic)

        step = self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_StateOfChargeStep
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            LogHelper.log_info(self, f"initial battery level = {to_int(ble_notification.data)}")
        except queue.Empty:
            ble_notification = BleProtocolTestUtils.read_characteristics(
                self, self.current_ble_device, BleUuid(BleUuidStandardService.BATTERY_SERVICE),
                BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL))[0]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"No notification received at startup, "
                                     f"{ble_notification}% read on the battery service characteristic")
            # ----------------------------------------------------------------------------------------------------------
        # end try

        initial_state_of_charge = to_int(ble_notification.data) - to_int(ble_notification.data) % step
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check that the initial state of charge is sufficiently higher than the "
                                 "critical state of charge, so can be lowered")
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(a=initial_state_of_charge-step, b=critical_state_of_charge,
                           msg="Initial state of charge is lower or equal to critical state of charge")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to lower the battery state of charge step by step")
        # --------------------------------------------------------------------------------------------------------------
        for state_of_charge in range(initial_state_of_charge - step, critical_state_of_charge, -step):
            battery_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set battery_voltage at {state_of_charge}% = {battery_voltage}v")
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_voltage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that a notification is received on this characteristic")
            # ----------------------------------------------------------------------------------------------------------
            if self.f.PRODUCT.F_IsGaming:
                ble_notification = None
                while True:
                    try:
                        ble_notification = self.notifications_queues[
                            (battery_service, battery_level_characteristic)].get(
                            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
                    except QueueEmpty:
                        break
                    # end try
                # end while
                assert ble_notification is not None, "No notification received"

                ble_notification.data = HexList(UnifiedBatteryTestUtils.adapt_soc(
                    test_case=self, input_soc=ble_notification.data, expected_soc=state_of_charge))

                LogHelper.log_info(self,
                                   f"battery_level at {state_of_charge}% =  {to_int(ble_notification.data)}")
                self.assertEqual(
                    expected=state_of_charge, obtained=to_int(ble_notification.data),
                    msg="level value received as battery notification is different from the expected one")
            else:
                for retry in range(2):
                    try:
                        ble_notification = (
                            self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                                timeout=UnifiedBatteryTestUtils.PWS_BATTERY_SOC_UPDATE_TIME))
                        LogHelper.log_info(
                            self, f"battery_level at {state_of_charge}% =  {to_int(ble_notification.data)}")
                        self.assertEqual(
                            expected=state_of_charge, obtained=to_int(ble_notification.data),
                            msg="level value received as battery notification is different from the expected one")
                        # end if
                        break
                    except queue.Empty:
                        if retry > 0:
                            self.fail(msg=f"No notification received when soc = {state_of_charge} after 2 retries")
                        else:
                            int_battery_voltage_mv = int(battery_voltage * UnifiedBatteryTestUtils.V_UNIT_CONVERT)
                            reduce_batt_voltage = round((int_battery_voltage_mv - 5) /
                                                        UnifiedBatteryTestUtils.V_UNIT_CONVERT,
                                                        PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS)
                            # ------------------------------------------------------------------------------------------
                            LogHelper.log_info(
                                self, f"Reduce battery_voltage 5mV at {state_of_charge}% = {reduce_batt_voltage}v")
                            # ------------------------------------------------------------------------------------------
                            self.power_supply_emulator.set_voltage(reduce_batt_voltage)
                        # end if
                    # end try
                # end for
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0007", _AUTHOR)
    # end def test_battery_level_notification

    @features('BLEProtocol')
    @features('Rechargeable')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @services('PowerSupply')
    @services('Rechargeable')
    @services('ChargingWithoutConnection')
    def test_battery_level_notification_charge(self):
        """
        Verify the battery level notification is sent when power raises
        """
        battery_service = BleUuid(BleUuidStandardService.BATTERY_SERVICE)
        battery_level_characteristic = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL)

        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        full_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'full')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Restart the device with input voltage to CRITICAL level "
                                         "and a state_of_charge of {battery_critical}%")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, starting_voltage=battery_critical, cleanup_battery_event=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Subscribe to the notification of the Battery Level characteristic")
        # --------------------------------------------------------------------------------------------------------------
        self._subscribe_characteristic(battery_service, battery_level_characteristic)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean battery notification queue")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            initial_state_of_charge = to_int(ble_notification.data)
            LogHelper.log_info(self, f"initial battery level = {initial_state_of_charge}")
        except queue.Empty:
            initial_state_of_charge = BleProtocolTestUtils.read_characteristics(
                self, self.current_ble_device, BleUuid(BleUuidStandardService.BATTERY_SERVICE),
                BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"No notification received at startup, "
                                     f"{initial_state_of_charge}% read on the battery service characteristic")
            # ----------------------------------------------------------------------------------------------------------
        # end try

        step = self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_StateOfChargeStep

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enter charging mode")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.ChargingHelper.enter_charging_mode(self)
        self.post_charge_mode = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "get the notification triggered by connecting the charge")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            LogHelper.log_info(self, f"initial battery level = {to_int(ble_notification.data)}")
            initial_state_of_charge = to_int(ble_notification.data)
        except queue.Empty:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "No notification after connecting charging cable")
            # ----------------------------------------------------------------------------------------------------------
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop to raise the battery state of charge step by step")
        # --------------------------------------------------------------------------------------------------------------
        for state_of_charge in range(initial_state_of_charge+step, full_state_of_charge, step):
            battery_voltage = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, state_of_charge,
                                                                                     discharge=False)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set battery_voltage at {state_of_charge}% or {battery_voltage}V")
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(battery_voltage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that a notification is received on this characteristic")
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.wait_soc_computation(self)
            try:
                battery_status_event = UnifiedBatteryTestUtils.wait_for_battery_status_event(
                    self, timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
                if self.f.PRODUCT.F_IsGaming:
                    for index in range(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_StateOfChargeStep, 0, -1):
                        ble_notification = self.notifications_queues[
                            (battery_service, battery_level_characteristic)].get(
                            timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
                        LogHelper.log_info(self,
                                           f"battery_level at {state_of_charge}% =  {to_int(ble_notification.data)}")
                        self.assertEqual(expected=state_of_charge + index - 1,
                                         obtained=to_int(ble_notification.data),
                                         msg="level value received as battery notification is different from the "
                                             "expected "
                                             "one")
                    # end for
                else:
                    ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                        timeout=UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
                    LogHelper.log_info(self, f"battery_level at {state_of_charge}% =  {to_int(ble_notification.data)}")
                    self.assertEqual(expected=state_of_charge, obtained=to_int(ble_notification.data),
                                     msg="level value received as battery notification is different from the expected "
                                         "one")
                # end if
            except queue.Empty:
                battery_level = BleProtocolTestUtils.read_characteristics(
                    self, self.current_ble_device, BleUuid(BleUuidStandardService.BATTERY_SERVICE, ),
                    BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL))[0].data

                get_status_response = UnifiedBatteryTestUtils.HIDppHelper.get_status(self)
                self.fail(msg=f"No notification received when soc = {state_of_charge}, "
                              f"reading the characteristic gives ={battery_level.toLong()}, "
                              f"1004 status = {get_status_response}")
            # end try
            break
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0009", _AUTHOR)
    # end def test_battery_level_notification_charge

    @features('BAS1.0+')
    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_battery_level_notification_on_reconnection(self):
        """
        Verify the battery level notification is sent upon a reconnection of a bounded central
        """
        battery_service = BleUuid(BleUuidStandardService.BATTERY_SERVICE)
        battery_level_characteristic = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL)
        battery_level_status_characteristic = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL_STATUS)

        gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)

        characteristics_to_use = [battery_level_characteristic]
        if self.hasFeature("BAS1.1"):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Subscribe to the notification of the Battery Level and Battery Level Status"
                                     " characteristic")
            # ----------------------------------------------------------------------------------------------------------
            characteristics_to_use.append(battery_level_status_characteristic)
        else:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Subscribe to the notification of the Battery Level characteristic")
            # --------------------------------------------------------------------------------------------------------------
        # end if

        for characteristic in characteristics_to_use:
            self._subscribe_characteristic(battery_service, characteristic, gatt_table)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean notification queue")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            LogHelper.log_info(self, f"initial battery level = {to_int(ble_notification.data)}")
        except queue.Empty:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "No notification received at startup")
            # ----------------------------------------------------------------------------------------------------------
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disconnect from device")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.disconnect_device(self, self.current_ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reconnect to the device without encrypting")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        BleProtocolTestUtils.connect_no_encryption(self, self.current_ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that no notification is received on this characteristic")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            self.fail(msg="Notification received after reconnection but before encryption")
        except queue.Empty:
            pass  # expected result
        # end try
        
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Encrypt connection")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.encrypt_connection(self, self.current_ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a notification is received on this characteristic")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            LogHelper.log_info(self, f"battery level = {to_int(ble_notification.data)}")
        except queue.Empty:
            self.fail(msg="No notification received on reconnection encryption")
        # end try

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0010", _AUTHOR)
    # end def test_battery_level_notification_on_reconnection

    @features('BAS1.0+')
    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_battery_notification_on_cccd_write(self):
        """
        Verify the battery level notification is not sent upon write on the CCCDs
        Note: Previous versions of the specification required the notification to be sent,
                this use case implementation tests that the fix is correctly propagated
        """
        battery_service = BleUuid(BleUuidStandardService.BATTERY_SERVICE)
        battery_level_characteristic = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL)
        battery_level_status_characteristic = BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL_STATUS)

        ble_context = BleProtocolTestUtils.get_ble_context(self)
        characteristics_to_use = [battery_level_characteristic]
        if self.hasFeature("BAS1.1"):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Subscribe to the notification of the Battery Level and Battery Level Status"
                                     " characteristic")
            # ----------------------------------------------------------------------------------------------------------
            characteristics_to_use.append(battery_level_status_characteristic)
        else:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Subscribe to the notification of the Battery Level characteristic")
            # --------------------------------------------------------------------------------------------------------------
        # end if

        for characteristic in characteristics_to_use:
            self._subscribe_characteristic(battery_service, characteristic)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check initial notification is received")
        # --------------------------------------------------------------------------------------------------------------

        for characteristic in characteristics_to_use:
            try:

                ble_notification = self.notifications_queues[(battery_service, characteristic)].get(
                    timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
                LogHelper.log_info(self, f"data on {characteristic} = {to_int(ble_notification.data)}")
                self.fail(msg=f"Notification received at startup for characteristic {characteristic}, "
                              "this is not compatible with June 2024 version of the specification")
            except queue.Empty:
                pass
            # end try
        # end for


        for characteristic in characteristics_to_use:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Rewrite enabling the notification on characteristic {characteristic}")
            # --------------------------------------------------------------------------------------------------------------
            characteristic = ble_context.get_service(self.current_ble_device, battery_service).get_characteristics(
                battery_level_characteristic)[0]

            try:
                ble_context.write_on_cccd_notification(
                    self.current_ble_device, characteristic=characteristic, enabled=True)
            except TransportContextException as e:
                self.fail(f"Transport exception when trying to rewrite on CCCDs.\n Cause={e.get_cause()}")
            # end try

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check initial notification is received after rewriting on CCCDs "
                                      "characteristic {characteristic}")
            # ----------------------------------------------------------------------------------------------------------

            try:
                ble_notification = self.notifications_queues[(battery_service, battery_level_characteristic)].get(
                    timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
                LogHelper.log_info(self, f"battery level = {to_int(ble_notification.data)}")
                self.fail(msg=f"Notification received on rewrite for characteristic {characteristic}, "
                              "this is not compatible with June 2024 version of the specification")
            except queue.Empty:
                pass
            # end try
        # end for
        self.testCaseChecked("FUN_BLE_GATT_SSRV_0011", _AUTHOR)
    # end def test_battery_notification_on_cccd_write

    @features('BLEProtocol')
    @features('Feature0003')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_exchange(self):
        """
        Verify blepp communication is possible
        """
        blepp_service = BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_SERVICE)
        hidpp_characteristic = BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_CHARACTERISTIC)

        self._get_feature_0003_index()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Subscribe to the HID++ In/Out characteristic")
        # --------------------------------------------------------------------------------------------------------------
        self._subscribe_characteristic(blepp_service, hidpp_characteristic)

        self._check_hidpp_communication_enabled(
            blepp_service=blepp_service,
            hidpp_characteristic=hidpp_characteristic
        )
        self.testCaseChecked("FUN_BLE_GATT_SSRV_0008", _AUTHOR)
    # end def test_blepp_exchange
# end class GattSmallServicesApplicationFunctionalityTestCase


class GattSmallServicesAdvertisingFunctionalityTestCase(GattSmallServiceAdvertisingTestCases):
    """
    Gatt Small Services Advertising Functionality Test Cases
    """

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_name_in_advertising_and_gatt_table(self):
        """
        Verify the name is the same in advertising and the GATT table
        """
        gap_service = BleUuid(BleUuidStandardService.GENERIC_ACCESS)
        device_name_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Complete_Name field in scan response")
        # --------------------------------------------------------------------------------------------------------------
        self.current_ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self,
                                                                               scan_timeout=2,
                                                                               send_scan_request=True,
                                                                               force_scan_for_all_timeout=True)
        scan_name = None
        # find complete name  in one of the scan response packet
        for data in self.current_ble_device.scan_response:
            if BleAdvertisingDataType.COMPLETE_LOCAL_NAME in data.records.keys():
                scan_name = HexList(data.records[BleAdvertisingDataType.COMPLETE_LOCAL_NAME]).toString()
                break
            # end if
        # end for
        self.assertIsNotNone(scan_name, "No complete local name found in scan response data")
        LogHelper.log_info(self, f"Name read: {scan_name}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(self, self.current_ble_device)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get GAP Service Device Name characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        gap_name = BleProtocolTestUtils.read_characteristics_as_string(test_case=self,
                                                                       ble_context_device=self.current_ble_device,
                                                                       service_uuid=gap_service,
                                                                       characteristic_uuid=device_name_char)[0]

        LogHelper.log_info(self, f"Name read: {gap_name}")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check both obtained values are identical")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=scan_name,
                         obtained=gap_name,
                         msg="The name read from the GAP service doesn't match the name during advertisement")

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0001", author=_AUTHOR)
    # end def test_name_in_advertising_and_gatt_table

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_appearance_in_advertising_and_gatt_table(self):
        """
        Verify the appearance value is the same in advertising and the GATT table
        """
        gap_service = BleUuid(BleUuidStandardService.GENERIC_ACCESS)
        device_appearance_char = BleUuid(BleUuidStandardCharacteristicAndObjectType.APPEARANCE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get appearance field in scan response")
        # --------------------------------------------------------------------------------------------------------------
        self.current_ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self,
                                                                               scan_timeout=2.5,
                                                                               send_scan_request=True,
                                                                               force_scan_for_all_timeout=True)
        scanned_appearance = None
        # find appareance in one of the advertising packet
        for data in self.current_ble_device.advertising_data:
            if BleAdvertisingDataType.APPEARANCE in data.records.keys():
                scanned_appearance = HexList(data.records[BleAdvertisingDataType.APPEARANCE])
                break
            # end if
        # end for
        self.assertIsNotNone(scanned_appearance, "No appearance found in advertisement data")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(self, self.current_ble_device)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get GAP Appearance characteristic value")
        # --------------------------------------------------------------------------------------------------------------
        gap_appearance = BleProtocolTestUtils.read_characteristics(test_case=self,
                                                                   ble_context_device=self.current_ble_device,
                                                                   service_uuid=gap_service,
                                                                   characteristic_uuid=device_appearance_char)[0].data

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check both obtained values are identical")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=scanned_appearance,
                         obtained=gap_appearance,
                         msg="The name read from the GAP service doesn't match the name during advertisement")

        self.testCaseChecked("FUN_BLE_GATT_SSRV_0005")
    # end def test_appearance_in_advertising_and_gatt_table
# end class GattSmallServicesAdvertisingFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
