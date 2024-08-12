#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.hids.functionality
:brief: Validate BLE GATT human interface device service functionality test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/03/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import queue

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.logiconstants import LogitechBleConstants
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.blereportmap import HidReportConsumerGenericWithChromeOSDescriptor
from pyhid.hid.blereportmap import HidReportConsumerGenericWithoutChromeOSDescriptor
from pyhid.hid.blereportmap import HidReportConsumerMinimumDescriptor
from pyhid.hid.blereportmap import HidReportConsumerMinimumDescriptorOptimizedInput
from pyhid.hid.blereportmap import HidReportHidppLongReportDescriptor
from pyhid.hid.blereportmap import HidReportHidppLongReportDescriptorLegacy
from pyhid.hid.blereportmap import HidReportKeyboardLedDescriptor
from pyhid.hid.blereportmap import HidReportKeyboardLedTopRowDescriptor
from pyhid.hid.blereportmap import HidReportMouse12Descriptor
from pyhid.hid.blereportmap import HidReportMouse16Descriptor
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.interfacedescriptors import GenericDesktopCallStateControlKeyDescriptor
from pyhid.hid.interfacedescriptors import GenericDesktopSystemControlDescriptorKeyboard
from pyhid.hid.usbhidusagetable import ConsumerHidUsage
from pyhid.hid.usbhidusagetable import format_consumer_usage_to_report_entry
from pyhid.hiddata import HidData
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import ReportReferences
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.ble.gatt.hids.hids import GattHIDSApplicationTestCases
from pytestbox.device.ble.gatt.hids.hids import GattHIDSBootloaderTestCases
from pytestbox.device.ble.gatt.hids.hids import GattHIDSTestCases
from pytestbox.device.hidpp20.common.feature_1806.business import LogHelper
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.blemessage import BleMessage

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# source https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/edit#gid=1276721922
# note: mapping not exhaustive
KEY_TO_OS = {
    KEY_ID.KEYBOARD_VOLUME_UP: BleNvsChunks.OsDetectedType.UNKNOWN,
    KEY_ID.KEYBOARD_VOLUME_DOWN: BleNvsChunks.OsDetectedType.UNKNOWN,
    KEY_ID.CALCULATOR: BleNvsChunks.OsDetectedType.UNKNOWN,
    KEY_ID.MULTI_PLATF_SEARCH_SPOTLIGHT: BleNvsChunks.OsDetectedType.UNKNOWN,
    KEY_ID.KEYBOARD_HOME: BleNvsChunks.OsDetectedType.UNKNOWN,
    KEY_ID.EMOJI_PANEL: BleNvsChunks.OsDetectedType.CHROME
}

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class GattHIDSFunctionalityTestCasesMixin(GattHIDSTestCases):
    """
    BLE HIDS Functionality Test Cases Common class
    """

    def _report_map_matches(self):
        """
        Verify the report map matches the reports characteristics exposed in the HIDS
        """
        self._prerequisite_gatt_table()

        service_uuid = BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)
        hids_list = BleProtocolTestUtils.get_services_list_in_gatt(
            self.gatt_table, service_uuid)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop on all instances of the hid service")
        # --------------------------------------------------------------------------------------------------------------
        for hids in hids_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "List the reports exposed by the device")
            # ----------------------------------------------------------------------------------------------------------
            reports = hids.get_characteristics(BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT))
            reports_references = []
            for characteristic in reports:
                message = BleProtocolTestUtils.read_descriptor(
                    test_case=self, ble_context_device=self.ble_context_device_used,
                    characteristic=characteristic, descriptor_uuid=BleUuid(BleUuidStandardDescriptor.REPORT_REFERENCE))
                reports_references.append(message.data)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Build a report map from the reports found")
            # ----------------------------------------------------------------------------------------------------------
            reports_descriptors = []
            reports_descriptors_legacy = []

            if HexList("0101") in reports_references and HexList("0102") in reports_references:
                if HexList("0903") in reports_references:
                    count = int(self.f.PRODUCT.HID_REPORT.F_TopRowUsagesCount)
                    reports_descriptors.append(HidReportKeyboardLedTopRowDescriptor(
                        top_raw_report_count=HexList(0x95, count), top_raw_usage_maximum=HexList(0x29, count)))
                else:
                    reports_descriptors.append(HidReportKeyboardLedDescriptor())
                # end if
            # end if

            if HexList("0201") in reports_references:
                btn_count = 16
                reports_descriptors.append(HidReportMouse12Descriptor(button_report_count=HexList(0x95, btn_count),
                                                                      button_usage_maximum=HexList(0x29, btn_count),))
            # end if

            if HexList("1501") in reports_references:
                btn_count = 16
                reports_descriptors.append(HidReportMouse16Descriptor(button_report_count=HexList(0x95, btn_count),
                                                                      button_usage_maximum=HexList(0x29, btn_count),))
            # end if

            if HexList("0301") in reports_references:
                if self.f.PRODUCT.PROTOCOLS.BLE.F_ChromeSupport:
                    reports_descriptors.append(HidReportConsumerGenericWithChromeOSDescriptor())
                else:
                    reports_descriptors.append(HidReportConsumerGenericWithoutChromeOSDescriptor())
                # end if
            # end if

            if HexList("0401") in reports_references:
                reports_descriptors.append(GenericDesktopSystemControlDescriptorKeyboard())
            # end if

            if HexList("0B01") in reports_references:
                reports_descriptors.append(GenericDesktopCallStateControlKeyDescriptor())
            # end if

            if HexList("0501") in reports_references:
                usages = [format_consumer_usage_to_report_entry(usage) for usage
                          in self.f.PRODUCT.HID_REPORT.F_ProductSpecificUsages if usage != '']
                count = len(usages)
                if count % 8 == 0:
                    reports_descriptors.append(
                        HidReportConsumerMinimumDescriptorOptimizedInput(cons_min_report_count=HexList(0x95, count),
                                                                         cons_min_usage_list=HexList(usages)))
                else:
                    reserved_count = 8 - (count % 8)
                    reports_descriptors.append(
                        HidReportConsumerMinimumDescriptor(cons_min_report_count=HexList(0x95, count),
                                                           cons_min_rsv_count=HexList(0x95, reserved_count),
                                                           cons_min_usage_list=HexList(usages)))
                # end if
            # end if
            if HexList("1101") in reports_references and HexList("1102") in reports_references:
                reports_descriptors_legacy = reports_descriptors.copy()
                reports_descriptors.append(HidReportHidppLongReportDescriptor())
                reports_descriptors_legacy.append(HidReportHidppLongReportDescriptorLegacy())
            # end if

            report_map = HexList()
            for report_descriptor in reports_descriptors:
                descriptor = HexList(report_descriptor)
                report_map.extend(descriptor)
            # end for
            # create a second report map, with the old byte ordering of the hidpp report
            report_map_legacy = HexList()
            for report_descriptor in reports_descriptors_legacy:
                descriptor = HexList(report_descriptor)
                report_map_legacy.extend(descriptor)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Read the report map on the device")
            # ----------------------------------------------------------------------------------------------------------
            report_map_characteristic = hids.get_characteristics(
                characteristic_uuid=BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT_MAP))[0]
            report_map_read = self.ble_context.attribute_read(ble_context_device=self.ble_context_device_used,
                                                              attribute=report_map_characteristic).data

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the report maps match")
            # ----------------------------------------------------------------------------------------------------------
            self.assertIn(container=[report_map, report_map_legacy],
                          member=report_map_read,
                          msg="Report map built from existing reports and read from the "
                              "HIDS Report Map characteristic don't match")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test loop on all instances of the hid service")
        # --------------------------------------------------------------------------------------------------------------
    # end def _report_map_matches

    def _check_get_notification(self, notification_queue, count):
        """
        Check if notifications are received on a notification queue, up to the amount specified
        :param notification_queue: the queue to check
        :type notification_queue: ``queue``
        :param count: the amount of notification to expect
        :type count: ``int``
        :return: list of ble notification
        :rtype: ``list[BleMessage]``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check notification arrives {count}x time(s)")
        # --------------------------------------------------------------------------------------------------------------
        notifications = []

        for i in range(count):
            try:
                ble_notification = notification_queue.get(
                    timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
                notifications.append(ble_notification)
            except queue.Empty:
                self.fail(msg="No notification received in time")
            # end try
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"notification arrived {i}")
            # --------------------------------------------------------------------------------------------------------------
        # end for
        return notifications
    # end def _check_get_notification

    def _prerequisite_report_input_test(self, report_reference):
        """
        Prerequisite for an input report test.
        Get the whole gatt table
        Subscribe to all reports
        get the report notification queue from the report reference
        :param report_reference: The report reference
        :type report_reference: ``HexList``
        :return: the notification queue
        :rtype: ``queue``
        """
        self._prerequisite_gatt_table()
        self._prerequisite_subscribe_to_input_report()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get the notification queue for report "
                                         f"{report_reference}")
        # --------------------------------------------------------------------------------------------------------------
        notification_queue = self.notifications_queues.get(report_reference.toLong())
        self.assertNotNone(notification_queue, msg="Report not present")
        return notification_queue
    # end def _prerequisite_report_input_test

    def _prerequisite_change_os(self, os_wanted):
        """
        Prerequisite for a different OS simulated on host

        :param os_wanted: the os to emulate
        :type os_wanted: ``BleNvsChunks.OsDetectedType``
        """
        if os_wanted != BleNvsChunks.OsDetectedType.UNKNOWN:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, f"Change host os emulation to {os_wanted}")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.disconnect_ble_channel(test_case=self)
            BleProtocolTestUtils.change_host_os_emulation(test_case=self,
                                                          os_emulation_type=os_wanted)
            DeviceBaseTestUtils.enter_pairing_mode_ble(test_case=self)
            self.current_ble_device = BleProtocolTestUtils.scan_for_current_device(
                test_case=self, scan_timeout=2, send_scan_request=False)
            BleProtocolTestUtils.connect_and_bond_device(test_case=self, ble_context_device=self.current_ble_device)
        # end if
    # end def _prerequisite_change_os

    def _common_test_hidpp_reports(self):
        """
        Common testing method to check the HID++ reports
        """
        self._prerequisite_feature_0003_index()
        notification_queue = self._prerequisite_report_input_test(ReportReferences.HIDPP_INPUT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get HIDPP output report")
        # --------------------------------------------------------------------------------------------------------------
        output_report = self._get_report(ReportReferences.HIDPP_OUTPUT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write on HID++ feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        get_fw_info_report = self.feature_0003.get_fw_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index,
            entity_index=0)
        message = HexList(get_fw_info_report)[1:]
        message.addPadding(size=LogitechBleConstants.HIDPP_MESSAGE_SIZE, fromLeft=False)
        ble_message = BleMessage(data=message)
        self.ble_context.characteristic_write(self.current_ble_device, output_report, ble_message)

        self._check_get_notification(notification_queue=notification_queue, count=1)
    # end def _common_test_hidpp_reports

    def _common_test_hid_control_point(self):
        """
        Common testing method to check the hid control point characteristic
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "write suspend on HID control point characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE),
                                                  characteristic_uuid=BleUuid(
                                                      BleUuidStandardCharacteristicAndObjectType.HID_CONTROL_POINT),
                                                  value=HexList(0x00))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "write exit suspend on HID control point characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE),
                                                  characteristic_uuid=BleUuid(
                                                      BleUuidStandardCharacteristicAndObjectType.HID_CONTROL_POINT),
                                                  value=HexList(0x01))
    # end def _common_test_hid_control_point
