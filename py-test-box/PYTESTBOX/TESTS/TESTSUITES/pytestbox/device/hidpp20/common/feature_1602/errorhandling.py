#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1602.errorhandling
:brief: HID++ 2.0 ``PasswordAuthentication`` error handling test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.powermodes import PowerModes
from pyhid.hidpp.features.common.powermodes import PowerModesFactory
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.common.feature_1602.passwordauthentication import DevicePasswordAuthenticationTestCase
from pytestbox.shared.hidpp.passwordauthentication.errorhandling import \
    SharedPasswordAuthenticationErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_LONG_PWD_WARNING = "Long password must be supported for this device. Check the settings or decorator"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class DevicePasswordAuthenticationErrorHandlingTestCase(SharedPasswordAuthenticationErrorHandlingTestCase,
                                                        DevicePasswordAuthenticationTestCase):
    """
    Validate ``PasswordAuthentication`` errorhandling test cases
    """
    _test_sending_password_without_started_session_expected_error_codes = [ErrorCodes.NOT_ALLOWED]
    _test_session_if_no_authentication_expected_error_codes = [ErrorCodes.NOT_ALLOWED]
    _test_session_is_closed_when_device_is_reset_expected_error_codes = [ErrorCodes.NOT_ALLOWED]
    _test_start_session_request_for_an_already_open_session_expected_error_codes = [ErrorCodes.NOT_ALLOWED]
    _test_start_session_with_wrong_authentication_expected_error_codes = [ErrorCodes.NOT_ALLOWED]
    _test_start_session_with_wrong_name_expected_error_codes = [ErrorCodes.INVALID_ARGUMENT]

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesSupportManufacturing")
    @level("ErrorHandling")
    @services("Debugger")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        account_name = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(
                value=list(range(self.feature_1602.get_max_function_index() + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1602.start_session_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1602_index,
                account_name=account_name)
            report.functionIndex = function_index
            self.PasswordAuthenticationTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self, report=report, error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_PWD_AUTH_0008", _AUTHOR)
    # end def test_wrong_function_index

    @features("PasswordAuthentication")
    @features("ManageDeactivatableFeaturesAuth")
    @features("ManageDeactivatableFeaturesSupportCompliance")
    @level("ErrorHandling")
    @services("Debugger")
    def test_a_session_in_the_authentication_phase(self):
        """
        Validate that a session in the authentication phase is immediately aborted if a new session is started
        """
        self.post_requisite_reload_nvs = True
        account_name_manf = self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value
        account_name_compl = self.PasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send StartSession request for {account_name_manf}")
        # --------------------------------------------------------------------------------------------------------------
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
            test_case=self, account_name=account_name_manf)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name_manf}")
        # --------------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
        checker.check_fields(self, response, self.PasswordAuthenticationTestUtils.HIDppHelper.
                             get_feature_interface(test_case=self).start_session_response_cls)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Passwd0 request for {account_name_compl}")
        # ----------------------------------------------------------------------------------------------------------
        passwd0 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_from_name(
            account_name=account_name_compl)
        response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(test_case=self, passwd=HexList(passwd0))

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name_compl}")
        # ----------------------------------------------------------------------------------------------------------
        checker = self.PasswordAuthenticationTestUtils.PasswordResponseChecker
        check_map = checker.get_default_check_map(self)
        status = HexList(self.PasswordAuthenticationTestUtils.Status.FAILURE.value)
        check_map.update({
            "status": (checker.check_status, status)
        })
        checker.check_fields(
            self, response,
            self.PasswordAuthenticationTestUtils.HIDppHelper.get_feature_interface(self).passwd0_response_cls,
            check_map)

        self.testCaseChecked("ERR_PWD_AUTH_0009", _AUTHOR)
    # end def test_a_session_in_the_authentication_phase

    @features("PasswordAuthentication")
    @features("Feature1830powerMode", 3)
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_session_is_closed_when_underlying_transport_channel_is_terminated(self):
        """
        Validate that session is closed when underlying transport channel is terminated
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get Feature 0x1830 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1830_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=PowerModes.FEATURE_ID)
        self.feature_1830 = PowerModesFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.POWER_MODES))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get Feature 0x1E00 index")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_hidden_feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=GetEnableHiddenFeatures.FEATURE_ID)

        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the response")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            checker.check_fields(self, response, self.feature_1602.start_session_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Authenticate and validate")
            # ----------------------------------------------------------------------------------------------------------
            self.PasswordAuthenticationTestUtils.HIDppHelper.authenticate_and_validate(
                test_case=self, start_session_response=response, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetPowerMode with powerModeNumber = 3")
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait for 5 seconds")
            # ----------------------------------------------------------------------------------------------------------
            sleep(5)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wake up the device over emulator(key press/mouse click)")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
            sleep(0.3)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Read hidden feature status")
            # ----------------------------------------------------------------------------------------------------------
            report = GetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(test_case=self),
                                             feature_index=self.enable_hidden_feature_id)
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=GetEnableHiddenFeaturesResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate Hidden Feature is disabled to ensure power mode changes")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=EnableHidden.DISABLED,
                             obtained=to_int(response.enableByte),
                             msg="The enableByte parameter has not been reset")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable hidden features")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send EnableFeatures to enable respective feature")
            # ----------------------------------------------------------------------------------------------------------
            manufacturing, compliance, gotthard = self.PasswordAuthenticationTestUtils.get_all_account_name_values(
                account_name=account_name.value)
            report = self.feature_1e02.enable_features_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e02_index,
                enable_all_bit=False,
                enable_manufacturing=manufacturing,
                enable_compliance=compliance,
                enable_gothard=gotthard)
            self.PasswordAuthenticationTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.NOT_ALLOWED])
        # end for

        self.testCaseChecked("ERR_PWD_AUTH_0010", _AUTHOR)
    # end def test_session_is_closed_when_underlying_transport_channel_is_terminated

    @features("PasswordAuthentication")
    @level("ErrorHandling")
    def test_end_session_request(self):
        """
        Validate that endSession request can be sent even if no session was opened and that it doesn't open a session
        """
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
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

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            passwd0 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_from_name(
                account_name=account_name.value)
            report = self.feature_1602.passwd0_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1602_index,
                passwd=HexList(passwd0))
            self.PasswordAuthenticationTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self, report=report, error_codes=[ErrorCodes.NOT_ALLOWED])
        # end for

        self.testCaseChecked("ERR_PWD_AUTH_0011", _AUTHOR)
    # end def test_end_session_request

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationLongPassword")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_both_password_functions_sent(self):
        """
        Validate that both passwd functions shall be sent if long_password flag is set and the password is null
        terminated in passwd0
        """
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Enable hidden features")
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

            passwd0, _ = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_and_password1_from_name(
                account_name=account_name.value)

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
            LogHelper.log_step(self, "Enable respective features")
            # ----------------------------------------------------------------------------------------------------------
            manufacturing, compliance, gotthard = self.PasswordAuthenticationTestUtils.get_all_account_name_values(
                account_name=account_name.value)
            report = self.feature_1e02.enable_features_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1e02_index,
                enable_all_bit=False,
                enable_manufacturing=manufacturing,
                enable_compliance=compliance,
                enable_gothard=gotthard)
            self.PasswordAuthenticationTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self, report=report, error_codes=[ErrorCodes.NOT_ALLOWED])
        # end for

        self.testCaseChecked("ERR_PWD_AUTH_0012", _AUTHOR)
    # end def test_both_password_functions_sent

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationLongPassword")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_only_the_last_function_returns_failure_status_password0(self):
        """
        Validate that only the last function returns a failure status, if failure occurs in passwd0, in case of long
        password
        """
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            checker.check_fields(self, response, self.feature_1602.start_session_response_cls)

            if not response.long_password:
                warnings.warn(_LONG_PWD_WARNING)
                return
            # end if

            passwd0 = "01020304050607080910111213141516"
            _, passwd1 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_and_password1_from_name(
                account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value} with wrong password")
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
            LogHelper.log_step(self, f"Send Passwd1 request for {account_name.value} with valid password")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd1(
                test_case=self, passwd=HexList(passwd1))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd1Response fields for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.FAILURE.value)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd1_response_cls, check_map)
        # end for

        self.testCaseChecked("ERR_PWD_AUTH_0013", _AUTHOR)
    # end def test_only_the_last_function_returns_failure_status_password0

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationLongPassword")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_only_the_last_function_returns_failure_status_password1(self):
        """
        Validate that only the last function returns a failure status, if failure occurs in passwd1, in case of long
        password
        """
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            checker.check_fields(self, response, self.feature_1602.start_session_response_cls)

            if not response.long_password:
                warnings.warn(_LONG_PWD_WARNING)
                return
            # end if

            passwd0, _ = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_and_password1_from_name(
                account_name=account_name.value)
            passwd1 = "17181920212223242526272829303132"

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value} with valid password")
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
            LogHelper.log_step(self, f"Send Passwd1 request for {account_name.value} with invalid password")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd1(
                test_case=self, passwd=HexList(passwd1))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd1Response fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.FAILURE.value)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd1_response_cls, check_map)
        # end for

        self.testCaseChecked("ERR_PWD_AUTH_0014", _AUTHOR)
    # end def test_only_the_last_function_returns_failure_status_password1

    @features("PasswordAuthentication")
    @features("PasswordAuthenticationLongPassword")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level("ErrorHandling")
    @services("Debugger")
    def test_only_the_last_function_returns_failure_status(self):
        """
        Validate that only the last function returns a failure status, if failure occurs in passwd1 and passwd1 is
        sent before passwd0, in case of long password
        """
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            checker.check_fields(self, response, self.feature_1602.start_session_response_cls)

            if not response.long_password:
                warnings.warn(_LONG_PWD_WARNING)
                return
            # end if

            passwd0, _ = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_and_password1_from_name(
                account_name=account_name.value)
            passwd1 = "17181920212223242526272829303132"

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd1 request for {account_name.value} with invalid password")
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
            LogHelper.log_step(self, f"Send Passwd0 request for {account_name.value} with valid password")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.passwd0(
                test_case=self, passwd=HexList(passwd0))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check Passwd0Response fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            status = HexList(self.PasswordAuthenticationTestUtils.Status.FAILURE.value)
            check_map.update({
                "status": (checker.check_status, status)
            })
            checker.check_fields(self, response, self.feature_1602.passwd0_response_cls, check_map)
        # end for

        self.testCaseChecked("ERR_PWD_AUTH_0015", _AUTHOR)
    # end def test_only_the_last_function_returns_failure_status

    @features("PasswordAuthentication")
    @features("NoPasswordAuthenticationLongPassword")
    @level("Interface")
    def test_passwd1_not_allowed_for_short_password(self):
        """
        Validate ``Passwd1`` interface for short password
        """
        self.post_requisite_reload_nvs = True
        for account_name in self.PasswordAuthenticationTestUtils.AccountNames:
            if not self.PasswordAuthenticationTestUtils.is_supported(self, account_name):
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartSession request for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            response = self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
                test_case=self, account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check StartSessionResponse fields for {account_name.value}")
            # ----------------------------------------------------------------------------------------------------------
            checker = self.PasswordAuthenticationTestUtils.StartSessionResponseChecker
            checker.check_fields(self, response, self.feature_1602.start_session_response_cls)

            if response.long_password:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Hence {account_name.value} supports long_password, continue next")
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            _, passwd1 = self.PasswordAuthenticationTestUtils.HIDppHelper.get_password0_and_password1_from_name(
                account_name=account_name.value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Passwd1 request for {account_name}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1602.passwd1_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1602_index,
                passwd=HexList(passwd1))
            self.PasswordAuthenticationTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self, report=report, error_codes=[ErrorCodes.NOT_ALLOWED])
        # end for

        self.testCaseChecked("ERR_PWD_AUTH_0016", _AUTHOR)
    # end def test_passwd1_not_allowed_for_short_password
# end class DevicePasswordAuthenticationErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
