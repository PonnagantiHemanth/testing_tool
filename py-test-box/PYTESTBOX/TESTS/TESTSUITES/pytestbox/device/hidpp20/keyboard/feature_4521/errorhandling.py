#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4521.errorhandling
:brief: HID++ 2.0 DisableKeys errorhandling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeys
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeysFactory
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysutils import DisableKeysUtils
from pytestbox.device.hidpp20.keyboard.feature_4521.disablekeys import DisableKeysBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysErrorHandlingTestCase(DisableKeysBaseTestCase):
    """
    0x4521 DisableKeys error handling test case
    """
    @features('Feature4521')
    @level('ErrorHandling')
    def test_invalid_function_index(self):
        """
        Invalid function index shall raise an error INVALID_FUNCTION_ID(0x07)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over functionIndex invalid range (typical wrong values)')
        # ---------------------------------------------------------------------------
        for invalid_function_index in compute_wrong_range(
                list(range(DisableKeys.MAX_FUNCTION_INDEX + 1)), max_value=0xF):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with functionIndex = {invalid_function_index}')
            # ---------------------------------------------------------------------------
            response = self.set_disable_key_with_function_index(function_index=invalid_function_index,
                                                                keys_to_disable=0x00)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes INVALID_FUNCTION_ID(7) returned by the device')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                                                                    test_case=self,
                                                                    error_message=response,
                                                                    feature_index=self.feature_4521_index,
                                                                    function_index=response.functionIndex,
                                                                    error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked('ERR_4521_0001')
    # end def test_invalid_function_index

    @features('Feature4521')
    @features('Feature4521UnsupportedKeys')
    @level('ErrorHandling')
    def test_disable_unsupported_disableable_key(self):
        """
        Disable unsupported key shall raise an error INVALID_ARGUMENT(0x02)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over keysToDisable in invalid range')
        # ---------------------------------------------------------------------------
        for keysToDisable in DisableKeysUtils.compute_unsupported_range(test_case=self):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {keysToDisable}')
            # ---------------------------------------------------------------------------
            response = self.disable_key_with_unsupported_disableable_key(unsupported_key=keysToDisable)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Error Codes INVALID_ARGUMENT(2) returned by the device")
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(test_case=self,
                                                                        error_message=response,
                                                                        feature_index=self.feature_4521_index,
                                                                        function_index=response.functionIndex,
                                                                        error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # ---------------------------------------------------------------------------

        self.testCaseChecked('ERR_4521_0002')
    # end def test_disable_unsupported_disableable_key

    @features('Feature4521')
    @level('ErrorHandling')
    def test_set_reserved_bits(self):
        """
        Set reserved bits shall raise an error INVALID_ARGUMENT(0x02)

        disabledKeys [2]SetDisabledKeys
        """
        reserved_value = [0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0, 0xE0]
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over value {reserved_value}')
        # ---------------------------------------------------------------------------
        for value in reserved_value:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with {value}')
            # ---------------------------------------------------------------------------
            response = self.disable_key_with_unsupported_disableable_key(unsupported_key=value)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate error code INVALID_ARGUMENT(0x02) returned by the device')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(test_case=self,
                                                                        error_message=response,
                                                                        feature_index=self.feature_4521_index,
                                                                        function_index=response.functionIndex,
                                                                        error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('ERR_4521_0003')
    # end def test_set_reserved_bits

    def set_disable_key_with_function_index(self, function_index, keys_to_disable, device_index=None, port_index=None):
        """
        Send SetDisabledKeys with specific function index. This could be used for invalid function index test.

        :param function_index: ID of function
        :type function_index: ``int``
        :param keys_to_disable: keys to disabled
        :type keys_to_disable: ``int``
        :param device_index: Device index - OPTIONAL
        :type device_index: ``int``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: The error message retrieved from the queue
        :rtype: ``ErrorCodes``
        """
        feature_4521_index, feature_4521, device_index, port_index = DisableKeysUtils.HIDppHelper.get_parameters(
            self, DisableKeys.FEATURE_ID, DisableKeysFactory, device_index, port_index)

        set_disabled_keys_request = feature_4521.set_disabled_keys_cls(device_index=device_index,
                                                                       feature_index=feature_4521_index,
                                                                       keys_to_disable=keys_to_disable)

        set_disabled_keys_request.functionIndex = function_index

        return ChannelUtils.send(test_case=self,
                                 report=set_disabled_keys_request,
                                 response_queue_name=HIDDispatcher.QueueName.ERROR,
                                 response_class_type=ErrorCodes)

    # end def set_disable_key_with_function_index

    def disable_key_with_unsupported_disableable_key(self, unsupported_key, device_index=None, port_index=None):
        """
        Send SetDisabledKeys with unsupported keys. This could be used for unsupported disableable key test

        :param unsupported_key: Value of disabled key that do not support by the feature
        :type unsupported_key: ``int``
        :param device_index: Device index - OPTIONAL
        :type device_index: ``int``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: The error message retrieved from the queue
        :rtype: ``ErrorCodes``
        """
        feature_4521_index, feature_4521, device_index, port_index = DisableKeysUtils.HIDppHelper.get_parameters(
            self, DisableKeys.FEATURE_ID, DisableKeysFactory, device_index, port_index)

        set_disabled_keys_request = feature_4521.set_disabled_keys_cls(device_index=device_index,
                                                                       feature_index=feature_4521_index,
                                                                       keys_to_disable=unsupported_key)

        return ChannelUtils.send(test_case=self,
                                 report=set_disabled_keys_request,
                                 response_queue_name=HIDDispatcher.QueueName.ERROR,
                                 response_class_type=ErrorCodes)
    # end def disable_key_with_unsupported_disableable_key
# end class DisableKeysErrorHandlingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
