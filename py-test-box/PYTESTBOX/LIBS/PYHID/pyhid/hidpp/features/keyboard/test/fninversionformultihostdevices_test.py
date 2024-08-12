#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.keyboard.test.fninversionformultihostdevices_test
:brief: HID++ 2.0 ``FnInversionForMultiHostDevices`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/04/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FLockChangeEvent
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevices
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevicesFactory
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevicesV0
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import GetGlobalFnInversion
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import GetGlobalFnInversionResponse
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import SetGlobalFnInversion
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import SetGlobalFnInversionResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FnInversionForMultiHostDevicesInstantiationTestCase(TestCase):
    """
    Test ``FnInversionForMultiHostDevices`` testing classes instantiations
    """

    @staticmethod
    def test_fn_inversion_for_multi_host_devices():
        """
        Test ``FnInversionForMultiHostDevices`` class instantiation
        """
        my_class = FnInversionForMultiHostDevices(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = FnInversionForMultiHostDevices(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_fn_inversion_for_multi_host_devices

    @staticmethod
    def test_get_global_fn_inversion():
        """
        Test ``GetGlobalFnInversion`` class instantiation
        """
        my_class = GetGlobalFnInversion(device_index=0, feature_index=0,
                                        host_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetGlobalFnInversion(device_index=0xFF, feature_index=0xFF,
                                        host_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_global_fn_inversion

    @staticmethod
    def test_get_global_fn_inversion_response():
        """
        Test ``GetGlobalFnInversionResponse`` class instantiation
        """
        my_class = GetGlobalFnInversionResponse(device_index=0, feature_index=0,
                                                host_index=0,
                                                fn_inversion_state=0,
                                                fn_inversion_default_state=0,
                                                capabilities_mask_reserved_bits=0,
                                                capabilities_mask_fn_lock=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetGlobalFnInversionResponse(device_index=0xFF, feature_index=0xFF,
                                                host_index=0xFF,
                                                fn_inversion_state=0xFF,
                                                fn_inversion_default_state=0xFF,
                                                capabilities_mask_reserved_bits=0x7F,
                                                capabilities_mask_fn_lock=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_global_fn_inversion_response

    @staticmethod
    def test_set_global_fn_inversion():
        """
        Test ``SetGlobalFnInversion`` class instantiation
        """
        my_class = SetGlobalFnInversion(device_index=0, feature_index=0,
                                        host_index=0,
                                        fn_inversion_state=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetGlobalFnInversion(device_index=0xFF, feature_index=0xFF,
                                        host_index=0xFF,
                                        fn_inversion_state=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_global_fn_inversion

    @staticmethod
    def test_set_global_fn_inversion_response():
        """
        Test ``SetGlobalFnInversionResponse`` class instantiation
        """
        my_class = SetGlobalFnInversionResponse(device_index=0, feature_index=0,
                                                host_index=0,
                                                fn_inversion_state=0,
                                                fn_inversion_default_state=0,
                                                capabilities_mask_reserved_bits=0,
                                                capabilities_mask_fn_lock=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetGlobalFnInversionResponse(device_index=0xFF, feature_index=0xFF,
                                                host_index=0xFF,
                                                fn_inversion_state=0xFF,
                                                fn_inversion_default_state=0xFF,
                                                capabilities_mask_reserved_bits=0x7F,
                                                capabilities_mask_fn_lock=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_global_fn_inversion_response

    @staticmethod
    def test_f_lock_change_event():
        """
        Test ``FLockChangeEvent`` class instantiation
        """
        my_class = FLockChangeEvent(device_index=0, feature_index=0,
                                    host_index=0,
                                    fn_inversion_state=0,
                                    fn_inversion_default_state=0,
                                    capabilities_mask_reserved_bits=0,
                                    capabilities_mask_fn_lock=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = FLockChangeEvent(device_index=0xFF, feature_index=0xFF,
                                    host_index=0xFF,
                                    fn_inversion_state=0xFF,
                                    fn_inversion_default_state=0xFF,
                                    capabilities_mask_reserved_bits=0x7F,
                                    capabilities_mask_fn_lock=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_f_lock_change_event
# end class FnInversionForMultiHostDevicesInstantiationTestCase


class FnInversionForMultiHostDevicesTestCase(TestCase):
    """
    Test ``FnInversionForMultiHostDevices`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            FnInversionForMultiHostDevicesV0.VERSION: {
                "cls": FnInversionForMultiHostDevicesV0,
                "interfaces": {
                    "get_global_fn_inversion_cls": GetGlobalFnInversion,
                    "get_global_fn_inversion_response_cls": GetGlobalFnInversionResponse,
                    "set_global_fn_inversion_cls": SetGlobalFnInversion,
                    "set_global_fn_inversion_response_cls": SetGlobalFnInversionResponse,
                    "f_lock_change_event_cls": FLockChangeEvent,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``FnInversionForMultiHostDevicesFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(FnInversionForMultiHostDevicesFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``FnInversionForMultiHostDevicesFactory`` using out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                FnInversionForMultiHostDevicesFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``FnInversionForMultiHostDevicesFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            fn_inversion_factory = FnInversionForMultiHostDevicesFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(fn_inversion_factory, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(fn_inversion_factory, interface)
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
            fn_inversion = FnInversionForMultiHostDevicesFactory.create(version)
            self.assertEqual(fn_inversion.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class FnInversionForMultiHostDevicesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
