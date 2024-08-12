#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4220.interface
:brief: HID++ 2.0 ``LockKeyState`` interface test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2022/04/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.lockkeystateutils import LockKeyStateTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4220.lockkeystate import LockKeyStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LockKeyStateInterfaceTestCase(LockKeyStateTestCase):
    """
    Validate ``LockKeyState`` interface test cases
    """

    @features("Feature4220")
    @level("Interface")
    def test_get_lock_key_state(self):
        """
        Validate ``GetLockKeyState`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetLockKeyState request")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_4220.get_lock_key_state_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_4220_index)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
            response_class_type=self.feature_4220.get_lock_key_state_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetLockKeyStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LockKeyStateTestUtils.GetLockKeyStateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, request.deviceIndex),
            "featureIndex": (checker.check_feature_index, request.featureIndex),
        })
        checker.check_fields(self, response, self.feature_4220.get_lock_key_state_response_cls, check_map)

        self.testCaseChecked("INT_4220_0001", _AUTHOR)
    # end def test_get_lock_key_state
# end class LockKeyStateInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
