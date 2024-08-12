#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8081.robustness
:brief: HID++ 2.0 ``PerKeyLighting`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.perkeylighting import PerKeyLighting
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.perkeylightingutils import PerKeyLightingTestUtils
from pytestbox.device.hidpp20.gaming.feature_8081.perkeylighting import PerKeyLightingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PerKeyLightingRobustnessTestCase(PerKeyLightingTestCase):
    """
    Validate ``PerKeyLighting`` robustness test cases
    """

    @features("Feature8081")
    @level("Robustness")
    def test_get_info_software_id(self):
        """
        Validate ``GetInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.TypeofInfo.Param1.0xPP

        SwID boundary values [0..F]
        """
        param1 = 0x0
        type_of_info = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PerKeyLighting.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.get_info_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                type_of_info=type_of_info,
                param1=param1)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.GetInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8081.get_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0001#1", _AUTHOR)
    # end def test_get_info_software_id

    @features("Feature8081")
    @level("Robustness")
    def test_set_individual_rgb_zones_software_id(self):
        """
        Validate ``SetIndividualRGBZones`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RGBZoneID0.RedIndex0.GreenIndex0.BlueIndex0.
        RGBZoneID1.RedIndex1.GreenIndex1.BlueIndex1.RGBZoneID2.RedIndex2.GreenIndex2.BlueIndex2.RGBZoneID3.RedIndex3.
        GreenIndex3.BlueIndex3

        SwID boundary values [0..F]
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = choice(supported_zones)
        red_index_0 = 0x0
        green_index_0 = 0x0
        blue_index_0 = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------

        for software_id in compute_inf_values(PerKeyLighting.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetIndividualRGBZones request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_individual_rgb_zones_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                rgb_zone_id_0=rgb_zone_id_0,
                red_index_0=red_index_0,
                green_index_0=green_index_0,
                blue_index_0=blue_index_0)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.set_individual_rgb_zones_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetIndividualRGBZonesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
                "rgb_zone_id_1": (checker.check_rgb_zone_id_1, HexList(0x0)),
                "rgb_zone_id_2": (checker.check_rgb_zone_id_2, HexList(0x0)),
                "rgb_zone_id_3": (checker.check_rgb_zone_id_3, HexList(0x0)),
            })
            checker.check_fields(self, response, self.feature_8081.set_individual_rgb_zones_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0001#2", _AUTHOR)
    # end def test_set_individual_rgb_zones_software_id

    @features("Feature8081")
    @level("Robustness")
    def test_set_consecutive_rgb_zones_software_id(self):
        """
        Validate ``SetConsecutiveRGBZones`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RGBZoneID0.RedIndex0.GreenIndex0.BlueIndex0.RedIndex1.
        GreenIndex1.BlueIndex1.RedIndex2.GreenIndex2.BlueIndex2.RedIndex3.GreenIndex3.BlueIndex3.RedIndex4.GreenIndex4.
        BlueIndex4

        SwID boundary values [0..F]
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = choice(supported_zones)
        red_index_0 = 0x0
        green_index_0 = 0x0
        blue_index_0 = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PerKeyLighting.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetConsecutiveRGBZones request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_consecutive_rgb_zones_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                rgb_zone_id_0=rgb_zone_id_0,
                red_index_0=red_index_0,
                green_index_0=green_index_0,
                blue_index_0=blue_index_0)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.set_consecutive_rgb_zones_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetConsecutiveRGBZonesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
            })
            checker.check_fields(self, response, self.feature_8081.set_consecutive_rgb_zones_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0001#3", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_software_id

    @features("Feature8081")
    @level("Robustness")
    def test_set_consecutive_rgb_zones_delta_compression_5bit_software_id(self):
        """
        Validate ``SetConsecutiveRGBZonesDeltaCompression5bit`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RGBZoneID0.RGBComponent5bit

        SwID boundary values [0..F]
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = choice(supported_zones)
        red_index_0 = 0
        green_index_0 = 0
        blue_index_0 = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PerKeyLighting.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConsecutiveRGBZonesDeltaCompression5bit request with software_id: "
                                     f"{software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                rgb_zone_id_0=rgb_zone_id_0,
                red_index_0=red_index_0,
                green_index_0=green_index_0,
                blue_index_0=blue_index_0)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetConsecutiveRGBZonesDeltaCompression5bitResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression5bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_5bit_response_cls,
                check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0001#4", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_delta_compression_5bit_software_id

    @features("Feature8081")
    @level("Robustness")
    def test_set_consecutive_rgb_zones_delta_compression_4bit_software_id(self):
        """
        Validate ``SetConsecutiveRGBZonesDeltaCompression4bit`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RGBZoneID0.RGBComponent4bit

        SwID boundary values [0..F]
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = supported_zones[0]
        red_index_0 = 0
        green_index_0 = 0
        blue_index_0 = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PerKeyLighting.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConsecutiveRGBZonesDeltaCompression4bit request with software_id: "
                                     f"{software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                rgb_zone_id_0=rgb_zone_id_0,
                red_index_0=red_index_0,
                green_index_0=green_index_0,
                blue_index_0=blue_index_0)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetConsecutiveRGBZonesDeltaCompression4bitResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetConsecutiveRGBZonesDeltaCompression4bitResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
            })
            checker.check_fields(
                self, response, self.feature_8081.set_consecutive_rgb_zones_delta_compression_4bit_response_cls,
                check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0001#5", _AUTHOR)
    # end def test_set_consecutive_rgb_zones_delta_compression_4bit_software_id

    @features("Feature8081")
    @level("Robustness")
    def test_set_range_rgb_zones_software_id(self):
        """
        Validate ``SetRangeRGBZones`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RGBFirstZoneID0.RGBLastZoneID0.RedIndex0.GreenIndex0.
        BlueIndex0.RGBFirstZoneID1.RGBLastZoneID1.RedIndex1.GreenIndex1.BlueIndex1.RGBFirstZoneID2.RGBLastZoneID2.
        RedIndex2.GreenIndex2.BlueIndex2.0xPP

        SwID boundary values [0..F]
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_first_zone_id_0 = supported_zones[0]
        rgb_last_zone_id_0 = supported_zones[-1]
        red_index_0 = 0x0
        green_index_0 = 0x0
        blue_index_0 = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PerKeyLighting.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetRangeRGBZones request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_range_rgb_zones_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                rgb_first_zone_id_0=rgb_first_zone_id_0,
                rgb_last_zone_id_0=rgb_last_zone_id_0,
                red_index_0=red_index_0,
                green_index_0=green_index_0,
                blue_index_0=blue_index_0
            )
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.set_range_rgb_zones_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRangeRGBZonesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetRangeRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_first_zone_id_0": (checker.check_rgb_first_zone_id_0, rgb_first_zone_id_0),
                "rgb_first_zone_id_1": (checker.check_rgb_first_zone_id_1, HexList(0x0)),
                "rgb_first_zone_id_2": (checker.check_rgb_first_zone_id_2, HexList(0x0)),
            })
            checker.check_fields(self, response, self.feature_8081.set_range_rgb_zones_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0001#6", _AUTHOR)
    # end def test_set_range_rgb_zones_software_id

    @features("Feature8081")
    @level("Robustness")
    def test_set_rgb_zones_single_value_software_id(self):
        """
        Validate ``SetRGBZonesSingleValue`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RGBZoneRed.RGBZoneGreen.RGBZoneBlue.RGBZoneID0.
        RGBZoneID1.RGBZoneID2.RGBZoneID3.RGBZoneID4.RGBZoneID5.RGBZoneID6.RGBZoneID7.RGBZoneID8.RGBZoneID9.RGBZoneID10.
        RGBZoneID11.RGBZoneID12

        SwID boundary values [0..F]
        """
        rgb_zone_red = 0x0
        rgb_zone_green = 0x0
        rgb_zone_blue = 0x0
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = supported_zones[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PerKeyLighting.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetRGBZonesSingleValue request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.set_rgb_zones_single_value_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                rgb_zone_red=rgb_zone_red,
                rgb_zone_green=rgb_zone_green,
                rgb_zone_blue=rgb_zone_blue,
                rgb_zone_id_0=rgb_zone_id_0)

            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.set_rgb_zones_single_value_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRGBZonesSingleValueResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
                "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
                "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
            })
            checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls,
                                 check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0001#7", _AUTHOR)
    # end def test_set_rgb_zones_single_value_software_id

    @features("Feature8081")
    @level("Robustness")
    def test_frame_end_software_id(self):
        """
        Validate ``FrameEnd`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Persistence.CurrentFrame.NFramesTillNextChange.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        persistence = 0x0
        current_frame = 0x0
        n_frames_till_next_change = 0x0
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = supported_zones[0]
        red_index_0 = 0x0
        green_index_0 = 0x0
        blue_index_0 = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PerKeyLighting.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetIndividualRGBZonesRequest")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(test_case=self,
                                                                                    rgb_zone_id_0=rgb_zone_id_0,
                                                                                    red_index_0=red_index_0,
                                                                                    green_index_0=green_index_0,
                                                                                    blue_index_0=blue_index_0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetIndividualRGBZonesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0)
            })
            checker.check_fields(self, response, self.feature_8081.set_individual_rgb_zones_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send FrameEnd request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8081.frame_end_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                persistence=persistence,
                current_frame=current_frame,
                n_frames_till_next_change=n_frames_till_next_change)
            report.software_id = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.frame_end_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check FrameEndResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8081.frame_end_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0001#8", _AUTHOR)
    # end def test_frame_end_software_id

    @features("Feature8081")
    @level("Robustness")
    def test_get_info_padding(self):
        """
        Validate ``GetInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.TypeofInfo.Param1.0xPP

        Padding (PP) boundary values [00..FF]
        """
        type_of_info = 0x0
        param1 = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8081.get_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                type_of_info=type_of_info,
                param1=HexList(param1)
            )
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.GetInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8081.get_info_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0002#1", _AUTHOR)
    # end def test_get_info_padding

    @features("Feature8081")
    @level("Robustness")
    def test_set_range_rgb_zones_padding(self):
        """
        Validate ``SetRangeRGBZones`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RGBFirstZoneID0.RGBLastZoneID0.RedIndex0.GreenIndex0.
        BlueIndex0.RGBFirstZoneID1.RGBLastZoneID1.RedIndex1.GreenIndex1.BlueIndex1.RGBFirstZoneID2.RGBLastZoneID2.
        RedIndex2.GreenIndex2.BlueIndex2.0xPP

        Padding (PP) boundary values [00..FF]
        """
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_first_zone_id_0 = supported_zones[0]
        rgb_last_zone_id_0 = supported_zones[-1]
        red_index_0 = 0x0
        green_index_0 = 0x0
        blue_index_0 = 0x0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8081.set_range_rgb_zones_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetRangeRGBZones request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                rgb_first_zone_id_0=rgb_first_zone_id_0,
                rgb_last_zone_id_0=rgb_last_zone_id_0,
                red_index_0=red_index_0,
                green_index_0=green_index_0,
                blue_index_0=blue_index_0)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.set_range_rgb_zones_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRangeRGBZonesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetRangeRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_first_zone_id_0": (checker.check_rgb_first_zone_id_0, rgb_first_zone_id_0),
                "rgb_first_zone_id_1": (checker.check_rgb_first_zone_id_1, HexList(0x0)),
                "rgb_first_zone_id_2": (checker.check_rgb_first_zone_id_2, HexList(0x0)),
            })
            checker.check_fields(self, response, self.feature_8081.set_range_rgb_zones_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0002#2", _AUTHOR)
    # end def test_set_range_rgb_zones_padding

    @features("Feature8081")
    @level("Robustness")
    def test_frame_end_padding(self):
        """
        Validate ``FrameEnd`` padding bytes are ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Persistence.CurrentFrame.NFramesTillNextChange.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        persistence = 0x0
        current_frame = 0x0
        n_frames_till_next_change = 0x0
        supported_zones = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(test_case=self)[0]
        rgb_zone_id_0 = supported_zones[0]
        red_index_0 = 0
        green_index_0 = 0
        blue_index_0 = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8081.frame_end_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetIndividualRGBZones request with RGBZoneID[0] = {rgb_zone_id_0} and all other inputs 0")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(test_case=self,
                                                                                    rgb_zone_id_0=rgb_zone_id_0,
                                                                                    red_index_0=red_index_0,
                                                                                    green_index_0=green_index_0,
                                                                                    blue_index_0=blue_index_0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetIndividualRGBZonesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0)
            })
            checker.check_fields(self, response, self.feature_8081.set_individual_rgb_zones_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send FrameEnd request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=HexList(ChannelUtils.get_device_index(test_case=self)),
                feature_index=HexList(self.feature_8081_index),
                persistence=persistence,
                current_frame=current_frame,
                n_frames_till_next_change=n_frames_till_next_change)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8081.frame_end_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check FrameEndResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8081.frame_end_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0002#3", _AUTHOR)
    # end def test_frame_end_padding

    @features("Feature8081")
    @features("Feature8081v1")
    @level("Robustness")
    def test_set_individual_zones_end(self):
        """
        Check set zoneID=0x0 can end of setting. The result shall be same as set zoneID=0xFF.

        [1] setIndividualRgbZones(rgbIndividualZones, rgbValues) -> rgbIndividualZones
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Random select 3 zones, z1, z2, z3, from zoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)
        z1 = zone_selector.random_zone_selector()
        z2 = zone_selector.random_zone_selector()
        z3 = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetIndividualRGBZones by [z1, rgbValue=RED, z2, rgbValue=RED, 0xFF,"
                                 "rgbValue=RED, z3, rgbValue=RED, 0]")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_id_0 = z1
        red_index_0 = 0xff
        green_index_0 = 0x0
        blue_index_0 = 0x0
        rgb_zone_id_1 = z2
        red_index_1 = 0xff
        green_index_1 = 0x0
        blue_index_1 = 0x0
        rgb_zone_id_2 = 0xff
        red_index_2 = 0xff
        green_index_2 = 0x0
        blue_index_2 = 0x0
        rgb_zone_id_3 = z3
        red_index_3 = 0xff
        green_index_3 = 0x0
        blue_index_3 = 0x0

        response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(
            test_case=self,
            device_index=ChannelUtils.get_device_index(test_case=self),
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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response shall be [z1, z2, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, HexList(rgb_zone_id_0)),
            "rgb_zone_id_1": (checker.check_rgb_zone_id_1, HexList(rgb_zone_id_1)),
            "rgb_zone_id_2": (checker.check_rgb_zone_id_2, HexList(0x0)),
            "rgb_zone_id_3": (checker.check_rgb_zone_id_3, HexList(0x0)),
        })
        checker.check_fields(self, response, self.feature_8081.set_individual_rgb_zones_response_cls, check_map)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetIndividualRGBZones by [z1, rgbValue=RED, z2, rgbValue=RED, 0x0,"
                                 "rgbValue=RED, z3, rgbValue=RED, 0]")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_id_0 = z1
        red_index_0 = 0xff
        green_index_0 = 0x0
        blue_index_0 = 0x0
        rgb_zone_id_1 = z2
        red_index_1 = 0xff
        green_index_1 = 0x0
        blue_index_1 = 0x0
        rgb_zone_id_2 = 0x0
        red_index_2 = 0xff
        green_index_2 = 0x0
        blue_index_2 = 0x0
        rgb_zone_id_3 = z3
        red_index_3 = 0xff
        green_index_3 = 0x0
        blue_index_3 = 0x0

        response = PerKeyLightingTestUtils.HIDppHelper.set_individual_rgb_zones(
            test_case=self,
            device_index=ChannelUtils.get_device_index(test_case=self),
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

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response shall be [z1, z2, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetIndividualRGBZonesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
            "rgb_zone_id_1": (checker.check_rgb_zone_id_1, rgb_zone_id_1),
            "rgb_zone_id_2": (checker.check_rgb_zone_id_2, HexList(0x0)),
            "rgb_zone_id_3": (checker.check_rgb_zone_id_3, HexList(0x0)),
        })
        checker.check_fields(self, response, self.feature_8081.set_individual_rgb_zones_response_cls,
                             check_map=check_map)
        self.testCaseChecked("ROB_8081_0003", _AUTHOR)
    # end def test_set_individual_zones_end

    @features("Feature8081")
    @features("Feature8081v1")
    @level("Robustness")
    def test_set_rgb_zones_single_value_end(self):
        """
        Check set zoneID to 0x0 or 0xFF has exactly same result. 

        [6] setRgbZonesSingleValue(rgbZoneR, rgbZoneG, rgbZoneB, rgbZoneID[0], .., rgbZoneID[12]) -> rgbZoneR,
        rgbZoneG, rgbZoneB, rgbZoneID[0]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Random select 4 zones, z1, z2, z3, z4, from zoneList")
        # --------------------------------------------------------------------------------------------------------------
        zone_selector = PerKeyLightingTestUtils.HIDppHelper.RandomZoneSelector(zone_id_list=self.supported_zone_list)
        z1 = zone_selector.random_zone_selector()
        z2 = zone_selector.random_zone_selector()
        z3 = zone_selector.random_zone_selector()
        z4 = zone_selector.random_zone_selector()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRGBZonesSingleValue w/ [rgbValue=RED, z1, z2, z3, 0xFF, z4, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0xff
        rgb_zone_green = 0x0
        rgb_zone_blue = 0x0
        rgb_zone_id_0 = z1
        rgb_zone_id_1 = z2
        rgb_zone_id_2 = z3
        rgb_zone_id_3 = 0xff
        rgb_zone_id_4 = z4

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
            rgb_zone_id_4=rgb_zone_id_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check can get the response [rgbValue=RED, z1]")
        # --------------------------------------------------------------------------------------------------------------
        checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "rgb_zone_red": (checker.check_rgb_zone_red, rgb_zone_red),
            "rgb_zone_green": (checker.check_rgb_zone_green, rgb_zone_green),
            "rgb_zone_blue": (checker.check_rgb_zone_blue, rgb_zone_blue),
            "rgb_zone_id_0": (checker.check_rgb_zone_id_0, rgb_zone_id_0),
        })
        checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRgbZonesSingleValue w/ [rgbValue=RED, z1, z2, z3, 0x0, z4, 0, .., 0]")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0xff
        rgb_zone_green = 0x0
        rgb_zone_blue = 0x0
        rgb_zone_id_0 = z1
        rgb_zone_id_1 = z2
        rgb_zone_id_2 = z3
        rgb_zone_id_3 = 0x0
        rgb_zone_id_4 = z4

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
            rgb_zone_id_4=rgb_zone_id_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check can get the response [rgbValue=RED, z1]")
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

        self.testCaseChecked("ROB_8081_0004", _AUTHOR)
    # end def test_set_rgb_zones_single_value_end

    # TODO implement this test case

    @features("Feature8081")
    @level("Robustness")
    @skip("Under development")
    def test_check_key_input_latency_time(self):
        """
        Check the key input debounce and latency time while doing [1]setRgbIndividualZone
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Collect all of valid zones into zoneList by getInfo")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start below thread")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Infinite Loop (in a thread)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Step 1: Random select a color rgbValue")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over z1, z2, z3, z4 in zoneList by step = 4")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Step 2: Send SetIndividualRgbZones w/ [z1, rgbValue, z2, rgbValue, z3, rgbValue, z4,"
                                 "rgbValue]")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send FrameEnd w/ all inputs = 0")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Infinite Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send the button pressed stimuli")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check can receive the button make packet")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send the button released stimuli")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check can receive the button break packet")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the button debounce and latency time shall not affect by 0x8081 operations.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8081_0005", _AUTHOR)
    # end def test_key_input_latency_time
# end class PerKeyLightingRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
