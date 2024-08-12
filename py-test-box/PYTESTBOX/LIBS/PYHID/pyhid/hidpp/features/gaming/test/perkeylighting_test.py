#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.gaming.test.perkeylighting_test
:brief: HID++ 2.0 ``PerKeyLighting`` test module
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.perkeylighting import FrameEnd
from pyhid.hidpp.features.gaming.perkeylighting import FrameEndResponse
from pyhid.hidpp.features.gaming.perkeylighting import GetInfo
from pyhid.hidpp.features.gaming.perkeylighting import GetInfoResponse
from pyhid.hidpp.features.gaming.perkeylighting import PerKeyLighting
from pyhid.hidpp.features.gaming.perkeylighting import PerKeyLightingFactory
from pyhid.hidpp.features.gaming.perkeylighting import PerKeyLightingV0
from pyhid.hidpp.features.gaming.perkeylighting import PerKeyLightingV2
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZones
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZonesDeltaCompression4bit
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZonesDeltaCompression4bitResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZonesDeltaCompression5bit
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZonesDeltaCompression5bitResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetConsecutiveRGBZonesResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetIndividualRGBZones
from pyhid.hidpp.features.gaming.perkeylighting import SetIndividualRGBZonesResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetRGBZonesSingleValue
from pyhid.hidpp.features.gaming.perkeylighting import SetRGBZonesSingleValueResponse
from pyhid.hidpp.features.gaming.perkeylighting import SetRangeRGBZones
from pyhid.hidpp.features.gaming.perkeylighting import SetRangeRGBZonesResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PerKeyLightingInstantiationTestCase(TestCase):
    """
    Test ``PerKeyLighting`` testing classes instantiations
    """

    @staticmethod
    def test_per_key_lighting():
        """
        Test ``PerKeyLighting`` class instantiation
        """
        my_class = PerKeyLighting(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = PerKeyLighting(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_per_key_lighting

    @staticmethod
    def test_get_info():
        """
        Test ``GetInfo`` class instantiation
        """
        my_class = GetInfo(device_index=0, feature_index=0,
                           type_of_info=0,
                           param1=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetInfo(device_index=0xff, feature_index=0xff,
                           type_of_info=0xff,
                           param1=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_info

    @staticmethod
    def test_get_info_response():
        """
        Test ``GetInfoResponse`` class instantiation
        """
        my_class = GetInfoResponse(device_index=0, feature_index=0,
                                   type_of_info=0,
                                   param1=0,
                                   zone_byte_0=0,
                                   zone_byte_1=0,
                                   zone_byte_2=0,
                                   zone_byte_3=0,
                                   zone_byte_4=0,
                                   zone_byte_5=0,
                                   zone_byte_6=0,
                                   zone_byte_7=0,
                                   zone_byte_8=0,
                                   zone_byte_9=0,
                                   zone_byte_10=0,
                                   zone_byte_11=0,
                                   zone_byte_12=0,
                                   zone_byte_13=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetInfoResponse(device_index=0xff, feature_index=0xff,
                                   type_of_info=0xff,
                                   param1=0xff,
                                   zone_byte_0=0xff,
                                   zone_byte_1=0xff,
                                   zone_byte_2=0xff,
                                   zone_byte_3=0xff,
                                   zone_byte_4=0xff,
                                   zone_byte_5=0xff,
                                   zone_byte_6=0xff,
                                   zone_byte_7=0xff,
                                   zone_byte_8=0xff,
                                   zone_byte_9=0xff,
                                   zone_byte_10=0xff,
                                   zone_byte_11=0xff,
                                   zone_byte_12=0xff,
                                   zone_byte_13=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_info_response

    @staticmethod
    def test_set_individual_rgb_zones():
        """
        Test ``SetIndividualRGBZones`` class instantiation
        """
        my_class = SetIndividualRGBZones(device_index=0, feature_index=0,
                                         rgb_zone_id_0=0,
                                         red_index_0=0,
                                         green_index_0=0,
                                         blue_index_0=0,
                                         rgb_zone_id_1=0,
                                         red_index_1=0,
                                         green_index_1=0,
                                         blue_index_1=0,
                                         rgb_zone_id_2=0,
                                         red_index_2=0,
                                         green_index_2=0,
                                         blue_index_2=0,
                                         rgb_zone_id_3=0,
                                         red_index_3=0,
                                         green_index_3=0,
                                         blue_index_3=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIndividualRGBZones(device_index=0xff, feature_index=0xff,
                                         rgb_zone_id_0=0xff,
                                         red_index_0=0xff,
                                         green_index_0=0xff,
                                         blue_index_0=0xff,
                                         rgb_zone_id_1=0xff,
                                         red_index_1=0xff,
                                         green_index_1=0xff,
                                         blue_index_1=0xff,
                                         rgb_zone_id_2=0xff,
                                         red_index_2=0xff,
                                         green_index_2=0xff,
                                         blue_index_2=0xff,
                                         rgb_zone_id_3=0xff,
                                         red_index_3=0xff,
                                         green_index_3=0xff,
                                         blue_index_3=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_individual_rgb_zones

    @staticmethod
    def test_set_individual_rgb_zones_response():
        """
        Test ``SetIndividualRGBZonesResponse`` class instantiation
        """
        my_class = SetIndividualRGBZonesResponse(device_index=0, feature_index=0,
                                                 rgb_zone_id_0=0,
                                                 rgb_zone_id_1=0,
                                                 rgb_zone_id_2=0,
                                                 rgb_zone_id_3=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetIndividualRGBZonesResponse(device_index=0xff, feature_index=0xff,
                                                 rgb_zone_id_0=0xff,
                                                 rgb_zone_id_1=0xff,
                                                 rgb_zone_id_2=0xff,
                                                 rgb_zone_id_3=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_individual_rgb_zones_response

    @staticmethod
    def test_set_consecutive_rgb_zones():
        """
        Test ``SetConsecutiveRGBZones`` class instantiation
        """
        my_class = SetConsecutiveRGBZones(device_index=0, feature_index=0,
                                          rgb_zone_id_0=0,
                                          red_index_0=0,
                                          green_index_0=0,
                                          blue_index_0=0,
                                          red_index_1=0,
                                          green_index_1=0,
                                          blue_index_1=0,
                                          red_index_2=0,
                                          green_index_2=0,
                                          blue_index_2=0,
                                          red_index_3=0,
                                          green_index_3=0,
                                          blue_index_3=0,
                                          red_index_4=0,
                                          green_index_4=0,
                                          blue_index_4=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetConsecutiveRGBZones(device_index=0xff, feature_index=0xff,
                                          rgb_zone_id_0=0xff,
                                          red_index_0=0xff,
                                          green_index_0=0xff,
                                          blue_index_0=0xff,
                                          red_index_1=0xff,
                                          green_index_1=0xff,
                                          blue_index_1=0xff,
                                          red_index_2=0xff,
                                          green_index_2=0xff,
                                          blue_index_2=0xff,
                                          red_index_3=0xff,
                                          green_index_3=0xff,
                                          blue_index_3=0xff,
                                          red_index_4=0xff,
                                          green_index_4=0xff,
                                          blue_index_4=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_consecutive_rgb_zones

    @staticmethod
    def test_set_consecutive_rgb_zones_response():
        """
        Test ``SetConsecutiveRGBZonesResponse`` class instantiation
        """
        my_class = SetConsecutiveRGBZonesResponse(device_index=0, feature_index=0,
                                                  rgb_zone_id_0=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetConsecutiveRGBZonesResponse(device_index=0xff, feature_index=0xff,
                                                  rgb_zone_id_0=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_consecutive_rgb_zones_response

    @staticmethod
    def test_set_consecutive_rgb_zones_delta_compression_5bit():
        """
        Test ``SetConsecutiveRGBZonesDeltaCompression5bit`` class instantiation
        """
        my_class = SetConsecutiveRGBZonesDeltaCompression5bit(device_index=0, feature_index=0,
                                                              rgb_zone_id_0=0,
                                                              red_index_0=0,
                                                              green_index_0=0,
                                                              blue_index_0=0,
                                                              red_index_1=0,
                                                              green_index_1=0,
                                                              blue_index_1=0,
                                                              red_index_2=0,
                                                              green_index_2=0,
                                                              blue_index_2=0,
                                                              red_index_3=0,
                                                              green_index_3=0,
                                                              blue_index_3=0,
                                                              red_index_4=0,
                                                              green_index_4=0,
                                                              blue_index_4=0,
                                                              red_index_5=0,
                                                              green_index_5=0,
                                                              blue_index_5=0,
                                                              red_index_6=0,
                                                              green_index_6=0,
                                                              blue_index_6=0,
                                                              red_index_7=0,
                                                              green_index_7=0,
                                                              blue_index_7=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetConsecutiveRGBZonesDeltaCompression5bit(device_index=0xff, feature_index=0xff,
                                                              rgb_zone_id_0=0xff,
                                                              red_index_0=0x1f,
                                                              green_index_0=0x1f,
                                                              blue_index_0=0x1f,
                                                              red_index_1=0x1f,
                                                              green_index_1=0x1f,
                                                              blue_index_1=0x1f,
                                                              red_index_2=0x1f,
                                                              green_index_2=0x1f,
                                                              blue_index_2=0x1f,
                                                              red_index_3=0x1f,
                                                              green_index_3=0x1f,
                                                              blue_index_3=0x1f,
                                                              red_index_4=0x1f,
                                                              green_index_4=0x1f,
                                                              blue_index_4=0x1f,
                                                              red_index_5=0x1f,
                                                              green_index_5=0x1f,
                                                              blue_index_5=0x1f,
                                                              red_index_6=0x1f,
                                                              green_index_6=0x1f,
                                                              blue_index_6=0x1f,
                                                              red_index_7=0x1f,
                                                              green_index_7=0x1f,
                                                              blue_index_7=0x1f)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_consecutive_rgb_zones_delta_compression_5bit

    @staticmethod
    def test_set_consecutive_rgb_zones_delta_compression_5bit_response():
        """
        Test ``SetConsecutiveRGBZonesDeltaCompression5bitResponse`` class instantiation
        """
        my_class = SetConsecutiveRGBZonesDeltaCompression5bitResponse(device_index=0, feature_index=0,
                                                                      rgb_zone_id_0=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetConsecutiveRGBZonesDeltaCompression5bitResponse(device_index=0xff, feature_index=0xff,
                                                                      rgb_zone_id_0=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_consecutive_rgb_zones_delta_compression_5bit_response

    @staticmethod
    def test_set_consecutive_rgb_zones_delta_compression_4bit():
        """
        Test ``SetConsecutiveRGBZonesDeltaCompression4bit`` class instantiation
        """
        my_class = SetConsecutiveRGBZonesDeltaCompression4bit(device_index=0, feature_index=0,
                                                              rgb_zone_id_0=0,
                                                              red_index_0=0,
                                                              green_index_0=0,
                                                              blue_index_0=0,
                                                              red_index_1=0,
                                                              green_index_1=0,
                                                              blue_index_1=0,
                                                              red_index_2=0,
                                                              green_index_2=0,
                                                              blue_index_2=0,
                                                              red_index_3=0,
                                                              green_index_3=0,
                                                              blue_index_3=0,
                                                              red_index_4=0,
                                                              green_index_4=0,
                                                              blue_index_4=0,
                                                              red_index_5=0,
                                                              green_index_5=0,
                                                              blue_index_5=0,
                                                              red_index_6=0,
                                                              green_index_6=0,
                                                              blue_index_6=0,
                                                              red_index_7=0,
                                                              green_index_7=0,
                                                              blue_index_7=0,
                                                              red_index_8=0,
                                                              green_index_8=0,
                                                              blue_index_8=0,
                                                              red_index_9=0,
                                                              green_index_9=0,
                                                              blue_index_9=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetConsecutiveRGBZonesDeltaCompression4bit(device_index=0xff, feature_index=0xff,
                                                              rgb_zone_id_0=0xff,
                                                              red_index_0=0xf,
                                                              green_index_0=0xf,
                                                              blue_index_0=0xf,
                                                              red_index_1=0xf,
                                                              green_index_1=0xf,
                                                              blue_index_1=0xf,
                                                              red_index_2=0xf,
                                                              green_index_2=0xf,
                                                              blue_index_2=0xf,
                                                              red_index_3=0xf,
                                                              green_index_3=0xf,
                                                              blue_index_3=0xf,
                                                              red_index_4=0xf,
                                                              green_index_4=0xf,
                                                              blue_index_4=0xf,
                                                              red_index_5=0xf,
                                                              green_index_5=0xf,
                                                              blue_index_5=0xf,
                                                              red_index_6=0xf,
                                                              green_index_6=0xf,
                                                              blue_index_6=0xf,
                                                              red_index_7=0xf,
                                                              green_index_7=0xf,
                                                              blue_index_7=0xf,
                                                              red_index_8=0xf,
                                                              green_index_8=0xf,
                                                              blue_index_8=0xf,
                                                              red_index_9=0xf,
                                                              green_index_9=0xf,
                                                              blue_index_9=0xf)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_consecutive_rgb_zones_delta_compression_4bit

    @staticmethod
    def test_set_consecutive_rgb_zones_delta_compression_4bit_response():
        """
        Test ``SetConsecutiveRGBZonesDeltaCompression4bitResponse`` class instantiation
        """
        my_class = SetConsecutiveRGBZonesDeltaCompression4bitResponse(device_index=0, feature_index=0,
                                                                      rgb_zone_id_0=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetConsecutiveRGBZonesDeltaCompression4bitResponse(device_index=0xff, feature_index=0xff,
                                                                      rgb_zone_id_0=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_consecutive_rgb_zones_delta_compression_4bit_response

    @staticmethod
    def test_set_range_rgb_zones():
        """
        Test ``SetRangeRGBZones`` class instantiation
        """
        my_class = SetRangeRGBZones(device_index=0, feature_index=0,
                                    rgb_first_zone_id_0=0,
                                    rgb_last_zone_id_0=0,
                                    red_index_0=0,
                                    green_index_0=0,
                                    blue_index_0=0,
                                    rgb_first_zone_id_1=0,
                                    rgb_last_zone_id_1=0,
                                    red_index_1=0,
                                    green_index_1=0,
                                    blue_index_1=0,
                                    rgb_first_zone_id_2=0,
                                    rgb_last_zone_id_2=0,
                                    red_index_2=0,
                                    green_index_2=0,
                                    blue_index_2=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRangeRGBZones(device_index=0xff, feature_index=0xff,
                                    rgb_first_zone_id_0=0xff,
                                    rgb_last_zone_id_0=0xff,
                                    red_index_0=0xff,
                                    green_index_0=0xff,
                                    blue_index_0=0xff,
                                    rgb_first_zone_id_1=0xff,
                                    rgb_last_zone_id_1=0xff,
                                    red_index_1=0xff,
                                    green_index_1=0xff,
                                    blue_index_1=0xff,
                                    rgb_first_zone_id_2=0xff,
                                    rgb_last_zone_id_2=0xff,
                                    red_index_2=0xff,
                                    green_index_2=0xff,
                                    blue_index_2=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_range_rgb_zones

    @staticmethod
    def test_set_range_rgb_zones_response():
        """
        Test ``SetRangeRGBZonesResponse`` class instantiation
        """
        my_class = SetRangeRGBZonesResponse(device_index=0, feature_index=0,
                                            rgb_first_zone_id_0=0,
                                            rgb_first_zone_id_1=0,
                                            rgb_first_zone_id_2=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRangeRGBZonesResponse(device_index=0xff, feature_index=0xff,
                                            rgb_first_zone_id_0=0xff,
                                            rgb_first_zone_id_1=0xff,
                                            rgb_first_zone_id_2=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_range_rgb_zones_response

    @staticmethod
    def test_set_rgb_zones_single_value():
        """
        Test ``SetRGBZonesSingleValue`` class instantiation
        """
        my_class = SetRGBZonesSingleValue(device_index=0, feature_index=0,
                                          rgb_zone_red=0,
                                          rgb_zone_green=0,
                                          rgb_zone_blue=0,
                                          rgb_zone_id_0=0,
                                          rgb_zone_id_1=0,
                                          rgb_zone_id_2=0,
                                          rgb_zone_id_3=0,
                                          rgb_zone_id_4=0,
                                          rgb_zone_id_5=0,
                                          rgb_zone_id_6=0,
                                          rgb_zone_id_7=0,
                                          rgb_zone_id_8=0,
                                          rgb_zone_id_9=0,
                                          rgb_zone_id_10=0,
                                          rgb_zone_id_11=0,
                                          rgb_zone_id_12=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRGBZonesSingleValue(device_index=0xff, feature_index=0xff,
                                          rgb_zone_red=0xff,
                                          rgb_zone_green=0xff,
                                          rgb_zone_blue=0xff,
                                          rgb_zone_id_0=0xff,
                                          rgb_zone_id_1=0xff,
                                          rgb_zone_id_2=0xff,
                                          rgb_zone_id_3=0xff,
                                          rgb_zone_id_4=0xff,
                                          rgb_zone_id_5=0xff,
                                          rgb_zone_id_6=0xff,
                                          rgb_zone_id_7=0xff,
                                          rgb_zone_id_8=0xff,
                                          rgb_zone_id_9=0xff,
                                          rgb_zone_id_10=0xff,
                                          rgb_zone_id_11=0xff,
                                          rgb_zone_id_12=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rgb_zones_single_value

    @staticmethod
    def test_set_rgb_zones_single_value_response():
        """
        Test ``SetRGBZonesSingleValueResponse`` class instantiation
        """
        my_class = SetRGBZonesSingleValueResponse(device_index=0, feature_index=0,
                                                  rgb_zone_red=0,
                                                  rgb_zone_green=0,
                                                  rgb_zone_blue=0,
                                                  rgb_zone_id_0=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetRGBZonesSingleValueResponse(device_index=0xff, feature_index=0xff,
                                                  rgb_zone_red=0xff,
                                                  rgb_zone_green=0xff,
                                                  rgb_zone_blue=0xff,
                                                  rgb_zone_id_0=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_rgb_zones_single_value_response

    @staticmethod
    def test_frame_end():
        """
        Test ``FrameEnd`` class instantiation
        """
        my_class = FrameEnd(device_index=0, feature_index=0,
                            persistence=0,
                            current_frame=0,
                            n_frames_till_next_change=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = FrameEnd(device_index=0xff, feature_index=0xff,
                            persistence=0xff,
                            current_frame=0xffff,
                            n_frames_till_next_change=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_frame_end

    @staticmethod
    def test_frame_end_response():
        """
        Test ``FrameEndResponse`` class instantiation
        """
        my_class = FrameEndResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = FrameEndResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_frame_end_response
# end class PerKeyLightingInstantiationTestCase


class PerKeyLightingTestCase(TestCase):
    """
    Test ``PerKeyLighting`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            PerKeyLightingV0.VERSION: {
                "cls": PerKeyLightingV0,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponse,
                    "set_individual_rgb_zones_cls": SetIndividualRGBZones,
                    "set_individual_rgb_zones_response_cls": SetIndividualRGBZonesResponse,
                    "set_consecutive_rgb_zones_cls": SetConsecutiveRGBZones,
                    "set_consecutive_rgb_zones_response_cls": SetConsecutiveRGBZonesResponse,
                    "set_consecutive_rgb_zones_delta_compression_5bit_cls": SetConsecutiveRGBZonesDeltaCompression5bit,
                    "set_consecutive_rgb_zones_delta_compression_5bit_response_cls":
                        SetConsecutiveRGBZonesDeltaCompression5bitResponse,
                    "set_consecutive_rgb_zones_delta_compression_4bit_cls":
                        SetConsecutiveRGBZonesDeltaCompression4bit,
                    "set_consecutive_rgb_zones_delta_compression_4bit_response_cls":
                        SetConsecutiveRGBZonesDeltaCompression4bitResponse,
                    "set_range_rgb_zones_cls": SetRangeRGBZones,
                    "set_range_rgb_zones_response_cls": SetRangeRGBZonesResponse,
                    "set_rgb_zones_single_value_cls": SetRGBZonesSingleValue,
                    "set_rgb_zones_single_value_response_cls": SetRGBZonesSingleValueResponse,
                    "frame_end_cls": FrameEnd,
                    "frame_end_response_cls": FrameEndResponse,
                },
                "max_function_index": 7
            },
            PerKeyLightingV2.VERSION: {
                "cls": PerKeyLightingV2,
                "interfaces": {
                    "get_info_cls": GetInfo,
                    "get_info_response_cls": GetInfoResponse,
                    "set_individual_rgb_zones_cls": SetIndividualRGBZones,
                    "set_individual_rgb_zones_response_cls": SetIndividualRGBZonesResponse,
                    "set_consecutive_rgb_zones_cls": SetConsecutiveRGBZones,
                    "set_consecutive_rgb_zones_response_cls": SetConsecutiveRGBZonesResponse,
                    "set_consecutive_rgb_zones_delta_compression_5bit_cls": SetConsecutiveRGBZonesDeltaCompression5bit,
                    "set_consecutive_rgb_zones_delta_compression_5bit_response_cls":
                        SetConsecutiveRGBZonesDeltaCompression5bitResponse,
                    "set_consecutive_rgb_zones_delta_compression_4bit_cls": SetConsecutiveRGBZonesDeltaCompression4bit,
                    "set_consecutive_rgb_zones_delta_compression_4bit_response_cls":
                        SetConsecutiveRGBZonesDeltaCompression4bitResponse,
                    "set_range_rgb_zones_cls": SetRangeRGBZones,
                    "set_range_rgb_zones_response_cls": SetRangeRGBZonesResponse,
                    "set_rgb_zones_single_value_cls": SetRGBZonesSingleValue,
                    "set_rgb_zones_single_value_response_cls": SetRGBZonesSingleValueResponse,
                    "frame_end_cls": FrameEnd,
                    "frame_end_response_cls": FrameEndResponse,
                },
                "max_function_index": 7
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``PerKeyLightingFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(PerKeyLightingFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``PerKeyLightingFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [3, 4]:
            with self.assertRaises(KeyError):
                PerKeyLightingFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``PerKeyLightingFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = PerKeyLightingFactory.create(version)
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
            obj = PerKeyLightingFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class PerKeyLightingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
