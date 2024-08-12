#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.keycode.timing
:brief: Hid Keyboard keycode timing test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LogitechReportType
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.keycode.keycode import KeyCodeTestCase
from pytransport.transportmessage import TransportMessage


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyCodeTimingTestCase(KeyCodeTestCase):
    """
    Validate Keyboard KeyCode Timing TestCases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        self.hid_report_timestamps = []

        # Start polling EP Keyboard Interface only
        self.polling_configuration(keyboard_only=True)

        # Empty hid_message_queue
        channel_to_use = self.current_channel.receiver_channel if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel
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
            # Start polling all EPs
            self.polling_configuration()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Verify no HID report was missing')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                             msg='Some HID reports were missing')
        # end with

        super().tearDown()
    # end def tearDown

    def polling_callback(self, transport_message):
        """
        Callback function called when an HID report is received on the EndPoint.

        :param transport_message: received data
        :type transport_message: ``TransportMessage``
        """
        # save the message timestamp
        self.hid_report_timestamps.append(transport_message.timestamp)
    # end def polling_callback

    def polling_configuration(self, keyboard_only=False):
        """
        Configure the task executor to poll the requested EPs

        :param keyboard_only: Flag to enable all EPs if True, otherwise the Keyboard EndPoint only.
        :type keyboard_only: ``bool``
        """
        if keyboard_only:
            # Update callback on Keyboard & Mouse Interfaces
            self.current_channel.update_callback(
                targeted_report_types=[LogitechReportType.KEYBOARD, LogitechReportType.MOUSE],
                callback=self.polling_callback)
        else:
            # Remove callback on Keyboard & Mouse Interfaces
            self.current_channel.update_callback(
                targeted_report_types=[LogitechReportType.KEYBOARD, LogitechReportType.MOUSE], callback=None)
        # end if
    # end def polling_configuration

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.DICTATION,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_mac_os_dictation(self):
        """
        User presses the dictation key, then waits until the dictation is activated.
         - Check the translation of the dictation key is correct when an Mac OS has been detected.
         - Check the interval between the make and the break HID reports.
        """
        hid_report_expected_count = 4

        # Force the switch in macOS mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(KEY_ID.DICTATION)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.DICTATION, repeat=1)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        for _ in range(hid_report_expected_count):
            # Retrieve Dictation HID report
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        # end for

        for index in range(KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL_COUNT):
            # Retrieve Dictation HID report
            delta = (self.hid_report_timestamps[index+1] - self.hid_report_timestamps[index]) // 1.e6
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the lower marker')
            # ----------------------------------------------------------------------------------------------------------
            self.assertGreater(delta, KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL * 0.9,
                               f'The delta n{index} is lower than 90% of the specified value')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate the upper marker')
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(delta, KeyCodeTestCase.DICTATION_MAKE_BREAK_INTERVAL * 1.1,
                            f'The delta n{index} is greater than 110% of the specified value')
        # end for

        self.testCaseChecked("TIM_MEMB_0001")
    # end def test_mac_os_dictation
# end class KeyCodeTimingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
