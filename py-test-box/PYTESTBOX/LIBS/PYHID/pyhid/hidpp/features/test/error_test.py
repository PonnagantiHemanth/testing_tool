#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.test.error_test

@brief  HID++ error test module

@author Martin Cryonnet

@date   2019/05/12
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ErrorTestCase(TestCase):
    """
    Error testing class
    """
    @staticmethod
    def _top_level_class_checker(a_class):
        """
        Checks some generic attributes from top-level class
        """
        # FEATURE_ID attribute presence
        assert(hasattr(a_class, 'FEATURE_ID') is True)
        # VERSION attribute presence
        assert(hasattr(a_class, 'VERSION') is True)
    # end def _top_level_class_checker

    def _function_class_checker(self, a_class, payload_size):
        """
        Checks some generic attributes from top-level class
        """
        # top-level attribute presence
        self._top_level_class_checker(a_class)
        # Check payload size
        buffer = HexList(a_class)
        assert(payload_size == len(buffer))
    # end def _function_class_checker

    def _short_function_class_checker(self, a_class):
        """
        Checks some generic attributes from top-level class
        """
        # short payload class verification
        self._function_class_checker(a_class, HidppMessage.SHORT_MSG_SIZE)
    # end def _short_function_class_checker

    def test_hidpp1_error(self):
        """
        Tests HID++ 1.0 Error class instantiation
        """
        # Minimum values
        my_class = Hidpp1ErrorCodes(device_index=0x00, command_sub_id=0x00, register=0x00, error_code=0x00)
        self._short_function_class_checker(my_class)

        # Maximum values
        my_class = Hidpp1ErrorCodes(device_index=0xFF, command_sub_id=0xFF, register=0xFF, error_code=0xFF)
        self._short_function_class_checker(my_class)
    # end def test_hidpp1_error

    @staticmethod
    def test_error_codes():
        """
        Tests error codes values

        Code (hex) | Name                    | Description
        0          | ERR_SUCCESS             | No error / undefined
        1          | ERR_INVALID_SUBID       |  Invalid SubID / command
        2          | ERR_INVALID_ADDRESS     | Invalid address
        3*         | ERR_INVALID_VALUE       | Invalid value
        4          | ERR_CONNECT_FAIL        | Connection request failed (Receiver)
        5          | ERR_TOO_MANY_DEVICES    | Too many devices connected (Receiver)
        6          | ERR_ALREADY_EXISTS      | Already exists (Receiver)
        7          | ERR_BUSY                | Busy (Receiver)
        8          | ERR_UNKNOWN_DEVICE      | Unknown device (Receiver)
        9          | ERR_RESOURCE_ERROR      | Resource error (Receiver)
        A          | ERR_REQUEST_UNAVAILABLE | "Request not valid in current context" error
        B          | ERR_INVALID_PARAM_VALUE | Request parameter has unsupported value
        C          | ERR_WRONG_PIN_CODE      | the PIN code entered on the device was wrong
        D - FF     | Reserved                |
        """
        error_codes = {
                'ERR_SUCCESS': 0x00,
                'ERR_INVALID_SUBID': 0x01,
                'ERR_INVALID_ADDRESS': 0x02,
                'ERR_INVALID_VALUE': 0x03,
                'ERR_CONNECT_FAIL': 0x04,
                'ERR_TOO_MANY_DEVICES': 0x05,
                'ERR_ALREADY_EXISTS': 0x06,
                'ERR_BUSY': 0x07,
                'ERR_UNKNOWN_DEVICE': 0x08,
                'ERR_RESOURCE_ERROR': 0x09,
                'ERR_REQUEST_UNAVAILABLE': 0x0A,
                'ERR_INVALID_PARAM_VALUE': 0x0B,
                'ERR_WRONG_PIN_CODE': 0x0C,
        }

        for key, value in error_codes.items():
            assert hasattr(Hidpp1ErrorCodes, key)
            assert getattr(Hidpp1ErrorCodes, key) == value
        # end for
    # end def test_error_codes
# end class ErrorTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
