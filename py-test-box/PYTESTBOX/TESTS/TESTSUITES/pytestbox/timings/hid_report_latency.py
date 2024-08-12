#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.timings.hid_report_latency
:brief: Validate 'HID report latency removal' feature
:author: Christophe Roquebert
:date: 2020/10/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HidLatencyTestCase(DeviceBaseTestCase):
    """
    HID Report latency TestCases
    """
    MAX_HID_REPORT_TIMING = 72000  # 72ms

    @features('BLELatencyRemoval')
    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_hid_report_latency_removal(self):
        """
        Central and Peripheral shall both support the latency removal feature

        Check the timing between the Device Connection notification and the first HID report
        """
        key_id = list(self.button_stimuli_emulator.get_key_id_list())[0]

        for i in range(5):
            # Empty hid_message_queue from HidMouse and HidKeyboard notifications sent by the receiver
            ChannelUtils.clean_messages(
                test_case=self, channel=self.current_channel.receiver_channel, queue_name=HIDDispatcher.QueueName.HID,
                class_type=HID_REPORTS)
            # Empty receiver_connection_event_queue from DeviceConnection notifications sent by the receiver
            ChannelUtils.clean_messages(
                test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=DeviceConnection)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Power off / on the device')
            # ---------------------------------------------------------------------------
            self.memory_manager.debugger.reset(soft_reset=False)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait for the device reconnection')
            # ---------------------------------------------------------------------------
            device_connection = ChannelUtils.get_only(
                test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), timeout=3,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection)
            while device_connection is not None:
                device_info_class = DeviceBaseTestCase.get_device_info_bit_field_structure_in_device_connection(
                    device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                if int(Numeral(device_info.device_info_link_status)) == DeviceConnection.LinkStatus.LINK_ESTABLISHED:
                    break
                # end if
                device_connection = ChannelUtils.get_only(
                    test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection,
                    timeout=3, allow_no_message=True)
            # end while

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press the first key supported by the button emulator')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=key_id)
            hid_msg = ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.HID, class_type=HID_REPORTS)
            delta = (hid_msg.timestamp - device_connection.timestamp) // 10 ** 3
            self.button_stimuli_emulator.key_release(key_id=key_id)
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID, class_type=HID_REPORTS)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Device Connection and HID report have been received')
            # --------------------------------------------------------------------------
            self.assertNotNone(obtained=device_connection,
                               msg='Device Connection notification should have been received')
            self.assertNotNone(obtained=hid_msg, msg='HID mouse message should have been received')

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the timing between Connection notification and first HID report: '
                                      f'{delta} < {HidLatencyTestCase.MAX_HID_REPORT_TIMING}us')
            # --------------------------------------------------------------------------
            self.assertNotNone(obtained=delta, msg='A timing should have been processed')
            self.assertTrue(delta < HidLatencyTestCase.MAX_HID_REPORT_TIMING,
                            msg=f'HID report received too late: timing from connection is {delta}us')

            ChannelUtils.clean_messages(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent)
        # end for

        self.testCaseChecked("FNT_TIME_0020")
    # end def test_hid_report_latency_removal

# end class HidLatencyTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
