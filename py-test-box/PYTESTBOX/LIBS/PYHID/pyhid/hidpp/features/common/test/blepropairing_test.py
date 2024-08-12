#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.feature.common.test.bleproprepairing_test
    :brief: HID++ 2.0 BLE Pro pairing test module
    :author: Christophe Roquebert
    :date:   2020/05/20
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingFactory
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingV0
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairing
from pyhid.hidpp.features.common.bleproprepairing import PrepairingDataManagement
from pyhid.hidpp.features.common.bleproprepairing import PrepairingDataManagementResponse
from pyhid.hidpp.features.common.bleproprepairing import SetKey
from pyhid.hidpp.features.common.bleproprepairing import SetLtk
from pyhid.hidpp.features.common.bleproprepairing import SetLtkResponse
from pyhid.hidpp.features.common.bleproprepairing import SetIrkRemote
from pyhid.hidpp.features.common.bleproprepairing import SetIrkRemoteResponse
from pyhid.hidpp.features.common.bleproprepairing import SetIrkLocal
from pyhid.hidpp.features.common.bleproprepairing import SetIrkLocalResponse
from pyhid.hidpp.features.common.bleproprepairing import SetCsrkRemote
from pyhid.hidpp.features.common.bleproprepairing import SetCsrkRemoteResponse
from pyhid.hidpp.features.common.bleproprepairing import SetCsrkLocal
from pyhid.hidpp.features.common.bleproprepairing import SetCsrkLocalResponse
from pyhid.hidpp.features.common.bleproprepairing import SetPrepairingData
from pyhid.hidpp.features.common.bleproprepairing import SetPrepairingDataResponse
from pyhid.hidpp.features.common.bleproprepairing import GetPrepairingData
from pyhid.hidpp.features.common.bleproprepairing import GetPrepairingDataResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList, RandHexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleProPrepairingInstantiationTestCase(TestCase):
    """
    BleProPrepairing testing class
    """

    @staticmethod
    def test_ble_pro_pairing():
        """
        Tests BleProPrepairing class instantiation
        """
        my_class = BleProPrepairing(device_index=0, feature_index=0)
        RootTestCase._top_level_class_checker(my_class)

        my_class = BleProPrepairing(device_index=0xFF, feature_index=0xFF)
        RootTestCase._top_level_class_checker(my_class)
    # end def test_ble_pro_pairing

    @staticmethod
    def test_prepairing_data_management():
        """
        Tests prepairing data management class instantiation
        """
        my_class = PrepairingDataManagement(
            device_index=0x00,
            feature_index=0x00,
            prepairing_slot=RandHexList(PrepairingDataManagement.LEN.PREPAIRING_SLOT//8),
            mode=PrepairingDataManagement.MODE.START)
        RootTestCase._short_function_class_checker(my_class)

        my_class = PrepairingDataManagement(
            device_index=RandHexList(1),
            feature_index=RandHexList(1),
            prepairing_slot=RandHexList(PrepairingDataManagement.LEN.PREPAIRING_SLOT//8),
            mode=PrepairingDataManagement.MODE.STORE)
        RootTestCase._short_function_class_checker(my_class)

        my_class = PrepairingDataManagement(
            device_index=RandHexList(1),
            feature_index=RandHexList(1),
            prepairing_slot=RandHexList(PrepairingDataManagement.LEN.PREPAIRING_SLOT//8),
            mode=PrepairingDataManagement.MODE.DELETE)
        RootTestCase._short_function_class_checker(my_class)

        my_class = PrepairingDataManagement(device_index=0xFF, feature_index=0xFF, prepairing_slot=0xFF,
                                            mode=PrepairingDataManagement.MODE.RFU)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_prepairing_data_management

    @staticmethod
    def test_prepairing_data_management_response():
        """
        Tests Prepairing Data Management response class instantiation
        """
        my_class = PrepairingDataManagementResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = PrepairingDataManagementResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_prepairing_data_management_response

    @staticmethod
    def test_set_key():
        """
        Tests SetKey class instantiation
        """
        my_class = SetKey(device_index=0x00, feature_index=0x00, key=HexList("00"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetKey(device_index=0xFF, feature_index=0xFF, key=HexList("FF"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetKey(device_index=0xFF, feature_index=0xFF, key=RandHexList(SetKey.LEN.KEY//8))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_key

    @staticmethod
    def test_set_ltk():
        """
        Tests SetLtk class instantiation
        """
        my_class = SetLtk(device_index=0x00, feature_index=0x00, ltk=HexList("00"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetLtk(device_index=0xFF, feature_index=0xFF, ltk=HexList("FF"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetLtk(device_index=0xFF, feature_index=0xFF, ltk=RandHexList(SetKey.LEN.KEY//8))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_ltk

    @staticmethod
    def test_set_ltk_response():
        """
        Tests Set Ltk response class instantiation
        """
        my_class = SetLtkResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetLtkResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_ltk_response

    @staticmethod
    def test_set_irk_remote():
        """
        Tests SetIrkRemote class instantiation
        """
        my_class = SetIrkRemote(device_index=0x00, feature_index=0x00, irk_remote=HexList("00"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIrkRemote(device_index=0xFF, feature_index=0xFF, irk_remote=HexList("FF"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIrkRemote(device_index=0xFF, feature_index=0xFF, irk_remote=RandHexList(SetKey.LEN.KEY//8))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_irk_remote

    @staticmethod
    def test_set_irk_remote_response():
        """
        Tests Set Irk Remote response class instantiation
        """
        my_class = SetIrkRemoteResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIrkRemoteResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_irk_remote_response

    @staticmethod
    def test_set_irk_local():
        """
        Tests SetIrkLocal class instantiation
        """
        my_class = SetIrkLocal(device_index=0x00, feature_index=0x00, irk_local=HexList("00"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIrkLocal(device_index=0xFF, feature_index=0xFF, irk_local=HexList("FF"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIrkLocal(device_index=0xFF, feature_index=0xFF, irk_local=RandHexList(SetKey.LEN.KEY//8))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_irk_local

    @staticmethod
    def test_set_irk_local_response():
        """
        Tests Set Irk Local response class instantiation
        """
        my_class = SetIrkLocalResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIrkLocalResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_irk_local_response

    @staticmethod
    def test_set_csrk_remote():
        """
        Tests SetCsrkRemote class instantiation
        """
        my_class = SetCsrkRemote(device_index=0x00, feature_index=0x00, csrk_remote=HexList("00"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCsrkRemote(device_index=0xFF, feature_index=0xFF, csrk_remote=HexList("FF"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCsrkRemote(device_index=0xFF, feature_index=0xFF, csrk_remote=RandHexList(SetKey.LEN.KEY//8))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_csrk_remote

    @staticmethod
    def test_set_csrk_remote_response():
        """
        Tests SetCsrkRemoteResponse class instantiation
        """
        my_class = SetCsrkRemoteResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCsrkRemoteResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_csrk_remote_response

    @staticmethod
    def test_set_csrk_local():
        """
        Tests SetCsrkLocal class instantiation
        """
        my_class = SetCsrkLocal(device_index=0x00, feature_index=0x00, csrk_local=HexList("00"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCsrkLocal(device_index=0xFF, feature_index=0xFF, csrk_local=HexList("FF"*(SetKey.LEN.KEY//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCsrkLocal(device_index=0xFF, feature_index=0xFF, csrk_local=RandHexList(SetKey.LEN.KEY//8))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_csrk_local

    @staticmethod
    def test_set_csrk_local_response():
        """
        Tests SetCsrkLocalResponse class instantiation
        """
        my_class = SetCsrkLocalResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetCsrkLocalResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_csrk_local_response

    @staticmethod
    def test_set_prepairing_data():
        """
        Tests SetPrepairingData class instantiation
        """
        my_class = SetPrepairingData(device_index=0x00, feature_index=0x00, data_type=SetPrepairingData.TYPE.REMOTE,
                                     remote_address=HexList("00"*(SetPrepairingData.LEN.ADDRESS//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPrepairingData(device_index=0x00, feature_index=0x00, data_type=SetPrepairingData.TYPE.LOCAL,
                                     local_address=RandHexList(SetPrepairingData.LEN.ADDRESS//8))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPrepairingData(device_index=0x00, feature_index=0x00, data_type=SetPrepairingData.TYPE.RFU,
                                     address=RandHexList(SetPrepairingData.LEN.ADDRESS//8))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPrepairingData(device_index=0xFF, feature_index=0xFF, data_type=0xFF,
                                     address=HexList("FF"*(SetPrepairingData.LEN.ADDRESS//8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_prepairing_data

    @staticmethod
    def test_set_prepairing_data_response():
        """
        Tests SetPrepairingDataResponse class instantiation
        """
        my_class = SetPrepairingDataResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPrepairingDataResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_prepairing_data_response

    @staticmethod
    def test_get_prepairing_data():
        """
        Tests GetPrepairingData class instantiation
        """
        my_class = GetPrepairingData(device_index=0x00, feature_index=0x00, data_type=SetPrepairingData.TYPE.REMOTE)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPrepairingData(device_index=RandHexList(1),
                                     feature_index=RandHexList(1),
                                     data_type=SetPrepairingData.TYPE.LOCAL)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPrepairingData(device_index=0xFF, feature_index=0xFF, data_type=SetPrepairingData.TYPE.RFU)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_prepairing_data

    @staticmethod
    def test_get_prepairing_data_response():
        """
        Tests GetPrepairingDataResponse class instantiation
        """
        my_class = GetPrepairingDataResponse(device_index=0x00, feature_index=0x00,
                                             data_type=SetPrepairingData.TYPE.REMOTE,
                                             remote_address=HexList("00"*(SetPrepairingData.LEN.ADDRESS//8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPrepairingDataResponse(device_index=RandHexList(1), feature_index=RandHexList(1),
                                             data_type=SetPrepairingData.TYPE.LOCAL,
                                             local_address=RandHexList(SetPrepairingData.LEN.ADDRESS//8))
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPrepairingDataResponse(device_index=0xFF, feature_index=0xFF,
                                             data_type=SetPrepairingData.TYPE.RFU,
                                             local_address=HexList("FF"*(SetPrepairingData.LEN.ADDRESS//8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_prepairing_data_response
# end class BleProPrepairingInstantiationTestCase


class BleProPrepairingTestCase(TestCase):
    """
    Ble Pro Pairing factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": BleProPrepairingV0,
                "interfaces": {
                    "prepairing_data_management_cls": PrepairingDataManagement,
                    "set_ltk_cls": SetLtk,
                    "set_irk_remote_cls": SetIrkRemote,
                    "set_irk_local_cls": SetIrkLocal,
                    "set_csrk_remote_cls": SetCsrkRemote,
                    "set_csrk_local_cls": SetCsrkLocal,
                    "set_prepairing_data_cls": SetPrepairingData,
                    "get_prepairing_data_cls": GetPrepairingData,
                    "prepairing_data_management_response_cls": PrepairingDataManagementResponse,
                    "set_ltk_response_cls": SetLtkResponse,
                    "set_irk_remote_response_cls": SetIrkRemoteResponse,
                    "set_irk_local_response_cls": SetIrkLocalResponse,
                    "set_csrk_remote_response_cls": SetCsrkRemoteResponse,
                    "set_csrk_local_response_cls": SetCsrkLocalResponse,
                    "set_prepairing_data_response_cls": SetPrepairingDataResponse,
                    "get_prepairing_data_response_cls": GetPrepairingDataResponse,
                },
                "max_function_index": 7
            },
        }
    # end def setUpClass

    def test_ble_pro_pairing_factory(self):
        """
        Tests BLE Pro pairing Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(BleProPrepairingFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_ble_pro_pairing_factory

    def test_ble_pro_pairing_factory_version_out_of_range(self):
        """
        Tests BLE Pro pairing Factory with out of range versions
        """
        for version in [1, 2, 3]:
            with self.assertRaises(KeyError):
                BleProPrepairingFactory.create(version)
            # end with
        # end for
    # end def test_ble_pro_pairing_factory_version_out_of_range

    def test_ble_pro_pairing_factory_interfaces(self):
        """
        Check BLE Pro pairing Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            ble_pro_pairing = BleProPrepairingFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(ble_pro_pairing, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(ble_pro_pairing, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_ble_pro_pairing_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            ble_pro_pairing = BleProPrepairingFactory.create(version)
            self.assertEqual(ble_pro_pairing.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class BleProPrepairingTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
