#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.base.channelutils
:brief: Help for Channel actions and information
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/11/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from contextlib import contextmanager
from queue import Empty
from time import perf_counter_ns
from time import time

from pychannel.blechannel import BleChannel
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import ChannelException
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.channelinterfaceclasses import LogitechReportType
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import WarningLevel
from pyhid.bitfieldcontainermixin import TimestampedBitFieldContainerMixin
from pyhid.hid.interfacedescriptors import ReportDescriptor
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.features.root import RootModel
from pyhid.hidpp.features.root import RootFactory
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import GetEnableHidppReportingRequest
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import GetEnableHidppReportingResponse
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import SetEnableHidppReportingRequest
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import SetEnableHidppReportingResponse
from pyhid.vlp.features.important.vlproot import VLPRoot
from pyhid.vlp.features.important.vlproot import VLPRootModel
from pyhid.vlp.features.important.vlproot import VLPRootFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.loghelper import LogHelper
from pyusb.libusbdriver import ChannelIdentifier
from pyusb.libusbdriver import LibusbDriver


# ------------------------------------------------------------------------------
# Features implementation
# ------------------------------------------------------------------------------
class ChannelUtils:
    """
    This class provides helpers for channel actions and information
    """
    TIME_STEP_GET_MESSAGE_IN_MULTIPLE_TIME_STAMPED_QUEUE = 0.005
    LOGGING_THRESHOLD = 1.5 * 10 ** 3
    GENERIC_MAX_RETRY_COUNT = 2
    ROOT_CIRCULAR_SOFTWARE_ID_MIN_VALUE = 1
    ROOT_CIRCULAR_SOFTWARE_ID_MAX_VALUE = 14
    ROOT_CIRCULAR_SOFTWARE_ID_MAX_ROTATION = ROOT_CIRCULAR_SOFTWARE_ID_MAX_VALUE - ROOT_CIRCULAR_SOFTWARE_ID_MIN_VALUE
    ROOT_CIRCULAR_SOFTWARE_ID = ROOT_CIRCULAR_SOFTWARE_ID_MIN_VALUE
    GENERIC_RESET_TIMEOUT = 15  # in seconds
    WAIT_CONNECTION_STATE_PERIOD = 0.1  # in seconds
    UPDATE_FEATURE_MAPPING_RETRY_COUNTER = 3

    @staticmethod
    @contextmanager
    def channel_open_state(test_case, channel=None, open_state_required=True, link_enabler=LinkEnablerInfo.ALL_MASK,
                           open_associated_channel=True, close_associated_channel=True):
        """
        Open a channel (if needed) for a section and close it after if it was opened by this method.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param open_state_required: Flag indicating the open state of the channel. `True`` (default) means it should
                                    be opened inside the "with", ``False`` means closed - OPTIONAL
        :type open_state_required: ``bool``
        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo`` - OPTIONAL
        :type link_enabler: ``int`` or ``BitStruct``
        :param open_associated_channel: Flag indicating to open the associated (receiver) channel before opening the
                                        wanted one - OPTIONAL
        :type open_associated_channel: ``bool``
        :param close_associated_channel: Flag indicating to close the associated (receiver) channel after closing the
                                         wanted one - OPTIONAL
        :type close_associated_channel: ``bool``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        close_channel_after = False
        open_channel_after = False
        if open_state_required and not channel.is_open:
            ChannelUtils.open_channel(test_case=test_case, channel=channel, link_enabler=link_enabler,
                                      open_associated_channel=open_associated_channel)
            close_channel_after = True
        elif not open_state_required and channel.is_open:
            ChannelUtils.close_channel(test_case=test_case, channel=channel,
                                       close_associated_channel=close_associated_channel)
            open_channel_after = True
        # end if

        try:
            yield
        finally:
            if close_channel_after:
                ChannelUtils.close_channel(test_case=test_case, channel=channel,
                                           close_associated_channel=close_associated_channel)
            elif open_channel_after:
                ChannelUtils.open_channel(test_case=test_case, channel=channel, link_enabler=link_enabler,
                                          open_associated_channel=open_associated_channel)
            # end if
        # end try
    # end def channel_open_state

    @staticmethod
    def open_channel(test_case, channel=None, link_enabler=LinkEnablerInfo.ALL_MASK, open_associated_channel=True):
        """
        Open a channel. If the channel is through a receiver channel and ``open_associated_channel`` is ``True``, it
        automatically opens the receiver channel (if not already open).

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo`` - OPTIONAL
        :type link_enabler: ``int`` or ``BitStruct``
        :param open_associated_channel: Flag indicating to open the associated (receiver) channel before opening the
                                        wanted one - OPTIONAL
        :type open_associated_channel: ``bool``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        if isinstance(channel, ThroughReceiverChannel) and \
                not channel.receiver_channel.is_open and \
                open_associated_channel:
            # open associated receiver channel
            channel.receiver_channel.open(link_enabler=link_enabler)

            LogHelper.log_trace(
                test_case=test_case, msg=f"Associated receiver channel {channel.receiver_channel} open")
        elif isinstance(channel, BleChannel) and not channel.is_device_connected(force_refresh_cache=True):
            # The device should be wakened up before trying to connect to it
            test_case.wake_up_device_with_user_action()
        # end if

        channel.open(link_enabler=link_enabler)

        LogHelper.log_trace(test_case=test_case, msg=f"Channel {channel} open")
    # end def open_channel

    @staticmethod
    def close_channel(test_case, channel=None, close_associated_channel=True):
        """
        Close a channel. If the channel is through a receiver channel and ``close_associated_channel`` is ``True``, it
        automatically closes the receiver channel (if not already closed).

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param close_associated_channel: Flag indicating to close the associated (receiver) channel after closing the
                                         wanted one - OPTIONAL
        :type close_associated_channel: ``bool``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        channel.close()

        LogHelper.log_trace(test_case=test_case, msg=f"Channel {channel} closed")

        if isinstance(channel, ThroughReceiverChannel) and \
                channel.receiver_channel.is_open and \
                close_associated_channel:
            channel.receiver_channel.close()

            LogHelper.log_trace(
                test_case=test_case, msg=f"Associated receiver channel {channel.receiver_channel} closed")
        # end if
    # end def close_channel

    @staticmethod
    def get_receiver_channel(test_case, channel=None):
        """
        Get the receiver channel associated to a channel. If the channel given is already a receiver channel, this
        method will return it back.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: Channel to get the receiver channel from
        :type channel: ``ThroughReceiverChannel`` or ``UsbReceiverChannel``

        :return: The receiver channel
        :rtype: ``UsbReceiverChannel``
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        if isinstance(test_case.current_channel, ThroughReceiverChannel):
            channel_receiver = test_case.current_channel.receiver_channel
        elif isinstance(test_case.current_channel, UsbReceiverChannel):
            channel_receiver = test_case.current_channel
        else:
            assert False, f"Unknown device channel type: current_channel = {test_case.current_channel}"
        # end if

        return channel_receiver
    # end def get_receiver_channel

    @staticmethod
    def set_idle(test_case, channel=None, idle_duration=0x00, interface_id=None):
        """
        The Set_Idle request silences a particular report on the Interrupt In pipe until a
        new event occurs or the specified amount of time passes.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``UsbChannel`` or ``ThroughReceiverChannel`` or ``None``
        :param idle_duration: Maximum amount of time between reports. 0 (zero): the duration is indefinite - OPTIONAL
        :type idle_duration: ``int``
        :param interface_id: Index of the interface that shall receive this request. If ``None``, the keyboard interface
                             is used - OPTIONAL
        :type interface_id: ``int`` or ``None``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        assert isinstance(channel, (UsbChannel, ThroughReceiverChannel)), \
            f"Channel should be a UsbChannel or a ThroughReceiverChannel, current channel = {channel}"

        if isinstance(channel, UsbChannel):
            channel_to_use = channel
        else:
            channel_to_use = channel.receiver_channel
        # end if

        interface_id = interface_id if interface_id is not None \
            else channel_to_use.report_type_to_interface.get(LogitechReportType.KEYBOARD, None)

        if interface_id is None:
            # The required interface is not available
            return
        # end if

        channel_to_use.hid_class_specific_request(interface_id=interface_id, w_value=idle_duration << 8)

        LogHelper.log_trace(
            test_case=test_case,
            msg=f"[{channel}] Set idle with idle duration = {idle_duration} on interface id = {interface_id}")
    # def set_idle

    @staticmethod
    def get_transport_id(test_case, channel=None, force_refresh_cache=False):
        """
        Get the transport ID of a given channel.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param force_refresh_cache: Flag indicating if the channel cache should be refreshed - OPTIONAL
        :type force_refresh_cache: ``bool``

        :return: The channel transport ID
        :rtype: ``int``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        return channel.get_transport_id(force_refresh_cache=force_refresh_cache)
    # end def get_transport_id

    @staticmethod
    def get_port_index(test_case, channel=None):
        """
        Get the port index of a given channel. The value ``0`` is for a USB channel which is not on a hub and
        ``-1`` is for BLE channel.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: The channel port index
        :rtype: ``int``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        :raise ``TypeError``: If the channel type is unknown
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        if isinstance(channel, (UsbChannel, ThroughReceiverChannel)):
            if LibusbDriver.is_usb_channel_on_hub(channel=channel):
                return channel.get_channel_usb_port_path_list()[-1]
            else:
                return LibusbDriver.NON_HUB_USB_PORT_INDEX
            # end if
        elif isinstance(channel, BleChannel):
            return LibusbDriver.BLE_PORT_INDEX
        # end if

        raise TypeError("Cannot get the port index if the channel is not the right type. It should be None "
                        "or one of the channel types (UsbChannel, BleChannel, ThroughReceiverChannel), it is "
                        f"{type(channel)}")
    # end def get_port_index

    @staticmethod
    def get_device_index(test_case, channel=None):
        """
        Get the device index of a given channel. The value ``0xFF`` is both for BLE and USB channels.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: The channel device index
        :rtype: ``int``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        :raise ``TypeError``: If the channel type is unknown
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        if isinstance(channel, (UsbChannel, BleChannel)):
            return Hidpp1Data.DeviceIndex.TRANSCEIVER
        elif isinstance(channel, ThroughReceiverChannel):
            return channel.device_index
        # end if

        raise TypeError("Cannot get the device index if the channel is not the right type. It should be None "
                        "or one of the channel types (UsbChannel, BleChannel, ThroughReceiverChannel), it is "
                        f"{type(channel)}")
    # end def get_device_index

    @classmethod
    def get_channel_identifier(cls, test_case, channel=None):
        """
        Get a channel ID corresponding to the given channel.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: The channel ID constructed with the channel
        :rtype: ``ChannelIdentifier``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        :raise ``TypeError``: If the channel type is unknown
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        transport_id = f"{channel.get_transport_id():04X}"
        if isinstance(channel, BleChannel):
            vid = None
            pid = None
            port_index = None
            device_index = None
        elif isinstance(channel, ThroughReceiverChannel):
            vid = f"{channel.receiver_channel.get_usb_vid():04X}"
            pid = f"{channel.receiver_channel.get_usb_pid():04X}"
            port_index = cls.get_port_index(test_case=test_case, channel=channel)
            device_index = cls.get_device_index(test_case=test_case, channel=channel)
        elif isinstance(channel, UsbChannel):
            vid = f"{channel.get_usb_vid():04X}"
            pid = f"{channel.get_usb_pid():04X}"
            port_index = cls.get_port_index(test_case=test_case, channel=channel)
            device_index = None
        else:
            raise TypeError("Cannot get the channel identifier if the channel is not the right type. It should be one "
                            "of the channel types (UsbChannel, BleChannel, ThroughReceiverChannel), it is "
                            f"{type(channel)}")
        # end if

        return ChannelIdentifier(
            port_index=port_index,
            device_index=device_index,
            transport_id=transport_id,
            protocol=channel.protocol,
            vendor_id=vid,
            product_id=pid)
    # end def get_channel_identifier

    @classmethod
    def set_hidpp_reporting(cls, test_case, channel=None, enable=True, force_send_unknown_channel_type=False):
        """
        Enable/disable the HID++ reporting flag of a receiver.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param enable: Flag to enable(default)/disable the HID++ reporting - OPTIONAL
        :type enable: ``bool``
        :param force_send_unknown_channel_type: Flag to send the exchange even if the channel is neither a
                                                ``UsbReceiverChannel`` nor a ``ThroughReceiverChannel`` - OPTIONAL
        :type force_send_unknown_channel_type: ``bool``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        if isinstance(channel, UsbReceiverChannel):
            LogHelper.log_trace(test_case=test_case, msg=f"[{channel}] Sending set HID++ reporting to {enable}")
            channel.enable_hidpp_reporting(enable=enable)
        elif isinstance(channel, ThroughReceiverChannel):
            LogHelper.log_trace(test_case=test_case, msg=f"[{channel}] Sending set HID++ reporting to {enable}")
            channel.receiver_channel.enable_hidpp_reporting(enable=enable)
        elif force_send_unknown_channel_type:
            get_register = GetEnableHidppReportingRequest()
            get_register_response = cls.send(
                test_case=test_case,
                report=get_register,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=GetEnableHidppReportingResponse,
                channel=channel)

            if int(enable) != get_register_response.receiver_reporting_flag_wireless_notifications:
                set_register_request = SetEnableHidppReportingRequest(
                    receiver_reporting_flag_wireless_notifications=int(enable))

                cls.send(
                    test_case=test_case,
                    report=set_register_request,
                    response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                    response_class_type=SetEnableHidppReportingResponse,
                    channel=channel)
            # end if
        # end if
    # end def set_hidpp_reporting

    @classmethod
    def update_feature_mapping(cls, test_case, feature_id, channel=None, skip_not_found=False):
        """
        Retrieve feature ID to feature index mapping from DUT and update the internal ``HidDispatcher``.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param feature_id: The feature ID to add to the feature mapping
        :type feature_id: ``int``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param skip_not_found: Flag indicating that the method shall raise an error when the feature ID is
                               not found if ``False`` and return 0 if ``True`` - OPTIONAL
        :type skip_not_found: ``bool``

        :return: The feature Index returned by the device (0 if not found)
        :rtype: ``int``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized or if the feature ID
                                   was not found and ``skip_not_found == False``
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        # Get the 0x0000 root feature object
        root_feature = RootFactory.create(
            test_case.config_manager.get_feature_version(test_case.f.PRODUCT.FEATURES.IMPORTANT.ROOT))

        device_index = cls.get_device_index(test_case=test_case, channel=channel)

        # Retry mechanism enabled (loop 3 times)
        message = None
        get_feature = None
        # Empty Error queue
        cls.empty_queue(test_case=test_case, channel=channel, queue_name=HIDDispatcher.QueueName.ERROR)
        # Empty Important queue
        cls.empty_queue(test_case=test_case, channel=channel, queue_name=HIDDispatcher.QueueName.IMPORTANT)
        for _ in range(cls.UPDATE_FEATURE_MAPPING_RETRY_COUNTER):
            if message is None:
                get_feature = root_feature.get_feature_cls(deviceIndex=device_index, featureId=feature_id)
                get_feature.softwareId = cls.ROOT_CIRCULAR_SOFTWARE_ID
                cls.ROOT_CIRCULAR_SOFTWARE_ID = (cls.ROOT_CIRCULAR_SOFTWARE_ID_MIN_VALUE +
                                                 (cls.ROOT_CIRCULAR_SOFTWARE_ID %
                                                  cls.ROOT_CIRCULAR_SOFTWARE_ID_MAX_VALUE))
                message = cls.send(
                    test_case=test_case,
                    channel=channel,
                    report=get_feature,
                    response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                    response_class_type=root_feature.get_feature_response_cls)
            # end if

            # Check if there is a de-synchronization in the communication i.e. wrong softwareId
            if isinstance(message, root_feature.get_feature_response_cls) and message.functionIndex == \
                    RootModel.INDEX.GET_FEATURE and not get_feature.softwareId == message.softwareId:
                message = cls.get_only(test_case=test_case, channel=channel,
                                       queue_name=HIDDispatcher.QueueName.IMPORTANT, allow_no_message=True)
            # end if

            # Does the response match our request
            if (message is not None and isinstance(message, root_feature.get_feature_response_cls) and
                    get_feature.softwareId == message.softwareId and
                    message.functionIndex == RootModel.INDEX.GET_FEATURE):
                # Does the device know the requested feature (0 is returned if unknown)
                if int(message.featIndex) > Root.FEATURE_NOT_FOUND:
                    channel.hid_dispatcher.add_feature_entry(
                        feature_index=int(message.featIndex),
                        feature_id=get_feature.featureId,
                        feature_version=message.featVer)
                    return int(message.featIndex)
                else:
                    # If the execution arrives here, it means the feature ID was not found
                    assert skip_not_found, f"Could not find feature ID 0x{feature_id:04X} in device"

                    return Root.FEATURE_NOT_FOUND
                # end if
            # end if

            # Process all received message from the channel in its HID dispatcher
            channel.process_all_report_type_in_dispatcher()

            # See if other messages are stack in the queue
            if channel.hid_dispatcher.important_message_queue.event_not_empty.is_set():
                message = cls.get_only(
                    test_case=test_case, channel=channel, queue_name=HIDDispatcher.QueueName.IMPORTANT,
                    received_trace_str="Received while updating feature mapping")
            # An error message had been received
            elif isinstance(message, Hidpp1ErrorCodes):
                break
            elif channel.hid_dispatcher.error_message_queue.event_not_empty.is_set():
                cls.get_only(test_case=test_case, channel=channel, queue_name=HIDDispatcher.QueueName.ERROR,
                             received_trace_str="Received error while updating feature mapping")
                break
            # The response has not been received - resend the request
            else:
                message = None
                continue
            # end if
        # end for

        # If the execution arrives here, it means the feature ID was not found
        assert skip_not_found, f"Could not find feature ID 0x{feature_id:04X} in device"

        return Root.FEATURE_NOT_FOUND
    # end def update_feature_mapping

    @classmethod
    def update_vlp_feature_mapping(cls, test_case, feature_id, channel=None, skip_not_found=False):
        """
        Retrieve feature ID to feature index mapping from DUT and update the internal ``HidDispatcher``.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param feature_id: The feature ID to add to the feature mapping
        :type feature_id: ``int``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param skip_not_found: Flag indicating that the method shall raise an error when the feature ID is
                               not found if ``False`` and return 0 if ``True`` - OPTIONAL
        :type skip_not_found: ``bool``

        :return: The feature Index returned by the device (0 if not found)
        :rtype: ``int``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized or if the feature ID
                                   was not found and ``skip_not_found == False``
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        # Get the 0x0102 vlp root feature object
        vlp_root_feature = VLPRootFactory.create(
            test_case.config_manager.get_feature_version(test_case.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT))

        device_index = cls.get_device_index(test_case=test_case, channel=channel)

        # Retry mechanism enabled (loop 3 times)
        message = None
        get_feature = None
        # Empty Error queue
        cls.empty_queue(test_case=test_case, channel=channel, queue_name=HIDDispatcher.QueueName.ERROR)
        # Empty Important queue
        cls.empty_queue(test_case=test_case, channel=channel, queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT)
        for _ in range(cls.UPDATE_FEATURE_MAPPING_RETRY_COUNTER):
            if message is None:
                get_feature = vlp_root_feature.get_feature_index_cls(
                    device_index=device_index,
                    feature_id=feature_id,
                    vlp_begin=True,
                    vlp_end=True,
                    vlp_ack=True)
                get_feature.softwareId = cls.ROOT_CIRCULAR_SOFTWARE_ID
                cls.ROOT_CIRCULAR_SOFTWARE_ID = (cls.ROOT_CIRCULAR_SOFTWARE_ID_MIN_VALUE +
                                                 (cls.ROOT_CIRCULAR_SOFTWARE_ID %
                                                  cls.ROOT_CIRCULAR_SOFTWARE_ID_MAX_VALUE))
                message = cls.send(
                    test_case=test_case,
                    channel=channel,
                    report=get_feature,
                    response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                    response_class_type=vlp_root_feature.get_feature_index_response_cls)
            # end if

            # Check if there is a de-synchronization in the communication i.e. wrong softwareId
            if isinstance(message, vlp_root_feature.get_feature_index_response_cls) and message.feature_index == \
                    VLPRootModel.INDEX.GET_FEATURE_INDEX and get_feature.softwareId == message.softwareId:
                message = cls.get_only(test_case=test_case, channel=channel,
                                       queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT, allow_no_message=True)
            # end if

            # Does the response match our request
            if (message is not None and isinstance(message, vlp_root_feature.get_feature_index_response_cls) and
                    get_feature.softwareId == message.softwareId and
                    Numeral(message.feature_index) == VLPRootModel.INDEX.GET_FEATURE_INDEX):
                channel.hid_dispatcher.add_vlp_feature_entry(
                    feature_index=int(Numeral(message.feature_idx)),
                    feature_id=get_feature.feature_id,
                    feature_version=message.feature_version)
                return int(Numeral(message.feature_idx))
                # end if
            # end if

            # Process all received message from the channel in its HID dispatcher
            channel.process_all_report_type_in_dispatcher()

            # See if other messages are stack in the queue
            if channel.hid_dispatcher.important_message_queue.event_not_empty.is_set():
                message = cls.get_only(
                    test_case=test_case, channel=channel, queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                    received_trace_str="Received while updating feature mapping")
            # An error message had been received
            elif isinstance(message, Hidpp1ErrorCodes):
                break
            elif channel.hid_dispatcher.error_message_queue.event_not_empty.is_set():
                cls.get_only(test_case=test_case, channel=channel, queue_name=HIDDispatcher.QueueName.ERROR,
                             received_trace_str="Received error while updating feature mapping")
                break
            # The response has not been received - resend the request
            else:
                message = None
                continue
            # end if
        # end for

        # If the execution arrives here, it means the feature ID was not found
        assert skip_not_found, f"Could not find feature ID 0x{feature_id:04X} in device"

        return VLPRoot.FEATURE_NOT_FOUND
    # end def update_vlp_feature_mapping

    @classmethod
    def empty_queue(cls, test_case, queue_name, channel=None):
        """
        Empty a queue of a channel's HID dispatcher.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param queue_name: The queue name (names can be found in ``HIDDispatcher.QueueName``)
        :type queue_name: ``str``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        try:
            message = cls.get_only(
                test_case=test_case, channel=channel, queue_name=queue_name, timeout=0,
                allow_no_message=True, received_trace_str="Received while emptying")
        except ChannelException as exception:
            if exception.get_cause() == ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT:
                return
            else:
                # Trigger an assertion error so that the result is handled as a test failure
                raise AssertionError(exception)
            # end if
        # end try

        while message is not None:
            message = cls.get_only(
                test_case=test_case, channel=channel, queue_name=queue_name, timeout=0,
                allow_no_message=True, received_trace_str="Received while emptying")
        # end while
    # end def empty_queue

    @classmethod
    def empty_queues(cls, test_case, channel=None):
        """
        Empty all queues of a channel's HID dispatcher.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        for queue in channel.hid_dispatcher.queue_list:
            cls.empty_queue(test_case=test_case, channel=channel, queue_name=queue.name)
        # end for

        if isinstance(channel, ThroughReceiverChannel):
            cls.empty_queues(test_case=test_case, channel=channel.receiver_channel)
        # end if
    # end def empty_queues

    @classmethod
    def warn_queue_not_empty(cls, test_case, queue_name, channel=None, low_warning_classes=None):
        """
        Warn if the dispatcher queue is not empty on a given channel.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param queue_name: The queue name (names can be found in ``HIDDispatcher.QueueName``)
        :type queue_name: ``str``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param low_warning_classes: The list of message classes which shall not generate an important warning - OPTIONAL
        :type low_warning_classes: ``tuple[type]`` or ``None``

        :return: ``True`` if the queue is empty, ``False`` otherwise
        :rtype: ``bool``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        message = cls.get_only(
            test_case=test_case, channel=channel, queue_name=queue_name, timeout=0,
            allow_no_message=True, received_trace_str=None)
        if message is not None:
            warning_level = WarningLevel.IMPORTANT if low_warning_classes is None or not isinstance(
                message, low_warning_classes) else WarningLevel.ROBUSTNESS
            test_case.log_warning(f"{str(test_case)}:\n{channel}, {queue_name} not empty: {str(message)}",
                                  warning_level=warning_level)
            return False
        # end if

        return True
    # end def warn_queue_not_empty

    @staticmethod
    def send_only(test_case, report, channel=None, timeout=BaseCommunicationChannel.GENERIC_SEND_TIMEOUT):
        """
        Send a report on a channel.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param report: The report to send
        :type report: ``TimestampedBitFieldContainerMixin``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param timeout: Timeout to send the report (0 to disable it)- OPTIONAL
        :type timeout: ``int`` or ``float``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        LogHelper.log_trace(test_case=test_case, msg=f"[{channel}] Sending {str(report)}")

        channel.send_data(data=report, timeout=timeout)

        LogHelper.log_trace(test_case=test_case, msg=f"[{channel}] Sent {str(report)}")
    # end def send_only

    @classmethod
    def get_only(
            cls,
            test_case,
            channel=None,
            queue_name=None,
            class_type=None,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            check_first_message=True,
            allow_no_message=False,
            skip_error_message=False,
            received_trace_str="Received"):
        """
        Get message from a channel. Note that queue and message type are optional.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param queue_name: The queue name (names can be found in ``HIDDispatcher.QueueName``). If None, it bypasses the
                           dispatcher and get the first new HID++ message (old messages already processed by the
                           dispatcher are not considered) received as a ``TransportMessage`` - OPTIONAL
        :type queue_name: ``str``
        :param class_type: The type(s) of expected message. If ``None``, the type is not checked - OPTIONAL
        :type class_type: ``type`` or ``tuple[type]`` or ``None``
        :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
        :type timeout: ``float``
        :param check_first_message: Flag indicating that we apply the checks on the first received message - OPTIONAL
        :type check_first_message: ``bool``
        :param allow_no_message: Flag to enable (default) / disable exception when the requested message in not
                                 received - OPTIONAL
        :type allow_no_message: ``bool``
        :param skip_error_message: Flag indicating if the automatic error catching mechanism should be skipped or
                                   not. This will be always True if the queue is hid_message_queue (HID++ error message
                                   are not important to HID messages) - OPTIONAL
        :type skip_error_message: ``bool``
        :param received_trace_str: Output message used to customize the log trace for when the message is received,
                                   Note that the logging can be disabled with ``None`` - OPTIONAL
        :type received_trace_str: ``str`` or ``None``

        :return: The message retrieved from the queue
        :rtype:  ``class_type``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized or if ``class_type``
                                   is not ``None`` and the message class is not equal to it
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        if queue_name is not None:
            queue = channel.hid_dispatcher.get_queue_by_name(name=queue_name)
            assert queue is not None, f"Could not find queue: {queue_name}"
        else:
            assert class_type is None, f"Cannot have no queue name specified but a class type {class_type} requested"
            queue = None
        # end if

        message = None
        delta = 0
        try:
            if queue == channel.hid_dispatcher.hid_message_queue:
                interface_types = [LogitechReportType.MOUSE, LogitechReportType.KEYBOARD, LogitechReportType.DIGITIZER]
                list_index = 0
                end_time = time() + timeout
                remaining_time = timeout
                if remaining_time > cls.TIME_STEP_GET_MESSAGE_IN_MULTIPLE_TIME_STAMPED_QUEUE:
                    timeout_to_use = cls.TIME_STEP_GET_MESSAGE_IN_MULTIPLE_TIME_STAMPED_QUEUE
                elif remaining_time > 0:
                    timeout_to_use = remaining_time
                else:
                    timeout_to_use = 0
                # end if
                message = None
                count = 0
                start = perf_counter_ns()
                while message is None and (remaining_time >= 0 or count < len(interface_types)):
                    try:
                        message = channel.get_message(
                            report_type=interface_types[list_index], dispatcher_queue=queue,
                            message_class=None if check_first_message else class_type,
                            timeout=timeout_to_use, skip_error=True)
                    except Empty as exception:
                        count += 1
                        list_index = (list_index + 1) % len(interface_types)
                        remaining_time = end_time - time()
                        if remaining_time > cls.TIME_STEP_GET_MESSAGE_IN_MULTIPLE_TIME_STAMPED_QUEUE:
                            timeout_to_use = cls.TIME_STEP_GET_MESSAGE_IN_MULTIPLE_TIME_STAMPED_QUEUE
                        elif remaining_time > 0:
                            timeout_to_use = remaining_time
                        else:
                            timeout_to_use = 0
                        # end if

                        if count < len(interface_types):
                            # This is done to ensure that all existing interface queues are polled
                            continue
                        # end if

                        if remaining_time <= 0:
                            raise exception
                        # end if
                    except ChannelException as exception:
                        if exception.get_cause() in \
                            [ChannelException.Cause.EXPECTED_LINK_NOT_PRESENT,
                             ChannelException.Cause.ASSOCIATED_RECEIVER_CHANNEL_EXPECTED_LINK_NOT_PRESENT]:
                            count += 1
                            list_index = (list_index + 1) % len(interface_types)
                            remaining_time = end_time - time()
                            if remaining_time > cls.TIME_STEP_GET_MESSAGE_IN_MULTIPLE_TIME_STAMPED_QUEUE:
                                timeout_to_use = cls.TIME_STEP_GET_MESSAGE_IN_MULTIPLE_TIME_STAMPED_QUEUE
                            elif remaining_time > 0:
                                timeout_to_use = remaining_time
                            else:
                                timeout_to_use = 0
                            # end if
                        else:
                            raise exception
                        # end if
                    # end try
                # end while
                delta = ((perf_counter_ns() // 10 ** 6) - (start // 10 ** 6))
            else:
                start = perf_counter_ns()
                message = channel.get_message(
                    dispatcher_queue=queue,
                    message_class=None if check_first_message else class_type,
                    timeout=timeout,
                    skip_error=skip_error_message)
                delta = ((perf_counter_ns() // 10 ** 6) - (start // 10 ** 6))
            # end if
        except Empty as exception:
            if not allow_no_message:
                if class_type is not None:
                    if not isinstance(class_type, tuple):
                        class_name = class_type.__name__
                    else:
                        class_name = []
                        for class_t in class_type:
                            class_name.append(class_t.__name__)
                        # end for
                    # end if
                    exception.args += (f"No {class_name} message received after {timeout}s",)
                # end if
                # Trigger an assertion error so that the result is handled as a test failure
                raise AssertionError(exception)
            # end if
        # end try

        if message is not None:
            if delta > cls.LOGGING_THRESHOLD:
                test_case.log_warning(
                    message=f'Get message takes {delta}ms to complete '
                            f'(message type is {message.__class__.__name__})',
                    warning_level=WarningLevel.ROBUSTNESS)
            # end if

            if class_type is not None and check_first_message:
                assert isinstance(message, class_type), f"bad message type: expected {class_type}, obtained {message}"
            # end if

            if received_trace_str is not None:
                LogHelper.log_trace(
                    test_case=test_case, msg=f"[{channel}] {received_trace_str} {str(message)}")
            # end if
        # end if

        return message
    # end def get_only

    @classmethod
    def clean_messages(cls, test_case, queue_name, class_type, channel=None):
        """
        Clean all message of a wanted type(s) from queue.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param queue_name: The queue name (names can be found in ``HIDDispatcher.QueueName``)
        :type queue_name: ``str``
        :param class_type: The type of messages to remove from the queue, cannot be ``None``
        :type class_type: ``type`` or ``tuple[type]``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: List of removed messages
        :rtype: ``list[class_type]``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        assert class_type is not None, "class_type cannot be None"

        removed_messages = []
        no_more_message = False
        while not no_more_message:
            message = cls.get_only(
                test_case=test_case, channel=channel, queue_name=queue_name, class_type=class_type, timeout=0,
                check_first_message=False, allow_no_message=True, received_trace_str="Received and cleaned")
            if message is not None:
                removed_messages.append(message)
            else:
                no_more_message = True
            # end if
        # end while

        return removed_messages
    # end def clean_messages

    @classmethod
    def check_queue_empty(cls, test_case, queue_name, channel=None, timeout=0, class_type=None):
        """
        Check that a queue is empty for the duration of ``timeout``.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param queue_name: The queue name (names can be found in ``HIDDispatcher.QueueName``)
        :type queue_name: ``str``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param timeout: Duration to check that the queue stays empty in second - OPTIONAL
        :type timeout: ``int`` or ``float``
        :param class_type: The type of messages to be retrieved from the queue, cannot be ``None``
        :type class_type: ``type`` or ``tuple[type]`` or ``None``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        # Wait for the first message
        message = cls.get_only(
            test_case=test_case, channel=channel, queue_name=queue_name, class_type=class_type, timeout=timeout,
            check_first_message=False, allow_no_message=True, skip_error_message=True,
            received_trace_str=f"Received while checking if the queue {queue_name} is empty")

        test_case.assertIsNone(obj=message, msg=f"[{channel}] {queue_name} not empty, received {message}")
    # end def check_queue_empty

    @classmethod
    def send(
            cls,
            test_case,
            report,
            response_queue_name,
            channel=None,
            send_timeout=BaseCommunicationChannel.GENERIC_SEND_TIMEOUT,
            get_timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            response_class_type=None,
            skip_error_message=False):
        """
        Send a request through a channel and get the response from the given queue. Note that the class type check is
        optional.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param report: The report to send
        :type report: ``TimestampedBitFieldContainerMixin``
        :param response_queue_name: The queue name (names can be found in ``HIDDispatcher.QueueName``)
        :type response_queue_name: ``str``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param send_timeout: The timeout of the send action in seconds (0 disable it) - OPTIONAL
        :type send_timeout: ``float``
        :param get_timeout: The timeout of the received action in seconds (0 disable it) - OPTIONAL
        :type get_timeout: ``float``
        :param response_class_type: The type of expected message. If ``None``, the type is not checked - OPTIONAL
        :type response_class_type: ``type`` or ``tuple[type]`` or ``None``
        :param skip_error_message: Flag indicating if the automatic error catching mechanism should be skipped or
                                   not. This will be always True if the queue is hid_message_queue (HID++ error message
                                   are not important to HID messages) - OPTIONAL
        :type skip_error_message: ``bool``

        :return: The message get from the queue
        :rtype: ``response_class_type``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        response_queue = channel.hid_dispatcher.get_queue_by_name(name=response_queue_name)
        assert response_queue is not None, f"Could not find queue: {response_queue_name}"

        retry_count = 0
        message = None
        # The retry mechanism is used in the event that the device is in sleep state and needs to be woken up
        while retry_count < cls.GENERIC_MAX_RETRY_COUNT:
            try:
                LogHelper.log_trace(test_case=test_case, msg=f"[{channel}] Sending {str(report)}")
                message = channel.send_data_wait_response(
                    data=report,
                    send_timeout=send_timeout,
                    reply_timeout=get_timeout,
                    dispatcher_queue=response_queue,
                    message_class=response_class_type,
                    skip_error=skip_error_message)
                break
            except ChannelException as exception:
                retry_count += 1
                if retry_count >= cls.GENERIC_MAX_RETRY_COUNT:
                    # Trigger an assertion error so that the result is handled as a test failure
                    raise AssertionError(exception)
                # end if

                if exception.get_cause() == ChannelException.Cause.ERROR_MESSAGE_RECEIVED:
                    error_message = exception.get_error_message_object()
                    if (isinstance(error_message, Hidpp1ErrorCodes) and int(Numeral(error_message.errorCode)) in
                            [Hidpp1ErrorCodes.ERR_RESOURCE_ERROR, Hidpp1ErrorCodes.ERR_CONNECT_FAIL]):
                        test_case.wake_up_device_with_user_action()
                        continue
                    elif (isinstance(error_message, Hidpp1ErrorCodes) and
                          (int(Numeral(error_message.errorCode)) in [Hidpp1ErrorCodes.ERR_INVALID_SUBID,
                                                                     Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])):
                        LogHelper.log_trace(test_case=test_case, msg=f"[{channel}] Sent {str(report)}")
                        LogHelper.log_trace(test_case=test_case, msg=f"[{channel}] Received error {str(message)}")
                        return error_message
                    # end if
                # end if
                # Trigger an assertion error so that the result is handled as a test failure
                raise AssertionError(exception)
            except QueueEmpty as exception:
                # Trigger an assertion error so that the result is handled as a test failure
                raise AssertionError(exception)
            # end try
        # end while

        assert message is not None, "This should never happen"

        LogHelper.log_trace(test_case=test_case,
                            msg=f"[{channel}] Sent {report.light_str() if hasattr(report, 'light_str') else report}")
        LogHelper.log_trace(test_case=test_case, msg=f"[{channel}] Received {str(message)}")
        return message
    # end def send

    @staticmethod
    def get_descriptors(test_case, channel=None):
        """
        Retrieve interface descriptors from the channel.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: The received descriptors
        :rtype: ``list[ReportDescriptor|None]``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        descriptors = channel.get_descriptors()
        for descriptor in [x for x in descriptors if x is not None]:
            LogHelper.log_trace(
                test_case=test_case, msg=f'[{channel}] Received Descriptor:\n{descriptor.light_str()}')
        # end for

        return descriptors
    # end def get_descriptors

    @staticmethod
    def get_feature_version(test_case, feature_index, channel=None):
        """
        Get version of a feature from a channel dispatcher using its feature id.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param feature_index: Feature index
        :type feature_index: ``int``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: Feature version
        :rtype: ``int``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        return channel.hid_dispatcher.get_feature_entry_by_index(feature_index=feature_index)[1]
    # end get_feature_version

    @staticmethod
    def get_vlp_feature_version(test_case, feature_index, channel=None):
        """
        Get version of a VLP feature from a channel dispatcher using its feature id.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param feature_index: Feature index
        :type feature_index: ``int``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``

        :return: Feature version
        :rtype: ``int``

        :raise ``AssertionError``: If no channel was given and current channel is not initialized
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        return channel.hid_dispatcher.get_vlp_feature_entry_by_index(feature_index=feature_index)[1]
    # end get_vlp_feature_version

    @classmethod
    def wait_through_receiver_channel_link_status(
            cls,
            test_case,
            channel,
            link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
            device_index=None,
            timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            allow_no_message=False):
        """
        Wait for a ``DeviceConnection`` with the expected link status (and device index if given).

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use, it can be a receiver channel or a "through receiver" channel
        :type channel: ``UsbReceiverChannel`` or ``ThroughReceiverChannel``
        :param link_status: The expected link status (Values can be found in ``DeviceConnection.LinkStatus``) - OPTIONAL
        :type link_status: ``int``
        :param device_index: The expected device index. If ``None``, it is ignored - OPTIONAL
        :type device_index: ``int`` or ``None``
        :param timeout: Time to wait for message before raising exception [seconds] - OPTIONAL
        :type timeout: ``float``
        :param allow_no_message: Flag to enable (default) / disable exception when the requested message in not
                                 received - OPTIONAL
        :type allow_no_message: ``bool``

        :return: Flag indicating if the expected packet is received (only useful when ``allow_no_message`` is True)
        :rtype: ``bool``

        :raise ``AssertionError``: If a ThroughReceiverChannel was given and device_index is not ``None`` and not the
                                   same as the channel or if the channel is not a valid type
        """
        if isinstance(channel, ThroughReceiverChannel):
            channel_to_use = channel.receiver_channel
            if device_index is None:
                device_index = channel.device_index
            else:
                assert device_index == channel.device_index, \
                    f"Parameters channel={channel} and device_index={device_index} do not match"
            # end if
        else:
            assert isinstance(channel, UsbReceiverChannel), f"{channel} has not a valid type"
            channel_to_use = channel
        # end if

        end_time = time() + timeout
        remaining_time = timeout
        packet_device_index = None
        packet_link_status = None

        while (packet_link_status != link_status or (device_index is not None and packet_device_index != device_index))\
                and remaining_time > 0:
            device_connection = cls.get_only(
                test_case=test_case,
                channel=channel_to_use,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=DeviceConnection,
                timeout=remaining_time,
                check_first_message=False,
                allow_no_message=allow_no_message,
                received_trace_str=f"Received while waiting for link status = {link_status}")

            if device_connection is None:
                # This will be reached only if ``allow_no_message`` is True and no message is received
                return False
            # end if

            device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(device_connection)

            packet_link_status = to_int(
                device_info_class.fromHexList(HexList(device_connection.information)).device_info_link_status)
            packet_device_index = to_int(device_connection.device_index)

            if isinstance(channel, ThroughReceiverChannel) and packet_device_index == channel.device_index:
                channel.connected = (packet_link_status == DeviceConnection.LinkStatus.LINK_ESTABLISHED)
            # end if

            remaining_time = end_time - time()
        # end while

        test_case.assertTrue(
            expr=remaining_time > 0, msg=f"Timeout ({timeout}s) reached while waiting for the right connection event")

        return True
    # end def wait_through_receiver_channel_link_status

    @classmethod
    def wait_usb_ble_channel_connection_state(
            cls, test_case, channel, connection_state=False, timeout=GENERIC_RESET_TIMEOUT, skip_error=False):
        """
        Wait for a connection state on a given channel (USB or BLE).

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. Could be ``UsbChannel`` or ``BleChannel``
        :type channel: ``BaseCommunicationChannel``
        :param connection_state: The expected connection state - OPTIONAL
        :type connection_state: ``bool``
        :param timeout: Time to wait for the expected connection state to happen [seconds] - OPTIONAL
        :type timeout: ``float``
        :param skip_error: Flag to enable (default) / disable exception when the expected connection state is not
                           obtained - OPTIONAL
        :type skip_error: ``bool``

        :return: Flag indicating if the expected connection state is obtained (only useful when ``skip_error`` is True)
        :rtype: ``bool``
        """
        assert isinstance(channel, (UsbChannel, BleChannel)), \
            f"This method is only for UsbChannel and BleChannel, not {type(channel)}"

        result = channel.wait_device_connection_state(connected=connection_state, timeout=timeout)

        if skip_error:
            return result
        # end if

        if isinstance(channel, UsbChannel):
            device_id = channel.get_channel_usb_port_path_str()
        else:
            device_id = channel.get_device_ble_address()
        # end if

        test_case.assertTrue(
            expr=result,
            msg=f"Timeout ({timeout}s) reached for device {device_id} ({channel.__class__.__name__}) while waiting "
                f"for the right connection state = {connection_state}")

        return True
    # end def wait_usb_ble_channel_connection_state

    @classmethod
    def wait_for_channel_device_to_be_connected(
            cls, test_case, channel=None, open_channel=True, link_enabler=LinkEnablerInfo.ALL_MASK,
            timeout=GENERIC_RESET_TIMEOUT):
        """
        Wait for the device of a channel to be connected and accessible again. This will open the current channel if
        it is closed.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BaseCommunicationChannel`` or ``None``
        :param open_channel: Flag indicating to open the channel after waiting for it to be connected - OPTIONAL
        :type open_channel: ``bool``
        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo`` - OPTIONAL
        :type link_enabler: ``int`` or ``BitStruct``
        :param timeout: Time to wait for the expected connection state to happen [seconds] - OPTIONAL
        :type timeout: ``float``
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"

        if isinstance(channel, ThroughReceiverChannel):
            with cls.channel_open_state(test_case=test_case, channel=channel.receiver_channel):
                cls.wait_through_receiver_channel_link_status(
                    test_case=test_case,
                    channel=channel,
                    link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                    timeout=timeout)
            # end with
        elif isinstance(channel, (UsbChannel, BleChannel)):
            cls.wait_usb_ble_channel_connection_state(
                test_case=test_case,
                channel=channel,
                connection_state=True,
                timeout=timeout)
        else:
            raise RuntimeError(f"Unknown channel type: {channel}")
        # end if

        if open_channel and not channel.is_open:
            cls.open_channel(test_case=test_case, link_enabler=link_enabler)
        # end if
    # end def wait_for_channel_device_to_be_connected

    @staticmethod
    def disconnect_ble_channel(test_case, channel=None):
        """
        Disconnect a BLE channel's device. Automatically close the channel if open.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: The channel to use. If ``None``, ``test_case.current_channel`` is used - OPTIONAL
        :type channel: ``BleChannel`` or ``None``
        """
        channel = channel if channel is not None else test_case.current_channel
        assert channel is not None, "No channel was given and current channel is not initialized"
        assert isinstance(channel, BleChannel), f"This method can only be used on a BleChannel, {channel} is not"

        channel.disconnect_from_device()
    # end def disconnect_ble_channel
# end class ChannelUtils

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
