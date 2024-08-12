#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
@package pyhid.hidpp.emulator.test.loadopticalsensordata_test

@brief  HID++ 2.0 LoadOpticalSensorData test module

@author Stanislas Cottard

@date   2019/05/27
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.emulator.loadopticalsensordata import LoadOpticalSensorData
from pyhid.hidpp.emulator.loadopticalsensordata import CreateImmediateDisplacement
from pyhid.hidpp.emulator.loadopticalsensordata import CreateImmediateDisplacementResponse
from pyhid.hidpp.emulator.loadopticalsensordata import SensorPolledEvent
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class LoadOpticalSensorDataTestCase(TestCase):
    """
    LoadOpticalSensorData testing class
    """

    @staticmethod
    def test_load_optical_sensor_data():
        """
        Tests LoadOpticalSensorData class instantiation
        """
        my_class = LoadOpticalSensorData(deviceIndex=0,
                                         featureIndex=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_load_optical_sensor_data

    @staticmethod
    def test_create_immediate_displacement():
        """
        Tests CreateImmediateDisplacement class instantiation
        """
        my_class = CreateImmediateDisplacement(deviceIndex=0,
                                               featureId=0,
                                               trigger_index=0,
                                               x_displacement=0,
                                               y_displacement=0,
                                               repetition=0,
                                               delay=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_create_immediate_displacement

    @staticmethod
    def test_create_immediate_displacement_response():
        """
        Tests CreateImmediateDisplacementResponse class instantiation
        """
        my_class = CreateImmediateDisplacementResponse(deviceIndex=0,
                                                       featureId=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_create_immediate_displacement_response

    @staticmethod
    def test_sensor_polled_event():
        """
        Tests SensorPolledEvent class instantiation
        """
        my_class = SensorPolledEvent(deviceIndex=0,
                                     featureId=0,
                                     status=0,
                                     motion_asserted_ts=0,
                                     sensor_polled_ts=0,
                                     delta_time=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_sensor_polled_event
# end class LoadOpticalSensorDataTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
