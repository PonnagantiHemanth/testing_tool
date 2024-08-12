#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.button.button
:brief: Hid mouse button test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/01/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils
from pytestbox.device.hid.mouse import EXCLUDED_BUTTONS

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
Event = HidReportTestUtils.Event
EventId = HidReportTestUtils.EventId
KEY_ID_EVENT_MAP = HidReportTestUtils.KEY_ID_EVENT_MAP


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ButtonTestCase(BaseTestCase):
    """
    Validate mouse button requirements
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.pressed_key_ids = None
        super().setUp()

        self.post_requisite_reload_nvs = True
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            if self.pressed_key_ids is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Release all pressed buttons")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.multiple_keys_release(key_ids=self.pressed_key_ids)
                self.pressed_key_ids = None
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def press_single_button(self, key_id):
        """
        Execute the following test sequence:
         - Press on the given button
         - Check a single HID Mouse report with only one bit set sent by the DUT
         - Release the given button
         - Check a single HID Mouse report with the bit reset sent by the DUT

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID``
        """
        self.pressed_key_ids = [key_id]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press on the {str(key_id)} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check a single HID Mouse report with one bit set sent by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(KEY_ID_EVENT_MAP[key_id], value=1)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release the {str(key_id)} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id)
        self.pressed_key_ids = None

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check a single HID Mouse report with the bit reset sent by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(KEY_ID_EVENT_MAP[key_id])])
    # end def press_single_button

    def press_multiple_buttons(self, key_id):
        """
        Execute the following test sequence:
         - Press on the given button and all the other supported buttons
         - Check multiple HID Mouse reports with all supported bits set incrementally
         - Release the given button and all the other supported buttons
         - Check multiple HID Mouse reports with all bits reset decrementally

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID``
        """
        self.pressed_key_ids = [key_id]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press on the {str(key_id)} first then all the other supported buttons")
        # --------------------------------------------------------------------------------------------------------------
        self.pressed_key_ids.extend([x for x in self.button_stimuli_emulator.get_key_id_list() if x not in
                                     EXCLUDED_BUTTONS and x != key_id and x < KEY_ID.BUTTON_1])
        self.button_stimuli_emulator.multiple_keys_press(key_ids=self.pressed_key_ids,
                                                         delay=ButtonStimuliInterface.DEFAULT_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check multiple HID Mouse reports with all supported bits set incrementally")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(len(self.pressed_key_ids)):
            HidReportTestUtils.check_hid_report_by_event(
                test_case=self, events=[Event(KEY_ID_EVENT_MAP[self.pressed_key_ids[index]], value=1)])
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release the {str(key_id)} button first then all the other supported buttons")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=self.pressed_key_ids,
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check multiple HID Mouse reports with all bits reset decrementally")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(len(self.pressed_key_ids)):
            HidReportTestUtils.check_hid_report_by_event(
                test_case=self, events=[Event(KEY_ID_EVENT_MAP[self.pressed_key_ids[index]])])
        # end for
        self.pressed_key_ids = None
    # end def press_multiple_buttons

# end class ButtonTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
