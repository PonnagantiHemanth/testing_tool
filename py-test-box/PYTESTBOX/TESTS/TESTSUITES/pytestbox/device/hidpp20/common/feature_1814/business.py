#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1814.business
:brief: HID++ 2.0 ``ChangeHost`` business test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inverted_bit_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.changehostutils import get_cookie_list
from pytestbox.device.hidpp20.common.feature_1814.changehost import ChangeHostMultiReceiverTestCase
from pytestbox.device.hidpp20.common.feature_1814.changehost import ChangeHostTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
from pyusb.libusbdriver import ChannelIdentifier

_AUTHOR = "Kevin Dayet"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ChangeHostBusinessTestCase(ChangeHostTestCase):
    """
    Validate ``ChangeHost`` business test cases
    """

    @features('Feature1814')
    @level('Business', 'SmokeTests')
    def test_set_cookie_with_all_index(self):
        """
        Validate SetCookie Business case sequence (Feature 0x1814)

        Change Host
         cookie[0], cookie[1], ..., cookie[nbHost-1] [2]GetCookies
         [3] SetCookie(hostIndex, cookie)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over some interesting hostIndex value in its valid range")
        # --------------------------------------------------------------------------------------------------------------
        value_list = compute_inverted_bit_range(HexList(0))
        value_list.append(0)
        value_list.append(0xFF)
        value_list = sorted(value_list)
        for index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test loop over some interesting cookie value in its valid range")
            # ----------------------------------------------------------------------------------------------------------
            for value in value_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetCookie with  hostIndex={index} and cookie={value}")
                # ------------------------------------------------------------------------------------------------------
                ChangeHostTestUtils.HIDppHelper.set_cookie(
                    self, host_index=index, cookie=value, device_index=ChannelUtils.get_device_index(test_case=self))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send ChangeHost.GetCookies")
                # ------------------------------------------------------------------------------------------------------
                response = ChangeHostTestUtils.HIDppHelper.get_cookies(
                    self, device_index=ChannelUtils.get_device_index(test_case=self))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Validate GetCookies.cookie[hostIndex] value")
                # ------------------------------------------------------------------------------------------------------
                cookies_list = get_cookie_list(response, self.f.PRODUCT.DEVICE.F_NbHosts)
                self.assertEqual(expected=value,
                                 obtained=int(cookies_list[index], 16),
                                 msg='The cookies[' + str(index) + '] parameter differs from the one expected')
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop with cookie")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop with hostIndex")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1814_0001")
    # end def test_set_cookie_with_all_index
# end class ChangeHostBusinessTestCase


class ChangeHostMultiReceiverBusinessTestCase(ChangeHostMultiReceiverTestCase):
    """
    Validate ``ChangeHost`` with Multi Receivers business test cases
    """
    @features('Feature1814')
    @level('Business')
    @services('MultiHost')
    def test_set_current_host_with_all_index(self):
        """
        Validate SetCurrentHost Business case sequence (Feature 0x1814)
        Change Host
         nbHost, currHost, flags [0]GetHostInfov1
         [1]SetCurrentHost
        """
        # Get all channels that fit the expected Transport ID
        channels_to_test = DeviceManagerUtils.get_channels(test_case=self, channel_id=ChannelIdentifier(
            transport_id=self.f.PRODUCT.F_TransportID[0]))

        self.assertTrue(expr=int(self.f.PRODUCT.DEVICE.F_NbHosts) == len(channels_to_test),
                        msg="Not the right amount of channels to test")

        channels_to_test_map = {}
        for channel in channels_to_test:
            if isinstance(channel, ThroughReceiverChannel):
                channels_to_test_map[channel.get_channel_usb_port_path_list()[-1]] = channel
            else:
                # It was done this was because the indexer of pycharm does not recognise self.assertIsInstance
                # and was highlighting non-existent errors for the rest of the test
                self.assertIsInstance(
                    obj=channel, cls=ThroughReceiverChannel, msg="This test is only for channels through receiver")
            # end if
        # end for

        self.assertEqual(
            expected=channels_to_test_map[self.host_number_to_port_index(host_index=0)],
            obtained=self.current_channel,
            msg="The current channel should be the first one of the channels to use in this test")

        current_index = 0
        for index_list in [range(1, self.f.PRODUCT.DEVICE.F_NbHosts),
                           range(self.f.PRODUCT.DEVICE.F_NbHosts - 1, 0, -1)]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send ChangeHost.SetCurrentHost with hostIndex {list(index_list)}")
            # ----------------------------------------------------------------------------------------------------------
            for index in index_list:
                ChannelUtils.clean_messages(
                    test_case=self,
                    channel=self.current_channel.receiver_channel,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                    class_type=DeviceConnection)

                LogHelper.log_info(self, f"SetCurrentHost with hostIndex = {index}\n")
                response = ChangeHostTestUtils.HIDppHelper.set_current_host(
                    self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=index)
                if response is not None:
                    LogHelper.log_info(self, f"SetCurrentHost Response: {str(response)}\n")
                # end if

                # It seems that equad devices do not send a connection event when sending SetCurrentHost with the
                # same host as the one currently used. In BLE Pro, it does.
                # TODO verify for LS2
                if not isinstance(self.current_channel, ThroughEQuadReceiverChannel) or current_index != index:
                    DeviceManagerUtils.switch_channel(
                        test_case=self,
                        new_channel=channels_to_test_map[self.host_number_to_port_index(host_index=index)],
                        close_associated_channel=True,
                        open_associated_channel=True)
                # end if

                current_index = index

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send ChangeHost.GetHostInfov1")
                # ------------------------------------------------------------------------------------------------------
                get_host_info_v1_response = ChangeHostTestUtils.HIDppHelper.get_host_info(
                    self, device_index=ChannelUtils.get_device_index(test_case=self))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Validate GetHostInfov1.curr_host value")
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=index,
                                 obtained=to_int(get_host_info_v1_response.curr_host),
                                 msg='The currHost parameter differs from the one expected')
            # end for

            # Empty queue
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Send SetCurrentHost with hostIndex=0")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=0)

        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel=channels_to_test_map[self.host_number_to_port_index(host_index=0)],
            close_associated_channel=True,
            open_associated_channel=True)

        self.testCaseChecked("BUS_1814_0002")
    # end def test_set_current_host_with_all_index
# end class ChangeHostMultiReceiverBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
