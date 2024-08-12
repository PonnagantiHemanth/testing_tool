#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pychannel.test.usbchannel_test
:brief: ``UsbChannel`` unit tests
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/08/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import sys
from unittest import TestCase

from pychannel.channelinterfaceclasses import ChannelException
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.usbchannel import LogitechReportType
from pychannel.usbchannel import UsbChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import GetEnableHidppReportingResponse
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import SetEnableHidppReportingResponse
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pylibrary.tools.docutils import DocUtils
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import synchronize_with_object_inner_lock
from pylibrary.tools.threadutils import ThreadedExecutor
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_wrong_range
from pytransport.transportmessage import TransportMessage
from pytransport.usb.usbconstants import EndpointDirection
from pytransport.usb.usbcontext import UsbContext
from pytransport.usb.usbcontext import UsbContextDevice

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()
INTERRUPT_DATA_SIZE = 64

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class MockUsbContext(UsbContext):
    """
    Mock USB context to be used in tests
    """

    def __init__(self, difference_bytes_sent=0, list_message_to_receive=None):
        """
        :param difference_bytes_sent: Bytes to add (or subtract if negative) in the return value
                                      of ``control_write`` - OPTIONAL
        :type difference_bytes_sent: ``int``
        :param list_message_to_receive: List of message to receive for each call of ``control_write`` - OPTIONAL
        :type list_message_to_receive: ``list[TransportMessage | list[TransportMessage]]`` or ``None``
        """
        self.difference_bytes_sent = difference_bytes_sent
        self.list_message_to_receive = list_message_to_receive
        self.hidpp_queue = None
        super().__init__()
        self._threaded_executor = MockThreadedExecutor()
    # end def __init__

    @classmethod
    def get_plugged_devices(cls, vid=None, pid=None):
        # See ``UsbContext.get_plugged_devices``
        return []
    # end def get_plugged_devices

    @classmethod
    def generate_configuration_file(cls, path, vid=None, pid=None, *args, **kwargs):
        # See ``UsbContext.generate_configuration_file``
        pass
    # end def generate_configuration_file

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def open(self):
        # See ``UsbContext.open``
        pass
    # end def open

    @synchronize_with_object_inner_lock("_opening_closing_lock")
    def close(self):
        # See ``UsbContext.close``
        pass
    # end def close

    def reset(self):
        # See ``UsbContext.reset``
        pass
    # end def reset

    def get_devices(self, index_in_cache=None, reader_name=None, vid=None, pid=None, *args, **kwargs):
        # See ``UsbContext.get_devices``
        return []
    # end def get_devices

    def open_device(self, usb_context_device):
        # See ``UsbContext.open_device``
        pass
    # end def open_device

    def close_device(self, usb_context_device):
        # See ``UsbContext.close_device``
        pass
    # end def close_device

    def control_write(self, usb_context_device, bm_request_type, b_request, w_value, w_index, data,
                      timeout=UsbContext.GENERIC_CONTROL_TIMEOUT, blocking=False, trace_owner=None):
        # See ``UsbContext.control_write``
        if self.list_message_to_receive is not None and \
                len(self.list_message_to_receive) > 0 and \
                self.hidpp_queue is not None:
            element_to_put = self.list_message_to_receive.pop(0)
            if isinstance(element_to_put, list):
                # This is to be able to add event with a response
                for element in element_to_put:
                    self.hidpp_queue.put(element)
                # end for
            else:
                self.hidpp_queue.put(element_to_put)
            # end if
        # end if
        return len(data.data) + self.difference_bytes_sent
    # end def control_write

    def control_read(self, usb_context_device, bm_request_type, b_request, w_value, w_index, w_length,
                     timeout=UsbContext.GENERIC_CONTROL_TIMEOUT, blocking=False, trace_owner=None):
        # See ``UsbContext.control_read``
        raise NotImplementedError("Not useful for testing")
    # end def control_read

    def bulk_write(self, usb_context_device, endpoint, data, timeout=0, blocking=False, trace_owner=None):
        # See ``UsbContext.bulk_write``
        raise NotImplementedError("Not useful for testing")
    # end def bulk_write

    def bulk_read(self, usb_context_device, endpoint, w_length, timeout=0, blocking=False, trace_owner=None):
        # See ``UsbContext.bulk_read``
        raise NotImplementedError("Not useful for testing")
    # end def bulk_read

    def interrupt_write(self, usb_context_device, endpoint, data, timeout=0, blocking=False, trace_owner=None):
        # See ``UsbContext.interrupt_write``
        raise NotImplementedError("Not useful for testing")
    # end def interrupt_write

    def interrupt_read(self, usb_context_device, endpoint, w_length, timeout=0, blocking=False, trace_owner=None):
        # See ``UsbContext.interrupt_read``
        raise NotImplementedError("Not useful for testing")
    # end def interrupt_read

    def start_interrupt_read_polling(self, usb_context_device, endpoint, w_length, time_stamped_msg_queue=None,
                                     trace_name=None, callback=None, discard_report=False):
        # See ``UsbContext.start_interrupt_read_polling``
        if trace_name == "HID++ polling":
            self.hidpp_queue = time_stamped_msg_queue
        # end if
    # end def start_interrupt_read_polling

    def stop_interrupt_read_polling(self, usb_context_device, endpoint=None):
        # See ``UsbContext.stop_interrupt_read_polling``
        self.hidpp_queue = None
    # end def stop_interrupt_read_polling

    def update_device_list(self):
        pass
    # end def update_device_list

    @staticmethod
    def get_driver_info():
        raise NotImplementedError("Not useful for testing")
    # end def get_driver_info

    def get_ascii_string_descriptor(self, usb_context_device, descriptor):
        raise NotImplementedError("Not useful for testing")
    # end def get_ascii_string_descriptor
