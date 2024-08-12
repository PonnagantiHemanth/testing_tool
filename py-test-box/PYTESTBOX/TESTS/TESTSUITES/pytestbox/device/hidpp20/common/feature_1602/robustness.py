#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1602.robustness
:brief: HID++ 2.0 ``PasswordAuthentication`` robustness test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_inf_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_1602.passwordauthentication import DevicePasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.robustness import SharedPasswordAuthenticationRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_ENABLE_FEATURES_0X1E02_MANUF = "Send EnableFeatures to enable x1E02_Manuf feature"
_ENABLE_HIDDEN_FEATURES = "Enable hidden features"
_ENABLE_RESPECTIVE_FEATURES = "Send EnableFeatures to enable respective feature"
_LONG_PWD_WARNING = "Long password must be supported for this device. Check the settings or decorator"
_LOOP_END = "End Test Loop"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class DevicePasswordAuthenticationRobustnessTestCase(SharedPasswordAuthenticationRobustnessTestCase,
                                                     DevicePasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` robustness test cases
    """
    _test_service_is_closed_when_underlying_transport_channel_is_terminated_err_codes = [ErrorCodes.NOT_ALLOWED]

    @features("PasswordAuthentication")
    @level("Robustness")
    @services("Debugger")
    def test_start_and_end_session_software_id(self):
        """
        Validate ``StartSession | EndSession`` software id field is ignored by the firmware

        [0] startSession(accountName) -> longPassword, fullAuthentication, constantCredentials

        [1] endSession(accountName) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.AccountName

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PasswordAuthentication.DEFAULT.SOFTWARE_ID):
            for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
                if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                    continue
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send StartSession request for {account_name.value}"
                                         f" with software_id: {software_id}")
                # ------------------------------------------------------------------------------------------------------
                response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                    test_case=self,
                    account_name=account_name.value,
                    software_id=software_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
                check_map = checker.get_default_check_map(self)
                checker.check_fields(self, response, self.feature_1602.start_session_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send EndSession request for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                response = self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
                    test_case=self,
                    account_name=account_name.value,
                    software_id=software_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check EndSessionResponse fields for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                self.PasswordAuthenticationTestUtils.MessageChecker.check_fields(
                    self, response, self.feature_1602.end_session_response_cls, {})
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_PWD_AUTH_0004", _AUTHOR)
        self.testCaseChecked("ROB_PWD_AUTH_0005", _AUTHOR)
    # end def test_start_and_end_session_software_id

    @features("PasswordAuthentication")
    @level("Robustness")
    @services("Debugger")
    def test_passwd0_software_id(self):
        """
        Validate ``Passwd0`` software id field is ignored by the firmware

        [2] passwd0(passwd) -> status

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Passwd

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PasswordAuthentication.DEFAULT.SOFTWARE_ID):
            for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
                if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                    continue
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                    test_case=self, account_name=account_name.value)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
                check_map = checker.get_default_check_map(self)
                checker.check_fields(self, response, self.feature_1602.start_session_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value}"
                                         f" with software_id: {software_id}")
                # ------------------------------------------------------------------------------------------------------
                passwd0 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_from_name(
                    account_name=account_name.value)
                response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
                    test_case=self, passwd=HexList(passwd0), software_id=software_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
                check_map = checker.get_default_check_map(self)
                checker.check_fields(self, response, self.feature_1602.passwd0_response_cls, check_map)
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_PWD_AUTH_0006", _AUTHOR)
    # end def test_passwd0_software_id

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationLongPassword")
    @level("Robustness")
    @services("Debugger")
    def test_passwd1_software_id(self):
        """
        Validate ``Passwd1`` software id field is ignored by the firmware

        [3] passwd1(passwd) -> status

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Passwd

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PasswordAuthentication.DEFAULT.SOFTWARE_ID):
            for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                    test_case=self, account_name=account_name.value)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
                check_map = checker.get_default_check_map(self)
                checker.check_fields(self, response, self.feature_1602.start_session_response_cls, check_map)

                if not response.long_password:
                    warnings.warn(_LONG_PWD_WARNING)
                    return
                # end if

                passwd0, passwd1 = self.PasswordAuthenticationTestUtils.HIDppHelper.\
                    get_password0_and_password1_from_name(account_name=account_name.value)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value}"
                                         f" with software_id: {software_id}")
                # ------------------------------------------------------------------------------------------------------
                response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
                    test_case=self, passwd=HexList(passwd0), software_id=software_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                status = HexList(self.PasswordAuthenticationTestUtils.Status.IN_PROGRESS.value)
                checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "status": (checker.check_status, status)
                })
                checker.check_fields(self, response, self.feature_1602.passwd0_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send Passwd1 request for {account_name.value}"
                                         f" with software_id: {software_id}")
                # ------------------------------------------------------------------------------------------------------
                response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd1(
                    test_case=self, passwd=HexList(passwd1), software_id=software_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Passwd1Response fields for {account_name.value}")
                # ------------------------------------------------------------------------------------------------------
                status = HexList(self.PasswordAuthenticationTestUtils.Status.SUCCESS.value)
                check_map.update({
                    "status": (checker.check_status, status)
                })
                checker.check_fields(self, response, self.feature_1602.passwd1_response_cls, check_map)
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_PWD_AUTH_0007", _AUTHOR)
    # end def test_passwd1_software_id

    @features("PasswordAuthentication")
    @level("Robustness")
    def test_end_session_account_names(self):
        """
        Validate that end session request for each known account name is successful
        """
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send EndSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check EndSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1602.end_session_response_cls, {})
        # end for

        self.testCaseChecked("ROB_PWD_AUTH_0008", _AUTHOR)
    # end def test_end_session_account_names

    @features("PasswordAuthentication")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @features("ManageDeactivatableFeaturesSupportManufacturing")
    @features("ManageDeactivatableFeaturesSupportCompliance")
    @level("Robustness")
    @services("Debugger")
    def test_ending_a_session_does_not_end_another(self):
        """
        Validate that ending a session does not end another session
        """
        account_name_manf = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        account_name_compl = self.PasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _ENABLE_HIDDEN_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send StartSession request for {account_name_manf}")
        # --------------------------------------------------------------------------------------------------------------
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
            test_case=self, account_name=account_name_manf)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name_manf}")
        # --------------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
        checker.check_fields(self, response, self.feature_1602.start_session_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send EndSession request for {account_name_compl}")
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
            test_case=self, account_name=account_name_compl)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Authenticate {account_name_manf} and validate")
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.authenticate_and_validate(
            test_case=self, start_session_response=response, account_name=account_name_manf)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _ENABLE_FEATURES_0X1E02_MANUF)
        # --------------------------------------------------------------------------------------------------------------
        self.ManageUtils.HIDppHelper.enable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check x1E02 state")
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True)
        self.ManageUtils.HIDppHelper.check_state(self, expected_state)

        self.testCaseChecked("ROB_PWD_AUTH_0009", _AUTHOR)
    # end def test_ending_a_session_does_not_end_another

    @features("PasswordAuthentication")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @features("ManageDeactivatableFeaturesSupportCompliance")
    @features("ManageDeactivatableFeaturesSupportManufacturing")
    @level("Robustness")
    @services("Debugger")
    def test_ending_a_session_does_not_end_another_authentication(self):
        """
        Validate that ending a session does not end another authenticated session
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _ENABLE_HIDDEN_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

        account_name_manf = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        account_name_compl = self.PasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value

        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
            test_case=self, account_name=account_name_manf)

        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session_and_authenticate(
            test_case=self, account_name=account_name_compl)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send EndSession request for {account_name_compl}")
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.end_session(
            test_case=self, account_name=account_name_compl)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _ENABLE_FEATURES_0X1E02_MANUF)
        # --------------------------------------------------------------------------------------------------------------
        self.ManageUtils.HIDppHelper.enable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check 0x1E02 state")
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True)
        self.ManageUtils.HIDppHelper.check_state(self, expected_state)

        self.testCaseChecked("ROB_PWD_AUTH_0010", _AUTHOR)
    # end def test_ending_a_session_does_not_end_another_authentication

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationLongPassword")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level("Robustness")
    @services("Debugger")
    def test_long_password(self):
        """
        Validate that password can be sent in any order for long password
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _ENABLE_HIDDEN_FEATURES)
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            manufacturing, compliance, gotthard = self.PasswordAuthenticationTestUtils.get_all_account_name_values(
                account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1602.start_session_response_cls, check_map)

            if not response.long_password:
                warnings.warn(_LONG_PWD_WARNING)
                return
            # end if

            passwd0, passwd1 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_and_password1_from_name(
                account_name=account_name)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
                test_case=self, passwd=HexList(passwd0))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.IN_PROGRESS.value)
            checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd0_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd1 request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd1(
                test_case=self, passwd=HexList(passwd1))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd1Response fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.SUCCESS.value)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd1_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _ENABLE_RESPECTIVE_FEATURES)
            # ----------------------------------------------------------------------------------------------------------
            self.ManageUtils.HIDppHelper.enable_features(self, manufacturing=manufacturing, compliance=compliance,
                                                         gotthard=gotthard)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check session is open for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(
                manufacturing=manufacturing, compliance=compliance, gothard=gotthard)
            self.ManageUtils.HIDppHelper.check_state(self, expected_state)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Force device reset")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _ENABLE_HIDDEN_FEATURES)
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_1602.start_session_response_cls, check_map)

            if not response.long_password:
                warnings.warn(_LONG_PWD_WARNING)
                return
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd1 request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd1(
                test_case=self, passwd=HexList(passwd1))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd1Response fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.IN_PROGRESS.value)
            checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd1_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
                test_case=self, passwd=HexList(passwd0))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.SUCCESS.value)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd0_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, _ENABLE_RESPECTIVE_FEATURES)
            # ----------------------------------------------------------------------------------------------------------
            self.ManageUtils.HIDppHelper.enable_features(self, manufacturing=manufacturing, compliance=compliance,
                                                         gotthard=gotthard)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check session is open for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(
                manufacturing=manufacturing, compliance=compliance, gothard=gotthard)
            self.ManageUtils.HIDppHelper.check_state(self, expected_state)
        # end for

        self.testCaseChecked("ROB_PWD_AUTH_0011", _AUTHOR)

        self.fail("Passwd1 not implemented yet")
    # end def test_long_password
# end class DevicePasswordAuthenticationRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
