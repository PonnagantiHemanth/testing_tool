#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0008.KeepAlive
:brief: Validate HID++ 2.0 ``KeepAlive`` feature
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randint

from pyhid.hidpp.features.common.keepalive import KeepAliveResponse
from pyhid.hidpp.features.common.keepalive import TerminateResponse
from pyhid.hidpp.features.common.keepalive import KeepAliveTimeoutEventV1
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keepaliveutils import KeepAliveTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class KeepAliveTestCase(DeviceBaseTestCase):
    """
    Validate ``KeepAlive`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()
        self.config = self.f.PRODUCT.FEATURES.COMMON.KEEP_ALIVE
        self.min_timeout = HexList(Numeral(self.config.F_TimeoutMin))
        self.max_timeout = HexList(Numeral(self.config.F_TimeoutMax))
        self.one_millisecond = 1000
        self.one_microsecond = 1000000

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0008 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0008_index, self.feature_0008, _, _ = KeepAliveTestUtils.HIDppHelper.get_parameters(
            test_case=self)
    # end def setUp

    def generate_random_times(self, number_of_requested_timeout, minimum=None, maximum=None):
        """
        Generate a random time within the specified minimum and maximum range.

        :param number_of_requested_timeout: It generates number of random values for requested_timeout.
        :type number_of_requested_timeout: ``int``
        :param minimum: The minimum value for the random time. If None, the minimum timeout value from dut
        settings is used. - OPTIONAL
        :type minimum: ``int``
        :param maximum: The maximum value for the random time. If None, the maximum timeout value from dut
        settings is used.  - OPTIONAL
        :type maximum: ``int``

        :return: The list of random timeout within range of maximum and minimum
        :rtype: ``list[HexList]``
        """

        minimum = self.config.F_TimeoutMin if minimum is None else minimum
        maximum = self.config.F_TimeoutMax if maximum is None else maximum

        self.number_of_requested_timeout = number_of_requested_timeout
        self.requested_timeout = []

        for _ in range(self.number_of_requested_timeout):
            timeout = randint(minimum, maximum)
            self.requested_timeout.append(HexList(Numeral(timeout)))
        # end for
        return self.requested_timeout
    # end def generate_random_time

    def check_expected_timeout_response(self, response, requested_timeout):
        """
        Check expected response form keep alive API.

        :param response: The keep alive response class
        :type response: ``KeepAliveResponse``
        :param requested_timeout: Keep alive requested timeout
        :type requested_timeout: ``HexList``
        """

        checker = KeepAliveTestUtils.KeepAliveResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "final_timeout": (checker.check_final_timeout, requested_timeout)
        })
        checker.check_fields(self, response, self.feature_0008.keep_alive_response_cls, check_map)
    # end def check_expected_request_timeout

    def check_expected_terminate_response(self, response):
        """
        Check expected response form terminate API.

        :param response: The terminate response class
        :type response: ``TerminateResponse``
        """

        checker = KeepAliveTestUtils.MessageChecker
        checker.check_fields(self, response, self.feature_0008.terminate_response_cls, {})
    # end def check_expected_terminate

    def check_expected_keepalive_event(self, event):
        """
        Check expected event form keep alive API.

        :param event: The keep alive event class
        :type event: ``KeepAliveTimeoutEventV1``
        """

        checker = KeepAliveTestUtils.KeepAliveTimeoutEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "reserved": (checker.check_reserved, HexList(0x00))
        })
        checker.check_fields(self, event, self.feature_0008.keep_alive_timeout_event_cls, check_map)
    # end def check_expected_event
# end class KeepAliveTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
