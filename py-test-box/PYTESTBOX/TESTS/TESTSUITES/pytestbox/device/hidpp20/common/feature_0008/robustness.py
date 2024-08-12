#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0008.robustness
:brief: HID++ 2.0 ``KeepAlive`` robustness test suite
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randint
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.keepalive import KeepAlive
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral, to_int
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keepaliveutils import KeepAliveTestUtils
from pytestbox.device.hidpp20.common.feature_0008.keepalive import KeepAliveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "HARISH KUMAR D"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class KeepAliveRobustnessTestCase(KeepAliveTestCase):
    """
    Validate ``KeepAlive`` robustness test cases
    """

    @features("Feature0008")
    @level("Robustness")
    def test_get_timeout_range_software_id(self):
        """
        Validate ``GetTimeoutRange`` software id field is ignored by the firmware

        [0] getTimeoutRange() -> timeoutMinimum, timeoutMaximum

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(KeepAlive.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetTimeoutRange request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.get_timeout_range(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetTimeoutRangeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = KeepAliveTestUtils.GetTimeoutRangeResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_0008.get_timeout_range_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0008_0001#1", _AUTHOR)
    # end def test_get_timeout_range_software_id

    @features("Feature0008")
    @level("Robustness")
    def test_keep_alive_software_id(self):
        """
        Validate ``KeepAlive`` software id field is ignored by the firmware

        [1] keepAlive(requestedTimeout) -> finalTimeout

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RequestedTimeout.0xPP
        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(KeepAlive.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send KeepAlive request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive(
                test_case=self,
                requested_timeout=self.min_timeout,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check KeepAliveResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = KeepAliveTestUtils.KeepAliveResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "final_timeout": (checker.check_final_timeout, self.min_timeout)
            })
            checker.check_fields(self, response, self.feature_0008.keep_alive_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0008_0001#2", _AUTHOR)
    # end def test_keep_alive_software_id

    @features("Feature0008")
    @level("Robustness")
    def test_terminate_software_id(self):
        """
        Validate ``Terminate`` software id field is ignored by the firmware

        [2] terminate() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(KeepAlive.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Terminate request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.terminate(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check TerminateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestUtils.MessageChecker.check_fields(
                self, response, self.feature_0008.terminate_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0008_0001#3", _AUTHOR)
    # end def test_terminate_software_id

    @features("Feature0008")
    @level("Robustness")
    def test_get_timeout_range_padding(self):
        """
        Validate ``GetTimeoutRange`` padding bytes are ignored by the firmware

        [0] getTimeoutRange() -> timeoutMinimum, timeoutMaximum

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_0008.get_timeout_range_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetTimeoutRange request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.get_timeout_range(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetTimeoutRangeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = KeepAliveTestUtils.GetTimeoutRangeResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_0008.get_timeout_range_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0008_0002#1", _AUTHOR)
    # end def test_get_timeout_range_padding

    @features("Feature0008")
    @level("Robustness")
    def test_keep_alive_padding(self):
        """
        Validate ``KeepAlive`` padding bytes are ignored by the firmware

        [1] keepAlive(requestedTimeout) -> finalTimeout

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RequestedTimeout.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_0008.keep_alive_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send KeepAlive request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive(
                test_case=self,
                requested_timeout=self.min_timeout,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check KeepAliveResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = KeepAliveTestUtils.KeepAliveResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "final_timeout": (checker.check_final_timeout, self.min_timeout)
            })
            checker.check_fields(self, response, self.feature_0008.keep_alive_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0008_0002#2", _AUTHOR)
    # end def test_keep_alive_padding

    @features("Feature0008")
    @level("Robustness")
    def test_terminate_padding(self):
        """
        Validate ``Terminate`` padding bytes are ignored by the firmware

        [2] terminate() -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_0008.terminate_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Terminate request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.terminate(test_case=self, padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check TerminateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestUtils.MessageChecker.check_fields(
                self, response, self.feature_0008.terminate_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0008_0002#3", _AUTHOR)
    # end def test_terminate_padding

    @features("Feature0008v1")
    @level("Robustness")
    def test_verify_keep_alive_after_power_reset(self):
        """
        Verify that Keep Alive is reset after Power Cycle.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={self.config.F_TimeoutMin}")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=self.min_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_timeout_response(
            self,
            response=response,
            requested_timeout=self.min_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Reset the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeout Event is NOT received after the selected timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.config.F_TimeoutMin / self.one_millisecond)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        ChannelUtils.check_queue_empty(
            test_case=self,
            timeout=self.config.F_TimeoutMin / self.one_millisecond,
            class_type=self.feature_0008.keep_alive_timeout_event_cls,
            queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={self.config.F_TimeoutMax}")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=self.max_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_timeout_response(
            self,
            response=response,
            requested_timeout=self.max_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Reset the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeout Event is NOT received after the selected timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.config.F_TimeoutMax / self.one_millisecond)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        ChannelUtils.check_queue_empty(
            test_case=self, timeout=self.config.F_TimeoutMax / self.one_millisecond,
            class_type=self.feature_0008.keep_alive_timeout_event_cls, queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("ROB_0008_0003", _AUTHOR)
    # end def test_verify_keep_alive_after_power_reset

    @features("Feature0008v1")
    @level("Robustness")
    def test_verify_no_event_after_terminate(self):
        """
        Verify terminate does not return an error when called before keepalive
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send terminate request")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.terminate(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check response is received")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_terminate_response(self, response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check keepAliveTimeout Event is NOT received upto {self.config.F_TimeoutMax}"
                                  " interval")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(
            test_case=self,
            timeout=self.config.F_TimeoutMax / self.one_millisecond,
            class_type=self.feature_0008.keep_alive_timeout_event_cls,
            queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("ROB_0008_0004", _AUTHOR)
    # end def test_verify_no_event_after_terminate

    @features("Feature0008v1")
    @level("Robustness")
    def test_validate_invalid_keep_alive_request_with_event(self):
        """
        Validate INVALID ARGUMENT is received when keepAlive is called without of range values
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over several interesting values between 0..{self.config.F_TimeoutMin}")
        # --------------------------------------------------------------------------------------------------------------
        rand_requested_timeouts = KeepAliveTestCase.generate_random_times(
            self, number_of_requested_timeout=10, minimum=1, maximum=self.config.F_TimeoutMin)

        for timeout in rand_requested_timeouts:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send keepAlive with requestedTimeout in "
                                     f"({self.config.F_TimeoutMin} < value < {self.config.F_TimeoutMax})")
            # ----------------------------------------------------------------------------------------------------------
            timeout_in_range = HexList(Numeral(randint(self.config.F_TimeoutMin, self.config.F_TimeoutMax)))
            response = KeepAliveTestUtils.HIDppHelper.keep_alive(
                test_case=self,
                requested_timeout=timeout_in_range)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_timeout_response(
                self,
                response=response,
                requested_timeout=timeout_in_range)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={timeout} and check "
                                     "error_code=INVALID ARGUMENT")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestUtils.HIDppHelper.keep_alive_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                requested_timeout=timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check keepAliveTimeout Event is received after {timeout} ")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive_timeout_event(
                test_case=self,
                timeout=to_int(timeout_in_range) / self.one_millisecond)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check keepAliveTimeout Event field")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_keepalive_event(self, response)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check no other keepAliveTimeoutEvent is received for same interval.")
            # ----------------------------------------------------------------------------------------------------------
            sleep(to_int(timeout_in_range) / self.one_millisecond)
            ChannelUtils.check_queue_empty(
                test_case=self,  timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                class_type=self.feature_0008.keep_alive_timeout_event_cls,
                queue_name=HIDDispatcher.QueueName.EVENT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send keepAlive with requestedTimeout in(timeoutMin<value<timeoutMax)")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive(
                test_case=self, requested_timeout=timeout_in_range)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_timeout_response(
                self, response=response, requested_timeout=timeout_in_range)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting values between timeoutMax..0xFFFF")
        # --------------------------------------------------------------------------------------------------------------
        rand_requested_timeouts = KeepAliveTestCase.generate_random_times(
            self, number_of_requested_timeout=10, minimum=10000, maximum=65535)

        for timeout in rand_requested_timeouts:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send keepAlive with requestedTimeout in (timeoutMin < value < timeoutMax)")
            # ----------------------------------------------------------------------------------------------------------
            timeout_in_range = HexList(Numeral(randint(self.config.F_TimeoutMin, self.config.F_TimeoutMax)))

            response = KeepAliveTestUtils.HIDppHelper.keep_alive(
                test_case=self,
                requested_timeout=timeout_in_range)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_timeout_response(
                self,
                response=response,
                requested_timeout=timeout_in_range)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={timeout}.")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestUtils.HIDppHelper.keep_alive_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                requested_timeout=timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check keepAliveTimeout Event is received after {to_int(timeout_in_range)}")
            # ----------------------------------------------------------------------------------------------------------
            response = KeepAliveTestUtils.HIDppHelper.keep_alive_timeout_event(
                test_case=self,
                timeout=to_int(timeout_in_range) / self.one_millisecond)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check keepAliveTimeout Event field")
            # ----------------------------------------------------------------------------------------------------------
            KeepAliveTestCase.check_expected_keepalive_event(self, response)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check no other keepAliveTimeoutEvent is received for same interval.")
            # ----------------------------------------------------------------------------------------------------------
            sleep(to_int(timeout_in_range) / self.one_millisecond)
            ChannelUtils.check_queue_empty(
                test_case=self,
                timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                class_type=self.feature_0008.keep_alive_timeout_event_cls,
                queue_name=HIDDispatcher.QueueName.EVENT)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0008_0005", _AUTHOR)
    # end def test_validate_invalid_keep_alive_request_with_event

    @features("Feature0008v1")
    @level("Robustness")
    def test_multiple_keep_alive_during_active(self):
        """
        Verify multiple terminate during an active keepAlive
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send keepAlive with requestedTimeout=timeoutMax")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=self.max_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_timeout_response(
            self,
            response=response,
            requested_timeout=self.max_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send terminate.")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestUtils.HIDppHelper.terminate(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeoutEvent is NOT received.")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(
            test_case=self,
            timeout=10,
            class_type=self.feature_0008.keep_alive_timeout_event_cls,
            queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send terminate again")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestUtils.HIDppHelper.terminate(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeoutEvent is NOT received.")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(
            test_case=self,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            class_type=self.feature_0008.keep_alive_timeout_event_cls,
            queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("ROB_0008_0006", _AUTHOR)
    # end def test_multiple_keep_alive_during_active

    @features("Feature0008v1")
    @level("Robustness")
    def test_multiple_keep_alive_during_inactive(self):
        """
        Verify multiple terminate during an inactive keepAlive
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send keepAlive with requestedTimeout=timeoutMin")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=self.min_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_timeout_response(
            self,
            response=response,
            requested_timeout=self.min_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeoutEvent is received at timeoutMin.")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive_timeout_event(
            test_case=self,
            timeout=self.config.F_TimeoutMin / self.one_millisecond)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeout Event response")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_keepalive_event(self, response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send terminate and check response field.")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.terminate(test_case=self)
        KeepAliveTestCase.check_expected_terminate_response(self, response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeoutEvent is NOT received.")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(
            test_case=self,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            class_type=self.feature_0008.keep_alive_timeout_event_cls,
            queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send terminate and check response field.")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.terminate(test_case=self)
        KeepAliveTestCase.check_expected_terminate_response(self, response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeoutEvent is NOT received.")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(
            test_case=self,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            class_type=self.feature_0008.keep_alive_timeout_event_cls,
            queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("ROB_0008_0007", _AUTHOR)
    # end def test_multiple_keep_alive_during_inactive
# end class KeepAliveRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
