#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.base.receiverbasetestutils
:brief:  Helpers for receiver specific feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/11/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverBaseTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for receiver specific features
    """
    class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
        """
        HID++ 1.0 helper class
        """
        @classmethod
        def send_report_wait_error(cls, test_case, report, error_type=Hidpp1ErrorCodes, error_codes=None):
            # See CommonBaseTestUtils.HIDppHelper.send_report_wait_error
            return super().send_report_wait_error(test_case, report, error_type, error_codes)
        # end def send_report_wait_error
    # end class HIDppHelper

    class ResetHelper:
        """
        Reset Helper class
        """
        @staticmethod
        def hardware_reset(test_case):
            """
            Perform a hardware reset
            This will NOT handle anything else (channel, connection events, ...) than the reset.

            NB: You shall close the receiver channel before calling this method !

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            if test_case.receiver_debugger is not None:
                test_case.receiver_debugger.reset(soft_reset=False)
            elif len(LibusbDriver.discover_usb_hub()) > 0:
                # Priority is let to the debugger because, currently, resetting using the hub is not stable enough.
                # It seems that the port is turned off without any notification, so the driver is lost because it
                # expects a device which is not here. If it can be fixed, this method should have higher priority
                # than debugger because it would be closer to real user action.
                with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=test_case.receiver_debugger):
                    try:
                        LibusbDriver.disable_usb_port(port_index=ChannelUtils.get_port_index(
                            test_case=test_case, channel=ChannelUtils.get_receiver_channel(test_case=test_case)))
                    finally:
                        LibusbDriver.enable_usb_port(port_index=ChannelUtils.get_port_index(
                            test_case=test_case, channel=ChannelUtils.get_receiver_channel(test_case=test_case)))
                    # end try
                # end with
            else:
                raise RuntimeError('No reset method available')
            # end if
        # end def hardware_reset
    # end class ResetHelper
# end class ReceiverBaseTestUtils

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