# end class GattHIDSFunctionalityTestCasesMixin


class GattHIDSApplicationFunctionalityTestCase(GattHIDSFunctionalityTestCasesMixin, GattHIDSApplicationTestCases):
    """
    BLE HIDS Functionality Test Cases Application class
    """

    def setUp(self):
        # See GattHIDSFunctionTestCasesMixin.setUp
        GattHIDSApplicationTestCases.setUp(self)
    # end def setUp

    @staticmethod
    def product_specific_usage_to_key(usages_list):
        """
        Convert a list of HID usage from report descriptor to a list of key for those function for usages tha
        :param usages_list: list of string describing the usages
        :type usages_list: ``list[str]``
        :return: list of key ids that send the keycode wanted
        :rtype: ``list[KEY_ID]``
        """
        key_conv = []
        for usage in usages_list:
            if usage == '':
                continue
            # end if
            usage = ConsumerHidUsage.__dict__[usage]
            key_id = CID_TO_KEY_ID_MAP.get(usage)
            if key_id is not None:
                key_conv.append(key_id)
            # end if
        # end for
        return key_conv
    # end def product_specific_usage_to_key

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @bugtracker('BLE_Unsupported_Report_Map')
    def test_report_map(self):
        """
        Verify the report map and report characteristics matches
        """
        self._report_map_matches()

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0001", _AUTHOR)
    # end def test_report_map

    @features('BLEProtocol')
    @features('Mice')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_mouse_report(self):
        """
        Verify the mouse input report sends a notification on user action
        """
        notification_queue = self._prerequisite_report_input_test(ReportReferences.MOUSE_INPUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate an event that will be sent through the mouse input report")
        LogHelper.log_info(self, "click left button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.LEFT_BUTTON)

        self._check_get_notification(notification_queue, 2)

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0003", _AUTHOR)
    # end def test_mouse_report

    @features('BLEProtocol')
    @features('Keyboard')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    def test_keyboard_report(self):
        """
        Verify the keyboard input report sends a notification on user action
        """
        if self.f.PRODUCT.F_IsGaming:
            notification_queue = self._prerequisite_report_input_test(ReportReferences.GAMING_KEYBOARD_INPUT)
        else:
            notification_queue = self._prerequisite_report_input_test(ReportReferences.KEYBOARD_INPUT)
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate an event that will be sent through the keyboard input report")
        LogHelper.log_info(self, "keystroke key O")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_O)

        self._check_get_notification(notification_queue, 2)

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0004", _AUTHOR)
    # end def test_keyboard_report

    @features('BLEProtocol')
    @features('Keyboard')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @services('RequiredKeys', (KEY_ID.SCREEN_LOCK,))
    def test_generic_desktop_system_control_report_keyboard(self):
        """
        Verify the product generic desktop system control input report sends a notification on user action on keyboards
        """
        self._prerequisite_change_os(BleNvsChunks.OsDetectedType.CHROME)
        notification_queue = self._prerequisite_report_input_test(ReportReferences.GENERIC_DESKTOP_SYSTEM_CONTROL)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate an event that will be sent through "
                                 "the Generic Desktop System Control input report")
        LogHelper.log_info(self, "Keystroke on the screen lock button")
        # --------------------------------------------------------------------------------------------------------------
        if KEY_ID.SCREEN_LOCK in self.button_stimuli_emulator.get_fn_keys():
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            self.button_stimuli_emulator.keystroke(
                key_id=self.button_stimuli_emulator.get_fn_keys()[KEY_ID.SCREEN_LOCK])
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
        else:
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.SCREEN_LOCK)
        # end if

        self._check_get_notification(notification_queue, 2)

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0005", _AUTHOR)
    # end def test_generic_desktop_system_control_report_keyboard

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @services('RequiredKeys', (KEY_ID.MUTE_MICROPHONE,))
    def test_desktop_call_state_management_control_report_keyboard(self):
        """
        Verify the call state management consumer input report sends a notification on user action on keyboards
        """
        self._prerequisite_change_os(BleNvsChunks.OsDetectedType.CHROME)
        notification_queue = self._prerequisite_report_input_test(ReportReferences.DESKTOP_CALL_STATE_MANAGEMENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate an event that will be sent through "
                                 "the Desktop Call State Management Control input report")
        # --------------------------------------------------------------------------------------------------------------
        if KEY_ID.MUTE_MICROPHONE in self.button_stimuli_emulator.get_fn_keys():
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            self.button_stimuli_emulator.keystroke(
                key_id=self.button_stimuli_emulator.get_fn_keys()[KEY_ID.MUTE_MICROPHONE])
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
        else:
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.MUTE_MICROPHONE)
        # end if

        self._check_get_notification(notification_queue, 2)

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0006", _AUTHOR)
    # end def test_desktop_call_state_management_control_report_keyboard

    @features('BLEProtocol')
    @features('Keyboard')
    @features('NoGamingDevice')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_product_specific_consumer_report_keyboard(self):
        """
        Verify the product specific consumer input report sends a notification on user action on keyboards
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select a key to press based on the usages in the product descriptor")
        # --------------------------------------------------------------------------------------------------------------
        key_ids = self.product_specific_usage_to_key(self.f.PRODUCT.HID_REPORT.F_ProductSpecificUsages)
        key_id = None
        os = None
        for key in key_ids:
            if key in KEY_TO_OS.keys():
                key_id = key
                os = KEY_TO_OS[key]
                break
            # end if
        # end for

        self.assertNotNone(key_id, "No compatible keys to press")
        self._prerequisite_change_os(os)
        notification_queue = self._prerequisite_report_input_test(ReportReferences.PRODUCT_SPECIFIC_CONSUMER_INPUT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate an event that will be sent through the "
                                 "Product Specific Consumer input report")
        LogHelper.log_info(self, f"Keystroke on the key with id {key_id}")
        # --------------------------------------------------------------------------------------------------------------
        fn_keys = self.button_stimuli_emulator.get_fn_keys()
        if key_id in fn_keys.keys():
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            self.button_stimuli_emulator.keystroke(key_id=fn_keys[key_id])
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
        else:
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end if

        self._check_get_notification(notification_queue, 2)

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0007", _AUTHOR)
    # end def test_product_specific_consumer_report_keyboard

    @features('BLEProtocol')
    @features('Keyboard')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_led_report(self):
        """
        Verify the LED output report can be written without errors
        """
        self._prerequisite_gatt_table()
        if self.f.PRODUCT.F_IsGaming:
            led_report = self._get_report(ReportReferences.GAMING_LED_OUTPUT)
        else:
            led_report = self._get_report(ReportReferences.LED_OUTPUT)
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read the Led Output Report initial value")
        # --------------------------------------------------------------------------------------------------------------
        initial_value = self.ble_context.attribute_read(ble_context_device=self.ble_context_device_used,
                                                        attribute=led_report)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write to Boot Keyboard Output Report")
        # --------------------------------------------------------------------------------------------------------------
        value = initial_value.data ^ 0x02
        self.ble_context.characteristic_write(ble_context_device=self.ble_context_device_used,
                                              characteristic=led_report,
                                              data=BleMessage(data=value))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read the value back")
        # --------------------------------------------------------------------------------------------------------------
        read_value = self.ble_context.attribute_read(ble_context_device=self.ble_context_device_used,
                                                     attribute=led_report)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the write and read values matches")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=value, obtained=read_value.data, msg="The value written doesn't match")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write without response to the Boot Keyboard Output Report")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.characteristic_write_without_response(ble_context_device=self.ble_context_device_used,
                                                               characteristic=led_report,
                                                               data=initial_value)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read the value back")
        # --------------------------------------------------------------------------------------------------------------
        read_value = self.ble_context.attribute_read(ble_context_device=self.ble_context_device_used,
                                                     attribute=led_report)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the write without response and read values matches")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=initial_value.data,
                         obtained=read_value.data,
                         msg="The value written without response doesn't match")
        # --------------------------------------------------------------------------------------------------------------
    # end def test_led_report

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_hidpp_reports(self):
        """
        Verify the HIDPP input and output reports are usable for HIDPP communication
        """
        self._common_test_hidpp_reports()

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0009", _AUTHOR)
    # end def test_hidpp_reports

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def _test_top_row_feature_report(self):
        """
        Verify the top row feature report
        Note disabled until further investigation on long writes
        """
        self._prerequisite_gatt_table()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get the feature report")
        # --------------------------------------------------------------------------------------------------------------
        report = self._get_report(ReportReferences.TOP_ROW_FEATURE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read the initial value on the report")
        # --------------------------------------------------------------------------------------------------------------
        read_value = self.ble_context.attribute_read(ble_context_device=self.ble_context_device_used,
                                                     attribute=report)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate a new value")
        # --------------------------------------------------------------------------------------------------------------
        write_value = HexList("03000700" * int(len(read_value.data) / 4))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write the new value to the report")
        LogHelper.log_info(self, f"Value to write: {write_value}")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.characteristic_long_write(ble_context_device=self.ble_context_device_used,
                                                   characteristic=report,
                                                   data=BleMessage(data=write_value))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read back the value on the report")
        # --------------------------------------------------------------------------------------------------------------
        read_value_2 = self.ble_context.attribute_read(ble_context_device=self.ble_context_device_used,
                                                       attribute=report)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check read match what was written")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=write_value, obtained=read_value_2.data, msg="Value read after write doesn't match "
                                                                               "written value")

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0010", _AUTHOR)
    # end def _test_top_row_feature_report

    @features('BLEProtocol')
    @features('Mice')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_boot_protocol_mouse(self):
        """
        Verify that the device switch to boot protocol mode correctly for mice
        """
        hids_uuid = BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)
        protocol_mode_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.PROTOCOL_MODE)
        boot_report_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_MOUSE_INPUT_REPORT)
        self._prerequisite_gatt_table()
        keys = self._prerequisite_subscribe_to_input_report()
        self._prerequisite_subscribe_to_boot_mouse_input_report()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Put device in Boot Protocol mode through a write "
                                 "on HIDS Boot Protocol characteristic")
        # --------------------------------------------------------------------------------------------------------------

        BleProtocolTestUtils.write_wo_resp_characteristic(test_case=self,
                                                          ble_context_device=self.ble_context_device_used,
                                                          service_uuid=hids_uuid,
                                                          characteristic_uuid=protocol_mode_uuid,
                                                          value=HexList(HidData.Protocol.BOOT))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device shows it is in boot protocol mode")
        # --------------------------------------------------------------------------------------------------------------
        protocol_mode_read = BleProtocolTestUtils.read_characteristics(test_case=self,
                                                                       ble_context_device=self.ble_context_device_used,
                                                                       service_uuid=hids_uuid,
                                                                       characteristic_uuid=protocol_mode_uuid)[0]
        self.assertEqual(expected=HexList(HidData.Protocol.BOOT), obtained=protocol_mode_read.data,
                         msg="The device didn't switch to BLE HID boot protocol mode")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate a mouse click user event")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check notification is received on boot mouse input report")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(hids_uuid, boot_report_uuid)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
        except queue.Empty:
            self.fail(msg="No notification received in time")
        # end try
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Ble notification={ble_notification}")
        LogHelper.log_check(self, "Check notification is not received on Report Protocol input reports")
        # --------------------------------------------------------------------------------------------------------------
        for key in keys:
            self.assertTrue(self.notifications_queues[key].empty(),
                            f"No notification should be received on Input report {key}")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Put device in Report Protocol mode through "
                                 "a write on HIDS Protocol Mode characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_wo_resp_characteristic(test_case=self,
                                                          ble_context_device=self.ble_context_device_used,
                                                          service_uuid=hids_uuid,
                                                          characteristic_uuid=protocol_mode_uuid,
                                                          value=HexList(HidData.Protocol.REPORT))
        self._empty_notification_queues()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device shows it is in report protocol mode")
        # --------------------------------------------------------------------------------------------------------------
        protocol_mode_read = BleProtocolTestUtils.read_characteristics(test_case=self,
                                                                       ble_context_device=self.ble_context_device_used,
                                                                       service_uuid=hids_uuid,
                                                                       characteristic_uuid=protocol_mode_uuid)[0]
        self.assertEqual(expected=HexList(HidData.Protocol.REPORT), obtained=protocol_mode_read.data,
                         msg="The device didn't switch to BLE HID report protocol mode")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate a mouse click user event")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check notification is NOT received on boot mouse input report")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notification = self.notifications_queues[(hids_uuid, boot_report_uuid)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            self.fail(msg=f"Notification received on the boot mouse input "
                          f"report while in report protocol mode. {ble_notification}")
        except queue.Empty:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "No notification received in time as expected")
            # ----------------------------------------------------------------------------------------------------------
            pass
        # end try
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check notification is received on Report Protocol input reports")
        # --------------------------------------------------------------------------------------------------------------
        empty = True
        for key in keys:
            empty &= self.notifications_queues[key].empty()
        # end for
        self.assertFalse(empty, f"Notification was not received on Input report")

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0011", _AUTHOR)
    # end def test_boot_protocol_mouse

    @features('BLEProtocol')
    @features('Keyboard')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    def test_boot_protocol_keyboard(self):
        """
        Verify that the device switch to boot protocol mode correctly for keyboards
        """
        hids_uuid = BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)
        protocol_mode_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.PROTOCOL_MODE)
        boot_input_report_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_INPUT_REPORT)
        boot_output_report_uuid = BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_OUTPUT_REPORT)
        self._prerequisite_gatt_table()
        keys = self._prerequisite_subscribe_to_input_report()
        self._prerequisite_subscribe_to_boot_keyboard_input_report()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Put device in Boot Protocol mode through a write "
                                 "on HIDS Boot Protocol characteristic")
        # --------------------------------------------------------------------------------------------------------------

        BleProtocolTestUtils.write_wo_resp_characteristic(test_case=self,
                                                          ble_context_device=self.ble_context_device_used,
                                                          service_uuid=hids_uuid,
                                                          characteristic_uuid=protocol_mode_uuid,
                                                          value=HexList(HidData.Protocol.BOOT))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device shows it is in boot protocol mode")
        # --------------------------------------------------------------------------------------------------------------
        protocol_mode_read = BleProtocolTestUtils.read_characteristics(test_case=self,
                                                                       ble_context_device=self.ble_context_device_used,
                                                                       service_uuid=hids_uuid,
                                                                       characteristic_uuid=protocol_mode_uuid)[0]
        self.assertEqual(expected=HexList(HidData.Protocol.BOOT), obtained=protocol_mode_read.data,
                         msg="The device didn't switch to BLE HID boot protocol mode")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate a keyboard click user event")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_O)

        ble_notifications = self._check_get_notification(self.notifications_queues[(hids_uuid, boot_input_report_uuid)],
                                                         2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Ble notifications = {ble_notifications}")
        LogHelper.log_check(self, "Check notification is not received on Report Protocol input reports")
        # --------------------------------------------------------------------------------------------------------------
        for key in keys:
            self.assertTrue(self.notifications_queues[key].empty(),
                            f"No notification should be received on Input report {key}")
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read the Boot Keyboard Output Report initial value")
        # --------------------------------------------------------------------------------------------------------------
        initial_value = BleProtocolTestUtils.read_characteristics(test_case=self,
                                                                  ble_context_device=self.ble_context_device_used,
                                                                  service_uuid=hids_uuid,
                                                                  characteristic_uuid=boot_output_report_uuid)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write to Boot Keyboard Output Report")
        # --------------------------------------------------------------------------------------------------------------

        value = initial_value.data ^ 0x02
        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.ble_context_device_used,
                                                  service_uuid=hids_uuid,
                                                  characteristic_uuid=boot_output_report_uuid,
                                                  value=value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read the value back")
        # --------------------------------------------------------------------------------------------------------------
        read_value = BleProtocolTestUtils.read_characteristics(test_case=self,
                                                               ble_context_device=self.ble_context_device_used,
                                                               service_uuid=hids_uuid,
                                                               characteristic_uuid=boot_output_report_uuid)[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the write and read values matches")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=value, obtained=read_value.data, msg="The value written doesn't match")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write without response to the Boot Keyboard Output Report")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_wo_resp_characteristic(test_case=self,
                                                          ble_context_device=self.ble_context_device_used,
                                                          service_uuid=hids_uuid,
                                                          characteristic_uuid=boot_output_report_uuid,
                                                          value=initial_value.data)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read the value back")
        # --------------------------------------------------------------------------------------------------------------
        read_value = BleProtocolTestUtils.read_characteristics(test_case=self,
                                                               ble_context_device=self.ble_context_device_used,
                                                               service_uuid=hids_uuid,
                                                               characteristic_uuid=boot_output_report_uuid)[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the write without response and read values matches")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=initial_value.data,
                         obtained=read_value.data,
                         msg="The value written without response doesn't match")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Put device in Report Protocol mode through "
                                 "a write on HIDS Protocol Mode characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_wo_resp_characteristic(test_case=self,
                                                          ble_context_device=self.ble_context_device_used,
                                                          service_uuid=hids_uuid,
                                                          characteristic_uuid=protocol_mode_uuid,
                                                          value=HexList(HidData.Protocol.REPORT))
        self._empty_notification_queues()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device shows it is in report protocol mode")
        # --------------------------------------------------------------------------------------------------------------
        protocol_mode_read = BleProtocolTestUtils.read_characteristics(test_case=self,
                                                                       ble_context_device=self.ble_context_device_used,
                                                                       service_uuid=hids_uuid,
                                                                       characteristic_uuid=protocol_mode_uuid)[0]
        self.assertEqual(expected=HexList(HidData.Protocol.REPORT), obtained=protocol_mode_read.data,
                         msg="The device didn't switch to BLE HID report protocol mode")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate a keyboard click user event")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check notification is NOT received on boot keyboard input report")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ble_notifications = self.notifications_queues[(hids_uuid, boot_input_report_uuid)].get(
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            self.fail(msg=f"Notification received on the boot keyboard input "
                          f"report while in report protocol mode. {ble_notifications}")
        except queue.Empty:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "No notification received in time as expected")
            # ----------------------------------------------------------------------------------------------------------
            pass
        # end try
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check notification is received on Report Protocol input reports")
        # --------------------------------------------------------------------------------------------------------------
        empty = True
        for key in keys:
            empty &= self.notifications_queues[key].empty()
        # end for
        self.assertFalse(empty, f"Notification was not received on Input report")

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0011", _AUTHOR)
    # end def test_boot_protocol_keyboard

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_hid_control_point(self):
        """
        Verify the hid control point characteristic is writable
        """
        self._common_test_hid_control_point()

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0013", _AUTHOR)
    # end def test_hid_control_point
# end class GattHIDSApplicationFunctionalityTestCase


@features.class_decorator("BootloaderBLESupport")
class GattHIDSBootloaderFunctionalityTestCase(GattHIDSFunctionalityTestCasesMixin, GattHIDSBootloaderTestCases):
    """
    BLE HIDS Functionality Test Cases Bootloader class
    """

    def setUp(self):
        # See GattHIDSFunctionTestCasesMixin.setUp
        GattHIDSBootloaderTestCases.setUp(self)
    # end def setUp

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_report_map(self):
        """
        Verify the report map and report characteristics matches
        """
        self._report_map_matches()

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0002", _AUTHOR)
    # end def test_report_map

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_hidpp_reports(self):
        """
        Verify the HIDPP input and output reports are usable for HIDPP communication
        """
        self._common_test_hidpp_reports()

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0009", _AUTHOR)
    # end def test_hidpp_reports

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_hid_control_point(self):
        """
        Verify the hid control point characteristic is writable
        """
        self._common_test_hid_control_point()

        self.testCaseChecked("FUN_BLE_GATT_HIDS_0014", _AUTHOR)
    # end def test_hid_control_point
# end class GattHIDSBootloaderFunctionalityTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
