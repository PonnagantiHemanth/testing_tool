#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8100.robustness
:brief: HID++ 2.0 ``OnboardProfiles`` robustness test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/01/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.gaming.feature_8100.onboardprofiles import OnboardProfilesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OnboardProfilesRobustnessTestCase(OnboardProfilesTestCase):
    """
    Validate ``OnboardProfiles`` robustness test cases
    """

    @features("Feature8100")
    @level("Robustness")
    def test_get_onboard_profiles_info_software_id(self):
        """
        Validate ``GetOnboardProfilesInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over software id range (several interesting values)")
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(OnboardProfiles.DEFAULT.SOFTWARE_ID):
            if software_id == 0:
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetOnboardProfilesInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8100.get_onboard_profiles_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8100_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8100.get_onboard_profiles_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetOnboardProfilesInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = OnboardProfilesTestUtils.GetOnboardProfilesInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            })
            checker.check_fields(self, response, self.feature_8100.get_onboard_profiles_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8100_0001", _AUTHOR)
    # end def test_get_onboard_profiles_info_software_id

    @features("Feature8100")
    @level("Robustness")
    def test_get_onboard_profiles_info_padding(self):
        """
        Validate ``GetOnboardProfilesInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over padding range (several interesting values)")
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8100.get_onboard_profiles_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetOnboardProfilesInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8100_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8100.get_onboard_profiles_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetOnboardProfilesInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = OnboardProfilesTestUtils.GetOnboardProfilesInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            })
            checker.check_fields(self, response, self.feature_8100.get_onboard_profiles_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8100_0002", _AUTHOR)
    # end def test_get_onboard_profiles_info_padding
# end class OnboardProfilesRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
