#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8081.errorhandling
:brief: HID++ 2.0 ``PerKeyLighting`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/11/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.perkeylightingutils import PerKeyLightingTestUtils
from pytestbox.device.hidpp20.gaming.feature_8081.perkeylighting import PerKeyLightingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"
_INVALID_ARGUMENT = "Check can get the Invalid_Argument(2) error return"
_LOOP_OVER_UNSUPPORTED_ZONES = "Test Loop over z in unsupportedZoneList (several unsupported values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PerKeyLightingErrorHandlingTestCase(PerKeyLightingTestCase):
    """
    Validate ``PerKeyLighting`` errorhandling test cases
    """

    @features("Feature8081")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_8081.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.get_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                type_of_info=0x0,
                param1=0x0)
            report.function_index = function_index

            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature8081")
    @level("ErrorHandling")
    def test_invalid_param1(self):
        """
        Check the error handling by several invalid inputs of param1
        
        [0] getInfo(typeOfInfo, param1) -> lightingInfo
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over param1 in error range (several invalid values)")
        # --------------------------------------------------------------------------------------------------------------
        for param1 in [0x03, 0x04, 0x05]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetInfo w/ typeOfInfo = 0 and invalid param1")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.get_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                type_of_info=0x0,
                param1=HexList(param1))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _INVALID_ARGUMENT)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                       report=report,
                                                                       error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0002", _AUTHOR)
    # end def test_invalid_param1

    @features("Feature8081")
    @level("ErrorHandling")
    def test_set_individual_rgb_zones_send_unsupported_zone_id(self):
        """
        Check can get Invalid_Argument(2) error return by sent unsupported zoneIDs.
        
        [1] setIndividualRgbZones(rgbIndividualZones, rgbValues) -> rgbIndividualZones
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select 2 zones, z1, z2 from zoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)
        z1 = zone_selector.random_zone_selector()
        z2 = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_UNSUPPORTED_ZONES)
        # --------------------------------------------------------------------------------------------------------------
        for z in [self.unsupported_zone_list[0], self.unsupported_zone_list[-1],
                  self.unsupported_zone_list[len(self.unsupported_zone_list) // 2]]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setIndividualRgbZones by [z1, rgbValue=RED, z2, rgbValue=RED, z,"
                                     "rgbValue=RED, 0]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_individual_rgb_zones_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                rgb_zone_id_0=z1,
                red_index_0=0xff,
                green_index_0=0x0,
                blue_index_0=0x0,
                rgb_zone_id_1=z2,
                red_index_1=0xff,
                green_index_1=0x0,
                blue_index_1=0x0,
                rgb_zone_id_2=z,
                red_index_2=0xff,
                green_index_2=0x0,
                blue_index_2=0x0,
                rgb_zone_id_3=0x0,
                red_index_3=0x0,
                green_index_3=0x0,
                blue_index_3=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _INVALID_ARGUMENT)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                       report=report,
                                                                       error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0003", _AUTHOR)
    # end def test_set_individual_rgb_zones_send_unsupported_zone_id

    @features("Feature8081")
    @level("ErrorHandling")
    def test_set_consecutive_rgb_zones_unsupported_zone_id(self):
        """
        Check can get Invalid_Argument(2) error return by sent unsupported zoneIDs.
        
        [2] setConsecutiveRgbZones(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_UNSUPPORTED_ZONES)
        # --------------------------------------------------------------------------------------------------------------
        for z in [self.unsupported_zone_list[0], self.unsupported_zone_list[-1],
                  self.unsupported_zone_list[len(self.unsupported_zone_list) // 2]]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setConsecutiveRgbZones by [z, rgbValue[0]=RED, rgbValue[1]=RED,"
                                     "rgbValue[2]=RED, rgbValue[3]=RED, rgbValue[4]=RED]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_consecutive_rgb_zones_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                rgb_zone_id_0=z,
                red_index_0=0xff,
                green_index_0=0x0,
                blue_index_0=0x0,
                red_index_1=0xff,
                green_index_1=0x0,
                blue_index_1=0x0,
                red_index_2=0xff,
                green_index_2=0x0,
                blue_index_2=0x0,
                red_index_3=0xff,
                green_index_3=0x0,
                blue_index_3=0x0,
                red_index_4=0xff,
                green_index_4=0x0,
                blue_index_4=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _INVALID_ARGUMENT)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                       report=report,
                                                                       error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0004", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_unsupported_zone_id

    @features("Feature8081")
    @level("ErrorHandling")
    def test_set_consecutive_rgb_zones_delta_compression_5bit_unsupported_zone_id(self):
        """
        Check can get Invalid_Argument(2) error return by sent unsupported zoneIDs.
        
        [3] setConsecutiveRgbZonesDeltaCompression5bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_UNSUPPORTED_ZONES)
        # --------------------------------------------------------------------------------------------------------------
        for z in [self.unsupported_zone_list[0], self.unsupported_zone_list[-1],
                  self.unsupported_zone_list[len(self.unsupported_zone_list) // 2]]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setConsecutiveRgbZonesDeltaCompression5bit by [z, 0, .., 0]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                rgb_zone_id_0=HexList(z),
                red_index_0=0x0,
                green_index_0=0x0,
                blue_index_0=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _INVALID_ARGUMENT)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self, 
                                                                       report=report,
                                                                       error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0005", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_delta_compression_5bit_unsupported_zone_id

    @features("Feature8081")
    @level("ErrorHandling")
    def test_set_consecutive_rgb_zones_deta_compression_4bit_unsupported_zone_id(self):
        """
        Check can get Invalid_Argument(2) error return by sent unsupported zoneIDs.
        
        [4] setConsecutiveRgbZonesDeltaCompression4bit(rgbZoneID[0], rgbValues) -> rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_OVER_UNSUPPORTED_ZONES)
        # --------------------------------------------------------------------------------------------------------------
        for z in [self.unsupported_zone_list[0], self.unsupported_zone_list[-1],
                  self.unsupported_zone_list[len(self.unsupported_zone_list)//2]]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setConsecutiveRgbZonesDeltaCompression4bit by [z, 0, .., 0]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                rgb_zone_id_0=HexList(z),
                red_index_0=0,
                green_index_0=0,
                blue_index_0=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _INVALID_ARGUMENT)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                       report=report,
                                                                       error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0006", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_deta_compression_4bit_unsupported_zone_id

    @features("Feature8081")
    @features("Feature8081v1")
    @level("ErrorHandling")
    def test_set_rgb_range_zones_same_last_and_first_zone_id(self):
        """
        Check can get Invalid_Argument(2) error return if rgbFirstZoneID > rgbLastZoneID.
        
        [5] setRangeRgbZones(rgbFirstZoneIDs, rgbLastZoneIDs, rgbValues) -> rgbFirstZoneIDs
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over x in range[1..3]")
        # --------------------------------------------------------------------------------------------------------------
        for x in [1, 2, 3]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Random select 2 zones, z1 and z2 from zoneList where z1 > z2")
            # ----------------------------------------------------------------------------------------------------------
            zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(
                zone_id_list=self.supported_zone_list)
            z1 = zone_selector.random_zone_selector()
            z2 = zone_selector.random_zone_selector()

            if z1 < z2:
                z1, z2 = z2, z1
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRangeRgbZones w/ [z1, z2, rgbValue=RED, 0xFF]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_range_rgb_zones_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                rgb_first_zone_id_0=z1,
                rgb_last_zone_id_0=z2,
                red_index_0=0xff,
                green_index_0=0x0,
                blue_index_0=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _INVALID_ARGUMENT)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                       report=report,
                                                                       error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0007", _AUTHOR)
    # end def test_set_rgb_range_zones_same_last_and_first_zone_id

    @features("Feature8081")
    @features("Feature8081v1")
    @level("ErrorHandling")
    def test_set_rgb_range_zones_last_id_invalid(self):
        """
        Check can get Invalid_Argument(2) error return if set rgbLastZoneID = 0x0 or 0xFF.
        
        [5] setRangeRgbZones(rgbFirstZoneIDs, rgbLastZoneIDs, rgbValues) -> rgbFirstZoneIDs
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select a zones, z1 from zoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)
        z1 = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRangeRgbZones w/ [z1, 0xFF, rgbValue=RED, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8081.set_range_rgb_zones_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8081_index,
            rgb_first_zone_id_0=z1,
            rgb_last_zone_id_0=0xff,
            red_index_0=0xff,
            green_index_0=0x0,
            blue_index_0=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _INVALID_ARGUMENT)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                   report=report,
                                                                   error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRangeRgbZones w/ [z1, 0x0, rgbValue=RED, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8081.set_range_rgb_zones_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8081_index,
            rgb_first_zone_id_0=z1,
            rgb_last_zone_id_0=0x0,
            red_index_0=0xff,
            green_index_0=0x0,
            blue_index_0=0x0,
            rgb_first_zone_id_1=0xff,
            rgb_last_zone_id_1=0xff,
            red_index_1=0x0,
            green_index_1=0x0,
            blue_index_1=0x0,
            rgb_first_zone_id_2=0xff,
            rgb_last_zone_id_2=0xff,
            red_index_2=0x0,
            green_index_2=0x0,
            blue_index_2=0x0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _INVALID_ARGUMENT)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                   report=report,
                                                                   error_codes=[ErrorCodes.INVALID_ARGUMENT])
        self.testCaseChecked("ERR_8081_0008", _AUTHOR)
    # end def test_set_rgb_range_zones_last_id_invalid

    @features("Feature8081")
    @features("Feature8081v1")
    @level("ErrorHandling")
    def test_set_rgb_range_zones_unsupported_zone_id(self):
        """
        Check can get Invalid_Argument(2) error return if set rgbLastZoneID = unsupported zones
        
        [5] setRangeRgbZones(rgbFirstZoneIDs, rgbLastZoneIDs, rgbValues) -> rgbFirstZoneIDs
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select a zones, z1, from zoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(self.supported_zone_list)
        z1 = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select a unsupported zone, uz, from unsupportedZoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(self.unsupported_zone_list)
        uz = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRangeRgbZones w/ [z1, uz, rgbValue=RED, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8081.set_range_rgb_zones_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8081_index,
            rgb_first_zone_id_0=z1,
            rgb_last_zone_id_0=uz,
            red_index_0=0xff,
            green_index_0=0x0,
            blue_index_0=0x0,
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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _INVALID_ARGUMENT)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                   report=report,
                                                                   error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setRangeRgbZones w/ [uz, z1, rgbValue=RED, 0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8081.set_range_rgb_zones_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8081_index,
            rgb_first_zone_id_0=uz,
            rgb_last_zone_id_0=z1,
            red_index_0=0xff,
            green_index_0=0x0,
            blue_index_0=0x0,
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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _INVALID_ARGUMENT)
        # --------------------------------------------------------------------------------------------------------------
        PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                   report=report,
                                                                   error_codes=[ErrorCodes.INVALID_ARGUMENT])
        self.testCaseChecked("ERR_8081_0009", _AUTHOR)
    # end def test_set_rgb_range_zones_unsupported_zone_id

    @features("Feature8081")
    @level("ErrorHandling")
    def test_set_rgb_zones_single_value_unsupported_zone_id(self):
        """
        Check can get Invalid_Argument(2) error return if set rgbLastZoneID = unsupported zones
        
        [6] setRgbZonesSingleValue(rgbZoneR, rgbZoneG, rgbZoneB, rgbZoneID[0], .., rgbZoneID[12]) -> rgbZoneR,
        rgbZoneG, rgbZoneB, rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select 4 zones, z1, z2, z3, z4, from zoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(self.supported_zone_list)
        z1 = zone_selector.random_zone_selector()
        z2 = zone_selector.random_zone_selector()
        z3 = zone_selector.random_zone_selector()
        z4 = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over uz in unsupportedZoneList (several unsupported values)")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(self.unsupported_zone_list)
        uz1 = zone_selector.random_zone_selector()
        uz2 = zone_selector.random_zone_selector()
        uz3 = zone_selector.random_zone_selector()
        uz4 = zone_selector.random_zone_selector()

        for uz in [uz1, uz2, uz3, uz4]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send setRgbZonesSingleValue w/ [rgbValue=RED, z1, z2, uz, z3, z4, 0, .., 0]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_rgb_zones_single_value_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                rgb_zone_red=0xff,
                rgb_zone_green=0x0,
                rgb_zone_blue=0x0,
                rgb_zone_id_0=z1,
                rgb_zone_id_1=z2,
                rgb_zone_id_2=uz,
                rgb_zone_id_3=z3,
                rgb_zone_id_4=z4)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _INVALID_ARGUMENT)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                       report=report,
                                                                       error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0010", _AUTHOR)
    # end def test_set_rgb_zones_single_value_unsupported_zone_id

    @features("Feature8081")
    @level("ErrorHandling")
    def test_set_persistence_invalid_value(self):
        """
        Set persistence w/ invalid value. Shall receive invalid_arguments(2) error return.
        
        [7] void frameEnd(persistence, nFramesTillNextChange)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over persistence in error range (several invalid values)")
        # --------------------------------------------------------------------------------------------------------------
        for persistence in [0x02, 0x03, 0x04]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send frameEnd w/ [persistence=invalid value, 0, .., 0]")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.frame_end_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8081_index,
                persistence=persistence,
                current_frame=0x0,
                n_frames_till_next_change=0x0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _INVALID_ARGUMENT)
            # ----------------------------------------------------------------------------------------------------------
            PerKeyLightingTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                                       report=report,
                                                                       error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8081_0011", _AUTHOR)
    # end def test_set_persistence _invalid_value
# end class PerKeyLightingErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
