#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.mouse.move
:brief: Validates HID response on xy move
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/01/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pytestbox.base.basetest import BaseTestCase
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level
from pyhid.hid.hidmouse import HidMouse
from pyhid.hid.hidkeyboard import HidKeyboard
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.numeral import Numeral

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
from pytestbox.base.channelutils import ChannelUtils


class XYMoveTestCase(BaseTestCase):
    """
    Validates XY displacement notifications TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(XYMoveTestCase, self).setUp()

        # Restart the executor by firstly stopping the initial task
        ChannelUtils.close_channel(test_case=self)
        # and secondly allocating a task per available interfaces
        ChannelUtils.open_channel(
            test_case=self, link_enabler=BitStruct(Numeral(LinkEnablerInfo.KEYBOARD_MASK + LinkEnablerInfo.MOUSE_MASK)))
    # end def setUp
    
    @features('Mice')
    @level('Interface')
    @services('OpticalSensor')
    def test_x(self):
        """
        @tc_synopsis Validates XY move HID notification

        """
        # TODO rework test method
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: ')
        # ---------------------------------------------------------------------------
        sleep(3)

        while not self.is_current_hid_dispatcher_queue_empty(queue=self.hidDispatcher.hid_message_queue):
            response = self.getMessage(queue=self.hidDispatcher.hid_message_queue, class_type=HidMouse)
            self.logTrace('HID Mouse Response: %s\n' % str(response))
            for field in response.FIELDS:
                fid = field.getFid()
                if response.get_absolute_value(fid) != 0:
                    self.logTrace('%s value = %d' % (field.name, response.get_absolute_value(fid)))
        # end while

        while not self.is_current_hid_dispatcher_queue_empty(queue=self.hidDispatcher.keyboard_message_queue):
            response = self.getMessage(queue=self.hidDispatcher.keyboard_message_queue,
                                       class_type=HidKeyboard)
            self.logTrace('HID Keyboard Response: %s\n' % str(response))
        # end while

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: ')
        # ---------------------------------------------------------------------------
        if self.device.time_stamped_msg_queue is not None:
            previous_timestamp = None
            while not self.device.time_stamped_msg_queue.empty():
                usbmessage = self.device.time_stamped_msg_queue.get()
                if (usbmessage is not None and
                   usbmessage.message_class is not None and
                   usbmessage.message_class == HidMouse):
                    if previous_timestamp is None:
                        previous_timestamp = usbmessage.timestamp
                    else:
                        timestamp = usbmessage.timestamp
                        delta = ((timestamp // 10 ** 6) - (previous_timestamp // 10 ** 6))
                        previous_timestamp = timestamp
                        self.logTrace('Timestamp delta = %.1f (ms)' % delta)
                    # end if
                # end if
            # end while
        # end if
        self.testCaseChecked("FNT_MICE_0001")
    # end def test_x
# end class XYMoveTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
