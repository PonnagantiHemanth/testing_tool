#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_18a1.errorhandling
:brief: HID++ 2.0 ``LEDTest`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.ledtestutils import LEDTestTestUtils
from pytestbox.device.hidpp20.common.feature_18a1.ledtest import LEDTestTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class LEDTestErrorHandlingTestCase(LEDTestTestCase):
    """
    Validate ``LEDTest`` errorhandling test cases
    """

    @features("Feature18A1")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_18a1.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetLEDList request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_18a1.get_led_list_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_18a1_index)
            report.function_index = function_index

            LEDTestTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_18A1_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature18A1")
    @level("ErrorHandling")
    def test_get_led_list_without_enabling_manufacturing_features(self):
        """
        Validate trying to send an API  without enabling manufacturing features returns an NOT_ALLOWED error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable manufaturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLEDList request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_18a1.get_led_list_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_18a1_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code")
        # --------------------------------------------------------------------------------------------------------------
        LEDTestTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_18A1_0002#1", _AUTHOR)
    # end def test_get_led_list_without_enabling_manufacturing_features

    @features("Feature18A1")
    @level("ErrorHandling")
    def test_get_led_test_mode_without_enabling_manufacturing_features(self):
        """
        Validate trying to send an API  without enabling manufacturing features returns an NOT_ALLOWED error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable manufaturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLEDTestMode request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_18a1.get_led_test_mode_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_18a1_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code")
        # --------------------------------------------------------------------------------------------------------------
        LEDTestTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_18A1_0002#2", _AUTHOR)
    # end def test_get_led_test_mode_without_enabling_manufacturing_features

    @features("Feature18A1")
    @level("ErrorHandling")
    def test_set_led_test_mode_without_enabling_manufacturing_features(self):
        """
        Validate trying to send an API  without enabling manufacturing features returns an NOT_ALLOWED error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable manufaturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLEDTestMode request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_18a1.set_led_test_mode_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_18a1_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code")
        # --------------------------------------------------------------------------------------------------------------
        LEDTestTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_18A1_0002#3", _AUTHOR)
    # end def test_set_led_test_mode_without_enabling_manufacturing_features

    @features("Feature18A1")
    @level("ErrorHandling")
    def test_trying_to_turn_on_led_not_available_in_device(self):
        """
        Validate trying to turn on an LED not available in device returns INVALID_ARGUMENT error
        """
        ON = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLEDTestMode API with an invalid led set to ON state")
        # --------------------------------------------------------------------------------------------------------------
        led_presence_map = LEDTestTestUtils.get_led_presence_map(self)
        led_state_map = LEDTestTestUtils.get_led_state_map()
        led_state_map[next(led for led, presence in led_presence_map.items() if not presence)] = ON

        report = self.feature_18a1.set_led_test_mode_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_18a1_index, **led_state_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check INVALID_ARGUMENT error is returned")
        # --------------------------------------------------------------------------------------------------------------
        LEDTestTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_18A1_0002", _AUTHOR)
    # end def test_trying_to_turn_on_led_not_available_in_device
# end class LEDTestErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
