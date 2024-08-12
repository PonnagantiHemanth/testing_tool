#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.test.common.uniqueidentifier32bytes_test

@brief  HID++ 2.0 UniqueIdentifier32Bytes test module

@author Stanislas Cottard

@date   2019/10/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.uniqueidentifier32bytes import UniqueIdentifier32Bytes
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte0To15
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte0To15Response
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte16To31
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte16To31Response
from pyhid.hidpp.features.common.uniqueidentifier32bytes import RegenId
from pyhid.hidpp.features.common.uniqueidentifier32bytes import RegenIdResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class UniqueIdentifier32BytesTestCase(TestCase):
    """
    UniqueIdentifier32Bytes testing class
    """

    @staticmethod
    def test_unique_identifier_32_bytes():
        """
        Tests UniqueIdentifier32Bytes class instantiation
        """
        my_class = UniqueIdentifier32Bytes(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = UniqueIdentifier32Bytes(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_unique_identifier_32_bytes

    @staticmethod
    def test_get_byte_0_to_15():
        """
        Tests GetByte0To15 class instantiation
        """
        my_class = GetByte0To15(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetByte0To15(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_byte_0_to_15

    @staticmethod
    def test_get_byte_16_to_31():
        """
        Tests GetByte16To31 class instantiation
        """
        my_class = GetByte16To31(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetByte16To31(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_byte_16_to_31

    @staticmethod
    def test_regen_id():
        """
        Tests RegenId class instantiation
        """
        my_class = RegenId(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = RegenId(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_regen_id

    @staticmethod
    def test_get_byte_0_to_15_response():
        """
        Tests GetByte0To15Response class instantiation
        """
        my_class = GetByte0To15Response(device_index=0, feature_index=0, bytes_0_to_15=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetByte0To15Response(device_index=0xFF,
                                        feature_index=0xFF,
                                        bytes_0_to_15=HexList([0xFF] * (GetByte0To15Response.LEN.BYTES_0_TO_15 // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_byte_0_to_15_response

    @staticmethod
    def test_get_byte_16_to_31_response():
        """
        Tests GetByte16To31Response class instantiation
        """
        my_class = GetByte16To31Response(device_index=0, feature_index=0, bytes_16_to_31=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetByte16To31Response(device_index=0xFF,
                                         feature_index=0xFF,
                                         bytes_16_to_31=HexList([0xFF] *
                                                                (GetByte16To31Response.LEN.BYTES_16_TO_31 // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_byte_16_to_31_response

    @staticmethod
    def test_regen_id_response():
        """
        Tests RegenIdResponse class instantiation
        """
        my_class = RegenIdResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RegenIdResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_regen_id_response
# end class UniqueIdentifier32BytesTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
