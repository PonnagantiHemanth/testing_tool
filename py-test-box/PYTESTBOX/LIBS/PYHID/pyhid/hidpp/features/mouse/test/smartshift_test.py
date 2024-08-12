# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package    pyhid.hidpp.features.mouse.test.smartshift_test
@brief      HID++ 2.0 SmartShift 3G/EPM wheel enhancement test module
@author     Fred Chen
@date       2019/08/20
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.mouse.smartshift import SmartShift
from pyhid.hidpp.features.mouse.smartshift import GetRatchetControlMode
from pyhid.hidpp.features.mouse.smartshift import GetRatchetControlModeResponse
from pyhid.hidpp.features.mouse.smartshift import SetRatchetControlMode
from pyhid.hidpp.features.mouse.smartshift import SetRatchetControlModeResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class SmartShiftTestCase(TestCase):
    """
    SmartShiftTestCase testing class
    """

    @staticmethod
    def test_smart_shift():
        """
        Tests SmartShift class instantiation
        """
        my_class = SmartShift(device_index=0,
                              feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = SmartShift(device_index=0xFF,
                              feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_smart_shift

    @staticmethod
    def test_get_ratchet_control_mode():
        """
        Tests GetRatchetControlMode class instantiation
        """
        my_class = GetRatchetControlMode(device_index=0,
                                         feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetRatchetControlMode(device_index=0xFF,
                                         feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_ratchet_control_mode

    @staticmethod
    def test_set_ratchet_control_mode():
        """
        Tests SetRatchetControlMode class instantiation
        """
        my_class = SetRatchetControlMode(device_index=0,
                                         feature_index=0,
                                         wheel_mode=0,
                                         auto_disengage=0,
                                         auto_disengage_default=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetRatchetControlMode(device_index=0xFF,
                                         feature_index=0xFF,
                                         wheel_mode=0xFF,
                                         auto_disengage=0xFF,
                                         auto_disengage_default=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_ratchet_control_mode

    @staticmethod
    def test_get_ratchet_control_mode_response():
        """
        Tests GetRatchetControlModeResponse class instantiation
        """
        my_class = GetRatchetControlModeResponse(device_index=0,
                                                 feature_index=0,
                                                 wheel_mode=0,
                                                 auto_disengage=0,
                                                 auto_disengage_default=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetRatchetControlModeResponse(device_index=0xFF,
                                                 feature_index=0xFF,
                                                 wheel_mode=0xFF,
                                                 auto_disengage=0xFF,
                                                 auto_disengage_default=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_ratchet_control_mode_response

    @staticmethod
    def test_set_ratchet_control_mode_response():
        """
        Tests SetRatchetControlModeResponse class instantiation
        """
        my_class = SetRatchetControlModeResponse(device_index=0,
                                                 feature_index=0,
                                                 wheel_mode=0,
                                                 auto_disengage=0,
                                                 auto_disengage_default=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRatchetControlModeResponse(device_index=0xFF,
                                                 feature_index=0xFF,
                                                 wheel_mode=0xFF,
                                                 auto_disengage=0xFF,
                                                 auto_disengage_default=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_ratchet_control_mode_response

# end class SmartShiftTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
