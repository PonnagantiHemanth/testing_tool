#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.managedeactivatablefeaturesauth.robustness
:brief: Manage deactivatable features (based on authentication) robustness test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/03/31
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.managedeactivatablefeaturesauth import \
    SharedManageDeactivatableFeaturesAuthTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class SharedManageDeactivatableFeaturesAuthRobustnessTestCase(SharedManageDeactivatableFeaturesAuthTestCase, ABC):
    """
    Validate Manage deactivatable features (based on authentication) robustness TestCases
    """
    _disable_not_supported_bits_expected_error_codes = None
    _enable_no_opened_session_does_not_enable_expected_error_codes = None
    _enable_no_opened_session_does_not_disable_expected_error_codes = None
    _enable_not_supported_bits_expected_error_codes = None
    _enable_features_closes_session = None

    @features('ManageDeactivatableFeaturesAuth')
    @level('Robustness')
    def test_disable_not_supported_bits(self):
        """
        Send disableFeatures for each bit set to 0 in the getInfo.supportBitMap
        """
        for bit_pos in range(ManageDeactivatableFeaturesAuth.BitMap.LEN.RESERVED):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send disableFeatures request')
            # ----------------------------------------------------------------------------------------------------------
            request = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_disable_features_req(self)
            request.disable_bit_map.reserved = 1 << bit_pos

            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.send_report_wait_error(
                self, request, error_codes=self._disable_not_supported_bits_expected_error_codes)
        # end for

        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0001")
    # end def test_disable_not_supported_bits

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Robustness')
    def test_enable_no_opened_session_does_not_enable(self):
        """
        Do not open any session and send enableFeatures for each bit in the bit map
        """
        self.post_requisite_reload_nvs = True

        use_cases = [{"all_bit": True, "gotthard": False, "compliance": False, "manufacturing": False}]
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportManufacturing:
            use_cases.append({"all_bit": False, "gotthard": False, "compliance": False, "manufacturing": True})
        # end if
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportCompliance:
            use_cases.append({"all_bit": False, "gotthard": False, "compliance": True, "manufacturing": False})
        # end if
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportGotthard:
            use_cases.append({"all_bit": False, "gotthard": True, "compliance": False, "manufacturing": False})
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Activate Features')
        # --------------------------------------------------------------------------------------------------------------
        self.TestUtilsFacade.HIDppHelper.activate_features(self)

        for use_case in use_cases:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send enableFeatures request')
            # ----------------------------------------------------------------------------------------------------------
            request = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_enable_features_req(
                self,
                enable_all=use_case["all_bit"],
                gotthard=use_case["gotthard"],
                compliance=use_case["compliance"],
                manufacturing=use_case["manufacturing"]
            )

            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.send_report_wait_error(
                self, request, error_codes=self._enable_no_opened_session_does_not_enable_expected_error_codes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check all features are disabled (get info state)')
            # ----------------------------------------------------------------------------------------------------------
            expected = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False, compliance=False, gothard=False)
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected)
        # end for

        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0002")
    # end def test_enable_no_opened_session_does_not_enable

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Robustness')
    def test_enable_no_opened_session_does_not_disable(self):
        """
        Do not open any session and send enableFeatures for each bit in the bit map
        """
        self.post_requisite_reload_nvs = True

        use_cases = [{"all_bit": True, "gotthard": False, "compliance": False, "manufacturing": False}]
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportManufacturing:
            use_cases.append({"all_bit": False, "gotthard": False, "compliance": False, "manufacturing": True})
        # end if
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportCompliance:
            use_cases.append({"all_bit": False, "gotthard": False, "compliance": True, "manufacturing": False})
        # end if
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportGotthard:
            use_cases.append({"all_bit": False, "gotthard": True, "compliance": False, "manufacturing": False})
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, enable_all=True)

        for use_case in use_cases:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send enableFeatures request')
            # ----------------------------------------------------------------------------------------------------------
            request = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_enable_features_req(
                self,
                enable_all=use_case["all_bit"],
                gotthard=use_case["gotthard"],
                compliance=use_case["compliance"],
                manufacturing=use_case["manufacturing"])

            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.send_report_wait_error(
                self, request, error_codes=self._enable_no_opened_session_does_not_disable_expected_error_codes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check all features are enabled (get info state)')
            # ----------------------------------------------------------------------------------------------------------
            expected = ManageDeactivatableFeaturesAuth.BitMap(
                manufacturing=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportManufacturing,
                compliance=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportCompliance,
                gothard=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportGotthard)
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected)
        # end for

        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0003")
    # end def test_enable_no_opened_session_does_not_disable

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Robustness')
    def test_enable_not_supported_bits(self):
        """
        Open all possible sessions and send enableFeatures for each bit set to 0 in the getInfo.supportBitMap
        """
        for bit_pos in range(ManageDeactivatableFeaturesAuth.BitMap.LEN.RESERVED):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Open all sessions')
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value)
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value)
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.GOTHARD.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send enableFeatures request')
            # ----------------------------------------------------------------------------------------------------------
            request = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_enable_features_req(
                self, enable_all=False, gotthard=False, compliance=False, manufacturing=False)
            request.enable_bit_map.reserved = 1 << bit_pos

            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.send_report_wait_error(
                self, request, error_codes=self._enable_not_supported_bits_expected_error_codes)
        # end for

        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0004")
    # end def test_enable_not_supported_bits

    @features('ManageDeactivatableFeaturesAuth')
    @level('Robustness')
    def test_disable_features_padding_ignored(self):
        """
        Padding bytes shall be ignored by the firmware
        """
        request = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_disable_features_req(self)
        for padding in compute_sup_values(HexList(Numeral(request.DEFAULT.PADDING, request.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send disableFeatures request with padding different from zero')
            # ----------------------------------------------------------------------------------------------------------
            request.padding = padding

            disable_features_resp = self.send_report_wait_response(
                report=request,
                response_queue=self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.feature_response_queue(self),
                response_class_type=self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_feature_interface(
                    test_case=self).disable_features_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check disableFeatures response fields')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.MessageChecker.check_fields(
                self,
                disable_features_resp,
                self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_feature_interface(
                    test_case=self).disable_features_response_cls,
                {})
        # end for
        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0007")
    # end def test_disable_features_padding_ignored

    @features('ManageDeactivatableFeaturesAuth')
    @level('Robustness')
    def test_enable_features_padding_ignored(self):
        """
        Padding bytes shall be ignored by the firmware
        """
        request = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_enable_features_req(self)
        config = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH

        for padding in compute_sup_values(HexList(Numeral(request.DEFAULT.PADDING, request.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start sessions')
            # ----------------------------------------------------------------------------------------------------------
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

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send enableFeatures request with padding different from zero')
            # ----------------------------------------------------------------------------------------------------------
            request = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_enable_features_req(
                self, enable_all=False, gotthard=False, compliance=False, manufacturing=False)
            request.padding = padding

            enable_features_resp = self.send_report_wait_response(
                report=request,
                response_queue=self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.feature_response_queue(self),
                response_class_type=self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_feature_interface(
                    test_case=self).enable_features_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check enableFeatures response fields')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.MessageChecker.check_fields(
                self, enable_features_resp,
                self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_feature_interface(
                    test_case=self).enable_features_response_cls,
                {})
        # end for
        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0008")
    # end def test_enable_features_padding_ignored

    @features('ManageDeactivatableFeaturesAuth')
    @level('Robustness')
    def test_enable_features_closes_session(self):
        """
        Check each write operation requires a new authentication
        """
        use_cases = []
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportManufacturing:
            use_cases.append({"gotthard": False, "compliance": False, "manufacturing": True})
        # end if
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportCompliance:
            use_cases.append({"gotthard": False, "compliance": True, "manufacturing": False})
        # end if
        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportGotthard:
            use_cases.append({"gotthard": True, "compliance": False, "manufacturing": False})
        # end if

        for use_case in use_cases:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enable features')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(
                self,
                manufacturing=use_case["manufacturing"],
                compliance=use_case["compliance"],
                gotthard=use_case["gotthard"])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send enableFeatures request')
            # ----------------------------------------------------------------------------------------------------------
            request = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_enable_features_req(
                self,
                gotthard=use_case["gotthard"],
                compliance=use_case["compliance"],
                manufacturing=use_case["manufacturing"]
            )

            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.send_report_wait_error(
                self, request, error_codes=self._enable_features_closes_session)
        # end for
        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0011")
    # end def test_enable_features_closes_session
# end class SharedManageDeactivatableFeaturesAuthRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
