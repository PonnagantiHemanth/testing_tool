#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.ghostkeys.ghostkeys
:brief: Hid Keyboard ghost keys test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/06/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hid import HID_REPORTS
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class GhostKeysTestCase(BaseTestCase):
    """
    Validate Keyboard GhostKeys requirement
    """

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

# end class GhostKeysTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
