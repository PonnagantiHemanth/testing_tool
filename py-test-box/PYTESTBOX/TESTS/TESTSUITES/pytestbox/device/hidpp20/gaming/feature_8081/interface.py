#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8081.interface
:brief: HID++ 2.0 ``PerKeyLighting`` interface test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.perkeylightingutils import PerKeyLightingTestUtils
from pytestbox.device.hidpp20.gaming.feature_8081.perkeylighting import PerKeyLightingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PerKeyLightingInterfaceTestCase(PerKeyLightingTestCase):
    """
    Validate ``PerKeyLighting`` interface test cases
    """

    @features("Feature8081")
    @level("Interface")
    def test_get_info(self):
        """
        Validate ``GetInfo`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetInfo request with all inputs as 0")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.get_info(
            test_case=self,
            type_of_info=0x0,
            param1=0x0
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.GetInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8081_index)),
        })
        checker.check_fields(self, response, self.feature_8081.get_info_response_cls, check_map)

        self.testCaseChecked("INT_8081_0001", _AUTHOR)
    # end def test_get_info

    @features("Feature8081")
    @level("Interface")
    def test_set_individual_rgb_zones(self):
        """
        Validate ``SetIndividualRGBZones`` interface
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = choice(supported_zones)
        red_index_0 = 0xff
        green_index_0 = 0x0
        blue_index_0 = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetIndividualRGBZones with RGBZoneID[0] = {rgb_zone_id_0}, RGB(255, 0, 0)")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(
            test_case=self,
            rgb_zone_id_0=rgb_zone_id_0,
            red_index_0=red_index_0,
            green_index_0=green_index_0,
            blue_index_0=blue_index_0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check SetIndividualRGBZonesResponse fields shall be ({rgb_zone_id_0}, ..., 0")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8081_index)),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0)
        })
        checker.check_fields(self, response, self.feature_8081.set_individual_rgb_zones_response_cls, check_map)

        self.testCaseChecked("INT_8081_0002", _AUTHOR)
    # end def test_set_individual_rgb_zones

    @features("Feature8081")
    @level("Interface")
    def test_set_consecutive_rgb_zones(self):
        """
        Validate ``SetConsecutiveRGBZones`` interface
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = choice(supported_zones)
        red_index_0 = 0xff
        green_index_0 = 0x0
        blue_index_0 = 0x0
        red_index_1 = 0xff
        green_index_1 = 0x0
        blue_index_1 = 0x0
        red_index_2 = 0xff
        green_index_2 = 0x0
        blue_index_2 = 0x0
        red_index_3 = 0xff
        green_index_3 = 0x0
        blue_index_3 = 0x0
        red_index_4 = 0xff
        green_index_4 = 0x0
        blue_index_4 = 0x0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self,
            f"Send SetConsecutiveRGBZones request with RGBZoneID[0] = {rgb_zone_id_0} and all RGB values[255, 0, 0]")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones(
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
            blue_index_4=blue_index_4
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check SetConsecutiveRGBZonesResponse fields shall be ({rgb_zone_id_0}, .., 0)")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8081_index)),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(self, response, self.feature_8081.set_consecutive_rgb_zones_response_cls, check_map)

        self.testCaseChecked("INT_8081_0003", _AUTHOR)
    # end def test_set_consecutive_rgb_zones

    @features("Feature8081")
    @level("Interface")
    def test_set_consecutive_rgb_zones_delta_compression_5bit(self):
        """
        Validate ``SetConsecutiveRGBZonesDeltaCompression5bit`` interface
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = choice(supported_zones)
        red_index_0 = 0
        green_index_0 = 0
        blue_index_0 = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetConsecutiveRGBZonesDeltaCompression5bit with RGBZoneID[0] = {rgb_zone_id_0} "
                                 f"and all RGB value to (0, 0, 0)")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones_delta_compression_5bit(
            test_case=self,
            rgb_zone_id_0=rgb_zone_id_0,
            red_index_0=red_index_0,
            green_index_0=green_index_0,
            blue_index_0=blue_index_0,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetConsecutiveRGBZonesDeltaCompression5bitResponse fields "
                                  f"shall be ({rgb_zone_id_0}, 0, 0, ..)")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression5bitResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8081_index)),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(
            self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_response_cls,
            check_map)

        self.testCaseChecked("INT_8081_0004", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_delta_compression_5bit

    @features("Feature8081")
    @level("Interface")
    def test_set_consecutive_rgb_zones_delta_compression_4bit(self):
        """
        Validate ``SetConsecutiveRGBZonesDeltaCompression4bit`` interface
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = choice(supported_zones)
        red_index_0 = 0
        green_index_0 = 0
        blue_index_0 = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send SetConsecutiveRGBZonesDeltaCompression4bit request with RGBZoneID[0] = {rgb_zone_id_0}")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_consecutive_rgb_zones_delta_compression_4bit(
            test_case=self,
            rgb_zone_id_0=rgb_zone_id_0,
            red_index_0=red_index_0,
            green_index_0=green_index_0,
            blue_index_0=blue_index_0,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetConsecutiveRGBZonesDeltaCompression4bitResponse fields "
                                  f"shall be ({rgb_zone_id_0}, 0, 0, ..)")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression4bitResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8081_index)),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(
            self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_response_cls,
            check_map)

        self.testCaseChecked("INT_8081_0005", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_delta_compression_4bit

    @features("Feature8081")
    @level("Interface")
    def test_set_range_rgb_zones(self):
        """
        Validate ``SetRangeRGBZones`` interface
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_first_zone_id_0 = supported_zones[0]
        rgb_last_zone_id_0 = supported_zones[-1]
        red_index_0 = 0xff
        green_index_0 = 0x0
        blue_index_0 = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRangeRGBZones request with RGB")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_range_rgb_zones(
            test_case=self,
            rgb_first_zone_id_0=rgb_first_zone_id_0,
            rgb_last_zone_id_0=rgb_last_zone_id_0,
            red_index_0=red_index_0,
            green_index_0=green_index_0,
            blue_index_0=blue_index_0,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetRangeRGBZonesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRangeRGBZonesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8081_index)),
            "rgb_first_zone_id_0": (checker.check_rgb_first_zone_id_0, HexList(rgb_first_zone_id_0)),
            "rgb_first_zone_id_1": (checker.check_rgb_first_zone_id_1, HexList(0x0)),
            "rgb_first_zone_id_2": (checker.check_rgb_first_zone_id_2, HexList(0x0)),
        })
        checker.check_fields(self, response, self.feature_8081.set_range_rgb_zones_response_cls, check_map)

        self.testCaseChecked("INT_8081_0006", _AUTHOR)
    # end def test_set_range_rgb_zones

    @features("Feature8081")
    @level("Interface")
    def test_set_rgb_zones_single_value(self):
        """
        Validate ``SetRGBZonesSingleValue`` interface
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_red = 0xff
        rgb_zone_green = 0x0
        rgb_zone_blue = 0x0
        rgb_zone_id_0 = choice(supported_zones)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send SetRGBZonesSingleValue request with RGBZoneID[0] = {rgb_zone_id_0}, RGB[255, 0, 0]")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(
            test_case=self,
            rgb_zone_red=rgb_zone_red,
            rgb_zone_green=rgb_zone_green,
            rgb_zone_blue=rgb_zone_blue,
            rgb_zone_id_0=rgb_zone_id_0,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check SetRGBZonesSingleValueResponse fields shall be (255, 0, 0, {rgb_zone_id_0}")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8081_index)),
            "rgb_zone_red": (checker.check_rgb_zone_red, HexList(rgb_zone_red)),
            "rgb_zone_green": (checker.check_rgb_zone_green, HexList(rgb_zone_green)),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls, check_map)

        self.testCaseChecked("INT_8081_0007", _AUTHOR)
    # end def test_set_rgb_zones_single_value

    @features("Feature8081")
    @level("Interface")
    def test_frame_end(self):
        """
        Validate ``FrameEnd`` interface
        """
        persistence = 0x0
        current_frame = 0
        n_frames_till_next_change = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send FrameEnd request with all inputs 0")
        # --------------------------------------------------------------------------------------------------------------
        response = PerKeyLightingTestUtils.HIDppHelper.frame_end(test_case=self, persistence=persistence,
                                                                 current_frame=current_frame,
                                                                 n_frames_till_next_change=n_frames_till_next_change)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check FrameEndResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8081_index))
        }
        checker.check_fields(self, response, self.feature_8081.frame_end_response_cls, check_map)

        self.testCaseChecked("INT_8081_0008", _AUTHOR)
    # end def test_frame_end
# end class PerKeyLightingInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