# end class MockUsbContext


class MockThreadedExecutor:
    """
    Mock ThreadedExecutor for tests
    """
    @DocUtils.copy_doc(ThreadedExecutor.resume)
    def resume(self):
        # See ``ThreadedExecutor.resume``
        pass
    # end def resume

    @DocUtils.copy_doc(ThreadedExecutor.pause)
    def pause(self):
        # See ``ThreadedExecutor.pause``
        pass
    # end def pause
# end class MockThreadedExecutor


class MockHardwareDevice:
    def __init__(self):
        self.is_on = False
    # end def __init__

    def turn_on(self):
        self.is_on = True
    # end def turn_on

    def turn_off(self):
        self.is_on = False
    # end def turn_off
# end class MockHardwareDevice


class UsbChannelTestCase(TestCase):
    """
    Test ``UsbChannel`` Class
    """
    def setUp(self):
        reader_name = "test device"
        vid = 0xA5A5
        pid = 0x5A5A
        self.usb_context_device = UsbContextDevice(reader_name=reader_name, vid=vid, pid=pid)
        self.usb_context_device.connected = True
        # Each interface has the format (interface_id, protocol, ep_id, size)
        self.usb_context_device.interface_list = [
            (0, LogitechReportType.HIDPP, [(0 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
            (1, LogitechReportType.MOUSE, [(1 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
            (2, LogitechReportType.KEYBOARD, [(2 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
            (3, LogitechReportType.DIGITIZER, [(0 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)])]
    # end def setUp

    def test_creation_business(self):
        """
        Test creation of a ``UsbChannel`` object
        """
        trace_level_to_use = TraceLevel.WARNING
        trace_file_name_to_use = None

        test_object = self._get_test_object(
            trace_level_to_use=trace_level_to_use, trace_file_name_to_use=trace_file_name_to_use)

        self._check_after_creation(test_object=test_object, trace_level_to_use=trace_level_to_use)
    # end def test_creation_business

    def test_open_business(self):
        """
        Test open method of a ``UsbChannel`` object
        """
        test_object = self._get_test_object()

        test_object.open()

        self._check_after_opening(test_object=test_object)
    # end def test_open_business

    def test_close_business(self):
        """
        Test close method of a ``UsbChannel`` object
        """
        test_object = self._get_test_object()

        test_object.open()
        test_object.close()

        self._check_after_closing(test_object=test_object)
    # end def test_close_business

    def test_turn_on_hardware_device_business(self):
        """
        Test turn_on_hardware_device method of a ``UsbChannel`` object
        """
        test_object = self._get_test_object()
        test_object.hardware_device = MockHardwareDevice()
        test_object.turn_on_hardware_device()

        self.assertTrue(
            expr=test_object.hardware_device.is_on,
            msg="Hardware device should be open after turn_on_hardware_device() method is called and passed")
        self.assertFalse(
            expr=test_object.is_open,
            msg="UsbChannel should not be opened after turn_on_hardware_device() method is called and passed")
        self.assertEqual(
            first=len(test_object.report_type_to_interface),
            second=0,
            msg="All interface should be closed after turn_on_hardware_device() method is called and passed")
        for report_type in test_object.report_type_time_stamped_msg_queue:
            self.assertEqual(
                first=test_object.report_type_time_stamped_msg_queue[report_type].qsize(),
                second=0,
                msg=f"Queue for report type {report_type} was not cleared after turn_on_hardware_device()")
        # end for

        test_object.open()

        self._check_after_opening(test_object=test_object)
    # end def test_turn_on_hardware_device_business

    def test_turn_off_hardware_device_business(self):
        """
        Test turn_off_hardware_device method of a ``UsbChannel`` object
        """
        test_object = self._get_test_object()
        test_object.hardware_device = MockHardwareDevice()
        test_object.turn_on_hardware_device()
        test_object.open()
        test_object.turn_off_hardware_device()

        self.assertFalse(
            expr=test_object.hardware_device.is_on,
            msg="Hardware device should be closed after turn_off_hardware_device() method is called and passed")
        self.assertFalse(
            expr=test_object.is_open,
            msg="UsbChannel should be closed after turn_off_hardware_device() method is called and passed")
        self.assertEqual(
            first=len(test_object.report_type_to_interface), second=0, msg="Not all interface were closed")
        for report_type in test_object.report_type_time_stamped_msg_queue:
            self.assertEqual(
                first=test_object.report_type_time_stamped_msg_queue[report_type].qsize(),
                second=0,
                msg=f"Queue for report type {report_type} was not cleared after turn_on_hardware_device()")
        # end for
    # end def test_turn_off_hardware_device_business

    def test_send_data_business(self):
        """
        Test send_data method of a ``UsbChannel`` object
        """
        test_object = self._get_test_object()

        test_object.open()
        test_object.send_data(data=HexList([0]*HidppMessage.SHORT_MSG_SIZE))
    # end def test_send_data_business

    def test_get_message_business(self):
        """
        Test send_data method of a ``UsbChannel`` object
        """
        test_object = self._get_test_object()
        message_to_put = TransportMessage(data=HexList('10ff8100000000'))
        test_object.open()
        test_object.report_type_time_stamped_msg_queue[LogitechReportType.HIDPP].put(message_to_put)
        message_to_get = test_object.get_message()

        self.assertEqual(first=message_to_put,
                         second=message_to_get,
                         msg="Message received is not the expected one")
    # end def test_get_message_business

    def test_open_different_link_enabler(self):
        """
        Test open method of a ``UsbChannel`` object with different link enabler
        """
        test_object = self._get_test_object()

        for link_enabler, expected_length in [(LinkEnablerInfo.HID_PP_MASK, 1),
                                              (LinkEnablerInfo.HID_PP_MASK | LinkEnablerInfo.MOUSE_MASK, 2),
                                              (LinkEnablerInfo.HID_PP_MASK | LinkEnablerInfo.MOUSE_MASK |
                                               LinkEnablerInfo.KEYBOARD_MASK, 3), (LinkEnablerInfo.ALL_MASK, 4)]:
            test_object.open(link_enabler=link_enabler)

            self.assertTrue(
                expr=test_object.is_open, msg="UsbChannel should be open after open() method is called and passed")
            self.assertEqual(first=len(test_object.report_type_to_interface),
                             second=expected_length,
                             msg="Not all wanted interface were opened")

            test_object.close()
        # end for
    # end def test_open_different_link_enabler

    def test_open_different_interface_number(self):
        """
        Test open method of a ``UsbChannel`` object with different interface number
        """
        test_object = self._get_test_object()

        for protocol_list in [(LogitechReportType.HIDPP,),
                              (LogitechReportType.HIDPP, LogitechReportType.MOUSE),
                              (LogitechReportType.HIDPP, LogitechReportType.MOUSE, LogitechReportType.KEYBOARD),
                              (LogitechReportType.HIDPP, LogitechReportType.MOUSE, LogitechReportType.KEYBOARD,
                               LogitechReportType.DIGITIZER)]:
            self.usb_context_device.interface_list = []
            counter = 0
            for protocol in protocol_list:
                self.usb_context_device.interface_list.append(
                    (counter, protocol, [(counter | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]))
                counter += 1
            # end for

            test_object.open()

            self.assertTrue(
                expr=test_object.is_open, msg="UsbChannel should be open after open() method is called and passed")
            self.assertEqual(first=len(test_object.report_type_to_interface),
                             second=len(self.usb_context_device.interface_list),
                             msg="Not all wanted interface were opened")

            test_object.close()
        # end for
    # end def test_open_different_interface_number

    def test_send_data_different_data_size(self):
        """
        Test send_data method of a ``UsbChannel`` object with different data size
        """
        test_object = self._get_test_object()

        test_object.open()

        for data_size in HidppMessage.HIDPP_REPORT_LEN_LIST:
            test_object.send_data(data=HexList([0]*data_size))
        # end for
    # end def test_send_data_different_data_size

    def test_multiple_open(self):
        """
        Test multiple call of open method of a ``UsbChannel`` object
        """
        test_object = self._get_test_object()

        for _ in range(5):
            test_object.open()
        # end for

        self._check_after_opening(test_object=test_object)
    # end def test_multiple_open

    def test_multiple_close(self):
        """
        Test multiple call of close method of a ``UsbChannel`` object
        """
        test_object = self._get_test_object()

        test_object.open()

        for _ in range(5):
            test_object.close()
        # end for

        self._check_after_closing(test_object=test_object)
    # end def test_multiple_close

    def test_error_open_when_hardware_device_off(self):
        """
        Test open method of a ``UsbChannel`` object when the hardware device is off raise an exception
        """
        test_object = self._get_test_object()
        test_object.hardware_device = MockHardwareDevice()

        exception = None
        try:
            test_object.open()
        except ChannelException as e:
            exception = e
        # end try

        self.assertIsNotNone(obj=exception, msg="open() should not passed if the hardware device is off")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.HARDWARE_DEVICE_OFF,
                         msg="ChannelException cause should be HARDWARE_DEVICE_OFF")
    # end def test_error_open_when_hardware_device_off

    def test_send_data_error_channel_closed(self):
        """
        Test send_data method of a ``UsbChannel`` object when the channel is closed raise an exception
        """
        test_object = self._get_test_object()

        exception = self._send_data_with_exception(test_object=test_object)

        self.assertIsNotNone(obj=exception, msg="send_data() should not passed if the channel is closed")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.CHANNEL_NOT_OPEN,
                         msg="ChannelException cause should be CHANNEL_NOT_OPEN")
    # end def test_send_data_error_channel_closed

    def test_send_data_error_hidpp_link_disable(self):
        """
        Test send_data method of a ``UsbChannel`` object when the HID++ link is disabled
        """
        test_object = self._get_test_object()

        test_object.open(link_enabler=LinkEnablerInfo.MOUSE_MASK | LinkEnablerInfo.KEYBOARD_MASK)

        exception = self._send_data_with_exception(test_object=test_object)

        self.assertIsNotNone(obj=exception, msg="send_data() should not passed if the HID++ link is disabled")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                         msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
    # end def test_send_data_error_hidpp_link_disable

    def test_send_data_error_hidpp_interface_not_present(self):
        """
        Test send_data method of a ``UsbChannel`` object when the HID++ interface is not present
        """
        test_object = self._get_test_object()
        self.usb_context_device.interface_list = [
            (1, LogitechReportType.MOUSE, [(1 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
            (2, LogitechReportType.KEYBOARD, [(2 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)])]

        test_object.open()

        exception = self._send_data_with_exception(test_object=test_object)

        self.assertIsNotNone(obj=exception, msg="send_data() should not passed if the HID++ interface is not present")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                         msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
    # end def test_send_data_error_hidpp_interface_not_present

    def test_send_data_error_wrong_data_size(self):
        """
        Test send_data method of a ``UsbChannel`` object when the data size is wrong
        """
        test_object = self._get_test_object()

        test_object.open()

        for report_id in HidppMessage.HIDPP_REPORT_ID_LIST:
            for data_size in compute_wrong_range(HidppMessage.HIDPP_REPORT_LEN_LIST):
                exception = None
                data = HexList("00" * data_size)
                if len(data) > 0:
                    data[0] = report_id
                # end if
                try:
                    test_object.send_data(data=data)
                except ChannelException as e:
                    exception = e
                # end try

                self.assertIsNotNone(
                    obj=exception,
                    msg=f"send_data() should not passed if the data size is wrong (data_size={data_size})")
                self.assertEqual(first=exception.get_cause(),
                                 second=ChannelException.Cause.WRONG_PARAMETER,
                                 msg=f"ChannelException cause should be WRONG_PARAMETER (data_size={data_size})")
            # end for
        # end for
    # end def test_send_data_error_wrong_data_size

    def test_send_data_error_wrong_data_size_sent(self):
        """
        Test send_data method of a ``UsbChannel`` object when the data size is wrong
        """
        for difference_bytes_sent in compute_wrong_range(
                0, min_value=-int(HidppMessage.SHORT_MSG_SIZE/2), max_value=int(HidppMessage.SHORT_MSG_SIZE/2)):
            test_object = self._get_test_object(usb_context=MockUsbContext(difference_bytes_sent=difference_bytes_sent))

            test_object.open()
            exception = UsbChannelTestCase._send_data_with_exception(test_object=test_object)

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
        Test get_message method of a ``UsbChannel`` object when the channel is closed raise an exception
        """
        test_object = self._get_test_object()

        exception = self._get_message_with_exception(test_object=test_object)

        self.assertIsNotNone(obj=exception, msg="get_message() should not passed if the channel is closed")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.CHANNEL_NOT_OPEN,
                         msg="ChannelException cause should be CHANNEL_NOT_OPEN")
    # end def test_get_message_error_channel_closed

    def test_get_message_error_hidpp_interface_not_present(self):
        """
        Test get_message method of a ``UsbChannel`` object when the HID++ interface is not present
        """
        test_object = self._get_test_object()
        self.usb_context_device.interface_list = [
            (1, LogitechReportType.MOUSE, [(1 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
            (2, LogitechReportType.KEYBOARD, [(2 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)])]

        test_object.open()

        exception = UsbChannelTestCase._get_message_with_exception(test_object=test_object)

        self.assertIsNotNone(obj=exception, msg="get_message() should not passed if the HID++ interface is not present")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                         msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
    # end def test_get_message_error_hidpp_interface_not_present

    def test_get_message_error_mouse_interface_not_present(self):
        """
        Test get_message method of a ``UsbChannel`` object when the Mouse interface is not present
        """
        test_object = self._get_test_object()
        self.usb_context_device.interface_list = [
            (0, LogitechReportType.HIDPP, [(0 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
            (2, LogitechReportType.KEYBOARD, [(2 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)])]

        test_object.open()

        exception = UsbChannelTestCase._get_message_with_exception(
            test_object=test_object, report_type=LogitechReportType.MOUSE)

        self.assertIsNotNone(obj=exception, msg="get_message() should not passed if the Mouse interface is not present")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                         msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
    # end def test_get_message_error_mouse_interface_not_present

    def test_get_message_error_keyboard_interface_not_present(self):
        """
        Test get_message method of a ``UsbChannel`` object when the Keyboard interface is not present
        """
        test_object = self._get_test_object()
        self.usb_context_device.interface_list = [
            (0, LogitechReportType.HIDPP, [(0 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)]),
            (1, LogitechReportType.MOUSE, [(1 | EndpointDirection.IN, INTERRUPT_DATA_SIZE)])]

        test_object.open()

        exception = UsbChannelTestCase._get_message_with_exception(
            test_object=test_object, report_type=LogitechReportType.KEYBOARD)

        self.assertIsNotNone(
            obj=exception, msg="get_message() should not passed if the Keyboard interface is not present")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                         msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
    # end def test_get_message_error_keyboard_interface_not_present

    def test_get_message_error_hidpp_link_disable(self):
        """
        Test get_message method of a ``UsbChannel`` object when the HID++ link is disable
        """
        test_object = self._get_test_object()

        test_object.open(link_enabler=LinkEnablerInfo.MOUSE_MASK | LinkEnablerInfo.KEYBOARD_MASK)

        exception = UsbChannelTestCase._get_message_with_exception(test_object=test_object)

        self.assertIsNotNone(obj=exception, msg="get_message() should not passed if the HID++ link is disable")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                         msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
    # end def test_get_message_error_hidpp_link_disable

    def test_get_message_error_mouse_link_disable(self):
        """
        Test get_message method of a ``UsbChannel`` object when the Mouse link is disable
        """
        test_object = self._get_test_object()

        test_object.open(link_enabler=LinkEnablerInfo.HID_PP_MASK | LinkEnablerInfo.KEYBOARD_MASK)

        exception = UsbChannelTestCase._get_message_with_exception(
            test_object=test_object, report_type=LogitechReportType.MOUSE)

        self.assertIsNotNone(obj=exception, msg="get_message() should not passed if the Mouse link is disable")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                         msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
    # end def test_get_message_error_mouse_link_disable

    def test_get_message_error_keyboard_link_disable(self):
        """
        Test get_message method of a ``UsbChannel`` object when the Keyboard link is disable
        """
        test_object = self._get_test_object()

        test_object.open(link_enabler=LinkEnablerInfo.HID_PP_MASK | LinkEnablerInfo.MOUSE_MASK)

        exception = UsbChannelTestCase._get_message_with_exception(
            test_object=test_object, report_type=LogitechReportType.KEYBOARD)

        self.assertIsNotNone(obj=exception, msg="get_message() should not passed if the Keyboard link is disable")
        self.assertEqual(first=exception.get_cause(),
                         second=ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                         msg="ChannelException cause should be EXPECTED_LINK_NOT_PRESENT")
    # end def test_get_message_error_keyboard_link_disable

    def _get_test_object(self,
                         usb_context=MockUsbContext(),
                         trace_level_to_use=TraceLevel.WARNING,
                         trace_file_name_to_use=None,
                         **kwargs):
        """
        Get the test object. It is in its own method to be used in inheriting class.

        :param usb_context: USB context to use for this channel - OPTIONAL
        :type usb_context: ``UsbContext``
        :param trace_level_to_use: Trace level of the channel - OPTIONAL
        :type trace_level_to_use: ``TraceLevel`` or ``int``
        :param trace_file_name_to_use: Trace output of the channel - OPTIONAL
        :type trace_file_name_to_use: ``str`` or ``None``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: The test object
        :rtype: ``UsbChannel``
        """
        return UsbChannel(usb_context=usb_context,
                          usb_context_device=self.usb_context_device,
                          trace_level=trace_level_to_use,
                          trace_file_name=trace_file_name_to_use)
    # end def _get_test_object

    def _check_after_creation(self, test_object, trace_level_to_use):
        """
        Check test object after creation.

        :param test_object: Test object to check
        :type test_object: ``UsbChannel``
        :param trace_level_to_use: Trace level of the channel
        :type trace_level_to_use: ``TraceLevel`` or ``int``
        """
        self.assertFalse(expr=test_object.is_open, msg="UsbChannel should be closed after creation")

        trace_name = TRACE_LOGGER.get_trace_name(subscription_owner=test_object)
        self.assertIn(member=self.usb_context_device.get_basic_reader_name(),
                      container=trace_name,
                      msg="The reader_name parameter should appear in the trace name")
        self.assertIn(member=f"{self.usb_context_device.vid:04X}",
                      container=trace_name,
                      msg="The vid parameter should appear in the trace name")
        self.assertIn(member=f"{self.usb_context_device.pid:04X}",
                      container=trace_name,
                      msg="The pid parameter should appear in the trace name")

        trace_output = TRACE_LOGGER.get_trace_output(subscription_owner=test_object)
        self.assertEqual(first=trace_output, second=sys.stdout, msg="The trace output is not the expected one")

        trace_level = TRACE_LOGGER.get_trace_level(subscription_owner=test_object)
        self.assertEqual(
            first=trace_level, second=trace_level_to_use, msg="The trace level is not the expected one")
    # end def _check_after_creation

    def _check_after_opening(self, test_object):
        """
        Check test object after opening.

        :param test_object: Test object to check
        :type test_object: ``UsbChannel``
        """
        self.assertTrue(
            expr=test_object.is_open, msg="UsbChannel should be open after open() method is called and passed")
        self.assertEqual(first=len(test_object.report_type_to_interface),
                         second=len(self.usb_context_device.interface_list),
                         msg="Not all wanted interface were opened")
        self.assertEqual(first=len(test_object.report_type_time_stamped_msg_queue),
                         second=len(self.usb_context_device.interface_list),
                         msg="Not all wanted queues were created")
    # end def _check_after_opening

    def _check_after_closing(self, test_object):
        """
        Check test object after opening.

        :param test_object: Test object to check
        :type test_object: ``UsbChannel``
        """
        self.assertFalse(
            expr=test_object.is_open, msg="UsbChannel should be closed after close() method is called and passed")
        self.assertEqual(
            first=len(test_object.report_type_to_interface), second=0, msg="Not all interface were closed")
        for report_type in test_object.report_type_time_stamped_msg_queue:
            self.assertEqual(
                first=test_object.report_type_time_stamped_msg_queue[report_type].qsize(),
                second=0,
                msg=f"Queue for report type {report_type} was not cleared")
        # end for
    # end def _check_after_closing

    @staticmethod
    def _send_data_with_exception(test_object, data_size=HidppMessage.SHORT_MSG_SIZE):
        """
        Call send_data and catch ChannelException if any.

        :param test_object: USB channel under test
        :type test_object: ``UsbChannel``
        :param data_size: Data size to send - OPTIONAL
        :type data_size: ``int``

        :return: Caught exception if any
        :rtype: ``ChannelException`` or ``None``
        """
        try:
            test_object.send_data(data=HexList([0]*data_size))
        except ChannelException as e:
            return e
        # end try
        return None
    # end def _send_data_with_exception

    @staticmethod
    def _get_message_with_exception(test_object, report_type=LogitechReportType.HIDPP):
        """
        Call get_message and catch ChannelException if any.

        :param test_object: USB channel under test
        :type test_object: ``UsbChannel``
        :param report_type: The report type of message to get - OPTIONAL
        :type report_type: ``LogitechReportType``

        :return: Caught exception if any
        :rtype: ``ChannelException`` or ``None``
        """
        try:
            test_object.get_message(report_type=report_type, timeout=.01)
        except ChannelException as e:
            return e
        # end try
        return None
    # end def _get_message_with_exception
# end class UsbChannelTestCase


class UsbReceiverChannelTestCase(UsbChannelTestCase):
    """
    Test ``UsbReceiverChannel`` Class
    """
    def test_enable_hidpp_reporting_business(self):
        """
        Test enable_hidpp_reporting method of a ``UsbReceiverChannel`` object
        """
        self._enable_hidpp_reporting_test()
    # end def test_enable_hidpp_reporting_business

    def test_perform_fake_arrival_business(self):
        """
        Test perform_fake_arrival method of a ``UsbReceiverChannel`` object
        """
        list_message_to_receive = [
            TransportMessage(data=HexList(GetEnableHidppReportingResponse(
                receiver_reporting_flag_wireless_notifications=True))),
            TransportMessage(data=HexList(SetConnectionStateResponse()))]
        test_object = self._get_test_object(usb_context=MockUsbContext(list_message_to_receive=list_message_to_receive))
        test_object.open()

        test_object.perform_fake_arrival()

        self.assertEqual(first=len(list_message_to_receive),
                         second=0,
                         msg="The number of response left in the list is not the expected one")
    # end def test_perform_fake_arrival_business

    def test_enable_hidpp_reporting_enable_true_flag_true(self):
        """
        Test enable_hidpp_reporting method of a ``UsbReceiverChannel`` object with enable = True and flag = True
        """
        self._enable_hidpp_reporting_test(enable=True, flag=True, response_left=1)
    # end def test_enable_hidpp_reporting_enable_true_flag_true

    def test_enable_hidpp_reporting_enable_false_flag_true(self):
        """
        Test enable_hidpp_reporting method of a ``UsbReceiverChannel`` object with enable = False and flag = True
        """
        self._enable_hidpp_reporting_test(enable=False, flag=True, response_left=0)
    # end def test_enable_hidpp_reporting_enable_false_flag_true

    def test_enable_hidpp_reporting_enable_false_flag_false(self):
        """
        Test enable_hidpp_reporting method of a ``UsbReceiverChannel`` object with enable = False and flag = False
        """
        self._enable_hidpp_reporting_test(enable=False, flag=False, response_left=1)
    # end def test_enable_hidpp_reporting_enable_false_flag_false

    def test_creation_max_number_of_paired_devices_robustness(self):
        """
        Test creation of a ``UsbReceiverChannel`` object with different valid values of ``max_number_of_paired_devices``
        """
        trace_level_to_use = TraceLevel.WARNING
        trace_file_name_to_use = None

        for max_number_of_paired_devices in range(1, 7):
            test_object = UsbReceiverChannel(max_number_of_paired_devices=max_number_of_paired_devices,
                                             usb_context=MockUsbContext(),
                                             usb_context_device=self.usb_context_device,
                                             trace_level=trace_level_to_use,
                                             trace_file_name=trace_file_name_to_use)
            self._check_after_creation(test_object=test_object, trace_level_to_use=trace_level_to_use)
        # end for
    # end def test_creation_max_number_of_paired_devices_robustness

    def test_creation_max_number_of_paired_devices_error(self):
        """
        Test creation of a ``UsbReceiverChannel`` object with different wrong values of ``max_number_of_paired_devices``
        """
        trace_level_to_use = TraceLevel.WARNING
        trace_file_name_to_use = None

        for max_number_of_paired_devices in compute_inf_values(value=1):
            exception = None
            try:
                UsbReceiverChannel(max_number_of_paired_devices=max_number_of_paired_devices,
                                   usb_context=MockUsbContext(),
                                   usb_context_device=self.usb_context_device,
                                   trace_level=trace_level_to_use,
                                   trace_file_name=trace_file_name_to_use)
            except ChannelException as e:
                exception = e
            # end try

            self.assertIsNotNone(
                obj=exception,
                msg=f"Creation of UsbReceiverChannel should not passed if the max number of paired device is wrong "
                    f"(max_number_of_paired_devices={max_number_of_paired_devices})")
            self.assertEqual(
                first=exception.get_cause(),
                second=ChannelException.Cause.WRONG_PARAMETER,
                msg=f"ChannelException cause should be WRONG_PARAMETER "
                    f"(difference_bytes_sent={max_number_of_paired_devices})")
        # end for
    # end def test_creation_max_number_of_paired_devices_error

    def _get_test_object(self,
                         max_number_of_paired_devices=6,
                         usb_context=MockUsbContext(),
                         trace_level_to_use=TraceLevel.WARNING,
                         trace_file_name_to_use=None,
                         **kwargs):
        """
        Get the test object. It is in its own method to be used in inheriting class.

        :param max_number_of_paired_devices: Maximum number of device paired to this receiver - OPTIONAL
        :type max_number_of_paired_devices: ``int``
        :param usb_context: USB context to use for this channel - OPTIONAL
        :type usb_context: ``UsbContext``
        :param trace_level_to_use: Trace level of the channel - OPTIONAL
        :type trace_level_to_use: ``TraceLevel`` or ``int``
        :param trace_file_name_to_use: Trace output of the channel - OPTIONAL
        :type trace_file_name_to_use: ``str`` or ``None``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: The test object
        :rtype: ``UsbReceiverChannel``
        """
        return UsbReceiverChannel(max_number_of_paired_devices=max_number_of_paired_devices,
                                  usb_context=usb_context,
                                  usb_context_device=self.usb_context_device,
                                  trace_level=trace_level_to_use,
                                  trace_file_name=trace_file_name_to_use)
    # end def _get_test_object

    def _enable_hidpp_reporting_test(self, enable=True, flag=False, response_left=0):
        """
        Perform a ``enable_hidpp_reporting`` with different parameters and check the right number of response left.

        :param enable: ``enable`` parameter for ``enable_hidpp_reporting``
        :param flag: ``receiver_reporting_flag_wireless_notifications`` parameter for
                     ``GetEnableHidppReportingResponse``
        """
        first_message = GetEnableHidppReportingResponse(receiver_reporting_flag_wireless_notifications=flag)
        second_message = SetEnableHidppReportingResponse()
        list_message_to_receive = [TransportMessage(data=HexList(first_message)),
                                   TransportMessage(data=HexList(second_message))]
        test_object = self._get_test_object(usb_context=MockUsbContext(list_message_to_receive=list_message_to_receive))
        test_object.open()

        test_object.enable_hidpp_reporting(enable=enable)

        self.assertEqual(first=len(list_message_to_receive),
                         second=response_left,
                         msg="The number of response left in the list is not the expected one")
    # end def _enable_hidpp_reporting_test
# end class UsbReceiverChannelTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
