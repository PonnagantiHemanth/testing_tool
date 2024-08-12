#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0008.business
:brief: HID++ 2.0 ``KeepAlive`` business test suite
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keepaliveutils import KeepAliveTestUtils
from pytestbox.device.hidpp20.common.feature_0008.keepalive import KeepAliveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Harish Kumar D"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class KeepAliveBusinessTestCase(KeepAliveTestCase):
    """
    Validate ``KeepAlive`` business test cases
    """

    @features("Feature0008v1")
    @level("Business")
    def test_verify_terminate_timeout_response(self):
        """
        Verify that Keep Alive timeout event is not received after terminate
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean Event queue")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={self.config.F_TimeoutMin}")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=self.min_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_timeout_response(
            self, response=response,
            requested_timeout=self.min_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send terminate")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.terminate(test_case=self)
        # --------------------------------------------------------------------------------------------------------------

        LogHelper.log_step(self, "Check terminate response field")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_terminate_response(self, response=response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeout Event is NOT received after the selected timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.config.F_TimeoutMin / self.one_millisecond)
        ChannelUtils.check_queue_empty(
            test_case=self, class_type=self.feature_0008.keep_alive_timeout_event_cls,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send keepAlive with requestedTimeout={self.config.F_TimeoutMax}")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.keep_alive(test_case=self, requested_timeout=self.max_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check finalTimeout received is same as requestedTimeout.")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_timeout_response(
            self, response=response, requested_timeout=self.max_timeout)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send terminate and check the response")
        # --------------------------------------------------------------------------------------------------------------
        response = KeepAliveTestUtils.HIDppHelper.terminate(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check the terminate response")
        # --------------------------------------------------------------------------------------------------------------
        KeepAliveTestCase.check_expected_terminate_response(self, response=response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check keepAliveTimeout Event is NOT received after the selected timeout")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.config.F_TimeoutMax / self.one_millisecond)
        ChannelUtils.check_queue_empty(
            test_case=self, class_type=self.feature_0008.keep_alive_timeout_event_cls,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT, queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_0008_0001", _AUTHOR)
    # end def test_verify_terminate_timeout_response
# end class KeepAliveBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
