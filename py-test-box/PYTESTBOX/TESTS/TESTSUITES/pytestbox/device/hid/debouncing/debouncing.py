#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.debouncing.debouncing
:brief: Hid Debouncing test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/29
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyhid.hid import HID_REPORTS
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DebouncingTestCase(BaseTestCase):
    """
    Validate Debouncing Algo v1 requirements
    """
    # Time range to monitor - 2ms
    TEST_DURATION = 2000
    # Time increment - 0.1ms
    STEP = 100

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        self.channel_to_use = self.current_channel.receiver_channel \
            if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Clean-up all HID reports in HID message queue')
        # ---------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self, channel=self.channel_to_use, queue_name=HIDDispatcher.QueueName.HID,
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

# end class DebouncingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
