#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.perkeylightingutils
:brief: Helpers for ``PerKeyLighting`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import random

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.perkeylighting import FrameEndResponse
from pyhid.hidpp.features.gaming.perkeylighting import GetInfoResponse
from pyhid.hidpp.features.gaming.perkeylighting import PerKeyLighting
from pyhid.hidpp.features.gaming.perkeylighting import PerKeyLightingFactory
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZonesDeltaCompression4bitResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZonesDeltaCompression5bitResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZonesResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetIndividualRGBZonesResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetRGBZonesSingleValueResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetRangeRGBZonesResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PerKeyLightingTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``PerKeyLighting`` feature
    """

    class GetInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetInfoResponse``
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
            return cls.get_check_map_from_param1(test_case=test_case, param1_value=0)
        # end get_default_check_map

        @classmethod
        def get_check_map_from_param1(cls, test_case, param1_value):
            """
            Get check map for ``GetInfoResponse`` form given param1 value

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :param param1_value: Param1 value
            :type param1_value: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.PER_KEY_LIGHTING
            return {
                "type_of_info": (
                    cls.check_type_of_info,
                    0x0),
                "param1": (
                    cls.check_param1,
                    config.ZONE_INFO_TABLE.F_SupportedZoneParam[param1_value]),
                "zone_byte_0": (
                    cls.check_zone_byte_0,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup0[param1_value]),
                "zone_byte_1": (
                    cls.check_zone_byte_1,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup1[param1_value]),
                "zone_byte_2": (
                    cls.check_zone_byte_2,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup2[param1_value]),
                "zone_byte_3": (
                    cls.check_zone_byte_3,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup3[param1_value]),
                "zone_byte_4": (
                    cls.check_zone_byte_4,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup4[param1_value]),
                "zone_byte_5": (
                    cls.check_zone_byte_5,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup5[param1_value]),
                "zone_byte_6": (
                    cls.check_zone_byte_6,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup6[param1_value]),
                "zone_byte_7": (
                    cls.check_zone_byte_7,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup7[param1_value]),
                "zone_byte_8": (
                    cls.check_zone_byte_8,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup8[param1_value]),
                "zone_byte_9": (
                    cls.check_zone_byte_9,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup9[param1_value]),
                "zone_byte_10": (
                    cls.check_zone_byte_10,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup10[param1_value]),
                "zone_byte_11": (
                    cls.check_zone_byte_11,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup11[param1_value]),
                "zone_byte_12": (
                    cls.check_zone_byte_12,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup12[param1_value]),
                "zone_byte_13": (
                    cls.check_zone_byte_13,
                    config.ZONE_INFO_TABLE.F_ZonePresenceGroup13[param1_value])
            }
        # end def get_check_map_from_param1

        @staticmethod
        def check_type_of_info(test_case, response, expected):
            """
            Check type_of_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert type_of_info that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="TypeofInfo shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.type_of_info),
                msg="The type_of_info parameter differs "
                    f"(expected:{expected}, obtained:{response.type_of_info})")
        # end def check_type_of_info

        @staticmethod
        def check_param1(test_case, response, expected):
            """
            Check param1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert param1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Param1 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.param1),
                msg="The param1 parameter differs "
                    f"(expected:{expected}, obtained:{response.param1})")
        # end def check_param1

        @staticmethod
        def check_zone_byte_0(test_case, response, expected):
            """
            Check zone_byte_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_0),
                msg="The zone_byte_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_0})")
        # end def check_zone_byte_0

        @staticmethod
        def check_zone_byte_1(test_case, response, expected):
            """
            Check zone_byte_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte1 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_1),
                msg="The zone_byte_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_1})")
        # end def check_zone_byte_1

        @staticmethod
        def check_zone_byte_2(test_case, response, expected):
            """
            Check zone_byte_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte2 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_2),
                msg="The zone_byte_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_2})")
        # end def check_zone_byte_2

        @staticmethod
        def check_zone_byte_3(test_case, response, expected):
            """
            Check zone_byte_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_3 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte3 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_3),
                msg="The zone_byte_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_3})")
        # end def check_zone_byte_3

        @staticmethod
        def check_zone_byte_4(test_case, response, expected):
            """
            Check zone_byte_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_4 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte4 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_4),
                msg="The zone_byte_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_4})")
        # end def check_zone_byte_4

        @staticmethod
        def check_zone_byte_5(test_case, response, expected):
            """
            Check zone_byte_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_5 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte5 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_5),
                msg="The zone_byte_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_5})")
        # end def check_zone_byte_5

        @staticmethod
        def check_zone_byte_6(test_case, response, expected):
            """
            Check zone_byte_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_6 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte6 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_6),
                msg="The zone_byte_6 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_6})")
        # end def check_zone_byte_6

        @staticmethod
        def check_zone_byte_7(test_case, response, expected):
            """
            Check zone_byte_7 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_7 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte7 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_7),
                msg="The zone_byte_7 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_7})")
        # end def check_zone_byte_7

        @staticmethod
        def check_zone_byte_8(test_case, response, expected):
            """
            Check zone_byte_8 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_8 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte8 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_8),
                msg="The zone_byte_8 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_8})")
        # end def check_zone_byte_8

        @staticmethod
        def check_zone_byte_9(test_case, response, expected):
            """
            Check zone_byte_9 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_9 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte9 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_9),
                msg="The zone_byte_9 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_9})")
        # end def check_zone_byte_9

        @staticmethod
        def check_zone_byte_10(test_case, response, expected):
            """
            Check zone_byte_10 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_10 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte10 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_10),
                msg="The zone_byte_10 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_10})")
        # end def check_zone_byte_10

        @staticmethod
        def check_zone_byte_11(test_case, response, expected):
            """
            Check zone_byte_11 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_11 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte11 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_11),
                msg="The zone_byte_11 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_11})")
        # end def check_zone_byte_11

        @staticmethod
        def check_zone_byte_12(test_case, response, expected):
            """
            Check zone_byte_12 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_12 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte12 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_12),
                msg="The zone_byte_12 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_12})")
        # end def check_zone_byte_12

        @staticmethod
        def check_zone_byte_13(test_case, response, expected):
            """
            Check zone_byte_13 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert zone_byte_13 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ZoneByte13 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.zone_byte_13),
                msg="The zone_byte_13 parameter differs "
                    f"(expected:{expected}, obtained:{response.zone_byte_13})")
        # end def check_zone_byte_13
    # end class GetInfoResponseChecker

    class SetIndividualRGBZonesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetIndividualRGBZonesResponse``
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
                "rgb_zone_id_0": (
                    cls.check_rgb_zone_id_0,
                    0x0),
                "rgb_zone_id_1": (
                    cls.check_rgb_zone_id_1,
                    0x0),
                "rgb_zone_id_2": (
                    cls.check_rgb_zone_id_2,
                    0x0),
                "rgb_zone_id_3": (
                    cls.check_rgb_zone_id_3,
                    0x0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_zone_id_0(test_case, response, expected):
            """
            Check rgb_zone_id_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetIndividualRGBZonesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetIndividualRGBZonesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_id_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneID0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_id_0),
                msg="The rgb_zone_id_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_id_0})")
        # end def check_rgb_zone_id_0

        @staticmethod
        def check_rgb_zone_id_1(test_case, response, expected):
            """
            Check rgb_zone_id_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetIndividualRGBZonesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetIndividualRGBZonesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_id_1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneID1 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_id_1),
                msg="The rgb_zone_id_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_id_1})")
        # end def check_rgb_zone_id_1

        @staticmethod
        def check_rgb_zone_id_2(test_case, response, expected):
            """
            Check rgb_zone_id_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetIndividualRGBZonesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetIndividualRGBZonesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_id_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneID2 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_id_2),
                msg="The rgb_zone_id_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_id_2})")
        # end def check_rgb_zone_id_2

        @staticmethod
        def check_rgb_zone_id_3(test_case, response, expected):
            """
            Check rgb_zone_id_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetIndividualRGBZonesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetIndividualRGBZonesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_id_3 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneID3 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_id_3),
                msg="The rgb_zone_id_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_id_3})")
        # end def check_rgb_zone_id_3
    # end class SetIndividualRGBZonesResponseChecker

    class SetConsecutiveRGBZonesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetConsecutiveRGBZonesResponse``
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
                "rgb_zone_id_0": (
                    cls.check_rgb_zone_id_0,
                    0x0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_zone_id_0(test_case, response, expected):
            """
            Check rgb_zone_id_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetConsecutiveRGBZonesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetConsecutiveRGBZonesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_id_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneID0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_id_0),
                msg="The rgb_zone_id_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_id_0})")
        # end def check_rgb_zone_id_0
    # end class SetConsecutiveRGBZonesResponseChecker

    class SetConsecutiveRGBZonesDeltaCompression5bitResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetConsecutiveRGBZonesDeltaCompression5bitResponse``
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
                "rgb_zone_id_0": (
                    cls.check_rgb_zone_id_0,
                    0x0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_zone_id_0(test_case, response, expected):
            """
            Check rgb_zone_id_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetConsecutiveRGBZonesDeltaCompression5bitResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.
                            SetConsecutiveRGBZonesDeltaCompression5bitResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_id_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneID0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_id_0),
                msg="The rgb_zone_id_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_id_0})")
        # end def check_rgb_zone_id_0
    # end class SetConsecutiveRGBZonesDeltaCompression5bitResponseChecker

    class SetConsecutiveRGBZonesDeltaCompression4bitResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetConsecutiveRGBZonesDeltaCompression4bitResponse``
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
                "rgb_zone_id_0": (
                    cls.check_rgb_zone_id_0,
                    0x0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_zone_id_0(test_case, response, expected):
            """
            Check rgb_zone_id_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetConsecutiveRGBZonesDeltaCompression4bitResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting
                            .SetConsecutiveRGBZonesDeltaCompression4bitResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_id_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneID0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_id_0),
                msg="The rgb_zone_id_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_id_0})")
        # end def check_rgb_zone_id_0
    # end class SetConsecutiveRGBZonesDeltaCompression4bitResponseChecker

    class SetRangeRGBZonesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetRangeRGBZonesResponse``
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
                "rgb_first_zone_id_0": (
                    cls.check_rgb_first_zone_id_0,
                    0x0),
                "rgb_first_zone_id_1": (
                    cls.check_rgb_first_zone_id_1,
                    0x0),
                "rgb_first_zone_id_2": (
                    cls.check_rgb_first_zone_id_2,
                    0x0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_first_zone_id_0(test_case, response, expected):
            """
            Check rgb_first_zone_id_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetRangeRGBZonesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetRangeRGBZonesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_first_zone_id_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBFirstZoneID0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_first_zone_id_0),
                msg="The rgb_first_zone_id_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_first_zone_id_0})")
        # end def check_rgb_first_zone_id_0

        @staticmethod
        def check_rgb_first_zone_id_1(test_case, response, expected):
            """
            Check rgb_first_zone_id_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetRangeRGBZonesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetRangeRGBZonesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_first_zone_id_1 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBFirstZoneID1 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_first_zone_id_1),
                msg="The rgb_first_zone_id_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_first_zone_id_1})")
        # end def check_rgb_first_zone_id_1

        @staticmethod
        def check_rgb_first_zone_id_2(test_case, response, expected):
            """
            Check rgb_first_zone_id_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetRangeRGBZonesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetRangeRGBZonesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_first_zone_id_2 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBFirstZoneID2 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_first_zone_id_2),
                msg="The rgb_first_zone_id_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_first_zone_id_2})")
        # end def check_rgb_first_zone_id_2
    # end class SetRangeRGBZonesResponseChecker

    class SetRGBZonesSingleValueResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetRGBZonesSingleValueResponse``
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
                "rgb_zone_red": (
                    cls.check_rgb_zone_red,
                    0x0),
                "rgb_zone_green": (
                    cls.check_rgb_zone_green,
                    0x0),
                "rgb_zone_blue": (
                    cls.check_rgb_zone_blue,
                    0x0),
                "rgb_zone_id_0": (
                    cls.check_rgb_zone_id_0,
                    0xFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rgb_zone_red(test_case, response, expected):
            """
            Check rgb_zone_red field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetRGBZonesSingleValueResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetRGBZonesSingleValueResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_red that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneRed shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_red),
                msg="The rgb_zone_red parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_red})")
        # end def check_rgb_zone_red

        @staticmethod
        def check_rgb_zone_green(test_case, response, expected):
            """
            Check rgb_zone_green field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetRGBZonesSingleValueResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetRGBZonesSingleValueResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_green that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneGreen shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_green),
                msg="The rgb_zone_green parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_green})")
        # end def check_rgb_zone_green

        @staticmethod
        def check_rgb_zone_blue(test_case, response, expected):
            """
            Check rgb_zone_blue field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetRGBZonesSingleValueResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetRGBZonesSingleValueResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_blue that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneBlue shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_blue),
                msg="The rgb_zone_blue parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_blue})")
        # end def check_rgb_zone_blue

        @staticmethod
        def check_rgb_zone_id_0(test_case, response, expected):
            """
            Check rgb_zone_id_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SetRGBZonesSingleValueResponse to check
            :type response: ``pyhid.hidpp.features.gaming.perkeylighting.SetRGBZonesSingleValueResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rgb_zone_id_0 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RGBZoneID0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.rgb_zone_id_0),
                msg="The rgb_zone_id_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.rgb_zone_id_0})")
        # end def check_rgb_zone_id_0
    # end class SetRGBZonesSingleValueResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=PerKeyLighting.FEATURE_ID, factory=PerKeyLightingFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_info(cls, test_case, type_of_info, param1, device_index=None, port_index=None):
            """
            Process ``GetInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param type_of_info: This parameter defines the type of information requested
            :type type_of_info: ``int | HexList``
            :param param1: These parameters help to further specify the request in some particular cases
            :type param1: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetInfoResponse
            :rtype: ``GetInfoResponse``
            """
            feature_8081_index, feature_8081, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8081.get_info_cls(
                device_index=device_index,
                feature_index=feature_8081_index,
                type_of_info=HexList(type_of_info),
                param1=HexList(param1))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8081.get_info_response_cls)
            return response
        # end def get_info

        @classmethod
        def set_individual_rgb_zones(cls, test_case, rgb_zone_id_0, red_index_0, green_index_0, blue_index_0,
                                     rgb_zone_id_1=0, red_index_1=0, green_index_1=0, blue_index_1=0, rgb_zone_id_2=0,
                                     red_index_2=0, green_index_2=0, blue_index_2=0, rgb_zone_id_3=0, red_index_3=0,
                                     green_index_3=0, blue_index_3=0, device_index=None, port_index=None):
            """
            Process ``SetIndividualRGBZones``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_zone_id_0: RGB Zone ID [0]
            :type rgb_zone_id_0: ``int | HexList``
            :param red_index_0: RGB Zone ID [0] R Component
            :type red_index_0: ``int | HexList``
            :param green_index_0: RGB Zone ID [0] G Component
            :type green_index_0: ``int | HexList``
            :param blue_index_0: RGB Zone ID [0] B Component
            :type blue_index_0: ``int | HexList``
            :param rgb_zone_id_1: RGB Zone ID [1] - OPTIONAL
            :type rgb_zone_id_1: ``int | HexList``
            :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
            :type red_index_1: ``int | HexList``
            :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
            :type green_index_1: ``int | HexList``
            :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
            :type blue_index_1: ``int | HexList``
            :param rgb_zone_id_2: RGB Zone ID [2] - OPTIONAL
            :type rgb_zone_id_2: ``int | HexList``
            :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
            :type red_index_2: ``int | HexList``
            :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
            :type green_index_2: ``int | HexList``
            :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
            :type blue_index_2: ``int | HexList``
            :param rgb_zone_id_3: RGB Zone ID [3] - OPTIONAL
            :type rgb_zone_id_3: ``int | HexList``
            :param red_index_3: RGB Zone ID [3] R Component - OPTIONAL
            :type red_index_3: ``int | HexList``
            :param green_index_3: RGB Zone ID [3] G Component - OPTIONAL
            :type green_index_3: ``int | HexList``
            :param blue_index_3: RGB Zone ID [3] B Component - OPTIONAL
            :type blue_index_3: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetIndividualRGBZonesResponse
            :rtype: ``SetIndividualRGBZonesResponse``
            """
            feature_8081_index, feature_8081, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8081.set_individual_rgb_zones_cls(
                device_index=device_index,
                feature_index=feature_8081_index,
                rgb_zone_id_0=HexList(rgb_zone_id_0),
                red_index_0=HexList(red_index_0),
                green_index_0=HexList(green_index_0),
                blue_index_0=HexList(blue_index_0),
                rgb_zone_id_1=HexList(rgb_zone_id_1),
                red_index_1=HexList(red_index_1),
                green_index_1=HexList(green_index_1),
                blue_index_1=HexList(blue_index_1),
                rgb_zone_id_2=HexList(rgb_zone_id_2),
                red_index_2=HexList(red_index_2),
                green_index_2=HexList(green_index_2),
                blue_index_2=HexList(blue_index_2),
                rgb_zone_id_3=HexList(rgb_zone_id_3),
                red_index_3=HexList(red_index_3),
                green_index_3=HexList(green_index_3),
                blue_index_3=HexList(blue_index_3))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8081.set_individual_rgb_zones_response_cls)
            return response
        # end def set_individual_rgb_zones

        @classmethod
        def set_consecutive_rgb_zones(cls, test_case, rgb_zone_id_0, red_index_0, green_index_0, blue_index_0,
                                      red_index_1=0, green_index_1=0, blue_index_1=0, red_index_2=0, green_index_2=0,
                                      blue_index_2=0, red_index_3=0, green_index_3=0, blue_index_3=0, red_index_4=0,
                                      green_index_4=0, blue_index_4=0, device_index=None, port_index=None):
            """
            Process ``SetConsecutiveRGBZones``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_zone_id_0: Starting Zone ID, RGB Zone ID [0]
            :type rgb_zone_id_0: ``int | HexList``
            :param red_index_0: RGB Zone ID [0] R Component
            :type red_index_0: ``int | HexList``
            :param green_index_0: RGB Zone ID [0] G Component
            :type green_index_0: ``int | HexList``
            :param blue_index_0: RGB Zone ID [0] B Component
            :type blue_index_0: ``int | HexList``
            :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
            :type red_index_1: ``int | HexList``
            :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
            :type green_index_1: ``int | HexList``
            :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
            :type blue_index_1: ``int | HexList``
            :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
            :type red_index_2: ``int | HexList``
            :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
            :type green_index_2: ``int | HexList``
            :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
            :type blue_index_2: ``int | HexList``
            :param red_index_3: RGB Zone ID [3] R Component - OPTIONAL
            :type red_index_3: ``int | HexList``
            :param green_index_3: RGB Zone ID [3] G Component - OPTIONAL
            :type green_index_3: ``int | HexList``
            :param blue_index_3: RGB Zone ID [3] B Component - OPTIONAL
            :type blue_index_3: ``int | HexList``
            :param red_index_4: RGB Zone ID [4] R Component - OPTIONAL
            :type red_index_4: ``int | HexList``
            :param green_index_4: RGB Zone ID [4] G Component - OPTIONAL
            :type green_index_4: ``int | HexList``
            :param blue_index_4: RGB Zone ID [4] B Component - OPTIONAL
            :type blue_index_4: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetConsecutiveRGBZonesResponse
            :rtype: ``SetConsecutiveRGBZonesResponse``
            """
            feature_8081_index, feature_8081, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8081.set_consecutive_rgb_zones_cls(
                device_index=device_index,
                feature_index=feature_8081_index,
                rgb_zone_id_0=HexList(rgb_zone_id_0),
                red_index_0=HexList(red_index_0),
                green_index_0=HexList(green_index_0),
                blue_index_0=HexList(blue_index_0),
                red_index_1=HexList(red_index_1),
                green_index_1=HexList(green_index_1),
                blue_index_1=HexList(blue_index_1),
                red_index_2=HexList(red_index_2),
                green_index_2=HexList(green_index_2),
                blue_index_2=HexList(blue_index_2),
                red_index_3=HexList(red_index_3),
                green_index_3=HexList(green_index_3),
                blue_index_3=HexList(blue_index_3),
                red_index_4=HexList(red_index_4),
                green_index_4=HexList(green_index_4),
                blue_index_4=HexList(blue_index_4))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8081.set_consecutive_rgb_zones_response_cls)
            return response
        # end def set_consecutive_rgb_zones

        @classmethod
        def set_consecutive_rgb_zones_delta_compression_5bit(cls, test_case, rgb_zone_id_0, red_index_0, green_index_0,
                                                             blue_index_0, red_index_1=0, green_index_1=0,
                                                             blue_index_1=0, red_index_2=0, green_index_2=0,
                                                             blue_index_2=0, red_index_3=0, green_index_3=0,
                                                             blue_index_3=0, red_index_4=0, green_index_4=0,
                                                             blue_index_4=0, red_index_5=0, green_index_5=0,
                                                             blue_index_5=0, red_index_6=0, green_index_6=0,
                                                             blue_index_6=0, red_index_7=0, green_index_7=0,
                                                             blue_index_7=0, device_index=None, port_index=None):
            """
            Process ``SetConsecutiveRGBZonesDeltaCompression5bit``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_zone_id_0: Starting Zone ID, RGB Zone ID [0]
            :type rgb_zone_id_0: ``int | HexList``
            :param red_index_0: RGB Zone ID [0] R Component
            :type red_index_0: ``int | HexList``
            :param green_index_0: RGB Zone ID [0] G Component
            :type green_index_0: ``int | HexList``
            :param blue_index_0: RGB Zone ID [0] B Component
            :type blue_index_0: ``int | HexList``
            :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
            :type red_index_1: ``int | HexList``
            :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
            :type green_index_1: ``int | HexList``
            :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
            :type blue_index_1: ``int | HexList``
            :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
            :type red_index_2: ``int | HexList``
            :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
            :type green_index_2: ``int | HexList``
            :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
            :type blue_index_2: ``int | HexList``
            :param red_index_3: RGB Zone ID [3] R Component - OPTIONAL
            :type red_index_3: ``int | HexList``
            :param green_index_3: RGB Zone ID [3] G Component - OPTIONAL
            :type green_index_3: ``int | HexList``
            :param blue_index_3: RGB Zone ID [3] B Component - OPTIONAL
            :type blue_index_3: ``int | HexList``
            :param red_index_4: RGB Zone ID [4] R Component - OPTIONAL
            :type red_index_4: ``int | HexList``
            :param green_index_4: RGB Zone ID [4] G Component - OPTIONAL
            :type green_index_4: ``int | HexList``
            :param blue_index_4: RGB Zone ID [4] B Component - OPTIONAL
            :type blue_index_4: ``int | HexList``
            :param red_index_5: RGB Zone ID [5] R Component - OPTIONAL
            :type red_index_5: ``int | HexList``
            :param green_index_5: RGB Zone ID [5] G Component - OPTIONAL
            :type green_index_5: ``int | HexList``
            :param blue_index_5: RGB Zone ID [5] B Component - OPTIONAL
            :type blue_index_5: ``int | HexList``
            :param red_index_6: RGB Zone ID [6] R Component - OPTIONAL
            :type red_index_6: ``int | HexList``
            :param green_index_6: RGB Zone ID [6] G Component - OPTIONAL
            :type green_index_6: ``int | HexList``
            :param blue_index_6: RGB Zone ID [6] B Component - OPTIONAL
            :type blue_index_6: ``int | HexList``
            :param red_index_7: RGB Zone ID [7] R Component - OPTIONAL
            :type red_index_7: ``int | HexList``
            :param green_index_7: RGB Zone ID [7] G Component - OPTIONAL
            :type green_index_7: ``int | HexList``
            :param blue_index_7: RGB Zone ID [7] B Component - OPTIONAL
            :type blue_index_7: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetConsecutiveRGBZonesDeltaCompression5bitResponse
            :rtype: ``SetConsecutiveRGBZonesDeltaCompression5bitResponse``
            """
            feature_8081_index, feature_8081, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_cls(
                device_index=device_index,
                feature_index=feature_8081_index,
                rgb_zone_id_0=HexList(rgb_zone_id_0),
                red_index_0=red_index_0,
                green_index_0=green_index_0,
                blue_index_0=blue_index_0,
                red_index_1=red_index_1,
                green_index_1=green_index_1,
                blue_index_1=blue_index_1,
                red_index_2=red_index_2,
                green_index_2=green_index_2,
                blue_index_2=blue_index_2,
                red_index_3=red_index_3,
                green_index_3=green_index_3,
                blue_index_3=blue_index_3,
                red_index_4=red_index_4,
                green_index_4=green_index_4,
                blue_index_4=blue_index_4,
                red_index_5=red_index_5,
                green_index_5=green_index_5,
                blue_index_5=blue_index_5,
                red_index_6=red_index_6,
                green_index_6=green_index_6,
                blue_index_6=blue_index_6,
                red_index_7=red_index_7,
                green_index_7=green_index_7,
                blue_index_7=blue_index_7)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_response_cls)
            return response
        # end def set_consecutive_rgb_zones_delta_compression_5bit

        @classmethod
        def set_consecutive_rgb_zones_delta_compression_4bit(cls, test_case, rgb_zone_id_0, red_index_0, green_index_0,
                                                             blue_index_0, red_index_1=0, green_index_1=0,
                                                             blue_index_1=0, red_index_2=0, green_index_2=0,
                                                             blue_index_2=0, red_index_3=0, green_index_3=0,
                                                             blue_index_3=0, red_index_4=0, green_index_4=0,
                                                             blue_index_4=0, red_index_5=0, green_index_5=0,
                                                             blue_index_5=0, red_index_6=0, green_index_6=0,
                                                             blue_index_6=0, red_index_7=0, green_index_7=0,
                                                             blue_index_7=0, red_index_8=0, green_index_8=0,
                                                             blue_index_8=0, red_index_9=0, green_index_9=0,
                                                             blue_index_9=0, device_index=None, port_index=None):
            """
            Process ``SetConsecutiveRGBZonesDeltaCompression4bit``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_zone_id_0: Starting Zone ID, RGB Zone ID [0]
            :type rgb_zone_id_0: ``int | HexList``
            :param red_index_0: RGB Zone ID [0] R Component
            :type red_index_0: ``int | HexList``
            :param green_index_0: RGB Zone ID [0] G Component
            :type green_index_0: ``int | HexList``
            :param blue_index_0: RGB Zone ID [0] B Component
            :type blue_index_0: ``int | HexList``
            :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
            :type red_index_1: ``int | HexList``
            :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
            :type green_index_1: ``int | HexList``
            :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
            :type blue_index_1: ``int | HexList``
            :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
            :type red_index_2: ``int | HexList``
            :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
            :type green_index_2: ``int | HexList``
            :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
            :type blue_index_2: ``int | HexList``
            :param red_index_3: RGB Zone ID [3] R Component - OPTIONAL
            :type red_index_3: ``int | HexList``
            :param green_index_3: RGB Zone ID [3] G Component - OPTIONAL
            :type green_index_3: ``int | HexList``
            :param blue_index_3: RGB Zone ID [3] B Component - OPTIONAL
            :type blue_index_3: ``int | HexList``
            :param red_index_4: RGB Zone ID [4] R Component - OPTIONAL
            :type red_index_4: ``int | HexList``
            :param green_index_4: RGB Zone ID [4] G Component - OPTIONAL
            :type green_index_4: ``int | HexList``
            :param blue_index_4: RGB Zone ID [4] B Component - OPTIONAL
            :type blue_index_4: ``int | HexList``
            :param red_index_5: RGB Zone ID [5] R Component - OPTIONAL
            :type red_index_5: ``int | HexList``
            :param green_index_5: RGB Zone ID [5] G Component - OPTIONAL
            :type green_index_5: ``int | HexList``
            :param blue_index_5: RGB Zone ID [5] B Component - OPTIONAL
            :type blue_index_5: ``int | HexList``
            :param red_index_6: RGB Zone ID [6] R Component - OPTIONAL
            :type red_index_6: ``int | HexList``
            :param green_index_6: RGB Zone ID [6] G Component - OPTIONAL
            :type green_index_6: ``int | HexList``
            :param blue_index_6: RGB Zone ID [6] B Component - OPTIONAL
            :type blue_index_6: ``int | HexList``
            :param red_index_7: RGB Zone ID [7] R Component - OPTIONAL
            :type red_index_7: ``int | HexList``
            :param green_index_7: RGB Zone ID [7] G Component - OPTIONAL
            :type green_index_7: ``int | HexList``
            :param blue_index_7: RGB Zone ID [7] B Component - OPTIONAL
            :type blue_index_7: ``int | HexList``
            :param red_index_8: RGB Zone ID [8] R Component - OPTIONAL
            :type red_index_8: ``int | HexList``
            :param green_index_8: RGB Zone ID [8] G Component - OPTIONAL
            :type green_index_8: ``int | HexList``
            :param blue_index_8: RGB Zone ID [8] B Component - OPTIONAL
            :type blue_index_8: ``int | HexList``
            :param red_index_9: RGB Zone ID [9] R Component - OPTIONAL
            :type red_index_9: ``int | HexList``
            :param green_index_9: RGB Zone ID [9] G Component - OPTIONAL
            :type green_index_9: ``int | HexList``
            :param blue_index_9: RGB Zone ID [9] B Component - OPTIONAL
            :type blue_index_9: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetConsecutiveRGBZonesDeltaCompression4bitResponse
            :rtype: ``SetConsecutiveRGBZonesDeltaCompression4bitResponse``
            """
            feature_8081_index, feature_8081, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_cls(
                device_index=device_index,
                feature_index=feature_8081_index,
                rgb_zone_id_0=HexList(rgb_zone_id_0),
                red_index_0=red_index_0,
                green_index_0=green_index_0,
                blue_index_0=blue_index_0,
                red_index_1=red_index_1,
                green_index_1=green_index_1,
                blue_index_1=blue_index_1,
                red_index_2=red_index_2,
                green_index_2=green_index_2,
                blue_index_2=blue_index_2,
                red_index_3=red_index_3,
                green_index_3=green_index_3,
                blue_index_3=blue_index_3,
                red_index_4=red_index_4,
                green_index_4=green_index_4,
                blue_index_4=blue_index_4,
                red_index_5=red_index_5,
                green_index_5=green_index_5,
                blue_index_5=blue_index_5,
                red_index_6=red_index_6,
                green_index_6=green_index_6,
                blue_index_6=blue_index_6,
                red_index_7=red_index_7,
                green_index_7=green_index_7,
                blue_index_7=blue_index_7,
                red_index_8=red_index_8,
                green_index_8=green_index_8,
                blue_index_8=blue_index_8,
                red_index_9=red_index_9,
                green_index_9=green_index_9,
                blue_index_9=blue_index_9)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_response_cls)
            return response
        # end def set_consecutive_rgb_zones_delta_compression_4bit

        @classmethod
        def set_range_rgb_zones(cls, test_case, rgb_first_zone_id_0, rgb_last_zone_id_0, red_index_0, green_index_0,
                                blue_index_0, rgb_first_zone_id_1=0, rgb_last_zone_id_1=0, red_index_1=0,
                                green_index_1=0, blue_index_1=0, rgb_first_zone_id_2=0, rgb_last_zone_id_2=0,
                                red_index_2=0, green_index_2=0, blue_index_2=0, device_index=None, port_index=None):
            """
            Process ``SetRangeRGBZones``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_first_zone_id_0: Starting Zone ID [0]
            :type rgb_first_zone_id_0: ``int | HexList``
            :param rgb_last_zone_id_0: Ending Zone ID [0]
            :type rgb_last_zone_id_0: ``int | HexList``
            :param red_index_0: RGB Zone ID [0] R Component
            :type red_index_0: ``int | HexList``
            :param green_index_0: RGB Zone ID [0] G Component
            :type green_index_0: ``int | HexList``
            :param blue_index_0: RGB Zone ID [0] B Component
            :type blue_index_0: ``int | HexList``
            :param rgb_first_zone_id_1: Starting Zone ID [1] - OPTIONAL
            :type rgb_first_zone_id_1: ``int | HexList``
            :param rgb_last_zone_id_1: Ending Zone ID [1] - OPTIONAL
            :type rgb_last_zone_id_1: ``int | HexList``
            :param red_index_1: RGB Zone ID [1] R Component - OPTIONAL
            :type red_index_1: ``int | HexList``
            :param green_index_1: RGB Zone ID [1] G Component - OPTIONAL
            :type green_index_1: ``int | HexList``
            :param blue_index_1: RGB Zone ID [1] B Component - OPTIONAL
            :type blue_index_1: ``int | HexList``
            :param rgb_first_zone_id_2: Starting Zone ID [2] - OPTIONAL
            :type rgb_first_zone_id_2: ``int | HexList``
            :param rgb_last_zone_id_2: Ending Zone ID [2] - OPTIONAL
            :type rgb_last_zone_id_2: ``int | HexList``
            :param red_index_2: RGB Zone ID [2] R Component - OPTIONAL
            :type red_index_2: ``int | HexList``
            :param green_index_2: RGB Zone ID [2] G Component - OPTIONAL
            :type green_index_2: ``int | HexList``
            :param blue_index_2: RGB Zone ID [2] B Component - OPTIONAL
            :type blue_index_2: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRangeRGBZonesResponse
            :rtype: ``SetRangeRGBZonesResponse``
            """
            feature_8081_index, feature_8081, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8081.set_range_rgb_zones_cls(
                device_index=device_index,
                feature_index=feature_8081_index,
                rgb_first_zone_id_0=HexList(rgb_first_zone_id_0),
                rgb_last_zone_id_0=HexList(rgb_last_zone_id_0),
                red_index_0=HexList(red_index_0),
                green_index_0=HexList(green_index_0),
                blue_index_0=HexList(blue_index_0),
                rgb_first_zone_id_1=HexList(rgb_first_zone_id_1),
                rgb_last_zone_id_1=HexList(rgb_last_zone_id_1),
                red_index_1=HexList(red_index_1),
                green_index_1=HexList(green_index_1),
                blue_index_1=HexList(blue_index_1),
                rgb_first_zone_id_2=HexList(rgb_first_zone_id_2),
                rgb_last_zone_id_2=HexList(rgb_last_zone_id_2),
                red_index_2=HexList(red_index_2),
                green_index_2=HexList(green_index_2),
                blue_index_2=HexList(blue_index_2))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8081.set_range_rgb_zones_response_cls)
            return response
        # end def set_range_rgb_zones

        @classmethod
        def set_rgb_zones_single_value(cls, test_case, rgb_zone_red, rgb_zone_green, rgb_zone_blue, rgb_zone_id_0,
                                       rgb_zone_id_1=0, rgb_zone_id_2=0, rgb_zone_id_3=0, rgb_zone_id_4=0,
                                       rgb_zone_id_5=0, rgb_zone_id_6=0, rgb_zone_id_7=0, rgb_zone_id_8=0,
                                       rgb_zone_id_9=0, rgb_zone_id_10=0, rgb_zone_id_11=0, rgb_zone_id_12=0,
                                       device_index=None, port_index=None):
            """
            Process ``SetRGBZonesSingleValue``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param rgb_zone_red: RGB Zone R Component
            :type rgb_zone_red: ``int | HexList``
            :param rgb_zone_green: RGB Zone G Component
            :type rgb_zone_green: ``int | HexList``
            :param rgb_zone_blue: RGB Zone B Component
            :type rgb_zone_blue: ``int | HexList``
            :param rgb_zone_id_0: RGB Zone ID [0]
            :type rgb_zone_id_0: ``int | HexList``
            :param rgb_zone_id_1: RGB Zone ID [1] - OPTIONAL
            :type rgb_zone_id_1: ``int | HexList``
            :param rgb_zone_id_2: RGB Zone ID [2] - OPTIONAL
            :type rgb_zone_id_2: ``int | HexList``
            :param rgb_zone_id_3: RGB Zone ID [3] - OPTIONAL
            :type rgb_zone_id_3: ``int | HexList``
            :param rgb_zone_id_4: RGB Zone ID [4] - OPTIONAL
            :type rgb_zone_id_4: ``int | HexList``
            :param rgb_zone_id_5: RGB Zone ID [5] - OPTIONAL
            :type rgb_zone_id_5: ``int | HexList``
            :param rgb_zone_id_6: RGB Zone ID [6] - OPTIONAL
            :type rgb_zone_id_6: ``int | HexList``
            :param rgb_zone_id_7: RGB Zone ID [7] - OPTIONAL
            :type rgb_zone_id_7: ``int | HexList``
            :param rgb_zone_id_8: RGB Zone ID [8] - OPTIONAL
            :type rgb_zone_id_8: ``int | HexList``
            :param rgb_zone_id_9: RGB Zone ID [9] - OPTIONAL
            :type rgb_zone_id_9: ``int | HexList``
            :param rgb_zone_id_10: RGB Zone ID [10] - OPTIONAL
            :type rgb_zone_id_10: ``int | HexList``
            :param rgb_zone_id_11: RGB Zone ID [11] - OPTIONAL
            :type rgb_zone_id_11: ``int | HexList``
            :param rgb_zone_id_12: RGB Zone ID [12] - OPTIONAL
            :type rgb_zone_id_12: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetRGBZonesSingleValueResponse
            :rtype: ``SetRGBZonesSingleValueResponse``
            """
            feature_8081_index, feature_8081, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8081.set_rgb_zones_single_value_cls(
                device_index=device_index,
                feature_index=feature_8081_index,
                rgb_zone_red=HexList(rgb_zone_red),
                rgb_zone_green=HexList(rgb_zone_green),
                rgb_zone_blue=HexList(rgb_zone_blue),
                rgb_zone_id_0=HexList(rgb_zone_id_0),
                rgb_zone_id_1=HexList(rgb_zone_id_1),
                rgb_zone_id_2=HexList(rgb_zone_id_2),
                rgb_zone_id_3=HexList(rgb_zone_id_3),
                rgb_zone_id_4=HexList(rgb_zone_id_4),
                rgb_zone_id_5=HexList(rgb_zone_id_5),
                rgb_zone_id_6=HexList(rgb_zone_id_6),
                rgb_zone_id_7=HexList(rgb_zone_id_7),
                rgb_zone_id_8=HexList(rgb_zone_id_8),
                rgb_zone_id_9=HexList(rgb_zone_id_9),
                rgb_zone_id_10=HexList(rgb_zone_id_10),
                rgb_zone_id_11=HexList(rgb_zone_id_11),
                rgb_zone_id_12=HexList(rgb_zone_id_12))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8081.set_rgb_zones_single_value_response_cls)
            return response
        # end def set_rgb_zones_single_value

        @classmethod
        def frame_end(cls, test_case, persistence=0, current_frame=0, n_frames_till_next_change=0, device_index=None,
                      port_index=None):
            """
            Process ``FrameEnd``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param persistence: Determines how the effect persists through a power cycle - OPTIONAL
            :type persistence: ``int | HexList``
            :param current_frame: Index of the frame that ends by this command - OPTIONAL
            :type current_frame: ``int | HexList``
            :param n_frames_till_next_change: Realtime information for playback: number of frames until next expected
                                              change - OPTIONAL
            :type n_frames_till_next_change: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: FrameEndResponse
            :rtype: ``FrameEndResponse``
            """
            feature_8081_index, feature_8081, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8081.frame_end_cls(
                device_index=device_index,
                feature_index=feature_8081_index,
                persistence=persistence,
                current_frame=current_frame,
                n_frames_till_next_change=n_frames_till_next_change)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8081.frame_end_response_cls)
            return response
        # end def frame_end

        @classmethod
        def get_valid_zones(cls, get_info_response):
            """
            Get all valid zone id from get info response

            :param get_info_response: get_info_response
            :type get_info_response: ``GetInfoResponse``

            :return: The list of all valid zone id
            :rtype: ``HexList``
            """
            zone_byte_list = [get_info_response.zone_byte_0,  get_info_response.zone_byte_1,
                              get_info_response.zone_byte_2,  get_info_response.zone_byte_3,
                              get_info_response.zone_byte_4,  get_info_response.zone_byte_5,
                              get_info_response.zone_byte_6,  get_info_response.zone_byte_7,
                              get_info_response.zone_byte_8,  get_info_response.zone_byte_9,
                              get_info_response.zone_byte_10, get_info_response.zone_byte_11,
                              get_info_response.zone_byte_12, get_info_response.zone_byte_13]

            return HexList(zone_byte_list)
        # end def get_valid_zones

        @classmethod
        def random_color_picker(cls):
            """
            Pick a random color from Red, Yellow, Green, Cyan, Blue and return the hex value

            :return: The hex value of color
            :rtype: ``tuple[int, int, int]``
            """
            red = (0xff, 0x0, 0x0)
            green = (0x0, 0xff, 0x0)
            blue = (0x0, 0x0, 0xff)
            yellow = (0xff, 0xff, 0x0)
            cyan = (0xff, 0x0, 0xff)
            color_list = (red, green, blue, yellow, cyan)

            return color_list[random.randrange(len(color_list))]
        # end def random_color_picker

        class RandomZoneSelector:
            """
            Select a random and unique zone id everytime from available zone id list
            """
            def __init__(self, zone_id_list):
                """
                :param zone_id_list: The list of available zone id
                :type zone_id_list: ``int``
                """
                self.seen_zones = []
                self.zone_id_list = zone_id_list
            # end def __init__

            def random_zone_selector(self):
                """
                Select a random and unique zone id everytime from available zone id list

                :return: A random zone id
                :rtype: ``int``
                """
                n = random.randrange(len(self.zone_id_list))
                if self.zone_id_list[n] not in self.seen_zones:
                    self.seen_zones.append(self.zone_id_list[n])
                    return self.zone_id_list[n]
                # end if
                return self.random_zone_selector()
            # end def random_zone_selector
        # end class RandomZoneSelector

        @classmethod
        def consecutive_zone_selector(cls, zone_list, consecutive_zones):
            """
            Return n number of random consecutive zones from zone list

            :param zone_list: The list of available zone id
            :type zone_list: ``list[int]``
            :param consecutive_zones: Number of consecutive zones to be returned
            :type consecutive_zones: ``int``

            :return: The list of consecutive zone id
            :rtype: ``list[int]``
            """
            starting_zone_id = random.randint(0, len(zone_list) - consecutive_zones)
            return zone_list[starting_zone_id:starting_zone_id + consecutive_zones]
        # end def consecutive_zone_selector

        @classmethod
        def get_supported_zones(cls, valid_zone_id_list):
            """
            Return list of all zone id supported by device from valid zone id list

            :param valid_zone_id_list: The list of all valid zone id
            :type valid_zone_id_list: ``list[int]``

            :return: The list of supported zone id
            :rtype: ``list[int]``
            """
            valid_zone_list = HexList(reversed(valid_zone_id_list))
            supported_zones = []
            for zone_bit in range(1, 255):
                if valid_zone_list.testBit(zone_bit):
                    supported_zones.append(zone_bit)
                # end if
            # end for

            return supported_zones
        # end def get_supported_zones

        @classmethod
        def get_unsupported_zones(cls, valid_zone_id_list):
            """
            Return list of all unsupported zone id from valid zone id list

            :param valid_zone_id_list: The list of all valid zone id
            :type valid_zone_id_list: ``list``

            :return: The list of unsupported zone id
            :rtype: ``list[int]``
            """
            unsupported_zones = []
            valid_zone_list = HexList(reversed(valid_zone_id_list))

            for zone_bit in range(1, 255):
                if not valid_zone_list.testBit(zone_bit):
                    unsupported_zones.append(zone_bit)
                # end if
            # end for

            return unsupported_zones
        # end def get_unsupported_zones

        @classmethod
        def get_zone_info(cls, test_case):
            """
            Return list of all supported, unsupported zone lists

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: The lists of supported and unsupported zone id
            :rtype: ``list[list[int], list[int]]``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.PER_KEY_LIGHTING.ZONE_INFO_TABLE
            valid_zone_list = []

            for param in [int(x) for x in config.F_SupportedZoneParam]:
                valid_zone_list.extend([config.F_ZonePresenceGroup0[param],
                                        config.F_ZonePresenceGroup1[param],  config.F_ZonePresenceGroup2[param],
                                        config.F_ZonePresenceGroup3[param],  config.F_ZonePresenceGroup4[param],
                                        config.F_ZonePresenceGroup5[param],  config.F_ZonePresenceGroup6[param],
                                        config.F_ZonePresenceGroup7[param],  config.F_ZonePresenceGroup8[param],
                                        config.F_ZonePresenceGroup9[param],  config.F_ZonePresenceGroup10[param],
                                        config.F_ZonePresenceGroup11[param], config.F_ZonePresenceGroup12[param],
                                        config.F_ZonePresenceGroup13[param]])
            # end for
            supported_zone_list = PerKeyLightingTestUtils.HIDppHelper.get_supported_zones(valid_zone_list)
            unsupported_zone_list = PerKeyLightingTestUtils.HIDppHelper.get_unsupported_zones(valid_zone_list)

            return [supported_zone_list, unsupported_zone_list]
        # end def get_zone_info
    # end class HIDppHelper
# end class PerKeyLightingTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
