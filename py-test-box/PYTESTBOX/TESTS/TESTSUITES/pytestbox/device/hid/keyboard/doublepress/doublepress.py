#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.doublepress.doublepress
:brief: Hid Keyboard double press test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/05/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hid import HID_REPORTS
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DoublePressTestCase(BaseTestCase):
    """
    Validate Keyboard Double Press translation
    """
    # time constants for 30ms, 50ms and 100ms
    THIRTY_MILLI = 30
    FIFTY_MILLI = 50
    HUNDRED_MILLI = 100
    # Double press maximum period of time: 500ms
    DOUBLE_CLICK_TIME = 500
    # Delay between 2 simultaneous make and break events (main loop frequency)
    MAKE_BREAK_DELAY = 4

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # Empty hid_message_queue
        ChannelUtils.clean_messages(
            test_case=self, channel=self.current_channel.receiver_channel, queue_name=HIDDispatcher.QueueName.HID,
            class_type=HID_REPORTS)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
        # end with

        super().tearDown()
    # end def tearDown

# end class DoublePressTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
