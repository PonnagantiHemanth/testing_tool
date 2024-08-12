#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4522.interface
:brief: HID++ 2.0 DisableKeysByUsage interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysbyusageutils import DisableKeysByUsageTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4522.disablekeysbyusage import DisableKeysByUsageBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysByUsageInterfaceTestCase(DisableKeysByUsageBaseTestCase):
    """
    x4522 - Disable keys by usage interface test case
    """
    @features('Feature4522')
    @level('Interface')
    def test_get_capabilities_api(self):
        """
        Validates getCapabilities basic processing (Feature 0x4522)
        maxDisabledUsages [0]getCapabilities
        """

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getCapabilities request and wait response')
        # ---------------------------------------------------------------------------
        get_capabilities_response = DisableKeysByUsageTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetCapabilities.maxDisabledUsages byte[0] in range')
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.GetCapabilitiesResponseChecker.check_fields(
            self, get_capabilities_response, self.feature_4522.get_capabilities_response_cls)

        self.testCaseChecked("INT_4522_0001")
    # end def test_get_capabilities_api

    @features('Feature4522')
    @level('Interface')
    def test_disable_keys_api(self):
        """
        Validates disableKeys basic processing (Feature 0x4522)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send disableKeys request")
        # ---------------------------------------------------------------------------
        disable_keys_resp = DisableKeysByUsageTestUtils.HIDppHelper.disable_keys(test_case=self, keys=[0])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
                                                            test_case=self,
                                                            messages=disable_keys_resp,
                                                            expected_cls=self.feature_4522.disable_keys_response_cls)

        self.testCaseChecked("INT_4522_0002")
    # end def test_disable_keys_api

    @features('Feature4522')
    @level('Interface')
    def test_enable_keys_api(self):
        """
        Validates enableKeys basic processing (Feature 0x4522)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send enableKeys request")
        # ---------------------------------------------------------------------------
        enable_keys_resp = DisableKeysByUsageTestUtils.HIDppHelper.enable_keys(test_case=self, keys=[0])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableKeysResponseChecker.check_enable_keys_responses(
                                                        test_case=self,
                                                        messages=enable_keys_resp,
                                                        expected_cls=self.feature_4522.enable_keys_response_cls)

        self.testCaseChecked("INT_4522_0003")
    # end def test_enable_keys_api

    @features('Feature4522')
    @level('Interface')
    def test_enable_all_keys_api(self):
        """
        Validates enableAllKeys basic processing (Feature 0x4522)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send enableAllKeys request")
        # ---------------------------------------------------------------------------
        enable_all_keys_resp = DisableKeysByUsageTestUtils.HIDppHelper.enable_all_keys(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check enableAllKeys response fields")
        # ---------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.EnableAllKeysResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=enable_all_keys_resp,
                                                        expected_cls=self.feature_4522.enable_all_keys_response_cls)

        self.testCaseChecked("INT_4522_0004")
    # end def test_enable_all_keys_api
# end class DisableKeysByUsageInterfaceTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
