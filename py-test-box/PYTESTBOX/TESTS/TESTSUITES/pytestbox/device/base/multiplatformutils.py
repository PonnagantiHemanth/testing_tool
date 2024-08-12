#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.multiplatformutils
:brief: Helpers for ``MultiPlatform`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2022/10/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.multiplatform import CapabilityMask
from pyhid.hidpp.features.keyboard.multiplatform import GetFeatureInfosResponse
from pyhid.hidpp.features.keyboard.multiplatform import GetHostPlatformResponse
from pyhid.hidpp.features.keyboard.multiplatform import GetPlatformDescriptorResponseV0
from pyhid.hidpp.features.keyboard.multiplatform import GetPlatformDescriptorResponseV1
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatformFactory
from pyhid.hidpp.features.keyboard.multiplatform import PlatformChangeEvent
from pyhid.hidpp.features.keyboard.multiplatform import SetHostPlatformResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiPlatformTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``MultiPlatform`` feature
    """

    class CapabilityMaskChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``CapabilityMask``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.MULTI_PLATFORM
            return {
                "reserved_0": (
                    cls.check_reserved_0,
                    0),
                "set_host_platform": (
                    cls.check_set_host_platform,
                    config.F_SetHostPlatform),
                "os_detection": (
                    cls.check_os_detection,
                    config.F_OsDetection),
                "reserved_1": (
                    cls.check_reserved_1,
                    0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved_0(test_case, bitmap, expected):
            """
            Check reserved_0 field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMask to check
            :type bitmap: ``CapabilityMask``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved_0 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved_0),
                msg="The reserved_0 parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved_0})")
        # end def check_reserved_0

        @staticmethod
        def check_set_host_platform(test_case, bitmap, expected):
            """
            Check set_host_platform field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMask to check
            :type bitmap: ``CapabilityMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert set_host_platform that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="SetHostPlatform shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.set_host_platform),
                msg="The set_host_platform parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.set_host_platform})")
        # end def check_set_host_platform

        @staticmethod
        def check_os_detection(test_case, bitmap, expected):
            """
            Check os_detection field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMask to check
            :type bitmap: ``CapabilityMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert os_detection that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="OSDetection shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.os_detection),
                msg="The os_detection parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.os_detection})")
        # end def check_os_detection

        @staticmethod
        def check_reserved_1(test_case, bitmap, expected):
            """
            Check reserved_1 field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: CapabilityMask to check
            :type bitmap: ``CapabilityMask``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved_1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved_1),
                msg="The reserved_1 parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved_1})")
        # end def check_reserved_1
    # end class CapabilityMaskChecker

    class GetFeatureInfosResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetFeatureInfosResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.MULTI_PLATFORM
            return {
                "capability_mask": (
                    cls.check_capability_mask,
                    MultiPlatformTestUtils.CapabilityMaskChecker.get_default_check_map(test_case)),
                "num_platforms": (
                    cls.check_num_platforms,
                    len(config.F_OsMask)),
                "num_platform_descriptor": (
                    cls.check_num_platform_descriptor,
                    len(config.F_OsMask)),
                "num_hosts": (
                    cls.check_num_hosts,
                    test_case.f.PRODUCT.DEVICE.F_NbHosts),
                "current_host": (
                    cls.check_current_host,
                    None),
                "current_host_platform": (
                    cls.check_current_host_platform,
                    None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_capability_mask(test_case, message, expected):
            """
            Check ``capability_mask``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetFeatureInfosResponse to check
            :type message: ``GetFeatureInfosResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MultiPlatformTestUtils.CapabilityMaskChecker.check_fields(
                test_case, message.capability_mask, CapabilityMask, expected)
        # end def check_capability_mask

        @staticmethod
        def check_num_platforms(test_case, response, expected):
            """
            Check num_platforms field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetFeatureInfosResponse to check
            :type response: ``GetFeatureInfosResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert num_platforms that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.num_platforms),
                msg="The num_platforms parameter differs "
                    f"(expected:{expected}, obtained:{response.num_platforms})")
        # end def check_num_platforms

        @staticmethod
        def check_num_platform_descriptor(test_case, response, expected):
            """
            Check num_platform_descriptor field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetFeatureInfosResponse to check
            :type response: ``GetFeatureInfosResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert num_platform_descriptor that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.num_platform_descriptor),
                msg="The num_platform_descriptor parameter differs "
                    f"(expected:{expected}, obtained:{response.num_platform_descriptor})")
        # end def check_num_platform_descriptor

        @staticmethod
        def check_num_hosts(test_case, response, expected):
            """
            Check num_hosts field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetFeatureInfosResponse to check
            :type response: ``GetFeatureInfosResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert num_hosts that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="NumHosts shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.num_hosts),
                msg="The num_hosts parameter differs "
                    f"(expected:{expected}, obtained:{response.num_hosts})")
        # end def check_num_hosts

        @staticmethod
        def check_current_host(test_case, response, expected):
            """
            Check current_host field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetFeatureInfosResponse to check
            :type response: ``GetFeatureInfosResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert current_host that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="CurrentHost shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.current_host),
                msg="The current_host parameter differs "
                    f"(expected:{expected}, obtained:{response.current_host})")
        # end def check_current_host

        @staticmethod
        def check_current_host_platform(test_case, response, expected):
            """
            Check current_host_platform field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetFeatureInfosResponse to check
            :type response: ``GetFeatureInfosResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert current_host_platform that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="CurrentHostPlatform shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.current_host_platform),
                msg="The current_host_platform parameter differs "
                    f"(expected:{expected}, obtained:{response.current_host_platform})")
        # end def check_current_host_platform
    # end class GetFeatureInfosResponseChecker

    class OSMaskChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``OSMask``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case, 0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, platform_descriptor_index):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param platform_descriptor_index: The index of platform descriptor
            :type platform_descriptor_index: ``int``

            :return: check map
            :rtype: ``dict``
            """
            os_mask = \
                int(test_case.f.PRODUCT.FEATURES.KEYBOARD.MULTI_PLATFORM.F_OsMask[platform_descriptor_index])
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "tizen": (
                    cls.check_tizen,
                    (os_mask & (2 ** 8)) >> 8),
                "web_os": (
                    cls.check_web_os,
                    (os_mask & (2 ** 7)) >> 7),
                "ios": (
                    cls.check_ios,
                    (os_mask & (2 ** 6)) >> 6),
                "mac_os": (
                    cls.check_mac_os,
                    (os_mask & (2 ** 5)) >> 5),
                "android": (
                    cls.check_android,
                    (os_mask & (2 ** 4)) >> 4),
                "chrome": (
                    cls.check_chrome,
                    (os_mask & (2 ** 3)) >> 3),
                "linux": (
                    cls.check_linux,
                    (os_mask & (2 ** 2)) >> 2),
                "win_emb": (
                    cls.check_win_emb,
                    (os_mask & (2 ** 1)) >> 1),
                "windows": (
                    cls.check_windows,
                    os_mask & (2 ** 0))
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_tizen(test_case, bitmap, expected):
            """
            Check tizen field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert tizen that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Tizen shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.tizen),
                msg="The tizen parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.tizen})")
        # end def check_tizen

        @staticmethod
        def check_web_os(test_case, bitmap, expected):
            """
            Check web_os field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert web_os that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="WebOS shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.web_os),
                msg="The web_os parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.web_os})")
        # end def check_web_os

        @staticmethod
        def check_ios(test_case, bitmap, expected):
            """
            Check ios field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert ios that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="iOS shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.ios),
                msg="The ios parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.ios})")
        # end def check_ios

        @staticmethod
        def check_mac_os(test_case, bitmap, expected):
            """
            Check mac_os field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert mac_os that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="MacOS shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.mac_os),
                msg="The mac_os parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.mac_os})")
        # end def check_mac_os

        @staticmethod
        def check_android(test_case, bitmap, expected):
            """
            Check android field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert android that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Android shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.android),
                msg="The android parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.android})")
        # end def check_android

        @staticmethod
        def check_chrome(test_case, bitmap, expected):
            """
            Check chrome field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert chrome that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Chrome shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.chrome),
                msg="The chrome parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.chrome})")
        # end def check_chrome

        @staticmethod
        def check_linux(test_case, bitmap, expected):
            """
            Check linux field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert linux that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Linux shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.linux),
                msg="The linux parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.linux})")
        # end def check_linux

        @staticmethod
        def check_win_emb(test_case, bitmap, expected):
            """
            Check win_emb field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert win_emb that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="WinEmb shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.win_emb),
                msg="The win_emb parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.win_emb})")
        # end def check_win_emb

        @staticmethod
        def check_windows(test_case, bitmap, expected):
            """
            Check windows field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OSMask to check
            :type bitmap: ``MultiPlatform.OSMask``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert windows that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Windows shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.windows),
                msg="The windows parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.windows})")
        # end def check_windows
    # end class OSMaskChecker

    class GetPlatformDescriptorResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetPlatformDescriptorResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "platform_index": (
                    cls.check_platform_index,
                    None),
                "platform_descriptor_index": (
                    cls.check_platform_descriptor_index,
                    None),
                "os_mask": (
                    cls.check_os_mask,
                    None),
                "from_version": (
                    cls.check_from_version,
                    0),
                "from_revision": (
                    cls.check_from_revision,
                    0),
                "to_version": (
                    cls.check_to_version,
                    0),
                "to_revision": (
                    cls.check_to_revision,
                    0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_platform_index(test_case, response, expected):
            """
            Check platform_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetPlatformDescriptorResponse to check
            :type response: ``GetPlatformDescriptorResponseV0 | GetPlatformDescriptorResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert platform_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="PlatformIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.platform_index),
                msg="The platform_index parameter differs "
                    f"(expected:{expected}, obtained:{response.platform_index})")
        # end def check_platform_index

        @staticmethod
        def check_platform_descriptor_index(test_case, response, expected):
            """
            Check platform_descriptor_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetPlatformDescriptorResponse to check
            :type response: ``GetPlatformDescriptorResponseV0 | GetPlatformDescriptorResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert platform_descriptor_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="PlatformDescriptorIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.platform_descriptor_index),
                msg="The platform_descriptor_index parameter differs "
                    f"(expected:{expected}, obtained:{response.platform_descriptor_index})")
        # end def check_platform_descriptor_index

        @staticmethod
        def check_os_mask(test_case, message, expected):
            """
            Check ``os_mask``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetPlatformDescriptorResponse to check
            :type message: ``GetPlatformDescriptorResponseV0 | GetPlatformDescriptorResponseV1``
            :param expected: Expected value
            :type expected: ``dict``
            """
            MultiPlatformTestUtils.OSMaskChecker.check_fields(
                test_case, message.os_mask, message.get_os_mask_cls(), expected)
        # end def check_os_mask

        @staticmethod
        def check_from_version(test_case, response, expected):
            """
            Check from_version field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetPlatformDescriptorResponse to check
            :type response: ``GetPlatformDescriptorResponseV0 | GetPlatformDescriptorResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert from_version that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="FromVersion shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.from_version),
                msg="The from_version parameter differs "
                    f"(expected:{expected}, obtained:{response.from_version})")
        # end def check_from_version

        @staticmethod
        def check_from_revision(test_case, response, expected):
            """
            Check from_revision field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetPlatformDescriptorResponse to check
            :type response: ``GetPlatformDescriptorResponseV0 | GetPlatformDescriptorResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert from_revision that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="FromRevision shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.from_revision),
                msg="The from_revision parameter differs "
                    f"(expected:{expected}, obtained:{response.from_revision})")
        # end def check_from_revision

        @staticmethod
        def check_to_version(test_case, response, expected):
            """
            Check to_version field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetPlatformDescriptorResponse to check
            :type response: ``GetPlatformDescriptorResponseV0 | GetPlatformDescriptorResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert to_version that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ToVersion shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.to_version),
                msg="The to_version parameter differs "
                    f"(expected:{expected}, obtained:{response.to_version})")
        # end def check_to_version

        @staticmethod
        def check_to_revision(test_case, response, expected):
            """
            Check to_revision field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetPlatformDescriptorResponse to check
            :type response: ``GetPlatformDescriptorResponseV0 | GetPlatformDescriptorResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert to_revision that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ToRevision shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.to_revision),
                msg="The to_revision parameter differs "
                    f"(expected:{expected}, obtained:{response.to_revision})")
        # end def check_to_revision
    # end class GetPlatformDescriptorResponseChecker

    class GetHostPlatformResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetHostPlatformResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "host_index": (
                    cls.check_host_index,
                    None),
                "status": (
                    cls.check_status,
                    None),
                "platform_index": (
                    cls.check_platform_index,
                    None),
                "platform_source": (
                    cls.check_platform_source,
                    None),
                "auto_platform": (
                    cls.check_auto_platform,
                    None),
                "auto_descriptor": (
                    cls.check_auto_descriptor,
                    None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_host_index(test_case, response, expected):
            """
            Check host_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHostPlatformResponse to check
            :type response: ``GetHostPlatformResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert host_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="HostIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.host_index),
                msg="The host_index parameter differs "
                    f"(expected:{expected}, obtained:{response.host_index})")
        # end def check_host_index

        @staticmethod
        def check_status(test_case, response, expected):
            """
            Check status field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHostPlatformResponse to check
            :type response: ``GetHostPlatformResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert status that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Status shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.status),
                msg="The status parameter differs "
                    f"(expected:{expected}, obtained:{response.status})")
        # end def check_status

        @staticmethod
        def check_platform_index(test_case, response, expected):
            """
            Check platform_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHostPlatformResponse to check
            :type response: ``GetHostPlatformResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert platform_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="PlatformIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.platform_index),
                msg="The platform_index parameter differs "
                    f"(expected:{expected}, obtained:{response.platform_index})")
        # end def check_platform_index

        @staticmethod
        def check_platform_source(test_case, response, expected):
            """
            Check platform_source field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHostPlatformResponse to check
            :type response: ``GetHostPlatformResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert platform_source that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="PlatformSource shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.platform_source),
                msg="The platform_source parameter differs "
                    f"(expected:{expected}, obtained:{response.platform_source})")
        # end def check_platform_source

        @staticmethod
        def check_auto_platform(test_case, response, expected):
            """
            Check auto_platform field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHostPlatformResponse to check
            :type response: ``GetHostPlatformResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert auto_platform that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="AutoPlatform shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.auto_platform),
                msg="The auto_platform parameter differs "
                    f"(expected:{expected}, obtained:{response.auto_platform})")
        # end def check_auto_platform

        @staticmethod
        def check_auto_descriptor(test_case, response, expected):
            """
            Check auto_descriptor field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHostPlatformResponse to check
            :type response: ``GetHostPlatformResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert auto_descriptor that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="AutoDescriptor shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.auto_descriptor),
                msg="The auto_descriptor parameter differs "
                    f"(expected:{expected}, obtained:{response.auto_descriptor})")
        # end def check_auto_descriptor
    # end class GetHostPlatformResponseChecker

    class SetHostPlatformResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetHostPlatformResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "host_index": (
                    cls.check_host_index,
                    None),
                "platform_index": (
                    cls.check_platform_index,
                    None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_host_index(test_case, response, expected):
            """
            Check host_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetHostPlatformResponse to check
            :type response: ``SetHostPlatformResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert host_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="HostIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.host_index),
                msg="The host_index parameter differs "
                    f"(expected:{expected}, obtained:{response.host_index})")
        # end def check_host_index

        @staticmethod
        def check_platform_index(test_case, response, expected):
            """
            Check platform_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetHostPlatformResponse to check
            :type response: ``SetHostPlatformResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert platform_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="PlatformIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.platform_index),
                msg="The platform_index parameter differs "
                    f"(expected:{expected}, obtained:{response.platform_index})")
        # end def check_platform_index
    # end class SetHostPlatformResponseChecker

    class PlatformChangeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``PlatformChangeEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "host_index": (
                    cls.check_host_index,
                    None),
                "platform_index": (
                    cls.check_platform_index,
                    None),
                "platform_source": (
                    cls.check_platform_source,
                    None),
            }
        # end def get_default_check_map

        @staticmethod
        def check_host_index(test_case, response, expected):
            """
            Check host_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: PlatformChangeEvent to check
            :type response: ``PlatformChangeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert host_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="HostIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.host_index),
                msg="The host_index parameter differs "
                    f"(expected:{expected}, obtained:{response.host_index})")
        # end def check_host_index

        @staticmethod
        def check_platform_index(test_case, response, expected):
            """
            Check platform_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetHostPlatformResponse to check
            :type response: ``PlatformChangeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert platform_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="PlatformIndex shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.platform_index),
                msg="The platform_index parameter differs "
                    f"(expected:{expected}, obtained:{response.platform_index})")
        # end def check_platform_index

        @staticmethod
        def check_platform_source(test_case, response, expected):
            """
            Check platform_source field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: PlatformChangeEvent to check
            :type response: ``PlatformChangeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert platform_source that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="PlatformSource shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.platform_source),
                msg="The platform_source parameter differs "
                    f"(expected:{expected}, obtained:{response.platform_source})")
        # end def check_platform_source
    # end class PlatformChangeEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=MultiPlatform.FEATURE_ID, factory=MultiPlatformFactory,
                           device_index=None, port_index=None, update_test_case=None):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(test_case, feature_id, factory, device_index, port_index, update_test_case)
        # end def get_parameters

        @classmethod
        def get_feature_infos(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetFeatureInfos``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetFeatureInfosResponse
            :rtype: ``GetFeatureInfosResponse``
            """
            feature_4531_index, feature_4531, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4531.get_feature_infos_cls(
                device_index=device_index,
                feature_index=feature_4531_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4531.get_feature_infos_response_cls)
            return response
        # end def get_feature_infos

        @classmethod
        def get_platform_descriptor(cls, test_case, platform_descriptor_index, device_index=None, port_index=None):
            """
            Process ``GetPlatformDescriptor``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param platform_descriptor_index: Platform Descriptor Index
            :type platform_descriptor_index: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetPlatformDescriptorResponse
            :rtype: ``GetPlatformDescriptorResponseV0 | GetPlatformDescriptorResponseV1``
            """
            feature_4531_index, feature_4531, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4531.get_platform_descriptor_cls(
                device_index=device_index,
                feature_index=feature_4531_index,
                platform_descriptor_index=HexList(platform_descriptor_index))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4531.get_platform_descriptor_response_cls)
            return response
        # end def get_platform_descriptor

        @classmethod
        def get_host_platform(cls, test_case, host_index, device_index=None, port_index=None):
            """
            Process ``GetHostPlatform``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param host_index: Host Index
            :type host_index: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetHostPlatformResponse
            :rtype: ``GetHostPlatformResponse``
            """
            feature_4531_index, feature_4531, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4531.get_host_platform_cls(
                device_index=device_index,
                feature_index=feature_4531_index,
                host_index=HexList(host_index))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4531.get_host_platform_response_cls)
            return response
        # end def get_host_platform

        @classmethod
        def set_host_platform(cls, test_case, host_index, platform_index, device_index=None, port_index=None):
            """
            Process ``SetHostPlatform``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param host_index: Host Index
            :type host_index: ``int | HexList``
            :param platform_index: Platform Index
            :type platform_index: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetHostPlatformResponse
            :rtype: ``SetHostPlatformResponse``
            """
            feature_4531_index, feature_4531, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4531.set_host_platform_cls(
                device_index=device_index,
                feature_index=feature_4531_index,
                host_index=HexList(host_index),
                platform_index=HexList(platform_index))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4531.set_host_platform_response_cls)
            return response
        # end def set_host_platform

        @classmethod
        def platform_change_event(cls, test_case, timeout=2,
                                  check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``PlatformChangeEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: PlatformChangeEvent
            :rtype: ``PlatformChangeEvent``
            """
            _, feature_4531, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_4531.platform_change_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def platform_change_event
    # end class HIDppHelper

    @staticmethod
    def get_supported_os_layouts(test_case):
        """
        Get all the device supported keyboard OS layouts

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The device supported keyboard OS layouts
        :rtype: ``list[list[int]]``
        """
        supported_os_layouts = []
        for os_mask in test_case.f.PRODUCT.FEATURES.KEYBOARD.MULTI_PLATFORM.F_OsMask:
            platforms = []
            for i in range(16):
                if int(os_mask) & (2 ** i):
                    platforms.append(2**i)
                # end if
            # end for
            supported_os_layouts.append(platforms)
        # end for

        return supported_os_layouts
    # end def get_supported_os_layouts

    @staticmethod
    def get_os_mask_thru_platform_index(test_case, platform_index, sub_platform_index=0):
        """
        Get the os mask through the platform index

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param platform_index: Platform index
        :type platform_index: ``int``
        :param sub_platform_index: Sub platform index - OPTIONAL
        :type sub_platform_index: ``int``

        :return: OS mask
        :rtype: ``int``
        """
        return MultiPlatformTestUtils.get_supported_os_layouts(test_case)[platform_index][sub_platform_index]
    # end def get_os_mask_thru_platform_index

    @staticmethod
    def get_platform_index_thru_os_mask(test_case, os_mask):
        """
        Get the platform index through the os mask

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param os_mask: OS mask
        :type os_mask: ``int``

        :return: Platform index
        :rtype: ``MultiPlatform.OsMask|int``

        :raise ``ValueError``: If input an unsupported OsMask
        """
        supported_os_layouts = MultiPlatformTestUtils.get_supported_os_layouts(test_case)

        for index, platforms in enumerate(supported_os_layouts):
            for platform in platforms:
                if platform == os_mask:
                    return index
                # end if
            # end for
        # end for

        raise ValueError(f"Invalid OsMask: {os_mask}")
    # end def get_platform_index_thru_os_mask

    @staticmethod
    def get_os_type_thru_os_mask(os_mask):
        """
        Get the OS type through the platform index

        :param os_mask: Platform Index
        :type os_mask: ``MultiPlatform.OsMask|int``

        :return: Os type
        :rtype: ``str|OS``

        :raise ``ValueError``: If input an unsupported OsMask
        """
        if os_mask == MultiPlatform.OsMask.WINDOWS:
            os_type = OS.WINDOWS
        elif os_mask == MultiPlatform.OsMask.WIN_EMB:
            os_type = OS.WIN_EMB
        elif os_mask == MultiPlatform.OsMask.LINUX:
            os_type = OS.LINUX
        elif os_mask == MultiPlatform.OsMask.CHROME_OS:
            os_type = OS.CHROME
        elif os_mask == MultiPlatform.OsMask.ANDROID:
            os_type = OS.ANDROID
        elif os_mask == MultiPlatform.OsMask.MAC_OS:
            os_type = OS.MAC
        elif os_mask == MultiPlatform.OsMask.IOS:
            os_type = OS.IPAD
        elif os_mask == MultiPlatform.OsMask.WEB_OS:
            os_type = OS.WEB_OS
        elif os_mask == MultiPlatform.OsMask.TIZEN:
            os_type = OS.TIZEN
        else:
            raise ValueError(f"Invalid OsMask: {os_mask}")
        # end if

        return os_type
    # end def get_os_type_thru_os_mask
# end class MultiPlatformTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
