#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4523.disablecontrolsbycidx
:brief: Validate HID++ 2.0 ``DisableControlsByCIDX`` feature
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import sample

from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDXTestCase(DeviceBaseTestCase):
    """
    Validate ``DisableControlsByCIDX`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x4523 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_4523_index, self.feature_4523, _, _ = DisableControlsByCIDXTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_CONTROLS_BY_CIDX
        self.enable_game_mode(enabled=False)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            # Reset the game mode emulator to its initial state before restoring NVS!
            if self.game_mode_emulator:
                self.game_mode_emulator.set_mode(activate_game_mode=False)
            # end if
        # end with

        with self.manage_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        super().tearDown()
    # end def tearDown

    def enable_game_mode(self, enabled=True):
        """
        Enable game mode

        :param enabled: Flag indicating to enable the game mode
        :type enabled: ``bool``
        """
        # query the current game mode
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        if enabled != get_game_mode_rsp.game_mode_full_state.enabled:
            self.game_mode_emulator.set_mode(activate_game_mode=enabled)
        # end if
    # end def enable_game_mode

    def enable_game_mode_lock(self, lock_enabled=True):
        """
        Enable game mode lock

        :param lock_enabled: Flag indicating to enable the game mode lock
        :type lock_enabled: ``bool``
        """
        # query the current game mode
        get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
        if lock_enabled != get_game_mode_rsp.game_mode_full_state.locked:
            self.button_stimuli_emulator.simultaneous_keystroke([KEY_ID.FN_KEY, KEY_ID.GAME_MODE_KEY], duration=.5)
        # end if
    # end def enable_game_mode_lock

    def generate_random_disabled_keys(self, count):
        """
        Generate the random disabled keys from standard keys

        :param count: the number of the keys to generate
        :type count: ``int``

        :return: disabled key list and non-disabled key list
        :rtype: ``dict{disabled_keys: list[{"key_id":,"cidx":}], non_disabled_keys: list[{"key_id":,"cidx":}]}``
        """
        disabled_keys = []
        non_disabled_keys = []

        candidates = FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_remappable_keys(test_case=self)

        disabled_keys_list = sample(population=candidates, k=count)
        for keyId in candidates:
            cidx = ControlListTestUtils.key_id_to_cidx(self, keyId)
            if keyId in disabled_keys_list:
                disabled_keys.append({"key_id": keyId, "cidx": cidx})
            else:
                non_disabled_keys.append({"key_id": keyId, "cidx": cidx})
            # end if
        # end for

        return {"disabled_keys": disabled_keys, "non_disabled_keys": non_disabled_keys}
    # end def generate_random_disabled_keys
# end class DisableControlsByCIDXTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
