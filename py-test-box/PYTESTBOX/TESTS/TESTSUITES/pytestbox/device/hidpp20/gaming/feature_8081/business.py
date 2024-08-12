#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8081.business
:brief: HID++ 2.0 ``PerKeyLighting`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.perkeylightingutils import PerKeyLightingTestUtils
from pytestbox.device.hidpp20.gaming.feature_8081.perkeylighting import PerKeyLightingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_COLLECT_VALID_ZONES = "Collect all of valid zones into zoneList by getInfo"
_SEND_FRAME_END = "Send frameEnd w/ all inputs = 0"
_LOOP_END = "End Test Loop"
_CHECK_RGB_VALUE = "TODO: For each zone, check the RGB value by LED Indicator/LED Driver IC shall be same as inputs"
_GET_INFO_LOOP = "Test Loop over all param1 values"
_CHECK_GET_INFO = "Check GetInfoResponse fields"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PerKeyLightingBusinessTestCase(PerKeyLightingTestCase):
    """
    Validate ``PerKeyLighting`` business test cases
    """

    @features("Feature8081")
    @level("Business")
    def test_check_can_set_zone_color_pair(self):
        """
        Check can set 1..4 {zone, color} pairs by setIndividualRgbZones. Shall random select zone and color for each
        pair.(Dependency: LED indicator or LED Driver IC)
        
        [1] setIndividualRgbZones(rgbIndividualZones, rgbValues) -> rgbIndividualZones
        """
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)
        color_picker = PerKeyLightingTestUtils.HIDppHelper.random_color_picker
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over n in range[1..4]")
        # --------------------------------------------------------------------------------------------------------------
        zone_list = [0] * 4
        color_list = [[0, 0, 0]] * 4
        for n in range(4):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Random select n {zone, color} pairs from zoneList and {RED, YELLOW, GREEN, CYAN,"
                                     "BLUE, MAGENTA} to settingList")
            # ----------------------------------------------------------------------------------------------------------
            zone_list[n] = zone_selector.random_zone_selector()
            color_list[n] = color_picker()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetIndividualRGBZones request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(test_case=self,
                                                                                    rgb_zone_id_0=zone_list[0],
                                                                                    red_index_0=color_list[0][0],
                                                                                    green_index_0=color_list[0][1],
                                                                                    blue_index_0=color_list[0][2],
                                                                                    rgb_zone_id_1=zone_list[1],
                                                                                    red_index_1=color_list[1][0],
                                                                                    green_index_1=color_list[1][1],
                                                                                    blue_index_1=color_list[1][2],
                                                                                    rgb_zone_id_2=zone_list[2],
                                                                                    red_index_2=color_list[2][0],
                                                                                    green_index_2=color_list[2][1],
                                                                                    blue_index_2=color_list[2][2],
                                                                                    rgb_zone_id_3=zone_list[3],
                                                                                    red_index_3=color_list[3][0],
                                                                                    green_index_3=color_list[3][1],
                                                                                    blue_index_3=color_list[3][2])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneIDs shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, zone_list[0]),
                "rgb_zone_id_1": (checker.check_rgb_zone_id_1, zone_list[1]),
                "rgb_zone_id_2": (checker.check_rgb_zone_id_2, zone_list[2]),
                "rgb_zone_id_3": (checker.check_rgb_zone_id_3, zone_list[3]),
            })
            checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
            checker.check_fields(test_case=self,
                                 message=response,
                                 expected_cls=self.feature_8081.set_individual_rgb_zones_response_cls,
                                 check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_FRAME_END)
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

        self.testCaseChecked("BUS_8081_0001", _AUTHOR)
    # end def test_check_can_set_zone_color_pair

    @features("Feature8081")
    @level('Business', 'SmokeTests')
    def test_apply_several_rgb_values(self):
        """
        Random select 4 zones and apply several RGB values by bitwise selection to verify RGB output result shall be
        same as input. And mandatory test color (0,0,0) and (255,255,255). (LED indicator or LED Driver IC)
        
        [1] setIndividualRgbZones(rgbIndividualZones, rgbValues) -> rgbIndividualZones
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select 4 zones (z1, z2, z3, z4) from zoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)
        z1 = zone_selector.random_zone_selector()
        z2 = zone_selector.random_zone_selector()
        z3 = zone_selector.random_zone_selector()
        z4 = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over rgb in several interesting RGB values shall include (0, 0, 0) "
                                 "and (255, 255, 255))")
        # --------------------------------------------------------------------------------------------------------------
        rgb_values = ((0x0, 0x0, 0x0), (0xff, 0x0, 0x0), (0x0, 0xff, 0x0), (0x0, 0x0, 0xff),
                      (0xff, 0xff, 0x0), (0x0, 0xff, 0xff), (0xff, 0xff, 0xff))
        rgb_zone_id_0, rgb_zone_id_1, rgb_zone_id_2, rgb_zone_id_3 = z1, z2, z3, z4

        for rgb_value in rgb_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set {z1, rgb, z2, rgb, z3, rgb, z4, rgb} to settingList")
            # ----------------------------------------------------------------------------------------------------------
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, \
                red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3 = rgb_value * 4

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetIndividualRGBZones request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(test_case=self,
                                                                                    rgb_zone_id_0=rgb_zone_id_0,
                                                                                    red_index_0=red_index_0,
                                                                                    green_index_0=green_index_0,
                                                                                    blue_index_0=blue_index_0,
                                                                                    rgb_zone_id_1=rgb_zone_id_1,
                                                                                    red_index_1=red_index_1,
                                                                                    green_index_1=green_index_1,
                                                                                    blue_index_1=blue_index_1,
                                                                                    rgb_zone_id_2=rgb_zone_id_2,
                                                                                    red_index_2=red_index_2,
                                                                                    green_index_2=green_index_2,
                                                                                    blue_index_2=blue_index_2,
                                                                                    rgb_zone_id_3=rgb_zone_id_3,
                                                                                    red_index_3=red_index_3,
                                                                                    green_index_3=green_index_3,
                                                                                    blue_index_3=blue_index_3)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetIndividualRGBZonesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
                "rgb_zone_id_1": (checker.check_rgb_zone_id_1, rgb_zone_id_1),
                "rgb_zone_id_2": (checker.check_rgb_zone_id_2, rgb_zone_id_2),
                "rgb_zone_id_3": (checker.check_rgb_zone_id_3, rgb_zone_id_3),
            })
            checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
            checker.check_fields(test_case=self,
                                 message=response,
                                 expected_cls=self.feature_8081.set_individual_rgb_zones_response_cls,
                                 check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_FRAME_END)
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

        self.testCaseChecked("BUS_8081_0002", _AUTHOR)
    # end def test_apply_several_rgb_values

    @features("Feature8081")
    @level("Business")
    def test_set_consecutive_rgb_values_random_zone(self):
        """
        Random select a starting zone and set 5 colors {RED, YELLOW, GREEN, CYAN, BLUE}. (LED indicator or LED Driver
        IC)
        
        [2] setConsecutiveRgbZones(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select a zone z from zoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)
        z = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set {z, RED, YELLOW, GREEN, CYAN, BLUE} to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_id_0 = z
        red_index_0, green_index_0, blue_index_0 = 0xff, 0x0, 0x0
        red_index_1, green_index_1, blue_index_1 = 0xff, 0xff, 0x0
        red_index_2, green_index_2, blue_index_2, = 0x0, 0xff, 0x0
        red_index_3, green_index_3, blue_index_3, = 0x0, 0xff, 0xff
        red_index_4, green_index_4, blue_index_4 = 0x0, 0x0, 0xff

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setConsecutiveRgbZones")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones(test_case=self,
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
                                                                                 blue_index_4=blue_index_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response zoneID shall be same as inputs")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_8081.set_consecutive_rgb_zones_response_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_FRAME_END)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self,
                                                      persistence=0x0,
                                                      current_frame=0x0,
                                                      n_frames_till_next_change=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_RGB_VALUE)
        # --------------------------------------------------------------------------------------------------------------
        # TODO: implement this check with kosmos
        self.testCaseChecked("BUS_8081_0003", _AUTHOR)
    # end def test_set_consecutive_rgb_values_random_zone

    @features("Feature8081")
    @level("Business")
    def test_set_all_5bit_delta_compression_values(self):
        """
        Random select a starting zone and set the 8 consecutive zones to color(128, 128, 128). Apply delta from -16 to
        +15 and check the result shall be same as expected. (LED indicator or LED Driver IC)
        
        [3] setConsecutiveRgbZonesDeltaCompression5bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select 8 valid consecutive zones from zoneList and the smallest one is the"
                                 "starting_zone")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_id_0, rgb_zone_id_1, rgb_zone_id_2, rgb_zone_id_3, rgb_zone_id_4, rgb_zone_id_5, rgb_zone_id_6, \
            rgb_zone_id_7 = PerKeyLightingTestUtils.HIDppHelper.consecutive_zone_selector(
                zone_list=self.supported_zone_list, consecutive_zones=8)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set [128, 128, 128, zoneID[0], .., zoneID[7], 0xFF] to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0x80
        rgb_zone_green = 0x80
        rgb_zone_blue = 0x80
        rgb_zone_id_8 = 0xff
        rgb_zone_id_9 = 0xff
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRGBZonesSingleValue request")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(test_case=self,
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
                                                                                  rgb_zone_id_12=rgb_zone_id_12,
                                                                                  rgb_zone_red=rgb_zone_red,
                                                                                  rgb_zone_green=rgb_zone_green,
                                                                                  rgb_zone_blue=rgb_zone_blue)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response shall be [128, 128, 128, starting_zone, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_8081.set_rgb_zones_single_value_response_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over delta_rgb in range[-16..15]")
        # --------------------------------------------------------------------------------------------------------------
        positive_delta = list(range(0, 16))
        negative_delta = list(range(16, 32))
        delta_values_5_bit = negative_delta + positive_delta

        for i in delta_values_5_bit:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set {starting_zone, rgbValues=delta_rgb} to settingList")
            # ----------------------------------------------------------------------------------------------------------
            starting_zone = rgb_zone_id_0
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, \
                red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3, \
                red_index_4, green_index_4, blue_index_4, red_index_5, green_index_5, blue_index_5, \
                red_index_6, green_index_6, blue_index_6, red_index_7, green_index_7, blue_index_7 = [i] * 24

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConsecutiveRGBZonesDeltaCompression5bit request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones_delta_compression_5bit(
                test_case=self,
                rgb_zone_id_0=starting_zone,
                red_index_0=red_index_0, green_index_0=green_index_0, blue_index_0=blue_index_0,
                red_index_1=red_index_1, green_index_1=green_index_1, blue_index_1=blue_index_1,
                red_index_2=red_index_2, green_index_2=green_index_2, blue_index_2=blue_index_2,
                red_index_3=red_index_3, green_index_3=green_index_3, blue_index_3=blue_index_3,
                red_index_4=red_index_4, green_index_4=green_index_4, blue_index_4=blue_index_4,
                red_index_5=red_index_5, green_index_5=green_index_5, blue_index_5=blue_index_5,
                red_index_6=red_index_6, green_index_6=green_index_6, blue_index_6=blue_index_6,
                red_index_7=red_index_7, green_index_7=green_index_7, blue_index_7=blue_index_7
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetConsecutiveRGBZonesDeltaCompression5bitResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression5bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, starting_zone),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_FRAME_END)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self,
                                                          persistence=0x0,
                                                          current_frame=0x0,
                                                          n_frames_till_next_change=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_RGB_VALUE)
            # ----------------------------------------------------------------------------------------------------------
            # TODO implement this check using kosmos
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8081_0004", _AUTHOR)
    # end def test_set_all_5bit_delta_compression_values

    @features("Feature8081")
    @level("Business")
    def test_alternate_min_and_max_values_5bit_delta(self):
        """
        Random select a starting zone and set the 8 consecutive zones to color(255, 255, 255). Apply the delta 1 and
        check the result shall be color(0, 0, 0). Apply the delta -1 and check the result shall be color(255, 255,
        255). (LED indicator or LED Driver IC)
        
        [3] setConsecutiveRgbZonesDeltaCompression5bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select 8 valid consecutive zones from zoneList and the smallest one is the"
                                 "starting_zone")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_id_0, rgb_zone_id_1, rgb_zone_id_2, rgb_zone_id_3, rgb_zone_id_4, rgb_zone_id_5, rgb_zone_id_6, \
            rgb_zone_id_7 = PerKeyLightingTestUtils.HIDppHelper.consecutive_zone_selector(zone_list=
                                                                                          self.supported_zone_list,
                                                                                          consecutive_zones=8)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set [255, 255, 255, zoneID[0], .., zoneID[7], 0xFF] to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0xff
        rgb_zone_green = 0xff
        rgb_zone_blue = 0xff
        rgb_zone_id_8 = 0xff
        rgb_zone_id_9 = 0xff
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRGBZonesSingleValue request")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(test_case=self,
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
                                                                                  rgb_zone_id_12=rgb_zone_id_12,
                                                                                  rgb_zone_red=rgb_zone_red,
                                                                                  rgb_zone_green=rgb_zone_green,
                                                                                  rgb_zone_blue=rgb_zone_blue)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response shall be [255, 255, 255, starting_zone, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_8081.set_rgb_zones_single_value_response_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over delta_rgb in [-1, 1]")
        # --------------------------------------------------------------------------------------------------------------
        for i in [31, 1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set {starting_zone, rgbValues=delta_rgb} to settingList")
            # ----------------------------------------------------------------------------------------------------------
            starting_zone = rgb_zone_id_0
            red_index_0, green_index_0, blue_index_0, red_index_1, green_index_1, blue_index_1, \
                red_index_2, green_index_2, blue_index_2, red_index_3, green_index_3, blue_index_3, \
                red_index_4, green_index_4, blue_index_4, red_index_5, green_index_5, blue_index_5, \
                red_index_6, green_index_6, blue_index_6, red_index_7, green_index_7, blue_index_7 = [i] * 24

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Send SetConsecutiveRGBZonesDeltaCompression5bit request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones_delta_compression_5bit(
                test_case=self,
                rgb_zone_id_0=starting_zone,
                red_index_0=red_index_0, green_index_0=green_index_0, blue_index_0=blue_index_0,
                red_index_1=red_index_1, green_index_1=green_index_1, blue_index_1=blue_index_1,
                red_index_2=red_index_2, green_index_2=green_index_2, blue_index_2=blue_index_2,
                red_index_3=red_index_3, green_index_3=green_index_3, blue_index_3=blue_index_3,
                red_index_4=red_index_4, green_index_4=green_index_4, blue_index_4=blue_index_4,
                red_index_5=red_index_5, green_index_5=green_index_5, blue_index_5=blue_index_5,
                red_index_6=red_index_6, green_index_6=green_index_6, blue_index_6=blue_index_6,
                red_index_7=red_index_7, green_index_7=green_index_7, blue_index_7=blue_index_7)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneID shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression5bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, starting_zone),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_FRAME_END)
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

        self.testCaseChecked("BUS_8081_0005", _AUTHOR)
    # end def test_alternate_min_and_max_values_5bit_delta

    @features("Feature8081")
    @level("Business")
    def test_set_all_4bit_delta_compression_values(self):
        """
        Random select a starting zone and set the 10 consecutive zones to color(128, 128, 128). Apply delta from -8 to
        +7 and check the result shall be same as expected. (LED indicator or LED Driver IC)
        
        [4] setConsecutiveRgbZonesDeltaCompression4bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select 10 valid consecutive zones from zoneList and the smallest one is the"
                                 "starting_zone")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_id_0, rgb_zone_id_1, rgb_zone_id_2, rgb_zone_id_3, rgb_zone_id_4, rgb_zone_id_5, rgb_zone_id_6, \
            rgb_zone_id_7, rgb_zone_id_8, rgb_zone_id_9 = PerKeyLightingTestUtils.HIDppHelper.consecutive_zone_selector(
                zone_list=self.supported_zone_list, consecutive_zones=10)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set [128, 128, 128, zoneID[0], .., zoneID[9], 0xFF] to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0x80
        rgb_zone_green = 0x80
        rgb_zone_blue = 0x80
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRGBZonesSingleValue request")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(test_case=self,
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
                                                                                  rgb_zone_id_12=rgb_zone_id_12,
                                                                                  rgb_zone_red=rgb_zone_red,
                                                                                  rgb_zone_green=rgb_zone_green,
                                                                                  rgb_zone_blue=rgb_zone_blue)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetRGBZonesSingleValueResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_8081.set_rgb_zones_single_value_response_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over delta_rgb in range[-8..7]")
        # --------------------------------------------------------------------------------------------------------------
        negative_delta_values = list(range(8, 16))
        positive_dela_values = list(range(0, 8))
        delta_values = negative_delta_values + positive_dela_values

        for i in delta_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set {starting_zone, rgbValues=delta_rgb} to settingList")
            # ----------------------------------------------------------------------------------------------------------
            starting_zone = rgb_zone_id_0
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
                blue_index_9=blue_index_9)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneID shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression4bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, starting_zone),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_FRAME_END)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self,
                                                          persistence=0x0,
                                                          current_frame=0x0,
                                                          n_frames_till_next_change=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_RGB_VALUE)
            # ----------------------------------------------------------------------------------------------------------
            # TODO implement this check using kosmos
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8081_0006", _AUTHOR)
    # end def test_set_all_4bit_delta_compression_values

    @features("Feature8081")
    @level("Business")
    def test_alternate_min_max_values_4bit_delta(self):
        """
        Random select a starting zone and set the 10 consecutive zones to color(255, 255, 255). Apply the delta 1 and
        check the result shall be color(0, 0, 0). Apply the delta -1 and check the result shall be color(255, 255,
        255). (LED indicator or LED Driver IC)
        
        [4] setConsecutiveRgbZonesDeltaCompression4bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select 10 valid consecutive zones from zoneList and the smallest one is the"
                                 "starting_zone")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_id_0, rgb_zone_id_1, rgb_zone_id_2, rgb_zone_id_3, rgb_zone_id_4, rgb_zone_id_5, rgb_zone_id_6, \
            rgb_zone_id_7, rgb_zone_id_8, rgb_zone_id_9 = PerKeyLightingTestUtils.HIDppHelper.consecutive_zone_selector(
                zone_list=self.supported_zone_list, consecutive_zones=10)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set [255, 255, 255, zoneID[0], .., zoneID[9], 0xFF] to settingList")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0xff
        rgb_zone_green = 0xff
        rgb_zone_blue = 0xff
        rgb_zone_id_10 = 0xff
        rgb_zone_id_11 = 0xff
        rgb_zone_id_12 = 0xff

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRGBZonesSingleValue request")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(test_case=self,
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
                                                                                  rgb_zone_id_12=rgb_zone_id_12,
                                                                                  rgb_zone_red=rgb_zone_red,
                                                                                  rgb_zone_green=rgb_zone_green,
                                                                                  rgb_zone_blue=rgb_zone_blue)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response shall be [255, 255, 255, starting_zone, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_8081.set_rgb_zones_single_value_response_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over delta_rgb in [1, -1]")
        # --------------------------------------------------------------------------------------------------------------
        for i in [15, 1]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set {starting_zone, rgbValues=delta_rgb} to settingList")
            # ----------------------------------------------------------------------------------------------------------
            starting_zone = rgb_zone_id_0
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
                blue_index_9=blue_index_9)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneID shall be same as inputs")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression4bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, starting_zone),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_FRAME_END)
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

        self.testCaseChecked("BUS_8081_0007", _AUTHOR)
    # end def test_alternate_min_max_values_4bit_delta

    @features("Feature8081")
    @level("Business")
    def test_check_can_set_ranges(self):
        """
        Divide first consecutive zoneIDs into 3 groups and random selects a color from {RED, YELLOW, GREEN, CYAN,
        BLUE, MAGENTA} to each group. Check can set 1, 2 and 3 ranges at a time. (LED indicator or LED Driver IC)
        
        [5] setRangeRgbZones(rgbFirstZoneIDs, rgbLastZoneIDs, rgbValues) -> rgbFirstZoneIDs
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Divides first consecutive zoneIDs from zoneList into 3 groups, groupList = [g1 ,g2,"
                                 "g3]")
        # --------------------------------------------------------------------------------------------------------------
        n = len(self.supported_zone_list) // 3
        group_1, group_2, group_3 = self.supported_zone_list[:n], self.supported_zone_list[n:2 * n], \
                                    self.supported_zone_list[2 * n:]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select a color rgbValue from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA} to"
                                 "each group, gn={firstZoneID[n], lastZoneID[n], rgbValue[n]}")
        # --------------------------------------------------------------------------------------------------------------
        color = PerKeyLightingTestUtils.HIDppHelper.random_color_picker
        red_index_0, green_index_0, blue_index_0 = color()
        red_index_1, green_index_1, blue_index_1 = color()
        red_index_2, green_index_2, blue_index_2 = color()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over n in range[1..3]")
        # --------------------------------------------------------------------------------------------------------------
        for n in range(1, 4):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "From groupList to settingsList, select n zones and append 0xff in the end of "
                                     "group settings")
            # ----------------------------------------------------------------------------------------------------------
            rgb_first_zone_id_0 = 0xff
            rgb_last_zone_id_0 = 0xff
            rgb_first_zone_id_1 = 0xff
            rgb_last_zone_id_1 = 0xff
            rgb_first_zone_id_2 = 0xff
            rgb_last_zone_id_2 = 0xff

            if n == 1:
                rgb_first_zone_id_0 = group_1[0]
                rgb_last_zone_id_0 = group_1[-1]
            elif n == 2:
                rgb_first_zone_id_0 = group_1[0]
                rgb_last_zone_id_0 = group_1[-1]
                rgb_first_zone_id_1 = group_2[0]
                rgb_last_zone_id_1 = group_2[-1]
            elif n == 3:
                rgb_first_zone_id_0 = group_1[0]
                rgb_last_zone_id_0 = group_1[-1]
                rgb_first_zone_id_1 = group_2[0]
                rgb_last_zone_id_1 = group_2[-1]
                rgb_first_zone_id_2 = group_3[0]
                rgb_last_zone_id_2 = group_3[-1]
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetRangeRGBZones request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_range_rgb_zones(test_case=self,
                                                                               rgb_first_zone_id_0=rgb_first_zone_id_0,
                                                                               red_index_0=red_index_0,
                                                                               green_index_0=green_index_0,
                                                                               blue_index_0=blue_index_0,
                                                                               rgb_last_zone_id_0=rgb_last_zone_id_0,
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

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the response zoneIDs shall be same as [firstZoneID[0], firstZoneID[1](if"
                                      "n > 1), firstZoneID[2] (if n > 2), 0, .., 0]")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetRangeRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_first_zone_id_0": (checker.check_rgb_first_zone_id_0, rgb_first_zone_id_0),
                "rgb_first_zone_id_1": (checker.check_rgb_first_zone_id_1, rgb_first_zone_id_1),
                "rgb_first_zone_id_2": (checker.check_rgb_first_zone_id_2, rgb_first_zone_id_2),
            })
            checker.check_fields(self, response, self.feature_8081.set_range_rgb_zones_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_FRAME_END)
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

        self.testCaseChecked("BUS_8081_0008", _AUTHOR)
    # end def test_can_check_ranges

    @features("Feature8081")
    @level("Business")
    def test_set_random_color_random_zone(self):
        """
        Random select a color from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA}. Check can set the color to 1..13 zones.
        Shall random select zones at each check. (LED indicator or LED Driver IC)
        
        [6] setRgbZonesSingleValue(rgbZoneR, rgbZoneG, rgbZoneB, rgbZoneID[0], .., rgbZoneID[12]) -> rgbZoneR,
        rgbZoneG, rgbZoneB, rgbZoneID[0]
        """
        zone_list = [0] * 13
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select a color rgbValue from {RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA}")
        # --------------------------------------------------------------------------------------------------------------
        color = PerKeyLightingTestUtils.HIDppHelper.random_color_picker
        rgb_zone_red, rgb_zone_green, rgb_zone_blue = color()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over n in range[1..13]")
        # --------------------------------------------------------------------------------------------------------------
        for i in range(13):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Random select n valid zones from zoneList and set [rgbValue,"
                                     "zoneID[0]..zoneID[n-1]] to settingList")
            # ----------------------------------------------------------------------------------------------------------
            zone_list[i] = zone_selector.random_zone_selector()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetRGBZonesSingleValue request")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(test_case=self,
                                                                                      rgb_zone_id_0=zone_list[0],
                                                                                      rgb_zone_id_1=zone_list[1],
                                                                                      rgb_zone_id_2=zone_list[2],
                                                                                      rgb_zone_id_3=zone_list[3],
                                                                                      rgb_zone_id_4=zone_list[4],
                                                                                      rgb_zone_id_5=zone_list[5],
                                                                                      rgb_zone_id_6=zone_list[6],
                                                                                      rgb_zone_id_7=zone_list[7],
                                                                                      rgb_zone_id_8=zone_list[8],
                                                                                      rgb_zone_id_9=zone_list[9],
                                                                                      rgb_zone_id_10=zone_list[10],
                                                                                      rgb_zone_id_11=zone_list[11],
                                                                                      rgb_zone_id_12=zone_list[12],
                                                                                      rgb_zone_red=rgb_zone_red,
                                                                                      rgb_zone_green=rgb_zone_green,
                                                                                      rgb_zone_blue=rgb_zone_blue)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRGBZonesSingleValueResponse response")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
                "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
                "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, zone_list[0]),
            })
            checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls,
                                 check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _SEND_FRAME_END)
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

        self.testCaseChecked("BUS_8081_0009", _AUTHOR)
    # end def test_set_random_color_random_zone
# end class PerKeyLightingBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
