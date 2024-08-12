# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package    pytestbox.hid.mouse.feature_2110_robustness
@brief      Validates HID mouse feature 0x2110 robustness test cases
@author     Fred Chen
@date       2019/08/21
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyhid.hidpp.features.mouse.smartshift import SmartShift
from pyhid.hidpp.features.mouse.smartshift import GetRatchetControlMode
from pyhid.hidpp.features.mouse.smartshift import GetRatchetControlModeResponse
from pyhid.hidpp.features.mouse.smartshift import SetRatchetControlMode
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pylibrary.tools.util import compute_inf_values
from pytestbox.device.hidpp20.mouse.feature_2110_interface import DONOTCHANGE
from pytestbox.device.hidpp20.mouse.feature_2110_interface import FREESPIN
from pytestbox.device.hidpp20.mouse.feature_2110_interface import RATCHET
from pytestbox.device.hidpp20.mouse.feature_2110_interface import SmartShiftBaseClassTestCase
from pytestbox.device.hidpp20.mouse.feature_2110_interface import get_ratchet_control_mode
from pytestbox.device.hidpp20.mouse.feature_2110_interface import set_ratchet_control_mode
from pytestbox.device.hidpp20.mouse.feature_2110_interface import verify_ratchet_control_mode


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SmartShiftRobustnessTestCase(SmartShiftBaseClassTestCase):
    """
    Validates SmartShift Robustness TestCases
    """

    @features('Feature2110')
    @level('Robustness')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetEngaged_IfChangeToRatchetModeAndWheelSpeedLessThanOldNewAutoDisengage(self):
        """
        @tc_synopsis Change ratchet mode and autoDisengage to another value than the one already in the device while
        the wheel is running and verify that the ratchet is engaged if speed below the old and new autoDisengage speed

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
        autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Send getRatchetControlMode to store the current configuration')
        # ---------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test=self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send setRatchetControlMode with wheelMode = 1 and other parameters to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test=self, wheel_mode=FREESPIN)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=FREESPIN)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Start wheel movement emulation with speed below '
                       f'{self.cur_settings.auto_disengage}')
        # ---------------------------------------------------------------------------
        # todo

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send setRatchetControlMode with wheelMode = 2, autoDisengage = '
                       f'{int(Numeral(self.cur_settings.auto_disengage)) + 10} and other parameters to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test=self, wheel_mode=RATCHET,
                                            auto_disengage=int(Numeral(self.cur_settings.auto_disengage))+10)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET,
                                    auto_disengage=int(Numeral(self.cur_settings.auto_disengage))+10)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate ratchet engaged Ratchet Spy')
        # ---------------------------------------------------------------------------
        # todo

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Stop wheel movement emulation')
        # ---------------------------------------------------------------------------
        # todo

        self.testCaseChecked("ROT_2110_0001")
    # end def test_ValidateRatchetEngaged_IfChangeToRatchetModeAndWheelSpeedLessThanOldNewAutoDisengage

    @features('Feature2110')
    @level('Robustness')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetDisengaged_IfChangeToRatchetModeAndWheelSpeedLargerThanAutoDisengage(self):
        """
        @tc_synopsis Change ratchet mode to ratchet mode and autoDisangage to another value than 'out of the
         box' while the wheel is running and verify that the ratchet is not engaged if speed above the old and
          new autoDisangage speed

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
         autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Send getRatchetControlMode to store the current configuration')
        # ---------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test=self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send setRatchetControlMode with wheelMode = 1 and other parameters to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test=self, wheel_mode=FREESPIN)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=FREESPIN)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Start wheel movement emulation with speed above '
                       f'{int(Numeral(self.cur_settings.auto_disengage)) + 10}')
        # ---------------------------------------------------------------------------
        # todo

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send setRatchetControlMode with wheelMode = 2, autoDisengage = '
                       f'{int(Numeral(self.cur_settings.auto_disengage)) + 10} and other parameters to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test=self, wheel_mode=RATCHET,
                                            auto_disengage=int(Numeral(self.cur_settings.auto_disengage)) + 10)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET,
                                    auto_disengage=int(Numeral(self.cur_settings.auto_disengage)) + 10)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate ratchet not engaged Ratchet Spy')
        # ---------------------------------------------------------------------------
        # todo

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Stop wheel movement emulation')
        # ---------------------------------------------------------------------------
        # todo

        self.testCaseChecked("ROT_2110_0002")
    # end def test_ValidateRatchetDisengaged_IfChangeToRatchetModeAndWheelSpeedLargerThanDisengage

    @features('Feature2110')
    @level('Robustness')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetEngaged_IfChangeToRatchetModeAndWheelSpeedBtwOldNewAutoDisengage(self):
        """
        @tc_synopsis Change ratchet mode to ratchet mode and autoDisengage to another value than 'out of the box' while
         the wheel is running and verify that the ratchet is engaged if speed above the old autoDisangage speed but
          below the new autoDisangage speed

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
         autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Send getRatchetControlMode to store the current configuration')
        # ---------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test=self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send setRatchetControlMode with wheelMode = 1 and other parameters to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test=self, wheel_mode=FREESPIN)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=FREESPIN)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Start wheel movement emulation with speed between '
                       f'{self.cur_settings.auto_disengage} and {int(Numeral(self.cur_settings.auto_disengage)) + 10}')
        # ---------------------------------------------------------------------------
        # todo

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send setRatchetControlMode with wheelMode = 2, autoDisengage = '
                       f'{int(Numeral(self.cur_settings.auto_disengage)) + 10} and other parameters to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test=self, wheel_mode=RATCHET,
                                            auto_disengage=int(Numeral(self.cur_settings.auto_disengage)) + 10)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET,
                                    auto_disengage=int(Numeral(self.cur_settings.auto_disengage)) + 10)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate ratchet engaged using Ratchet Spy')
        # ---------------------------------------------------------------------------
        # todo

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Stop wheel movement emulation')
        # ---------------------------------------------------------------------------
        # todo

        self.testCaseChecked("ROT_2110_0003")
    # end def test_ValidateRatchetEngaged_IfChangeToRatchetModeAndWheelSpeedBtwOldNewAutoDisengage

    @features('Feature2110')
    @level('Robustness')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetDisengaged_IfChangeToFreeWheelModeDuringWheelRunning(self):
        """
        @tc_synopsis Change rachet mode to free wheel while the wheel is running and verify that the rachet mode is
        changed before the wheel stops and ratchet not engaged

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
         autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Send getRatchetControlMode to store the current configuration')
        # ---------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test=self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send setRatchetControlMode with wheelMode = 2 and other parameters to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test=self, wheel_mode=RATCHET)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Start wheel movement emulation with speed below '
                       f'{self.cur_settings.auto_disengage}')
        # ---------------------------------------------------------------------------
        # todo

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send setRatchetControlMode with wheelMode = 1, autoDisengage = '
                       f'{int(Numeral(self.cur_settings.auto_disengage)) + 10} and other parameters to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test=self, wheel_mode=FREESPIN,
                                            auto_disengage=int(Numeral(self.cur_settings.auto_disengage)) + 10)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=FREESPIN,
                                    auto_disengage=int(Numeral(self.cur_settings.auto_disengage)) + 10)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate ratchet not engaged Ratchet Spy')
        # ---------------------------------------------------------------------------
        # todo

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Stop wheel movement emulation')
        # ---------------------------------------------------------------------------
        # todo

        self.testCaseChecked("ROT_2110_0004")
    # end def test_ValidateRatchetDisengaged_IfChangeToFreeWheelModeDuringWheelRunning

    @features('Feature2110')
    @level('ErrorHandling')
    @bugtracker('SetRatchetControlMode_ErrorCode')
    def test_VerifyInvalidWheelModeError(self):
        """
        @tc_synopsis Invalid setRatchetControlMode.wheelMode shall raise an error

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
         autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over wheelMode invalid range (typical wrong values)')
        # ---------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for invalid_wheel_mode in compute_wrong_range(list(range(3)), max_value=0xFF):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send setRatchetControlMode with wheelMode = {invalid_wheel_mode} and '
                           'other parameters to 0')
            # ---------------------------------------------------------------------------
            set_ratchet_ctrl_mode = SetRatchetControlMode(device_index=self.deviceIndex,
                                                          feature_index=self.feature_index,
                                                          wheel_mode=invalid_wheel_mode,
                                                          auto_disengage=DONOTCHANGE,
                                                          auto_disengage_default=DONOTCHANGE)
            response = self.send_report_wait_response(
                report=set_ratchet_ctrl_mode,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidArgument (0x02) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=self.feature_index,
                             obtained=response.feature_index,
                             msg='The feature_index parameter differs from the one expected')
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_2110_0005")
    # end def test_VerifyInvalidWheelModeError

    @features('Feature2110')
    @level('ErrorHandling')
    def test_VerifyInvalidFunctionIndexError(self):
        """
        @tc_synopsis Invalid getRatchetControlMode.functionIndex shall raise an error

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over functionIndex invalid range (typical wrong values)')
        # ---------------------------------------------------------------------------
        for invalid_func_index in compute_wrong_range(list(range(SmartShift.MAX_FUNCTION_INDEX + 1)), max_value=0xF):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send getRatchetControlMode with functionIndex = {invalid_func_index}')
            # ---------------------------------------------------------------------------
            get_ratchet_ctrl_mode = GetRatchetControlMode(device_index=self.deviceIndex,
                                                          feature_index=self.feature_index)
            get_ratchet_ctrl_mode.functionIndex = invalid_func_index
            get_ratchet_ctrl_mode_response = self.send_report_wait_response(
                report=get_ratchet_ctrl_mode,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidFunctionId (0x07) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_FUNCTION_ID),
                             obtained=get_ratchet_ctrl_mode_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_2110_0006")
    # end def test_VerifyInvalidFunctionIndexError

    @features('Feature2110')
    @level('Robustness')
    def test_VerifySoftwareIdIgnored(self):
        """
        @tc_synopsis Validates getRatchetControlMode.softwareId is ignored

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over softwareId range (several interesting values)')
        # ---------------------------------------------------------------------------
        for software_id in compute_inf_values(SmartShift.DEFAULT.SOFTWARE_ID):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send getRatchetControlMode with softwareId = {software_id}')
            # ---------------------------------------------------------------------------
            get_ratchet_ctrl_mode = GetRatchetControlMode(device_index=self.deviceIndex,
                                                          feature_index=self.feature_index)
            get_ratchet_ctrl_mode.softwareId = software_id
            get_ratchet_ctrl_mode_response = self.send_report_wait_response(
                report=get_ratchet_ctrl_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetRatchetControlModeResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate returned values are in valid range')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=get_ratchet_ctrl_mode.softwareId,
                             obtained=get_ratchet_ctrl_mode_response.softwareId,
                             msg='The softwareId parameter differs from the one expected')
            verify_ratchet_control_mode(test_case=self,
                                        response=get_ratchet_ctrl_mode_response,
                                        check_valid_range=True)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_2110_0007")
    # end def test_VerifySoftwareIdIgnored

    @features('Feature2110')
    @level('Robustness')
    def test_Padding(self):
        """
        @tc_synopsis Validates getRatchetControlMode.padding bytes are ignored

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over padding range (several interesting values)')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(GetRatchetControlMode.DEFAULT.PADDING,
                                                             GetRatchetControlMode.LEN.PADDING // 8))):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send getRatchetControlMode with padding = {padding_byte}')
            # ---------------------------------------------------------------------------
            get_ratchet_ctrl_mode = GetRatchetControlMode(device_index=self.deviceIndex,
                                                          feature_index=self.feature_index)
            get_ratchet_ctrl_mode.padding = padding_byte
            get_ratchet_ctrl_mode_response = self.send_report_wait_response(
                report=get_ratchet_ctrl_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetRatchetControlModeResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate returned values are in valid range')
            # ---------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=get_ratchet_ctrl_mode_response,
                                        check_valid_range=True)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_2110_0008")
    # end def test_Padding

# end class SmartShiftRobustnessTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
