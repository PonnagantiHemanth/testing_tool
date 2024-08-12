#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4521.interface
:brief: HID++ 2.0 DisableKeys interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/12/07
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysutils import DisableKeysUtils
from pytestbox.device.hidpp20.keyboard.feature_4521.disablekeys import DisableKeysBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysInterfaceTestCase(DisableKeysBaseTestCase):
    """
    0x4521 DisableKeys interface test case
    """
    @features('Feature4521')
    @level('Interface')
    def test_get_capabilities_api(self):
        """
        Validate GetCapabilities basic processing (Feature 0x4521)

        disableableKeys [0]GetCapabilities
        """

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetCapabilities request and wait response')
        # ---------------------------------------------------------------------------
        get_capabilities_response = DisableKeysUtils.HIDppHelper.get_capabilities(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetCapabilities.disableableKeys value is equal to product default settings')
        # ---------------------------------------------------------------------------
        DisableKeysUtils.GetCapabilitiesResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=get_capabilities_response,
                                                        expected_cls=self.feature_4521.get_capabilities_response_cls)

        self.testCaseChecked('INT_4521_0001')
    # end def test get_capabilities

    @features('Feature4521')
    @level('Interface')
    def test_get_disabled_keys_api(self):
        """
        Validate GetDisabledKeys API basic processing

        disabledKeys [1]GetDisabledKeys
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDisabledKeys request and wait response')
        # ---------------------------------------------------------------------------
        get_disabled_keys_response = DisableKeysUtils.HIDppHelper.get_disabled_keys(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate GetCapabilities.disabledKeys value is equal to 0x00')
        # ---------------------------------------------------------------------------
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=get_disabled_keys_response,
                                                        expected_cls=self.feature_4521.get_disabled_keys_response_cls)

        self.testCaseChecked('INT_4521_0002')
    # end def test_get_disabled_keys_api

    @features('Feature4521')
    @level('Interface')
    def test_set_disabled_keys_api(self):
        """
        Validate SetDisabledKeys API basic processing

        disabledKeys [2]SetDisabledKeys
        """
        keys_to_disable = 0x00

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetDisabledKeys request and wait response')
        # ---------------------------------------------------------------------------
        set_disabled_keys_response = DisableKeysUtils.HIDppHelper.set_disabled_keys(test_case=self,
                                                                                    keys_to_disable=keys_to_disable)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(
            self, f'Validate GetCapabilities.disabledKeys value is equal to {keys_to_disable}')
        # ---------------------------------------------------------------------------
        check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                        keys_to_disable=keys_to_disable)
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=set_disabled_keys_response,
                                                        expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                        check_map=check_map)

        self.testCaseChecked('INT_4521_0003')
    # end def test_set_disabled_keys_api
# end class DisableKeysInterfaceTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
