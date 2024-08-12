#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.common.test.equaddjdebuginfo_test

@brief  HID++ 2.0 PowerModes test module

@author Stanislas Cottard

@date   2019/04/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.equaddjdebuginfo import EquadDJDebugInfo
from pyhid.hidpp.features.common.equaddjdebuginfo import ReadEquadDJDebugInfo
from pyhid.hidpp.features.common.equaddjdebuginfo import ReadEquadDJDebugInfoResponse
from pyhid.hidpp.features.common.equaddjdebuginfo import WriteEquadDJDebugInfo
from pyhid.hidpp.features.common.equaddjdebuginfo import WriteEquadDJDebugInfoResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class EquadDJDebugInfoTestCase(TestCase):
    """
    EquadDJDebugInfo testing class
    """

    @staticmethod
    def test_equad_dj_debug_info():
        """
        Tests EquadDJDebugInfo class instantiation
        """
        my_class = EquadDJDebugInfo(device_index=0,
                                    feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = EquadDJDebugInfo(device_index=0xFF,
                                    feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_equad_dj_debug_info

    @staticmethod
    def test_read_equad_dj_debug_info():
        """
        Tests ReadEquadDJDebugInfo class instantiation
        """
        my_class = ReadEquadDJDebugInfo(device_index=0,
                                        feature_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadEquadDJDebugInfo(device_index=0xFF,
                                        feature_id=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_equad_dj_debug_info

    @staticmethod
    def test_write_equad_dj_debug_info():
        """
        Tests WriteEquadDJDebugInfo class instantiation
        """
        my_class = WriteEquadDJDebugInfo(device_index=0,
                                         feature_id=0,
                                         equad_dj_debug_info_reg=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = WriteEquadDJDebugInfo(device_index=0xFF,
                                         feature_id=0xFF,
                                         equad_dj_debug_info_reg=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_write_equad_dj_debug_info

    @staticmethod
    def test_read_equad_dj_debug_info_response():
        """
        Tests ReadEquadDJDebugInfoResponse class instantiation
        """
        my_class = ReadEquadDJDebugInfoResponse(device_index=0,
                                                feature_id=0,
                                                equad_dj_debug_info_reg=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadEquadDJDebugInfoResponse(device_index=0xFF,
                                                feature_id=0xFF,
                                                equad_dj_debug_info_reg=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_equad_dj_debug_info_response

    @staticmethod
    def test_write_equad_dj_debug_info_response():
        """
        Tests WriteEquadDJDebugInfoResponse class instantiation
        """
        my_class = WriteEquadDJDebugInfoResponse(device_index=0,
                                                 feature_id=0,
                                                 equad_dj_debug_info_reg=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteEquadDJDebugInfoResponse(device_index=0xFF,
                                                 feature_id=0xFF,
                                                 equad_dj_debug_info_reg=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_equad_dj_debug_info_response
# end class EquadDJDebugInfoTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
