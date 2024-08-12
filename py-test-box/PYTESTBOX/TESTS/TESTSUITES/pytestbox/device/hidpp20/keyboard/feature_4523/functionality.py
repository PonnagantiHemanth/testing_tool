#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4523.functionality
:brief: HID++ 2.0 ``DisableControlsByCIDX`` functionality test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4523.disablecontrolsbycidx import DisableControlsByCIDXTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDXFunctionalityTestCase(DisableControlsByCIDXTestCase):
    """
    Validate ``DisableControlsByCIDX`` functionality test cases
    """

    def _verify_key_strokes_for_game_mode_and_game_mode_lock(self, game_mode, game_mode_lock):
        """
        Verify key strokes for game mode and game mode lock

        :param  game_mode: Flag indicating to enable the game mode (if game mode locked, this must be True)
        :type game_mode: ``bool``
        :param  game_mode_lock: Flag indicating to enable the game mode lock
        :type game_mode_lock: ``bool``
        """
        self.assertIn(member=(game_mode, game_mode_lock), container=[(False, False), (True, False), (True, True)])
        self.post_requisite_reload_nvs = True
        ChannelUtils.empty_queues(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate random disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        keys = self.generate_random_disabled_keys(count=16)
        disabled_keys = keys["disabled_keys"]
        params = {}
        for key in disabled_keys:
            params[f'cidx_{key["cidx"]}'] = 1
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set game mode and game mode lock")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode(enabled=game_mode)
        self.enable_game_mode_lock(lock_enabled=game_mode_lock)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(test_case=self, **params)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Keystroke keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in disabled_keys:
            self.button_stimuli_emulator.keystroke(key_id=key["key_id"])
        # end for

        if not game_mode:
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check HID reports of keystrokes")
            # ----------------------------------------------------------------------------------------------------------
            for key in disabled_keys:
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(key_id=key["key_id"], state=MAKE))
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(key_id=key["key_id"], state=BREAK))
                KeyMatrixTestUtils.KeyExpectedActions.reset()
            # end for

            self.assertEqual(expected=0,
                             obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                             msg='Some HID reports were missing')
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check no HID report is received")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)
        # end if
    # end def _verify_key_strokes_for_game_mode_and_game_mode_lock

    @features("Feature4523")
    @level("Functionality")
    def test_check_to_set_disabled_keys_when_game_mode_off_and_game_mode_lock_off(self):
        """
        Check to add keys to the disabled key list when game mode is inactive and game mode lock disabled
        """
        self._verify_key_strokes_for_game_mode_and_game_mode_lock(game_mode=False, game_mode_lock=False)
        self.testCaseChecked('FUN_4523_0001#1', _AUTHOR)
    # end def test_check_to_set_disabled_keys_when_game_mode_off_and_game_mode_lock_off

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @level("Functionality")
    @services("GameModeButton")
    def test_check_to_set_disabled_keys_when_game_mode_on(self):
        """
        Check to add keys to the disabled key list when game mode is active
        """
        self._verify_key_strokes_for_game_mode_and_game_mode_lock(game_mode=True, game_mode_lock=False)
        self.testCaseChecked('FUN_4523_0001#2', _AUTHOR)
    # end def test_check_to_set_disabled_keys_when_game_mode_on


    """
    'FUN_4523_0001#3':
    test_check_to_set_disabled_keys_when_game_mode_lock_on
    (OBSOLETE No longer relevant as game mode can not be disabled when game mode is locked.)
    """


    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @features("Feature4523GameModeLockSupported")
    @level("Functionality")
    @services("GameModeButton")
    def test_check_to_set_disabled_keys_when_game_mode_on_and_game_mode_lock_on(self):
        """
        Check to add keys to the disabled key list when game mode is active and game mode lock is locked.
        """
        self._verify_key_strokes_for_game_mode_and_game_mode_lock(game_mode=True, game_mode_lock=True)
        self.testCaseChecked('FUN_4523_0001#4', _AUTHOR)
    # end def test_check_to_set_disabled_keys_when_game_mode_on_and_game_mode_lock_on

    @features("Feature4523")
    @features("Feature4523PowerOnGameModeSupported")
    @level("Functionality")
    def test_game_mode_state_following_poweron_game_mode_setting_at_next_poweron(self):
        """
        Check the game mode state following the poweron game mode setting at next power-on
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set power-on game mode ON')
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(test_case=self,
                                                                           poweron_game_mode_lock_valid=0,
                                                                           poweron_game_mode_valid=1,
                                                                           poweron_game_mode_lock=0,
                                                                           poweron_game_mode=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode")
        # --------------------------------------------------------------------------------------------------------------
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        self.assertEqual(expected=1,
                         obtained=get_game_mode_rsp.game_mode_full_state.enabled,
                         msg="Game mode shall be enabled at next power-on")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set power-on game mode OFF')
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(test_case=self,
                                                                           poweron_game_mode_lock_valid=0,
                                                                           poweron_game_mode_valid=1,
                                                                           poweron_game_mode_lock=0,
                                                                           poweron_game_mode=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode")
        # --------------------------------------------------------------------------------------------------------------
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        self.assertEqual(expected=0,
                         obtained=get_game_mode_rsp.game_mode_full_state.enabled,
                         msg="Game mode shall be disabled at next power-on")

        self.testCaseChecked('FUN_4523_0002', _AUTHOR)
    # end def test_game_mode_state_following_poweron_game_mode_setting_at_next_poweron

    @features("Feature4523")
    @features("Feature4523PowerOnGameModeSupported")
    @features('Feature1830powerMode', 3)
    @level("Functionality")
    def test_game_mode_state_following_poweron_game_mode_setting_while_wakeup_from_deep_sleep(self):
        """
        Check the game mode state following the poweron game mode setting while wake-up from deep sleep
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set power-on game mode ON')
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(test_case=self,
                                                                           poweron_game_mode_lock_valid=0,
                                                                           poweron_game_mode_valid=1,
                                                                           poweron_game_mode_lock=0,
                                                                           poweron_game_mode=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep-sleep mode by 0x1830.SetPowerMode")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wake up DUT via keystroke enter key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode")
        # --------------------------------------------------------------------------------------------------------------
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        self.assertEqual(expected=1,
                         obtained=get_game_mode_rsp.game_mode_full_state.enabled,
                         msg="Game mode shall be enabled at next power-on")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set power-on game mode OFF')
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(test_case=self,
                                                                           poweron_game_mode_lock_valid=0,
                                                                           poweron_game_mode_valid=1,
                                                                           poweron_game_mode_lock=0,
                                                                           poweron_game_mode=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep-sleep mode by 0x1830.SetPowerMode")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wake up DUT via keystroke enter key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode")
        # --------------------------------------------------------------------------------------------------------------
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        self.assertEqual(expected=0,
                         obtained=get_game_mode_rsp.game_mode_full_state.enabled,
                         msg="Game mode shall be disabled at next power-on")

        self.testCaseChecked('FUN_4523_0003', _AUTHOR)
    # end def test_game_mode_state_following_poweron_game_mode_setting_while_wakeup_from_deep_sleep

    @features("Feature4523")
    @features("Feature4523PowerOnGameModeLockSupported")
    @level("Functionality")
    def test_game_mode_lock_state_following_poweron_game_mode_lock_setting_at_next_poweron(self):
        """
        Check the game mode lock state following the poweron game mode lock setting at next power-on
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set power-on game mode lock ON')
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(test_case=self,
                                                                           poweron_game_mode_lock_valid=1,
                                                                           poweron_game_mode_valid=1,
                                                                           poweron_game_mode_lock=1,
                                                                           poweron_game_mode=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode")
        # --------------------------------------------------------------------------------------------------------------
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        self.assertEqual(expected=1,
                         obtained=get_game_mode_rsp.game_mode_full_state.locked,
                         msg="Game mode lock shall be enabled at next power-on")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set power-on game mode lock OFF')
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(test_case=self,
                                                                           poweron_game_mode_lock_valid=1,
                                                                           poweron_game_mode_valid=1,
                                                                           poweron_game_mode_lock=0,
                                                                           poweron_game_mode=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode")
        # --------------------------------------------------------------------------------------------------------------
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        self.assertEqual(expected=0,
                         obtained=get_game_mode_rsp.game_mode_full_state.locked,
                         msg="Game mode lock shall be disabled at next power-on")

        self.testCaseChecked('FUN_4523_0004', _AUTHOR)
    # end def test_game_mode_lock_state_following_poweron_game_mode_lock_setting_at_next_poweron

    @features("Feature4523")
    @features("Feature4523PowerOnGameModeLockSupported")
    @features('Feature1830powerMode', 3)
    @level("Functionality")
    def test_game_mode_lock_state_following_poweron_game_mode_lock_setting_while_wakeup_from_deep_sleep(self):
        """
        Check the game mode lock state following the poweron game mode lock setting while wake-up from deep sleep
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set power-on game mode lock ON')
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(test_case=self,
                                                                           poweron_game_mode_lock_valid=1,
                                                                           poweron_game_mode_valid=1,
                                                                           poweron_game_mode_lock=1,
                                                                           poweron_game_mode=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep-sleep mode by 0x1830.SetPowerMode")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wake up DUT via keystroke enter key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode")
        # --------------------------------------------------------------------------------------------------------------
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        self.assertEqual(expected=1,
                         obtained=get_game_mode_rsp.game_mode_full_state.locked,
                         msg="Game mode lock shall be enabled at next power-on")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set power-on game mode lock OFF')
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(test_case=self,
                                                                           poweron_game_mode_lock_valid=1,
                                                                           poweron_game_mode_valid=1,
                                                                           poweron_game_mode_lock=0,
                                                                           poweron_game_mode=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set DUT into deep-sleep mode by 0x1830.SetPowerMode")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wake up DUT via keystroke enter key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode")
        # --------------------------------------------------------------------------------------------------------------
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        self.assertEqual(expected=0,
                         obtained=get_game_mode_rsp.game_mode_full_state.locked,
                         msg="Game mode lock shall be disabled at next power-on")

        self.testCaseChecked('FUN_4523_0005', _AUTHOR)
    # end def test_game_mode_lock_state_following_poweron_game_mode_lock_setting_while_wakeup_from_deep_sleep

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @level("Functionality")
    @services("GameModeButton")
    def test_check_notifications_for_game_mode_changed(self):
        """
        Check receiving the notifications whenever game mode is enabled or disabled.
        """
        self.post_requisite_reload_nvs = True

        self.enable_game_mode(enabled=False)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable game mode")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode event")
        # --------------------------------------------------------------------------------------------------------------
        game_mode_event = DisableControlsByCIDXTestUtils.HIDppHelper.game_mode_event(test_case=self,
                                                                                     check_first_message=False)
        self.assertEqual(expected=1,
                         obtained=game_mode_event.game_mode_state.enabled,
                         msg="Game mode shall be enabled!")

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable game mode")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode(enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode event")
        # --------------------------------------------------------------------------------------------------------------
        game_mode_event = DisableControlsByCIDXTestUtils.HIDppHelper.game_mode_event(test_case=self,
                                                                                     check_first_message=False)
        self.assertEqual(expected=0,
                         obtained=game_mode_event.game_mode_state.enabled,
                         msg="Game mode shall be disabled!")

        self.testCaseChecked('FUN_4523_0006#1', _AUTHOR)
    # end def test_check_notifications_for_game_mode_changed

    @features("Feature4523")
    @features("Feature4523GameModeLockSupported")
    @level("Functionality")
    def test_check_notifications_for_game_mode_lock_changed(self):
        """
        Check receiving the notifications whenever game mode lock is enabled or disabled.
        """
        self.post_requisite_reload_nvs = True

        self.enable_game_mode_lock(lock_enabled=False)

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable game mode lock")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode_lock()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode event")
        # --------------------------------------------------------------------------------------------------------------
        game_mode_event = DisableControlsByCIDXTestUtils.HIDppHelper.game_mode_event(test_case=self,
                                                                                     check_first_message=False)
        self.assertEqual(expected=1,
                         obtained=game_mode_event.game_mode_state.locked,
                         msg="Game mode lock shall be locked!")

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable game mode lock")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode_lock(lock_enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode event")
        # --------------------------------------------------------------------------------------------------------------
        game_mode_event = DisableControlsByCIDXTestUtils.HIDppHelper.game_mode_event(test_case=self,
                                                                                     check_first_message=False)
        self.assertEqual(expected=0,
                         obtained=game_mode_event.game_mode_state.locked,
                         msg="Game mode lock shall be unlocked!")

        self.testCaseChecked('FUN_4523_0006#2', _AUTHOR)
    # end def test_check_notifications_for_game_mode_lock_changed
# end class DisableControlsByCIDXFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------