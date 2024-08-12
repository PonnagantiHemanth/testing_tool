#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1805.business
:brief: HID++ 2.0 ``OobState`` business test suite
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2022/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.oobstateutils import OobStateTestUtils
from pytestbox.device.hidpp20.common.feature_1805.oobstate import OobStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sanjib Hazra"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobStateBusinessTestCase(OobStateTestCase):
    """
    Validate ``OobState`` business test cases
    """

    @features("Feature1805")
    @features("Wireless")
    @level('Business', 'SmokeTests')
    @services("Debugger")
    @services("HardwareReset")
    def test_connection_lost_on_next_power_reset(self):
        """
        Validate that after sending SetOobState, connection with the host generating the command is lost, at next power
        on
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetOobState request")
        # --------------------------------------------------------------------------------------------------------------
        response = OobStateTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetOobStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.MessageChecker.check_fields(
            test_case=self, message=response, expected_cls=self.feature_1805.set_oob_state_response_cls,
            check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.ResetHelper.hardware_reset(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetReceiverChannel request")
        # --------------------------------------------------------------------------------------------------------------
        channel_receiver = ChannelUtils.get_receiver_channel(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check a valid Device Connection notification is not received')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self,  channel=channel_receiver,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=3,
            class_type=DeviceConnection)
        device_info_class = \
            self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertTrue(to_int(device_info.device_info_link_status) ==
                        DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                        msg='Device Info Link Status shall be set to established')

        self.testCaseChecked("BUS_1805_0001", _AUTHOR)
    # end def test_connection_lost_on_next_power_reset
# end class OobStateBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
