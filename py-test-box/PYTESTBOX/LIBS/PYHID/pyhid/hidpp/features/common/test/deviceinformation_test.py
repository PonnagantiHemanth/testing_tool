#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.feature.common.test.deviceinformation_test
:brief: HID++ 2.0 device information test module
:author: Stanislas Cottard
:date: 2019/12/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationFactory
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationV1
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationV2
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationV3
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationV4
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationV5
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationV6
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationV7
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationV8
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoResponseV1
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoResponseV2ToV3
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoResponseV4ToV5
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoResponseV6ToV8
from pyhid.hidpp.features.common.deviceinformation import GetDeviceInfoV1ToV8
from pyhid.hidpp.features.common.deviceinformation import GetDeviceSerialNumberResponseV4ToV8
from pyhid.hidpp.features.common.deviceinformation import GetDeviceSerialNumberV4ToV8
from pyhid.hidpp.features.common.deviceinformation import GetFwInfoResponseV1ToV7
from pyhid.hidpp.features.common.deviceinformation import GetFwInfoResponseV8
from pyhid.hidpp.features.common.deviceinformation import GetFwInfoV1ToV8
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DeviceInformationInstantiationTestCase(TestCase):
    """
    DeviceInformation testing classes instantiations
    """

    @staticmethod
    def test_device_information():
        """
        Test DeviceInformation class instantiation
        """
        my_class = DeviceInformation(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = DeviceInformation(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_device_information

    @staticmethod
    def test_get_device_info_v1_to_v8():
        """
        Test ``GetDeviceInfoV1ToV8`` class instantiation
        """
        my_class = GetDeviceInfoV1ToV8(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDeviceInfoV1ToV8(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_device_info_v1_to_v8

    @staticmethod
    def test_get_device_info_response_v1():
        """
        Test GetDeviceInfoResponseV1 class instantiation
        """
        my_class = GetDeviceInfoResponseV1(device_index=0,
                                           feature_index=0,
                                           entity_count=0,
                                           unit_id=HexList('00' * (
                                                   GetDeviceInfoResponseV1.LEN.UNIT_ID // 8)),
                                           usb=False,
                                           e_quad=False,
                                           btle=False,
                                           bt=False,
                                           model_id=HexList('00' * (
                                                   GetDeviceInfoResponseV1.LEN.MODEL_ID // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceInfoResponseV1(device_index=0xFF,
                                           feature_index=0xFF,
                                           entity_count=0xFF,
                                           unit_id=HexList('FF' * (
                                                   GetDeviceInfoResponseV1.LEN.UNIT_ID // 8)),
                                           usb=True,
                                           e_quad=True,
                                           btle=True,
                                           bt=True,
                                           model_id=HexList('FF' * (
                                                   GetDeviceInfoResponseV1.LEN.MODEL_ID // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_info_response_v1

    @staticmethod
    def test_get_device_info_response_v2_to_v3():
        """
        Test GetDeviceInfoResponseV2ToV3 class instantiation
        """
        my_class = GetDeviceInfoResponseV2ToV3(device_index=0,
                                               feature_index=0,
                                               entity_count=0,
                                               unit_id=HexList('00' * (
                                                       GetDeviceInfoResponseV2ToV3.LEN.UNIT_ID // 8)),
                                               usb=False,
                                               e_quad=False,
                                               btle=False,
                                               bt=False,
                                               model_id=HexList('00' * (
                                                       GetDeviceInfoResponseV2ToV3.LEN.MODEL_ID // 8)),
                                               extended_model_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceInfoResponseV2ToV3(device_index=0xFF,
                                               feature_index=0xFF,
                                               entity_count=0xFF,
                                               unit_id=HexList('FF' * (
                                                       GetDeviceInfoResponseV2ToV3.LEN.UNIT_ID // 8)),
                                               usb=True,
                                               e_quad=True,
                                               btle=True,
                                               bt=True,
                                               model_id=HexList('FF' * (
                                                       GetDeviceInfoResponseV2ToV3.LEN.MODEL_ID // 8)),
                                               extended_model_id=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_info_response_v2_to_v3

    @staticmethod
    def test_get_device_info_response_v4_to_v5():
        """
        Test GetDeviceInfoResponseV4ToV5 class instantiation
        """
        my_class = GetDeviceInfoResponseV4ToV5(device_index=0,
                                               feature_index=0,
                                               entity_count=0,
                                               unit_id=HexList('00' * (
                                                       GetDeviceInfoResponseV4ToV5.LEN.UNIT_ID // 8)),
                                               usb=False,
                                               e_quad=False,
                                               btle=False,
                                               bt=False,
                                               model_id=HexList('00' * (
                                                       GetDeviceInfoResponseV4ToV5.LEN.MODEL_ID // 8)),
                                               extended_model_id=0,
                                               serial_number=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceInfoResponseV4ToV5(device_index=0xFF,
                                               feature_index=0xFF,
                                               entity_count=0xFF,
                                               unit_id=HexList('FF' * (
                                                       GetDeviceInfoResponseV4ToV5.LEN.UNIT_ID // 8)),
                                               usb=True,
                                               e_quad=True,
                                               btle=True,
                                               bt=True,
                                               model_id=HexList('FF' * (
                                                       GetDeviceInfoResponseV4ToV5.LEN.MODEL_ID // 8)),
                                               extended_model_id=0xFF,
                                               serial_number=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_info_response_v4_to_v5

    @staticmethod
    def test_get_device_info_response_v6_to_v8():
        """
        Test GetDeviceInfoResponseV6ToV8 class instantiation
        """
        my_class = GetDeviceInfoResponseV6ToV8(device_index=0,
                                               feature_index=0,
                                               entity_count=0,
                                               unit_id=HexList('00' * (
                                                       GetDeviceInfoResponseV6ToV8.LEN.UNIT_ID // 8)),
                                               serial=False,
                                               usb=False,
                                               e_quad=False,
                                               btle=False,
                                               bt=False,
                                               model_id=HexList('00' * (
                                                       GetDeviceInfoResponseV6ToV8.LEN.MODEL_ID // 8)),
                                               extended_model_id=0,
                                               serial_number=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceInfoResponseV6ToV8(device_index=0xFF,
                                               feature_index=0xFF,
                                               entity_count=0xFF,
                                               unit_id=HexList('FF' * (
                                                       GetDeviceInfoResponseV6ToV8.LEN.UNIT_ID // 8)),
                                               serial=True,
                                               usb=True,
                                               e_quad=True,
                                               btle=True,
                                               bt=True,
                                               model_id=HexList('FF' * (
                                                       GetDeviceInfoResponseV6ToV8.LEN.MODEL_ID // 8)),
                                               extended_model_id=0xFF,
                                               serial_number=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_info_response_v6_to_v8

    @staticmethod
    def test_get_fw_info_v1_to_v8():
        """
        Test GetFwInfoV1ToV8 class instantiation
        """
        my_class = GetFwInfoV1ToV8(device_index=0, feature_index=0, entity_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetFwInfoV1ToV8(device_index=0xFF, feature_index=0xFF, entity_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_fw_info_v1_to_v8

    @staticmethod
    def test_get_fw_info_response_v1_to_v7():
        """
        Test GetFwInfoResponseV1ToV7 class instantiation
        """
        my_class = GetFwInfoResponseV1ToV7(
            device_index=0,
            feature_index=0,
            fw_type=0,
            fw_prefix=HexList('00' * (GetFwInfoResponseV1ToV7.LEN.FW_PREFIX // 8)),
            fw_number=HexList('00' * (GetFwInfoResponseV1ToV7.LEN.FW_NUMBER // 8)),
            fw_revision=HexList('00' * (GetFwInfoResponseV1ToV7.LEN.FW_REVISION // 8)),
            fw_build=HexList('00' * (GetFwInfoResponseV1ToV7.LEN.FW_BUILD // 8)),
            active=False,
            transport_id=0,
            extra_version_information=HexList('00' * (
                    GetFwInfoResponseV1ToV7.LEN.EXTRA_VERSION_INFORMATION // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetFwInfoResponseV1ToV7(
            device_index=0xFF,
            feature_index=0xFF,
            fw_type=0xFF,
            fw_prefix=HexList('FF' * (GetFwInfoResponseV1ToV7.LEN.FW_PREFIX // 8)),
            fw_number=HexList('99' * (GetFwInfoResponseV1ToV7.LEN.FW_NUMBER // 8)),
            fw_revision=HexList('99' * (GetFwInfoResponseV1ToV7.LEN.FW_REVISION // 8)),
            fw_build=HexList('99' * (GetFwInfoResponseV1ToV7.LEN.FW_BUILD // 8)),
            active=True,
            transport_id=0xFF,
            extra_version_information=HexList('FF' * (
                    GetFwInfoResponseV1ToV7.LEN.EXTRA_VERSION_INFORMATION // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_fw_info_response_v1_to_v7

    @staticmethod
    def test_get_fw_info_response_v8():
        """
        Test GetFwInfoResponseV8 class instantiation
        """
        my_class = GetFwInfoResponseV8(
            device_index=0,
            feature_index=0,
            fw_type=0,
            fw_prefix=HexList('00' * (GetFwInfoResponseV8.LEN.FW_PREFIX // 8)),
            fw_number=HexList('00' * (GetFwInfoResponseV8.LEN.FW_NUMBER // 8)),
            fw_revision=HexList('00' * (GetFwInfoResponseV8.LEN.FW_REVISION // 8)),
            fw_build=HexList('00' * (GetFwInfoResponseV8.LEN.FW_BUILD // 8)),
            slot_id=False,
            invalid=False,
            active=False,
            transport_id=0,
            extra_version_information=HexList('00' * (
                    GetFwInfoResponseV8.LEN.EXTRA_VERSION_INFORMATION // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetFwInfoResponseV8(
            device_index=0xFF,
            feature_index=0xFF,
            fw_type=0xFF,
            fw_prefix=HexList('FF' * (GetFwInfoResponseV8.LEN.FW_PREFIX // 8)),
            fw_number=HexList('99' * (GetFwInfoResponseV8.LEN.FW_NUMBER // 8)),
            fw_revision=HexList('99' * (GetFwInfoResponseV8.LEN.FW_REVISION // 8)),
            fw_build=HexList('99' * (GetFwInfoResponseV8.LEN.FW_BUILD // 8)),
            slot_id=True,
            invalid=True,
            active=True,
            transport_id=0xFF,
            extra_version_information=HexList('FF' * (
                    GetFwInfoResponseV8.LEN.EXTRA_VERSION_INFORMATION // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_fw_info_response_v8

    @staticmethod
    def test_get_serial_number_v4_to_v8():
        """
        Test GetDeviceSerialNumberV4ToV8 class instantiation
        """
        my_class = GetDeviceSerialNumberV4ToV8(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDeviceSerialNumberV4ToV8(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_serial_number_v4_to_v8

    @staticmethod
    def test_get_serial_number_response_v4_to_v8():
        """
        Test GetDeviceSerialNumberResponseV4ToV8 class instantiation
        """
        my_class = GetDeviceSerialNumberResponseV4ToV8(
            device_index=0,
            feature_index=0,
            serial_number=HexList('00' * (GetDeviceSerialNumberResponseV4ToV8.LEN.SERIAL_NUMBER // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceSerialNumberResponseV4ToV8(
            device_index=0xFF,
            feature_index=0xFF,
            serial_number=HexList('FF' * (GetDeviceSerialNumberResponseV4ToV8.LEN.SERIAL_NUMBER // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_serial_number_response_v4_to_v8
# end class DeviceInformationInstantiationTestCase


class DeviceInformationTestCase(TestCase):
    """
    Device information factory testing
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            1: {
                "cls": DeviceInformationV1,
                "interfaces": {
                    "entity_types": DeviceInformation.EntityTypeV1,
                    "get_device_info_cls": GetDeviceInfoV1ToV8,
                    "get_device_info_response_cls": GetDeviceInfoResponseV1,
                    "get_fw_info_cls": GetFwInfoV1ToV8,
                    "get_fw_info_response_cls": GetFwInfoResponseV1ToV7,
                    "get_device_serial_number_cls": None,
                    "get_device_serial_number_response_cls": None,
                },
                "max_function_index": 1
            },
            2: {
                "cls": DeviceInformationV2,
                "interfaces": {
                    "entity_types": DeviceInformation.EntityTypeV2,
                    "get_device_info_cls": GetDeviceInfoV1ToV8,
                    "get_device_info_response_cls": GetDeviceInfoResponseV2ToV3,
                    "get_fw_info_cls": GetFwInfoV1ToV8,
                    "get_fw_info_response_cls": GetFwInfoResponseV1ToV7,
                    "get_device_serial_number_cls": None,
                    "get_device_serial_number_response_cls": None,
                },
                "max_function_index": 1
            },
            3: {
                "cls": DeviceInformationV3,
                "interfaces": {
                    "entity_types": DeviceInformation.EntityTypeV3ToV4,
                    "get_device_info_cls": GetDeviceInfoV1ToV8,
                    "get_device_info_response_cls": GetDeviceInfoResponseV2ToV3,
                    "get_fw_info_cls": GetFwInfoV1ToV8,
                    "get_fw_info_response_cls": GetFwInfoResponseV1ToV7,
                    "get_device_serial_number_cls": None,
                    "get_device_serial_number_response_cls": None,
                },
                "max_function_index": 1
            },
            4: {
                "cls": DeviceInformationV4,
                "interfaces": {
                    "entity_types": DeviceInformation.EntityTypeV3ToV4,
                    "get_device_info_cls": GetDeviceInfoV1ToV8,
                    "get_device_info_response_cls": GetDeviceInfoResponseV4ToV5,
                    "get_fw_info_cls": GetFwInfoV1ToV8,
                    "get_fw_info_response_cls": GetFwInfoResponseV1ToV7,
                    "get_device_serial_number_cls": GetDeviceSerialNumberV4ToV8,
                    "get_device_serial_number_response_cls": GetDeviceSerialNumberResponseV4ToV8,
                },
                "max_function_index": 2
            },
            5: {
                "cls": DeviceInformationV5,
                "interfaces": {
                    "entity_types": DeviceInformation.EntityTypeV5ToV6,
                    "get_device_info_cls": GetDeviceInfoV1ToV8,
                    "get_device_info_response_cls": GetDeviceInfoResponseV4ToV5,
                    "get_fw_info_cls": GetFwInfoV1ToV8,
                    "get_fw_info_response_cls": GetFwInfoResponseV1ToV7,
                    "get_device_serial_number_cls": GetDeviceSerialNumberV4ToV8,
                    "get_device_serial_number_response_cls": GetDeviceSerialNumberResponseV4ToV8,
                },
                "max_function_index": 2
            },
            6: {
                "cls": DeviceInformationV6,
                "interfaces": {
                    "entity_types": DeviceInformation.EntityTypeV5ToV6,
                    "get_device_info_cls": GetDeviceInfoV1ToV8,
                    "get_device_info_response_cls": GetDeviceInfoResponseV6ToV8,
                    "get_fw_info_cls": GetFwInfoV1ToV8,
                    "get_fw_info_response_cls": GetFwInfoResponseV1ToV7,
                    "get_device_serial_number_cls": GetDeviceSerialNumberV4ToV8,
                    "get_device_serial_number_response_cls": GetDeviceSerialNumberResponseV4ToV8,
                },
                "max_function_index": 2
            },
            7: {
                "cls": DeviceInformationV7,
                "interfaces": {
                    "entity_types": DeviceInformation.EntityTypeV7ToV8,
                    "get_device_info_cls": GetDeviceInfoV1ToV8,
                    "get_device_info_response_cls": GetDeviceInfoResponseV6ToV8,
                    "get_fw_info_cls": GetFwInfoV1ToV8,
                    "get_fw_info_response_cls": GetFwInfoResponseV1ToV7,
                    "get_device_serial_number_cls": GetDeviceSerialNumberV4ToV8,
                    "get_device_serial_number_response_cls": GetDeviceSerialNumberResponseV4ToV8,
                },
                "max_function_index": 2
            },
            8: {
                "cls": DeviceInformationV8,
                "interfaces": {
                    "entity_types": DeviceInformation.EntityTypeV7ToV8,
                    "get_device_info_cls": GetDeviceInfoV1ToV8,
                    "get_device_info_response_cls": GetDeviceInfoResponseV6ToV8,
                    "get_fw_info_cls": GetFwInfoV1ToV8,
                    "get_fw_info_response_cls": GetFwInfoResponseV8,
                    "get_device_serial_number_cls": GetDeviceSerialNumberV4ToV8,
                    "get_device_serial_number_response_cls": GetDeviceSerialNumberResponseV4ToV8,
                },
                "max_function_index": 2
            },
        }
    # end def setUpClass

    def test_device_information_factory(self):
        """
        Test DeviceInformationFactory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(DeviceInformationFactory.create(version)), expected["cls"])
        # end for
    # end def test_device_information_factory

    def test_device_information_factory_version_out_of_range(self):
        """
        Test ``DeviceInformationFactory`` using out of range versions
        """
        for version in [9, 10]:
            with self.assertRaises(KeyError):
                DeviceInformationFactory.create(version)
            # end with
        # end for
    # end def test_device_information_factory_version_out_of_range

    def test_device_information_factory_interfaces(self):
        """
        Check DeviceInformationFactory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            device_information = DeviceInformationFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(device_information, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(device_information, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_device_information_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            device_information = DeviceInformationFactory.create(version)
            self.assertEqual(device_information.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class DeviceInformationTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
