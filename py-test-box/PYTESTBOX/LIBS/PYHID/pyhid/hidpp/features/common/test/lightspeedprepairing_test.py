#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.common.test.lightspeedprepairing_test
:brief: HID++ 2.0 ``LightspeedPrepairing`` test module
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.lightspeedprepairing import GetCapabilities
from pyhid.hidpp.features.common.lightspeedprepairing import GetCapabilitiesResponse
from pyhid.hidpp.features.common.lightspeedprepairing import GetPrepairingData
from pyhid.hidpp.features.common.lightspeedprepairing import GetPrepairingDataResponse
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairing
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairingFactory
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairingV0
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagement
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagementResponse
from pyhid.hidpp.features.common.lightspeedprepairing import SetLTK
from pyhid.hidpp.features.common.lightspeedprepairing import SetLTKResponse
from pyhid.hidpp.features.common.lightspeedprepairing import SetPrepairingData
from pyhid.hidpp.features.common.lightspeedprepairing import SetPrepairingDataResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LightspeedPrepairingInstantiationTestCase(TestCase):
    """
    Test ``LightspeedPrepairing`` testing classes instantiations
    """

    @staticmethod
    def test_lightspeed_prepairing():
        """
        Test ``LightspeedPrepairing`` class instantiation
        """
        my_class = LightspeedPrepairing(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = LightspeedPrepairing(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_lightspeed_prepairing

    @staticmethod
    def test_get_capabilities():
        """
        Test ``GetCapabilities`` class instantiation
        """
        my_class = GetCapabilities(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilities(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           use_attr=0,
                                           ls2=False,
                                           crush=False,
                                           ls=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(device_index=0xff, feature_index=0xff,
                                           use_attr=0x1,
                                           ls2=True,
                                           crush=True,
                                           ls=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_prepairing_management():
        """
        Test ``PrepairingManagement`` class instantiation
        """
        my_class = PrepairingManagement(device_index=0, feature_index=0,
                                        ls2=False,
                                        crush=False,
                                        ls=False,
                                        prepairing_management_control=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = PrepairingManagement(device_index=0xff, feature_index=0xff,
                                        ls2=True,
                                        crush=True,
                                        ls=True,
                                        prepairing_management_control=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_prepairing_management

    @staticmethod
    def test_prepairing_management_response():
        """
        Test ``PrepairingManagementResponse`` class instantiation
        """
        my_class = PrepairingManagementResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = PrepairingManagementResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_prepairing_management_response

    @staticmethod
    def test_set_ltk():
        """
        Test ``SetLTK`` class instantiation
        """
        my_class = SetLTK(device_index=0, feature_index=0,
                          ltk=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetLTK(device_index=0xff, feature_index=0xff,
                          ltk=HexList('FF' * (SetLTK.LEN.LTK // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_ltk

    @staticmethod
    def test_set_ltk_response():
        """
        Test ``SetLTKResponse`` class instantiation
        """
        my_class = SetLTKResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetLTKResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_ltk_response

    @staticmethod
    def test_set_prepairing_data():
        """
        Test ``SetPrepairingData`` class instantiation
        """
        my_class = SetPrepairingData(device_index=0, feature_index=0,
                                     data_type=0,
                                     pairing_address_base=0,
                                     address_dest=0,
                                     equad_attributes=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPrepairingData(device_index=0xff, feature_index=0xff,
                                     data_type=0xff,
                                     pairing_address_base=
                                     HexList('FF' * (LightspeedPrepairing.DataDetailsPairingAddress.
                                                     LEN.PAIRING_ADDRESS_BASE // 8)),
                                     address_dest=0xff,
                                     equad_attributes=HexList('FF' * (LightspeedPrepairing.DataDetailsEquadAttributes.
                                                                      LEN.EQUAD_ATTRIBUTES // 8))
                                     )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_prepairing_data

    @staticmethod
    def test_set_prepairing_data_response():
        """
        Test ``SetPrepairingDataResponse`` class instantiation
        """
        my_class = SetPrepairingDataResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPrepairingDataResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_prepairing_data_response

    @staticmethod
    def test_get_prepairing_data():
        """
        Test ``GetPrepairingData`` class instantiation
        """
        my_class = GetPrepairingData(device_index=0, feature_index=0,
                                     information_type=0,
                                     data_type=0,
                                     reserved=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPrepairingData(device_index=0xff, feature_index=0xff,
                                     information_type=0xff,
                                     data_type=0xff,
                                     reserved=HexList('FF' * (GetPrepairingData.LEN.RESERVED // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_prepairing_data

    @staticmethod
    def test_get_prepairing_data_response():
        """
        Test ``GetPrepairingDataResponse`` class instantiation
        """
        my_class = GetPrepairingDataResponse(device_index=0, feature_index=0,
                                             information_type=0,
                                             data_type=0,
                                             data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPrepairingDataResponse(device_index=0xff, feature_index=0xff,
                                             information_type=0xff,
                                             data_type=0xff,
                                             data=HexList('FF' * (GetPrepairingDataResponse.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_prepairing_data_response
# end class LightspeedPrepairingInstantiationTestCase


class LightspeedPrepairingTestCase(TestCase):
    """
    Test ``LightspeedPrepairing`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            LightspeedPrepairingV0.VERSION: {
                "cls": LightspeedPrepairingV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "prepairing_management_cls": PrepairingManagement,
                    "prepairing_management_response_cls": PrepairingManagementResponse,
                    "set_ltk_cls": SetLTK,
                    "set_ltk_response_cls": SetLTKResponse,
                    "set_prepairing_data_cls": SetPrepairingData,
                    "set_prepairing_data_response_cls": SetPrepairingDataResponse,
                    "get_prepairing_data_cls": GetPrepairingData,
                    "get_prepairing_data_response_cls": GetPrepairingDataResponse,
                },
                "max_function_index": 4
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``LightspeedPrepairingFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(LightspeedPrepairingFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``LightspeedPrepairingFactory`` using out of range versions
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                LightspeedPrepairingFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``LightspeedPrepairingFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = LightspeedPrepairingFactory.create(version)
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
            obj = LightspeedPrepairingFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class LightspeedPrepairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
