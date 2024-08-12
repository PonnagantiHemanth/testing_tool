#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.gaming.test.brakeforce_test
:brief: HID++ 2.0 ``BrakeForce`` test module
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.brakeforce import BrakeForce
from pyhid.hidpp.features.gaming.brakeforce import BrakeForceFactory
from pyhid.hidpp.features.gaming.brakeforce import BrakeForceV0
from pyhid.hidpp.features.gaming.brakeforce import GetInfo
from pyhid.hidpp.features.gaming.brakeforce import GetInfoResponse
from pyhid.hidpp.features.gaming.brakeforce import GetMaxLoadPoint
from pyhid.hidpp.features.gaming.brakeforce import GetMaxLoadPointResponse
from pyhid.hidpp.features.gaming.brakeforce import MaxLoadPointChangedEvent
from pyhid.hidpp.features.gaming.brakeforce import SetMaxLoadPoint
from pyhid.hidpp.features.gaming.brakeforce import SetMaxLoadPointResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrakeForceInstantiationTestCase(TestCase):
    """
    Test ``BrakeForce`` testing classes instantiations
    """

    @staticmethod
    def test_brake_force():
        """
        Test ``BrakeForce`` class instantiation
        """
        my_class = BrakeForce(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = BrakeForce(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_brake_force

    @staticmethod
    def test_get_info():
        """
        Test ``GetInfo`` class instantiation
        """
        my_class = GetInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetInfo(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_info

    @staticmethod
    def test_get_info_response():
        """
        Test ``GetInfoResponse`` class instantiation
        """
        my_class = GetInfoResponse(device_index=0, feature_index=0,
                                   maximum_kg_load=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponse(device_index=0xff, feature_index=0xff,
                                   maximum_kg_load=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response

    @staticmethod
    def test_get_max_load_point():
        """
        Test ``GetMaxLoadPoint`` class instantiation
        """
        my_class = GetMaxLoadPoint(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetMaxLoadPoint(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_max_load_point

    @staticmethod
    def test_get_max_load_point_response():
        """
        Test ``GetMaxLoadPointResponse`` class instantiation
        """
        my_class = GetMaxLoadPointResponse(device_index=0, feature_index=0,
                                           maximum_load_point=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetMaxLoadPointResponse(device_index=0xff, feature_index=0xff,
                                           maximum_load_point=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_max_load_point_response

    @staticmethod
    def test_set_max_load_point():
        """
        Test ``SetMaxLoadPoint`` class instantiation
        """
        my_class = SetMaxLoadPoint(device_index=0, feature_index=0,
                                   maximum_load_point=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetMaxLoadPoint(device_index=0xff, feature_index=0xff,
                                   maximum_load_point=0xffff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_max_load_point

    @staticmethod
    def test_set_max_load_point_response():
        """
        Test ``SetMaxLoadPointResponse`` class instantiation
        """
        my_class = SetMaxLoadPointResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetMaxLoadPointResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_max_load_point_response

    @staticmethod
    def test_max_load_point_changed_event():
        """
        Test ``MaxLoadPointChangedEvent`` class instantiation
        """
        my_class = MaxLoadPointChangedEvent(device_index=0, feature_index=0,
                                            maximum_load_point=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = MaxLoadPointChangedEvent(device_index=0xff, feature_index=0xff,
                                            maximum_load_point=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_max_load_point_changed_event
# end class BrakeForceInstantiationTestCase


class BrakeForceTestCase(TestCase):
    """
    Test ``BrakeForce`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            BrakeForceV0.VERSION: {
                "cls": BrakeForceV0,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponse,
                    "get_max_load_point_cls": GetMaxLoadPoint,
                    "get_max_load_point_response_cls": GetMaxLoadPointResponse,
                    "set_max_load_point_cls": SetMaxLoadPoint,
                    "set_max_load_point_response_cls": SetMaxLoadPointResponse,
                    "max_load_point_changed_event_cls": MaxLoadPointChangedEvent,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``BrakeForceFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(BrakeForceFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``BrakeForceFactory`` with out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                BrakeForceFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``BrakeForceFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = BrakeForceFactory.create(version)
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
            obj = BrakeForceFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class BrakeForceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
