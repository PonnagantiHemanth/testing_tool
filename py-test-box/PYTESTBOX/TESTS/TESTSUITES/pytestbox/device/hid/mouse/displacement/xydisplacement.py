#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.displacement.xydisplacement
:brief: Hid mouse XY displacement test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/01/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class XYDisplacementTestCase(BaseTestCase):
    """
    Validate mouse XY displacement requirements
    """

    MAX_12_BITS_SIGNED = (1 << 11) - 1
    MIN_12_BITS_SIGNED = -MAX_12_BITS_SIGNED

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.pressed_key_ids = None
        super().setUp()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            if self.pressed_key_ids is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Release all pressed buttons")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.multiple_keys_release(key_ids=self.pressed_key_ids)
                self.pressed_key_ids = None
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def clip(self, motion):
        """
        Apply limitation on the resolution of the given X/Y motion value, depending on whether the DUT is Gaming or not.

        Rationale:
         - If the DUT is from the Gaming category, then return the given motion as-is.
           The X/Y motion resolution of Gaming Products is typically 16 bits.
         - If the DUT is NOT from the Gaming category (i.e. PWS), then apply limitation of resolution.
           The X/Y motion resolution of PWS Products is typically 12 bits.

        :param motion: X or Y motion value
        :type motion: ``int``

        :return: motion value, clipped if DUT is not a Gaming Product, raw otherwise.
        :rtype: ``int``
        """
        if self.f.PRODUCT.F_IsGaming:
            return motion
        else:
            return self.MIN_12_BITS_SIGNED if motion < self.MIN_12_BITS_SIGNED \
                else self.MAX_12_BITS_SIGNED if motion > self.MAX_12_BITS_SIGNED \
                else motion
        # end if
    # end def clip

    def force_report_rate(self, report_rate):
        """
        Force the reporting rate to the given value using the 0x8061 HID++ feature API

        :param report_rate: Report Rate
        :type report_rate: ``int`` or ``HexList``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8061 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_8061, _, _ = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_parameters(self)

        # Add a loop to ensure that the DUT has successfully transitioned to the new report rate.
        # We noticed that occasionally, our Bazooka2 sample was resetting and reverting to the default value.
        # Loop counter = 4 is an empirical value based on experience
        loop_counter = 4
        for index in range(loop_counter):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with report rate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(
                test_case=self, check_first_message=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReportRateInfoEvent response inputs fields are as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate)
            })
            checker.check_fields(self, response, self.feature_8061.report_rate_info_event_cls, check_map)

            # The DUT could reset after receiving the previous SetReportRate request
            message = ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, timeout=3,
                class_type=WirelessDeviceStatusBroadcastEvent, check_first_message=False, allow_no_message=True)
            if message is None:
                break
            elif index == (loop_counter - 1):
                raise Exception(f'Report Rate could not be configured at {report_rate}')
            else:
                # --------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = host mode")
                # --------------------------------------------------------------------------------------------------
                OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(
                    test_case=self, onboard_mode=OnboardProfiles.Mode.HOST_MODE)

                ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                            class_type=(WirelessDeviceStatusBroadcastEvent,
                                                        self.feature_8061.report_rate_info_event_cls))
            # end if
        # end for
    # end def force_report_rate
# end class XYDisplacementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
