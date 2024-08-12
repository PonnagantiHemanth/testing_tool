#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.mouse.feature_2111.business
:brief: HID++ 2.0 SmartShiftTunable business test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.controlidtable import CidTable
from pyhid.hidpp.features.hireswheel import HiResWheel
from pyhid.hidpp.features.hireswheel import HiResWheelFactory
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunable
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.smartshiftunableutils import SmartShiftTunableTestUtils
from pytestbox.device.hidpp20.mouse.feature_2111.smartshifttunable import SmartShiftTunableBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SmartShiftTunableBusinessTestCase(SmartShiftTunableBaseTestCase):
    """
    x2111 - SmartShift 3G/EPM wheel with tunable torque business test case
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
    @level('Business')
    @services('MainWheel')
    @services('Ratchet')
    def test_ratchet_engagement_business(self):
        """
        Ratchet shall disengage when the wheel speed exceeds the speed threshold
        Ratchet shall remain disengaged as the wheel slows down and stops
        Ratchet shall remain engaged as long as the speed remains less than the threshold
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, f'Set wheel mode to ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, f'Set wheel speed to 0')
        # ----------------------------------------------------------------------------
        self.main_wheel_emulator.set_speed(0)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'Test Loop over autoDisengage valid range')
        # ----------------------------------------------------------------------------
        for auto_disengage in [SmartShiftTunable.AutoDisengageConst.RANGE[0],
                               SmartShiftTunable.AutoDisengageConst.RANGE[1]]:
            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Set autoDisengage value')
            CommonBaseTestUtils.LogHelper.log_check(self, f'Check autoDisengage value is set')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.set_auto_disengage(self, auto_disengage)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(
                self, f'Set wheel speed to less than the threshold, i.e. autoDisengage - 1')
            # ----------------------------------------------------------------------------
            self.main_wheel_emulator.set_speed(auto_disengage - 1)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Check ratchet is engaged')
            # ----------------------------------------------------------------------------
            self.assertEqual(expected=self.ratchet_spy.STATE.ENGAGED,
                             obtained=self.ratchet_spy.get_state(),
                             msg='Ratchet should be engaged')

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Set wheel speed to the threshold, i.e. autoDisengage')
            # ----------------------------------------------------------------------------
            self.main_wheel_emulator.set_speed(auto_disengage)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Check ratchet is disengaged')
            # ----------------------------------------------------------------------------
            self.assertEqual(expected=self.ratchet_spy.STATE.DISENGAGED,
                             obtained=self.ratchet_spy.get_state(),
                             msg='Ratchet should be disengaged')

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(
                self, f'Set wheel speed to less than the threshold, i.e. autoDisengage - 1')
            # ----------------------------------------------------------------------------
            self.main_wheel_emulator.set_speed(auto_disengage - 1)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Check ratchet is disengaged')
            # ----------------------------------------------------------------------------
            self.assertEqual(expected=self.ratchet_spy.STATE.DISENGAGED,
                             obtained=self.ratchet_spy.get_state(),
                             msg='Ratchet should be disengaged')

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Set wheel speed to the minimum before stop, i.e. 1')
            # ----------------------------------------------------------------------------
            self.main_wheel_emulator.set_speed(1)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Check ratchet is disengaged')
            # ----------------------------------------------------------------------------
            self.assertEqual(expected=self.ratchet_spy.STATE.DISENGAGED,
                             obtained=self.ratchet_spy.get_state(),
                             msg='Ratchet should be disengaged')

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Set wheel speed to 0')
            # ----------------------------------------------------------------------------
            self.main_wheel_emulator.set_speed(0)

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, f'Check ratchet is engaged')
            # ----------------------------------------------------------------------------
            self.assertEqual(expected=self.ratchet_spy.STATE.ENGAGED,
                             obtained=self.ratchet_spy.get_state(),
                             msg='Ratchet should be engaged')
        # end for
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_info(self, f'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("BUS_2111_0001")
    # end def test_ratchet_engagement_business

    @features('Feature2111')
    @level('Business', 'SmokeTests')
    @services('EmulatedKeys', (CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT],))
    def test_wheel_mode_change_with_button(self):
        """
        Pressing the ratchet control button shall change the wheel mode (both from free spin mode to ratchet mode and
        from ratchet mode to free spin mode)
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, f'Set wheel mode to ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, f'Press ratchet control button (using emulator)')
        # ----------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT])

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(
            self, f'Send getRatchetControlMode to check wheel mode is free spin mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, SmartShiftTunable.WheelModeConst.FREESPIN)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, f'Press ratchet control button (using emulator)')
        # ----------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT])

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, f'Send getRatchetControlMode to check wheel mode is ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, SmartShiftTunable.WheelModeConst.RATCHET)

        self.testCaseChecked("BUS_2111_0002")
    # end def test_wheel_mode_change_with_button

    @features('Feature2111')
    @features('Feature2121')
    @level('Business')
    def test_hires_wheel_feature_change_business(self):
        """
        Feature 0x2121 shall report the wheel mode

        The 0x2121 feature should generate a ratchet change event when the wheel mode is changed by software calling
        setRatchetControlMode
        """
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Get feature HiRes Wheel (0x2121)')
        # ----------------------------------------------------------------------------
        feature_2121_index, feature_2121, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, HiResWheel.FEATURE_ID, HiResWheelFactory)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, f'Set wheel mode to ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, f'Send setRatchetControlMode to set free spin mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_freespin(self)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(
            self, f'Check 0x2121 - getRatchetSwitchState() reports ratchet switch state')
        # ----------------------------------------------------------------------------
        get_ratchet_switch_state = feature_2121.get_ratchet_switch_state_cls(self.deviceIndex, feature_2121_index)
        get_ratchet_switch_state_response = self.send_report_wait_response(
            report=get_ratchet_switch_state,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=feature_2121.get_ratchet_switch_state_response_cls)

        self.assertEqual(HiResWheel.FREE_WHEEL, get_ratchet_switch_state_response.state,
                         'Ratchet state should be free wheel')

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(
            self, f'Check 0x2121 [event1] ratchetSwitch() reports ratchet switch state changes')
        # ----------------------------------------------------------------------------
        ratchet_switch_evt = self.getMessage(queue=self.hidDispatcher.event_message_queue,
                                             class_type=feature_2121.ratchet_switch_event_cls)
        self.assertEqual(HiResWheel.FREE_WHEEL, ratchet_switch_evt.state, 'Ratchet state should be free wheel')

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, f'Send setRatchetControlMode to set ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(
            self, 'Check 0x2121 [3] getRatchetSwitchState() reports ratchet switch state')
        # ----------------------------------------------------------------------------
        get_ratchet_switch_state_response = self.send_report_wait_response(
            report=get_ratchet_switch_state,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=feature_2121.get_ratchet_switch_state_response_cls)

        self.assertEqual(HiResWheel.RATCHET_ENGAGED, get_ratchet_switch_state_response.state,
                         'Ratchet state should be engaged')

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(
            self, 'Check 0x2121 [event1] ratchetSwitch() reports ratchet switch state changes')
        # ----------------------------------------------------------------------------
        ratchet_switch_evt = self.getMessage(queue=self.hidDispatcher.event_message_queue,
                                             class_type=feature_2121.ratchet_switch_event_cls)
        self.assertEqual(HiResWheel.RATCHET_ENGAGED, ratchet_switch_evt.state, 'Ratchet state should be engaged')

        self.testCaseChecked("BUS_2111_0003")
    # end def test_hires_wheel_feature_change_business
# end class SmartShiftTunableBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
