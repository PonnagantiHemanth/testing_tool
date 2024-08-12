#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4523.business
:brief: HID++ 2.0 ``DisableControlsByCIDX`` business test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/06/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDX
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4523.disablecontrolsbycidx import DisableControlsByCIDXTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDXBusinessTestCase(DisableControlsByCIDXTestCase):
    """
    Validate ``DisableControlsByCIDX`` business test cases
    """

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @features("Feature4523GameModeLockSupported")
    @level("Business")
    @services("GameModeButton")
    def test_verify_gamemode_not_changed_when_gamemode_enabled_and_gamemodelock_enabled(self):
        """
        Verify game mode is not changed when game mode locked is enabled and game mode is enabled.
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable game mode lock")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode_lock(lock_enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable game mode")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable game mode lock")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode_lock()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable game mode")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode(enabled=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetGameMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetGameModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=DisableControlsByCIDX.GameModeLock.ENABLE,
                         obtained=response.game_mode_full_state.locked,
                         msg="Game mode lock shall be enabled!")
        self.assertEqual(expected=DisableControlsByCIDX.GameMode.ENABLE,
                         obtained=response.game_mode_full_state.enabled,
                         msg="Game mode shall not be changed when game mode lock is enabled!")
        self.testCaseChecked('BUS_4523_0001', _AUTHOR)
    # end def test_verify_gamemode_not_changed_when_gamemode_enabled_and_gamemodelock_enabled


    """
    'BUS_4523_0002':
    test_verify_gamemode_not_changed_when_gamemode_disabled_and_gamemodelock_enabled
    (OBSOLETE due to game mode is enabled when game mode lock is enabled)
    """


    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @level('Business', 'SmokeTests')
    @services("GameModeButton")
    def test_verify_gamemode_disabled_keys_are_disabled_when_gamemode_is_activated(self):
        """
        Verify game mode disabled keys are disabled when game mode is activated.
        """
        self.post_requisite_reload_nvs = True

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
        LogHelper.log_step(self, "Send SetDisabledControl request")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(test_case=self, **params)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Set Game Mode request to enable game mode")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode()

        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Keystroke disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = True
        for key in disabled_keys:
            self.button_stimuli_emulator.keystroke(key_id=key["key_id"])
        # end for

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no HID reports of keystrokes")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)

        self.testCaseChecked('BUS_4523_0003', _AUTHOR)
    # end def test_verify_gamemode_disabled_keys_are_disabled_when_gamemode_is_activated

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @level("Business")
    @services("GameModeButton")
    def test_verify_gamemode_disabled_keys_are_enabled_when_gamemode_is_deactivated(self):
        """
        Verify game mode disabled keys are enabled when game mode is deactivated.
        """
        self.post_requisite_reload_nvs = True

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
        LogHelper.log_step(self, "Send SetDisabledControl request")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(test_case=self, **params)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Set Game Mode request to disable game mode")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode(enabled=False)

        self.kosmos.sequencer.offline_mode = True
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Keystroke disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in disabled_keys:
            self.button_stimuli_emulator.keystroke(key_id=key["key_id"])
        # end for

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID reports of keystrokes")
        # --------------------------------------------------------------------------------------------------------------
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

        self.testCaseChecked('BUS_4523_0004', _AUTHOR)
    # end def test_verify_gamemode_disabled_keys_are_enabled_when_gamemode_is_deactivated

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @level("Business")
    @services("GameModeButton")
    def test_verify_non_disabled_keys_are_not_disabled_when_gamemode_is_activated(self):
        """
        Verify non-disabled keys are not disabled when game mode is activated.
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate random disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        keys = self.generate_random_disabled_keys(count=16)
        disabled_keys = keys["disabled_keys"]
        non_disabled_keys = keys["non_disabled_keys"]
        params = {}
        for key in disabled_keys:
            params[f'cidx_{key["cidx"]}'] = 1
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDisabledControl request")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(test_case=self, **params)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Set Game Mode request to enable game mode")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode()

        self.kosmos.sequencer.offline_mode = True
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Keystroke non-disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in non_disabled_keys:
            self.button_stimuli_emulator.keystroke(key_id=key["key_id"])
        # end for

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID reports of keystrokes")
        # --------------------------------------------------------------------------------------------------------------
        for key in non_disabled_keys:
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id=key["key_id"], state=MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id=key["key_id"], state=BREAK))
            KeyMatrixTestUtils.KeyExpectedActions.reset()
        # end for

        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked('BUS_4523_0005', _AUTHOR)
    # end def test_verify_non_disabled_keys_are_not_disabled_when_gamemode_is_activated

    @features("Feature4523")
    @features("Feature8101")
    @level("Business")
    @services("GameModeButton")
    def test_verify_default_game_mode_disable_keys(self):
        """
        Verify the game mode disabled keys in OOB state as below:
        “Windows” key, “Context menu” key, “LS/BLE button”, “Brightness button”
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the first OOB profile")
        # --------------------------------------------------------------------------------------------------------------
        oob_profile = ProfileManagementTestUtils.ProfileHelper.get_oob_profile(test_case=self, oob_profile_index=0)
        oob_disabled_keys = oob_profile.tag_fields[ProfileManagement.Tag.X4523_CIDX_BITMAP].Data

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the CID list")
        # --------------------------------------------------------------------------------------------------------------
        cid_list = ControlListTestUtils.get_cid_list_from_device(test_case=self)

        targets = [
            CidTable.CONTEXTUAL_MENU,
            CidTable.BLUETOOTH,
            CidTable.LS2_BTN,
            CidTable.LEFT_GUI,
            CidTable.RIGHT_GUI,
            CidTable.BRIGHTNESS_UP,
            CidTable.BRIGHTNESS_DOWN,
            CidTable.KEY_BRIGHTNESS_CYCLE,
        ]

        self.assertTrue(
            expr=any(x in targets for x in cid_list), msg=f"{cid_list} as no intersection with {targets}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify default disabled keys are set correctly in the OOB profile")
        # --------------------------------------------------------------------------------------------------------------
        for candidate in targets:
            if candidate in cid_list:
                cid_index = cid_list.index(candidate)
                nth_byte = cid_index // 8
                nth_bit  = cid_index % 8
                value = (oob_disabled_keys[nth_byte] & (1 << nth_bit) != 0)
                self.assertEqual(expected=1,
                                 obtained=value,
                                 msg=f"cidx_{cid_index} shall be 1 for {candidate}!")
            # end if
        # end for

        self.testCaseChecked('BUS_4523_0006', _AUTHOR)
    # end def test_verify_default_game_mode_disable_keys

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @level("Business")
    @services("GameModeButton")
    def test_verify_keystrokes_that_re_enable_disabled_keys_in_game_mode(self):
        """
        Verify to remove a disabled keys from the list while the game mode is enabled then verifying that the keystroke
        on this key generate an HID report.
        """
        self.post_requisite_reload_nvs = True

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
        LogHelper.log_step(self, "Send SetDisabledControl request")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(test_case=self, **params)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Set Game Mode request to enable game mode")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDisabledControl request to re-enable disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(test_case=self)

        self.kosmos.sequencer.offline_mode = True
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Keystroke re-enabled keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in disabled_keys:
            self.button_stimuli_emulator.keystroke(key_id=key["key_id"])
        # end for

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID reports of keystrokes")
        # --------------------------------------------------------------------------------------------------------------
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

        self.testCaseChecked('BUS_4523_0007', _AUTHOR)
    # end def test_verify_keystrokes_that_re_enable_disabled_keys_in_game_mode

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @features("Feature4523GameModeLockSupported")
    @level("Business")
    @services("GameModeButton")
    def test_game_mode_after_locking_while_disabled(self):
        """
        Verify the behavior of the game mode after locking it while the game mode is disabled.
        The game mode is enabled automatically when the game mode lock is enabled.
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press FN + game mode button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.simultaneous_keystroke([KEY_ID.FN_KEY, KEY_ID.GAME_MODE_KEY], duration=.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetGameMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode is enabled and locked")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=DisableControlsByCIDX.GameModeLock.ENABLE,
                         obtained=response.game_mode_full_state.locked,
                         msg="Game mode lock shall be locked!")
        self.assertEqual(expected=DisableControlsByCIDX.GameMode.ENABLE,
                         obtained=response.game_mode_full_state.enabled,
                         msg="Game mode shall be enabled!")

        self.testCaseChecked('BUS_4523_0008', _AUTHOR)
    # end def test_game_mode_after_locking_while_disabled

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @features("Feature4523GameModeLockSupported")
    @level("Business")
    @services("GameModeButton")
    def test_game_mode_after_locking_while_enabled(self):
        """
        Verify the behavior of the game mode after locking it while the game mode is enabled.
        The game mode is enabled automatically when the game mode lock is enabled.
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Game mode is enabled")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode(enabled=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press FN + game mode button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.simultaneous_keystroke([KEY_ID.FN_KEY, KEY_ID.GAME_MODE_KEY], duration=.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetGameMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode is enabled and locked")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=DisableControlsByCIDX.GameModeLock.ENABLE,
                         obtained=response.game_mode_full_state.locked,
                         msg="Game mode lock shall be locked!")
        self.assertEqual(expected=DisableControlsByCIDX.GameMode.ENABLE,
                         obtained=response.game_mode_full_state.enabled,
                         msg="Game mode shall be enabled!")

        self.testCaseChecked('BUS_4523_0009', _AUTHOR)
    # end def test_game_mode_after_locking_while_enabled

    @features("Feature4523")
    @features("Feature4523GameModeSupported")
    @features("Feature4523GameModeLockSupported")
    @level("Business")
    @services("GameModeButton")
    def test_game_mode_after_unlocking(self):
        """
        Verify the behavior of the game mode after unlocking it.
        The game mode is disabled automatically when the game mode lock is disabled.
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Game mode is enabled and locked")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_game_mode_lock(lock_enabled=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press FN + game mode button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.simultaneous_keystroke([KEY_ID.FN_KEY, KEY_ID.GAME_MODE_KEY], duration=.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetGameMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check game mode is disabled and unlocked")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=DisableControlsByCIDX.GameModeLock.DISABLE,
                         obtained=response.game_mode_full_state.locked,
                         msg="Game mode lock shall be unlocked!")
        self.assertEqual(expected=DisableControlsByCIDX.GameMode.DISABLE,
                         obtained=response.game_mode_full_state.enabled,
                         msg="Game mode shall be disabled!")

        self.testCaseChecked('BUS_4523_0010', _AUTHOR)
    # end def test_game_mode_after_unlocking

# end class DisableControlsByCIDXBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------