#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.keyboard.test.lockkeystate_test
:brief: HID++ 2.0 ``LockKeyState`` test module
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/03/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.keyboard.lockkeystate import GetLockKeyState
from pyhid.hidpp.features.keyboard.lockkeystate import GetLockKeyStateResponse
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyChangeEvent
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyState
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyStateFactory
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyStateV0
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LockKeyStateInstantiationTestCase(TestCase):
    """
    Test ``LockKeyState`` testing classes instantiations
    """

    @staticmethod
    def test_lock_key_state():
        """
        Test ``LockKeyState`` class instantiation
        """
        my_class = LockKeyState(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = LockKeyState(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_lock_key_state

    @staticmethod
    def test_get_lock_key_state():
        """
        Test ``GetLockKeyState`` class instantiation
        """
        my_class = GetLockKeyState(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetLockKeyState(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_lock_key_state

    @staticmethod
    def test_get_lock_key_state_response():
        """
        Test ``GetLockKeyStateResponse`` class instantiation
        """
        my_class = GetLockKeyStateResponse(device_index=0, feature_index=0,
                                           kana=False,
                                           compose=False,
                                           scroll_lock=False,
                                           caps_lock=False,
                                           num_lock=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetLockKeyStateResponse(device_index=0xff, feature_index=0xff,
                                           kana=True,
                                           compose=True,
                                           scroll_lock=True,
                                           caps_lock=True,
                                           num_lock=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_lock_key_state_response

    @staticmethod
    def test_lock_key_change_event():
        """
        Test ``LockKeyChangeEvent`` class instantiation
        """
        my_class = LockKeyChangeEvent(device_index=0, feature_index=0,
                                      kana=False,
                                      compose=False,
                                      scroll_lock=False,
                                      caps_lock=False,
                                      num_lock=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = LockKeyChangeEvent(device_index=0xff, feature_index=0xff,
                                      kana=True,
                                      compose=True,
                                      scroll_lock=True,
                                      caps_lock=True,
                                      num_lock=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_lock_key_change_event
# end class LockKeyStateInstantiationTestCase


class LockKeyStateTestCase(TestCase):
    """
    Test ``LockKeyState`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            LockKeyStateV0.VERSION: {
                "cls": LockKeyStateV0,
                "interfaces": {
                    "get_lock_key_state_cls": GetLockKeyState,
                    "get_lock_key_state_response_cls": GetLockKeyStateResponse,
                    "lock_key_change_event_cls": LockKeyChangeEvent,
                },
                "max_function_index": 0
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``LockKeyStateFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(LockKeyStateFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``LockKeyStateFactory`` using out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                LockKeyStateFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``LockKeyStateFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = LockKeyStateFactory.create(version)
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
            obj = LockKeyStateFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class LockKeyStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
