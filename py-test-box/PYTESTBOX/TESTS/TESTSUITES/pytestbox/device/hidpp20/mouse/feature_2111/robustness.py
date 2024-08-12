#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.mouse.feature_2111.robustness
:brief: HID++ 2.0 SmartShiftTunable robustness test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunable
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.smartshiftunableutils import SmartShiftTunableTestUtils
from pytestbox.device.hidpp20.mouse.feature_2111.smartshifttunable import SmartShiftTunableBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SmartShiftTunableRobustnessTestCase(SmartShiftTunableBaseTestCase):
    """
    x2111 - SmartShift 3G/EPM wheel with tunable torque robustness test case
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Set default values before each test')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_control_mode_configuration(
            self,
            wheel_mode=self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_WheelModeDefault,
            auto_disengage=self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_AutoDisengageDefault,
            current_tunable_torque=self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_DefaultTunableTorque)
    # end def setUp

    @features('Feature2111')
    @level('Robustness')
    def test_set_wheel_mode_out_of_range(self):
        """
        Inputs.setRatchetControlMode.wheelMode out of range shall raise an INVALID_ARGUMENT error
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'Test Loop over wheel mode out of range values (0x03, 0xFF)')
        # ----------------------------------------------------------------------------
        list_valid_values = [SmartShiftTunable.WheelModeConst.DO_NOT_CHANGE,
                             SmartShiftTunable.WheelModeConst.FREESPIN,
                             SmartShiftTunable.WheelModeConst.RATCHET]
        for wheel_mode in compute_wrong_range(value=list_valid_values, min_value=0x00, max_value=0xFF):
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(
                self, f'Send setRatchetControlMode with wheel mode out of range value (i.e. {wheel_mode})')
            # ----------------------------------------------------------------------------
            set_ratchet_control_mode = self.feature_2111.set_ratchet_control_mode_cls(
                self.deviceIndex,
                self.feature_2111_index,
                wheel_mode,
                SmartShiftTunable.AutoDisengageConst.DO_NOT_CHANGE,
                SmartShiftTunable.TunableTorqueConst.DO_NOT_CHANGE)

            error_response = self.send_report_wait_response(
                report=set_ratchet_control_mode,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Check INVALID_ARGUMENT error code is raised')
            # ----------------------------------------------------------------------------
            self.assertEqual(ErrorCodes.INVALID_ARGUMENT, error_response.errorCode,
                             "Wheel mode out of range should raise an Invalid argument error")
        # end for
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROB_2111_0001")
    # end def test_set_wheel_mode_out_of_range

    @features('Feature2111')
    @level('Robustness')
    def test_set_current_tunable_torque_out_of_range(self):
        """
        Inputs.setRatchetControlMode.currentTunableTorque out of range shall raise an INVALID_ARGUMENT error
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, f'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(
            self, f'Test Loop over current tunable torque out of range values (0x65, 0xFF)')
        # ----------------------------------------------------------------------------
        list_valid_values = [SmartShiftTunable.TunableTorqueConst.DO_NOT_CHANGE]
        list_valid_values += list(range(SmartShiftTunable.TunableTorqueConst.RANGE[0],
                                        SmartShiftTunable.TunableTorqueConst.RANGE[1] + 1))
        for torque in compute_wrong_range(value=list_valid_values, min_value=0x00, max_value=0xFF):
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(
                self, f'Send setRatchetControlMode with current tunable torque out of range value (i.e. {torque})')
            # ----------------------------------------------------------------------------
            set_ratchet_control_mode = self.feature_2111.set_ratchet_control_mode_cls(
                self.deviceIndex,
                self.feature_2111_index,
                SmartShiftTunable.WheelModeConst.DO_NOT_CHANGE,
                SmartShiftTunable.AutoDisengageConst.DO_NOT_CHANGE,
                torque)

            error_response = self.send_report_wait_response(
                report=set_ratchet_control_mode,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Check INVALID_ARGUMENT error code is raised')
            # ----------------------------------------------------------------------------
            self.assertEqual(ErrorCodes.INVALID_ARGUMENT, error_response.errorCode,
                             "Tunable torque out of range should raise an Invalid argument error")
        # end for
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROB_2111_0002")
    # end def test_set_current_tunable_torque_out_of_range

    @features('Feature2111')
    @level('Robustness')
    def test_function_index_error(self):
        """
        Invalid Inputs.functionIndex shall raise an error
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self,
                                               f'Test Loop over functionIndex invalid range (typical wrong values)')
        # ----------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(
                self.feature_2111.get_max_function_index() + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self,
                                                   f'Send getRatchetControlMode with functionIndex = {function_index}')
            # ----------------------------------------------------------------------------
            get_ratchet_control_mode = self.feature_2111.get_ratchet_control_mode_cls(
                self.deviceIndex, self.feature_2111_index)
            get_ratchet_control_mode.functionIndex = function_index

            error_response = self.send_report_wait_response(
                report=get_ratchet_control_mode,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self,
                                                    f'Check INVALID_FUNCTION_ID Error Code returned by the device')
            # ----------------------------------------------------------------------------
            self.assertEqual(ErrorCodes.INVALID_FUNCTION_ID, error_response.errorCode,
                             "Function index out of range should raise an Invalid function id error")
        # end for
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROB_2111_0003")
    # end def test_function_index_error

    @features('Feature2111')
    @level('Robustness')
    def test_software_id_robustness(self):
        """
        Inputs.softwareId input is ignored by the firmware
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'Test Loop over softwareId range (several interesting values)')
        # ----------------------------------------------------------------------------
        for software_id in compute_wrong_range(value=SmartShiftTunable.DEFAULT.SOFTWARE_ID,
                                             max_value=0xF):
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Send getRatchetControlMode with softwareId = {software_id}')
            # ----------------------------------------------------------------------------
            get_ratchet_control_mode = self.feature_2111.get_ratchet_control_mode_cls(
                self.deviceIndex, self.feature_2111_index)
            get_ratchet_control_mode.softwareId = software_id

            get_ratchet_control_mode_response = self.send_report_wait_response(
                report=get_ratchet_control_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=self.feature_2111.get_ratchet_control_mode_response_cls)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Validate returned values are in valid range')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_fields(
                self,
                get_ratchet_control_mode_response,
                self.feature_2111.get_ratchet_control_mode_response_cls,
                SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.get_range_check_map())
        # end for
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROB_2111_0004")
    # end def test_software_id_robustness

    @features('Feature2111')
    @level('Robustness')
    def test_get_ratchet_control_mode_padding_robustness(self):
        """
        Inputs.padding shall be ignored by the firmware
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'Test Loop over padding range (several interesting values)')
        # ----------------------------------------------------------------------------
        for padding in compute_sup_values(
                HexList(Numeral(SmartShiftTunable.DEFAULT.PADDING,
                                self.feature_2111.get_ratchet_control_mode_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Send getRatchetControlMode with padding = {padding}')
            # ----------------------------------------------------------------------------
            get_ratchet_control_mode = self.feature_2111.get_ratchet_control_mode_cls(
                self.deviceIndex, self.feature_2111_index)
            get_ratchet_control_mode.padding = padding

            get_ratchet_control_mode_response = self.send_report_wait_response(
                report=get_ratchet_control_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=self.feature_2111.get_ratchet_control_mode_response_cls)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Validate returned values are in valid range')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_fields(
                self,
                get_ratchet_control_mode_response,
                self.feature_2111.get_ratchet_control_mode_response_cls,
                SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.get_range_check_map())
        # end for
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROB_2111_0005")
    # end def test_get_ratchet_control_mode_padding_robustness

    @features('Feature2111')
    @level('Robustness')
    def test_get_capabilities_padding_robustness(self):
        """
        Inputs.padding shall be ignored by the firmware
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'Test Loop over padding range (several interesting values)')
        # ----------------------------------------------------------------------------
        for padding in compute_sup_values(
                HexList(Numeral(SmartShiftTunable.DEFAULT.PADDING,
                                self.feature_2111.get_capabilities_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Send getCapabilites with padding = {padding}')
            # ----------------------------------------------------------------------------
            get_capabilities = self.feature_2111.get_capabilities_cls(
                self.deviceIndex, self.feature_2111_index)
            get_capabilities.padding = padding

            get_capabilities_response = self.send_report_wait_response(
                report=get_capabilities,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=self.feature_2111.get_capabilities_response_cls)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Validate returned values are in valid range')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.GetCapabilitiesChecker.check_fields(
                self, get_capabilities_response, self.feature_2111.get_capabilities_response_cls)
        # end for
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROB_2111_0006")
    # end def test_get_capabilities_padding_robustness
# end class SmartShiftTunableRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
