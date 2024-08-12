#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.mouse.test.ratchetwheel_test
:brief: HID++ 2.0 ``RatchetWheel`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2022/11/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.mouse.ratchetwheel import GetWheelMode
from pyhid.hidpp.features.mouse.ratchetwheel import GetWheelModeResponse
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheel
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheelFactory
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheelV0
from pyhid.hidpp.features.mouse.ratchetwheel import SetModeStatus
from pyhid.hidpp.features.mouse.ratchetwheel import SetModeStatusResponse
from pyhid.hidpp.features.mouse.ratchetwheel import WheelMovementEvent
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RatchetWheelInstantiationTestCase(TestCase):
    """
    Test ``RatchetWheel`` testing classes instantiations
    """

    @staticmethod
    def test_ratchet_wheel():
        """
        Test ``RatchetWheel`` class instantiation
        """
        my_class = RatchetWheel(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = RatchetWheel(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_ratchet_wheel

    @staticmethod
    def test_get_wheel_mode():
        """
        Test ``GetWheelMode`` class instantiation
        """
        my_class = GetWheelMode(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetWheelMode(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_wheel_mode

    @staticmethod
    def test_get_wheel_mode_response():
        """
        Test ``GetWheelModeResponse`` class instantiation
        """
        my_class = GetWheelModeResponse(device_index=0, feature_index=0,
                                        divert=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetWheelModeResponse(device_index=0xff, feature_index=0xff,
                                        divert=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_wheel_mode_response

    @staticmethod
    def test_set_mode_status():
        """
        Test ``SetModeStatus`` class instantiation
        """
        my_class = SetModeStatus(device_index=0, feature_index=0,
                                 divert=False)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetModeStatus(device_index=0xff, feature_index=0xff,
                                 divert=True)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_mode_status

    @staticmethod
    def test_set_mode_status_response():
        """
        Test ``SetModeStatusResponse`` class instantiation
        """
        my_class = SetModeStatusResponse(device_index=0, feature_index=0,
                                         divert=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetModeStatusResponse(device_index=0xff, feature_index=0xff,
                                         divert=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_mode_status_response

    @staticmethod
    def test_wheel_movement_event():
        """
        Test ``WheelMovementEvent`` class instantiation
        """
        my_class = WheelMovementEvent(device_index=0, feature_index=0,
                                      delta_v=0,
                                      delta_h=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WheelMovementEvent(device_index=0xff, feature_index=0xff,
                                      delta_v=0xff,
                                      delta_h=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_wheel_movement_event
# end class RatchetWheelInstantiationTestCase


class RatchetWheelTestCase(TestCase):
    """
    Test ``RatchetWheel`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            RatchetWheelV0.VERSION: {
                "cls": RatchetWheelV0,
                "interfaces": {
                    "get_wheel_mode_cls": GetWheelMode,
                    "get_wheel_mode_response_cls": GetWheelModeResponse,
                    "set_mode_status_cls": SetModeStatus,
                    "set_mode_status_response_cls": SetModeStatusResponse,
                    "wheel_movement_event_cls": WheelMovementEvent,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``RatchetWheelFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(RatchetWheelFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``RatchetWheelFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                RatchetWheelFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``RatchetWheelFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = RatchetWheelFactory.create(version)
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
            obj = RatchetWheelFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class RatchetWheelTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
