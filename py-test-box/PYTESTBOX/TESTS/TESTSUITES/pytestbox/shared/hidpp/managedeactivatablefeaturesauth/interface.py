#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.managedeactivatablefeaturesauth.interface
:brief: Manage deactivatable features (based on authentication) interface test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.managedeactivatablefeaturesauth import \
    SharedManageDeactivatableFeaturesAuthTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedManageDeactivatableFeaturesAuthInterfaceTestCase(SharedManageDeactivatableFeaturesAuthTestCase, ABC):
    """
    Validate Manage deactivatable features (based on authentication) interface TestCases
    """
    @features('ManageDeactivatableFeaturesAuth')
    @level('Interface')
    def test_get_info_api(self):
        """
        Validates getInfo API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getInfo request')
        # --------------------------------------------------------------------------------------------------------------
        get_info_resp = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check getInfo response fields')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.GetInfoResponseChecker.check_fields(
            self,
            get_info_resp,
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_feature_interface(
                test_case=self).get_info_response_cls)

        self.testCaseChecked("INT_MAN_DEACT_FEAT_0001")
    # end def test_get_info_api

    @features('ManageDeactivatableFeaturesAuth')
    @level('Interface')
    def test_disable_features_api(self):
        """
        Validate disableFeatures API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disableFeatures request')
        # --------------------------------------------------------------------------------------------------------------
        disable_features_resp = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check disableFeatures response fields')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.MessageChecker.check_fields(
            self,
            disable_features_resp,
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_feature_interface(
                test_case=self).disable_features_response_cls,
            {})

        self.testCaseChecked("INT_MAN_DEACT_FEAT_0002")
    # end def test_disable_features_api

    @features('ManageDeactivatableFeaturesAuth')
    @level('Interface')
    def test_enable_features_api(self):
        """
        Validate enableFeatures API
        """
        config = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start sessions')
        # --------------------------------------------------------------------------------------------------------------
        if config.F_SupportManufacturing:
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value)
        # end if
        if config.F_SupportCompliance:
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value)
        # end if
        if config.F_SupportGotthard:
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.GOTHARD.value)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send enableFeatures request')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER
        enable_features_resp = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(
            self, start_session=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check enableFeatures response fields')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.MessageChecker.check_fields(
            self, enable_features_resp,
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_feature_interface(
                test_case=self).enable_features_response_cls,
            {})

        self.testCaseChecked("INT_MAN_DEACT_FEAT_0003")
    # end def test_enable_features_api
# end class SharedManageDeactivatableFeaturesAuthInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
