#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.peripheral.test.pmw3816andpmw3826_test
:brief: HID++ 2.0 ``PMW3816andPMW3826`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2023/03/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ContinuousPower
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ContinuousPowerResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import FrameCaptureReportEvent
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import FrameCaptureResponseV0
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import FrameCaptureV0
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import GetStrapDataResponseV1
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import GetStrapDataV1
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import PMW3816andPMW3826
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import PMW3816andPMW3826Factory
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import PMW3816andPMW3826V0
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import PMW3816andPMW3826V1
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ReadSensorRegister
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ReadSensorRegisterResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ResetSensor
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ResetSensorResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ShutdownSensor
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ShutdownSensorResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import TrackingReportEvent
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import TrackingTest
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import TrackingTestResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import WriteSensorRegister
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import WriteSensorRegisterResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826InstantiationTestCase(TestCase):
    """
    Test ``PMW3816andPMW3826`` testing classes instantiations
    """

    @staticmethod
    def test_pmw3816_and_pmw3826():
        """
        Test ``PMW3816andPMW3826`` class instantiation
        """
        my_class = PMW3816andPMW3826(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = PMW3816andPMW3826(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_pmw3816_and_pmw3826

    @staticmethod
    def test_read_sensor_register():
        """
        Test ``ReadSensorRegister`` class instantiation
        """
        my_class = ReadSensorRegister(device_index=0, feature_index=0,
                                      register_address=HexList(0x0))

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadSensorRegister(device_index=0xFF, feature_index=0xFF,
                                      register_address=HexList("FF" * (ReadSensorRegister.LEN.REGISTER_ADDRESS // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_sensor_register

    @staticmethod
    def test_write_sensor_register():
        """
        Test ``WriteSensorRegister`` class instantiation
        """
        my_class = WriteSensorRegister(device_index=0, feature_index=0,
                                       register_address=HexList(0x0),
                                       register_value=HexList(0x0))

        RootTestCase._short_function_class_checker(my_class)

        my_class = WriteSensorRegister(device_index=0xFF, feature_index=0xFF,
                                       register_address=HexList("FF" * (WriteSensorRegister.LEN.REGISTER_ADDRESS // 8)),
                                       register_value=HexList("FF" * (WriteSensorRegister.LEN.REGISTER_VALUE // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_write_sensor_register

    @staticmethod
    def test_reset_sensor():
        """
        Test ``ResetSensor`` class instantiation
        """
        my_class = ResetSensor(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ResetSensor(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_reset_sensor

    @staticmethod
    def test_shutdown_sensor():
        """
        Test ``ShutdownSensor`` class instantiation
        """
        my_class = ShutdownSensor(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ShutdownSensor(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_shutdown_sensor

    @staticmethod
    def test_tracking_test():
        """
        Test ``TrackingTest`` class instantiation
        """
        my_class = TrackingTest(device_index=0, feature_index=0,
                                count=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = TrackingTest(device_index=0xFF, feature_index=0xFF,
                                count=0xFFFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_tracking_test

    @staticmethod
    def test_frame_capture_v0():
        """
        Test ``FrameCaptureV0`` class instantiation
        """
        my_class = FrameCaptureV0(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = FrameCaptureV0(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_frame_capture_v0

    @staticmethod
    def test_get_strap_data_v1():
        """
        Test ``GetStrapDataV1`` class instantiation
        """
        my_class = GetStrapDataV1(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetStrapDataV1(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_strap_data_v1

    @staticmethod
    def test_continuous_power():
        """
        Test ``ContinuousPower`` class instantiation
        """
        my_class = ContinuousPower(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ContinuousPower(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_continuous_power

    @staticmethod
    def test_read_sensor_register_response():
        """
        Test ``ReadSensorRegisterResponse`` class instantiation
        """
        my_class = ReadSensorRegisterResponse(device_index=0, feature_index=0,
                                              register_value=HexList(0x0))

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadSensorRegisterResponse(device_index=0xFF, feature_index=0xFF,
                                              register_value=HexList("FF" * (
                                                  ReadSensorRegisterResponse.LEN.REGISTER_VALUE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_sensor_register_response

    @staticmethod
    def test_write_sensor_register_response():
        """
        Test ``WriteSensorRegisterResponse`` class instantiation
        """
        my_class = WriteSensorRegisterResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteSensorRegisterResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_sensor_register_response

    @staticmethod
    def test_reset_sensor_response():
        """
        Test ``ResetSensorResponse`` class instantiation
        """
        my_class = ResetSensorResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ResetSensorResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_reset_sensor_response

    @staticmethod
    def test_shutdown_sensor_response():
        """
        Test ``ShutdownSensorResponse`` class instantiation
        """
        my_class = ShutdownSensorResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ShutdownSensorResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_shutdown_sensor_response

    @staticmethod
    def test_tracking_test_response():
        """
        Test ``TrackingTestResponse`` class instantiation
        """
        my_class = TrackingTestResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = TrackingTestResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_tracking_test_response

    @staticmethod
    def test_frame_capture_response_v0():
        """
        Test ``FrameCaptureResponseV0`` class instantiation
        """
        my_class = FrameCaptureResponseV0(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = FrameCaptureResponseV0(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_frame_capture_response_v0

    @staticmethod
    def test_get_strap_data_response_v1():
        """
        Test ``GetStrapDataResponseV1`` class instantiation
        """
        my_class = GetStrapDataResponseV1(device_index=0, feature_index=0,
                                          sensor=0,
                                          strap_measurement_x=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetStrapDataResponseV1(device_index=0xFF, feature_index=0xFF,
                                          sensor=0x3,
                                          strap_measurement_x=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_strap_data_response_v1

    @staticmethod
    def test_continuous_power_response():
        """
        Test ``ContinuousPowerResponse`` class instantiation
        """
        my_class = ContinuousPowerResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ContinuousPowerResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_continuous_power_response

    @staticmethod
    def test_tracking_report_event():
        """
        Test ``TrackingReportEvent`` class instantiation
        """
        my_class = TrackingReportEvent(device_index=0, feature_index=0,
                                       delta_x=0,
                                       delta_y=0,
                                       surface_quality_value=0,
                                       pixel_sum=0,
                                       maximum_pixel=0,
                                       minimum_pixel=0,
                                       shutter=0,
                                       counter=0,
                                       squal_average=0,
                                       shutter_average=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = TrackingReportEvent(device_index=0xFF, feature_index=0xFF,
                                       delta_x=0xFFFF,
                                       delta_y=0xFFFF,
                                       surface_quality_value=0xFF,
                                       pixel_sum=0xFF,
                                       maximum_pixel=0xFF,
                                       minimum_pixel=0xFF,
                                       shutter=0xFFFF,
                                       counter=0xFFFF,
                                       squal_average=0xFF,
                                       shutter_average=0xFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_tracking_report_event

    @staticmethod
    def test_frame_capture_report_event():
        """
        Test ``FrameCaptureReportEvent`` class instantiation
        """
        my_class = FrameCaptureReportEvent(device_index=0, feature_index=0,
                                           frame_data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = FrameCaptureReportEvent(device_index=0xFF, feature_index=0xFF,
                                           frame_data=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_frame_capture_report_event
# end class PMW3816andPMW3826InstantiationTestCase


class PMW3816andPMW3826TestCase(TestCase):
    """
    Test ``PMW3816andPMW3826`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            PMW3816andPMW3826V0.VERSION: {
                "cls": PMW3816andPMW3826V0,
                "interfaces": {
                    "read_sensor_register_cls": ReadSensorRegister,
                    "read_sensor_register_response_cls": ReadSensorRegisterResponse,
                    "write_sensor_register_cls": WriteSensorRegister,
                    "write_sensor_register_response_cls": WriteSensorRegisterResponse,
                    "reset_sensor_cls": ResetSensor,
                    "reset_sensor_response_cls": ResetSensorResponse,
                    "shutdown_sensor_cls": ShutdownSensor,
                    "shutdown_sensor_response_cls": ShutdownSensorResponse,
                    "tracking_test_cls": TrackingTest,
                    "tracking_test_response_cls": TrackingTestResponse,
                    "frame_capture_cls": FrameCaptureV0,
                    "frame_capture_response_cls": FrameCaptureResponseV0,
                    "continuous_power_cls": ContinuousPower,
                    "continuous_power_response_cls": ContinuousPowerResponse,
                    "tracking_report_event_cls": TrackingReportEvent,
                    "frame_capture_report_event_cls": FrameCaptureReportEvent,
                },
                "max_function_index": 6
            },
            PMW3816andPMW3826V1.VERSION: {
                "cls": PMW3816andPMW3826V1,
                "interfaces": {
                    "read_sensor_register_cls": ReadSensorRegister,
                    "read_sensor_register_response_cls": ReadSensorRegisterResponse,
                    "write_sensor_register_cls": WriteSensorRegister,
                    "write_sensor_register_response_cls": WriteSensorRegisterResponse,
                    "reset_sensor_cls": ResetSensor,
                    "reset_sensor_response_cls": ResetSensorResponse,
                    "shutdown_sensor_cls": ShutdownSensor,
                    "shutdown_sensor_response_cls": ShutdownSensorResponse,
                    "tracking_test_cls": TrackingTest,
                    "tracking_test_response_cls": TrackingTestResponse,
                    "get_strap_data_cls": GetStrapDataV1,
                    "get_strap_data_response_cls": GetStrapDataResponseV1,
                    "continuous_power_cls": ContinuousPower,
                    "continuous_power_response_cls": ContinuousPowerResponse,
                    "tracking_report_event_cls": TrackingReportEvent,
                    "frame_capture_report_event_cls": FrameCaptureReportEvent,
                },
                "max_function_index": 6
            },
        }
        cls.max_version = 1
    # end def setUpClass

    def test_factory(self):
        """
        Test ``PMW3816andPMW3826Factory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(PMW3816andPMW3826Factory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``PMW3816andPMW3826Factory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                PMW3816andPMW3826Factory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``PMW3816andPMW3826Factory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = PMW3816andPMW3826Factory.create(version)
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

        :raise ``AssertionError``: Assert max_function_index that raise an exception
        """
        for version, expected in self.expected.items():
            obj = PMW3816andPMW3826Factory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class PMW3816andPMW3826TestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
