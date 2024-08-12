#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.keycode.keycode
:brief: Hid Keyboard KeyCode test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyhid.hid import HID_REPORTS
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyCodeTestCase(BaseTestCase):
    """
    Validate Keyboard KeyCode translation
    """
    # Double press interval: 70ms
    # Double press sequence: Make - Interval - Break - Interval - Second make
    DICTATION_MAKE_BREAK_INTERVAL = 70
    DICTATION_MAKE_BREAK_INTERVAL_COUNT = 2
    # Business use cases leverages the first 5 supported keys of the exposed key matrix
    NUMBER_OF_KEYS = 5

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_clean_fn_lock_state = False
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # Empty hid_message_queue
        channel_to_use = self.current_channel.receiver_channel if (
            isinstance(self.current_channel, ThroughReceiverChannel)) else self.current_channel
        ChannelUtils.clean_messages(
            test_case=self, channel=channel_to_use, queue_name=HIDDispatcher.QueueName.HID, class_type=HID_REPORTS)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
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
                if self.post_requisite_clean_fn_lock_state:
                    # NB: the NVS_FN_INVERSION_HOST_ID chunk is removed by the restore_nvs call
                    self.button_stimuli_emulator.fn_locked = False
                    self.post_requisite_clean_fn_lock_state = False
                # end if
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def _test_key_code(self, group_count=None):
        """
        Common part of the 5 first and all available keys tests.

        :param group_count: number of groups to select or ``None`` to test all keys
        :type group_count: ``int`` or ``None``
        """
        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=group_count, group_size=1, random=False)
        for (key_id,) in keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for (key_id,) in keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report linked to the key id={str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_key_code

    def _test_fn_key(self):
        """
        Common part of the Fn-Key tests.
        """
        self.kosmos.sequencer.offline_mode = True
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key press on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=1)
        assert self.button_stimuli_emulator.fn_pressed, 'FN key has not been correctly pressed !'

        for key_id in iter(fn_keys.values()):
            if KEY_ID.FN_LOCK in fn_keys and key_id == fn_keys[KEY_ID.FN_LOCK]:
                # Skip Fn-lock key in this test
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key release on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_id in iter(fn_keys.keys()):
            if key_id == KEY_ID.FN_LOCK:
                # Fn-lock key has been skipped in this test
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for
    # end def _test_fn_key

    def _test_fn_lock_key(self):
        """
        Common part of the Fn_lock key tests.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable the FN_LOCK mode')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True

        fn_lock_change = KeyMatrixTestUtils.switch_fn_lock_state(self)
        if fn_lock_change and self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_HasFnLock:
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get fLockChange event")
            # ------------------------------------------------------------------------------------------------------
            FnInversionForMultiHostDevicesTestUtils.HIDppHelper.f_lock_change_event(self,
                                                                                    check_first_message=False)
        # end if
        self.post_requisite_clean_fn_lock_state = True

        self.kosmos.sequencer.offline_mode = True
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        for key_id in range(KEY_ID.KEYBOARD_F1, KEY_ID.KEYBOARD_F24):
            if key_id not in fn_keys:
                # Skip keys not supported by the DUT
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=fn_keys[KEY_ID(key_id)])
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_id in [x for x in KEY_ID if KEY_ID.KEYBOARD_F1 <= x <= KEY_ID.KEYBOARD_F24]:
            if key_id not in fn_keys:
                # Skip keys not supported by the DUT
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for
    # end def _test_fn_lock_key

# end class KeyCodeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
