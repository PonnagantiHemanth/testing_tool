#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1e02.robustness
:brief: HID++ 2.0 Manage deactivatable features (based on authentication) robustness test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1e02.managedeactivatablefeaturesauth import \
    DeviceManageDeactivatableFeaturesAuthTestCase
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.robustness import \
    SharedManageDeactivatableFeaturesAuthRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceManageDeactivatableFeaturesAuthRobustnessTestCase(
        DeviceManageDeactivatableFeaturesAuthTestCase, SharedManageDeactivatableFeaturesAuthRobustnessTestCase):
    """
    Validate the 'manage deactivatable features' mechanism (based on password authentication) robustness test cases
    with a device as a DUT
    """
    _disable_not_supported_bits_expected_error_codes = [Hidpp2ErrorCodes.INVALID_ARGUMENT]
    _enable_no_opened_session_does_not_enable_expected_error_codes = [Hidpp2ErrorCodes.NOT_ALLOWED]
    _enable_no_opened_session_does_not_disable_expected_error_codes = [Hidpp2ErrorCodes.NOT_ALLOWED]
    _enable_not_supported_bits_expected_error_codes = [Hidpp2ErrorCodes.INVALID_ARGUMENT]
    _enable_features_closes_session = [Hidpp2ErrorCodes.NOT_ALLOWED]

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Robustness')
    def test_wrong_session(self):
        """
        Open all possible sessions except one and send enableFeatures for the not opened session.
        """
        use_cases = [
            {"gotthard": False, "compliance": False, "manufacturing": True},
            {"gotthard": False, "compliance": True, "manufacturing": False},
            {"gotthard": True, "compliance": False, "manufacturing": False},
        ]

        for use_case in use_cases:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Open all possible sessions except one')
            # ----------------------------------------------------------------------------------------------------------
            if not use_case["manufacturing"]:
                self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                    test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value)
            # end if
            if not use_case["compliance"]:
                self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                    test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value)
            # end if
            if not use_case["gotthard"]:
                self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                    test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.GOTHARD.value)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send enableFeatures request related to the not opened session')
            # ----------------------------------------------------------------------------------------------------------
            enable_features_req = self.feature_1e02.enable_features_cls(
                self.deviceIndex,
                self.feature_1e02_index,
                enable_all_bit=False,
                enable_gothard=use_case["manufacturing"],
                enable_compliance=use_case["compliance"],
                enable_manufacturing=use_case["gotthard"])

            err_resp = self.send_report_wait_response(
                report=enable_features_req,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_NOT_ALLOWED (5) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=enable_features_req.featureIndex,
                function_index=enable_features_req.functionIndex,
                error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])
        # end for

        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0005")
    # end def test_wrong_session

    @features('ManageDeactivatableFeaturesAuth')
    @level('Robustness')
    def test_get_info_padding_ignored(self):
        """
        Padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1e02.get_info_cls.DEFAULT.PADDING,
                                                          self.feature_1e02.get_info_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getInfo request with padding different from zero')
            # ----------------------------------------------------------------------------------------------------------
            get_info_req = self.feature_1e02.get_info_cls(self.deviceIndex, self.feature_1e02_index)
            get_info_req.padding = padding

            get_info_resp = self.send_report_wait_response(
                report=get_info_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1e02.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getInfo response fields')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.GetInfoResponseChecker.check_fields(
                self, get_info_resp, self.feature_1e02.get_info_response_cls)
        # end for
        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0006")
    # end def test_get_info_padding_ignored

    @features('ManageDeactivatableFeaturesAuth')
    @level('Robustness')
    def test_get_react_info_padding_ignored(self):
        """
        Padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1e02.get_reactivation_info_cls.DEFAULT.PADDING,
                                                          self.feature_1e02.get_reactivation_info_cls.LEN.PADDING // 8)
                                                  )):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getReactInfo request')
            # ----------------------------------------------------------------------------------------------------------
            get_react_info_req = self.feature_1e02.get_reactivation_info_cls(self.deviceIndex, self.feature_1e02_index)
            get_react_info_req.padding = padding

            get_react_info_resp = self.send_report_wait_response(
                report=get_react_info_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1e02.get_reactivation_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check response fields')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.GetReactInfoResponseChecker.check_fields(
                self, get_react_info_resp, self.feature_1e02.get_reactivation_info_response_cls)
        # end for

        self.testCaseChecked("ROT_MAN_DEACT_FEAT_0009")
    # end def test_get_react_info_padding_ignored

    @features('ManageDeactivatableFeaturesAuth')
    @level('Robustness')
    def test_function_index_out_of_range(self):
        """
        Check function index out of range return error.
        """
        for function_index in compute_wrong_range(value=list(range(self.feature_1e02.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send request with function index out of range')
            # ----------------------------------------------------------------------------------------------------------
            request = self.feature_1e02.get_info_cls(self.deviceIndex, self.feature_1e02_index)
            request.functionIndex = function_index

            err_resp = self.send_report_wait_response(
                report=request,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=Hidpp2ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_ARGUMENT (2) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
                test_case=self,
                error_message=err_resp,
                feature_index=request.featureIndex,
                function_index=request.functionIndex,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID])
        # end for

        self.testCaseChecked("ROB_MAN_DEACT_FEAT_0010")
    # end def test_function_index_out_of_range
# end class ManageDeactivatableFeaturesAuthRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
