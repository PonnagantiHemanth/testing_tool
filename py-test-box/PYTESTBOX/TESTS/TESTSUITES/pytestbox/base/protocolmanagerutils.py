#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.base.protocolmanagerutils
:brief: Help for protocol management actions and information
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/01/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from copy import deepcopy

from pychannel.blechannel import BleChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# Features implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProtocolManagerUtils:
    """
    This class provides helpers for Protocol manager actions and information
    """

    @classmethod
    def is_corded_device_only(cls, test_case):
        """
        Check if the current device is a pure-corded device (No wireless mode).

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Flag indicating if the device under test is only a corded device.
        :rtype: ``bool``
        """
        fw_info = test_case.getFeatures().PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION
        return fw_info.F_TransportUsb and not (fw_info.F_TransportEQuad or
                                               fw_info.F_TransportBTLE or
                                               fw_info.F_TransportBT)
    # end def is_corded_device_only

    @classmethod
    def switch_to_usb_channel(cls, test_case):
        """
        Switch to USB channel.

        Note:
        1. The USB cable shall be plugged on the last port of Phidgets USB Hub.
        2. At least one gaming receiver be plugged on USB Hub

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        if (test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb and
                not cls.is_corded_device_only(test_case=test_case)):
            usb_channel_id = ChannelIdentifier(
                port_index=test_case.device.CHARGING_PORT_NUMBER, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER)
            usb_channel = DeviceManagerUtils.get_channel(test_case=test_case, channel_id=usb_channel_id)
            if test_case.device.is_usb_channel_on_hub(usb_channel):
                test_case.device.turn_on_usb_charging_cable()
                try:
                    DeviceManagerUtils.switch_channel(test_case, new_channel=usb_channel)
                except Exception as e:
                    test_case.device.turn_off_usb_charging_cable()
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case, f"Switch channel failed with error = {str(e)}. Try again")
                    # --------------------------------------------------------------------------------------------------
                    test_case.device.turn_on_usb_charging_cable()
                    ChannelUtils.wait_usb_ble_channel_connection_state(
                        test_case=test_case, channel=usb_channel, connection_state=True)
                    DeviceManagerUtils.set_channel(test_case=test_case, new_channel=usb_channel)
                # end try
            else:
                raise RuntimeError('USB channel not found')
            # end if
        else:
            raise RuntimeError('USB protocol not available')
        # end if
    # end def switch_to_usb_channel

    @classmethod
    def exit_usb_channel(cls, test_case):
        """
        Exit the USB channel if another wireless protocol is supported.

        Note:
        1. The USB cable shall be plugged on the last port of Phidgets USB Hub.
        2. At least one gaming receiver be plugged on Phidgets USB Hub.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        if (test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb and
                not cls.is_corded_device_only(test_case=test_case)):
            if test_case.device.is_usb_channel_on_hub(test_case.current_channel):
                test_case.device.turn_off_usb_charging_cable()
                DeviceManagerUtils.switch_channel(test_case, new_channel=test_case.backup_dut_channel)
            # end if
        # end if
    # end def exit_usb_channel

    @classmethod
    def switch_to_ble_channel(cls, test_case):
        """
        Switch to BLE channel.

        Note:
         * Test case should have BLE context to change to BLE protocol

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Get the BLE context here to do the sanity checks sooner")
        # --------------------------------------------------------------------------------------------------------------
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Close channel")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=test_case)

        DeviceBaseTestUtils.enter_pairing_mode_ble(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg='Scan for BLE device')
        # --------------------------------------------------------------------------------------------------------------
        test_case.ble_context_device_used = BleProtocolTestUtils.scan_for_current_device(
            test_case=test_case, scan_timeout=1, send_scan_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg=f"Found device: {test_case.ble_context_device_used}")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg='Connect and bond to the BLE device')
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(test_case=test_case,
                                                     ble_context_device=test_case.ble_context_device_used)

        current_channel = BleChannel(ble_context=ble_context, ble_context_device=test_case.ble_context_device_used)
        if test_case.current_channel.protocol in [LogitechProtocol.BLE_PRO, LogitechProtocol.BLE]:
            test_case.current_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(current_channel.hid_dispatcher)
        # end if
        DeviceManagerUtils.set_channel(test_case=test_case, new_channel=current_channel)

        test_case.backup_dut_protocol_channel = test_case.backup_dut_channel
        test_case.backup_dut_channel = test_case.current_channel
    # end def switch_to_ble_channel

    @classmethod
    def exit_ble_channel(cls, test_case):
        """
        Exit BLE channel.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``
        """
        # noinspection PyBroadException
        try:
            ChannelUtils.close_channel(test_case=test_case)
            DeviceManagerUtils.set_channel(test_case=test_case, new_channel=test_case.backup_dut_protocol_channel)
        finally:
            # Delete bond from direct BLE device
            BleProtocolTestUtils.delete_device_bond(
                test_case=test_case, ble_context_device=test_case.ble_context_device_used)
            test_case.backup_dut_channel = test_case.backup_dut_protocol_channel
        # end try
    # end def exit_ble_channel

    @classmethod
    def switch_to_crush_channel(cls, test_case):
        """
        Switch to Crush channel

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Close channel")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Back up pairing info for crush receiver")
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.CrushReceiver.fetch_pairing_info(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Pair crush receiver")
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.CrushReceiver.pairing(test_case=test_case)

        test_case.backup_dut_protocol_channel = test_case.backup_dut_channel
        test_case.backup_dut_channel = test_case.current_channel
    # end def switch_to_crush_channel

    @classmethod
    def exit_crush_channel(cls, test_case):
        """
        Exit Crush channel

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase``
        """
        from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Restore pairing info for crush receiver")
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.CrushReceiver.force_close_lock(test_case=test_case)

        try:
            ChannelUtils.close_channel(test_case=test_case)
            DeviceManagerUtils.set_channel(test_case=test_case, new_channel=test_case.backup_dut_protocol_channel)
        finally:
            test_case.backup_dut_channel = test_case.backup_dut_protocol_channel
        # end try
    # end def exit_crush_channel

    @classmethod
    def select_channel_by_protocol(cls, test_case, protocol):
        """
        Select first channel matching required protocol.

        If protocol to select matches the current protocol, then it is not changed.
        Protocol to select can be:
        * ``None`` if no specific protocol is required. Then current protocol is kept selected.
        * Unifying protocols list if any Unifying protocol can be used. Then if current protocol is a Unifying protocol
        it is not changed. Else, first available Unifying protocol should be selected (TODO).
        * ``LogitechProtocol`` and it will be selected using its specific method (TODO).

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param protocol: Protocol or list of protocols which can be selected
        :type protocol: ``None`` or ``LogitechProtocol`` or ``list[LogitechProtocol]``

        :raise ``NotImplementedError``: If channel switch for given protocol is not available
        """
        if protocol not in [None, test_case.config_manager.current_protocol] and not (
                protocol == LogitechProtocol.unifying_protocols() and
                test_case.config_manager.current_protocol in LogitechProtocol.unifying_protocols()):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg='Backup NVS data before switching protocol')
            # ----------------------------------------------------------------------------------------------------------
            test_case.memory_manager.read_nvs()
            test_case.nvs_before_protocol_change = deepcopy(test_case.memory_manager.nvs_parser)
            if protocol == LogitechProtocol.USB:
                test_case.post_requisite_exit_usb = True
                cls.switch_to_usb_channel(test_case)
            elif protocol == LogitechProtocol.BLE:
                test_case.post_requisite_exit_ble = True
                cls.switch_to_ble_channel(test_case)
            elif protocol == LogitechProtocol.LS2_CA_CRC24_FOR_CRUSH:
                cls.switch_to_crush_channel(test_case=test_case)
            else:
                raise NotImplementedError(f"Unable to select channel by protocol: {protocol}")
            # end if
        # end if
    # end def select_channel_by_protocol
# end class ProtocolManagerUtils
# ----------------------------------------------------------------------------------------------------------------------
# End of file
# ----------------------------------------------------------------------------------------------------------------------
