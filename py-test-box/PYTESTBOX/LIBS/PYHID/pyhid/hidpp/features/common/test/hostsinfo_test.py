#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.feature.common.test.hostsinfo_test
    :brief: HID++ 2.0 Hosts Info (based on authentication mechanism) test module
    :author: Martin Cryonnet
    :date:   2020/11/10
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.hostsinfo import GetFeatureInfoResponseV1ToV2
from pyhid.hidpp.features.common.hostsinfo import GetFeatureInfoV1ToV2
from pyhid.hidpp.features.common.hostsinfo import GetHostDescriptorResponseV1
from pyhid.hidpp.features.common.hostsinfo import GetHostDescriptorResponseV2
from pyhid.hidpp.features.common.hostsinfo import GetHostDescriptorV1ToV2
from pyhid.hidpp.features.common.hostsinfo import GetHostFriendlyNameResponseV1ToV2
from pyhid.hidpp.features.common.hostsinfo import GetHostFriendlyNameV1ToV2
from pyhid.hidpp.features.common.hostsinfo import GetHostInfoResponseV1
from pyhid.hidpp.features.common.hostsinfo import GetHostInfoResponseV2
from pyhid.hidpp.features.common.hostsinfo import GetHostInfoV1ToV2
from pyhid.hidpp.features.common.hostsinfo import GetHostOsVersionResponseV1ToV2
from pyhid.hidpp.features.common.hostsinfo import GetHostOsVersionV1ToV2
from pyhid.hidpp.features.common.hostsinfo import HostsInfoFactory
from pyhid.hidpp.features.common.hostsinfo import HostsInfoV1
from pyhid.hidpp.features.common.hostsinfo import HostsInfoV2
from pyhid.hidpp.features.common.hostsinfo import SetHostFriendlyNameResponseV1ToV2
from pyhid.hidpp.features.common.hostsinfo import SetHostFriendlyNameV1ToV2
from pyhid.hidpp.features.common.hostsinfo import SetHostOsVersionResponseV1ToV2
from pyhid.hidpp.features.common.hostsinfo import SetHostOsVersionV1ToV2
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class HostsInfoInstantiationTestCase(TestCase):
    """
    ``HostsInfo`` testing class
    """

    @staticmethod
    def test_get_feature_info():
        """
        Tests ``GetFeatureInfoV1ToV2`` class instantiation
        """
        my_class = GetFeatureInfoV1ToV2(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetFeatureInfoV1ToV2(device_index=0xFF, feature_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_info

    @staticmethod
    def test_get_feature_info_response():
        """
        Tests ``GetFeatureInfoResponseV1ToV2`` class instantiation
        """
        my_class = GetFeatureInfoResponseV1ToV2(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetFeatureInfoResponseV1ToV2(device_index=0x00, feature_index=0x00, set_os_version=False,
                                                set_name=False, get_name=False, ble_hd=False, num_hosts=0,
                                                current_host=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetFeatureInfoResponseV1ToV2(device_index=0xFF, feature_index=0xFF, set_os_version=True,
                                                set_name=True, get_name=True, ble_hd=True, num_hosts=0xFF,
                                                current_host=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_feature_info_response

    @staticmethod
    def test_get_host_info():
        """
        Tests ``GetHostInfoV1ToV2`` class instantiation
        """
        my_class = GetHostInfoV1ToV2(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostInfoV1ToV2(device_index=0x00, feature_index=0x00, host_index=0)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostInfoV1ToV2(device_index=0xFF, feature_index=0xFF, host_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_host_info

    @staticmethod
    def test_get_host_info_response_v1():
        """
        Tests ``GetHostInfoResponseV1`` class instantiation
        """
        my_class = GetHostInfoResponseV1(device_index=0x00, feature_index=0x00, host_index=0, status=0, bus_type=0,
                                         num_pages=0, name_len=0, name_max_len=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostInfoResponseV1(device_index=0xFF, feature_index=0xFF, host_index=0xFF, status=0xFF,
                                         bus_type=0xFF, num_pages=0xFF, name_len=0xFF, name_max_len=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_info_response_v1

    @staticmethod
    def test_get_host_info_response_v2():
        """
        Tests ``GetHostInfoResponseV2`` class instantiation
        """
        my_class = GetHostInfoResponseV2(device_index=0x00, feature_index=0x00, host_index=0, status=0, bus_type=0,
                                         num_pages=0, name_len=0, name_max_len=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostInfoResponseV2(device_index=0xFF, feature_index=0xFF, host_index=0xFF, status=0xFF,
                                         bus_type=0xFF, num_pages=0xFF, name_len=0xFF, name_max_len=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_info_response_v2

    @staticmethod
    def test_get_host_descriptor_v1_to_v2():
        """
        Tests ``GetHostDescriptorV1ToV2`` class instantiation
        """
        my_class = GetHostDescriptorV1ToV2(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostDescriptorV1ToV2(device_index=0x00, feature_index=0x00, host_index=0x00, page_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostDescriptorV1ToV2(device_index=0xFF, feature_index=0xFF, host_index=0xFF, page_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_host_descriptor_v1_to_v2

    @staticmethod
    def test_get_host_descriptor_response_v1():
        """
        Tests ``GetHostDescriptorResponseV1`` response class instantiation
        """
        my_class = GetHostDescriptorResponseV1(
            device_index=0x00, feature_index=0x00, host_index=0x00, bus_type=0x00, page_index=0x00,
            host_descriptor=HexList('00'*(GetHostDescriptorResponseV1.LEN.HOST_DESCRIPTOR // 8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostDescriptorResponseV1(
            device_index=0xFF, feature_index=0xFF, host_index=0x00, bus_type=7, page_index=31,
            host_descriptor=HexList('FF'*(GetHostDescriptorResponseV1.LEN.HOST_DESCRIPTOR // 8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_descriptor_response_v1

    @staticmethod
    def test_get_host_descriptor_response_v2():
        """
        Tests ``GetHostDescriptorResponseV2`` response class instantiation
        """
        my_class = GetHostDescriptorResponseV2(
            device_index=0x00, feature_index=0x00, host_index=0x00, bus_type=0x00, page_index=0x00,
            host_descriptor=HexList('00'*(GetHostDescriptorResponseV2.LEN.HOST_DESCRIPTOR // 8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostDescriptorResponseV2(
            device_index=0xFF, feature_index=0xFF, host_index=0x00, bus_type=7, page_index=31,
            host_descriptor=HexList('FF'*(GetHostDescriptorResponseV2.LEN.HOST_DESCRIPTOR // 8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_descriptor_response_v2

    @staticmethod
    def test_get_host_friendly_name():
        """
        Tests ``GetHostFriendlyNameV1ToV2`` class instantiation
        """
        my_class = GetHostFriendlyNameV1ToV2(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostFriendlyNameV1ToV2(device_index=0x00, feature_index=0x00, host_index=0, byte_index=0)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostFriendlyNameV1ToV2(device_index=0xFF, feature_index=0xFF, host_index=0xFF, byte_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_host_friendly_name

    @staticmethod
    def test_get_host_friendly_name_response():
        """
        Tests ``GetHostFriendlyNameResponseV1ToV2`` class instantiation
        """
        my_class = GetHostFriendlyNameResponseV1ToV2(
            device_index=0x00, feature_index=0x00, host_index=0, byte_index=0,
            name_chunk=HexList('00'*(GetHostFriendlyNameResponseV1ToV2.LEN.NAME_CHUNK // 8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostFriendlyNameResponseV1ToV2(
            device_index=0xFF, feature_index=0xFF, host_index=0xFF, byte_index=0xFF,
            name_chunk=HexList('FF'*(GetHostFriendlyNameResponseV1ToV2.LEN.NAME_CHUNK // 8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_friendly_name_response

    @staticmethod
    def test_set_host_friendly_name():
        """
        Tests ``SetHostFriendlyNameV1ToV2`` class instantiation
        """
        my_class = SetHostFriendlyNameV1ToV2(
            device_index=0x00, feature_index=0x00, host_index=0, byte_index=0,
            name_chunk=HexList('00'*(GetHostFriendlyNameResponseV1ToV2.LEN.NAME_CHUNK // 8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetHostFriendlyNameV1ToV2(
            device_index=0xFF, feature_index=0xFF, host_index=0xFF, byte_index=0xFF,
            name_chunk=HexList('FF'*(GetHostFriendlyNameResponseV1ToV2.LEN.NAME_CHUNK // 8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_host_friendly_name

    @staticmethod
    def test_set_host_friendly_name_response():
        """
        Tests ``SetHostFriendlyNameResponseV1ToV2`` class instantiation
        """
        my_class = SetHostFriendlyNameResponseV1ToV2(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetHostFriendlyNameResponseV1ToV2(device_index=0x00, feature_index=0x00, host_index=0, byte_index=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetHostFriendlyNameResponseV1ToV2(
            device_index=0xFF, feature_index=0xFF, host_index=0xFF, byte_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_host_friendly_name_response

    @staticmethod
    def test_get_host_os_version():
        """
        Tests ``GetHostOsVersionV1ToV2`` class instantiation
        """
        my_class = GetHostOsVersionV1ToV2(device_index=0x00, feature_index=0x00)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostOsVersionV1ToV2(device_index=0x00, feature_index=0x00, host_index=0)
        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostOsVersionV1ToV2(device_index=0xFF, feature_index=0xFF, host_index=0xFF)
        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_host_os_version

    @staticmethod
    def test_get_host_os_version_response():
        """
        Tests ``GetHostOsVersionResponseV1ToV2`` class instantiation
        """
        my_class = GetHostOsVersionResponseV1ToV2(
            device_index=0x00, feature_index=0x00, host_index=0, os_type=0, os_version=0, os_revision=0, os_build=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostOsVersionResponseV1ToV2(
            device_index=0xFF, feature_index=0xFF, host_index=0xFF, os_type=0xFF, os_version=0xFF, os_revision=0xFFFF,
            os_build=0xFFFF)
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostOsVersionResponseV1ToV2(
            device_index=0x00, feature_index=0x00, host_index=0, os_type=0, os_version=0,
            os_revision=HexList('00' * (SetHostOsVersionV1ToV2.LEN.OS_REVISION // 8)),
            os_build=HexList('00' * (SetHostOsVersionV1ToV2.LEN.OS_BUILD // 8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostOsVersionResponseV1ToV2(
            device_index=0xFF, feature_index=0xFF, host_index=0xFF, os_type=0xFF, os_version=0xFF,
            os_revision=HexList('FF' * (SetHostOsVersionV1ToV2.LEN.OS_REVISION // 8)),
            os_build=HexList('FF' * (SetHostOsVersionV1ToV2.LEN.OS_BUILD // 8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_os_version_response

    @staticmethod
    def test_set_host_os_version():
        """
        Tests ``SetHostOsVersionV1ToV2`` class instantiation
        """
        my_class = SetHostOsVersionV1ToV2(
            device_index=0x00, feature_index=0x00, host_index=0, os_type=0, os_version=0, os_revision=0, os_build=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetHostOsVersionV1ToV2(
            device_index=0xFF, feature_index=0xFF, host_index=0xFF, os_type=0xFF, os_version=0xFF,
            os_revision=0xFFFF, os_build=0xFFFF)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetHostOsVersionV1ToV2(
            device_index=0x00, feature_index=0x00, host_index=0, os_type=0, os_version=0,
            os_revision=HexList('00' * (SetHostOsVersionV1ToV2.LEN.OS_REVISION // 8)),
            os_build=HexList('00' * (SetHostOsVersionV1ToV2.LEN.OS_BUILD // 8)))
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetHostOsVersionV1ToV2(
            device_index=0xFF, feature_index=0xFF, host_index=0xFF, os_type=0xFF, os_version=0xFF,
            os_revision=HexList('FF' * (SetHostOsVersionV1ToV2.LEN.OS_REVISION // 8)),
            os_build=HexList('FF' * (SetHostOsVersionV1ToV2.LEN.OS_BUILD // 8)))
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_host_os_version

    @staticmethod
    def test_set_host_os_version_response():
        """
        Tests ``SetHostOsVersionResponseV1ToV2`` class instantiation
        """
        my_class = SetHostOsVersionResponseV1ToV2(device_index=0x00, feature_index=0x00)
        RootTestCase._long_function_class_checker(my_class)

        my_class = SetHostOsVersionResponseV1ToV2(device_index=0xFF, feature_index=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_host_os_version_response
# end class HostsInfoInstantiationTestCase


class HostsInfoTestCase(TestCase):
    """
    ``HostsInfo`` factory model testing class
    """
    @classmethod
    def setUpClass(cls):
        """
        setUpClass
        """
        cls.expected = {
            HostsInfoV1.VERSION: {
                "cls": HostsInfoV1,
                "interfaces": {
                    "get_feature_info_cls": GetFeatureInfoV1ToV2,
                    "get_feature_info_response_cls": GetFeatureInfoResponseV1ToV2,
                    "get_host_info_cls": GetHostInfoV1ToV2,
                    "get_host_info_response_cls": GetHostInfoResponseV1,
                    "get_host_descriptor_cls": GetHostDescriptorV1ToV2,
                    "get_host_descriptor_response_cls": GetHostDescriptorResponseV1,
                    "get_host_friendly_name_cls": GetHostFriendlyNameV1ToV2,
                    "get_host_friendly_name_response_cls": GetHostFriendlyNameResponseV1ToV2,
                    "set_host_friendly_name_cls": SetHostFriendlyNameV1ToV2,
                    "set_host_friendly_name_response_cls": SetHostFriendlyNameResponseV1ToV2,
                    "get_host_os_version_cls": GetHostOsVersionV1ToV2,
                    "get_host_os_version_response_cls": GetHostOsVersionResponseV1ToV2,
                    "set_host_os_version_cls": SetHostOsVersionV1ToV2,
                    "set_host_os_version_response_cls": SetHostOsVersionResponseV1ToV2,
                },
                "max_function_index": 8
            },
            HostsInfoV2.VERSION: {
                "cls": HostsInfoV2,
                "interfaces": {
                    "get_feature_info_cls": GetFeatureInfoV1ToV2,
                    "get_feature_info_response_cls": GetFeatureInfoResponseV1ToV2,
                    "get_host_info_cls": GetHostInfoV1ToV2,
                    "get_host_info_response_cls": GetHostInfoResponseV2,
                    "get_host_descriptor_cls": GetHostDescriptorV1ToV2,
                    "get_host_descriptor_response_cls": GetHostDescriptorResponseV2,
                    "get_host_friendly_name_cls": GetHostFriendlyNameV1ToV2,
                    "get_host_friendly_name_response_cls": GetHostFriendlyNameResponseV1ToV2,
                    "set_host_friendly_name_cls": SetHostFriendlyNameV1ToV2,
                    "set_host_friendly_name_response_cls": SetHostFriendlyNameResponseV1ToV2,
                    "get_host_os_version_cls": GetHostOsVersionV1ToV2,
                    "get_host_os_version_response_cls": GetHostOsVersionResponseV1ToV2,
                    "set_host_os_version_cls": SetHostOsVersionV1ToV2,
                    "set_host_os_version_response_cls": SetHostOsVersionResponseV1ToV2,
                },
                "max_function_index": 8
            },
        }
    # end def setUpClass

    def test_hosts_info_factory(self):
        """
        Tests Hosts Info Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(HostsInfoFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_hosts_info_factory

    def test_hosts_info_factory_version_out_of_range(self):
        """
        Tests Hosts Info Factory with out of range versions
        """
        for version in [0, 3, 4]:
            with self.assertRaises(KeyError):
                HostsInfoFactory.create(version)
            # end with
        # end for
    # end def test_hosts_info_factory_version_out_of_range

    def test_hosts_info_factory_interfaces(self):
        """
        Check Hosts Info Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            hosts_info = HostsInfoFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(hosts_info, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(hosts_info, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_hosts_info_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            hosts_info = HostsInfoFactory.create(version)
            self.assertEqual(hosts_info.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class HostsInfoTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
