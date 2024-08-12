#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.devicediscoveryutils
:brief:  Helpers for device discovery feature
:author: Martin Cryonnet
:date: 2020/04/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import time
from sys import stdout
from warnings import warn

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.devicerecovery import DeviceRecovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import SetPerformDeviceDiscoveryRequest
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import SetPerformDeviceDiscoveryResponse
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
BT_PID_GRAVITON = 'B34E'
BT_PID_AVALON = 'B029'
BT_PID_KAVALON = 'B37E'
BT_PIDS_PLATFORM = [BT_PID_GRAVITON, BT_PID_AVALON, BT_PID_KAVALON]


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DiscoveryTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on device discovery feature
    """
    # Timeout the device stays in discoverable mode
    DEVICE_DISCOVERY_TIMEOUT = 180
    # Tolerance in second around the 3 minutes timeout
    DEVICE_DISCOVERY_TOLERANCE = 12
    # Number of authorized Bluetooth address
    # The valid range is [LAST_GAP_ADDR : LAST_GAP_ADDR + AUTH_BLE_ADDR_COUNT]
    AUTH_BLE_ADDR_COUNT = 0x20

    @classmethod
    def set_ble_device_name(cls, test_case, device_name):
        """
        Set the crafted BLE device name

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_name: BLE device name used in advertising response
        :type device_name: ``str``
        """
        test_case.ble_device_name = device_name
    # end def set_ble_device_name

    @classmethod
    def get_ble_device_name(cls, test_case):
        """
        Retrieve the crafted BLE device name

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: BLE device name used in advertising response
        :rtype: ``str`` or ``None``
        """
        return test_case.ble_device_name if hasattr(test_case, 'ble_device_name') else None
    # end def get_ble_device_name

    class GetPerformDeviceDiscoveryResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on Perform Device Discovery response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Default checks
            """
            return cls.get_check_map(PerformDeviceDiscovery.DeviceDiscoveryStatus.NOTHING_ONGOING)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, expected_device_discovery_status):
            """
            Checks for a given expected Device Discovery Status
            """
            return {"discover_devices_status": (cls.check_discover_devices_status, expected_device_discovery_status)}
        # end def get_check_map

        @staticmethod
        def check_discover_devices_status(test_case, message, expected):
            """
            Check Device Discovery Status field
            """
            test_case.assertEqual(obtained=int(Numeral(message.discover_devices_status)), expected=expected,
                                  msg="Device Discovery Status is not as expected")
        # end def check_discover_devices_status

        @classmethod
        def get_range_check_map(cls):
            """
            Check fields are within a range
            """
            return {
                "discover_devices_status": (cls.check_discover_devices_status_in_range,
                                            PerformDeviceDiscovery.DeviceDiscoveryStatus.range())
            }
        # end def get_range_check_map

        @staticmethod
        def check_discover_devices_status_in_range(test_case, actual_response, expected):
            """
            Check field Discover Devices Status is within a range
            """
            test_case.assertTrue(
                expr=(expected[0] <= int(Numeral(actual_response.discover_devices_status)) <= expected[1]),
                msg='Discovery Device Status should be in valid range'
            )
        # end def check_discover_devices_status_in_range
    # end class GetPerformDeviceDiscoveryResponseChecker

    class DeviceDiscoveryNotificationChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on Device Discovery Notification
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Default checks
            """
            return {
                "notification_counter": (cls.check_notification_counter, DeviceDiscovery.DEFAULT.NOTIFICATION_COUNTER),
                "notification_counter_lsb": None,
                "notification_counter_msb": None,
                "notification_part": (cls.check_notification_part, DeviceDiscovery.PART.CONFIGURATION),
                "reserved": (cls.check_reserved, 0),
                "data": None,
            }
        # end def get_default_check_map

        @staticmethod
        def check_notification_counter(test_case, actual_notification, expected):
            """
            Check notification counter field
            """
            test_case.assertEqual(obtained=int(Numeral(actual_notification.notification_counter)), expected=expected,
                                  msg="Notification counter is not as expected")
        # end def check_notification_counter

        @staticmethod
        def check_notification_part(test_case, actual_notification, expected):
            """
            Check notification part field
            """
            test_case.assertEqual(obtained=int(Numeral(actual_notification.notification_part)), expected=expected,
                                  msg="Notification part is not as expected")
        # end def check_notification_part

        @staticmethod
        def check_reserved(test_case, actual_notification, expected):
            """
            Check reserved field
            """
            test_case.assertEqual(obtained=int(Numeral(actual_notification.reserved)), expected=expected,
                                  msg="Reserved is not as expected")
        # end def check_reserved

        @staticmethod
        def check_notification_data(test_case, actual_notification, expected):
            """
            Check notification data
            """
            test_case.assertEqual(obtained=actual_notification.data, expected=expected,
                                  msg="Notification data is not as expected")
        # end def check_notification_data

        @classmethod
        def check_name(cls, test_case, actual_notifications, expected=None):
            """
            Check name, from a set of notification
            """
            expected = expected if expected is not None else test_case.f.SHARED.DEVICES.F_Name[0]
            for part in range(DeviceDiscovery.PART.NAME_1, DeviceDiscovery.PART.NAME_3 + 1):
                if actual_notifications[part] is not None:
                    cls.check_notification_part(test_case, actual_notifications[part], part)
                # end if
            # end for

            name = DiscoveryTestUtils.get_name(actual_notifications)

            test_case.assertEqual(obtained=name, expected=expected, msg="Name is not as expected")
        # end def check_name

        class DataChecker(CommonBaseTestUtils.MessageChecker):
            """
            This class provides helpers for common checks on Device Discovery Notification data
            """
            @classmethod
            def get_default_check_map(cls, test_case):
                """
                Default checks and expected values for each field
                """
                devices_config = test_case.f.SHARED.DEVICES
                bluetooth_pid = test_case.config_manager.get_feature(ConfigurationManager.ID.DEVICES_BLUETOOTH_PIDS)[0]
                bluetooth_pid = HexList(bluetooth_pid)
                bluetooth_pid.reverse()
                return {
                    "protocol_type": (cls.check_protocol_type,
                                      DeviceDiscovery.DeviceDiscoveryPart0.BLE_PRO_PROTOCOL_TYPE),
                    "device_type": (cls.check_device_type, devices_config.F_Type[0]),
                    "bluetooth_pid": (cls.check_bluetooth_pid, bluetooth_pid),
                    "bluetooth_address": None,  # TODO : read from device NVS
                    "ble_pro_service_version": (cls.check_ble_pro_service_version,
                                                test_case.config_manager.get_feature(
                                                    ConfigurationManager.ID.BLE_PRO_SRV_VERSION)[0]),
                    "product_specific_data": (cls.check_product_specific_data, devices_config.F_ExtendedModelId[0]),
                    "prepairing_auth_method": (cls.check_prepairing_auth_method, 0),
                    "emu_2buttons_auth_method": (cls.check_emu_2_buttons_auth_method,
                                                 devices_config.F_Passkey2ButtonsAuthMethod[0]),
                    "passkey_auth_method": (cls.check_passkey_auth_method, devices_config.F_PasskeyAuthMethod[0]),
                    "device_info_reserved": (cls.check_device_info_reserved, 0),
                    "reserved_auth_method": (cls.check_reserved_auth_method, 0),
                    "rssi_level": None
                }
            # end def get_default_check_map

            @classmethod
            def get_range_check_map(cls, test_case):
                """
                Checks and expected range to check range for each field
                """
                bluetooth_pid = test_case.config_manager.get_feature(ConfigurationManager.ID.DEVICES_BLUETOOTH_PIDS)[0]
                bluetooth_pid = HexList(bluetooth_pid)
                bluetooth_pid.reverse()
                return {
                    "protocol_type": (cls.check_protocol_type,
                                      DeviceDiscovery.DeviceDiscoveryPart0.BLE_PRO_PROTOCOL_TYPE),
                    "device_type": (cls.check_device_type_range, list(Hidpp1Data.DeviceType)),
                    "bluetooth_pid": (cls.check_bluetooth_pid, HexList(bluetooth_pid)),
                    "bluetooth_address": None,
                    "ble_pro_service_version": None,
                    "product_specific_data": None,
                    "prepairing_auth_method": None,
                    "emu_2buttons_auth_method": None,
                    "passkey_auth_method": None,
                    "device_info_reserved": (cls.check_device_info_reserved, 0),
                    "reserved_auth_method": (cls.check_reserved_auth_method, 0)
                }
            # end def get_range_check_map

            @classmethod
            def check_protocol_type(cls, test_case, actual_data, expected):
                """
                Check protocol type field
                """
                test_case.assertEqual(obtained=int(Numeral(actual_data.protocol_type)), expected=expected,
                                      msg="Protocol type is not as expected")
            # end def check_protocol_type

            @classmethod
            def check_bluetooth_pid(cls, test_case, actual_data, expected):
                """
                Check Bluetooth PID field
                """
                test_case.assertEqual(expected=HexList(expected),
                                      obtained=HexList(actual_data.bluetooth_pid),
                                      msg="Bluetooth PID should be as expected")
            # end def check_bluetooth_pid

            @classmethod
            def check_ble_pro_service_version(cls, test_case, response_message, expected):
                """
                Check BLE Pro Service Version
                """
                test_case.assertEqual(expected=HexList(expected),
                                      obtained=HexList(response_message.ble_pro_service_version),
                                      msg="BLE Pro Service Version should be as expected")
            # end def check_ble_pro_service_version

            @classmethod
            def check_product_specific_data(cls, test_case, response_message, expected):
                """
                Check Product Specific Data / Extended Model ID
                """
                test_case.assertEqual(expected=int(expected),
                                      obtained=int(Numeral(response_message.product_specific_data)),
                                      msg="Product Specific Data / Extended Model ID should be as expected")
            # end def check_product_specific_data

            @classmethod
            def check_device_info_reserved(cls, test_case, actual_data, expected):
                """
                Check device info reserved bits
                """
                test_case.assertEqual(obtained=actual_data.device_info_reserved, expected=expected,
                                      msg="Reserved bits are not as expected")
            # end def check_device_info_reserved

            @classmethod
            def check_device_type(cls, test_case, actual_data, expected):
                """
                Check device type field
                """
                test_case.assertEqual(obtained=int(Numeral(actual_data.device_type)),
                                      expected=int(expected),
                                      msg="The device type should be as expected")
            # end def check_device_type

            @classmethod
            def check_device_type_range(cls, test_case, actual_data, expected_range):
                """
                Check device type range
                """
                test_case.assertIn(member=actual_data.device_type,
                                   container=expected_range,
                                   msg="The device type should be in the expected range")
            # end def check_device_type_range

            @classmethod
            def check_prepairing_auth_method(cls, test_case, actual_data, expected):
                """
                Check authentification method pre-pairing bit
                """
                test_case.assertEqual(expected=int(expected),
                                      obtained=int(Numeral(actual_data.prepairing_auth_method)),
                                      msg="Authentification Method pre-pairing bit should be as expected")

            # end def check_prepairing_auth_method

            @classmethod
            def check_reserved_auth_method(cls, test_case, actual_data, expected):
                """
                Check authentification method reserved bits
                """
                test_case.assertEqual(expected=int(expected),
                                      obtained=int(Numeral(actual_data.reserved_auth_method)),
                                      msg="Authentification Method reserved bits should be as expected")

            # end def check_reserved_auth_method

            @classmethod
            def check_emu_2_buttons_auth_method(cls, test_case, actual_data, expected):
                """
                Check Passkey emulation with 2 buttons authentication method
                """
                test_case.assertEqual(
                    expected=int(expected),
                    obtained=int(Numeral(actual_data.emu_2buttons_auth_method)),
                    msg="Passkey emulation with 2 buttons authentication method should be as expected")
            # end def check_emu_2_buttons_auth_method

            @classmethod
            def check_passkey_auth_method(cls, test_case, actual_data, expected):
                """
                Check Passkey authentication method
                """
                test_case.assertEqual(expected=int(expected),
                                      obtained=int(Numeral(actual_data.passkey_auth_method)),
                                      msg="Passkey authentication method should be as expected")
            # end def check_passkey_auth_method
        # end class DataChecker
    # end class DeviceDiscoveryNotificationChecker

    @classmethod
    def start_discovery(cls, test_case, timeout=PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT):
        """
        Send Perform Device Discovery to start discovery
        """
        return cls.perform_device_discovery(
            test_case, timeout, PerformDeviceDiscovery.DiscoverDevices.DISCOVER_HID_DEVICES)
    # end def start_discovery

    @classmethod
    def cancel_discovery(cls, test_case):
        """
        Send Perform Device Discovery to cancel discovery
        """
        return cls.perform_device_discovery(
            test_case,
            PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
            PerformDeviceDiscovery.DiscoverDevices.CANCEL_DISCOVERY)
    # end def cancel_discovery

    @classmethod
    def perform_device_discovery(cls, test_case, discovery_timeout, discover_devices):
        """
        Send Perform Device Discovery
        """
        perform_device_discovery = SetPerformDeviceDiscoveryRequest(discovery_timeout=discovery_timeout,
                                                                    discover_devices=discover_devices)
        return ChannelUtils.send(
            test_case=test_case,
            report=perform_device_discovery,
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPerformDeviceDiscoveryResponse)
    # end def perform_device_discovery

    @classmethod
    def get_first_device_discovery_notification(cls, test_case, timeout, max_tries=None, raise_err=True):
        """
        Get all parts of first available Device Discovery Notification starting at Part 0.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param timeout: Time to wait for message before raising exception [seconds]
        :type timeout: ``int`` or ``float``
        :param max_tries: retry counter
        :type max_tries: ``int``
        :param raise_err: flag to enable / disable exception handling
        :type raise_err: ``bool``

        :return: device discovery notifications array if required BLE PID and optionaly address match
                 None otherwise
        :rtype: ``None`` or ``list[DeviceDiscovery]``
        """
        is_group_matching_criteria = False

        if not raise_err and max_tries is None:
            warn(message="max_tries parameter shall be set when calling the function with raise_err to False")
        # end if
        if max_tries is None:
            # Set value to support receiving 20 * 4 discovery notifications from 5 other devices and still get the ones
            # from our DUT
            max_tries = 20 * DeviceDiscovery.PART.RESERVED * 5
        # end if

        next_message = None
        last_notification_counter = None
        device_discovery = [None] * DeviceDiscovery.PART.RESERVED
        big_endian_ble_pid = test_case.config_manager.get_feature(ConfigurationManager.ID.DEVICES_BLUETOOTH_PIDS)[0]
        bluetooth_pid = HexList(big_endian_ble_pid)
        bluetooth_pid.reverse()

        while max_tries > 0:
            is_first_notification_matching_criteria = False
            if next_message is None:
                try:
                    next_message = test_case.get_first_message_type_in_queue(
                        queue=test_case.hidDispatcher.receiver_event_queue, class_type=DeviceDiscovery, timeout=timeout)
                except AssertionError as no_msg_received_err:
                    if raise_err:
                        raise no_msg_received_err
                    else:
                        # If no device discovery notification received, exit
                        return None
                    # end if
                # end try
            # end if
            max_tries -= 1
            if next_message is None or next_message.notification_part != DeviceDiscovery.PART.CONFIGURATION:
                # The device discovery notification is not the first of a group, get the next one in the queue
                next_message = None
                continue
            else:
                # Device discovery notification with part index 0 found
                if next_message.data.bluetooth_pid == bluetooth_pid:
                    # The notification is matching the requested PID
                    if test_case.last_ble_address is not None:
                        curr_addr = Numeral(HexList(reversed(next_message.data.bluetooth_address)))
                        min_addr = Numeral(HexList(reversed(test_case.last_ble_address)))
                        # Filter notifications with BLE device address out of the authorized range
                        is_first_notification_matching_criteria = \
                            (min_addr <= curr_addr <= (min_addr + DiscoveryTestUtils.AUTH_BLE_ADDR_COUNT))
                    else:
                        # Take all the notifications whatever the BLE address
                        is_first_notification_matching_criteria = True
                    # end if
                    if is_first_notification_matching_criteria:
                        last_notification_counter = next_message.notification_counter
                        device_discovery[DeviceDiscovery.PART.CONFIGURATION] = next_message
                    # end if
                # end if
            # end if
            if not is_first_notification_matching_criteria:
                # The device discovery notification doesn't match the criteria, get the next message in the queue
                next_message = None
                continue
            # end if
            max_msg_cnt = DeviceDiscovery.PART.RESERVED
            while max_msg_cnt > 0:
                # Additional part loop
                try:
                    next_message = test_case.get_first_message_type_in_queue(
                        queue=test_case.hidDispatcher.receiver_event_queue, class_type=DeviceDiscovery, timeout=timeout)
                except AssertionError:
                    break
                # end try
                max_msg_cnt -= 1
                if next_message.notification_counter == last_notification_counter and \
                        device_discovery[next_message.notification_part] is None:
                    device_discovery[next_message.notification_part] = next_message
                elif next_message.notification_counter != last_notification_counter and \
                        next_message.notification_part == DeviceDiscovery.PART.CONFIGURATION:
                    # The notification is linked to another group, exit the additional part loop
                    last_notification_counter = None
                    break
                # end if
            # end while
            if device_discovery[DeviceDiscovery.PART.NAME_1] is not None:
                crafted_device_name = DiscoveryTestUtils.get_ble_device_name(test_case=test_case)
                if (big_endian_ble_pid in BT_PIDS_PLATFORM and cls.get_name(device_discovery)
                        not in [test_case.f.SHARED.DEVICES.F_Name[0], crafted_device_name]):
                    stdout.write(f'BLE device names mismatch: {cls.get_name(device_discovery)} not in '
                                 f'[{test_case.f.SHARED.DEVICES.F_Name[0]}, {crafted_device_name}]. Please check it!\n')
                    continue
                # end if
                # At least device discovery notification parts 0 & 1 have been found, exit the main loop
                is_group_matching_criteria = True
                break
            # end if
        # end while

        if not is_group_matching_criteria:
            return None
        else:
            if test_case.last_ble_address is None:
                # Temporarily displays the warning message to track tests missing the last BLE address initialization
                stdout.write('Last BLE address in NVS has not been proofread. First notification received has a '
                             f'{cls.get_name(device_discovery)} device name. Please check it!\n')
            # end if
            return device_discovery
        # end if
    # end def get_first_device_discovery_notification

    @classmethod
    def get_all_device_discovery_notifications(cls, test_case, timeout=PerformDeviceDiscovery.DiscoveryTimeout.MIN):
        """
        Get all Device Discovery notifications from the queue
        """
        notifications = []
        try:
            notifications.append(
                test_case.get_first_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue,
                                                          DeviceDiscovery, timeout))
            notifications += test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue,
                                                                   DeviceDiscovery)
        except AssertionError:
            pass
        # end try
        return notifications
    # end def get_all_device_discovery_notifications

    @staticmethod
    def get_name(notifications_set):
        """
        Retrieve device name from Device Discovery notifications
        """
        name_length = int(Numeral(notifications_set[DeviceDiscovery.PART.NAME_1].data.device_name_length))
        name = notifications_set[DeviceDiscovery.PART.NAME_1].data.device_name_start.toString()

        if notifications_set[DeviceDiscovery.PART.NAME_2] is not None:
            name += notifications_set[DeviceDiscovery.PART.NAME_2].data.device_name_chunk.toString()
        # end if
        if notifications_set[DeviceDiscovery.PART.NAME_3] is not None:
            name += notifications_set[DeviceDiscovery.PART.NAME_3].data.device_name_chunk.toString()
        # end if
        return name[:name_length]
    # end def get_name

    @staticmethod
    def check_status_notification(test_case, expected_status, expected_error_type):
        """
        Check status and error type of first received Device Discovery Status notification
        """
        test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, DeviceDiscovery)
        msg = test_case.getMessage(test_case.hidDispatcher.receiver_event_queue,
                                   (DiscoveryStatus, DeviceDiscovery, DeviceRecovery, PairingStatus))
        if isinstance(msg, DiscoveryStatus):
            disc_status = msg
        else:
            disc_status = test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue,
                                                                DiscoveryStatus)
            test_case.assertGreater(len(disc_status), 0, 'Discovery Status notification should have been received')
            disc_status = disc_status[0]
        # end if
        test_case.assertEqual(obtained=disc_status.device_discovery_status, expected=HexList(expected_status),
                              msg="Device Discovery Status is not as expected")
        test_case.assertEqual(obtained=disc_status.error_type, expected=HexList(expected_error_type),
                              msg="Error Type is not as expected")
    # end def check_status_notification

    @staticmethod
    def check_device_discovery_notifications_until_timeout(test_case, end_time, step_time, tolerance):
        """
        Check Device Discovery notifications are received until the end of the timeout

        :param test_case: The current test case
        :type test_case: ``TestCase``
        :param end_time: End time
        :type end_time: ``float``
        :param step_time: Step time between 2 consecutive checks
        :type step_time: ``float``
        :param tolerance: Tolerance
        :type tolerance: ``float``
        """
        remaining_time = end_time
        while remaining_time > tolerance:
            test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, DiscoveryStatus)
            msg = test_case.getMessage(test_case.hidDispatcher.receiver_event_queue,
                                       (DeviceDiscovery, DiscoveryStatus, DeviceRecovery), step_time)
            if isinstance(msg, DiscoveryStatus):
                test_case.getMessage(test_case.hidDispatcher.receiver_event_queue,
                                     (DeviceDiscovery, DiscoveryStatus, DeviceRecovery), step_time)
            # end if
            test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, DeviceDiscovery)
            remaining_time = end_time - time.perf_counter()
        # end while

        while time.perf_counter() < end_time + tolerance:
            time.sleep(step_time)
            test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue,
                                                  (DeviceDiscovery, DiscoveryStatus, DeviceRecovery))
        # end while
    # end def check_device_discovery_notifications_until_timeout

    @staticmethod
    def check_timeout_discovery_status_notification(test_case, end_time, step_time, tolerance):
        """
        Check Discovery Status Notification is received at the end of the timeout and only at the end, with status
        Stop and Error Type Timeout.

        :param test_case: The current test case
        :type test_case: ``TestCase``
        :param end_time: End time
        :type end_time: ``float``
        :param step_time: Step time between 2 consecutive checks
        :type step_time: ``float``
        :param tolerance: Tolerance
        :type tolerance: ``float``
        """
        remaining_time = end_time
        while remaining_time > tolerance:
            disc_status = test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue,
                                                                DiscoveryStatus)
            test_case.assertListEqual(disc_status, [],
                                      f'No discovery status should be received ({remaining_time:.2f}s remaining '
                                      f'until end time)')
            time.sleep(step_time)
            remaining_time = end_time - time.perf_counter()
        # end while
        while time.perf_counter() < end_time + tolerance:
            time.sleep(step_time)
        # end while
        DiscoveryTestUtils.check_status_notification(
            test_case, DiscoveryStatus.DeviceDiscoveryStatus.STOP, DiscoveryStatus.ErrorType.TIMEOUT)
    # end def check_timeout_discovery_status_notification

    @staticmethod
    def check_discovery_notifications_until_timeout(test_case, end_time, step_time, tolerance,
                                                    check_device_discovery=True, check_discovery_status=True,
                                                    log_check=0):
        """
        Check Device Discovery notifications are received until the end of the timeout and check Discovery Status
        Notification is received at the end of the timeout and only at the end, with status Stop and Error Type Timeout.

        :param test_case: The current test case
        :type test_case: ``TestCase``
        :param end_time: End time
        :type end_time: ``float``
        :param step_time: Step time between 2 consecutive checks
        :type step_time: ``float``
        :param tolerance: Tolerance
        :type tolerance: ``float``
        :param check_device_discovery: Flag to activate device discovery notifications check
        :type check_device_discovery: ``bool``
        :param check_discovery_status: Flag to activate discovery status notifications check
        :type check_discovery_status: ``bool``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``
        """
        if log_check > 0:
            # ---------------------------------------------------------------------------
            test_case.logTitle2(f'Test Check {log_check}: Check Device Discovery notifications are received until the '
                                f'end of the timeout and check Discovery Status Notification is received at the end '
                                f'of the timeout and only at the end, with status Stop and Error Type Timeout.')
            # ---------------------------------------------------------------------------
        # end if
        remaining_time = end_time
        while remaining_time > tolerance:
            if check_device_discovery:
                msg = test_case.get_first_message_type_in_queue(
                    test_case.hidDispatcher.receiver_event_queue, DeviceDiscovery, step_time)
            elif check_discovery_status:
                disc_status = test_case.clean_message_type_in_queue(
                    test_case.hidDispatcher.receiver_event_queue, DiscoveryStatus)
                msg = disc_status[0] if len(disc_status) > 0 else None
                time.sleep(step_time)
            else:
                test_case.clean_message_type_in_queue(
                    test_case.hidDispatcher.receiver_event_queue, (DeviceDiscovery, DiscoveryStatus))
                msg = None
                time.sleep(step_time)
            # end if
            if check_discovery_status and isinstance(msg, DiscoveryStatus):
                test_case.fail('No Discovery Status notification should be received')
            # end if
            remaining_time = end_time - time.perf_counter()
        # end while

        while time.perf_counter() < end_time + tolerance:
            time.sleep(step_time)
            test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, DeviceDiscovery)
        # end while

        if check_discovery_status:
            DiscoveryTestUtils.check_status_notification(
                test_case, DiscoveryStatus.DeviceDiscoveryStatus.STOP, DiscoveryStatus.ErrorType.TIMEOUT)
        else:
            test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, DiscoveryStatus)
        # end if
    # end def check_discovery_notifications_until_timeout

    @classmethod
    def device_discovery_sequence(cls, test_case, trigger_user_action=True):
        """
        Run the standard Device Discovery Sequence

        Sequence diagram:
            SW -> Receiver: Perform Device Discovery (Discover HID Devices)
            SW <- Receiver: Discovery Status Notification (Discovery Start)
            Device <- User: Put in Pairing Mode
            Receiver <- Device: Advertising
            Receiver -> Device: SCAN_REQ
            Receiver <- Device : SCAN_RSP
            SW <- Receiver: Device Discovery Notification

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :param trigger_user_action: long key press on Connect or Easyswitch button if True
                                    skip the user action otherwise
        :type trigger_user_action: ``bool``
        :return: First device discovery notifications
        :rtype: ``list[DeviceDiscovery]``
        """
        cls.start_discovery(test_case)

        cls.check_status_notification(
            test_case, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, (DeviceRecovery,
                                                                                             DeviceDiscovery))

        if trigger_user_action:
            if test_case.f.PRODUCT.DEVICE.F_NbHosts > 1:
                test_case.button_stimuli_emulator.enter_pairing_mode()
            else:
                test_case.button_stimuli_emulator.enter_pairing_mode(HOST.CH1)
            # end if
        # end if

        device_discovery = cls.get_first_device_discovery_notification(
            test_case, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)

        test_case.assertNotNone(device_discovery,
                                "device discovery should always be received")
        test_case.assertNotNone(device_discovery[DeviceDiscovery.PART.CONFIGURATION],
                                "Part 0 (configuration) should always be received")
        test_case.assertNotNone(device_discovery[DeviceDiscovery.PART.NAME_1],
                                "Part 1 (Device name first part) should always be received")

        cls.DeviceDiscoveryNotificationChecker.DataChecker.check_protocol_type(
            test_case,
            device_discovery[DeviceDiscovery.PART.CONFIGURATION].data,
            DeviceDiscovery.DeviceDiscoveryPart0.BLE_PRO_PROTOCOL_TYPE)

        test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, DeviceDiscovery)

        return device_discovery
    # end def device_discovery_sequence

    @classmethod
    def discover_device(cls, test_case, trigger_user_action=True):
        """
        Discover connected device

        :param test_case: The current test case
        :type test_case: ``ReceiverBaseTestCase``
        :param trigger_user_action: long key press on Connect or Easyswitch button if True
                                    skip the user action otherwise
        :type trigger_user_action: ``bool``

        :return: The discovered device 6 bytes bluetooth address
        :rtype: ``HexList``
        """
        # Clean discovery notifications
        test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_event_queue, (DeviceDiscovery,
                                                                                             DiscoveryStatus))

        return cls.device_discovery_sequence(test_case, trigger_user_action)[
            DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address
    # end def discover_device
# end class DiscoveryTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
