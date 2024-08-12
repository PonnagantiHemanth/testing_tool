#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.gaming.test.modestatus_test
:brief: HID++ 2.0 ``ModeStatus`` test module
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.modestatus import GetDevConfig
from pyhid.hidpp.features.gaming.modestatus import GetDevConfigResponseV1
from pyhid.hidpp.features.gaming.modestatus import GetDevConfigResponseV2ToV3
from pyhid.hidpp.features.gaming.modestatus import GetModeStatus
from pyhid.hidpp.features.gaming.modestatus import GetModeStatusResponse
from pyhid.hidpp.features.gaming.modestatus import GetModeStatusResponseV3
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pyhid.hidpp.features.gaming.modestatus import ModeStatusBroadcastingEvent
from pyhid.hidpp.features.gaming.modestatus import ModeStatusFactory
from pyhid.hidpp.features.gaming.modestatus import ModeStatusV0
from pyhid.hidpp.features.gaming.modestatus import ModeStatusV1
from pyhid.hidpp.features.gaming.modestatus import ModeStatusV2
from pyhid.hidpp.features.gaming.modestatus import ModeStatusV3
from pyhid.hidpp.features.gaming.modestatus import SetModeStatus
from pyhid.hidpp.features.gaming.modestatus import SetModeStatusResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ModeStatusInstantiationTestCase(TestCase):
    """
    Test ``ModeStatus`` testing classes instantiations
    """

    @staticmethod
    def test_mode_status():
        """
        Test ``ModeStatus`` class instantiation
        """
        my_class = ModeStatus(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ModeStatus(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_mode_status

    @staticmethod
    def test_get_mode_status():
        """
        Test ``GetModeStatus`` class instantiation
        """
        my_class = GetModeStatus(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetModeStatus(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_mode_status

    @staticmethod
    def test_get_mode_status_response():
        """
        Test ``GetModeStatusResponse`` class instantiation
        """
        my_class = GetModeStatusResponse(device_index=0, feature_index=0,
                                         mode_status_0=False,
                                         power_mode=False,
                                         force_gaming_surface_mode=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetModeStatusResponse(device_index=0xff, feature_index=0xff,
                                         mode_status_0=True,
                                         power_mode=True,
                                         force_gaming_surface_mode=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_mode_status_response

    @staticmethod
    def test_set_mode_status():
        """
        Test ``SetModeStatus`` class instantiation
        """
        my_class = SetModeStatus(device_index=0, feature_index=0,
                                 mode_status_0=False,
                                 mode_status_1=0,
                                 changed_mask_0=0,
                                 changed_mask_1=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetModeStatus(device_index=0xff, feature_index=0xff,
                                 mode_status_0=True,
                                 mode_status_1=0xff,
                                 changed_mask_0=0xff,
                                 changed_mask_1=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_mode_status

    @staticmethod
    def test_set_mode_status_response():
        """
        Test ``SetModeStatusResponse`` class instantiation
        """
        my_class = SetModeStatusResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetModeStatusResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_mode_status_response

    @staticmethod
    def test_get_dev_config():
        """
        Test ``GetDevConfig`` class instantiation
        """
        my_class = GetDevConfig(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDevConfig(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_dev_config

    @staticmethod
    def test_get_dev_config_response_v1():
        """
        Test ``GetDevConfigResponseV1`` class instantiation
        """
        my_class = GetDevConfigResponseV1(device_index=0, feature_index=0,
                                          mode_status_0_changed_by_hw=False,
                                          mode_status_0_changed_by_sw=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDevConfigResponseV1(device_index=0xff, feature_index=0xff,
                                          mode_status_0_changed_by_hw=True,
                                          mode_status_0_changed_by_sw=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_dev_config_response_v1

    @staticmethod
    def test_get_dev_config_response_v2_to_v3():
        """
        Test ``GetDevConfigResponseV2ToV3`` class instantiation
        """
        my_class = GetDevConfigResponseV2ToV3(device_index=0, feature_index=0,
                                              mode_status_0_changed_by_hw=False,
                                              mode_status_0_changed_by_sw=False,
                                              power_save_mode=False,
                                              surface_mode=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDevConfigResponseV2ToV3(device_index=0xff, feature_index=0xff,
                                              mode_status_0_changed_by_hw=True,
                                              mode_status_0_changed_by_sw=True,
                                              power_save_mode=True,
                                              surface_mode=True)

        RootTestCase._long_function_class_checker(my_class)

    # end def test_get_dev_config_response_v2_to_v3

    @staticmethod
    def test_mode_status_broadcasting_event():
        """
        Test ``ModeStatusBroadcastingEvent`` class instantiation
        """
        my_class = ModeStatusBroadcastingEvent(device_index=0, feature_index=0,
                                               mode_status_0=False,
                                               power_mode=False,
                                               force_gaming_surface_mode=False,
                                               changed_mask_0=0,
                                               changed_mask_1=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ModeStatusBroadcastingEvent(device_index=0xff, feature_index=0xff,
                                               mode_status_0=True,
                                               power_mode=True,
                                               force_gaming_surface_mode=True,
                                               changed_mask_0=0xff,
                                               changed_mask_1=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_mode_status_broadcasting_event
# end class ModeStatusInstantiationTestCase


class ModeStatusTestCase(TestCase):
    """
    Test ``ModeStatus`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ModeStatusV0.VERSION: {
                "cls": ModeStatusV0,
                "interfaces": {
                    "get_mode_status_cls": GetModeStatus,
                    "get_mode_status_response_cls": GetModeStatusResponse,
                    "mode_status_broadcasting_event_cls": ModeStatusBroadcastingEvent,
                },
                "max_function_index": 0
            },
            ModeStatusV1.VERSION: {
                "cls": ModeStatusV1,
                "interfaces": {
                    "get_mode_status_cls": GetModeStatus,
                    "get_mode_status_response_cls": GetModeStatusResponse,
                    "set_mode_status_cls": SetModeStatus,
                    "set_mode_status_response_cls": SetModeStatusResponse,
                    "get_dev_config_cls": GetDevConfig,
                    "get_dev_config_response_cls": GetDevConfigResponseV1,
                    "mode_status_broadcasting_event_cls": ModeStatusBroadcastingEvent,
                },
                "max_function_index": 2
            },
            ModeStatusV2.VERSION: {
                "cls": ModeStatusV2,
                "interfaces": {
                    "get_mode_status_cls": GetModeStatus,
                    "get_mode_status_response_cls": GetModeStatusResponse,
                    "set_mode_status_cls": SetModeStatus,
                    "set_mode_status_response_cls": SetModeStatusResponse,
                    "get_dev_config_cls": GetDevConfig,
                    "get_dev_config_response_cls": GetDevConfigResponseV2ToV3,
                    "mode_status_broadcasting_event_cls": ModeStatusBroadcastingEvent,
                },
                "max_function_index": 2
            },
            ModeStatusV3.VERSION: {
                "cls": ModeStatusV3,
                "interfaces": {
                    "get_mode_status_cls": GetModeStatus,
                    "get_mode_status_response_cls": GetModeStatusResponseV3,
                    "set_mode_status_cls": SetModeStatus,
                    "set_mode_status_response_cls": SetModeStatusResponse,
                    "get_dev_config_cls": GetDevConfig,
                    "get_dev_config_response_cls": GetDevConfigResponseV2ToV3,
                    "mode_status_broadcasting_event_cls": ModeStatusBroadcastingEvent,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ModeStatusFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ModeStatusFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ModeStatusFactory`` using out of range versions
        """
        for version in [4, 5]:
            with self.assertRaises(KeyError):
                ModeStatusFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ModeStatusFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = ModeStatusFactory.create(version)
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
            obj = ModeStatusFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ModeStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
