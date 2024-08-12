#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.mouse.feature_2111.functionality
:brief: HID++ 2.0 SmartShiftTunable functionality test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.core import TestException
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.changehost import ChangeHost
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtons
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsFactory
from pyhid.hidpp.features.devicereset import DeviceReset
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pyhid.hidpp.features.hireswheel import HiResWheel
from pyhid.hidpp.features.hireswheel import HiResWheelFactory
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunable
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunableFactory
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.smartshiftunableutils import SmartShiftTunableTestUtils
from pytestbox.device.hidpp20.mouse.feature_2111.smartshifttunable import SmartShiftTunableBaseTestCase
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SmartShiftTunableFunctionalityTestCase(SmartShiftTunableBaseTestCase):
    """
    x2111 - SmartShift 3G/EPM wheel with tunable torque functionality test case
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Set default values before each test')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_control_mode_configuration(
            self,
            wheel_mode=self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_WheelModeDefault,
            auto_disengage=self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_AutoDisengageDefault,
            current_tunable_torque=self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_DefaultTunableTorque)
    # end def setUp

    @features('Feature2111')
    @level('Functionality')
    def test_set_wheel_mode(self):
        """
        setRatchetControlMode wheel mode parameter shall set the current wheel mode
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set wheel mode to free spin mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_freespin(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is free spin mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, SmartShiftTunable.WheelModeConst.FREESPIN)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set wheel mode to ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, SmartShiftTunable.WheelModeConst.RATCHET)

        self.testCaseChecked("FUN_2111_0002")
    # end def test_set_wheel_mode

    @features('Feature2111')
    @level('Functionality')
    def test_do_not_change_wheel_mode(self):
        """
        setRatchetControlMode wheelMode parameter shall not change wheel mode if set to "Do not change"
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to get initial wheel mode')
        # ----------------------------------------------------------------------------
        initial_wheel_mode = SmartShiftTunableTestUtils.HIDppHelper.get_wheel_mode(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode with wheel mode to "Do not change"')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, SmartShiftTunable.WheelModeConst.DO_NOT_CHANGE)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is equal to the initial wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, initial_wheel_mode)

        self.testCaseChecked("FUN_2111_0003")
    # end def test_do_not_change_wheel_mode

    @features('Feature2111')
    @level('Functionality')
    def test_set_auto_disengage(self):
        """
        Set ratchet control mode request should set parameters in ratchet mode and in freespin mode
        """
        result = []
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over auto disengage valid range and wheel modes')
        # ----------------------------------------------------------------------------
        for mode in [SmartShiftTunable.WheelModeConst.RATCHET, SmartShiftTunable.WheelModeConst.FREESPIN]:
            for auto_disengage in [SmartShiftTunable.AutoDisengageConst.RANGE[0],
                                   SmartShiftTunable.AutoDisengageConst.RANGE[1],
                                   SmartShiftTunable.AutoDisengageConst.ALWAYS_ENGAGED]:
                # ----------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f'Send setRatchetControlMode to set wheel mode with wheel mode = {mode} and auto disengage = '
                    f'{auto_disengage}')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, mode)

                # ----------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send setRatchetControlMode to set autoDisengage to valid value')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.set_auto_disengage(self, auto_disengage)

                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, 'Send getRatchetControlMode to check autoDisengage valid value')
                # ----------------------------------------------------------------------------
                try:
                    SmartShiftTunableTestUtils.HIDppHelper.get_and_check_auto_disengage(self, auto_disengage)
                except TestException as e:
                    result.append(e)
                # end try
            # end for
        # end for
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------
        self.assertListEqual(result, [], 'Auto disengage value should be as expected for all values')
        self.testCaseChecked("FUN_2111_0004")
    # end def test_set_auto_disengage

    @features('Feature2111')
    @level('Functionality')
    @services('MainWheel')
    @services('Ratchet')
    def test_auto_disengage_always_engage(self):
        """
        setRatchetControlMode autoDisengage parameter shall immediately engage the ratchet if set to "Always Engaged" in
        ratchet mode
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Set wheel speed to more than auto disengage threshold to disengage the ratchet')
        # ----------------------------------------------------------------------------
        self.main_wheel_emulator.set_speed(SmartShiftTunableTestUtils.HIDppHelper.get_auto_disengage(self) + 1)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set autoDisengage to "Always Engaged"')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_auto_disengage(self,
                                                                  SmartShiftTunable.AutoDisengageConst.ALWAYS_ENGAGED)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check ratchet is engaged')
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=self.ratchet_spy.STATE.ENGAGED,
                         obtained=self.ratchet_spy.get_state(),
                         msg='Ratchet should be engaged')

        self.testCaseChecked("FUN_2111_0005")
    # end def test_auto_disengage_always_engage

    @features('Feature2111')
    @level('Functionality')
    def test_do_not_change_auto_disengage(self):
        """
        setRatchetControlMode autoDisengage parameter shall not change auto disengage value if set to "Do not change"
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to get initial auto disengage value')
        # ----------------------------------------------------------------------------
        initial_auto_disengage = SmartShiftTunableTestUtils.HIDppHelper.get_auto_disengage(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set autoDisengage to "Do not change"')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_auto_disengage(self,
                                                                  SmartShiftTunable.AutoDisengageConst.DO_NOT_CHANGE)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode to check autoDisengage value is equal to initial value')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_auto_disengage(self, initial_auto_disengage)

        self.testCaseChecked("FUN_2111_0006")
    # end def test_do_not_change_auto_disengage

    @features('Feature2111')
    @level('Functionality')
    def test_set_current_tunable_torque(self):
        """
        setRatchetControlMode currentTunableTorque shall set the current tunable torque in % of the maxForce
        """
        result = []
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over current tunable torque valid range and wheel modes')
        # ----------------------------------------------------------------------------
        for mode in [SmartShiftTunable.WheelModeConst.RATCHET, SmartShiftTunable.WheelModeConst.FREESPIN]:
            for torque in [SmartShiftTunable.TunableTorqueConst.RANGE[0],
                           SmartShiftTunable.TunableTorqueConst.RANGE[1]]:
                LogHelper.log_info(self, f'Wheel mode = {mode}. Current tunable torque = {torque}')
                # ----------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send setRatchetControlMode to set wheel mode')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, mode)

                # ----------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send setRatchetControlMode to set currentTunableTorque to valid value')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.set_current_tunable_torque(self, torque)

                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, 'Send getRatchetControlMode to check currentTunableTorque valid value')
                # ----------------------------------------------------------------------------
                try:
                    SmartShiftTunableTestUtils.HIDppHelper.get_and_check_current_tunable_torque(self, torque)
                except TestException as e:
                    result.append(e)
                # end try
            # end for
        # end for
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------
        self.assertListEqual(result, [], "Current tunable torque value should be as expected for all values")

        self.testCaseChecked("FUN_2111_0007")
    # end def test_set_current_tunable_torque

    @features('Feature2111')
    @level('Functionality')
    def test_do_not_change_current_tunable_torque(self):
        """
        setRatchetControlMode currentTunableTorque parameter shall not change the current tunable torque if set to
        "Do not change"
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to get initial current tunable torque')
        # ----------------------------------------------------------------------------
        initial_current_tunable_torque = SmartShiftTunableTestUtils.HIDppHelper.get_current_tunable_torque(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set currentTunableTorque to "Do not change"')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_current_tunable_torque(
            self, SmartShiftTunable.TunableTorqueConst.DO_NOT_CHANGE)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Send getRatchetControlMode to check currentTunableTorque value is equal to initial value')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_current_tunable_torque(
            self, initial_current_tunable_torque)

        self.testCaseChecked("FUN_2111_0008")
    # end def test_do_not_change_current_tunable_torque

    @features('Feature2111')
    @level('Functionality')
    @services('Ratchet')
    def test_ratchet_disengaged_freespin_mode(self):
        """
        Ratchet should be disengaged when Inputs.setRatchetControlMode.wheelMode is set to freespin mode
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Set wheel speed to 0')
        # ----------------------------------------------------------------------------
        self.main_wheel_emulator.set_speed(0)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set free spin wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_freespin(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check ratchet is disengaged')
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=self.ratchet_spy.STATE.DISENGAGED,
                         obtained=self.ratchet_spy.get_state(),
                         msg='Ratchet should be disengaged')

        self.testCaseChecked("FUN_2111_0009")
    # end def test_ratchet_disengaged_freespin_mode

    @features('Feature2111')
    @level('Functionality')
    @services('MainWheel')
    @services('Ratchet')
    def test_ratchet_disengaged_ratchet_mode_high_speed(self):
        """
        Ratchet should be disengaged when Inputs.setRatchetControlMode.wheelMode is set to ratchet mode while wheel
        speed is more than the threshold
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set free spin wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_freespin(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Wheel speed is more than autoDisengage')
        # ----------------------------------------------------------------------------
        self.main_wheel_emulator.set_speed(SmartShiftTunableTestUtils.HIDppHelper.get_auto_disengage(self) + 1)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check ratchet is disengaged')
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=self.ratchet_spy.STATE.DISENGAGED,
                         obtained=self.ratchet_spy.get_state(),
                         msg='Ratchet should be disengaged')

        self.testCaseChecked("FUN_2111_0010")
    # end def test_ratchet_disengaged_ratchet_mode_high_speed

    @features('Feature2111')
    @level('Functionality')
    @services('MainWheel')
    @services('Ratchet')
    def test_ratchet_engaged_ratchet_mode_low_speed(self):
        """
        Ratchet should be engaged when Inputs.setRatchetControlMode.wheelMode is set to ratchet mode while wheel
        speed is less than the threshold
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set free spin wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_freespin(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Wheel speed is less than autoDisengage')
        # ----------------------------------------------------------------------------
        self.main_wheel_emulator.set_speed(SmartShiftTunableTestUtils.HIDppHelper.get_auto_disengage(self) - 1)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check ratchet is engaged')
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=self.ratchet_spy.STATE.ENGAGED,
                         obtained=self.ratchet_spy.get_state(),
                         msg='Ratchet should be engaged')

        self.testCaseChecked("FUN_2111_0011")
    # end def test_ratchet_engaged_ratchet_mode_low_speed

    @features('Feature2111')
    @level('Functionality')
    @services('MainWheel')
    @services('Ratchet')
    def test_ratchet_disengaged_auto_disengage_low_high_transition(self):
        """
        Ratchet shall be disengage when Inputs.setRatchetControlMode.autoDisengage is set to more than speed while in
        ratchet mode and speed is more than initial auto disengage
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Wheel speed is more than autoDisengage')
        # ----------------------------------------------------------------------------
        self.main_wheel_emulator.set_speed(SmartShiftTunableTestUtils.HIDppHelper.get_auto_disengage(self) + 1)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set autoDisengage to more than wheel speed')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_auto_disengage(self, self.main_wheel_emulator.get_speed() + 1)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check ratchet is disengaged')
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=self.ratchet_spy.STATE.DISENGAGED,
                         obtained=self.ratchet_spy.get_state(),
                         msg='Ratchet should be disengaged')

        self.testCaseChecked("FUN_2111_0012")
    # end def test_ratchet_disengaged_auto_disengage_low_high_transition

    @features('Feature2111')
    @level('Functionality')
    @services('MainWheel')
    @services('Ratchet')
    def test_ratchet_engaged_auto_disengage_high_low_transition(self):
        """
        Ratchet shall be engaged when Inputs.setRatchetControlMode.autoDisengage is set to less than current speed
        while in ratchet mode and speed is less than initial auto disengage
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Wheel speed is less than autoDisengage')
        # ----------------------------------------------------------------------------
        self.main_wheel_emulator.set_speed(SmartShiftTunableTestUtils.HIDppHelper.get_auto_disengage(self) - 1)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode to set autoDisengage to less than wheel speed')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_auto_disengage(self, self.main_wheel_emulator.get_speed() - 1)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check ratchet is engaged')
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=self.ratchet_spy.STATE.ENGAGED,
                         obtained=self.ratchet_spy.get_state(),
                         msg='Ratchet should be engaged')

        self.testCaseChecked("FUN_2111_0013")
    # end def test_ratchet_engaged_auto_disengage_high_low_transition

    @features('Feature2111')
    @level('Functionality')
    @services('Ratchet')
    def test_auto_disengage_no_effect_in_freespin(self):
        """
        Ratchet shall remain disengaged when Inputs.setRatchetControlMode.autoDisengage is changed
        while in free spin mode
        """
        mid_value = (SmartShiftTunable.AutoDisengageConst.RANGE[1] - SmartShiftTunable.AutoDisengageConst.RANGE[0]) // 2
        significant_values = [SmartShiftTunable.AutoDisengageConst.DO_NOT_CHANGE,
                              SmartShiftTunable.AutoDisengageConst.RANGE[0],
                              mid_value,
                              SmartShiftTunable.AutoDisengageConst.RANGE[1],
                              SmartShiftTunable.AutoDisengageConst.ALWAYS_ENGAGED]
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'autoDisengage is not one of the significant value')
        # ----------------------------------------------------------------------------
        initial_auto_disengage = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_AutoDisengageDefault
        self.assertNotIn(initial_auto_disengage, significant_values, "Initial value should not be in tested values")

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set free spin wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_freespin(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over significant values {significant_values}')
        # ----------------------------------------------------------------------------
        result = []
        for auto_disengage in significant_values:
            LogHelper.log_info(self, f'auto disengage = {auto_disengage}')
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setRatchetControlMode to set autoDisengage')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.set_auto_disengage(self, auto_disengage)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check ratchet is disengaged')
            # ----------------------------------------------------------------------------
            try:
                self.assertEqual(expected=self.ratchet_spy.STATE.DISENGAGED,
                                 obtained=self.ratchet_spy.get_state(),
                                 msg='Ratchet should be disengaged')
            except TestException as e:
                result.append(e)
            # end try
        # end for
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------
        self.assertEqual(result, [], "Ratchet should be disengaged for all values of auto disengage")

        self.testCaseChecked("FUN_2111_0014")
    # end def test_auto_disengage_no_effect_in_freespin

    @features('Feature2111')
    @features('Feature1B04')
    @level('Functionality')
    @services('EmulatedKeys', (CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT],))
    def test_wheel_mode_button_remapping(self):
        """
        Outputs.getRatchetControlMode.wheelMode shall not change on button press when ratchet control button has been
        remapped
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature Special Keys and Mouse buttons (0x1b04)')
        # ----------------------------------------------------------------------------
        feature_1b04_index, feature_1b04, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, SpecialKeysMSEButtons.FEATURE_ID, SpecialKeysMSEButtonsFactory)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get next available CID where SmartShift can be remapped')
        # ----------------------------------------------------------------------------
        cids_groups_gmasks = list(zip(self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID),
                                      self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_GROUP),
                                      self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_GMASK)))
        smart_shift_gmask = cids_groups_gmasks[
            self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID).index(CidTable.SMART_SHIFT)][2]

        new_cid_value = None
        for cid, group, gmask in cids_groups_gmasks:
            if (group & smart_shift_gmask) == group:
                new_cid_value = cid
                break
            # end if
        # end for
        assert new_cid_value, "No CID available for remapping"

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, f'Send setCidReporting with CID {CidTable.SMART_SHIFT} and remap to new CID value {new_cid_value}')
        # ----------------------------------------------------------------------------
        set_cid_reporting = feature_1b04.set_cid_reporting_cls(
            self.deviceIndex, feature_1b04_index, ctrl_id=CidTable.SMART_SHIFT, remap=new_cid_value)

        self.send_report_wait_response(
            report=set_cid_reporting,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=feature_1b04.set_cid_reporting_response_cls)

        try:
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press ratchet control button')
            # ----------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT])

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is ratchet mode')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self,
                                                                            SmartShiftTunable.WheelModeConst.RATCHET)
        finally:
            # ----------------------------------------------------------------------------
            LogHelper.log_post_requisite(
                self, f'Send setCidReporting with CID {CidTable.SMART_SHIFT} to reset original CID')
            # ----------------------------------------------------------------------------
            set_cid_reporting = feature_1b04.set_cid_reporting_cls(
                self.deviceIndex, feature_1b04_index, ctrl_id=CidTable.SMART_SHIFT, remap=CidTable.SMART_SHIFT)
            self.send_report_wait_response(
                report=set_cid_reporting,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=feature_1b04.set_cid_reporting_response_cls)
        # end try

        self.testCaseChecked("FUN_2111_0015")
    # end def test_wheel_mode_button_remapping

    @features('Feature2111')
    @features('Feature1B04')
    @level('Functionality')
    @services('EmulatedKeys', (CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT],))
    def test_wheel_mode_button_diverted(self):
        """
        Outputs.getRatchetControlMode.wheelMode shall not change on button press when ratchet control button has been
        diverted
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature Special Keys and Mouse buttons (0x1b04)')
        # ----------------------------------------------------------------------------
        feature_1b04_index, feature_1b04, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, SpecialKeysMSEButtons.FEATURE_ID, SpecialKeysMSEButtonsFactory)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode to set ratchet wheel mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setCidReporting with CID 196 and set divert and dvalid flags')
        # ----------------------------------------------------------------------------
        set_cid_reporting = feature_1b04.set_cid_reporting_cls(
            self.deviceIndex, feature_1b04_index, ctrl_id=CidTable.SMART_SHIFT, divert=True, divert_valid=True)

        self.send_report_wait_response(
            report=set_cid_reporting,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=feature_1b04.set_cid_reporting_response_cls)

        try:
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press ratchet control button')
            # ----------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT])

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is ratchet mode')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self,
                                                                            SmartShiftTunable.WheelModeConst.RATCHET)
        finally:
            # ----------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Send setCidReporting with CID 196 to unset diverting')
            # ----------------------------------------------------------------------------
            set_cid_reporting = feature_1b04.set_cid_reporting_cls(
                self.deviceIndex, feature_1b04_index, ctrl_id=CidTable.SMART_SHIFT, divert=False, divert_valid=True)

            self.send_report_wait_response(
                report=set_cid_reporting,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=feature_1b04.set_cid_reporting_response_cls)
        # end try
        self.testCaseChecked("FUN_2111_0016")
    # end def test_wheel_mode_button_diverted

    @features('Feature2111')
    @features('Feature1B04')
    @features('Feature1802')
    @level('Functionality')
    @services('EmulatedKeys', (CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT],))
    def test_wheel_mode_button_remapped_and_reset(self):
        """
        Outputs.getRatchetControlMode.wheelMode shall change on button press after a reset when ratchet control
        button has been remapped before reset
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature Special Keys and Mouse buttons (0x1b04)')
        # ----------------------------------------------------------------------------
        feature_1b04_index, feature_1b04, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, SpecialKeysMSEButtons.FEATURE_ID, SpecialKeysMSEButtonsFactory)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get next available CID where SmartShift can be remapped')
        # ----------------------------------------------------------------------------
        cids_groups_gmasks = list(zip(self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID),
                                      self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_GROUP),
                                      self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_GMASK)))
        smart_shift_gmask = cids_groups_gmasks[
            self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID).index(CidTable.SMART_SHIFT)][2]

        new_cid_value = None
        for cid, group, gmask in cids_groups_gmasks:
            if (group & smart_shift_gmask) == group:
                new_cid_value = cid
                break
            # end if
        # end for
        assert new_cid_value, "No CID available for remapping"

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self,
            f'Send setCidReporting with CID {CidTable.SMART_SHIFT} and remap to another CID value ({new_cid_value})')
        # ----------------------------------------------------------------------------
        set_cid_reporting = feature_1b04.set_cid_reporting_cls(
            self.deviceIndex, feature_1b04_index, ctrl_id=CidTable.SMART_SHIFT, remap=new_cid_value)

        self.send_report_wait_response(
            report=set_cid_reporting,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=feature_1b04.set_cid_reporting_response_cls)

        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform a device hardware reset")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press ratchet control button')
            # ----------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT])

            # ----------------------------------------------------------------------------
            # noinspection Duplicates
            LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is free spin mode')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self,
                                                                            SmartShiftTunable.WheelModeConst.FREESPIN)
        finally:
            # ----------------------------------------------------------------------------
            LogHelper.log_post_requisite(
                self, f'Send setCidReporting with CID {CidTable.SMART_SHIFT} to reset original CID')
            # ----------------------------------------------------------------------------
            set_cid_reporting = feature_1b04.set_cid_reporting_cls(
                self.deviceIndex, feature_1b04_index, ctrl_id=CidTable.SMART_SHIFT, remap=CidTable.SMART_SHIFT)

            self.send_report_wait_response(
                report=set_cid_reporting,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=feature_1b04.set_cid_reporting_response_cls)
        # end try

        self.testCaseChecked("FUN_2111_0017")
    # end def test_wheel_mode_button_remapped_and_reset

    @features('Feature2111')
    @features('Feature1B04')
    @level('Functionality')
    @services('EmulatedKeys', (CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT],))
    def test_wheel_mode_button_diverted_and_reset(self):
        """
        Outputs.getRatchetControlMode.wheelMode shall change on button press after a reset when ratchet control
        button has been diverted before reset
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature Special Keys and Mouse buttons (0x1b04)')
        # ----------------------------------------------------------------------------
        feature_1b04_index, feature_1b04, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, SpecialKeysMSEButtons.FEATURE_ID, SpecialKeysMSEButtonsFactory)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, f'Send setCidReporting with CID {CidTable.SMART_SHIFT} and set divert and dvalid flags')
        # ----------------------------------------------------------------------------
        set_cid_reporting = feature_1b04.set_cid_reporting_cls(
            self.deviceIndex, feature_1b04_index, ctrl_id=CidTable.SMART_SHIFT, divert=True, divert_valid=True)

        self.send_report_wait_response(
            report=set_cid_reporting,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=feature_1b04.set_cid_reporting_response_cls)

        try:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform a device hardware reset")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press ratchet control button')
            # ----------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT])

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is freespin mode')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self,
                                                                            SmartShiftTunable.WheelModeConst.FREESPIN)
        finally:
            # ----------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Send setCidReporting with CID 196 to unset diverting')
            # ----------------------------------------------------------------------------
            set_cid_reporting = feature_1b04.set_cid_reporting_cls(
                self.deviceIndex, feature_1b04_index, ctrl_id=CidTable.SMART_SHIFT, divert=False, divert_valid=True)

            self.send_report_wait_response(
                report=set_cid_reporting,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=feature_1b04.set_cid_reporting_response_cls)
        # end try

        self.testCaseChecked("FUN_2111_0018")
    # end def test_wheel_mode_button_diverted_and_reset

    @features('Feature2111')
    @features('Feature2121')
    @level('Functionality')
    @services('EmulatedKeys', (CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT],))
    def test_set_ratchet_control_mode_while_button_pressed(self):
        """
        Changes of wheel mode when smartshift button is pressed, then setRatchetControlMode and then smartshift
        button is released.
        Check with 0x2121 event and getRatchetControlMode that setRatchetControlMode is received even while
        smartshift button is pressed
        """
        wheel_mode_to_state = {
            SmartShiftTunable.WheelModeConst.FREESPIN: HiResWheel.FREE_WHEEL,
            SmartShiftTunable.WheelModeConst.RATCHET: HiResWheel.RATCHET_ENGAGED,
        }

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature HiRes Wheel (0x2121)')
        # ----------------------------------------------------------------------------
        feature_2121_index, feature_2121, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, HiResWheel.FEATURE_ID, HiResWheelFactory)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # ----------------------------------------------------------------------------
        initial_config = SmartShiftTunableTestUtils.HIDppHelper.get_ratchet_control_mode_response(self)

        try:
            # ----------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over valid wheelMode values')
            # ----------------------------------------------------------------------------
            for wheel_mode in wheel_mode_to_state:
                # ----------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and other parameters to 0')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, wheel_mode)

                # ----------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f'Validate receive ratchetSwitch event with state = {wheel_mode_to_state[wheel_mode]}')
                # ----------------------------------------------------------------------------
                ratchet_switch_evt = self.getMessage(queue=self.hidDispatcher.event_message_queue,
                                                     class_type=feature_2121.ratchet_switch_event_cls)
                self.assertEqual(wheel_mode_to_state[wheel_mode], ratchet_switch_evt.state,
                                 f'Ratchet state should be {wheel_mode_to_state[wheel_mode]}')

                # ----------------------------------------------------------------------------
                LogHelper.log_step(
                    self,
                    f'Simulate SmartShift button press by sending CID = {CidTable.SMART_SHIFT} key press stimulus to '
                    f'DUT')
                # ----------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT])
                sleep(0.2)

                # ----------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and other parameters to 0')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, wheel_mode)

                # ----------------------------------------------------------------------------
                LogHelper.log_step(
                    self,
                    f'Simulate SmartShift button release by sending CID = {CidTable.SMART_SHIFT} key release stimulus '
                    f'to DUT')
                # ----------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT])
                sleep(0.2)

                if wheel_mode == SmartShiftTunable.WheelModeConst.RATCHET:
                    other_mode = SmartShiftTunable.WheelModeConst.FREESPIN
                else:
                    other_mode = SmartShiftTunable.WheelModeConst.RATCHET
                # end if

                # ----------------------------------------------------------------------------
                LogHelper.log_check(
                    self,
                    f'Validate receive 2 ratchetSwitch event in the right order: {wheel_mode_to_state[other_mode]} '
                    f'then {wheel_mode_to_state[wheel_mode]}')
                # ----------------------------------------------------------------------------
                ratchet_switch_evt = self.getMessage(queue=self.hidDispatcher.event_message_queue,
                                                     class_type=feature_2121.ratchet_switch_event_cls)
                self.assertEqual(wheel_mode_to_state[other_mode], ratchet_switch_evt.state,
                                 f'Ratchet state should be {wheel_mode_to_state[other_mode]}')

                ratchet_switch_evt = self.getMessage(queue=self.hidDispatcher.event_message_queue,
                                                     class_type=feature_2121.ratchet_switch_event_cls)
                self.assertEqual(wheel_mode_to_state[wheel_mode], ratchet_switch_evt.state,
                                 f'Ratchet state should be {wheel_mode_to_state[wheel_mode]}')

                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, f'Send getRatchetControlMode and validate response.wheelMode = {wheel_mode}')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, wheel_mode)
            # end for
            # ----------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------
        finally:
            # ----------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Reload and verify the value stored during pre-requisite')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, initial_config.wheel_mode)

            final_config = SmartShiftTunableTestUtils.HIDppHelper.get_ratchet_control_mode_response(self)
            self.assertEqual(final_config, initial_config, "Final configuration should be same as initial")
        # end try

        self.testCaseChecked("FUN_2111_0019")
    # end def test_set_ratchet_control_mode_while_button_pressed

    @features('Feature2111')
    @features('Feature2121')
    @features('Feature1B04')
    @features('CidRemapTargetEmulated', CidTable.SMART_SHIFT)
    @level('Functionality')
    def test_set_ratchet_control_mode_while_remapped_button_pressed(self):
        """
        Changes of wheel mode when button remapped on Smart Shift is pressed, then setRatchetControlMode and then
        button remapped on Smart Shift is released
        Check with 0x2121 event and getRatchetControlMode
        """
        wheel_mode_to_state = {
            SmartShiftTunable.WheelModeConst.FREESPIN: HiResWheel.FREE_WHEEL,
            SmartShiftTunable.WheelModeConst.RATCHET: HiResWheel.RATCHET_ENGAGED,
        }

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature HiRes Wheel (0x2121)')
        # ----------------------------------------------------------------------------
        feature_2121_index, feature_2121, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, HiResWheel.FEATURE_ID, HiResWheelFactory)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature Special Keys and Mouse buttons (0x1b04)')
        # ----------------------------------------------------------------------------
        feature_1b04_index, feature_1b04, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, SpecialKeysMSEButtons.FEATURE_ID, SpecialKeysMSEButtonsFactory)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # ----------------------------------------------------------------------------
        initial_config = SmartShiftTunableTestUtils.HIDppHelper.get_ratchet_control_mode_response(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get next available CID which can be remapped on SmartShift')
        # ----------------------------------------------------------------------------
        cids_groups_gmasks = list(zip(self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID),
                                      self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_GROUP),
                                      self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_GMASK)))
        smart_shift_group = cids_groups_gmasks[
            self.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID).index(CidTable.SMART_SHIFT)][1]

        new_cid_value = None
        for cid, group, gmask in cids_groups_gmasks:
            if cid in CID_TO_KEY_ID_MAP and CID_TO_KEY_ID_MAP[cid] in self.button_stimuli_emulator.connected_key_ids \
                    and (gmask & smart_shift_group) == smart_shift_group:
                new_cid_value = cid
                break
            # end if
        # end for
        assert new_cid_value, "No emulated CID available for remapping"

        # ----------------------------------------------------------------------------
        LogHelper.log_step(
            self,
            f'Send setCidReporting request with CID = {new_cid_value} and set remap = {CidTable.SMART_SHIFT} and all '
            f'other parameters = 0')
        # ----------------------------------------------------------------------------
        set_cid_reporting = feature_1b04.set_cid_reporting_cls(
            self.deviceIndex, feature_1b04_index, ctrl_id=new_cid_value, remap=CidTable.SMART_SHIFT)

        set_cid_reporting_resp = self.send_report_wait_response(
            report=set_cid_reporting,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=feature_1b04.set_cid_reporting_response_cls)

        try:
            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs ')
            # ----------------------------------------------------------------------------
            self.assertEqual(int(Numeral(new_cid_value)),
                             int(Numeral(set_cid_reporting_resp.ctrl_id)),
                             "setCidReporting response cid should echo the request")
            self.assertEqual(CidTable.SMART_SHIFT, int(Numeral(set_cid_reporting_resp.remap)),
                             "setCidReporting response remap should echo the request")

            # ----------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over valid wheelMode values')
            # ----------------------------------------------------------------------------
            for wheel_mode in wheel_mode_to_state:
                # ----------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode}')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, wheel_mode)

                # ----------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f'Validate receive ratchetSwitch event with state = {wheel_mode_to_state[wheel_mode]}')
                # ----------------------------------------------------------------------------
                ratchet_switch_evt = self.getMessage(queue=self.hidDispatcher.event_message_queue,
                                                     class_type=feature_2121.ratchet_switch_event_cls)
                self.assertEqual(wheel_mode_to_state[wheel_mode], ratchet_switch_evt.state,
                                 f'Ratchet state should be {wheel_mode_to_state[wheel_mode]}')

                # ----------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send CID = {new_cid_value} key press stimulus to DUT')
                # ----------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(CID_TO_KEY_ID_MAP[new_cid_value])
                sleep(0.2)

                # ----------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and other parameters to 0')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, wheel_mode)

                # ----------------------------------------------------------------------------
                LogHelper.log_step(
                    self,
                    f'Simulate SmartShift button release by sending CID = {new_cid_value} key release stimulus to DUT')
                # ----------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(CID_TO_KEY_ID_MAP[new_cid_value])

                if wheel_mode == SmartShiftTunable.WheelModeConst.RATCHET:
                    other_mode = SmartShiftTunable.WheelModeConst.FREESPIN
                else:
                    other_mode = SmartShiftTunable.WheelModeConst.RATCHET
                # end if

                # ----------------------------------------------------------------------------
                LogHelper.log_check(
                    self,
                    f'Validate receive 2 ratchetSwitch event in the right order: {wheel_mode_to_state[other_mode]} '
                    f'then {wheel_mode_to_state[wheel_mode]}')
                # ----------------------------------------------------------------------------
                ratchet_switch_evt = self.getMessage(queue=self.hidDispatcher.event_message_queue,
                                                     class_type=feature_2121.ratchet_switch_event_cls)
                self.assertEqual(wheel_mode_to_state[other_mode], ratchet_switch_evt.state,
                                 f'Ratchet state should be {wheel_mode_to_state[other_mode]}')

                ratchet_switch_evt = self.getMessage(queue=self.hidDispatcher.event_message_queue,
                                                     class_type=feature_2121.ratchet_switch_event_cls)
                self.assertEqual(wheel_mode_to_state[wheel_mode], ratchet_switch_evt.state,
                                 f'Ratchet state should be {wheel_mode_to_state[wheel_mode]}')

                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, f'Send getRatchetControlMode validate response.wheelMode = {wheel_mode}')
                # ----------------------------------------------------------------------------
                SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, wheel_mode)
            # end for
            # ----------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------
        finally:
            # ----------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Reload and verify the value stored during pre-requisite')
            # ----------------------------------------------------------------------------
            SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(self, initial_config.wheel_mode)

            final_config = SmartShiftTunableTestUtils.HIDppHelper.get_ratchet_control_mode_response(self)
            self.assertEqual(final_config, initial_config, "Final configuration should be same as initial")
        # end try

        self.testCaseChecked("FUN_2111_0020")
    # end def test_set_ratchet_control_mode_while_remapped_button_pressed

    @features('Feature2111')
    @features('Feature1805')
    @features('Feature1E00')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_oob_state(self):
        """
        Sending OOB reset using 0x1805 shall put all the parameters in OOB
        """
        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)
        # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
        self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
            test_case=self, memory_manager=self.device_memory_manager)
        self.post_requisite_reload_nvs = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Cleanup receiver pairing data")
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable Hidden Features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Send setRatchetControlMode to set wheel mode, autoDisengage and currentTunableTorque to new values')
        # ----------------------------------------------------------------------------
        if self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_WheelModeDefault == \
                SmartShiftTunable.WheelModeConst.RATCHET:
            new_wheel_mode = SmartShiftTunable.WheelModeConst.FREESPIN
        else:
            new_wheel_mode = SmartShiftTunable.WheelModeConst.RATCHET
        # end if

        new_auto_disengage = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_AutoDisengageDefault + 1
        new_current_tunable_torque = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_DefaultTunableTorque + 1

        SmartShiftTunableTestUtils.HIDppHelper.set_control_mode_configuration(
            self, new_wheel_mode, new_auto_disengage, new_current_tunable_torque)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send 0x1805 - setOobState to restore default parameters')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        self.hardware_reset()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # ---------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # ---------------------------------------------------------------------------
        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
        # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
        # previous events
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=DeviceConnection,
            channel=self.current_channel)
        pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address)

        DeviceManagerUtils.set_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot),
            open_channel=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode to get parameters values')
        # ----------------------------------------------------------------------------
        get_ratchet_control_mode = self.feature_2111.get_ratchet_control_mode_cls(self.deviceIndex,
                                                                                  self.feature_2111_index)
        get_ratchet_control_mode_response = self.send_report_wait_response(
            report=get_ratchet_control_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=self.feature_2111.get_ratchet_control_mode_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check parameters are equal to default value')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_fields(
            self,
            get_ratchet_control_mode_response,
            self.feature_2111.get_ratchet_control_mode_response_cls)

        self.testCaseChecked("FUN_2111_0021")
    # end def test_oob_state

    @features('Feature2111')
    @features('Feature2121')
    @level('Functionality')
    @services('EmulatedKeys', (CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT],))
    def test_multiple_button_press(self):
        """
        Pressing the ratchet control button multiple time shall change the wheel mode, with respect to the number of
        button press:
        - even number of key pressed in less than 0.5s -> no change
        - odd number in 0.5s -> mode switched
        0x2121 event shall be triggered at each mode change, i.e. at each button press
        """
        repetition_base = 10

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature HiRes Wheel (0x2121)')
        # ----------------------------------------------------------------------------
        feature_2121_index, feature_2121, _, _ = SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self, HiResWheel.FEATURE_ID, HiResWheelFactory)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Wheel mode is ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode_ratchet(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Press ratchet control button 2*N times (even number)')
        # ----------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT], repeat=2 * repetition_base)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is ratchet mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, SmartShiftTunable.WheelModeConst.RATCHET)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check 2*N 0x2121 events have been received')
        # ----------------------------------------------------------------------------
        ratchet_switch_events = []
        message = self.get_first_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                                       class_type=feature_2121.ratchet_switch_event_cls,
                                                       allow_no_message=True)
        while message is not None:
            ratchet_switch_events.append(message)
            message = self.get_first_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                                           class_type=feature_2121.ratchet_switch_event_cls,
                                                           allow_no_message=True)
        # end while
        self.assertEqual(2 * repetition_base, len(ratchet_switch_events),
                         "2*N 0x2121 ratchetSwitch events should have been received")

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Press ratchet control button 2*N+1 (odd number)')
        # ----------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[CidTable.SMART_SHIFT], repeat=2 * repetition_base + 1)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Send getRatchetControlMode to check wheel mode is freespin mode')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, SmartShiftTunable.WheelModeConst.FREESPIN)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check 2*N+1 0x2121 events have been received')
        # ----------------------------------------------------------------------------
        ratchet_switch_events = []
        message = self.get_first_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                                       class_type=feature_2121.ratchet_switch_event_cls,
                                                       allow_no_message=True)
        while message is not None:
            ratchet_switch_events.append(message)
            message = self.get_first_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                                           class_type=feature_2121.ratchet_switch_event_cls,
                                                           allow_no_message=True)
        # end while
        self.assertEqual(2 * repetition_base + 1, len(ratchet_switch_events),
                         "2*N+1 0x2121 ratchetSwitch events should have been received")

        self.testCaseChecked("FUN_2111_0022")
    # end def test_multiple_button_press

    @features('Feature2111')
    @features('BLEDevicePairing')
    @level('Functionality')
    @services('MultiHost')
    def test_change_host(self):
        """
        Smart Shift configuration shall be kept from one host to the other
        """
        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair device to all available receivers')
        # ---------------------------------------------------------------------------
        # Cleanup all pairing slots except the first one
        CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        ble_pro_receiver_port_indexes = ReceiverTestUtils.get_receiver_port_indexes(
            self,
            ReceiverTestUtils.USB_PID_MEZZY_BLE_PRO,
            skip=[ChannelUtils.get_port_index(test_case=self)])

        self.post_requisite_reconnect_first_receiver = True
        device_slot = 1
        dispatcher_to_dump = self.current_channel.hid_dispatcher
        for index in ble_pro_receiver_port_indexes:
            DevicePairingTestUtils.pair_device_slot_to_other_receiver(
                test_case=self,
                device_slot=device_slot,
                other_receiver_port_index=index,
                hid_dispatcher_to_dump=dispatcher_to_dump)
            device_slot += 1
        # end for

        # Reconnect with the first receiver
        ReceiverTestUtils.switch_to_receiver(
            self, receiver_port_index=ChannelUtils.get_port_index(test_case=self, channel=self.backup_dut_channel))

        # Change host on Device
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1814)')
        # ---------------------------------------------------------------------------
        feature_1814_index = self.updateFeatureMapping(feature_id=ChangeHost.FEATURE_ID)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send setRatchetControlMode from first host to set new values')
        # ----------------------------------------------------------------------------
        if self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_WheelModeDefault == \
                SmartShiftTunable.WheelModeConst.RATCHET:
            new_wheel_mode = SmartShiftTunable.WheelModeConst.FREESPIN
        else:
            new_wheel_mode = SmartShiftTunable.WheelModeConst.RATCHET
        # end if

        new_auto_disengage = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_AutoDisengageDefault + 1
        new_current_tunable_torque = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_DefaultTunableTorque + 1

        SmartShiftTunableTestUtils.HIDppHelper.set_control_mode_configuration(
            self, new_wheel_mode, new_auto_disengage, new_current_tunable_torque)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a ChangeHost request to switch to the next receiver')
        # ---------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(self,
                                                         device_index=self.deviceIndex,
                                                         host_index=1)

        secondary_receiver_port_index = ble_pro_receiver_port_indexes[0]
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Switch communication channel to receiver on port {secondary_receiver_port_index}')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.switch_to_receiver(self, secondary_receiver_port_index)
        SmartShiftTunableTestUtils.HIDppHelper.get_parameters(
            self,
            SmartShiftTunable.FEATURE_ID,
            SmartShiftTunableFactory,
            device_index=1,  # Device index on secondary receiver should be 1
            port_index=secondary_receiver_port_index)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(
            self,
            'Send getRatchetControlMode with second host to check values are equal to the one set by the first host')
        # ----------------------------------------------------------------------------
        get_ratchet_control_mode = self.feature_2111.get_ratchet_control_mode_cls(self.deviceIndex,
                                                                                  self.feature_2111_index)
        get_ratchet_control_mode_response = self.send_report_wait_response(
            report=get_ratchet_control_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=self.feature_2111.get_ratchet_control_mode_response_cls)

        check_map = {
            "wheel_mode": (SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_wheel_mode,
                           new_wheel_mode),
            "auto_disengage": (SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_auto_disengage,
                               new_auto_disengage),
            "current_tunable_torque": (
                SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_current_tunable_torque,
                new_current_tunable_torque)
        }

        SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_fields(
            self,
            get_ratchet_control_mode_response,
            self.feature_2111.get_ratchet_control_mode_response_cls,
            check_map)

        self.testCaseChecked("FUN_2111_0023")
    # end def test_change_host
# end class SmartShiftTunableFunctionalityTestCase


class SmartShiftTunableFunctionalityResetTestCase(SmartShiftTunableBaseTestCase):
    """
    Reset (HID Reset / Hardware reset / battery unplug-plug) shall not change the persistent values (wheel mode,
    autoDisengage and currentTunableTorque)
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        # Start with super setUp()
        super().setUp()

        if self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_WheelModeDefault == \
                SmartShiftTunable.WheelModeConst.RATCHET:
            self.new_wheel_mode = SmartShiftTunable.WheelModeConst.FREESPIN
        else:
            self.new_wheel_mode = SmartShiftTunable.WheelModeConst.RATCHET
        # end if

        self.new_auto_disengage = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_AutoDisengageDefault + 1
        self.new_current_tunable_torque = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_DefaultTunableTorque + 1

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Send setRatchetControlMode to set wheel mode, autoDisengage and currentTunableTorque to new values')
        # ----------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_control_mode_configuration(
            self,
            wheel_mode=self.new_wheel_mode,
            auto_disengage=self.new_auto_disengage,
            current_tunable_torque=self.new_current_tunable_torque)
    # end def setUp

    @features('Feature2111')
    @features('Feature1802')
    @level('Functionality')
    def test_configuration_persistent_to_hid_reset(self):
        """
        Parameters should be persistent to HID reset
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get Device Reset (0x1802) feature index')
        # ----------------------------------------------------------------------------
        device_reset_index = self.updateFeatureMapping(DeviceReset.FEATURE_ID)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable Hidden Features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        force_device_reset = ForceDeviceReset(self.deviceIndex, device_reset_index)
        self.send_report_to_device(report=force_device_reset)
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
        self._check_parameters_after_reset()
        self.testCaseChecked("FUN_2111_0001#1")
    # end def test_configuration_persistent_to_hid_reset

    @features('Feature2111')
    @level('Functionality')
    @services('PowerSwitch')
    def test_configuration_persistent_to_hw_reset(self):
        """
        Parameters should be persistent to Hardware reset
        """
        self.power_switch_emulator.switch_off_on()
        self.reset(hardware_reset=False)
        self._check_parameters_after_reset()
        self.testCaseChecked("FUN_2111_0001#2")
    # end def test_configuration_persistent_to_hw_reset

    @features('Feature2111')
    @level('Functionality')
    @services('PowerSupply')
    def test_configuration_persistent_to_pwr_reset(self):
        """
        Parameters should be persistent to Power reset
        """
        self.reset(hardware_reset=True)
        self._check_parameters_after_reset()
        self.testCaseChecked("FUN_2111_0001#3")
    # end def test_configuration_persistent_to_pwr_reset

    def _check_parameters_after_reset(self):
        """
        Common check to all tests : check the parameters after reset
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Send getRatchetControlMode to check parameters have the new values')
        # ----------------------------------------------------------------------------
        get_ratchet_control_mode_resp = SmartShiftTunableTestUtils.HIDppHelper.get_ratchet_control_mode_response(self)

        SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_wheel_mode(
            self, get_ratchet_control_mode_resp, self.new_wheel_mode)
        SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_auto_disengage(
            self, get_ratchet_control_mode_resp, self.new_auto_disengage)
        SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_current_tunable_torque(
            self, get_ratchet_control_mode_resp, self.new_current_tunable_torque)
    # end def _check_parameters_after_reset
# end class SmartShiftTunableFunctionalityResetTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
