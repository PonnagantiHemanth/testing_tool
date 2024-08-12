#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80d0.robustness
:brief: HID++ 2.0 ``CombinedPedals`` robustness test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.combinedpedals import CombinedPedals
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.combinedpedalsutils import CombinedPedalsTestUtils
from pytestbox.device.hidpp20.gaming.feature_80d0.combinedpedals import CombinedPedalsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CombinedPedalsRobustnessTestCase(CombinedPedalsTestCase):
    """
    Validates ``CombinedPedals`` robustness test cases
    """
    @features("Feature80D0")
    @level("Robustness")
    def test_get_combined_pedals_software_id(self):
        """
        Validate ``GetCombinedPedals`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID .EnableCombinedPedals.0xPP.0xPP
          SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(CombinedPedals.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCombinedPedals request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80d0.get_combined_pedals_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_80d0_index)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_80d0.get_combined_pedals_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCombinedPedalsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = CombinedPedalsTestUtils.CombinedPedalsResponseChecker
            checker.check_fields(self, response, self.feature_80d0.get_combined_pedals_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80D0_0001", _AUTHOR)
    # end def test_get_combined_pedals_software_id

    @features("Feature80D0")
    @level("Robustness")
    def test_set_combined_pedals_software_id(self):
        """
        Validate ``SetCombinedPedals`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID .EnableCombinedPedals.0xPP.0xPP
          SwID boundary values [0..F]
        """
        enable_combined_pedals = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(CombinedPedals.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCombinedPedals request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_80d0.set_combined_pedals_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_80d0_index,
                enable_combined_pedals=enable_combined_pedals)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_80d0.set_combined_pedals_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetCombinedPedalsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = CombinedPedalsTestUtils.CombinedPedalsResponseChecker
            checker.check_fields(self, response, self.feature_80d0.set_combined_pedals_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80D0_0002", _AUTHOR)
    # end def test_set_combined_pedals_software_id

    @features("Feature80D0")
    @level("Robustness")
    def test_get_combined_pedals_padding(self):
        """
        Validate ``GetCombinedPedals`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.0xPP.0xPP.0xPP
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80d0.get_combined_pedals_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCombinedPedals request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_80d0_index)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_80d0.get_combined_pedals_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCombinedPedalsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = CombinedPedalsTestUtils.CombinedPedalsResponseChecker
            checker.check_fields(self, response, self.feature_80d0.get_combined_pedals_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80D0_0003", _AUTHOR)
    # end def test_get_combined_pedals_padding

    @features("Feature80D0")
    @level("Robustness")
    def test_set_combined_pedals_padding(self):
        """
        Validate ``SetCombinedPedals`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex.EnableCombinedPedals.0xPP.0xPP
        """
        enable_combined_pedals = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80d0.set_combined_pedals_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCombinedPedals request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_80d0_index,
                enable_combined_pedals=enable_combined_pedals)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_80d0.set_combined_pedals_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetCombinedPedalsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = CombinedPedalsTestUtils.CombinedPedalsResponseChecker
            checker.check_fields(self, response, self.feature_80d0.set_combined_pedals_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80D0_0004", _AUTHOR)
    # end def test_set_combined_pedals_padding

    @features("Feature80D0")
    @level("Robustness")
    def test_set_combined_pedals_reserved(self):
        """
        Validate ``SetCombinedPedals`` reserved bytes are ignored by the firmware
        """
        enable_combined_pedals = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_80d0.set_combined_pedals_cls
        for wrong_reserved in compute_wrong_range(0, max_value=(1 << request_cls.LEN.RESERVED) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCombinedPedals request with reserved: {wrong_reserved}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_80d0_index,
                enable_combined_pedals=enable_combined_pedals)
            report.reserved = wrong_reserved
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_80d0.set_combined_pedals_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetCombinedPedalsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = CombinedPedalsTestUtils.CombinedPedalsResponseChecker
            checker.check_fields(self, response, self.feature_80d0.set_combined_pedals_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_80D0_0005", _AUTHOR)
    # end def test_set_combined_pedals_reserved
# end class CombinedPedalsRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
