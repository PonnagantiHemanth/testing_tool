#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
@package pyhid.hidpp.emulator.test.configurebuttons_test

@brief  HID++ 2.0 ConfigureButtons test module

@author Stanislas Cottard

@date   2019/05/27
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.emulator.configurebuttons import ConfigureButtons
from pyhid.hidpp.emulator.configurebuttons import GetButtonTableInfo
from pyhid.hidpp.emulator.configurebuttons import GetButtonTableInfoResponse
from pyhid.hidpp.emulator.configurebuttons import CreateSimpleEvent
from pyhid.hidpp.emulator.configurebuttons import CreateSimpleEventResponse
from pyhid.hidpp.emulator.configurebuttons import CreateWaveformEvent
from pyhid.hidpp.emulator.configurebuttons import CreateWaveformEventResponse
from pyhid.hidpp.emulator.configurebuttons import ConfigureWaveformPoints
from pyhid.hidpp.emulator.configurebuttons import ConfigureWaveformPointsResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class ConfigureButtonsTestCase(TestCase):
    """
    ConfigureButtons testing class
    """

    @staticmethod
    def test_configure_buttons():
        """
        Tests ConfigureButtons class instantiation
        """
        my_class = ConfigureButtons(deviceIndex=0,
                                    featureIndex=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_configure_buttons

    @staticmethod
    def test_get_button_table_info():
        """
        Tests GetButtonTableInfo class instantiation
        """
        my_class = GetButtonTableInfo(deviceIndex=0,
                                      featureId=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_button_table_info

    @staticmethod
    def test_create_simple_event():
        """
        Tests CreateSimpleEvent class instantiation
        """
        my_class = CreateSimpleEvent(deviceIndex=0,
                                     featureId=0,
                                     trigger_index=0,
                                     gpio=0,
                                     polarity=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_create_simple_event

    @staticmethod
    def test_create_waveform_event():
        """
        Tests CreateWaveformEvent class instantiation
        """
        my_class = CreateWaveformEvent(deviceIndex=0,
                                       featureId=0,
                                       trigger_index=0,
                                       table_id=0,
                                       gpio=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_create_waveform_event

    @staticmethod
    def test_configure_waveform_points():
        """
        Tests ConfigureWaveformPoints class instantiation
        """
        my_class = ConfigureWaveformPoints(deviceIndex=0,
                                           featureId=0,
                                           table_id=0,
                                           row_index=0)

        RootTestCase._long_function_class_checker(my_class)

        # Test also with other values than the default ones
        my_class = ConfigureWaveformPoints(deviceIndex=0,
                                           featureId=0,
                                           table_id=0,
                                           row_index=0,
                                           point_0=1,
                                           point_1=1,
                                           point_2=1,
                                           point_3=1,
                                           point_4=1,
                                           point_5=1,
                                           point_6=1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_configure_waveform_points

    @staticmethod
    def test_get_button_table_info_response():
        """
        Tests CreateImmediateDisplacementResponse class instantiation
        """
        my_class = GetButtonTableInfoResponse(deviceIndex=0,
                                              featureId=0,
                                              table_id_count=0,
                                              points_per_table=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_button_table_info_response

    @staticmethod
    def test_create_simple_event_response():
        """
        Tests CreateSimpleEventResponse class instantiation
        """
        my_class = CreateSimpleEventResponse(deviceIndex=0,
                                             featureId=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_create_simple_event_response

    @staticmethod
    def test_create_waveform_event_response():
        """
        Tests CreateWaveformEventResponse class instantiation
        """
        my_class = CreateWaveformEventResponse(deviceIndex=0,
                                               featureId=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_create_waveform_event_response

    @staticmethod
    def test_configure_waveform_points_response():
        """
        Tests ConfigureWaveformPointsResponse class instantiation
        """
        my_class = ConfigureWaveformPointsResponse(deviceIndex=0,
                                                   featureId=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_configure_waveform_points_response
# end class ConfigureButtonsTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
