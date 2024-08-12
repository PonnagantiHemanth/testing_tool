# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: pytestbox.hid.mouse.feature_2110_functionality
:brief: Validate HID mouse feature 0x2110 functionality test cases
:author: Fred Chen <fchen7@logitech.com>
:date: 2019/08/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randrange

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtons
from pyhid.hidpp.features.devicereset import DeviceReset
from pyhid.hidpp.features.hireswheel import HiResWheel
from pyhid.hidpp.features.hireswheel import RatchetSwitchEvent
from pyhid.hidpp.features.mouse.smartshift import SetRatchetControlMode
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.mouse.feature_2110_interface import DONOTCHANGE
from pytestbox.device.hidpp20.mouse.feature_2110_interface import FREESPIN
from pytestbox.device.hidpp20.mouse.feature_2110_interface import RATCHET
from pytestbox.device.hidpp20.mouse.feature_2110_interface import SmartShiftBaseClassTestCase
from pytestbox.device.hidpp20.mouse.feature_2110_interface import check_ratchet_switch_event
from pytestbox.device.hidpp20.mouse.feature_2110_interface import divert_button
from pytestbox.device.hidpp20.mouse.feature_2110_interface import get_1b04_classes
from pytestbox.device.hidpp20.mouse.feature_2110_interface import get_cids_can_remap_to_c4
from pytestbox.device.hidpp20.mouse.feature_2110_interface import get_cids_for_c4_can_remap_to
from pytestbox.device.hidpp20.mouse.feature_2110_interface import get_ratchet_control_mode
from pytestbox.device.hidpp20.mouse.feature_2110_interface import remap_button
from pytestbox.device.hidpp20.mouse.feature_2110_interface import reset_device_by_x1802
from pytestbox.device.hidpp20.mouse.feature_2110_interface import set_ratchet_control_mode
from pytestbox.device.hidpp20.mouse.feature_2110_interface import verify_divert_button
from pytestbox.device.hidpp20.mouse.feature_2110_interface import verify_divert_event
from pytestbox.device.hidpp20.mouse.feature_2110_interface import verify_keystroke
from pytestbox.device.hidpp20.mouse.feature_2110_interface import verify_ratchet_control_mode
from pytestbox.device.hidpp20.mouse.feature_2110_interface import verify_remap_button


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SmartShiftFunctionalityTestCase(SmartShiftBaseClassTestCase):
    """
    Validate SmartShift Functionality TestCases
    """

    @features('Feature2110')
    @features('Feature2121')
    @level('Business')
    def test_WheelModeBusinessCase(self):
        """
        Validate setRatchetControlMode.wheelMode business case : check changing wheel mode value

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2121)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=HiResWheel.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over wheelMode valid range')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        check_list_1 = [DONOTCHANGE, RATCHET, FREESPIN, DONOTCHANGE, FREESPIN, RATCHET]  # 0, 2, 1, 0, 1, 2
        check_list_2 = [DONOTCHANGE, FREESPIN, RATCHET, DONOTCHANGE, RATCHET, FREESPIN]  # 0, 1, 2, 0, 2, 1
        test_wheel_mode_list = check_list_1 if int(Numeral(self.cur_settings.wheel_mode)) is RATCHET \
            else check_list_2
        prev_wheel_mode = int(Numeral(self.cur_settings.wheel_mode))
        for wheel_mode in test_wheel_mode_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and other parameters '
                                     'to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate receive ratchetSwitch event with state = {wheel_mode - 1}  if wheel '
                                      'mode changes, otherwise no event')
            # ----------------------------------------------------------------------------------------------------------
            if wheel_mode != DONOTCHANGE and prev_wheel_mode != wheel_mode:
                check_ratchet_switch_event(test_case=self, wheel_mode=wheel_mode)
                prev_wheel_mode = wheel_mode
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0003")
    # end def test_WheelModeBusinessCase

    @features('Feature2110')
    @level('Business')
    def test_AutoDisengageBusinessCase(self):
        """
        Validate setRatchetControlMode.autoDisengage business case : check changing auto
        ratchet disengage value

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over autoDisengage valid range (only some interesting values)')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for auto_disengage in [1, 2, 3, 4, 8, 15, 16, 31, 32, 63, 64, 127, 128, 254, 255]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with autoDisengage = {auto_disengage} and other '
                                     'parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, auto_disengage=auto_disengage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, auto_disengage=auto_disengage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            tmp_settings = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.autoDisengage = {auto_disengage}')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=tmp_settings,
                                        wheel_mode=self.cur_settings.wheel_mode,
                                        auto_disengage=auto_disengage,
                                        auto_disengage_default=self.cur_settings.auto_disengage_default)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0004")
    # end def test_AutoDisengageBusinessCase

    @features('Feature2110')
    @level('Business')
    def test_AutoDisengageDefaultBusinessCase(self):
        """
        Validate setRatchetControlMode.autoDisengageDefault business case : check changing auto
        ratchet disengage default value

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over autoDisengageDefault valid range (only some interesting values)')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for auto_disengage_default in [1, 2, 3, 4, 8, 15, 16, 31, 32, 63, 64, 127, 128, 254, 255]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setRatchetControlMode with autoDisengageDefault = '
                                     f'{auto_disengage_default} and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response,
                                        auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            tmp_settings = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.autoDisengageDefault = {auto_disengage_default}')
            # ----------------------------------------------------------------------------------------------------------
            """
            It has been observed by test that the auto_disengage is also changed when auto_disengage_default 
            is changed. Since it is not specified, we need confirmation on this behaviour.
            """
            verify_ratchet_control_mode(test_case=self,
                                        response=tmp_settings,
                                        wheel_mode=self.cur_settings.wheel_mode,
                                        auto_disengage=auto_disengage_default,
                                        auto_disengage_default=auto_disengage_default)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0005")
    # end def test_AutoDisengageDefaultBusinessCase

    @features('Feature2110')
    @level('Functionality')
    def test_SetRatchetControlMode_WithAllZero(self):
        """
        Validate setRatchetControlMode with all parameters to 0 does not change the configuration

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode and store configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode with the values to 0')
        # --------------------------------------------------------------------------------------------------------------
        response = set_ratchet_control_mode(test_case=self, wheel_mode=DONOTCHANGE, auto_disengage=DONOTCHANGE,
                                            auto_disengage_default=DONOTCHANGE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate returned values are the echo of the request')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode')
        # --------------------------------------------------------------------------------------------------------------
        tmp_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate configuration didn\'t change from the stored one')
        # --------------------------------------------------------------------------------------------------------------
        verify_ratchet_control_mode(test_case=self,
                                    response=tmp_settings,
                                    wheel_mode=self.cur_settings.wheel_mode,
                                    auto_disengage=self.cur_settings.auto_disengage,
                                    auto_disengage_default=self.cur_settings.auto_disengage_default)

        self.testCaseChecked("FNT_2110_0006")
    # end def test_SetRatchetControlMode_WithAllZero

    @features('Feature2110')
    @level('Functionality')
    @services('RatchetSpy')
    def test_ValidateRatchetDisengaged_IfUnderFreeWheelMode(self):
        """
        Validate ratchet not engage when Inputs.wheelMode = 1 using EPM drive

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode with wheelMode = 1 and other parameters to 0')
        # --------------------------------------------------------------------------------------------------------------
        response = set_ratchet_control_mode(test_case=self, wheel_mode=FREESPIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate returned values are the echo of the request')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=FREESPIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate ratchet not engaged using Ratchet Spy')
        # --------------------------------------------------------------------------------------------------------------
        # todo

        self.testCaseChecked("FNT_2110_0007")
    # den def test_ValidateRatchetDisengaged_IfUnderFreeWheelMode

    @features('Feature2110')
    @level('Functionality')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetEngaged_IfWheelSlowerThanAutoDisengage(self):
        """
        Validate ratchet engaged when Inputs.wheelMode = 2 and wheel movement slower than autoDisengage

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode with wheelMode = 2 and other parameters to 0')
        # --------------------------------------------------------------------------------------------------------------
        response = set_ratchet_control_mode(test_case=self, wheel_mode=RATCHET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate returned values are the echo of the request')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate wheel movement slower than the autoDisengage')
        # --------------------------------------------------------------------------------------------------------------
        # todo

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate ratchet engaged using Ratchet Spy')
        # --------------------------------------------------------------------------------------------------------------
        # todo

        self.testCaseChecked("FNT_2110_0008")
    # end def test_ValidateRatchetEngaged_IfWheelSlowerThanAutoDisengage

    @features('Feature2110')
    @level('Functionality')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetEngaged_IfWheelSlowerThanAutoDisengageOnLimitValues(self):
        """
        @tc_synopsis Check ratchet engaged when Inputs.wheelMode = 2 and wheel slower than autoDisengage on limit values

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over autoDisengage in [0x01, 0xFE]')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for auto_disengage in [0x01, 0xFE]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setRatchetControlMode with wheelMode = 2, autoDisengage = '
                                     f'{auto_disengage} and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=RATCHET, auto_disengage=auto_disengage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET,
                                        auto_disengage=auto_disengage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Emulate wheel movement slower than the autoDisengage')
            # ----------------------------------------------------------------------------------------------------------
            # todo

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate ratchet engaged using Ratchet Spy')
            # ----------------------------------------------------------------------------------------------------------
            # todo

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0009")
    # end def test_ValidateRatchetEngaged_IfWheelSlowerThanAutoDisengageOnLimitValues

    @features('Feature2110')
    @level('Functionality')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetDisengaged_IfWheelFasterThanAutoDisengage(self):
        """
        Validate ratchet not engaged when Inputs.wheelMode = 2 and wheel faster than autoDisengage

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, ' Send setRatchetControlMode with wheelMode = 2 and other parameters to 0')
        # --------------------------------------------------------------------------------------------------------------
        response = set_ratchet_control_mode(test_case=self, wheel_mode=RATCHET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate returned values are the echo of the request')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate wheel movement faster than the autoDisengage')
        # --------------------------------------------------------------------------------------------------------------
        # todo

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate ratchet not engaged using Ratchet Spy')
        # --------------------------------------------------------------------------------------------------------------
        # todo

        self.testCaseChecked("FNT_2110_0010")
    # end def test_ValidateRatchetDisengaged_IfWheelFasterThanAutoDisengage

    @features('Feature2110')
    @level('Functionality')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetDisengaged_IfWheelFasterThanAutoDisengageOnLimitValues(self):
        """
        Validate ratchet not engaged when Inputs.wheelMode = 2 and wheel faster than autoDisengage
         on limit values

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over autoDisengage in [0x01, 0xFE]')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for auto_disengage in [0x01, 0xFE]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setRatchetControlMode with wheelMode = 2, autoDisengage = '
                                     f'{auto_disengage} and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=RATCHET, auto_disengage=auto_disengage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET,
                                        auto_disengage=auto_disengage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Emulate wheel movement faster than the autoDisengage')
            # ----------------------------------------------------------------------------------------------------------
            # todo

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate ratchet not engaged using Ratchet Spy')
            # ----------------------------------------------------------------------------------------------------------
            # todo

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0011")
    # end def test_ValidateRatchetDisengaged_IfWheelFasterThanAutoDisengageOnLimitValues

    @features('Feature2110')
    @level('Functionality')
    @services('MainWheel')
    @services('RatchetSpy')
    def test_ValidateRatchetEngaged_IfAutoDisengageIs0xFF(self):
        """
        Validate ratchet engaged when Inputs.wheelMode = 2, Inputs.autoDisengage = 0xFF and wheel
         at whatever speed

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, ' Send setRatchetControlMode with wheelMode = 2, autoDisengage = 0xFF and'
                                 ' autoDisengageDefault = 0')
        # --------------------------------------------------------------------------------------------------------------
        response = set_ratchet_control_mode(test_case=self, wheel_mode=RATCHET, auto_disengage=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate returned values are the echo of the request')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=RATCHET, auto_disengage=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over wheel movement speed (only some interesting values)')
        # --------------------------------------------------------------------------------------------------------------
        for wheel_movement in compute_sup_values(HexList(Numeral(0x00, SetRatchetControlMode.LEN.AUTO_DISENGAGE // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate wheel movement = {wheel_movement}')
            # ----------------------------------------------------------------------------------------------------------
            # todo

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate ratchet engaged using Ratchet Spy')
            # ----------------------------------------------------------------------------------------------------------
            # todo

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0012")
    # end def test_ValidateRatchetEngaged_IfAutoDisengageIs0xFF

    @features('Feature2110')
    @features('Feature2121')
    @level('Functionality')
    def test_ValidateWheelModeNotChanged_IfAutoDisengageChanged(self):
        """
        Validate setRatchetControlMode.autoDisengage does not trigger a wheelMode change

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2121)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=HiResWheel.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over wheelMode valid range')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        test_wheel_mode_list = [FREESPIN, RATCHET] \
            if int(Numeral(self.cur_settings.wheel_mode)) is RATCHET else [RATCHET, FREESPIN]
        for wheel_mode in test_wheel_mode_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and other '
                                     'parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate receive ratchetSwitch event with state = {wheel_mode - 1}')
            # ----------------------------------------------------------------------------------------------------------
            check_ratchet_switch_event(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Sub-Loop over autoDisengage valid range (only some interesting values)')
            # ----------------------------------------------------------------------------------------------------------
            for auto_disengage in compute_sup_values(
                    HexList(Numeral(0x00, SetRatchetControlMode.LEN.AUTO_DISENGAGE // 8))):
                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send setRatchetControlMode with autoDisengage = {auto_disengage} and '
                                         'other parameters to 0')
                # ----------------------------------------------------------------------------------------------------------
                response = set_ratchet_control_mode(test_case=self, auto_disengage=auto_disengage)

                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate returned values are the echo of the request')
                # ----------------------------------------------------------------------------------------------------------
                verify_ratchet_control_mode(test_case=self, response=response, auto_disengage=auto_disengage)

                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send getRatchetControlMode')
                # ----------------------------------------------------------------------------------------------------------
                tmp_settings = get_ratchet_control_mode(test_case=self)

                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Validate response.wheelMode = {wheel_mode}')
                # ----------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=wheel_mode,
                                 obtained=int(Numeral(tmp_settings.wheel_mode)),
                                 msg='The wheel_mode parameter differs from the one expected')

                # ----------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate did not receive ratchetSwitch event')
                # ----------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                               timeout=.4, class_type=RatchetSwitchEvent)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Sub-Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0013")
    # end def test_ValidateWheelModeNotChanged_IfAutoDisengageChanged

    @features('Feature2110')
    @features('Feature2121')
    @level('Functionality')
    @services('ButtonPressed')
    def test_ValidateWheelModeChanged_BySmartShiftBtn(self):
        """
        Validate changes of wheel mode when smartshift button is triggered

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2121)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=HiResWheel.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop 2 times')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for _ in range(2):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode and store wheelMode')
            # ----------------------------------------------------------------------------------------------------------
            before_settings = get_ratchet_control_mode(test_case=self)
            expected_wheel_mode = FREESPIN if int(Numeral(before_settings.wheel_mode)) is RATCHET else RATCHET

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Simulate SmartShift button click by sending CID = 0xC4 key press and released'
                                     ' stimulus to DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[0xC4])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate receive ratchetSwitch event with state is not the one previously'
                                      ' stored')
            # ----------------------------------------------------------------------------------------------------------
            check_ratchet_switch_event(test_case=self, wheel_mode=expected_wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            after_settings = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate response.wheelMode goes back and forth between \'Freespin\' and '
                                      '\'Ratchet\'')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=after_settings,
                                        wheel_mode=expected_wheel_mode,
                                        auto_disengage=self.cur_settings.auto_disengage,
                                        auto_disengage_default=self.cur_settings.auto_disengage_default)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0014")
    # end def test_ValidateWheelModeChanged_BySmartShiftBtn

    @features('Feature2110')
    @features('Feature2121')
    @level('Functionality')
    @services('ButtonPressed')
    def test_ValidateWheelModeChanged_BySmartShiftBtnAndAPI(self):
        """
        @tc_synopsis Changes of wheel mode when smartshift button is pressed, then setRatchetControlMode and
         then smartshift button is released

        Check with 0x2121 event and getRatchetControlMode

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2121)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=HiResWheel.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over valid wheelMode values')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        test_wheel_mode_list = [FREESPIN, RATCHET] \
            if int(Numeral(self.cur_settings.wheel_mode)) is RATCHET else [RATCHET, FREESPIN]
        for wheel_mode in test_wheel_mode_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and other '
                                     'parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request ')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate receive ratchetSwitch event with state = {wheel_mode - 1}')
            # ----------------------------------------------------------------------------------------------------------
            check_ratchet_switch_event(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Simulate SmartShift button press by sending CID = 0xC4 key press stimulus '
                                     'to DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(CID_TO_KEY_ID_MAP[0xC4])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and other '
                                     'parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request ')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Simulate SmartShift button release by sending CID = 0xC4 key release stimulus '
                                     'to DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(CID_TO_KEY_ID_MAP[0xC4])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate receive 2 ratchetSwitch event in the '
                                      f'right order: {(1 if wheel_mode == 2 else 2) - 1} then {wheel_mode -1}')
            # ----------------------------------------------------------------------------------------------------------
            check_ratchet_switch_event(test_case=self, wheel_mode=FREESPIN if wheel_mode is RATCHET else RATCHET)
            check_ratchet_switch_event(test_case=self, wheel_mode=RATCHET if wheel_mode is RATCHET else FREESPIN)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            after_settings = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.wheelMode = {wheel_mode}')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=after_settings,
                                        wheel_mode=wheel_mode,
                                        auto_disengage=self.cur_settings.auto_disengage,
                                        auto_disengage_default=self.cur_settings.auto_disengage_default)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0015")
    # end def test_ValidateWheelModeChanged_BySmartShiftBtnAndAPI

    @features('Feature2110')
    @features('Feature2121')
    @features('Feature1B04V1+')
    @level('Functionality')
    @services('ButtonPressed')
    def test_ValidateWheelModeChanged_ByButtonRemappedToSmartShiftBtn(self):
        """
        Validate changes of wheel mode when button remapped on smartshift is triggered

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault
        """
        # Get the supported version
        self.get_cid_info_response_class, self.set_cid_reporting_class, self.set_cid_reporting_response_class = \
            get_1b04_classes(test=self)

        # Get the CID list where supported remap to C4
        cids_can_remap_to_c4 = get_cids_can_remap_to_c4(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2121)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=HiResWheel.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1B04)')
        # --------------------------------------------------------------------------------------------------------------
        self.specialkeysmousebuttons_feature_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=SpecialKeysMSEButtons.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cids_can_remap_to_c4[0]} and '
                                 'set remap = 0xC4 and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting_response = remap_button(test_case=self,
                                                  cid=cids_can_remap_to_c4[0],
                                                  remap_id=0xC4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_remap = True
        self.teardown_restore_remap_cid = cids_can_remap_to_c4[0]
        self.teardown_restore_remap_remapped_cid = cids_can_remap_to_c4[0]
        verify_remap_button(test_case=self,
                            response=set_cid_reporting_response,
                            expected_cid=cids_can_remap_to_c4[0],
                            expected_remap_cid=0xC4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop 2 times')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for _ in range(2):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode and store wheelMode')
            # ----------------------------------------------------------------------------------------------------------
            stored_settings = get_ratchet_control_mode(test_case=self)
            expected_wheel_mode = FREESPIN if int(Numeral(stored_settings.wheel_mode)) is RATCHET else RATCHET

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send CID = {cids_can_remap_to_c4[0]} key pressed and '
                                     'released stimulus to DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[int(Numeral(cids_can_remap_to_c4[0]))])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate receive ratchetSwitch event with state is not the one previously'
                                      ' stored')
            # ----------------------------------------------------------------------------------------------------------
            check_ratchet_switch_event(test_case=self, wheel_mode=expected_wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            check_settings = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate response.wheelMode goes back and forth between \'Freespin\' and'
                                      ' \'Ratchet\'')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=expected_wheel_mode,
                             obtained=int(Numeral(check_settings.wheel_mode)),
                             msg='The wheel_mode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0016")
    # end def test_ValidateWheelModeChanged_ByButtonRemappedToSmartShiftBtn

    @features('Feature2110')
    @features('Feature2121')
    @features('Feature1B04V1+')
    @level('Functionality')
    @services('ButtonPressed')
    def test_ValidateWheelModeChanged_ByButtonRemappedToSmartShiftBtnAndAPI(self):
        """
        @tc_synopsis Changes of wheel mode when button remapped on smartshift is pressed, then setRatchetControlMode
         and then button remapped on smartshift is released

        Check with 0x2121 event and getRatchetControlMode

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # Get the supported version
        self.get_cid_info_response_class, self.set_cid_reporting_class, self.set_cid_reporting_response_class = \
            get_1b04_classes(test=self)

        # Get the CID list where supported remap to C4
        cids_can_remap_to_c4 = get_cids_can_remap_to_c4(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2121)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=HiResWheel.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1B04)')
        # --------------------------------------------------------------------------------------------------------------
        self.specialkeysmousebuttons_feature_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=SpecialKeysMSEButtons.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cids_can_remap_to_c4[0]} and set '
                                 'remap = 0xC4 and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting_response = remap_button(test_case=self,
                                                  cid=cids_can_remap_to_c4[0],
                                                  remap_id=0xC4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_remap = True
        self.teardown_restore_remap_cid = cids_can_remap_to_c4[0]
        self.teardown_restore_remap_remapped_cid = cids_can_remap_to_c4[0]
        verify_remap_button(test_case=self,
                            response=set_cid_reporting_response,
                            expected_cid=cids_can_remap_to_c4[0],
                            expected_remap_cid=0xC4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over valid wheelMode values')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        test_wheel_mode_list = [FREESPIN, RATCHET] \
            if int(Numeral(self.cur_settings.wheel_mode)) is RATCHET else [RATCHET, FREESPIN]
        for wheel_mode in test_wheel_mode_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode}')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate receive ratchetSwitch event with state = {wheel_mode - 1}')
            # ----------------------------------------------------------------------------------------------------------
            check_ratchet_switch_event(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send CID = {cids_can_remap_to_c4[0]} key press stimulus to DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(CID_TO_KEY_ID_MAP[int(Numeral(cids_can_remap_to_c4[0]))])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and other parameters '
                                     'to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Simulate SmartShift button release by sending CID = {cids_can_remap_to_c4[0]}'
                                     ' key release stimulus to DUT')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(CID_TO_KEY_ID_MAP[int(Numeral(cids_can_remap_to_c4[0]))])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate receive 2 ratchetSwitch event in the right order: '
                                      f'{(1 if wheel_mode == 2 else 2) - 1} then {wheel_mode - 1}')
            # ----------------------------------------------------------------------------------------------------------
            check_ratchet_switch_event(test_case=self, wheel_mode=FREESPIN if wheel_mode is RATCHET else RATCHET)
            check_ratchet_switch_event(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            response = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.wheelMode = {wheel_mode}')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=wheel_mode,
                                        auto_disengage=self.cur_settings.auto_disengage,
                                        auto_disengage_default=self.cur_settings.auto_disengage_default)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0017")
    # end def test_ValidateWheelModeChanged_ByButtonRemappedToSmartShiftBtnAndAPI

    @features('Feature2110')
    @features('Feature2121')
    @features('Feature1B04V1+')
    @level('Functionality')
    @services('ButtonPressed')
    def test_ValidateWheelModeNotChanged_IfSmartShiftBtnHadRemapped(self):
        """
        Validate no change of wheel mode when smartshift button is triggered and smartshift button
         is remapped

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault
        """
        # Get the supported version
        self.get_cid_info_response_class, self.set_cid_reporting_class, self.set_cid_reporting_response_class =\
            get_1b04_classes(test=self)

        # Get the CID list where CID 0xC4 can be remapped to
        cids_for_c4_can_remap_to = get_cids_for_c4_can_remap_to(test=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2121)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=HiResWheel.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1B04)')
        # --------------------------------------------------------------------------------------------------------------
        self.specialkeysmousebuttons_feature_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=SpecialKeysMSEButtons.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setCidReporting request with CID = 0xC4 and set '
                                 f'remap = {cids_for_c4_can_remap_to[0]} and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting_response = remap_button(test_case=self,
                                                  cid=0xC4,
                                                  remap_id=cids_for_c4_can_remap_to[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs ')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_remap = True
        self.teardown_restore_remap_cid = 0xC4
        self.teardown_restore_remap_remapped_cid = 0xC4
        verify_remap_button(test_case=self,
                            response=set_cid_reporting_response,
                            expected_cid=0xC4,
                            expected_remap_cid=cids_for_c4_can_remap_to[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode and store wheelMode')
        # --------------------------------------------------------------------------------------------------------------
        before_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send CID = 0xC4 key pressed and released stimulus to DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[0xC4])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate receive HID pressed and released for '
                                  f'CID = {cids_for_c4_can_remap_to[0]} (if any necessary)')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_keystroke(test_case=self, cid=cids_for_c4_can_remap_to[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate did not receive ratchetSwitch event')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                       timeout=.4, class_type=RatchetSwitchEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode')
        # --------------------------------------------------------------------------------------------------------------
        after_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate response.wheelMode matches the one previously stored')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=before_settings.wheel_mode,
                         obtained=after_settings.wheel_mode,
                         msg='The wheel_mode parameter differs from the one expected')

        self.testCaseChecked("FNT_2110_0018")
    # end def test_ValidateWheelModeNotChanged_IfSmartShiftBtnHadRemapped

    @features('Feature2110')
    @features('Feature2121')
    @features('Feature1B04')
    @level('Functionality')
    @services('ButtonPressed')
    def test_ValidateWheelModeNotChanged_IfSmartShiftBtnHadDiverted(self):
        """
        Validate no change of wheel mode when smartshift button is triggered and smartshift button
        is diverted

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault
        """
        # Get the supported version
        self.get_cid_info_response_class, self.set_cid_reporting_class, self.set_cid_reporting_response_class =\
            get_1b04_classes(test=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x2121)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=HiResWheel.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1B04)')
        # --------------------------------------------------------------------------------------------------------------
        self.specialkeysmousebuttons_feature_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=SpecialKeysMSEButtons.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setCidReporting request with CID = 0xC4 and set divert = 1, dvalid = 1 and'
                                 ' all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting_response = divert_button(test=self, cid=0xC4, divert_valid=1, divert=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_divert = True
        verify_divert_button(test=self, response=set_cid_reporting_response,
                             expected_cid=0xC4, divert_valid=1, divert=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode and store wheelMode')
        # --------------------------------------------------------------------------------------------------------------
        before_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send CID = 0xC4 key pressed and released stimulus to DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[0xC4])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate received divertedButtonsEvents = make [0xC4, 0, 0, 0] and'
                                  ' break [0, 0, 0, 0]')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_divert_event(test=self, expected_make=[0xC4, 0, 0, 0], expected_break=[0, 0, 0, 0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate did not receive ratchetSwitch event')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                       timeout=.4, class_type=RatchetSwitchEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode')
        # --------------------------------------------------------------------------------------------------------------
        after_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate response.wheelMode matches the one previously stored')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=before_settings.wheel_mode,
                         obtained=after_settings.wheel_mode,
                         msg='The wheel_mode parameter differs from the one expected')

        self.testCaseChecked("FNT_2110_0019")
    # end def test_ValidateWheelModeNotChanged_IfSmartShiftBtnHadDiverted

    @features('Feature2110')
    @level('Functionality')
    @services('PowerSwitch')
    def test_ValidateWheelModeNotChanged_AfterHwReset(self):
        """
        @tc_synopsis No change of wheel mode when hardware reset (power switch)

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over valid wheelMode values')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        test_wheel_mode_list = [FREESPIN, RATCHET] \
            if int(Numeral(self.cur_settings.wheel_mode)) is RATCHET else [RATCHET, FREESPIN]
        for wheel_mode in test_wheel_mode_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and '
                                     'other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send power switch stimuli to trigger a reset')
            # ----------------------------------------------------------------------------------------------------------
            # todo

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            response = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.wheelMode = {wheel_mode}')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=wheel_mode,
                                        auto_disengage=self.cur_settings.auto_disengage,
                                        auto_disengage_default=self.cur_settings.auto_disengage_default)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0021")
    # end def test_ValidateWheelModeNotChanged_AfterHwReset

    @features('Feature2110')
    @level('Functionality')
    @services('PowerSupply')
    def test_ValidateWheelModeNotChanged_AfterPowerReset(self):
        """
        @tc_synopsis No change of wheel mode when battery unplug/replug (power supply)

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over valid wheelMode values')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        test_wheel_mode_list = [FREESPIN, RATCHET] \
            if int(Numeral(self.cur_settings.wheel_mode)) is RATCHET else [RATCHET, FREESPIN]
        for wheel_mode in test_wheel_mode_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and '
                                     'other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request ')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send power supply reset')
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode ')
            # ----------------------------------------------------------------------------------------------------------
            response = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.wheelMode = {wheel_mode}')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=wheel_mode,
                                        auto_disengage=self.cur_settings.auto_disengage,
                                        auto_disengage_default=self.cur_settings.auto_disengage_default)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0022")
    # end def test_ValidateWheelModeNotChanged_AfterPowerReset

    @features('Feature2110')
    @level('Functionality')
    @services('PowerSwitch')
    def test_ValidateAutoDisengageReturnToDefault_AfterHwReset(self):
        """
        @tc_synopsis AutoDisengage return to default when hardware reset (power switch)

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over autoDisengageDefault valid range')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for value in compute_sup_values(HexList(Numeral(0x00, SetRatchetControlMode.LEN.AUTO_DISENGAGE_DEFAULT // 8))):
            auto_disengage_default = int(Numeral(value))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with autoDisengage = '
                                     f'{(auto_disengage_default + 1) % 256}, autoDisengageDefault = '
                                     f'{auto_disengage_default} and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self,
                                                auto_disengage=(auto_disengage_default + 1) % 256,
                                                auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        auto_disengage=(auto_disengage_default + 1) % 256,
                                        auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send power switch stimuli to trigger a reset')
            # ----------------------------------------------------------------------------------------------------------
            # todo

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            response = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.autoDisengage = {auto_disengage_default}')
            # ----------------------------------------------------------------------------------------------------------
            """
            It has been observed by test that the auto_disengage is also changed when auto_disengage_default 
            is changed. Since it is not specified, we need confirmation on this behaviour.
            """
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=self.cur_settings.wheel_mode,
                                        auto_disengage=auto_disengage_default,
                                        auto_disengage_default=auto_disengage_default)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0024")
    # end def test_ValidateAutoDisengageReturnToDefault_AfterHwReset

    @features('Feature2110')
    @level('Functionality')
    @services('PowerSupply')
    def test_ValidateAutoDisengageReturnToDefault_AfterPowerReset(self):
        """
        @tc_synopsis AutoDisengage return to default when battery unplug/replug (power supply)

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over autoDisengageDefault valid range')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        for value in compute_sup_values(HexList(Numeral(0x00, SetRatchetControlMode.LEN.AUTO_DISENGAGE_DEFAULT // 8))):
            auto_disengage_default = int(Numeral(value))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setRatchetControlMode with autoDisengage = '
                                     f'{(auto_disengage_default + 1) % 256}, autoDisengageDefault = '
                                     f'{auto_disengage_default} and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self,
                                                auto_disengage=(auto_disengage_default + 1) % 256,
                                                auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        auto_disengage=(auto_disengage_default + 1) % 256,
                                        auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send power supply reset')
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            response = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.autoDisengage = {auto_disengage_default}')
            # ----------------------------------------------------------------------------------------------------------
            """
            It has been observed by test that the auto_disengage is also changed when auto_disengage_default 
            is changed. Since it is not specified, we need confirmation on this behaviour.
            """
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=self.cur_settings.wheel_mode,
                                        auto_disengage=auto_disengage_default,
                                        auto_disengage_default=auto_disengage_default)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0025")
    # end def test_ValidateAutoDisengageReturnToDefault_AfterPowerReset

    @features('Feature2110')
    @level('Functionality')
    @services('PowerSwitch')
    def test_ValidateAutoDisengageDefaultNotChange_AfterHwReset(self):
        """
        @tc_synopsis No change of AutoDisengageDefault when hardware reset (power switch)

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode with autoDisengageDefault = random([1..254]) and'
                                 ' other parameters to 0')
        # --------------------------------------------------------------------------------------------------------------
        auto_disengage_default = randrange(1, 255)
        response = set_ratchet_control_mode(test_case=self,
                                            auto_disengage_default=auto_disengage_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate returned values are the echo of the request')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self,
                                    response=response,
                                    auto_disengage_default=auto_disengage_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send power switch stimuli to trigger a reset')
        # --------------------------------------------------------------------------------------------------------------
        # todo

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode')
        # --------------------------------------------------------------------------------------------------------------
        response = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate response.autoDisengageDefault did not change')
        # --------------------------------------------------------------------------------------------------------------
        """
        It has been observed by test that the auto_disengage is also changed when auto_disengage_default 
        is changed. Since it is not specified, we need confirmation on this behaviour.
        """
        verify_ratchet_control_mode(test_case=self,
                                    response=response,
                                    wheel_mode=self.cur_settings.wheel_mode,
                                    auto_disengage=auto_disengage_default,
                                    auto_disengage_default=auto_disengage_default)

        self.testCaseChecked("FNT_2110_0027")
    # end def test_ValidateAutoDisengageDefaultNotChange_AfterHwReset

    @features('Feature2110')
    @level('Functionality')
    @services('PowerSupply')
    def test_ValidateAutoDisengageDefaultNotChange_AfterPowerReset(self):
        """
        @tc_synopsis No change of AutoDisengageDefault when battery unplug/replug (power supply)

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode with autoDisengageDefault = random([1..254]) and'
                                 ' other parameters to 0')
        # --------------------------------------------------------------------------------------------------------------
        auto_disengage_default = randrange(1, 255)
        response = set_ratchet_control_mode(test_case=self,
                                            auto_disengage_default=auto_disengage_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate returned values are the echo of the request')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self,
                                    response=response,
                                    auto_disengage_default=auto_disengage_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send power supply reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode')
        # --------------------------------------------------------------------------------------------------------------
        response = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate response.autoDisengageDefault did not change')
        # --------------------------------------------------------------------------------------------------------------
        """
        It has been observed by test that the auto_disengage is also changed when auto_disengage_default 
        is changed. Since it is not specified, we need confirmation on this behaviour.
        """
        verify_ratchet_control_mode(test_case=self,
                                    response=response,
                                    wheel_mode=self.cur_settings.wheel_mode,
                                    auto_disengage=auto_disengage_default,
                                    auto_disengage_default=auto_disengage_default)

        self.testCaseChecked("FNT_2110_0028")
    # end def test_ValidateAutoDisengageDefaultNotChange_AfterPowerReset

    @features('Feature2110')
    @level('Business')
    def test_ValidateParamsCombinatoryLogic(self):
        """
        Validate setRatchetControlMode parameters combinatory logic

        Change wheelMode, autoDisengage and autoDisengageDefault in the same request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over (wheelMode, autoDisengage, autoDisengageDefault) valid range '
                                 '(only some interesting values)')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        prev_wheel_mode = int(Numeral(self.cur_settings.wheel_mode))
        prev_auto_disengage_default = int(Numeral(self.cur_settings.auto_disengage_default))
        for n in range(15):
            wheel_mode = randrange(0, 3)
            auto_disengage = randrange(1, 256)
            auto_disengage_default = randrange(1, 256)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode}, autoDisengage = '
                                     f'{auto_disengage} and autoDisengageDefault = {auto_disengage_default}')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self,
                                                wheel_mode=wheel_mode,
                                                auto_disengage=auto_disengage,
                                                auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=wheel_mode,
                                        auto_disengage=auto_disengage,
                                        auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            response = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.wheelMode = {wheel_mode}, autoDisengage = '
                                      f'{auto_disengage} and autoDisengageDefault = {auto_disengage_default}')
            # ----------------------------------------------------------------------------------------------------------
            """
            It has been observed by test that the auto_disengage is also changed when auto_disengage_default 
            is changed. Since it is not specified, we need confirmation on this behaviour.
            """
            expected_auto_disengage = auto_disengage_default
            if prev_auto_disengage_default == auto_disengage_default:
                expected_auto_disengage = auto_disengage
            else:
                prev_auto_disengage_default = auto_disengage_default
            # end if
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=wheel_mode if wheel_mode != DONOTCHANGE else prev_wheel_mode,
                                        auto_disengage=expected_auto_disengage,
                                        auto_disengage_default=auto_disengage_default)
            if wheel_mode != DONOTCHANGE:
                prev_wheel_mode = wheel_mode
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0029")
    # end def test_ValidateParamsCombinatoryLogic

# end class SmartShiftFunctionalityTestCase


class SmartShiftFunctionalityDeviceResetTestCase(SmartShiftBaseClassTestCase):
    """
    Validates SmartShift Functionality TestCases with a DeviceReset request dependency
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()
    # end def setUp

    @features('Feature2110')
    @features('Feature1E00')
    @features('Feature1802')
    @level('Functionality')
    def test_ValidateWheelModeNotChanged_AfterSwReset(self):
        """
        @tc_synopsis No change of wheel mode when HID reset

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1802)')
        # --------------------------------------------------------------------------------------------------------------
        self.devicereset_feature_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=DeviceReset.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over valid wheelMode values')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        self.teardown_restore_hidden = True
        test_wheel_mode_list = [FREESPIN, RATCHET] \
            if int(Numeral(self.cur_settings.wheel_mode)) is RATCHET else [RATCHET, FREESPIN]
        for wheel_mode in test_wheel_mode_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setRatchetControlMode with wheelMode = {wheel_mode} and '
                                     'other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetEnableHiddenFeatures with enableByte = 1')
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate SetEnableHiddenFeatures response received')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send ForceDeviceReset')
            # ----------------------------------------------------------------------------------------------------------
            reset_device_by_x1802(test=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            response = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.wheelMode = {wheel_mode}')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=wheel_mode,
                                        auto_disengage=self.cur_settings.auto_disengage,
                                        auto_disengage_default=self.cur_settings.auto_disengage_default)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0020")
    # end def test_ValidateWheelModeNotChanged_AfterSwReset

    @features('Feature2110')
    @features('Feature1E00')
    @features('Feature1802')
    @level('Functionality')
    def test_ValidateAutoDisengageReturnToDefault_AfterSwReset(self):
        """
        @tc_synopsis AutoDisengage return to default when HID reset

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1802)')
        # --------------------------------------------------------------------------------------------------------------
        self.devicereset_feature_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=DeviceReset.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over autoDisengageDefault valid range')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        self.teardown_restore_hidden = True
        for value in compute_sup_values(HexList(Numeral(0x00, SetRatchetControlMode.LEN.AUTO_DISENGAGE_DEFAULT // 8))):
            auto_disengage_default = int(Numeral(value))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setRatchetControlMode with autoDisengage = '
                                     f'{(auto_disengage_default + 1) % 256}, autoDisengageDefault = '
                                     f'{auto_disengage_default} and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            response = set_ratchet_control_mode(test_case=self,
                                                auto_disengage=(auto_disengage_default+1) % 256,
                                                auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate returned values are the echo of the request')
            # ----------------------------------------------------------------------------------------------------------
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        auto_disengage=(auto_disengage_default+1) % 256,
                                        auto_disengage_default=auto_disengage_default)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetEnableHiddenFeatures with enableByte = 1')
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate SetEnableHiddenFeatures response received')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send ForceDeviceReset')
            # ----------------------------------------------------------------------------------------------------------
            reset_device_by_x1802(test=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getRatchetControlMode')
            # ----------------------------------------------------------------------------------------------------------
            response = get_ratchet_control_mode(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate response.autoDisengage = {auto_disengage_default}')
            # ----------------------------------------------------------------------------------------------------------
            """
            It has been observed by test that the auto_disengage is also changed when auto_disengage_default 
            is changed. Since it is not specified, we need confirmation on this behaviour.
            """
            verify_ratchet_control_mode(test_case=self,
                                        response=response,
                                        wheel_mode=self.cur_settings.wheel_mode,
                                        auto_disengage=auto_disengage_default,
                                        auto_disengage_default=auto_disengage_default)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_2110_0023")
    # end def test_ValidateAutoDisengageReturnToDefault_AfterSwReset

    @features('Feature2110')
    @features('Feature1E00')
    @features('Feature1802')
    @level('Functionality')
    def test_ValidateAutoDisengageDefaultNotChange_AfterSwReset(self):
        """
        @tc_synopsis No change of AutoDisengageDefault when HID reset

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1802)')
        # --------------------------------------------------------------------------------------------------------------
        self.devicereset_feature_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=DeviceReset.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send getRatchetControlMode to store the current configuration')
        # --------------------------------------------------------------------------------------------------------------
        self.cur_settings = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setRatchetControlMode with autoDisengageDefault = random([1..254]) and'
                                 ' other parameters to 0')
        # --------------------------------------------------------------------------------------------------------------
        auto_disengage_default = randrange(1, 255)
        response = set_ratchet_control_mode(test_case=self,
                                            auto_disengage_default=auto_disengage_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate returned values are the echo of the request')
        # --------------------------------------------------------------------------------------------------------------
        self.teardown_restore_ratchet = True
        verify_ratchet_control_mode(test_case=self,
                                    response=response,
                                    auto_disengage_default=auto_disengage_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetEnableHiddenFeatures with enableByte = 1')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetEnableHiddenFeatures response received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send ForceDeviceReset')
        # --------------------------------------------------------------------------------------------------------------
        reset_device_by_x1802(test=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getRatchetControlMode')
        # --------------------------------------------------------------------------------------------------------------
        response = get_ratchet_control_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate response.autoDisengageDefault did not change')
        # --------------------------------------------------------------------------------------------------------------
        """
        It has been observed by test that the auto_disengage is also changed when auto_disengage_default 
        is changed. Since it is not specified, we need confirmation on this behaviour.
        """
        verify_ratchet_control_mode(test_case=self,
                                    response=response,
                                    wheel_mode=self.cur_settings.wheel_mode,
                                    auto_disengage=auto_disengage_default,
                                    auto_disengage_default=auto_disengage_default)

        self.testCaseChecked("FNT_2110_0026")
    # end def test_ValidateAutoDisengageDefaultNotChange_AfterSwReset

# end class SmartShiftFunctionalityDeviceResetTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
