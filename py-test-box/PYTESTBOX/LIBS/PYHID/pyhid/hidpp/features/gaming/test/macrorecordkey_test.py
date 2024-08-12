#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.gaming.test.macrorecordkey_test
:brief: HID++ 2.0 ``MacroRecordkey`` test module
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.macrorecordkey import ButtonReportEvent
from pyhid.hidpp.features.gaming.macrorecordkey import MacroRecordkey
from pyhid.hidpp.features.gaming.macrorecordkey import MacroRecordkeyFactory
from pyhid.hidpp.features.gaming.macrorecordkey import MacroRecordkeyV0
from pyhid.hidpp.features.gaming.macrorecordkey import SetLED
from pyhid.hidpp.features.gaming.macrorecordkey import SetLEDResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MacroRecordkeyInstantiationTestCase(TestCase):
    """
    Test ``MacroRecordkey`` testing classes instantiations
    """

    @staticmethod
    def test_macrorecord_key():
        """
        Test ``MacroRecordkey`` class instantiation
        """
        my_class = MacroRecordkey(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = MacroRecordkey(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_macrorecord_key

    @staticmethod
    def test_set_led():
        """
        Test ``SetLED`` class instantiation
        """
        my_class = SetLED(device_index=0, feature_index=0,
                          enabled=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetLED(device_index=0xFF, feature_index=0xFF,
                          enabled=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_led

    @staticmethod
    def test_set_led_response():
        """
        Test ``SetLEDResponse`` class instantiation
        """
        my_class = SetLEDResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetLEDResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_led_response

    @staticmethod
    def test_button_report_event():
        """
        Test ``ButtonReportEvent`` class instantiation
        """
        my_class = ButtonReportEvent(device_index=0, feature_index=0,
                                     mr_button_status=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ButtonReportEvent(device_index=0xFF, feature_index=0xFF,
                                     mr_button_status=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_button_report_event
# end class MacroRecordkeyInstantiationTestCase


class MacroRecordkeyTestCase(TestCase):
    """
    Test ``MacroRecordkey`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            MacroRecordkeyV0.VERSION: {
                "cls": MacroRecordkeyV0,
                "interfaces": {
                    "set_led_cls": SetLED,
                    "set_led_response_cls": SetLEDResponse,
                    "button_report_event_cls": ButtonReportEvent,
                },
                "max_function_index": 0
            },
        }
        cls.max_version = 0
    # end def setUpClass

    def test_factory(self):
        """
        Test ``MacroRecordkeyFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(MacroRecordkeyFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``MacroRecordkeyFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [self.max_version + 1, self.max_version + 2]:
            with self.assertRaises(KeyError):
                MacroRecordkeyFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``MacroRecordkeyFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = MacroRecordkeyFactory.create(version)
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
            obj = MacroRecordkeyFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class MacroRecordkeyTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
