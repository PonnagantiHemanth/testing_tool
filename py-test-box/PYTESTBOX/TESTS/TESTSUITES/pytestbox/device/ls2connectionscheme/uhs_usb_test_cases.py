#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.uhs_usb_test_cases
:brief: Validate UHS connection scheme for USB test cases
:author: Zane Lu
:date: 2022/11/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.ls2connectionscheme.uhs_connection_scheme import UhsConnectionSchemeBase
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UhsUsbTestCases(UhsConnectionSchemeBase):
    """
    UHS connection scheme - Usb Test Cases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # start from only usb cable connection
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is connected via USB cable')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.disable_all_receiver_usb_ports(self)
        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.power_supply_emulator.restart_device()
        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)
    # end def setUp

    def tearDown(self):
        with self.manage_post_requisite():
            self.connect_to_the_pre_paired_receiver()
        # end with
        super().tearDown()
    # end def tearDown

    @features('UhsConnectionScheme')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_starts_up_in_oob_state_with_usb_cable_and_crush_pre_paired_ls2_receiver_are_on(self):
        """
        The device starts up in OOB state while the USB charging cable plugged in
        and Crush / LS2 and pre-paired receivers are available and powered on.
        """
        Ls2ConnectionSchemeTestUtils.enable_hidden_features(self)
        Ls2ConnectionSchemeTestUtils.set_oob_state(self)
        self.power_supply_emulator.turn_off()

        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        LogHelper.log_prerequisite(self, 'Crush never paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered on')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and receiver powered on')
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [True, True, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is USB connected')
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.power_supply_emulator.turn_on()

        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        self.testCaseChecked("FUN_UHS_USB_0001")
    # end def test_device_starts_up_in_oob_state_with_usb_cable_and_crush_pre_paired_ls2_receiver_are_on

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_is_powered_on_with_usb_cable_and_crush_pre_paired_ls2_receiver_are_on(self):
        """
        The device is powered on while the USB charging cable plugged in
        and Crush / LS2 and pre-paired receivers are available and powered on.
        """
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [True, True, True, False, False])

        self.power_supply_emulator.turn_off()
        sleep(0.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is USB connected')
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.power_supply_emulator.turn_on()

        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        self.testCaseChecked("FUN_UHS_USB_0002")
    # end def test_device_is_powered_on_with_usb_cable_and_crush_pre_paired_ls2_receiver_are_on

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_reconnects_to_host_with_usb_cable_and_crush_pre_paired_ls2_receivers_are_on(self):
        """
        The device reconnects to the host while the USB charging cable plugged in
        and Crush / LS2 and pre-paired receivers are available and powered on.
        """
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [True, True, True, False, False])

        LogHelper.log_prerequisite(self, 'the device is in Disconnected state')
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, PortConfiguration.LS2_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.wait_for_deep_sleep_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is USB connected')
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        self.testCaseChecked("FUN_UHS_USB_0003")
    # end def test_device_reconnects_to_host_with_usb_cable_and_crush_pre_paired_ls2_receivers_are_on

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_the_device_connected_to_crush_shall_reconnect_to_host_via_usb_while_cable_is_plugged_in(self):
        """
        While connected to Crush, the device shall reconnect to the host on USB
        as soon as the USB charging cable is plugged in.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is not USB connected')
        # --------------------------------------------------------------------------------------------------------------
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is Crush connected')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection)
        )

        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.check_device_connected(link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)

        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        self.testCaseChecked("FUN_UHS_USB_0004")
    # end def test_the_device_connected_to_crush_shall_reconnect_to_host_via_usb_while_cable_is_plugged_in

    @features('UhsConnectionScheme')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_the_device_connected_to_pre_paired_rcvr_shall_reconnect_to_host_via_usb_while_cable_is_plugged_in(self):
        """
        While connected to a pre-paired receiver, the device shall reconnect to the host on USB
        as soon as the USB charging cable is plugged in.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is pre-paired receiver connected')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.connect_to_the_pre_paired_receiver()
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [True, False, False, False, False])

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection)
        )
        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.check_device_connected(link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)

        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        self.testCaseChecked("FUN_UHS_USB_0005")
    # end def test_the_device_connected_to_pre_paired_rcvr_shall_reconnect_to_host_via_usb_while_cable_is_plugged_in

    @features('UhsConnectionScheme')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_the_device_connected_to_ls_receiver_shall_reconnect_to_host_via_usb_while_cable_is_plugged_in(self):
        """
        While connected to a LS2-Pairing receiver, the device shall reconnect to the host on USB
        as soon as the USB charging cable is plugged in.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is not USB connected')
        # --------------------------------------------------------------------------------------------------------------
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is LS2-pairing receiver connected')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'LS2-pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [False, False, True, False, False])

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection)
        )

        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.check_device_connected(link_status=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)

        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        self.testCaseChecked("FUN_UHS_USB_0006")
    # end def test_the_device_connected_to_ls_receiver_shall_reconnect_to_host_via_usb_while_cable_is_plugged_in

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_the_device_connected_via_usb_shall_reconnect_to_crush_while_cable_is_unplugged(self):
        """
        While connected to a host on USB, the device shall reconnect to Crush
        as soon as the USB charging cable is unplugged.
        """
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'LS2-pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is USB connected')
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, PortConfiguration.CRUSH_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [False, True, True, False, False])

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection)
        )

        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.check_device_connected()

        self.testCaseChecked("FUN_UHS_USB_0007")
    # end def test_the_device_connected_via_usb_shall_reconnect_to_crush_while_cable_is_unplugged

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_the_device_connected_via_usb_shall_reconnect_to_pre_paired_receiver_while_cable_is_unplugged(self):
        """
        While connected to a host on USB, the device shall reconnect to the pre-paired receiver
        as soon as the USB charging cable is unplugged.
        """
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'LS2-pairing receiver paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is USB connected')
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, PortConfiguration.PRE_PAIRED_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [True, False, False, False, False])

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection)
        )

        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.check_device_connected()

        self.testCaseChecked("FUN_UHS_USB_0008")
    # end def test_the_device_connected_via_usb_shall_reconnect_to_pre_paired_receiver_while_cable_is_unplugged

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @features('USBCableSupport')
    @level('Functionality')
    @services('PowerSupply')
    def test_the_device_connected_via_usb_shall_reconnect_to_ls_pairing_receiver_while_calble_is_unplugged(self):
        """
        While connected to a host on USB, the device shall reconnect to the LS2-Pairing receiver
        as soon as the USB charging cable is unplugged.
        """
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'LS2-pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is USB connected')
        # --------------------------------------------------------------------------------------------------------------
        self.device.enable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        Ls2ConnectionSchemeTestUtils.check_device_connection_via_usb_cable(self, PortConfiguration.CABLE_CONNECTED_PORT)

        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, PortConfiguration.LS2_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [False, False, True, False, False])

        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection)
        )

        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)
        self.check_device_connected()

        self.testCaseChecked("FUN_UHS_USB_0009")
    # end def test_the_device_connected_via_usb_shall_reconnect_to_ls_pairing_receiver_while_calble_is_unplugged

# end class UhsUsbTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
