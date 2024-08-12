#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.base.devicemanagerutils
:brief: Help for Device management actions and information
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/11/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.blechannel import BleChannel
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# Features implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceManagerUtils:
    """
    This class provides helpers for device manager actions and information
    """
    MAX_SWITCHING_TIME = 1

    @staticmethod
    def get_channels(test_case, channel_id, check_connected=False):
        """
        Get a list of channels from the device manager matching the wanted channel identifier.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel_id: The wanted channel identifier
        :type channel_id: ``ChannelIdentifier`` or ``list[ChannelIdentifier]``
        :param check_connected: The wanted channel should be a connected one - OPTIONAL
        :type check_connected: ``bool``

        :return: A list of channels from the device manager
        :rtype: ``list[BaseCommunicationChannel]``
        """
        if test_case.device is None:
            return []
        # end if

        if not isinstance(channel_id, list):
            channel_id = [channel_id]
        # end if

        return test_case.device.get_channels(channel_ids=channel_id, check_connected=check_connected)
    # end def get_channels

    @staticmethod
    def get_channel(test_case, channel_id, check_connected=False):
        """
        Get the first channel from the device manager matching the wanted channel identifier. ``None`` is returned if
        nothing is found.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel_id: The wanted channel identifier
        :type channel_id: ``ChannelIdentifier`` or ``list[ChannelIdentifier]``
        :param check_connected: The wanted channel should be a connected one - OPTIONAL
        :type check_connected: ``bool``

        :return: A list of channels from the device manager
        :rtype: ``BaseCommunicationChannel`` or ``None``
        """
        if test_case.device is None:
            return None
        # end if

        if not isinstance(channel_id, list):
            channel_id = [channel_id]
        # end if

        return test_case.device.get_channel(channel_ids=channel_id, check_connected=check_connected)
    # end def get_channel

    @staticmethod
    def refresh_channel_cache(test_case):
        """
        Refresh the channel cache:
        - Wait for all cached USB devices to be connected
        - Refresh all through receiver channel by communicating with each receiver

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        assert test_case.device is not None, "Cannot refresh channel cache is no device manager was found"

        for usb_channel in test_case.device.USB_CHANNEL_MAPPING.values():
            if ChannelUtils.get_port_index(test_case=test_case, channel=usb_channel) != \
                    test_case.device.CHARGING_PORT_NUMBER:
                ChannelUtils.wait_usb_ble_channel_connection_state(
                    test_case=test_case, channel=usb_channel, connection_state=True)
            # end if
        # end for

        test_case.device.refresh_through_receiver_channel_cache()
    # end def refresh_channel_cache

    @staticmethod
    def add_channel_to_cache(test_case, channel):
        """
        Add a channel to the cache. For now only ThroughReceiverChannel are accepted. If the channel is already in
        cache, nothing is done. This method cannot be used to replace an existing channel in the cache by another
        channel with the same port index and device index.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param channel: Channel to add
        :type channel: ``ThroughReceiverChannel``
        """
        assert test_case.device is not None, "Cannot add channel to cache is no device manager was found"

        test_case.device.add_channel_to_cache(channel=channel)
    # end add_channel_to_cache

    @staticmethod
    def remove_channel_from_cache(test_case, port_index, device_index=None):
        """
        Remove a channel from the cache. For now only ThroughReceiverChannel are affected by this method. If no
        channel with the given port index and device index is in cache, nothing is done.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param port_index: Port index of the channel to remove
        :type port_index: ``int``
        :param device_index: Device index of the device to remove. If ``None``, all device indexes for the receiver
                             on ``port_index`` are removed - OPTIONAL
        :type device_index: ``int`` or ``None``
        """
        assert test_case.device is not None, "Cannot remove channel to cache is no device manager was found"

        test_case.device.remove_channel_from_cache(port_index=port_index, device_index=device_index)
    # end remove_channel_from_cache

    @staticmethod
    def log_all_channels_in_cache(test_case):
        """
        Use the LogHelper to log all the channel in the cache, regardless of the channel protocol.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        if len(test_case.device.USB_CHANNEL_MAPPING) == 0:
            log_to_write = "\nNo USB channel in cache:\n"
        else:
            log_to_write = "\nAll USB channel in cache:\n"
            for channel in test_case.device.USB_CHANNEL_MAPPING.values():
                log_to_write += f"\t{channel}\n"
            # end for
        # end if

        if len(test_case.device.THROUGH_RECEIVER_CHANNEL_MAPPING) == 0:
            log_to_write += "\nNo Through Receiver channel in cache:\n"
        else:
            log_to_write += "\nAll Through Receiver channel in cache:\n"
            for channel in test_case.device.THROUGH_RECEIVER_CHANNEL_MAPPING.values():
                log_to_write += f"\t{channel}\n"
            # end for
        # end if

        if len(test_case.device.BLE_CHANNEL_MAPPING) == 0:
            log_to_write += "\nNo BLE channel in cache:\n"
        else:
            log_to_write += "\nAll BLE channel in cache:\n"
            for channel in test_case.device.BLE_CHANNEL_MAPPING.values():
                log_to_write += f"\t{channel}\n"
            # end for
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg=log_to_write)
        # --------------------------------------------------------------------------------------------------------------
    # end log_all_channels_in_cache

    @classmethod
    def switch_channel(
            cls,
            test_case,
            new_channel=None,
            new_channel_id=None,
            close_associated_channel=True,
            open_associated_channel=True,
            allow_no_message=False):
        """
        Switch the current channel to a new one. This method close the previous channel and open the new one. This
        method can either be used with a channel (``new_channel``) object directly or with a channel identifier
        (``new_channel_id``). For the second option, the first channel found using ``get_channels`` will be used.
        The first option takes precedence over the second one. The value ``None`` is to not use the option. At least
        one option should not be ``None``.

        This method will check the transition to the new channel, depending on the protocol of the previous and the
        new channels (``DeviceConnection`` packets or physical disconnection of USB port for example).

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param new_channel: The new channel to use. ``None`` not to use this option - OPTIONAL
        :type new_channel: ``BaseCommunicationChannel`` or ``None``
        :param new_channel_id: The new channel identifier to use. ``None`` not to use this option - OPTIONAL
        :type new_channel_id: ``ChannelIdentifier`` or ``None``
        :param close_associated_channel: Flag used for closing the previous channel. See ``ChannelUtils.close_channel``
                                         parameter with the same name - OPTIONAL
        :type close_associated_channel: ``bool``
        :param open_associated_channel: Flag used for opening the new channel. See ``ChannelUtils.open_channel``
                                        parameter with the same name - OPTIONAL
        :type open_associated_channel: ``bool``
        :param allow_no_message: Flag to enable (default) / disable exception when the requested message in not
                                 received - OPTIONAL
        :type allow_no_message: ``bool``
        """
        assert new_channel is not None or new_channel_id is not None, \
            "Cannot perform switch_channel without a new channel to switch to (both optional parameters for " \
            "that are None)"

        if new_channel is None:
            new_channel = cls.get_channel(test_case=test_case, channel_id=new_channel_id)
        # end if

        if isinstance(test_case.current_channel, ThroughReceiverChannel):
            ChannelUtils.wait_through_receiver_channel_link_status(
                test_case=test_case,
                channel=test_case.current_channel,
                link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT,
                allow_no_message=True if test_case.f.PRODUCT.F_IsGaming or allow_no_message else False)
        elif isinstance(test_case.current_channel, BleChannel):
            ChannelUtils.wait_usb_ble_channel_connection_state(
                test_case=test_case,
                channel=test_case.current_channel,
                connection_state=False,
                timeout=1,
                skip_error=False)
        elif isinstance(test_case.current_channel, UsbChannel):
            # Check USB port state
            test_case.assertFalse(test_case.device.get_usb_ports_status()[5], 'HUB USB port has not been powered off')
        else:
            raise RuntimeError(f"Unknown current channel type: {test_case.current_channel}")
        # end if

        ChannelUtils.close_channel(test_case=test_case, close_associated_channel=close_associated_channel)

        if isinstance(new_channel, ThroughReceiverChannel):
            if open_associated_channel and not new_channel.receiver_channel.is_open:
                ChannelUtils.open_channel(test_case=test_case, channel=new_channel.receiver_channel)
            # end if

            status = ChannelUtils.wait_through_receiver_channel_link_status(
                test_case=test_case,
                channel=new_channel,
                link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                timeout=.5,
                allow_no_message=True)

            if not status:
                # it is possible to have missed the connection event so the check is done with a fake arrival
                test_case.assertTrue(
                    expr=new_channel.is_device_connected(force_refresh_cache=True),
                    msg=f"New channel not connected: {new_channel}")
            else:
                new_channel.connected = True
            # end if
        elif isinstance(new_channel, (UsbChannel, BleChannel)):
            ChannelUtils.wait_usb_ble_channel_connection_state(
                test_case=test_case,
                channel=new_channel,
                connection_state=True,
                timeout=cls.MAX_SWITCHING_TIME)
        else:
            raise RuntimeError(f"Unknown new channel type: {new_channel}")
        # end if

        cls.set_channel(test_case=test_case, new_channel=new_channel, open_associated_channel=open_associated_channel)
    # end switch_channel

    @classmethod
    def set_channel(
            cls, test_case, new_channel=None, new_channel_id=None, open_channel=True, open_associated_channel=True,
            dump_current_hid_dispatcher=True):
        """
        Set the current channel to a new one. This method only set the current channel and optionally open it. This
        method can either be used with a channel (``new_channel``) object directly or with a channel identifier
        (``new_channel_id``). For the second option, the first channel found using ``get_channels`` will be used.
        The first option takes precedence over the second one. The value ``None`` is to not use the option. At least
        one option should not be ``None``.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param new_channel: The new channel to use. ``None`` not to use this option - OPTIONAL
        :type new_channel: ``BaseCommunicationChannel`` or ``None``
        :param new_channel_id: The new channel identifier to use. ``None`` not to use this option - OPTIONAL
        :type new_channel_id: ``ChannelIdentifier`` or ``None``
        :param open_channel: Open new channel after setting it as the current channel - OPTIONAL
        :type open_channel: ``bool``
        :param open_associated_channel: Flag used for opening the new channel. See ``open_channel`` parameter
                                        with the same name - OPTIONAL
        :type open_associated_channel: ``bool``
        :param dump_current_hid_dispatcher: Flag used for dumping the HID dispatcher of the current channel to the
                                            new channel (if they have the same protocol) the new channel - OPTIONAL
        :type dump_current_hid_dispatcher: ``bool``
        """
        assert new_channel is not None or new_channel_id is not None, \
            "Cannot perform switch_channel without a new channel to switch to (both optional parameters for " \
            "that are None)"

        if new_channel is None:
            new_channel = cls.get_channel(test_case=test_case, channel_id=new_channel_id)
        # end if

        if test_case.current_channel != new_channel:
            # Test case currently not on the right channel
            if test_case.current_channel.protocol == new_channel.protocol and dump_current_hid_dispatcher:
                test_case.current_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
                    other_dispatcher=new_channel.hid_dispatcher)
            elif test_case.backup_dut_channel.protocol == new_channel.protocol:
                test_case.backup_dut_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
                    other_dispatcher=new_channel.hid_dispatcher)
            else:
                # Add root feature to the new channel HID dispatcher
                root_version = test_case.config_manager.get_feature_version(test_case.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
                new_channel.hid_dispatcher.add_feature_entry(Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)
                if isinstance(new_channel, ThroughReceiverChannel):
                    new_channel.receiver_channel.hid_dispatcher.add_feature_entry(
                        Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)
                # end if
            # end if

            test_case.current_channel = new_channel

            # Configure current protocol in ConfigurationManager
            test_case.config_manager.current_protocol = test_case.current_channel.protocol
        # end if

        if open_channel and not new_channel.is_open:
            ChannelUtils.open_channel(test_case=test_case, open_associated_channel=open_associated_channel)
        # end if
    # end set_channel
# end class DeviceManagerUtils

# ----------------------------------------------------------------------------------------------------------------------
# End of file
# ----------------------------------------------------------------------------------------------------------------------
