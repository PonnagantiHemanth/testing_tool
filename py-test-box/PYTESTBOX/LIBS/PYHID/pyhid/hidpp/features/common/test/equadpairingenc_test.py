#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.feature.common.test.equadpairingenc_test
    :brief: HID++ 2.0 eQuad Pairing Encryption test module
    :author: Christophe Roquebert
    :date:   2020/05/20
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.equadpairingenc import EquadPairingEncFactory
from pyhid.hidpp.features.common.equadpairingenc import EquadPairingEncInterface
from pyhid.hidpp.features.common.equadpairingenc import EquadPairingEncModel
from pyhid.hidpp.features.common.equadpairingenc import EquadPairingEncV0
from pyhid.hidpp.features.common.equadpairingenc import EquadPairingEnc
from pyhid.hidpp.features.common.equadpairingenc import GetPairingInfo
from pyhid.hidpp.features.common.equadpairingenc import GetPairingInfoResponse
from pyhid.hidpp.features.common.equadpairingenc import SetPairingInfo
from pyhid.hidpp.features.common.equadpairingenc import SetPairingInfoResponse
from pyhid.hidpp.features.common.equadpairingenc import SetEncKey
from pyhid.hidpp.features.common.equadpairingenc import SetEncKeyResponse
from pyhid.hidpp.features.common.equadpairingenc import PairingInfoFormat
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList, RandHexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class EquadPairingEncInstantiationTestCase(TestCase):
    """
    EquadPairingEnc testing class
    """

    @staticmethod
    def test_equad_pairing_enc():
        """
        Tests EquadPairingEnc class instantiation
        """
        my_class = EquadPairingEnc(device_index=0, feature_index=0)
        RootTestCase._top_level_class_checker(my_class)

        my_class = EquadPairingEnc(device_index=0xFF, feature_index=0xFF)
        RootTestCase._top_level_class_checker(my_class)
    # end def test_equad_pairing_enc

    @staticmethod
    def test_get_pairing_info():
        """
        Tests GetPairingInfo class instantiation
        """
        my_class = GetPairingInfo(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetPairingInfo(device_index=0xFF, feature_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_pairing_info

    @staticmethod
    def test_get_pairing_info_response():
        """
        Tests GetPairingInfo response class instantiation
        """
        my_class = GetPairingInfoResponse(device_index=0x00, feature_index=0x00,
                                          addr_base=HexList("00"*(PairingInfoFormat.LEN.ADDR_BASE//8)),
                                          addr_dest=HexList("00"*(PairingInfoFormat.LEN.ADDR_DEST//8)),)
        RootTestCase._long_function_class_checker(my_class)

        addr_base_value = RandHexList(PairingInfoFormat.LEN.ADDR_BASE//8)
        my_class = GetPairingInfoResponse(device_index=RandHexList(1), feature_index=RandHexList(1),
                                          addr_base=addr_base_value,
                                          addr_dest=RandHexList(PairingInfoFormat.LEN.ADDR_DEST//8),
                                          equad_attrb_tpad_info=False,
                                          equad_attrb_16bit_mse=False,
                                          equad_attrb_high_rpt_rate=False,
                                          equad_attrb_otp_device=False,
                                          equad_attrb_multidevice=False,
                                          equad_attrb_ota_dfu=False,
                                          equad_attrb_encryption=False,
                                          eqattr_01_05=RandHexList(PairingInfoFormat.LEN.EQATTR_01_05//8),
                                          serial=RandHexList(PairingInfoFormat.LEN.SERIAL//8),
                                          flags_use_attr=False)
        RootTestCase._long_function_class_checker(my_class)
        assert(my_class.addr_base == addr_base_value)

        my_class = GetPairingInfoResponse(device_index=0xFF, feature_index=0xFF,
                                          addr_base=HexList("FF"*(PairingInfoFormat.LEN.ADDR_BASE//8)),
                                          addr_dest=HexList("FF"*(PairingInfoFormat.LEN.ADDR_DEST//8)),
                                          equad_attrb_tpad_info=True,
                                          equad_attrb_16bit_mse=True,
                                          equad_attrb_high_rpt_rate=True,
                                          equad_attrb_otp_device=True,
                                          equad_attrb_multidevice=True,
                                          equad_attrb_ota_dfu=True,
                                          equad_attrb_encryption=True,
                                          eqattr_01_05=HexList("FF"*(PairingInfoFormat.LEN.EQATTR_01_05//8)),
                                          serial=HexList("FF"*(PairingInfoFormat.LEN.SERIAL//8)),
                                          flags_use_attr=True)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_pairing_info_response

    @staticmethod
    def test_set_pairing_info():
        """
        Tests SetPairingInfo class instantiation
        """
        my_class = SetPairingInfo(device_index=0x00, feature_index=0x00,
                                          addr_base=HexList("00"*(PairingInfoFormat.LEN.ADDR_BASE//8)),
                                          addr_dest=HexList("00"*(PairingInfoFormat.LEN.ADDR_DEST//8)),)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPairingInfo(device_index=RandHexList(1), feature_index=RandHexList(1),
                                          addr_base=RandHexList(PairingInfoFormat.LEN.ADDR_BASE//8),
                                          addr_dest=RandHexList(PairingInfoFormat.LEN.ADDR_DEST//8),
                                          equad_attrb_tpad_info=False,
                                          equad_attrb_16bit_mse=False,
                                          equad_attrb_high_rpt_rate=False,
                                          equad_attrb_otp_device=False,
                                          equad_attrb_multidevice=False,
                                          equad_attrb_ota_dfu=False,
                                          equad_attrb_encryption=False,
                                          eqattr_01_05=RandHexList(PairingInfoFormat.LEN.EQATTR_01_05//8),
                                          serial=RandHexList(PairingInfoFormat.LEN.SERIAL//8),
                                          flags_use_attr=False)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPairingInfo(device_index=0xFF, feature_index=0xFF,
                                          addr_base=HexList("FF"*(PairingInfoFormat.LEN.ADDR_BASE//8)),
                                          addr_dest=HexList("FF"*(PairingInfoFormat.LEN.ADDR_DEST//8)),
                                          equad_attrb_tpad_info=True,
                                          equad_attrb_16bit_mse=True,
                                          equad_attrb_high_rpt_rate=True,
                                          equad_attrb_otp_device=True,
                                          equad_attrb_multidevice=True,
                                          equad_attrb_ota_dfu=True,
                                          equad_attrb_encryption=True,
                                          eqattr_01_05=HexList("FF"*(PairingInfoFormat.LEN.EQATTR_01_05//8)),
                                          serial=HexList("FF"*(PairingInfoFormat.LEN.SERIAL//8)),
                                          flags_use_attr=True)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_pairing_info

    @staticmethod
    def test_set_pairing_info_response():
        """
        Tests GetPairingInfo class instantiation
        """
        my_class = SetPairingInfoResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetPairingInfoResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_pairing_info_response

    @staticmethod
    def test_set_enc_key():
        """
        Tests SetEncKey class instantiation
        """
        my_class = SetEncKey(device_index=0x00, feature_index=0x00, enc_key=HexList("00"*(SetEncKey.LEN.ENC_KEY//8)),)
        RootTestCase._long_function_class_checker(my_class)

        enc_key_value = RandHexList(SetEncKey.LEN.ENC_KEY//8)
        my_class = SetEncKey(device_index=RandHexList(1), feature_index=RandHexList(1), enc_key=enc_key_value)
        RootTestCase._long_function_class_checker(my_class)
        assert(my_class.enc_key == enc_key_value)

        my_class = SetEncKey(device_index=0xFF, feature_index=0xFF, enc_key=HexList("FF"*(SetEncKey.LEN.ENC_KEY//8)),)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_enc_key

    @staticmethod
    def test_set_enc_key_response():
        """
        Tests SetEncKey response class instantiation
        """
        my_class = SetEncKeyResponse(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetEncKeyResponse(device_index=RandHexList(1), feature_index=RandHexList(1))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetEncKeyResponse(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_enc_key_response
# end class EquadPairingEncInstantiationTestCase


class EquadPairingEncTestCase(TestCase):
    """
    Equad Pairing Encryption factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": EquadPairingEncV0,
                "interfaces": {
                    "get_pairing_info_cls": GetPairingInfo,
                    "set_pairing_info_cls": SetPairingInfo,
                    "set_enc_key_cls": SetEncKey,
                    "get_pairing_info_response_cls": GetPairingInfoResponse,
                    "set_pairing_info_response_cls": SetPairingInfoResponse,
                    "set_enc_key_response_cls": SetEncKeyResponse,
                },
                "max_function_index": 2
            },
        }

    # end def setUpClass

    def test_equad_pairing_enc_factory(self):
        """
        Tests Equad Pairing Enc Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(EquadPairingEncFactory.create(version)), expected["cls"])
        # end for loop

    # end def test_equad_pairing_enc_factory

    def test_equad_pairing_enc_factory_version_out_of_range(self):
        """
        Tests Equad Pairing Enc Factory with out of range versions
        """
        for version in [1, 2, 3]:
            with self.assertRaises(KeyError):
                EquadPairingEncFactory.create(version)
            # end with
        # end for

    # end def test_equad_pairing_enc_factory_version_out_of_range

    def test_equad_pairing_enc_factory_interfaces(self):
        """
        Check Equad Pairing Enc Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            equad_pairing_enc = EquadPairingEncFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(equad_pairing_enc, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(equad_pairing_enc, interface)
                # end if
            # end for loop
        # end for loop

    # end def test_equad_pairing_enc_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            equad_pairing_enc = EquadPairingEncFactory.create(version)
            self.assertEqual(equad_pairing_enc.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class EquadPairingEncTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
