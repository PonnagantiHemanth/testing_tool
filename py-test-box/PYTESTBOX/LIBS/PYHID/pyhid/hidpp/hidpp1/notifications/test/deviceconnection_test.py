#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.notifications.test.deviceconnection_test
    :brief: HID++ 1.0 HID++ 1.0 devioce connection notification tests
    :author: Christophe Roquebert
    :date: 2020/04/08
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.test.registerbasetest import RegisterBaseTestCase
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceConnectionTestCase(RegisterBaseTestCase):
    """
    Device Connection testing class
    """

    def test_device_connection_request(self):
        """
        Tests Device Connection class instantiation
        """
        # Test Class request minimum values
        my_class = DeviceConnection(device_index=0,  protocol_type=0,
                                    information=HexList("00"*(DeviceConnection.LEN.INFORMATION_SHORT//8)))
        self._short_function_class_checker(my_class)

        # Test Class maximum value
        my_class = DeviceConnection(device_index=0xFF, protocol_type=0xFF,
                                    information=HexList("00"*(DeviceConnection.LEN.INFORMATION_LONG//8)))
        self._long_function_class_checker(my_class)
    # end def test_device_connection_request

    def test_protocol_types(self):
        """
        Tests Protocol Types constants
        """
        # Test BLE_PRO constant
        my_class = DeviceConnection(device_index=0,  protocol_type=DeviceConnection.ProtocolTypes.BLE_PRO,
                                    information=HexList("00"*(DeviceConnection.LEN.INFORMATION_SHORT//8)))
        self._short_function_class_checker(my_class)

        # Test DVC_DEF_PROTOCOL_GAMING_LS2_CA constant
        my_class = DeviceConnection(device_index=0,
                                    protocol_type=DeviceConnection.ProtocolTypes.DVC_DEF_PROTOCOL_GAMING_LS2_CA,
                                    information=HexList("00" * (DeviceConnection.LEN.INFORMATION_SHORT // 8)))
        self._short_function_class_checker(my_class)
    # end def test_protocol_types

    def test_link_status(self):
        """
        Tests Link Status constants
        """
        # Test LINK_ESTABLISHED constant
        my_class = DeviceConnection(device_index=0,  protocol_type=DeviceConnection.ProtocolTypes.BLE_PRO,
                                    information=HexList("00"*(DeviceConnection.LEN.INFORMATION_SHORT//8)))
        self._short_function_class_checker(my_class)

        # Test DVC_DEF_PROTOCOL_GAMING_LS2_CA constant
        my_class = DeviceConnection(device_index=0,
                                    protocol_type=DeviceConnection.ProtocolTypes.DVC_DEF_PROTOCOL_GAMING_LS2_CA,
                                    information=HexList("00" * (DeviceConnection.LEN.INFORMATION_SHORT // 8)))
        self._short_function_class_checker(my_class)
    # end def test_link_status
# end class DeviceConnectionTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
