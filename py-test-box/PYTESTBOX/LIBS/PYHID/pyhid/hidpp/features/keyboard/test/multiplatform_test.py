#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.keyboard.test.multiplatform_test
:brief: HID++ 2.0 ``MultiPlatform`` test module
:author: YY Liu <yliu5@logitech.com>
:date: 2022/10/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.keyboard.multiplatform import GetFeatureInfos
from pyhid.hidpp.features.keyboard.multiplatform import GetFeatureInfosResponse
from pyhid.hidpp.features.keyboard.multiplatform import GetHostPlatform
from pyhid.hidpp.features.keyboard.multiplatform import GetHostPlatformResponse
from pyhid.hidpp.features.keyboard.multiplatform import GetPlatformDescriptor
from pyhid.hidpp.features.keyboard.multiplatform import GetPlatformDescriptorResponseV0
from pyhid.hidpp.features.keyboard.multiplatform import GetPlatformDescriptorResponseV1
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatformFactory
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatformV0
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatformV1
from pyhid.hidpp.features.keyboard.multiplatform import PlatformChangeEvent
from pyhid.hidpp.features.keyboard.multiplatform import SetHostPlatform
from pyhid.hidpp.features.keyboard.multiplatform import SetHostPlatformResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiPlatformInstantiationTestCase(TestCase):
    """
    Test ``MultiPlatform`` testing classes instantiations
    """

    @staticmethod
    def test_multi_platform():
        """
        Test ``MultiPlatform`` class instantiation
        """
        my_class = MultiPlatform(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = MultiPlatform(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_multi_platform

    @staticmethod
    def test_get_feature_infos():
        """
        Test ``GetFeatureInfos`` class instantiation
        """
        my_class = GetFeatureInfos(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetFeatureInfos(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_feature_infos

    @staticmethod
    def test_get_feature_infos_response():
        """
        Test ``GetFeatureInfosResponse`` class instantiation
        """
        my_class = GetFeatureInfosResponse(device_index=0, feature_index=0,
                                           set_host_platform=False,
                                           os_detection=False,
                                           num_platforms=0,
                                           num_platform_descriptor=0,
                                           num_hosts=0,
                                           current_host=0,
                                           current_host_platform=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetFeatureInfosResponse(device_index=0xff, feature_index=0xff,
                                           set_host_platform=True,
                                           os_detection=True,
                                           num_platforms=0xff,
                                           num_platform_descriptor=0xff,
                                           num_hosts=0xff,
                                           current_host=0xff,
                                           current_host_platform=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_feature_infos_response

    @staticmethod
    def test_get_platform_descriptor():
        """
        Test ``GetPlatformDescriptor`` class instantiation
        """
        my_class = GetPlatformDescriptor(device_index=0, feature_index=0,
                                         platform_descriptor_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetPlatformDescriptor(device_index=0xff, feature_index=0xff,
                                         platform_descriptor_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_platform_descriptor

    @staticmethod
    def test_get_platform_descriptor_response_v0():
        """
        Test ``GetPlatformDescriptorResponseV0`` class instantiation
        """
        my_class = GetPlatformDescriptorResponseV0(device_index=0, feature_index=0,
                                                   platform_index=0,
                                                   platform_descriptor_index=0,
                                                   ios=False,
                                                   mac_os=False,
                                                   android=False,
                                                   chrome=False,
                                                   linux=False,
                                                   win_emb=False,
                                                   windows=False,
                                                   from_version=0,
                                                   from_revision=0,
                                                   to_version=0,
                                                   to_revision=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPlatformDescriptorResponseV0(device_index=0xff, feature_index=0xff,
                                                   platform_index=0xff,
                                                   platform_descriptor_index=0xff,
                                                   ios=True,
                                                   mac_os=True,
                                                   android=True,
                                                   chrome=True,
                                                   linux=True,
                                                   win_emb=True,
                                                   windows=True,
                                                   from_version=0xff,
                                                   from_revision=0xff,
                                                   to_version=0xff,
                                                   to_revision=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_platform_descriptor_response_v0

    @staticmethod
    def test_get_platform_descriptor_response_v1():
        """
        Test ``GetPlatformDescriptorResponseV1`` class instantiation
        """
        my_class = GetPlatformDescriptorResponseV1(device_index=0, feature_index=0,
                                                   platform_index=0,
                                                   platform_descriptor_index=0,
                                                   tizen=False,
                                                   web_os=False,
                                                   ios=False,
                                                   mac_os=False,
                                                   android=False,
                                                   chrome=False,
                                                   linux=False,
                                                   win_emb=False,
                                                   windows=False,
                                                   from_version=0,
                                                   from_revision=0,
                                                   to_version=0,
                                                   to_revision=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetPlatformDescriptorResponseV1(device_index=0xff, feature_index=0xff,
                                                   platform_index=0xff,
                                                   platform_descriptor_index=0xff,
                                                   tizen=True,
                                                   web_os=True,
                                                   ios=True,
                                                   mac_os=True,
                                                   android=True,
                                                   chrome=True,
                                                   linux=True,
                                                   win_emb=True,
                                                   windows=True,
                                                   from_version=0xff,
                                                   from_revision=0xff,
                                                   to_version=0xff,
                                                   to_revision=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_platform_descriptor_response_v1

    @staticmethod
    def test_get_host_platform():
        """
        Test ``GetHostPlatform`` class instantiation
        """
        my_class = GetHostPlatform(device_index=0, feature_index=0,
                                   host_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetHostPlatform(device_index=0xff, feature_index=0xff,
                                   host_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_host_platform

    @staticmethod
    def test_get_host_platform_response():
        """
        Test ``GetHostPlatformResponse`` class instantiation
        """
        my_class = GetHostPlatformResponse(device_index=0, feature_index=0,
                                           host_index=0,
                                           status=0,
                                           platform_index=0,
                                           platform_source=0,
                                           auto_platform=0,
                                           auto_descriptor=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHostPlatformResponse(device_index=0xff, feature_index=0xff,
                                           host_index=0xff,
                                           status=0xff,
                                           platform_index=0xff,
                                           platform_source=0xff,
                                           auto_platform=0xff,
                                           auto_descriptor=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_host_platform_response

    @staticmethod
    def test_set_host_platform():
        """
        Test ``SetHostPlatform`` class instantiation
        """
        my_class = SetHostPlatform(device_index=0, feature_index=0,
                                   host_index=0,
                                   platform_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetHostPlatform(device_index=0xff, feature_index=0xff,
                                   host_index=0xff,
                                   platform_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_host_platform

    @staticmethod
    def test_set_host_platform_response():
        """
        Test ``SetHostPlatformResponse`` class instantiation
        """
        my_class = SetHostPlatformResponse(device_index=0,
                                           feature_index=0,
                                           host_index=0,
                                           platform_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetHostPlatformResponse(device_index=0xff,
                                           feature_index=0xff,
                                           host_index=0xff,
                                           platform_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_host_platform_response

    @staticmethod
    def test_platform_change_event():
        """
        Test ``PlatformChangeEvent`` class instantiation
        """
        my_class = PlatformChangeEvent(device_index=0, feature_index=0,
                                       host_index=0,
                                       platform_index=0,
                                       platform_source=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = PlatformChangeEvent(device_index=0xff, feature_index=0xff,
                                       host_index=0xff,
                                       platform_index=0xff,
                                       platform_source=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_platform_change_event
# end class MultiPlatformInstantiationTestCase


class MultiPlatformTestCase(TestCase):
    """
    Test ``MultiPlatform`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            MultiPlatformV0.VERSION: {
                "cls": MultiPlatformV0,
                "interfaces": {
                    "get_feature_infos_cls": GetFeatureInfos,
                    "get_feature_infos_response_cls": GetFeatureInfosResponse,
                    "get_platform_descriptor_cls": GetPlatformDescriptor,
                    "get_platform_descriptor_response_cls": GetPlatformDescriptorResponseV0,
                    "get_host_platform_cls": GetHostPlatform,
                    "get_host_platform_response_cls": GetHostPlatformResponse,
                    "set_host_platform_cls": SetHostPlatform,
                    "set_host_platform_response_cls": SetHostPlatformResponse,
                    "platform_change_event_cls": PlatformChangeEvent,
                },
                "max_function_index": 3
            },
            MultiPlatformV1.VERSION: {
                "cls": MultiPlatformV1,
                "interfaces": {
                    "get_feature_infos_cls": GetFeatureInfos,
                    "get_feature_infos_response_cls": GetFeatureInfosResponse,
                    "get_platform_descriptor_cls": GetPlatformDescriptor,
                    "get_platform_descriptor_response_cls": GetPlatformDescriptorResponseV1,
                    "get_host_platform_cls": GetHostPlatform,
                    "get_host_platform_response_cls": GetHostPlatformResponse,
                    "set_host_platform_cls": SetHostPlatform,
                    "set_host_platform_response_cls": SetHostPlatformResponse,
                    "platform_change_event_cls": PlatformChangeEvent,
                },
                "max_function_index": 3
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``MultiPlatformFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(MultiPlatformFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``MultiPlatformFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                MultiPlatformFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``MultiPlatformFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = MultiPlatformFactory.create(version)
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
            obj = MultiPlatformFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class MultiPlatformTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
