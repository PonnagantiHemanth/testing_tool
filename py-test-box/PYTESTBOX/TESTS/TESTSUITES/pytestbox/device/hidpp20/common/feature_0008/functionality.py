#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0008.functionality
:brief: HID++ 2.0 ``KeepAlive`` functionality test suite
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keepaliveutils import KeepAliveTestUtils
from pytestbox.device.hidpp20.common.feature_0008.keepalive import KeepAliveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Harish Kumar D"
_CHECK_EVENT = "Check keepAliveTimeout Event response field"
_END_TEST_LOOP = "End Test Loop"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class KeepAliveFunctionalityTestCase(KeepAliveTestCase):
    """
    Validate ``KeepAlive`` functionality test cases
    """

    @features("Feature0008v1")
    @level("Functionality")
    def test_check_keep_alive_requested_with_timeout(self):
        """
        Check Keep Alive can be requested within the valid timeout range
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over various interesting values between "
                                 f"{self.config.F_TimeoutMin} and {self.config.F_TimeoutMax}")
        # --------------------------------------------------------------------------------------------------------------
        rand_requested_timeouts = KeepAliveTestCase.generate_random_times(self, number_of_requested_timeout=10)

        for timeout in rand_requested_timeouts:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send keepAlive with requested Timeout = {timeout}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive(
                test_case=self,
                requested_timeout=timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, F"Check finalTimeout received is same as requested Timeout = "
                                      F"{timeout}.")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_timeout_response(
                self,
                response=response,
                requested_timeout=timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check keepAliveTimeout Event is received after the selected timeout "
                                      "interval")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive_timeout_event(
                test_case=self,
                timeout=to_int(timeout) / self.one_millisecond)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_EVENT)
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_keepalive_event(self, response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_0008_0001", _AUTHOR)
    # end def test_check_keep_alive_requested_with_timeout

    @features("Feature0008v1")
    @level("Functionality")
    def test_check_multiple_keep_alive_requested_with_timeout(self):
        """
        Check Multiple Keep Alive can be requested within the valid timeout range and without triggering timeout
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over various interesting values between {self.config.F_TimeoutMin} and "
                                 f"{self.config.F_TimeoutMax}")
        # --------------------------------------------------------------------------------------------------------------
        requested_timeouts = KeepAliveTestCase.generate_random_times(self, number_of_requested_timeout=10)

        for timeout in requested_timeouts:
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send keepAlive with requested Timeout= {timeout}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check finalTimeout received is same as requested Timeout.")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_timeout_response(self, response=response, requested_timeout=timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check keepAliveTimeout Event is NOT received within the time less than "
                                      f"{(to_int(timeout) - self.config.F_ToleranceMs) / self.one_millisecond}")
            # ----------------------------------------------------------------------------------------------------------
            sleep(abs(to_int(timeout) - self.one_millisecond) / self.one_millisecond)
            ChannelUtils.check_queue_empty(
                test_case=self,
                class_type=self.feature_0008.keep_alive_timeout_event_cls,
                queue_name=HIDDispatcher.QueueName.EVENT)

            # wait for keep alive event occurred
            sleep(self.config.F_TimeoutMax / self.one_millisecond)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeout Event is received once after the last keepAlive and"
                                  "requested Timeout.")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive_timeout_event(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_EVENT)
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_keepalive_event(self, response)

        self.testCaseChecked("FUN_0008_0002", _AUTHOR)
    # end def test_check_multiple_keep_alive_requested_with_timeout

    @features("Feature0008v1")
    @level("Functionality")
    def test_verify_keep_alive_requested_with_timeout(self):
        """
        Verify the keepAliveTimeout is received at requestedTimeout (one keepalive)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over several interesting values between "
                                 f"{self.config.F_TimeoutMin}..{self.config.F_TimeoutMax}")
        # --------------------------------------------------------------------------------------------------------------
        rand_requested_timeouts = KeepAliveTestCase.generate_random_times(self, number_of_requested_timeout=10)

        for timeout in rand_requested_timeouts:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send keepAlive with requested Timeout= {timeout}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=timeout)
            last_timestamp = response.timestamp

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check finalTimeout is same as requested Timeout.")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_timeout_response(self, response=response, requested_timeout=timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check keepAliveTimeout event is received exactly at requested Timeout(~20ms)")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive_timeout_event(
                test_case=self, timeout=to_int(timeout) / self.one_millisecond)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_EVENT)
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_keepalive_event(self, response)

            # convert timestamp (ns) into milliseconds
            delta = (((response.timestamp - last_timestamp) / self.one_microsecond) - to_int(timeout))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check keepAliveTimeout is received exactly at requested Timeout(~20ms)")
            # ----------------------------------------------------------------------------------------------------------
            self.assertLessEqual(a=delta, b=self.config.F_ToleranceMs,
                                 msg=f"Timeout is occurred outside the range (Time difference = {delta} ms)")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_0008_0003", _AUTHOR)
    # end def test_verify_keep_alive_requested_with_timeout

    @features("Feature0008v1")
    @level("Functionality")
    def test_verify_multiple_keep_alive_requested_with_timeout(self):
        """
        Verify the keepAliveTimeout is received at requestedTimeout (multiple keepalive)
        """
        last_timestamp = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={self.config.F_TimeoutMax}.")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(
            test_case=self,
            requested_timeout=self.max_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate response fields")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_timeout_response(
            self,
            response=response,
            requested_timeout=self.max_timeout)

        LogHelper.log_info(self, "Wait for event to occur")
        sleep(self.config.F_TimeoutMax / self.one_millisecond)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over several values between "
                                 f"{self.config.F_TimeoutMin}..{self.config.F_TimeoutMax}-1")
        # --------------------------------------------------------------------------------------------------------------
        high_requested_timeouts = KeepAliveTestCase.generate_random_times(
            self,
            number_of_requested_timeout=10,
            minimum=self.config.F_TimeoutMin,
            maximum=self.config.F_TimeoutMax - 1)

        for timeout in high_requested_timeouts:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "sleep for selected timeout window")
            # ----------------------------------------------------------------------------------------------------------
            sleep(to_int(timeout) / self.one_millisecond)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={self.config.F_TimeoutMax}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive(
                test_case=self,
                requested_timeout=self.max_timeout)

            last_timestamp = response.timestamp

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate response fields and check event is not received")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_timeout_response(
                self,
                response=response,
                requested_timeout=self.max_timeout)

            ChannelUtils.check_queue_empty(
                test_case=self,
                class_type=self.feature_0008.keep_alive_timeout_event_cls,
                queue_name=HIDDispatcher.QueueName.EVENT)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeout is received exactly at requestedTimeout(+/- 20ms) from "
                                  "the last keepAlive request")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive_timeout_event(
            test_case=self,
            timeout=self.config.F_TimeoutMax / self.one_millisecond)

        KeepAliveTestCase.check_expected_keepalive_event(self, response)

        # convert timestamp (ns) into milliseconds
        delta = ((response.timestamp - last_timestamp) / self.one_microsecond) - self.config.F_TimeoutMax

        self.assertLessEqual(
            a=delta,
            b=self.config.F_ToleranceMs,
            msg=f"Timeout is occurred outside the range (Time difference = {delta} ms)")

        self.testCaseChecked("FUN_0008_0004", _AUTHOR)
    # end def test_verify_multiple_keep_alive_requested_with_timeout
# end class KeepAliveFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
