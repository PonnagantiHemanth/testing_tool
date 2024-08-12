#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.ble_pro.ble_pro
:brief: Validate Gatt Ble Pro services  test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/06/29
"""


# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceApplicationTestCase
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceBootloaderTestCase
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
def attribute_value_format(suppressed_latency):
    """
    Create the value for the attributes characteristics based on the parameters

    :param suppressed_latency:  Flag indicating if latency is suppressed for control or supported for capability
    :type suppressed_latency: ``bool``
    
    :return: a properly formatted hexlist of the BLE pro attribute value
    :rtype: ``Hexlist``
    """
    attribute = HexList(0x01 if suppressed_latency else 0x00)
    attribute.addPadding(4, fromLeft=False)
    return attribute
# end def attribute_value_format


class GattBleProTestCase(GattSmallServiceTestCase):
    """
    BLE OS Gatt Ble Pro Test Cases common class
    """
# end class GattBleProTestCase


class GattBleProApplicationTestCase(GattBleProTestCase, GattSmallServiceApplicationTestCase):
    """
    BLE OS Gatt Ble Pro Test Cases common application class
    """
# end class GattBleProApplicationTestCase


class GattBleProBootloaderTestCase(GattBleProTestCase, GattSmallServiceBootloaderTestCase):
    """
    BLE OS Gatt Ble Pro Test Cases common bootloader class
    """
# end class GattBleProBootloaderTestCase


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
