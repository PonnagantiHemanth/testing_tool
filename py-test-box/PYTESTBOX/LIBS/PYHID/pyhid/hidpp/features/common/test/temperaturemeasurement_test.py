#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.test.temperaturemeasurement_test
:brief: HID++ 2.0 ``TemperatureMeasurement`` test module
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/07/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.temperaturemeasurement import GetInfo
from pyhid.hidpp.features.common.temperaturemeasurement import GetInfoResponse
from pyhid.hidpp.features.common.temperaturemeasurement import GetTemperature
from pyhid.hidpp.features.common.temperaturemeasurement import GetTemperatureResponse
from pyhid.hidpp.features.common.temperaturemeasurement import TemperatureMeasurement
from pyhid.hidpp.features.common.temperaturemeasurement import TemperatureMeasurementFactory
from pyhid.hidpp.features.common.temperaturemeasurement import TemperatureMeasurementV0
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TemperatureMeasurementInstantiationTestCase(TestCase):
    """
    ``TemperatureMeasurement`` testing classes instantiations
    """
    @staticmethod
    def test_temperature_measurement():
        """
        Tests ``TemperatureMeasurement`` class instantiation
        """
        my_class = TemperatureMeasurement(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = TemperatureMeasurement(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_temperature_measurement

    @staticmethod
    def test_get_info():
        """
        Tests ``GetInfo`` class instantiation
        """
        my_class = GetInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetInfo(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_info

    @staticmethod
    def test_get_info_response():
        """
        Tests ``GetInfoResponse`` class instantiation
        """
        my_class = GetInfoResponse(device_index=0, feature_index=0,
                                   sensor_count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponse(device_index=0xff, feature_index=0xff,
                                   sensor_count=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response

    @staticmethod
    def test_get_temperature():
        """
        Tests ``GetTemperature`` class instantiation
        """
        my_class = GetTemperature(device_index=0, feature_index=0,
                                  sensor_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetTemperature(device_index=0xff, feature_index=0xff,
                                  sensor_id=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_temperature

    @staticmethod
    def test_get_temperature_response():
        """
        Tests ``GetTemperatureResponse`` class instantiation
        """
        my_class = GetTemperatureResponse(device_index=0, feature_index=0,
                                          sensor_id=0,
                                          temperature=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetTemperatureResponse(device_index=0xff, feature_index=0xff,
                                          sensor_id=0xff,
                                          temperature=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_temperature_response
# end class TemperatureMeasurementInstantiationTestCase


class TemperatureMeasurementTestCase(TestCase):
    """
    ``TemperatureMeasurement`` factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            TemperatureMeasurementV0.VERSION: {
                "cls": TemperatureMeasurementV0,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponse,
                    "get_temperature_cls": GetTemperature,
                    "get_temperature_response_cls": GetTemperatureResponse,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Tests ``TemperatureMeasurementFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(TemperatureMeasurementFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Tests ``TemperatureMeasurementFactory`` with out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                TemperatureMeasurementFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``TemperatureMeasurementFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = TemperatureMeasurementFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(obj, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(obj, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check ``get_max_function_index`` returns correct value at each version
        """
        for version, expected in self.expected.items():
            obj = TemperatureMeasurementFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class TemperatureMeasurementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
