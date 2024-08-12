#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8081.functionality
:brief: HID++ 2.0 ``PerKeyLighting`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/11/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from itertools import zip_longest

from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.perkeylightingutils import PerKeyLightingTestUtils
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.gaming.feature_8081.perkeylighting import PerKeyLightingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_CHECK_RGB_VALUE = "TODO: For each zone, check the RGB value by LED Indicator/LED Driver IC shall be same as inputs"
_FRAME_END = "Send frameEnd w/ all inputs = 0"
_CHECK_SET_RGB_ZONES_SINGLE_VALUE = "Check SetRGBZonesSingleValueResponse fields"
_SEND_SET_RGB_ZONES_SINGLE_VALUE_REQ = "Send SetRGBZonesSingleValue request"
_ADD_TO_SETTING_LIST = "Set {starting_zone, rgbValues=delta_rgb} to settingList"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PerKeyLightingFunctionalityTestCase(PerKeyLightingTestCase):
    """
    Validate ``PerKeyLighting`` functionality test cases
    """

    @features("Feature8081")
    @level("Functionality")
    def test_check_get_info_response_with_product_specification(self):
        """
        Dump all of available zones information of device.

        [0] getInfo(typeOfInfo, param1) -> lightingInfo
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over n in range[0..2]")
        # --------------------------------------------------------------------------------------------------------------
        for param in [0, 1, 2]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with param1: {param}")
            # ----------------------------------------------------------------------------------------------------------
            get_info_response = PerKeyLightingTestUtils.HIDppHelper.get_info(test_case=self,
                                                                             type_of_info=0x0,
                                                                             param1=param)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the returned supported/non-supported info of zoneID shall be same as"
                                      "product definition.")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.GetInfoResponseChecker
            check_map = checker.get_check_map_from_param1(self, param1_value=param)
            checker.check_fields(self, get_info_response, self.feature_8081.get_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8081_0001", _AUTHOR)
    # end def test_check_get_info_response_with_product_specification

    @features("Feature8081")
    @level("Functionality")
    def test_set_individual_rgb_zones_to_all_valid_zones(self):
        """
        Random select a color from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA}. Check can set the color to all of valid
        zones.(LED indicator or LED Driver IC)

        [1] setIndividualRGBZones(rgbIndividualZones, rgbValues) -> rgbIndividualZones
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Random select a color rgbValue")
        # --------------------------------------------------------------------------------------------------------------
        color = PerKeyLightingTestUtils.HIDppHelper.random_color_picker()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over z1, z2, z3, z4 in zoneList by step = 4")
        # --------------------------------------------------------------------------------------------------------------
        for zones in zip_longest(*[iter(self.supported_zone_list)] * 4, fillvalue='00'):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set {zn, rgbValue} pairs to settingList")
            # ----------------------------------------------------------------------------------------------------------
            z1, z2, z3, z4 = zones
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, red_index_2, \
                green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3 = color * 4

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetIndividualRGBZones request")
            # ---------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(test_case=self,
                                                                                    rgb_zone_id_0=z1,
                                                                                    rgb_zone_id_1=z2,
                                                                                    rgb_zone_id_2=z3,
                                                                                    rgb_zone_id_3=z4,
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
                                                                                    blue_index_3=blue_index_3)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneIDs shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, z1),
                "rgb_zone_id_1": (checker.check_rgb_zone_id_1, z2),
                "rgb_zone_id_2": (checker.check_rgb_zone_id_2, z3),
                "rgb_zone_id_3": (checker.check_rgb_zone_id_3, z4),
            })
            checker.check_fields(self, response, self.feature_8081.set_individual_rgb_zones_response_cls,
                                 check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _FRAME_END)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self,
                                                      persistence=0x0,
                                                      current_frame=0x0,
                                                      n_frames_till_next_change=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "For all of zones, check the RGB value by LED Indicator/LED Driver IC shall be same"
                                  "as inputs")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: implement this check with kosmos
        
        self.testCaseChecked("FUN_8081_0002", _AUTHOR)
    # end def test_set_individual_rgb_zones_to_all_valid_zones

    @features("Feature8081")
    @level("Functionality")
    def test_set_consecutive_rgb_zones_all_valid_zones(self):
        """
        Random select a color from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA}. Check can set the color to all of
        available zones. (LED indicator or LED Driver IC)

        [2] setConsecutiveRGBZones(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Random select a color rgb from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA}")
        # --------------------------------------------------------------------------------------------------------------
        color = PerKeyLightingTestUtils.HIDppHelper.random_color_picker()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over z in zoneList by step = 5")
        # --------------------------------------------------------------------------------------------------------------
        for zones in zip_longest(*[iter(self.supported_zone_list)] * 5, fillvalue='00'):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set {z, rgb, rgb, rgb, rgb, rgb} to settingList")
            # ----------------------------------------------------------------------------------------------------------
            z1, z2, z3, z4, z5 = zones
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, \
                red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3, \
                red_index_4, green_index_4, blue_index_4, = color * 5

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConsecutiveRGBZones request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones(test_case=self,
                                                                          rgb_zone_id_0=z1,
                                                                          red_index_0=red_index_0,
                                                                          green_index_0=green_index_0,
                                                                          blue_index_0=blue_index_0,
                                                                          red_index_1=red_index_1,
                                                                          green_index_1=green_index_2,
                                                                          blue_index_1=green_index_1,
                                                                          red_index_2=red_index_2,
                                                                          green_index_2=green_index_2,
                                                                          blue_index_2=blue_index_2,
                                                                          red_index_3=red_index_3,
                                                                          green_index_3=green_index_3,
                                                                          blue_index_3=blue_index_3,
                                                                          red_index_4=red_index_4,
                                                                          green_index_4=green_index_4,
                                                                          blue_index_4=blue_index_4)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetConsecutiveRGBZonesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, z1),
            })
            checker.check_fields(self, response, self.feature_8081.set_consecutive_rgb_zones_response_cls,
                                 check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _FRAME_END)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self,
                                                      persistence=0x0,
                                                      current_frame=0x0,
                                                      n_frames_till_next_change=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_RGB_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        # TODO: implement this check with kosmos

        self.testCaseChecked("FUN_8081_0003", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_all_valid_zones

    @features("Feature8081")
    @level("Functionality")
    def test_apply_all_delta_5bit_values(self):
        """
        Start from the Zone 1. Set 8 consecutive zones to color(128, 128, 128). Apply delta from -16 to +15 and check
        the result shall be same as expected. (LED indicator or LED Driver IC)
        
        [3] setConsecutiveRGBZonesDeltaCompression5bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start from zone 1 to select 8 consecutive zones . And the starting_zone is zone 1.")
        # --------------------------------------------------------------------------------------------------------------
        z1, z2, z3, z4, z5, z6, z7, z8 = self.supported_zone_list[:8]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set [128, 128, 128, zoneID[0], .., zoneID[7], 0xFF] to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0x80
        rgb_zone_green = 0x80
        rgb_zone_blue = 0x80
        rgb_zone_id_0 = z1
        rgb_zone_id_1 = z2
        rgb_zone_id_2 = z3
        rgb_zone_id_3 = z4
        rgb_zone_id_4 = z5
        rgb_zone_id_5 = z6
        rgb_zone_id_6 = z7
        rgb_zone_id_7 = z8
        rgb_zone_id_8 = 0xff
        rgb_zone_id_9 = 0xff
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_RGB_ZONES_SINGLE_VALUE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(
            test_case=self,
            device_index=ChannelUtils.get_device_index(test_case=self),
            rgb_zone_red=rgb_zone_red,
            rgb_zone_green=rgb_zone_green,
            rgb_zone_blue=rgb_zone_blue,
            rgb_zone_id_0=rgb_zone_id_0,
            rgb_zone_id_1=rgb_zone_id_1,
            rgb_zone_id_2=rgb_zone_id_2,
            rgb_zone_id_3=rgb_zone_id_3,
            rgb_zone_id_4=rgb_zone_id_4,
            rgb_zone_id_5=rgb_zone_id_5,
            rgb_zone_id_6=rgb_zone_id_6,
            rgb_zone_id_7=rgb_zone_id_7,
            rgb_zone_id_8=rgb_zone_id_8,
            rgb_zone_id_9=rgb_zone_id_9,
            rgb_zone_id_10=rgb_zone_id_10,
            rgb_zone_id_11=rgb_zone_id_11,
            rgb_zone_id_12=rgb_zone_id_12
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_SET_RGB_ZONES_SINGLE_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over delta_rgb in range[-16..15]")
        # --------------------------------------------------------------------------------------------------------------
        positive_delta = list(range(0, 16))
        negative_delta = list(range(31, 16, -1))
        delta_values_5_bit = negative_delta + positive_delta

        for i in delta_values_5_bit:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, _ADD_TO_SETTING_LIST)
            # ----------------------------------------------------------------------------------------------------------
            starting_zone_id = rgb_zone_id_0
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, \
                red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3, \
                red_index_4, green_index_4, blue_index_4, red_index_5, green_index_5, blue_index_5, \
                red_index_6, green_index_6, blue_index_6, red_index_7, green_index_7, blue_index_7 = [i] * 24

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConsecutiveRGBZonesDeltaCompression5bit request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones_delta_compression_5bit(
                test_case=self,
                rgb_zone_id_0=rgb_zone_id_0,
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
                blue_index_7=blue_index_7
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneID shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression5bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, starting_zone_id),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _FRAME_END)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self,
                                                          persistence=0x0,
                                                          current_frame=0x0,
                                                          n_frames_till_next_change=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_RGB_VALUE)
            # ----------------------------------------------------------------------------------------------------------
            # TODO: implement this check with kosmos
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8081_0004", _AUTHOR)
    # end def test_apply_all_delta_5bit_values

    @features("Feature8081")
    @level("Functionality")
    def test_alternate_min_max_values_5bit_delta(self):
        """
        Start from the Zone 1. Set 8 consecutive zones to color(255, 255, 255). Apply the delta 1 and check the result
        shall be color(0, 0, 0). Apply the delta -1 and check the result shall be color(255, 255, 255). (LED indicator
        or LED Driver IC)
        
        [3] setConsecutiveRGBZonesDeltaCompression5bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start from zone 1 to select 8 consecutive zones . And the starting_zone is zone 1.")
        # --------------------------------------------------------------------------------------------------------------
        z1, z2, z3, z4, z5, z6, z7, z8, = self.supported_zone_list[:8]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set [255, 255, 255, zoneID[0], .., zoneID[7], 0xFF] to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0xff
        rgb_zone_green = 0xff
        rgb_zone_blue = 0xff
        rgb_zone_id_0 = z1
        rgb_zone_id_1 = z2
        rgb_zone_id_2 = z3
        rgb_zone_id_3 = z4
        rgb_zone_id_4 = z5
        rgb_zone_id_5 = z6
        rgb_zone_id_6 = z7
        rgb_zone_id_7 = z8
        rgb_zone_id_8 = 0xff
        rgb_zone_id_9 = 0xff
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_RGB_ZONES_SINGLE_VALUE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(
            test_case=self,
            rgb_zone_red=rgb_zone_red,
            rgb_zone_green=rgb_zone_green,
            rgb_zone_blue=rgb_zone_blue,
            rgb_zone_id_0=rgb_zone_id_0,
            rgb_zone_id_1=rgb_zone_id_1,
            rgb_zone_id_2=rgb_zone_id_2,
            rgb_zone_id_3=rgb_zone_id_3,
            rgb_zone_id_4=rgb_zone_id_4,
            rgb_zone_id_5=rgb_zone_id_5,
            rgb_zone_id_6=rgb_zone_id_6,
            rgb_zone_id_7=rgb_zone_id_7,
            rgb_zone_id_8=rgb_zone_id_8,
            rgb_zone_id_9=rgb_zone_id_9,
            rgb_zone_id_10=rgb_zone_id_10,
            rgb_zone_id_11=rgb_zone_id_11,
            rgb_zone_id_12=rgb_zone_id_12
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_SET_RGB_ZONES_SINGLE_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over delta_rgb in [1, -1]")
        # --------------------------------------------------------------------------------------------------------------
        for i in [17, 1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, _ADD_TO_SETTING_LIST)
            # ----------------------------------------------------------------------------------------------------------
            starting_zone_id = rgb_zone_id_0
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, \
                red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3, \
                red_index_4, green_index_4, blue_index_4, red_index_5, green_index_5, blue_index_5, \
                red_index_6, green_index_6, blue_index_6, red_index_7, green_index_7, blue_index_7 = [i] * 24

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConsecutiveRGBZonesDeltaCompression5bit fields")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones_delta_compression_5bit(
                test_case=self,
                rgb_zone_id_0=rgb_zone_id_0,
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
                blue_index_7=blue_index_7
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneID shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression5bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, starting_zone_id),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _FRAME_END)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self,
                                                          persistence=0x0,
                                                          current_frame=0x0,
                                                          n_frames_till_next_change=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_RGB_VALUE)
            # ----------------------------------------------------------------------------------------------------------
            # TODO: implement this check with kosmos
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8081_0005", _AUTHOR)
    # end def test_alternate_min_max_values_5bit_delta

    @features("Feature8081")
    @level("Functionality")
    def test_apply_all_delta_4bit_values(self):
        """
        Start from the Zone 1. Set 10 consecutive zones to color(128, 128, 128). Apply delta from -8 to +7 and check
        the result shall be same as expected. (LED indicator or LED Driver IC)
        
        [4] setConsecutiveRGBZonesDeltaCompression4bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Start from zone 1 to select 10 consecutive zones . And the starting_zone is zone 1.")
        # --------------------------------------------------------------------------------------------------------------
        z1, z2, z3, z4, z5, z6, z7, z8, z9, z10 = self.supported_zone_list[:10]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set [128, 128, 128, zoneID[0], .., zoneID[9], 0xFF] to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0x80
        rgb_zone_green = 0x80
        rgb_zone_blue = 0x80
        rgb_zone_id_0 = z1
        rgb_zone_id_1 = z2
        rgb_zone_id_2 = z3
        rgb_zone_id_3 = z4
        rgb_zone_id_4 = z5
        rgb_zone_id_5 = z6
        rgb_zone_id_6 = z7
        rgb_zone_id_7 = z8
        rgb_zone_id_8 = z9
        rgb_zone_id_9 = z10
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_RGB_ZONES_SINGLE_VALUE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(
            test_case=self,
            rgb_zone_red=rgb_zone_red,
            rgb_zone_green=rgb_zone_green,
            rgb_zone_blue=rgb_zone_blue,
            rgb_zone_id_0=rgb_zone_id_0,
            rgb_zone_id_1=rgb_zone_id_1,
            rgb_zone_id_2=rgb_zone_id_2,
            rgb_zone_id_3=rgb_zone_id_3,
            rgb_zone_id_4=rgb_zone_id_4,
            rgb_zone_id_5=rgb_zone_id_5,
            rgb_zone_id_6=rgb_zone_id_6,
            rgb_zone_id_7=rgb_zone_id_7,
            rgb_zone_id_8=rgb_zone_id_8,
            rgb_zone_id_9=rgb_zone_id_9,
            rgb_zone_id_10=rgb_zone_id_10,
            rgb_zone_id_11=rgb_zone_id_11,
            rgb_zone_id_12=rgb_zone_id_12
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_SET_RGB_ZONES_SINGLE_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over delta_rgb in range[-8..7]")
        # --------------------------------------------------------------------------------------------------------------
        negative_delta_values = list(range(15, 8, -1))
        positive_dela_values = list(range(0, 8))
        delta_values_4bit = negative_delta_values + positive_dela_values

        for i in delta_values_4bit:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _ADD_TO_SETTING_LIST)
            # ----------------------------------------------------------------------------------------------------------
            starting_zone_id = rgb_zone_id_0
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, \
                red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3, \
                red_index_4, green_index_4, blue_index_4, red_index_5, green_index_5, blue_index_5, \
                red_index_6, green_index_6, blue_index_6, red_index_7, green_index_7, blue_index_7, \
                red_index_8, green_index_8, blue_index_8, red_index_9, green_index_9, blue_index_9 = [i] * 30

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConsecutiveRGBZonesDeltaCompression4bit request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones_delta_compression_4bit(
                test_case=self,
                rgb_zone_id_0=rgb_zone_id_0,
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
                blue_index_9=blue_index_9
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneID shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression4bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, starting_zone_id),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _FRAME_END)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self, 
                                                          persistence=0x0,
                                                          current_frame=0x0,
                                                          n_frames_till_next_change=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_RGB_VALUE)
            # ----------------------------------------------------------------------------------------------------------
            # TODO implement this check with kosmos
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8081_0006", _AUTHOR)
    # end def test_apply_all_delta_4bit_values

    @features("Feature8081")
    @level("Functionality")
    def test_alternate_max_min_values_4bit_delta(self):
        """
        Start from the Zone 1. Set 10 consecutive zones to color(255, 255, 255). Apply the delta 1 and check the
        result shall be color(0, 0, 0). Apply the delta -1 and check the result shall be color(255, 255, 255). (LED
        indicator or LED Driver IC)
        
        [4] setConsecutiveRGBZonesDeltaCompression4bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Start from zone 1 to select 10 consecutive zones. And the starting_zone is zone 1.")
        # --------------------------------------------------------------------------------------------------------------
        z1, z2, z3, z4, z5, z6, z7, z8, z9, z10 = self.supported_zone_list[:10]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set [255, 255, 255, zoneID[0], .., zoneID[9], 0xFF] to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0xff
        rgb_zone_green = 0xff
        rgb_zone_blue = 0xff
        rgb_zone_id_0 = z1
        rgb_zone_id_1 = z2
        rgb_zone_id_2 = z3
        rgb_zone_id_3 = z4
        rgb_zone_id_4 = z5
        rgb_zone_id_5 = z6
        rgb_zone_id_6 = z7
        rgb_zone_id_7 = z8
        rgb_zone_id_8 = z9
        rgb_zone_id_9 = z10
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_RGB_ZONES_SINGLE_VALUE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(
            test_case=self,
            rgb_zone_red=rgb_zone_red,
            rgb_zone_green=rgb_zone_green,
            rgb_zone_blue=rgb_zone_blue,
            rgb_zone_id_0=rgb_zone_id_0,
            rgb_zone_id_1=rgb_zone_id_1,
            rgb_zone_id_2=rgb_zone_id_2,
            rgb_zone_id_3=rgb_zone_id_3,
            rgb_zone_id_4=rgb_zone_id_4,
            rgb_zone_id_5=rgb_zone_id_5,
            rgb_zone_id_6=rgb_zone_id_6,
            rgb_zone_id_7=rgb_zone_id_7,
            rgb_zone_id_8=rgb_zone_id_8,
            rgb_zone_id_9=rgb_zone_id_9,
            rgb_zone_id_10=rgb_zone_id_10,
            rgb_zone_id_11=rgb_zone_id_11,
            rgb_zone_id_12=rgb_zone_id_12
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_SET_RGB_ZONES_SINGLE_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over delta_rgb in [-1, 1]")
        # --------------------------------------------------------------------------------------------------------------
        for i in [9, 1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _ADD_TO_SETTING_LIST)
            # ----------------------------------------------------------------------------------------------------------
            starting_zone_id = rgb_zone_id_0
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, \
                red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3, \
                red_index_4, green_index_4, blue_index_4, red_index_5, green_index_5, blue_index_5, \
                red_index_6, green_index_6, blue_index_6, red_index_7, green_index_7, blue_index_7, \
                red_index_8, green_index_8, blue_index_8, red_index_9, green_index_9, blue_index_9 = [i] * 30

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConsecutiveRGBZonesDeltaCompression4bit request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones_delta_compression_4bit(
                test_case=self,
                rgb_zone_id_0=rgb_zone_id_0,
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
                blue_index_9=blue_index_9
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneID shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression4bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, starting_zone_id),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _FRAME_END)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self, 
                                                          persistence=0x0,
                                                          current_frame=0x0,
                                                          n_frames_till_next_change=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_RGB_VALUE)
            # ----------------------------------------------------------------------------------------------------------
            # TODO: implement this check with kosmos
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8081_0007", _AUTHOR)
    # end test_alternate_max_min_values_4bit_delta

    @features("Feature8081")
    @level("Functionality")
    def test_range_rgb_zones_all_consecutive_zones(self):
        """
        Random select a color from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA} and set the color to all of valid zones.
        (LED indicator or LED Driver IC)

        [5] setRangeRGBZones(rgbFirstZoneIDs, rgbLastZoneIDs, rgbValues) -> rgbFirstZoneIDs
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Collect all of consecutive zones from zoneList into groupList")
        # --------------------------------------------------------------------------------------------------------------
        consecutive_zones = self.supported_zone_list

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select a color rgbValue from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA} to all"
                                 "of groups, gn = {firstZoneID[n], lastZoneID[n], rgbValue}")
        # --------------------------------------------------------------------------------------------------------------
        color = PerKeyLightingTestUtils.HIDppHelper.random_color_picker()
        red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1,\
            red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3 = color * 4
        rgb_last_zone_id_0, rgb_last_zone_id_1, rgb_last_zone_id_2 = [consecutive_zones[-1]] * 3

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over g in groupList by step = 3")
        # --------------------------------------------------------------------------------------------------------------
        for zones in zip_longest(*[iter(consecutive_zones[:-1])] * 3, fillvalue='01'):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set [g1, g2(option), g3(option), 0xFF] to settingList where g1 or g2, g3 are"
                                     "available.")
            # ----------------------------------------------------------------------------------------------------------
            rgb_first_zone_id_0, rgb_first_zone_id_1, rgb_first_zone_id_2 = zones

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Send SetRangeRGBZones w/ {settingList}")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_range_rgb_zones(test_case=self,
                                                                    rgb_first_zone_id_0=rgb_first_zone_id_0,
                                                                    rgb_last_zone_id_0=rgb_last_zone_id_0,
                                                                    red_index_0=red_index_0,
                                                                    blue_index_0=blue_index_0,
                                                                    green_index_0=green_index_0,
                                                                    rgb_first_zone_id_1=rgb_first_zone_id_1,
                                                                    rgb_last_zone_id_1=rgb_last_zone_id_1,
                                                                    red_index_1=red_index_1,
                                                                    green_index_1=green_index_1,
                                                                    blue_index_1=blue_index_1,
                                                                    rgb_first_zone_id_2=rgb_first_zone_id_2,
                                                                    rgb_last_zone_id_2=rgb_last_zone_id_2,
                                                                    red_index_2=red_index_2,
                                                                    green_index_2=green_index_2,
                                                                    blue_index_2=blue_index_2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneIDs shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetRangeRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_first_zone_id_0": (checker.check_rgb_first_zone_id_0, rgb_first_zone_id_0),
                "rgb_first_zone_id_1": (checker.check_rgb_first_zone_id_1, rgb_first_zone_id_1),
                "rgb_first_zone_id_2": (checker.check_rgb_first_zone_id_2, rgb_first_zone_id_2),
            })
            checker.check_fields(self, response, self.feature_8081.set_range_rgb_zones_response_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _FRAME_END)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self, 
                                                      persistence=0x0,
                                                      current_frame=0x0,
                                                      n_frames_till_next_change=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_RGB_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        # TODO: implement this check with kosmos
        
        self.testCaseChecked("FUN_8081_0008", _AUTHOR)
    # end def test_range_rgb_zones_all_consecutive_zones

    @features("Feature8081")
    @level("Functionality")
    def test_set_zones_single_value_all_supported_zones(self):
        """
        Random select a color from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA}. Check can set the color to all of valid
        zones. (LED indicator or LED Driver IC)
        
        [6] setRGBZonesSingleValue(rgbZoneR, rgbZoneG, rgbZoneB, rgbZoneID[0], .., rgbZoneID[12]) -> rgbZoneR,
        rgbZoneG, rgbZoneB, rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select a color rgbValue from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA}")
        # --------------------------------------------------------------------------------------------------------------
        color = PerKeyLightingTestUtils.HIDppHelper.random_color_picker()
        rgb_zone_red, rgb_zone_green, rgb_zone_blue = color

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over z in zoneList by step 13")
        # --------------------------------------------------------------------------------------------------------------
        for zones in zip_longest(*[iter(self.supported_zone_list)] * 13, fillvalue='00'):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set [rgbValue, zoneID[0]..zoneID[12]] to settingList")
            # ----------------------------------------------------------------------------------------------------------
            rgb_zone_id_0, rgb_zone_id_1, rgb_zone_id_2, rgb_zone_id_3, \
                rgb_zone_id_4, rgb_zone_id_5, rgb_zone_id_6, rgb_zone_id_7, rgb_zone_id_8, rgb_zone_id_9, \
                rgb_zone_id_10, rgb_zone_id_11, rgb_zone_id_12 = zones

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_SET_RGB_ZONES_SINGLE_VALUE_REQ)
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(test_case=self,
                                                                                      rgb_zone_red=rgb_zone_red,
                                                                                      rgb_zone_green=rgb_zone_green,
                                                                                      rgb_zone_blue=rgb_zone_blue,
                                                                                      rgb_zone_id_0=rgb_zone_id_0,
                                                                                      rgb_zone_id_1=rgb_zone_id_1,
                                                                                      rgb_zone_id_2=rgb_zone_id_2,
                                                                                      rgb_zone_id_3=rgb_zone_id_3,
                                                                                      rgb_zone_id_4=rgb_zone_id_4,
                                                                                      rgb_zone_id_5=rgb_zone_id_5,
                                                                                      rgb_zone_id_6=rgb_zone_id_6,
                                                                                      rgb_zone_id_7=rgb_zone_id_7,
                                                                                      rgb_zone_id_8=rgb_zone_id_8,
                                                                                      rgb_zone_id_9=rgb_zone_id_9,
                                                                                      rgb_zone_id_10=rgb_zone_id_10,
                                                                                      rgb_zone_id_11=rgb_zone_id_11,
                                                                                      rgb_zone_id_12=rgb_zone_id_12)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_SET_RGB_ZONES_SINGLE_VALUE)
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
                "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
                "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
            })
            checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _FRAME_END)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self,
                                                      persistence=0x0,
                                                      current_frame=0x0,
                                                      n_frames_till_next_change=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_RGB_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        # TODO: implement this check with kosmos
        
        self.testCaseChecked("FUN_8081_0009", _AUTHOR)
    # end def test_set_zones_single_value_all_supported_zones

    @features("Feature8081")
    @level("Functionality")
    def test_can_reflect_changes_after_multiple_requests(self):
        """
        Check can reflect changes after set colors by setIndividualRGBZones, setRangeRGBZones and
        setRGBZonesSingleValue. (LED indicator or LED Driver IC)

        setIndividualRGBZons: zoneID = 1, color = RED 
        
        setRangeRGBZones: zoneID = 2, color = GREEN
        
        setRGBZonesSingleValue zoneID = 3, color = BLUE
        
        [7] void frameEnd(persistence, nFramesTillNextChange)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Random select 3 zones from zoneList: z1, z2 and z3")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)
        z1 = zone_selector.random_zone_selector()
        z2 = zone_selector.random_zone_selector()
        z3 = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIndividualRgbZones by [zoneID=z1, rgbValue=RED, 0xFF, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_id_0 = z1
        red_index_0 = 0xff
        green_index_0 = 0x0
        blue_index_0 = 0x0

        response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(
            test_case=self,
            rgb_zone_id_0=rgb_zone_id_0,
            red_index_0=red_index_0,
            green_index_0=green_index_0,
            blue_index_0=blue_index_0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response shall be [z1, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
            "rgb_zone_id_1": (checker.check_rgb_zone_id_1, HexList(0x0)),
            "rgb_zone_id_2": (checker.check_rgb_zone_id_2, HexList(0x0)),
            "rgb_zone_id_3": (checker.check_rgb_zone_id_3, HexList(0x0)),
        })
        checker.check_fields(self, response, self.feature_8081.set_individual_rgb_zones_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRangeRgbZones by [firstZoneID=z2, lastZoneID=z2, rgbValue=GREEN, 0xFF, ..,"
                                 "0]")
        # --------------------------------------------------------------------------------------------------------------
        rgb_first_zone_id_0 = z2
        rgb_last_zone_id_0 = z2
        red_index_0 = 0x0
        green_index_0 = 0xff
        blue_index_0 = 0x0
        rgb_first_zone_id_1 = 0xff
        rgb_last_zone_id_1 = 0xff
        red_index_1 = 0xff
        green_index_1 = 0xff
        blue_index_1 = 0xff
        rgb_first_zone_id_2 = 0xff
        rgb_last_zone_id_2 = 0xff
        red_index_2 = 0xff
        green_index_2 = 0xff
        blue_index_2 = 0xff

        response = PerKeyLightingTestUtils.HIDppHelper.set_range_rgb_zones(
            test_case=self,
            rgb_first_zone_id_0=rgb_first_zone_id_0,
            rgb_last_zone_id_0=rgb_last_zone_id_0,
            red_index_0=red_index_0,
            green_index_0=green_index_0,
            blue_index_0=blue_index_0,
            rgb_first_zone_id_1=rgb_first_zone_id_1,
            rgb_last_zone_id_1=rgb_last_zone_id_1,
            red_index_1=red_index_1,
            green_index_1=green_index_1,
            blue_index_1=blue_index_1,
            rgb_first_zone_id_2=rgb_first_zone_id_2,
            rgb_last_zone_id_2=rgb_last_zone_id_2,
            red_index_2=red_index_2,
            green_index_2=green_index_2,
            blue_index_2=blue_index_2
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response shall be [z2, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRangeRGBZonesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_first_zone_id_0": (checker.check_rgb_first_zone_id_0, rgb_first_zone_id_0),
            "rgb_first_zone_id_1": (checker.check_rgb_first_zone_id_1, rgb_first_zone_id_1),
            "rgb_first_zone_id_2": (checker.check_rgb_first_zone_id_2, rgb_first_zone_id_2),
        })
        checker.check_fields(self, response, self.feature_8081.set_range_rgb_zones_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRgbZonesSingleValue by [rgbValue = BLUE, zoneID=z3, 0xFF, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0x0
        rgb_zone_green = 0x0
        rgb_zone_blue = 0xff
        rgb_zone_id_0 = z3
        rgb_zone_id_1 = 0xff
        rgb_zone_id_2 = 0xff
        rgb_zone_id_3 = 0xff
        rgb_zone_id_4 = 0xf
        rgb_zone_id_5 = 0xff
        rgb_zone_id_6 = 0xff
        rgb_zone_id_7 = 0xff
        rgb_zone_id_8 = 0xff
        rgb_zone_id_9 = 0xff
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff

        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(
            test_case=self,
            rgb_zone_red=rgb_zone_red,
            rgb_zone_green=rgb_zone_green,
            rgb_zone_blue=rgb_zone_blue,
            rgb_zone_id_0=rgb_zone_id_0,
            rgb_zone_id_1=rgb_zone_id_1,
            rgb_zone_id_2=rgb_zone_id_2,
            rgb_zone_id_3=rgb_zone_id_3,
            rgb_zone_id_4=rgb_zone_id_4,
            rgb_zone_id_5=rgb_zone_id_5,
            rgb_zone_id_6=rgb_zone_id_6,
            rgb_zone_id_7=rgb_zone_id_7,
            rgb_zone_id_8=rgb_zone_id_8,
            rgb_zone_id_9=rgb_zone_id_9,
            rgb_zone_id_10=rgb_zone_id_10,
            rgb_zone_id_11=rgb_zone_id_11,
            rgb_zone_id_12=rgb_zone_id_12
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_SET_RGB_ZONES_SINGLE_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _FRAME_END)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self, 
                                                      persistence=0x0,
                                                      current_frame=0x0,
                                                      n_frames_till_next_change=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_RGB_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        # TODO: implement this check with kosmos

        self.testCaseChecked("FUN_8081_0010", _AUTHOR)
    # end def test_can_reflect_changes_after_multiple_requests
# end class PerKeyLightingFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
