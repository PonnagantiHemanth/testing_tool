#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.base.bleppserviceutils
:brief:  Helpers for BLE++ service (applicable to device targets only)
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/09/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.blechannel import HidReportId
from pychannel.logiconstants import LogitechBleConstants
from pychannel.logiconstants import LogitechVendorUuid
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import QueueWithFilter
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.blemessage import BleMessage


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleppServiceUtils(DeviceBaseTestUtils):
    """
    Test utils for BLE++ service (applicable to device targets only)
    """

    @staticmethod
    def get_blepp_service(test_case):
        """
        Retrieve the BLE++ service.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``
        """
        blepp_service = None
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg='Retrieve the BLE++ service')
        # --------------------------------------------------------------------------------------------------------------
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=test_case)
        for service in ble_context.get_gatt_table(ble_context_device=test_case.ble_context_device_used):
            if service.uuid == BleUuid.from_array(uuid_array=LogitechVendorUuid.APPLICATION_SERVICE):
                blepp_service = service
                break
            # end if
        # end for
        return blepp_service
    # end def get_blepp_service

    @classmethod
    def get_blepp_characteristic(cls, test_case):
        """
        Retrieve the BLE++ characteristic.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg='Retrieve the BLE++ characteristic')
        # --------------------------------------------------------------------------------------------------------------
        blepp_service = cls.get_blepp_service(test_case=test_case)
        blepp_characteristic = blepp_service.get_characteristics(
            characteristic_uuid=BleUuid.from_array(uuid_array=LogitechVendorUuid.APPLICATION_CHARACTERISTIC))[0]
        return blepp_characteristic
    # end def get_blepp_characteristic

    @classmethod
    def configure_blepp_cccds(cls, test_case, enabled=True):
        """
        Enable / disable the BLE++ characteristic CCCD.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``
        :param enabled: Flag indicating the required cccd state.
        :type enabled: ``bool``
        """
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=test_case)
        if enabled:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=test_case, text='Enable CCCD on BLE++ service')
            # --------------------------------------------------------------------------------------------------------------
            ble_context.enable_notification(
                ble_context_device=test_case.ble_context_device_used,
                characteristic=cls.get_blepp_characteristic(test_case=test_case),
                time_stamped_queue=cls.get_blepp_time_stamped_msg_queue(test_case=test_case))
        else:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=test_case, text='Disable CCCD on BLE++ service')
            # --------------------------------------------------------------------------------------------------------------
            ble_context.disable_notification(
                ble_context_device=test_case.ble_context_device_used,
                characteristic=cls.get_blepp_characteristic(test_case=test_case))
        # end if
    # end def configure_blepp_cccds

    @staticmethod
    def get_blepp_time_stamped_msg_queue(test_case):
        """
        Create a message queue to store the response and notification received on the BLE++ characteristic

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``

        :return: Timestamped message queue
        :rtype: ``QueueWithFilter``
        """
        if not hasattr(test_case, 'blepp_time_stamped_msg_queue') or \
                getattr(test_case, 'blepp_time_stamped_msg_queue') is None:
            test_case.blepp_time_stamped_msg_queue = QueueWithFilter()
        # end if
        return getattr(test_case, 'blepp_time_stamped_msg_queue')
    # end def get_blepp_time_stamped_msg_queue

    @classmethod
    def get_blepp_notification(cls, test_case):
        """Wait for a BLE++ notification

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``

        :return: The first message received on this characteristic
        :rtype: ``BleMessage``
        """
        return cls.get_blepp_time_stamped_msg_queue(test_case=test_case).get(
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
    # end def get_blepp_notification

    @classmethod
    def read_blepp_characteristic(cls, test_case):
        """
        Read the BLE++ characteristic and optionally returned the BLE message

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``

        :return: The first message received on this characteristic
        :rtype: ``BleMessage``
        """
        ble_message = None
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=test_case)
        while ble_message in [None, BleMessage(data=HexList("00"*18))]:
            ble_message = ble_context.attribute_read(ble_context_device=test_case.ble_context_device_used,
                                                     attribute=cls.get_blepp_characteristic(test_case=test_case))
        # end while

        if not cls.get_blepp_time_stamped_msg_queue(test_case=test_case).empty():
            ble_message_from_queue = cls.get_blepp_time_stamped_msg_queue(test_case=test_case).get()
            assert ble_message == ble_message_from_queue
        # end if
        return ble_message
    # end def read_blepp_characteristic

    @staticmethod
    def convert_blepp_to_hidpp_message(ble_message, current_channel):
        """
        Convert the BLE message into ``HidppMessage``

        :param ble_message: A message received on the BLE++ characteristic
        :type ble_message: ``BleMessage``
        :param current_channel: The active channel
        :type current_channel: ``BaseCommunicationChannel``

        :return: The HID++ message
        :rtype: ``HidppMessage``
        """
        if len(ble_message.data) == LogitechBleConstants.BLEPP_MESSAGE_SIZE:
            ble_message.data = HexList(Hidpp1Data.DeviceIndex.TRANSCEIVER) + ble_message.data
        # end if
        ble_message.data = HexList(HidReportId.LONG_HID_PP) + ble_message.data
        return current_channel.hid_dispatcher.get_response_message(transport_message=ble_message)
    # end def convert_blepp_to_hidpp_message

    @staticmethod
    def convert_hidpp_to_blepp_message(hidpp_message):
        """
        Convert a ``HidppMessage`` into BLE message, the first two bytes are deleted as they are considered useless in BLE

        :param hidpp_message: A HID++ response or notification
        :type hidpp_message: ``HidppMessage``

        :return: The BLE++ message
        :rtype: ``BleppMessage``
        """
        assert isinstance(hidpp_message, HidppMessage)
        message = HexList(hidpp_message)[2:]
        message.addPadding(size=LogitechBleConstants.BLEPP_MESSAGE_SIZE, fromLeft=False)
        return BleMessage(data=message)
    # end def convert_hidpp_to_blepp_message

    @classmethod
    def write_blepp_characteristic(cls, test_case, hidpp_message):
        """
        Write a request into the BLE++ characteristic and optionally returned the BLE message

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``
        :param hidpp_message: An HID++ 2.0 message
        :type hidpp_message: ``HidppMessage``

        :return: The first message received on this characteristic
        :rtype: ``BleMessage``
        """
        message = HexList(hidpp_message)[2:]
        message.addPadding(size=LogitechBleConstants.BLEPP_MESSAGE_SIZE, fromLeft=False)
        ble_message = BleMessage(data=message)

        ble_context = BleProtocolTestUtils.get_ble_context(test_case=test_case)
        ble_context.characteristic_write(ble_context_device=test_case.ble_context_device_used,
                                         characteristic=cls.get_blepp_characteristic(test_case=test_case),
                                         data=ble_message)
        return cls.get_blepp_time_stamped_msg_queue(test_case=test_case).get(
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
    # end def write_blepp_characteristic

    @staticmethod
    def extract_feature_index_from_blepp_notification(ble_notification):
        """
        Extract the feature index from a blepp notification
        
        :param ble_notification: the notification to extract it from
        :type ble_notification: ``BleMessage``
        
        :return: the corresponding feature index
        :rtype: ``int``
        """
        if len(ble_notification.data) == LogitechBleConstants.BLEPP_MESSAGE_SIZE:
            ble_notification.data = HexList(Hidpp1Data.DeviceIndex.TRANSCEIVER) + ble_notification.data
        # end if
        ble_notification.data = HexList(HidReportId.LONG_HID_PP) + ble_notification.data
        feature_index = ble_notification.data[HidppMessage.OFFSET.FEATURE_INDEX]
        return feature_index
    # end def extract_feature_index_from_blepp_notification

# end class BleppServiceUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
