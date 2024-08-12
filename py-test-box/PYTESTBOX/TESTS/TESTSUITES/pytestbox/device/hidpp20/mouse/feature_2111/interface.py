#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.mouse.feature_2111.interface
:brief: HID++ 2.0 SmartShiftTunable interface test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.smartshiftunableutils import SmartShiftTunableTestUtils
from pytestbox.device.hidpp20.mouse.feature_2111.smartshifttunable import SmartShiftTunableBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SmartShiftTunableInterfaceTestCase(SmartShiftTunableBaseTestCase):
    """
    x2111 - SmartShift 3G/EPM wheel with tunable torque interface test case
    """
    @features('Feature2111')
    @level('Interface')
    def test_get_capabilities_api(self):
        """
        Validate getCapabilities interface
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send getCapabilities request and wait response')
        # ----------------------------------------------------------------------------
        get_capabilities = self.feature_2111.get_capabilities_cls(self.deviceIndex, self.feature_2111_index)
        get_capabilities_response = self.send_report_wait_response(
            report=get_capabilities,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=self.feature_2111.get_capabilities_response_cls)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check product specific constants')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.GetCapabilitiesChecker.check_fields(
            self, get_capabilities_response, self.feature_2111.get_capabilities_response_cls)

        self.testCaseChecked("INT_2111_0001")
    # end def test_get_capabilities_api

    @features('Feature2111')
    @level('Interface')
    def test_get_ratchet_control_mode_api(self):
        """
        Validate getRatchetControlMode interface
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send getRatchetControlMode request and wait response')
        # ----------------------------------------------------------------------------
        get_ratchet_control_mode = self.feature_2111.get_ratchet_control_mode_cls(
            self.deviceIndex, self.feature_2111_index)
        get_ratchet_control_mode_response = self.send_report_wait_response(
            report=get_ratchet_control_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=self.feature_2111.get_ratchet_control_mode_response_cls)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check returned values are in valid range')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_fields(
            self,
            get_ratchet_control_mode_response,
            self.feature_2111.get_ratchet_control_mode_response_cls,
            SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.get_range_check_map())

        self.testCaseChecked("INT_2111_0002")
    # end def test_get_ratchet_control_mode_api

    @features('Feature2111')
    @level('Interface')
    def test_set_ratchet_control_mode_api(self):
        """
        Validate setRatchetControlMode interface
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(
            self, 'Send setRatchetControlMode request with "Do not change" values and wait response')
        # ----------------------------------------------------------------------------
        set_ratchet_control_mode = self.feature_2111.set_ratchet_control_mode_cls(
            self.deviceIndex,
            self.feature_2111_index,
            self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_WheelModeDefault,
            self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_AutoDisengageDefault,
            self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_DefaultTunableTorque)

        set_ratchet_control_mode_response = self.send_report_wait_response(
            report=set_ratchet_control_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=self.feature_2111.set_ratchet_control_mode_response_cls)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(
            self, 'Validate returned values are the actual values (i.e. default values)')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_fields(
            self, set_ratchet_control_mode_response,
            self.feature_2111.set_ratchet_control_mode_response_cls)

        self.testCaseChecked("INT_2111_0003")
    # end def test_set_ratchet_control_mode_api
# end class SmartShiftTunableInterfaceTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
