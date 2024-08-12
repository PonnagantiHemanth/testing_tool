#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.test.devicerecovery_test
    :brief: HID++ 1.0 HID++ 1.0 devioce recovery notification tests
    :author: Christophe Roquebert
    :date: 2020/03/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.test.registerbasetest import RegisterBaseTestCase
from pyhid.hidpp.hidpp1.notifications.devicerecovery import DeviceRecovery


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceRecoveryTestCase(RegisterBaseTestCase):
    """
    Device Recovery testing class
    """

    def test_device_recovery_notification_part_0(self):
        """
        Tests Device Recovery class instantiation part 0
        """
        # Test Class notification minimum values
        part = HexList(
            # protocol_type
            0,
            # bluetooth_pid
            HexList("00"*(DeviceRecovery.DeviceRecoveryPart0.LEN.BLUETOOTH_PID//8)),
            # bluetooth_address
            HexList("00"*(DeviceRecovery.DeviceRecoveryPart0.LEN.BLUETOOTH_ADDRESS//8)),
            # ble_pro_service_version
            HexList("00"*(DeviceRecovery.DeviceRecoveryPart0.LEN.BLE_PRO_SERVICE_VERSION//8)),
            # unit_id
            HexList("00"*(DeviceRecovery.DeviceRecoveryPart0.LEN.UNIT_ID//8)))
        my_class = DeviceRecovery(device_index=0, notification_counter=0,
                                  notification_part=DeviceRecovery.PART.CONFIGURATION,
                                  data=part)
        self._long_function_class_checker(my_class)

        # Test Class maximum value
        part = HexList(
            # protocol_type
            0xFF,
            # bluetooth_pid
            HexList("FF"*(DeviceRecovery.DeviceRecoveryPart0.LEN.BLUETOOTH_PID//8)),
            # bluetooth_address
            HexList("FF"*(DeviceRecovery.DeviceRecoveryPart0.LEN.BLUETOOTH_ADDRESS//8)),
            # ble_pro_service_version
            HexList("FF"*(DeviceRecovery.DeviceRecoveryPart0.LEN.BLE_PRO_SERVICE_VERSION//8)),
            # unit_id
            HexList("FF"*(DeviceRecovery.DeviceRecoveryPart0.LEN.UNIT_ID//8)))
        my_class = DeviceRecovery(device_index=0xFF, notification_counter=0xFF,
                                  notification_part=DeviceRecovery.PART.CONFIGURATION,
                                  data=part)
        self._long_function_class_checker(my_class)
    # end def test_device_recovery_notification_part_0

    def test_device_recovery_notification_part_1(self):
        """
        Tests Device Recovery class instantiation part 1
        """
        # Test Class notification minimum values
        part = HexList(
            # device_name_length
            0,
            # device_name_start
            HexList("00"*(DeviceRecovery.DeviceRecoveryPart1.LEN.DEVICE_NAME_START//8)))
        my_class = DeviceRecovery(device_index=0, notification_counter=0,
                                  notification_part=DeviceRecovery.PART.NAME_1,
                                  data=part)
        self._long_function_class_checker(my_class)

        # Test Class maximum value
        part = HexList(
            # device_name_length
            0xFF,
            # device_name_start
            HexList("FF"*(DeviceRecovery.DeviceRecoveryPart1.LEN.DEVICE_NAME_START//8)))
        my_class = DeviceRecovery(device_index=0xFF, notification_counter=0xFF,
                                  notification_part=DeviceRecovery.PART.NAME_1,
                                  data=part)
        self._long_function_class_checker(my_class)
    # end def test_device_recovery_notification_part_1

    def test_device_recovery_notification_part_2(self):
        """
        Tests Device Recovery class instantiation part 2
        """
        # Test Class notification minimum values
        part = HexList(
            # device_name_chunk
            HexList("00"*(DeviceRecovery.DeviceRecoveryPart2.LEN.DEVICE_NAME_CHUNK//8)))
        my_class = DeviceRecovery(device_index=0, notification_counter=0,
                                  notification_part=DeviceRecovery.PART.NAME_2,
                                  data=part)
        self._long_function_class_checker(my_class)

        # Test Class maximum value
        part = HexList(
            # device_name_chunk
            HexList("FF"*(DeviceRecovery.DeviceRecoveryPart2.LEN.DEVICE_NAME_CHUNK//8)))
        my_class = DeviceRecovery(device_index=0xFF, notification_counter=0xFF,
                                  notification_part=DeviceRecovery.PART.NAME_2,
                                  data=part)
        self._long_function_class_checker(my_class)
    # end def test_device_recovery_notification_part_2

    def test_device_recovery_notification_part_3(self):
        """
        Tests Device Recovery class instantiation part 3
        """
        # Test Class notification minimum values
        part = HexList(
            # device_name_chunk
            HexList("00"*(DeviceRecovery.DeviceRecoveryPart3.LEN.DEVICE_NAME_CHUNK//8)))
        my_class = DeviceRecovery(device_index=0, notification_counter=0,
                                  notification_part=DeviceRecovery.PART.NAME_3,
                                  data=part)
        self._long_function_class_checker(my_class)

        # Test Class maximum value
        part = HexList(
            # device_name_chunk
            HexList("FF"*(DeviceRecovery.DeviceRecoveryPart2.LEN.DEVICE_NAME_CHUNK//8)))
        my_class = DeviceRecovery(device_index=0xFF, notification_counter=0xFF,
                                  notification_part=DeviceRecovery.PART.NAME_3,
                                  data=part)
        self._long_function_class_checker(my_class)
    # end def test_device_recovery_notification_part_3
# end class DeviceRecoveryTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
