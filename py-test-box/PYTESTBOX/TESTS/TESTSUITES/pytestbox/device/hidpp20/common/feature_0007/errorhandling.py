#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0007.errorhandling
:brief: HID++ 2.0 DeviceFriendlyName error handling test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/10/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname import DeviceFriendlyNameTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceFriendlyNameErrorHandlingTestCase(DeviceFriendlyNameTestCase):
    """
    Validates DeviceFriendlyName error handling test cases
    """
    @features('Feature0007')
    @level('ErrorHandling')
    def test_get_friendly_name_wrong_starting_position(self):
        """
        Validates get friendly name read with wrong starting position
        """
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        byte_index = int(Numeral(response.name_max_len)) + 1
        # -------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send GetFriendlyName request with wrong byte_index: {byte_index} '
                                 f'for name_max_len: {response.name_max_len}')
        # -------------------------------------------------------------------------------------------
        report = self.feature_0007.get_friendly_name_cls(
            ChannelUtils.get_device_index(test_case=self), self.feature_0007_index, HexList(byte_index))
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_0007.get_friendly_name_response_cls)

        # --------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate default padding 0x00 is received')
        # --------------------------------------------------------------------
        self.assertEqual(
            obtained=response.name_chunk,
            expected=HexList("00" * (self.feature_0007.get_friendly_name_response_cls.LEN.NAME_CHUNK // 8)),
            msg="The parameter differs from the one expected")
        self.testCaseChecked("ERR_0007_0001", _AUTHOR)
    # end def test_get_friendly_name_wrong_starting_position

    @features('Feature0007')
    @level('ErrorHandling')
    def test_get_default_friendly_name_wrong_starting_position(self):
        """
        Validates default friendly name read with wrong starting position
        """
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        byte_index = int(Numeral(response.name_max_len)) + 1
        # --------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send GetDefaultFriendlyName request with wrong byte_index: {byte_index} '
                                 f'for name_max_len: {response.name_max_len}')
        # --------------------------------------------------------------------------------------------------
        report = self.feature_0007.get_default_friendly_name_cls(
                ChannelUtils.get_device_index(test_case=self), self.feature_0007_index, HexList(byte_index))
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_0007.get_default_friendly_name_response_cls)

        # --------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate default padding 0x00 is received')
        # --------------------------------------------------------------------
        self.assertEqual(obtained=response.name_chunk,
                         expected=HexList("00" * (
                                 self.feature_0007.get_default_friendly_name_response_cls.LEN.NAME_CHUNK // 8)),
                         msg="The parameter differs from the one expected")
        self.testCaseChecked("ERR_0007_0002", _AUTHOR)
    # end def test_get_default_friendly_name_wrong_starting_position

    @features('Feature0007')
    @level('ErrorHandling')
    def test_wrong_function_index(self):
        """
        Validates function index
        """
        wrong_index = DeviceFriendlyName.MAX_FUNCTION_INDEX + 1
        # ---------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetFriendlyNameLen request with function index: {wrong_index}")
        # ---------------------------------------------------------------------------------------------
        report = self.feature_0007.get_friendly_name_len_cls(
            ChannelUtils.get_device_index(test_case=self), self.feature_0007_index)
        report.functionIndex = wrong_index
        error_response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate error code: {ErrorCodes.INVALID_FUNCTION_ID}")
        # ---------------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                         expected=ErrorCodes.INVALID_FUNCTION_ID,
                         msg="The error_code parameter differs from the one expected")
        self.testCaseChecked("ERR_0007_0003", _AUTHOR)
    # end def test_wrong_function_index
# end class DeviceFriendlyNameErrorHandlingTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
