#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8135.robustness
:brief: HID++ 2.0 ``PedalStatus`` robustness test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.pedalstatus import PedalStatus
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.pedalstatusutils import PedalStatusTestUtils
from pytestbox.device.hidpp20.gaming.feature_8135.pedalstatus import PedalStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PedalStatusRobustnessTestCase(PedalStatusTestCase):
    """
    Validate ``PedalStatus`` robustness test cases
    """

    @features("Feature8135")
    @level("Robustness")
    def test_get_pedal_status_software_id(self):
        """
        Validate ``GetPedalStatus`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PedalStatus.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPedalStatus request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8135.get_pedal_status_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8135_index)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_8135.get_pedal_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPedalStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PedalStatusTestUtils.GetPedalStatusResponseChecker
            checker.check_fields(self, response, self.feature_8135.get_pedal_status_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8135_0001", _AUTHOR)
    # end def test_get_pedal_status_software_id

    @features("Feature8135")
    @level("Robustness")
    def test_get_pedal_status_padding(self):
        """
        Validate ``GetPedalStatus`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8135.get_pedal_status_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPedalStatus request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8135_index)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_8135.get_pedal_status_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPedalStatusResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PedalStatusTestUtils.GetPedalStatusResponseChecker
            checker.check_fields(self, response, self.feature_8135.get_pedal_status_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8135_0002", _AUTHOR)
    # end def test_get_pedal_status_padding
# end class PedalStatusRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
