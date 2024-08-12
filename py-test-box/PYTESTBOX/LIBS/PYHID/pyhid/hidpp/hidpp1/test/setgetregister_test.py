#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.test.setgetregister_test
    :brief: HID++ 1.0 set get register test module
    :author: Christophe Roquebert
    :date: 2020/03/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse
from pyhid.hidpp.hidpp1.setgetregister import GetRegister
from pyhid.hidpp.hidpp1.setgetregister import GetRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import GetRegisterResponse
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegisterResponse
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegisterResponse
from pyhid.hidpp.hidpp1.test.registerbasetest import RegisterBaseTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class RegisterTestCase(RegisterBaseTestCase):
    """
    Set/Get Register testing class
    """
    def test_set_register(self):
        """
        Tests SetRegister class instantiation
        """
        # Test Class minimum value
        my_class = SetRegister(device_index=0, address=0)
        self._top_level_class_checker(my_class)

        # Test Class maximum value
        my_class = SetRegister(device_index=0xFF, address=0xFF)
        self._top_level_class_checker(my_class)
    # end def test_set_register

    def test_set_register_request(self):
        """
        Tests SetRegister Request class instantiation
        """
        # Test Class default value
        my_class = SetRegisterRequest(device_index=0, address=0)
        self._short_function_class_checker(my_class)

        # Test Class minimum value
        my_class = SetRegisterRequest(device_index=0, address=0, p0=0, p1=0, p2=0)
        self._short_function_class_checker(my_class)

        # Test Class maximum value
        my_class = SetRegisterRequest(device_index=0xFF, address=0xFF, p0=0xFF, p1=0xFF, p2=0xFF)
        self._short_function_class_checker(my_class)
    # end def test_set_register_request

    def test_set_register_response(self):
        """
        Tests SetRegister Response class instantiation
        """
        # Test Class minimum value
        my_class = SetRegisterResponse(device_index=0, address=0)
        self._short_function_class_checker(my_class)

        # Test Class maximum value
        my_class = SetRegisterResponse(device_index=0xFF, address=0xFF)
        self._short_function_class_checker(my_class)
    # end def test_set_register_response

    def test_get_register(self):
        """
        Tests GetRegister class instantiation
        """
        # Test Class minimum value
        my_class = GetRegister(device_index=0, address=0)
        self._top_level_class_checker(my_class)

        # Test Class maximum value
        my_class = GetRegister(device_index=0xFF, address=0xFF)
        self._top_level_class_checker(my_class)
    # end def test_get_register

    def test_get_register_request(self):
        """
        Tests GetRegister Request class instantiation
        """
        # Test Class default value
        my_class = GetRegisterRequest(device_index=0, address=0)
        self._short_function_class_checker(my_class)

        # Test Class minimum value
        my_class = GetRegisterRequest(device_index=0, address=0, r0=0, r1=0, r2=0)
        self._short_function_class_checker(my_class)

        # Test Class maximum value
        my_class = GetRegisterRequest(device_index=0xFF, address=0xFF, r0=0xFF, r1=0xFF, r2=0xFF)
        self._short_function_class_checker(my_class)
    # end def test_get_register_request

    def test_get_register_response(self):
        """
        Tests GetRegister Response class instantiation
        """
        # Test Class minimum value
        my_class = GetRegisterResponse(device_index=0, address=0, value=0)
        self._short_function_class_checker(my_class)

        # Test Class maximum value
        my_class = GetRegisterResponse(device_index=0xFF, address=0xFF, value=0xFF)
        self._short_function_class_checker(my_class)
    # end def test_get_register_request

    def test_set_long_register(self):
        """
        Tests SetLongRegister class instantiation
        """
        # Test Class minimum value
        my_class = SetLongRegister(device_index=0, address=0)
        self._top_level_class_checker(my_class)

        # Test Class maximum value
        my_class = SetLongRegister(device_index=0xFF, address=0xFF)
        self._top_level_class_checker(my_class)

    # end def test_set_long_register

    def test_set_long_register_request(self):
        """
        Tests SetLongRegister Request class instantiation
        """
        # Test Class default value
        my_class = SetLongRegisterRequest(device_index=0, address=0)
        self._long_function_class_checker(my_class)

        # Test Class minimum value
        my_class = SetLongRegisterRequest(device_index=0, address=0,
                                          value=HexList("00"*(SetLongRegisterRequest.LEN.VALUE//8)))
        self._long_function_class_checker(my_class)

        # Test Class maximum value
        my_class = SetLongRegisterRequest(device_index=0xFF, address=0xFF,
                                          value=HexList("FF"*(SetLongRegisterRequest.LEN.VALUE//8)))
        self._long_function_class_checker(my_class)
    # end def test_set_long_register_request

    def test_set_long_register_response(self):
        """
        Tests SetLongRegister Response class instantiation
        """
        # Test Class minimum value
        my_class = SetLongRegisterResponse(device_index=0, address=0)
        self._short_function_class_checker(my_class)

        # Test Class maximum value
        my_class = SetLongRegisterResponse(device_index=0xFF, address=0xFF)
        self._short_function_class_checker(my_class)

    # end def test_set_long_register_request

    def test_get_long_register(self):
        """
        Tests GetLongRegister class instantiation
        """
        # Test Class minimum value
        my_class = GetLongRegister(device_index=0, address=0)
        self._top_level_class_checker(my_class)

        # Test Class maximum value
        my_class = GetLongRegister(device_index=0xFF, address=0xFF)
        self._top_level_class_checker(my_class)

    # end def test_get_long_register

    def test_get_long_register_request(self):
        """
        Tests GetLongRegister Request class instantiation
        """
        # Test Class minimum value
        my_class = GetLongRegisterRequest(device_index=0, address=0)
        self._short_function_class_checker(my_class)

        # Test Class maximum value
        my_class = GetLongRegisterRequest(device_index=0xFF, address=0xFF)
        self._short_function_class_checker(my_class)

    # end def test_get_register_request

    def test_get_long_register_response(self):
        """
        Tests GetLongRegister Response class instantiation
        """
        # Test Class minimum value
        my_class = GetLongRegisterResponse(device_index=0, address=0,
                                           value=HexList("00"*(GetLongRegisterResponse.LEN.VALUE//8)))
        self._long_function_class_checker(my_class)

        # Test Class maximum value
        my_class = GetLongRegisterResponse(device_index=0xFF, address=0xFF,
                                           value=HexList("FF"*(GetLongRegisterResponse.LEN.VALUE//8)))
        self._long_function_class_checker(my_class)
    # end def test_get_long_register_request
# end class RegisterTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
