#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pychannel.test.throughreceiverchannel_test
:brief: ``ThroughReceiverChannel`` unit tests
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/08/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import sys
from queue import Empty
from queue import Queue
from unittest import TestCase

from pychannel.channelinterfaceclasses import ChannelException
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.test.usbchannel_test import INTERRUPT_DATA_SIZE
from pychannel.test.usbchannel_test import MockUsbContext
from pychannel.test.usbchannel_test import MockHardwareDevice
from pychannel.throughreceiverchannel import ThroughBleProReceiverChannel
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import LogitechReportType
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import GetEnableHidppReportingResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformationModel
from pyhid.hidpp.hidpp1.setgetregister import GetLongRegister
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_wrong_range
from pytransport.transportmessage import TransportMessage
from pytransport.usb.usbconstants import EndpointDirection
from pytransport.usb.usbcontext import UsbContextDevice

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()
DEVICE_INDEX_FOR_TEST = 1
MAX_NUMBER_OF_PAIRED_DEVICES_FOR_TEST = 6


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
def get_common_testcase_class():
    """
    This method was created so the common class would not be run for tests while still having the common test
    script methods.

    :return: The common test case class
    :rtype: ``type``
    """
    class CommonThroughReceiverChannelTestCase(TestCase):
        """
        Test ``ThroughReceiverChannel`` common class
        """
        PARTIAL_TRACE_NAME_TO_CHECK = ""
        TEST_OBJECT_CLASS = None
        PROTOCOL_TYPE = None

        def setUp(self):
            # See ``TestCase.setUp``
            self.usb_context_device = UsbContextDevice(reader_name="test device", vid=0xA5A5, pid=0x5A5A)
            self.usb_context_device.connected = True
            # Each interface has the format (interface_id, protocol, ep_id, size)
            self.usb_context_device.interface_list = [
                (0, LogitechReportType.HIDPP, [(0 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
                (1, LogitechReportType.MOUSE, [(1 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
                (2, LogitechReportType.KEYBOARD, [(2 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)])]

            self.usb_context = None
            self.receiver_channel = None

            self.trace_name_to_check = None
        # end def setUp

        def tearDown(self):
            # See ``TestCase.tearDown``
            self.receiver_channel.close()
        # end def tearDown

        def test_creation_business(self):
            """
            Test creation of a ``ThroughReceiverChannel`` object
            """
            trace_level_to_use = TraceLevel.WARNING
            trace_file_name_to_use = None

            test_object = self._get_test_object(
                trace_level_to_use=trace_level_to_use, trace_file_name_to_use=trace_file_name_to_use)

            self._check_after_creation(test_object=test_object,
                                       trace_level_to_check=trace_level_to_use)
        # end def test_creation_business

        def test_open_business(self):
            """
            Test open method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()

            self.receiver_channel.open()
            test_object.open()

            self._check_after_opening(test_object=test_object)
        # end def test_open_business

        def test_close_business(self):
            """
            Test close method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()

            self.receiver_channel.open()
            test_object.open()
            test_object.close()

            self._check_after_closing(test_object=test_object)
        # end def test_close_business

        def test_turn_on_hardware_device_business(self):
            """
            Test turn_on_hardware_device method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()
            test_object.hardware_device = MockHardwareDevice()
            test_object.turn_on_hardware_device()

            self.assertTrue(
                expr=test_object.hardware_device.is_on,
                msg="Hardware device should be open after turn_on_hardware_device() method is called and passed")
            self.assertFalse(
                expr=test_object.is_open,
                msg="ThroughReceiverChannel should not be opened after turn_on_hardware_device() method is called "
                    "and passed")
            self.assertTrue(
                expr=(test_object.hidpp_time_stamped_msg_queue is None or
                      test_object.hidpp_time_stamped_msg_queue.qsize() == 0),
                msg="The time stamped message queue should be None or empty after turn_off_hardware_device() method is "
                    "called and passed")

            self.receiver_channel.open()
            test_object.open()

            self._check_after_opening(test_object=test_object)
        # end def test_turn_on_hardware_device_business

        def test_turn_off_hardware_device_business(self):
            """
            Test turn_off_hardware_device method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()
            test_object.hardware_device = MockHardwareDevice()
            test_object.turn_on_hardware_device()
            self.receiver_channel.open()
            test_object.open()
            test_object.turn_off_hardware_device()

            self.assertFalse(
                expr=test_object.hardware_device.is_on,
                msg="Hardware device should be closed after turn_off_hardware_device() method is called and passed")
            self.assertFalse(
                expr=test_object.is_open,
                msg="UsbChannel should be closed after turn_off_hardware_device() method is called and passed")
            self.assertTrue(
                expr=(test_object.hidpp_time_stamped_msg_queue is None or
                      test_object.hidpp_time_stamped_msg_queue.qsize() == 0),
                msg="The time stamped message queue should be None or empty after turn_off_hardware_device() method is "
                    "called and passed")
        # end def test_turn_off_hardware_device_business

        def test_send_data_business(self):
            """
            Test send_data method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()

            self.receiver_channel.open()
            test_object.open()
            data = HexList([0]*HidppMessage.SHORT_MSG_SIZE)
            data[HidppMessage.OFFSET.DEVICE_INDEX] = test_object.device_index
            test_object.send_data(data=data)
        # end def test_send_data_business

        def test_get_message_business(self):
            """
            Test get_message method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()
            self._common_test_get_message(
                test_object=test_object, queue_to_put=test_object.hidpp_time_stamped_msg_queue)
        # end def test_get_message_business

        def test_is_device_connected_business(self):
            """
            Test is_device_connected method of a ``ThroughReceiverChannel`` object when link is established
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()

            self._common_test_is_device_connected(test_object=test_object)
        # end def test_is_device_connected_business

        def test_get_device_info_business(self):
            """
            Test get_device_info method of a ``ThroughReceiverChannel`` object when channel is not open (but receiver
            channel is).
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()

            self._common_test_get_device_info(test_object=test_object)
        # end def test_get_device_info_business

        def test_is_device_connected_channel_not_open(self):
            """
            Test is_device_connected method of a ``ThroughReceiverChannel`` object when channel is not open
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()

            self._common_test_is_device_connected(test_object=test_object)
        # end def test_is_device_connected_channel_not_open

        def test_is_device_connected_receiver_channel_not_open(self):
            """
            Test is_device_connected method of a ``ThroughReceiverChannel`` object when its receiver channel is not open
            """
            test_object = self._get_test_object()

            self._common_test_is_device_connected(test_object=test_object)
        # end def test_is_device_connected_receiver_channel_not_open

        def test_is_device_connected_link_not_established(self):
            """
            Test is_device_connected method of a ``ThroughReceiverChannel`` object when link is not established
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()

            list_message_to_receive = self._get_list_for_is_device_connected(
                link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            self.usb_context.list_message_to_receive = list_message_to_receive

            is_device_connected = test_object.is_device_connected(force_refresh_cache=True)

            self.assertEqual(first=len(list_message_to_receive),
                             second=0,
                             msg="The number of response left in the list is not the expected one")
            self.assertFalse(expr=is_device_connected, msg="The device should be seen as connected")

            self._check_after_closing(test_object=test_object)
        # end def test_is_device_connected_link_not_established

        def test_is_device_connected_device_not_paired(self):
            """
            Test is_device_connected method of a ``ThroughReceiverChannel`` object when device is not paired (thus
            having no DeviceConnection event).
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()

            list_message_to_receive = [
                TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                        receiver_reporting_flag_wireless_notifications=True))),
                TransportMessage(data=HexList(SetConnectionStateResponse()))]
            self.usb_context.list_message_to_receive = list_message_to_receive

            is_device_connected = test_object.is_device_connected(force_refresh_cache=True)

            self.assertEqual(first=len(list_message_to_receive),
                             second=0,
                             msg="The number of response left in the list is not the expected one")
            self.assertFalse(expr=is_device_connected, msg="The device should be seen as connected")

            self._check_after_closing(test_object=test_object)
        # end def test_is_device_connected_device_not_paired

        def test_get_device_info_cache(self):
            """
            Test get_device_info method of a ``ThroughReceiverChannel`` object when channel is not open
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()

            get_pairing_info_response_class = NonVolatilePairingInformationModel.get_message_cls(
                sub_id=Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                message_type="response",
                r0=self.TEST_OBJECT_CLASS.DEVICE_PAIRING_INFORMATION_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)
            get_name_response_class = NonVolatilePairingInformationModel.get_message_cls(
                sub_id=Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                message_type="response",
                r0=self.TEST_OBJECT_CLASS.DEVICE_NAME_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)
            list_message_to_receive = [
                TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                    receiver_reporting_flag_wireless_notifications=True))),
                TransportMessage(data=HexList(get_pairing_info_response_class(
                    r0=self.TEST_OBJECT_CLASS.DEVICE_PAIRING_INFORMATION_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1))),
                TransportMessage(data=HexList(get_name_response_class(
                    r0=self.TEST_OBJECT_CLASS.DEVICE_NAME_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1))),
                TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                    receiver_reporting_flag_wireless_notifications=True))),
                TransportMessage(data=HexList(get_pairing_info_response_class(
                    r0=self.TEST_OBJECT_CLASS.DEVICE_PAIRING_INFORMATION_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1))),
                TransportMessage(data=HexList(get_name_response_class(
                    r0=self.TEST_OBJECT_CLASS.DEVICE_NAME_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)))]
            self.usb_context.list_message_to_receive = list_message_to_receive

            device_info_1 = test_object.get_device_info()
            device_info_2 = test_object.get_device_info()

            self.assertEqual(first=len(list_message_to_receive),
                             second=3,
                             msg="The number of response left in the list is not the expected one")
            self.assertEqual(first=device_info_1,
                             second=device_info_2,
                             msg="The value returned is not a cache")
            self.assertIsInstance(
                obj=device_info_1[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_PAIRING_INFORMATION],
                cls=get_pairing_info_response_class,
                msg="The class for device pairing information is not the expected one")
            self.assertIsInstance(
                obj=device_info_1[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_NAME],
                cls=get_name_response_class,
                msg="The class for device name is not the expected one")
        # end def test_get_device_info_cache

        def test_get_device_info_force_refresh_cache(self):
            """
            Test get_device_info method of a ``ThroughReceiverChannel`` object when channel is not open
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()

            get_pairing_info_response_class = NonVolatilePairingInformationModel.get_message_cls(
                sub_id=Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                message_type="response",
                r0=self.TEST_OBJECT_CLASS.DEVICE_PAIRING_INFORMATION_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)
            get_pairing_info_response_1 = HexList(get_pairing_info_response_class(
                r0=self.TEST_OBJECT_CLASS.DEVICE_PAIRING_INFORMATION_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1))
            get_pairing_info_response_2 = HexList(get_pairing_info_response_class(
                r0=self.TEST_OBJECT_CLASS.DEVICE_PAIRING_INFORMATION_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1))
            get_pairing_info_response_2[GetLongRegister.OFFSET.ADDRESS + 2] = 0xFF

            get_name_response_class = NonVolatilePairingInformationModel.get_message_cls(
                sub_id=Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                message_type="response",
                r0=self.TEST_OBJECT_CLASS.DEVICE_NAME_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)

            list_message_to_receive = [
                TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                    receiver_reporting_flag_wireless_notifications=True))),
                TransportMessage(data=get_pairing_info_response_1),
                TransportMessage(data=HexList(get_name_response_class(
                    r0=self.TEST_OBJECT_CLASS.DEVICE_NAME_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1))),
                TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                    receiver_reporting_flag_wireless_notifications=True))),
                TransportMessage(data=get_pairing_info_response_2),
                TransportMessage(data=HexList(get_name_response_class(
                    r0=self.TEST_OBJECT_CLASS.DEVICE_NAME_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)))]
            self.usb_context.list_message_to_receive = list_message_to_receive

            device_info_1 = test_object.get_device_info()
            # A copy of the object is needed as the object returned is the cache, device_info_1 and device_info_2 will
            # always be the same
            old_device_info = device_info_1.copy()
            device_info_2 = test_object.get_device_info(force_refresh_cache=True)

            self.assertEqual(first=len(list_message_to_receive),
                             second=0,
                             msg="The number of response left in the list is not the expected one")
            self.assertEqual(first=device_info_1,
                             second=device_info_2,
                             msg="The value returned is not a cache")
            self.assertNotEqual(first=old_device_info,
                                second=device_info_2,
                                msg="The second value returned is still the old cache value")
            self.assertIsInstance(
                obj=device_info_1[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_PAIRING_INFORMATION],
                cls=get_pairing_info_response_class,
                msg="The class for device pairing information is not the expected one")
            self.assertIsInstance(
                obj=device_info_1[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_NAME],
                cls=get_name_response_class,
                msg="The class for device name is not the expected one")
        # end def test_get_device_info_force_refresh_cache

        def test_get_device_info_channel_not_open(self):
            """
            Test get_device_info method of a ``ThroughReceiverChannel`` object when channel is not open
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()

            self._common_test_get_device_info(test_object=test_object)
        # end def test_get_device_info_channel_not_open

        def test_get_device_info_receiver_channel_not_open(self):
            """
            Test get_device_info method of a ``ThroughReceiverChannel`` object when its receiver channel is not open
            raise an exception
            """
            test_object = self._get_test_object()

            self._common_test_get_device_info(test_object=test_object)
        # end def test_get_device_info_receiver_channel_not_open

        def test_get_message_message_put_in_the_receiver_queue(self):
            """
            Test get_message method of a ``ThroughReceiverChannel`` object when message is put in the receiver queue
            with the right device index
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()
            self._common_test_get_message(
                test_object=test_object,
                queue_to_put=self.receiver_channel.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP])
        # end def test_get_message_message_put_in_the_receiver_queue

        def test_open_link_enabler_empty(self):
            """
            Test open method of a ``ThroughReceiverChannel`` object with different link enabler
            """
            test_object = self._get_test_object()

            self.receiver_channel.open()
            test_object.open(link_enabler=0)

            self.assertTrue(expr=test_object.is_open,
                            msg="ThroughReceiverChannel should be open after open() method is called and passed")
            self.assertIsNotNone(
                obj=test_object.hidpp_time_stamped_msg_queue,
                msg="The time stamped message queue should be None if open with no HID++ link enabler")
        # end def test_open_link_enabler_empty

        def test_send_data_different_data_size(self):
            """
            Test send_data method of a ``ThroughReceiverChannel`` object with different data size
            """
            test_object = self._get_test_object()

            self.receiver_channel.open()
            test_object.open()

            for data_size in HidppMessage.HIDPP_REPORT_LEN_LIST:
                data = HexList([0]*data_size)
                data[HidppMessage.OFFSET.DEVICE_INDEX] = test_object.device_index
                test_object.send_data(data=data)
            # end for
        # end def test_send_data_different_data_size

        def test_multiple_open(self):
            """
            Test multiple call of open method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()

            self.receiver_channel.open()
            for _ in range(5):
                test_object.open()
            # end for

            self._check_after_opening(test_object=test_object)
        # end def test_multiple_open

        def test_multiple_close(self):
            """
            Test multiple call of close method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()

            self.receiver_channel.open()
            test_object.open()

            for _ in range(5):
                test_object.close()
            # end for

            self._check_after_closing(test_object=test_object)
        # end def test_multiple_close

        def test_close_receiver_channel(self):
            """
            Test close method of a ``ThroughReceiverChannel`` object
            """
            test_object = self._get_test_object()

            self.receiver_channel.open()
            test_object.open()
            self.receiver_channel.close()

            # Closing the receiver channel should have closed the test object channel
            self._check_after_closing(test_object=test_object)
        # end def test_close_receiver_channel

        def test_message_put_in_receiver_channel_queue_with_wrong_device_index(self):
            """
            Test data put in the receiver channel queue of a ``ThroughReceiverChannel`` object but with the wrong
            device index should not have the data in the tes object queue.
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()
            data = HexList([0]*HidppMessage.SHORT_MSG_SIZE)

            for device_index in compute_wrong_range(
                    value=test_object.device_index, min_value=1, max_value=MAX_NUMBER_OF_PAIRED_DEVICES_FOR_TEST):
                data[HidppMessage.OFFSET.DEVICE_INDEX] = device_index
                message_to_put = TransportMessage(data=data)
                self.receiver_channel.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP].put(message_to_put)

                exception = self._get_message_with_exception(test_object=test_object)

                self.assertIsNotNone(
                    obj=exception,
                    msg="get_message() should not passed if the device index of the message is not the right one")
                self.assertIsInstance(obj=exception,
                                      cls=Empty,
                                      msg="The exception should be of type queue.Empty")

                # Remove message before testing next value
                self.receiver_channel.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP].get()
            # end for
        # end def test_message_put_in_receiver_channel_queue_with_wrong_device_index

        def test_error_open_hidpp_receiver_channel_link_disable(self):
            """
            Test open method of a ``ThroughReceiverChannel`` object when the HID++ of the receiver channel link
            is disabled raise an exception
            """
            test_object = self._get_test_object()
            self.receiver_channel.open(link_enabler=LinkEnablerInfo.MOUSE_MASK | LinkEnablerInfo.KEYBOARD_MASK)

            exception = self._open_with_exception(test_object=test_object)

            self.assertIsNotNone(
                obj=exception, msg="open() should not passed if the HID++ of the receiver channel link is disabled")
            self.assertEqual(
                first=exception.get_cause(),
                second=ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT,
                msg="ChannelException cause should be ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT")
        # end def test_error_open_hidpp_receiver_channel_link_disable

        def test_error_open_when_hardware_device_off(self):
            """
            Test open method of a ``UsbChannel`` object when the hardware device is off raise an exception
            """
            test_object = self._get_test_object()
            test_object.hardware_device = MockHardwareDevice()
            self.receiver_channel.open()

            exception = self._open_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception, msg="open() should not passed if the hardware device is off")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.HARDWARE_DEVICE_OFF,
                             msg="ChannelException cause should be HARDWARE_DEVICE_OFF")
        # end def test_error_open_when_hardware_device_off

        def test_error_open_when_link_not_established(self):
            """
            Test open method of a ``UsbChannel`` object when the link is not established raise an exception
            """
            test_object = self._get_test_object(link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            self.receiver_channel.open()

            exception = self._open_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception, msg="open() should not passed if the hardware device is off")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.DEVICE_NOT_CONNECTED,
                             msg="ChannelException cause should be DEVICE_NOT_CONNECTED")
        # end def test_error_open_when_link_not_established

        def test_error_open_when_device_not_paired(self):
            """
            Test open method of a ``UsbChannel`` object when device is not paired (thus having no DeviceConnection
            event) raise an exception.
            """
            test_object = self._get_test_object()
            list_message_to_receive = [
                TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                        receiver_reporting_flag_wireless_notifications=True))),
                TransportMessage(data=HexList(SetConnectionStateResponse()))]
            self.usb_context.list_message_to_receive = list_message_to_receive
            self.receiver_channel.open()

            exception = self._open_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception, msg="open() should not passed if the hardware device is off")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.DEVICE_NOT_CONNECTED,
                             msg="ChannelException cause should be DEVICE_NOT_CONNECTED")
        # end def test_error_open_when_device_not_paired

        def test_send_data_error_channel_closed(self):
            """
            Test send_data method of a ``ThroughReceiverChannel`` object when the channel is closed raise an exception
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()

            exception = self._send_data_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception, msg="send_data() should not passed if the channel is closed")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.CHANNEL_NOT_OPEN,
                             msg="ChannelException cause should be CHANNEL_NOT_OPEN")
        # end def test_send_data_error_channel_closed

        def test_send_data_error_both_channel_and_receiver_channel_closed(self):
            """
            Test send_data method of a ``ThroughReceiverChannel`` object when the channel is closed raise an exception
            """
            test_object = self._get_test_object()

            exception = self._send_data_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception, msg="send_data() should not passed if the channel is closed")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.CHANNEL_NOT_OPEN,
                             msg="ChannelException cause should be CHANNEL_NOT_OPEN")
        # end def test_send_data_error_both_channel_and_receiver_channel_closed

        def test_send_data_error_hidpp_link_disable(self):
            """
            Test send_data method of a ``ThroughReceiverChannel`` object when the HID++ link is disabled raise an
            exception
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()

            test_object.open(link_enabler=0)

            exception = self._send_data_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception, msg="send_data() should not passed if the HID++ link is disabled")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                             msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
        # end def test_send_data_error_hidpp_link_disable

        def test_send_data_error_wrong_data_size(self):
            """
            Test send_data method of a ``ThroughReceiverChannel`` object when the data size is wrong
            (error risen from receiver channel) raise an exception
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open()

            for data_size in compute_wrong_range(
                    HidppMessage.HIDPP_REPORT_LEN_LIST, max_value=HidppMessage.VERY_LONG_MSG_SIZE):
                exception = self._send_data_with_exception(test_object=test_object, data_size=data_size)

                self.assertIsNotNone(
                    obj=exception,
                    msg=f"send_data() should not passed if the data size is wrong (data_size={data_size})")
                self.assertEqual(first=exception.get_cause(),
                                 second=ChannelException.Cause.WRONG_PARAMETER,
                                 msg=f"ChannelException cause should be WRONG_PARAMETER (data_size={data_size})")
            # end for
        # end def test_send_data_error_wrong_data_size

        def test_send_data_error_wrong_data_size_sent(self):
            """
            Test send_data method of a ``ThroughReceiverChannel`` object when the data size is wrong
            (error risen from receiver channel) raise an exception
            """
            for difference_bytes_sent in compute_wrong_range(
                    0, min_value=-int(HidppMessage.SHORT_MSG_SIZE/2), max_value=int(HidppMessage.SHORT_MSG_SIZE/2)):
                self.usb_context = MockUsbContext()
                self.receiver_channel = UsbReceiverChannel(
                    max_number_of_paired_devices=MAX_NUMBER_OF_PAIRED_DEVICES_FOR_TEST,
                    usb_context=self.usb_context,
                    usb_context_device=self.usb_context_device)
                test_object = self._get_test_object()
                self.receiver_channel.open()
                test_object.open()

                self.usb_context.difference_bytes_sent = difference_bytes_sent
                exception = self._send_data_with_exception(test_object=test_object)

                self.assertIsNotNone(
                    obj=exception,
                    msg=f"send_data() should not passed if the data size sent is wrong "
                        f"(difference_bytes_sent={difference_bytes_sent})")
                self.assertEqual(
                    first=exception.get_cause(),
                    second=ChannelException.Cause.ERROR_BYTES_ARE_SENT,
                    msg=f"ChannelException cause should be NOT_ALL_BYTES_ARE_SENT "
                        f"(difference_bytes_sent={difference_bytes_sent})")
            # end for
        # end def test_send_data_error_wrong_data_size_sent

        def test_get_message_error_channel_closed(self):
            """
            Test get_message method of a ``ThroughReceiverChannel`` object when the channel is closed raise an exception
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()

            exception = self._get_message_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception, msg="get_message() should not passed if the channel is closed")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.CHANNEL_NOT_OPEN,
                             msg="ChannelException cause should be CHANNEL_NOT_OPEN")
        # end def test_get_message_error_channel_closed

        def test_get_message_error_both_channel_and_receiver_channel_closed(self):
            """
            Test get_message method of a ``UsbChannel`` object when the channel is closed raise an exception
            """
            test_object = self._get_test_object()

            exception = self._get_message_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception, msg="get_message() should not passed if the channel is closed")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.CHANNEL_NOT_OPEN,
                             msg="ChannelException cause should be CHANNEL_NOT_OPEN")
        # end def test_get_message_error_channel_closed

        def test_get_message_error_hidpp_link_disable(self):
            """
            Test get_message method of a ``ThroughReceiverChannel`` object when the HID++ link is disabled raise an
            exception
            """
            test_object = self._get_test_object()
            self.receiver_channel.open()
            test_object.open(link_enabler=0)

            exception = self._get_message_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception,
                                 msg="get_message() should not passed if the HID++ interface is not present")
            self.assertEqual(first=exception.get_cause(),
                             second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                             msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
        # end def test_get_message_error_hidpp_link_disable

        def test_get_message_error_receiver_channel_mouse_link_disable(self):
            """
            Test get_message method of a ``ThroughReceiverChannel`` object when the Mouse link of the receiver channel
            is disabled raise an exception
            """
            test_object = self._get_test_object()
            self.receiver_channel.open(link_enabler=LinkEnablerInfo.HID_PP_MASK | LinkEnablerInfo.KEYBOARD_MASK)
            test_object.open()

            exception = self._get_message_with_exception(test_object=test_object, report_type=LogitechReportType.MOUSE)

            self.assertIsNotNone(
                obj=exception,
                msg="get_message() should not passed if the Mouse link of the receiver channel is disabled")
            self.assertEqual(
                first=exception.get_cause(),
                second=ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT,
                msg="ChannelException cause should be ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT")
        # end def test_get_message_error_receiver_channel_mouse_link_disable

        def test_get_message_error_receiver_channel_keyboard_link_disable(self):
            """
            Test get_message method of a ``ThroughReceiverChannel`` object when the Keyboard link of the receiver
            channel is disabled raise an exception
            """
            test_object = self._get_test_object()
            self.receiver_channel.open(link_enabler=LinkEnablerInfo.HID_PP_MASK | LinkEnablerInfo.MOUSE_MASK)
            test_object.open()

            exception = self._get_message_with_exception(
                test_object=test_object, report_type=LogitechReportType.KEYBOARD)

            self.assertIsNotNone(
                obj=exception,
                msg="get_message() should not passed if the Keyboard link of the receiver channel is disabled")
            self.assertEqual(
                first=exception.get_cause(),
                second=ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT,
                msg="ChannelException cause should be ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT")
        # end def test_get_message_error_receiver_channel_keyboard_link_disable

        def test_is_device_connected_error_receiver_channel_hidpp_interface_not_present(self):
            """
            Test is_device_connected method of a ``ThroughReceiverChannel`` object when the HID++ interface of its
            receiver channel is not present raise an exception
            """
            test_object = self._get_test_object()
            self.usb_context_device.interface_list = [
                (1, LogitechReportType.MOUSE, [(1 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
                (2, LogitechReportType.KEYBOARD, [(2 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)])]
            self.receiver_channel.open()

            exception = self._is_device_connected_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception,
                                 msg="is_device_connected() should not passed if the receiver channel is not open")
            self.assertEqual(
                first=exception.get_cause(),
                second=ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT,
                msg="ChannelException cause should be ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT")
        # end def test_is_device_connected_error_receiver_channel_hidpp_interface_not_present

        def test_get_device_info_error_receiver_channel_hidpp_interface_not_present(self):
            """
            Test get_device_info method of a ``ThroughReceiverChannel`` object when the HID++ interface of its
            receiver channel is not present raise an exception
            """
            test_object = self._get_test_object()
            self.usb_context_device.interface_list = [
                (1, LogitechReportType.MOUSE, [(1 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
                (2, LogitechReportType.KEYBOARD, [(2 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)])]
            self.receiver_channel.open()

            exception = self._get_device_info_with_exception(test_object=test_object)

            self.assertIsNotNone(obj=exception,
                                 msg="is_device_connected() should not passed if the receiver channel is not open")
            self.assertEqual(
                first=exception.get_cause(),
                second=ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT,
                msg="ChannelException cause should be ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT")
        # end def test_get_device_info_error_receiver_channel_hidpp_interface_not_present

        def _get_test_object(self,
                             add_open_response_list=True,
                             link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                             device_index=DEVICE_INDEX_FOR_TEST,
                             trace_level_to_use=TraceLevel.WARNING,
                             trace_file_name_to_use=None):
            """
            Get the test object with different options. Opening a ``ThroughReceiverChannel`` require some
            communication to check the link status, that is why it needs a list of response for opening.

            :param add_open_response_list: Flag indicating that the list of expected response when opening the channel
                                           have to be included in the mock context - OPTIONAL
            :type add_open_response_list: ``bool``
            :param link_status: Value of ``device_info_link_status`` in the ``DeviceConnection`` packet. Values can
                                be found in ``DeviceConnection.LinkStatus`` - OPTIONAL
            :type link_status: ``int``
            :param device_index: Index of the device in the receiver - OPTIONAL
            :type device_index: ``int``
            :param trace_level_to_use: Trace level of the channel - OPTIONAL
            :type trace_level_to_use: ``TraceLevel`` or ``int``
            :param trace_file_name_to_use: Trace output of the channel - OPTIONAL
            :type trace_file_name_to_use: ``str`` or ``None``

            :return: The test object
            :rtype: ``ThroughReceiverChannel``
            """
            if add_open_response_list:
                list_message_to_receive = self._get_list_for_is_device_connected(link_status=link_status)
            else:
                list_message_to_receive = None
            # end if

            self.usb_context = MockUsbContext(list_message_to_receive=list_message_to_receive)
            self.receiver_channel = UsbReceiverChannel(
                max_number_of_paired_devices=MAX_NUMBER_OF_PAIRED_DEVICES_FOR_TEST,
                usb_context=self.usb_context,
                usb_context_device=self.usb_context_device)

            return self.TEST_OBJECT_CLASS(receiver_channel=self.receiver_channel,
                                          device_index=device_index,
                                          trace_level=trace_level_to_use,
                                          trace_file_name=trace_file_name_to_use)
        # end def _get_test_object

        def _check_after_creation(self, test_object, trace_level_to_check):
            """
            Check test object after creation.

            :param test_object: Test object to check
            :type test_object: ``ThroughReceiverChannel``
            :param trace_level_to_check: Trace level of the channel to check
            :type trace_level_to_check: ``TraceLevel`` or ``int``
            """
            self.assertFalse(
                expr=test_object.is_open, msg="ThroughReceiverChannel is_open property should be false at creation")

            trace_name = TRACE_LOGGER.get_trace_name(subscription_owner=test_object)
            self.assertIn(member=self.PARTIAL_TRACE_NAME_TO_CHECK,
                          container=trace_name,
                          msg="The expected partial trace name is not the actual trace name")
            self.assertIn(member=f"{test_object.device_index}",
                          container=trace_name,
                          msg="The device index is not the actual trace name")

            trace_output = TRACE_LOGGER.get_trace_output(subscription_owner=test_object)
            self.assertEqual(first=trace_output, second=sys.stdout, msg="The trace output is not the expected one")

            trace_level = TRACE_LOGGER.get_trace_level(subscription_owner=test_object)
            self.assertEqual(
                first=trace_level, second=trace_level_to_check, msg="The trace level is not the expected one")

            self.assertIsNotNone(
                obj=test_object.hidpp_time_stamped_msg_queue,
                msg="The time stamped message queue should not be None after creation")
        # end def _check_after_creation

        def _check_after_opening(self, test_object):
            """
            Check test object after calling the ``open`` method.

            :param test_object: Test object to check
            :type test_object: ``ThroughReceiverChannel``
            """
            self.assertTrue(expr=test_object.is_open,
                            msg="ThroughReceiverChannel should be open after open() method is called and passed")

            self.assertIsNotNone(obj=test_object.hidpp_time_stamped_msg_queue,
                                 msg="The time stamped message queue should not be None after creation")
            self.assertIsInstance(obj=test_object.hidpp_time_stamped_msg_queue,
                                  cls=Queue,
                                  msg="The time stamped message queue should be a Queue after creation")
            self.assertEqual(first=test_object.protocol,
                             second=self.PROTOCOL_TYPE,
                             msg="The protocol parameter is not the expected one")
        # end def _check_after_opening

        def _check_after_closing(self, test_object):
            """
            Check test object after calling the ``close`` method.

            :param test_object: Test object to check
            :type test_object: ``ThroughReceiverChannel``
            """
            self.assertFalse(
                expr=test_object.is_open, msg="ThroughReceiverChannel should be closed after close() method is called "
                                              "and passed")
            self.assertTrue(
                expr=(test_object.hidpp_time_stamped_msg_queue is None or
                      test_object.hidpp_time_stamped_msg_queue.qsize() == 0),
                msg="The time stamped message queue should be None or empty after close() method is called and passed")
            self.assertEqual(first=test_object.protocol,
                             second=self.PROTOCOL_TYPE,
                             msg="The protocol parameter is not the expected one")
        # end def _check_after_closing

        def _common_test_get_message(self, test_object, queue_to_put):
            """
            Common implementation for tests to use get_message but with different queue where the message is put
            before the get.

            :param queue_to_put: Queue to put the message in
            :type queue_to_put: ``Queue``
            """
            data = HexList([0]*HidppMessage.SHORT_MSG_SIZE)
            data[HidppMessage.OFFSET.DEVICE_INDEX] = test_object.device_index
            message_to_put = TransportMessage(data=data)
            queue_to_put.put(message_to_put)
            message_to_get = test_object.get_message()

            self.assertEqual(first=message_to_put,
                             second=message_to_get,
                             msg="Message received is not the expected one")
        # end def _common_test_get_message

        def _common_test_is_device_connected(self, test_object):
            """
            Common implementation for tests to use is_device_connected.
            """
            list_message_to_receive = self._get_list_for_is_device_connected()
            self.usb_context.list_message_to_receive = list_message_to_receive

            is_device_connected = test_object.is_device_connected(force_refresh_cache=True)

            self.assertEqual(first=len(list_message_to_receive),
                             second=0,
                             msg="The number of response left in the list is not the expected one")
            self.assertTrue(expr=is_device_connected, msg="The device should be seen as connected")
            self.assertEqual(first=test_object.protocol,
                             second=self.PROTOCOL_TYPE,
                             msg="The protocol parameter is not the expected one")
        # end def _common_test_is_device_connected

        def _common_test_get_device_info(self, test_object):
            """
            Common implementation for tests to use get_device_info.
            """
            get_pairing_info_response_class = NonVolatilePairingInformationModel.get_message_cls(
                sub_id=Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                message_type="response",
                r0=self.TEST_OBJECT_CLASS.DEVICE_PAIRING_INFORMATION_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)
            get_name_response_class = NonVolatilePairingInformationModel.get_message_cls(
                sub_id=Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                message_type="response",
                r0=self.TEST_OBJECT_CLASS.DEVICE_NAME_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)
            list_message_to_receive = [
                TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                    receiver_reporting_flag_wireless_notifications=True))),
                TransportMessage(data=HexList(get_pairing_info_response_class(
                    r0=self.TEST_OBJECT_CLASS.DEVICE_PAIRING_INFORMATION_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1))),
                TransportMessage(data=HexList(get_name_response_class(
                    r0=self.TEST_OBJECT_CLASS.DEVICE_NAME_MIN_R0 + DEVICE_INDEX_FOR_TEST - 1)))]
            self.usb_context.list_message_to_receive = list_message_to_receive

            device_info = test_object.get_device_info()

            self.assertEqual(first=len(list_message_to_receive),
                             second=0,
                             msg="The number of response left in the list is not the expected one")
            self.assertIsInstance(
                obj=device_info[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_PAIRING_INFORMATION],
                cls=get_pairing_info_response_class,
                msg="The class for device pairing information is not the expected one")
            self.assertIsInstance(
                obj=device_info[ThroughReceiverChannel.DeviceInformationOffset.DEVICE_NAME],
                cls=get_name_response_class,
                msg="The class for device name is not the expected one")
        # end def _common_test_get_device_info

        @staticmethod
        def _open_with_exception(test_object):
            """
            Call open and catch ChannelException if any.

            :param test_object: USB channel under test
            :type test_object: ``ThroughReceiverChannel``

            :return: Caught exception if any
            :rtype: ``ChannelException`` or ``None``
            """
            try:
                test_object.open()
            except ChannelException as e:
                return e
            # end try

            return None
        # end def _open_with_exception

        @staticmethod
        def _get_message_with_exception(test_object, report_type=LogitechReportType.HIDPP):
            """
            Call get_message and catch ChannelException if any.

            :param test_object: USB channel under test
            :type test_object: ``ThroughReceiverChannel``

            :return: Caught exception if any
            :rtype: ``ChannelException`` or ``None``
            """
            try:
                test_object.get_message(report_type=report_type, timeout=.01)
            except ChannelException as e:
                return e
            except Empty as e:
                return e
            # end try
            return None
        # end def _get_message_with_exception

        @staticmethod
        def _send_data_with_exception(test_object, data_size=HidppMessage.SHORT_MSG_SIZE):
            """
            Call send_data and catch ChannelException if any.

            :param test_object: USB channel under test
            :type test_object: ``ThroughReceiverChannel``
            :param data_size: Data size to send - OPTIONAL
            :type data_size: ``int``

            :return: Caught exception if any
            :rtype: ``ChannelException`` or ``None``
            """
            try:
                data = HexList([0]*data_size)
                if len(data) > HidppMessage.OFFSET.DEVICE_INDEX:
                    data[HidppMessage.OFFSET.DEVICE_INDEX] = test_object.device_index
                # end if
                test_object.send_data(data=data)
            except ChannelException as e:
                return e
            # end try
            return None
        # end def _send_data_with_exception

        @staticmethod
        def _is_device_connected_with_exception(test_object):
            """
            Call is_device_connected and catch ChannelException if any.

            :param test_object: USB channel under test
            :type test_object: ``ThroughReceiverChannel``

            :return: Caught exception if any
            :rtype: ``ChannelException`` or ``None``
            """
            try:
                test_object.is_device_connected(force_refresh_cache=True)
            except ChannelException as e:
                return e
            # end try
            return None
        # end def _is_device_connected_with_exception

        @staticmethod
        def _get_device_info_with_exception(test_object):
            """
            Call get_device_info and catch ChannelException if any.

            :param test_object: USB channel under test
            :type test_object: ``ThroughReceiverChannel``

            :return: Caught exception if any
            :rtype: ``ChannelException`` or ``None``
            """
            try:
                test_object.get_device_info()
            except ChannelException as e:
                return e
            # end try
            return None
        # end def _get_device_info_with_exception

        def _get_list_for_is_device_connected(self, link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED):
            """
            Get the list of expected response for the method ``is_device_connected``

            :param link_status: Value of ``device_info_link_status`` in the ``DeviceConnection`` packet. Values can
                                be found in ``DeviceConnection.LinkStatus`` - OPTIONAL
            :type link_status: ``int``

            :return: The list of expected response
            :rtype: ``list[TransportMessage | list[TransportMessage]]``
            """
            device_information = self.TEST_OBJECT_CLASS.DEVICE_INFORMATION_CLASS.fromHexList(HexList("000000"))
            device_information.device_info_link_status = link_status
            return [TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                        receiver_reporting_flag_wireless_notifications=True))),
                    [TransportMessage(data=HexList(DeviceConnection(
                        device_index=DEVICE_INDEX_FOR_TEST,
                        protocol_type=self.PROTOCOL_TYPE,
                        information=HexList(device_information)))),
                     TransportMessage(data=HexList(SetConnectionStateResponse()))]]
        # end def _get_list_for_is_device_connected
    # end class CommonThroughReceiverChannelTestCase

    return CommonThroughReceiverChannelTestCase
# end def get_common_testcase_class


class ThroughEQuadReceiverChannelTestCase(get_common_testcase_class()):
    PARTIAL_TRACE_NAME_TO_CHECK = "Channel through eQuad receiver"
    TEST_OBJECT_CLASS = ThroughEQuadReceiverChannel
    PROTOCOL_TYPE = LogitechProtocol.EQUAD_STEP_4_DJ
# end class ThroughReceiverChannelTestCase


class ThroughBleProReceiverChannelTestCase(get_common_testcase_class()):
    PARTIAL_TRACE_NAME_TO_CHECK = "Channel through BLE Pro receiver"
    TEST_OBJECT_CLASS = ThroughBleProReceiverChannel
    PROTOCOL_TYPE = LogitechProtocol.BLE_PRO
# end class ThroughBleProReceiverChannelTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
