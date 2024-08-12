#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.protocol_switch
:brief: Validate LS2/UHS connection scheme for LS2 / BLE switch test cases
:author: Zane Lu <zlu@logitech.com>
:date: 2024/03/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import ReportReferences
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration
from pytestbox.device.ls2connectionscheme.uhs_connection_scheme import UhsConnectionSchemeBase
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils
from pytransport.ble.bleconstants import BleAdvertisingPduType
from pytransport.ble.blecontext import BleContextDevice
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProtocolSwitchTestCases(UhsConnectionSchemeBase):
    """
    LS2 connection scheme - Protocol Switch Test Cases
    """

    PROTOCOL_LS2 = 1
    PROTOCOL_BLE = 2

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.previous_devices_to_delete_bond = []
        self.ble_context = None
        self.ble_device = None
        self.ble_channel = None

        self.current_protocol = self.PROTOCOL_LS2

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.restart_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get the BLE context")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.ble_channel is not None:
                if self.ble_channel.is_open:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Close BLE channel")
                    # --------------------------------------------------------------------------------------------------
                    self.ble_channel.close()
                # end if
                self.ble_channel = None
            # end if
        # end with

        with self.manage_post_requisite():
            if self.ble_device is not None and self.ble_device.connected:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Disconnect device")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.disconnect_device(test_case=self, ble_context_device=self.ble_device)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.ble_device is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Delete device bond")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.ble_device)
                self.ble_device = None
            # end if
        # end with

        with self.manage_post_requisite():
            for previous_device in self.previous_devices_to_delete_bond:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, f"Delete device bond of {previous_device}")
                # ------------------------------------------------------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=previous_device)
            # end for
        # end with

        super().tearDown()
    # end def tearDown

    def trigger_protocol_change(self, to_protocol, pairing_mode=False, long_press=False):
        """
        Press the connect button to switch the channel

        :param to_protocol: switch to the protocol
        :type to_protocol: ``int``
        :param pairing_mode: Flag indicating if the current channel shall be forced in pairing mode - OPTIONAL
        :type pairing_mode: ``bool``
        :param long_press: Flag indicating to trigger protocol switch by long-press - OPTIONAL
        :type long_press: ``bool``
        """
        assert [pairing_mode, long_press].count(
            True) <= 1, "pairing_mode and long_press shall not be True at the same time"
        self.assertIn(member=to_protocol, container=[self.PROTOCOL_LS2, self.PROTOCOL_BLE],
                      msg="Invalid protocol value.")

        if self.current_protocol == to_protocol:
            return
        # end if

        if self.f.PRODUCT.F_IsMice:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Gaming Mouse: switch to protocol {to_protocol}")
            # ----------------------------------------------------------------------------------------------------------
            self.assertTrue(expr=KEY_ID.CONNECT_BUTTON in self.button_stimuli_emulator.connected_key_ids,
                            msg="No connect button to switch the protocol.")

            if not pairing_mode:
                # Wait connection LED timeout
                sleep(5)
                # Double click connection button to switch to another channel
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON, delay=0.05, repeat=2)
            else:
                # Single click connection button to switch to another channel
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON)
            # end if

            if long_press:
                # Long-press connection button
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON,
                                                       duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
            # end if
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Gaming Keyboard: switch to protocol {to_protocol}")
            # ----------------------------------------------------------------------------------------------------------
            if KEY_ID.LS2_BLE_CONNECTION_TOGGLE in self.button_stimuli_emulator.connected_key_ids:
                if not pairing_mode:
                    # Wait connection LED timeout
                    sleep(5)
                    # Double click connection button to switch to another channel
                    self.button_stimuli_emulator.keystroke(key_id=KEY_ID.LS2_BLE_CONNECTION_TOGGLE,
                                                           delay=0.05, repeat=2)
                else:
                    # Single click connection button to switch to another channel
                    self.button_stimuli_emulator.keystroke(key_id=KEY_ID.LS2_BLE_CONNECTION_TOGGLE)
                # end if

                if long_press:
                    # Long-press connection button
                    self.button_stimuli_emulator.keystroke(key_id=KEY_ID.LS2_BLE_CONNECTION_TOGGLE,
                                                           duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
                # end if
            else:
                if to_protocol == self.PROTOCOL_LS2:
                    self.assertTrue(expr=KEY_ID.LS2_CONNECTION in self.button_stimuli_emulator.connected_key_ids,
                                    msg="No LS2 connection button to switch the protocol.")
                    self.button_stimuli_emulator.keystroke(
                        key_id=KEY_ID.LS2_CONNECTION,
                        duration=ButtonStimuliInterface.LONG_PRESS_DURATION if long_press
                        else ButtonStimuliInterface.DEFAULT_DURATION)
                else:
                    self.assertTrue(expr=KEY_ID.BLE_CONNECTION in self.button_stimuli_emulator.connected_key_ids,
                                    msg="No BLE connection button to switch the protocol.")
                    self.button_stimuli_emulator.keystroke(
                        key_id=KEY_ID.BLE_CONNECTION,
                        duration=ButtonStimuliInterface.LONG_PRESS_DURATION if long_press
                        else ButtonStimuliInterface.DEFAULT_DURATION)
                # end if
            # end if
        # end if
        self.current_protocol = to_protocol
    # end def trigger_protocol_change

    def enter_pairing_mode(self, protocol):
        """
        Long-press the connect button to enter into the pairing mode

        :param protocol: the protocol to enter pairing mode
        :type protocol: ``int``
        """
        self.assertIn(member=protocol, container=[self.PROTOCOL_LS2, self.PROTOCOL_BLE],
                      msg="Invalid protocol value")

        if self.f.PRODUCT.F_IsMice:
            key_id = KEY_ID.CONNECT_BUTTON
        else:
            if KEY_ID.LS2_BLE_CONNECTION_TOGGLE in self.button_stimuli_emulator.connected_key_ids:
                key_id = KEY_ID.LS2_BLE_CONNECTION_TOGGLE
            else:
                key_id = KEY_ID.LS2_CONNECTION if protocol == self.PROTOCOL_LS2 else KEY_ID.BLE_CONNECTION
            # end if
        # end if

        # Long-press connection button
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
    # end def enter_pairing_mode

    def pair_ble_device(self):
        """
        Scan the BLE device and connect the device
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Enter pairing mode")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Scan for BLE device")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self, scan_timeout=2,
                                                                       send_scan_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Connect to BLE device")
        # --------------------------------------------------------------------------------------------------------------
        self.reconnect_ble_device()
    # end def pair_ble_device

    def reconnect_ble_device(self):
        """
        Connect the BLE device and get its notification queue
        """
        # Adding type hint does not add overhead and greatly helps the indexer
        self.ble_device: BleContextDevice

        self.ble_channel = BleProtocolTestUtils.create_new_ble_channel(test_case=self,
                                                                       ble_context_device=self.ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Get the notification queue")
        # --------------------------------------------------------------------------------------------------------------
        if self.f.PRODUCT.F_IsGaming:
            if self.f.PRODUCT.F_IsMice:
                self.ble_notification_queue = (
                    self.get_ble_report_notification_queue(ReportReferences.MOUSE_16BITS_INPUT))
            else:
                self.ble_notification_queue = (
                    self.get_ble_report_notification_queue(ReportReferences.GAMING_KEYBOARD_INPUT))
            # end if
        else:
            if self.f.PRODUCT.F_IsMice:
                self.ble_notification_queue = self.get_ble_report_notification_queue(ReportReferences.MOUSE_INPUT)
            else:
                self.ble_notification_queue = self.get_ble_report_notification_queue(ReportReferences.KEYBOARD_INPUT)
            # end if
        # end if
    # end def reconnect_ble_device

    def get_ble_report_notification_queue(self, report_reference):
        """
        Get the report notification queue from the report reference as a test prerequisite.
        This function will also perform the following steps:
         - Get the whole gatt table
         - Subscribe to all reports

        :param report_reference: The report reference
        :type report_reference: ``HexList``

        :return: the notification queue
        :rtype: ``queue``
        """
        self.gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Get the notification queue for report {report_reference}")
        # --------------------------------------------------------------------------------------------------------------
        characteristic = BleProtocolTestUtils.get_hid_report(
            self, self.gatt_table, self.ble_device, report_reference)
        self.assertNotNone(characteristic, msg="Report not present")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Get the notification queue for report {report_reference}")
        # --------------------------------------------------------------------------------------------------------------
        notification_queue = BleProtocolTestUtils.direct_subscribe_notification(self, self.ble_device, characteristic)
        self.assertNotNone(notification_queue, msg="Report not present")
        return notification_queue
    # end def get_ble_report_notification_queue

    def check_hid_input(
            self, count, ble_notification_queue=None, make_timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
            break_timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT):
        """
        Check if the number of notifications received in a queue is correct

        :param count: the amount of notification to expect
        :type count: ``int``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        :param make_timeout: The waiting time before receiving the make report - OPTIONAL
        :type make_timeout: ``int``
        :param break_timeout: The waiting time before receiving the break report - OPTIONAL
        :type break_timeout: ``int``
        """
        if ble_notification_queue is None:
            for _ in range(count):
                # Retrieve the HID make report
                ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=make_timeout)
                # Retrieve the HID release report
                ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=break_timeout)
            # end for
        else:
            for _ in range(count):
                # Retrieve the HID make report
                # noinspection PyUnresolvedReferences
                ble_notification_queue.get(timeout=make_timeout)
                # Retrieve the HID release report
                # noinspection PyUnresolvedReferences
                ble_notification_queue.get(timeout=break_timeout)
            # end for
        # end if
    # end def check_hid_input

    def prerequisite_device_pairing(self, pair_ble, pair_ls_order, port_settings):
        """
        Prerequisite for device pairing including BLE, pre-paired receiver, crush receiver and ls2-pairing receiver.
        Set the power of USB ports

        :param pair_ble: The flag to indicate the need to pair the device via BLE channel
        :type pair_ble: ``bool``
        :param pair_ls_order: The list to indicate the orders to pair the device via LS2 channels
        :type pair_ls_order: ``list``
        :param port_settings: The list to indicate the power status of USB hub ports
        :type port_settings: ``list``
        """
        if pair_ble:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Pair BLE device')
            # ----------------------------------------------------------------------------------------------------------
            self.pair_ble_device()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'switch back to LS2 channel')
            # ----------------------------------------------------------------------------------------------------------
            self.trigger_protocol_change(to_protocol=self.PROTOCOL_LS2)
        # end if

        for port_index in pair_ls_order:
            if port_index == PortConfiguration.CRUSH_RECEIVER_PORT:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_prerequisite(self, 'Pair crush')
                # ------------------------------------------------------------------------------------------------------
                self.pair_crush_receiver()
            elif port_index == PortConfiguration.LS2_RECEIVER_PORT:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_prerequisite(self, 'Pair ls2 receiver')
                # ------------------------------------------------------------------------------------------------------
                self.pair_ls2_receiver()
            elif port_index == PortConfiguration.PRE_PAIRED_RECEIVER_PORT:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_prerequisite(self, 'Connect to the pre-paired receiver')
                # ------------------------------------------------------------------------------------------------------
                self.connect_to_the_pre_paired_receiver()
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Set the power of the usb ports')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(test_case=self, desired=port_settings)
    # end def prerequisite_device_pairing

    def verify_ble_reconnection(self):
        """
        Verify the BLE channel reconnection
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'short key pressed on the connect button')
        # --------------------------------------------------------------------------------------------------------------
        # switch to BLE channel
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the advertising type')
        # --------------------------------------------------------------------------------------------------------------
        ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self, scan_timeout=2,
                                                                  send_scan_request=True)
        self.assertEqual(
            obtained=ble_device.advertising_type,
            expected=BleAdvertisingPduType.CONNECTABLE_DIRECTED,
            msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_DIRECTED.name}. "
                f"Got {ble_device.advertising_type}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the connection to the BLE slot')
        # --------------------------------------------------------------------------------------------------------------
        self.reconnect_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the HID event')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        self.check_hid_input(count=1, ble_notification_queue=self.ble_notification_queue)
    # end def verify_ble_reconnection

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_connection_from_crush_to_ble_reconnection(self):
        """
        While connected to Crush in LS2, the device shall move to BLE reconnection
        when the user does a short key press on the connect or the Bluetooth button and BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'Crush paired and powered on and connected')
        LogHelper.log_info(self, 'Pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.CRUSH_RECEIVER_PORT],
                                         port_settings=[True, True, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_reconnection()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0001")
    # end def test_connection_from_crush_to_ble_reconnection

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_connection_from_pre_paired_receiver_to_ble_reconnection(self):
        """
        While connected to the pre-paired receiver in LS2, the device shall move to BLE reconnection
        when the user does a short key press on the connect or the Bluetooth button and the BLE channel is paired
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'Pre-paired receiver powered on and connected')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.PRE_PAIRED_RECEIVER_PORT],
                                         port_settings=[True, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_reconnection()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0002")
    # end def test_connection_from_pre_paired_receiver_to_ble_reconnection

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_connection_from_ls2_pairing_receiver_to_ble_reconnection(self):
        """
        While connected to the LS2-Pairing receiver in LS2, the device shall move to BLE reconnection
        when the user does a short key press on the connect or the Bluetooth button and the BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on and connected')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_reconnection()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0003")
    # end def test_connection_from_ls2_pairing_receiver_to_ble_reconnection

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_connection_from_ls2_pairing_sequence_to_ble_reconnection(self):
        """
        While in the middle of an LS2 pairing sequence, the device shall move to BLE reconnection
        when the user does a short key press on the connect or the Bluetooth button and the BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on and connected')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "In the middle of a LS2 Pairing sequence")
        # --------------------------------------------------------------------------------------------------------------
        # go into LS2 pairing mode
        self.enter_pairing_mode(protocol=self.PROTOCOL_LS2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_reconnection()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0004")
    # end def test_connection_from_ls2_pairing_sequence_to_ble_reconnection

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @features('LS2WakeUpByConnectButton')
    @level('Functionality')
    def test_connection_from_deep_sleep_mode_to_ble_reconnection(self):
        """
        After entering deep sleep from LS2 Connected state, the device shall move to BLE reconnection
        when the user does a short key press on the connect or the Bluetooth button and the BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on and connected')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enter deep sleep mode from LS2 connected state")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.wait_for_deep_sleep_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE reconnection')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_reconnection()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0005")
    # end def test_connection_from_deep_sleep_mode_to_ble_reconnection

    def verify_ble_pairing_with_ble_unpaired(self):
        """
        Verify the BLE channel pairing for unpaired BLE channel
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'short key pressed on the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the advertising type')
        # --------------------------------------------------------------------------------------------------------------
        ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self, scan_timeout=2,
                                                                  send_scan_request=True)
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no HID event')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)
    # end def verify_ble_pairing_with_ble_unpaired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_connection_from_crush_to_ble_pairing_with_ble_unpaired(self):
        """
        While connected to Crush in LS2, the device shall move to BLE pairing
        when the user does a short key press on the connect or the Bluetooth button and BLE channel is unpaired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'Crush paired and powered on and connected')
        LogHelper.log_info(self, 'Pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=False,
                                         pair_ls_order=[PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.CRUSH_RECEIVER_PORT],
                                         port_settings=[True, True, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE pairing')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_pairing_with_ble_unpaired()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0006")
    # end def test_connection_from_crush_to_ble_pairing_with_ble_unpaired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_connection_from_pre_paired_reciever_to_ble_pairing_with_ble_unpaired(self):
        """
        While connected to the pre-paired receiver in LS2, the device shall move to BLE pairing
        when the user does a short key press on the connect or the Bluetooth button and the BLE channel is unpaired
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'Pre-paired receiver powered on and connected')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=False,
                                         pair_ls_order=[PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.PRE_PAIRED_RECEIVER_PORT],
                                         port_settings=[True, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE pairing')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_pairing_with_ble_unpaired()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0007")
    # end def test_connection_from_pre_paired_reciever_to_ble_pairing_with_ble_unpaired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_connection_from_ls2_pairing_receiver_to_ble_pairing_with_ble_unpaired(self):
        """
        While connected to the LS2-Pairing receiver in LS2, the device shall move to BLE pairing
        when the user does a short key press on the connect or the Bluetooth button and the BLE channel is unpaired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on and connected')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=False,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE pairing')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_pairing_with_ble_unpaired()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0008")
    # end def test_connection_from_ls2_pairing_receiver_to_ble_pairing_with_ble_unpaired

    def verify_ble_pairing_with_ble_paired(self):
        """
        Verify the BLE channel pairing for BLE channel already paired
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get the target BLE address")
        # --------------------------------------------------------------------------------------------------------------
        target_ble_address = BleProtocolTestUtils.increment_address(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Enter BLE pairing mode")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.start_scan_for_devices(
            test_case=self, ble_addresses=[target_ble_address],
            scan_timeout=15, send_scan_request=True)

        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE, long_press=True)

        ble_devices = BleProtocolTestUtils.get_scanning_result(test_case=self, timeout=10)
        self.assertTrue(expr=len(ble_devices) > 0, msg=f"Could not find the device with param: {[target_ble_address]}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the advertising type')
        # --------------------------------------------------------------------------------------------------------------
        ble_device = ble_devices[0]
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no HID event')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)
    # end def verify_ble_pairing_with_ble_paired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_connection_long_press_from_crush_to_ble_pairing_with_ble_paired(self):
        """
        While connected to Crush in LS2, the device shall move to BLE pairing
        when the user does a long key press on the connect or the Bluetooth button and the BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'Crush paired and powered on and connected')
        LogHelper.log_info(self, 'Pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.CRUSH_RECEIVER_PORT],
                                         port_settings=[True, True, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE pairing')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_pairing_with_ble_paired()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0009")
    # end def test_connection_long_press_from_crush_to_ble_pairing_with_ble_paired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_connection_long_press_from_pre_paired_receiver_to_ble_pairing_with_ble_paired(self):
        """
        While connected to the pre-paired receiver in LS2, the device shall move to BLE pairing
        when the user does a long key press on the connect or the Bluetooth button and the BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'Pre-paired receiver powered on and connected')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.PRE_PAIRED_RECEIVER_PORT],
                                         port_settings=[True, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE pairing')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_pairing_with_ble_paired()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0010")
    # end def test_connection_long_press_from_pre_paired_receiver_to_ble_pairing_with_ble_paired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_connection_long_press_from_ls2_pairing_receiver_to_ble_pairing_with_ble_paired(self):
        """
        While connected to the LS2-Pairing receiver in LS2, the device shall move to BLE pairing
        when the user does a long key press on the connect or the Bluetooth button and the BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on and connected')
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'Pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE pairing')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_pairing_with_ble_paired()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0011")
    # end def test_connection_long_press_from_ls2_pairing_receiver_to_ble_pairing_with_ble_paired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_connection_long_press_from_crush_to_ble_pairing_with_ble_unpaired(self):
        """
        While connected to Crush in LS2, the device shall move to BLE pairing
        when the user does a long key press on the connect or the Bluetooth button and the BLE channel is unpaired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host unpaired')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'Crush paired and powered on and connected')
        LogHelper.log_info(self, 'Pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=False,
                                         pair_ls_order=[PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.CRUSH_RECEIVER_PORT],
                                         port_settings=[True, True, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Long-press the connect button")
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE, long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Scan for BLE device")
        # --------------------------------------------------------------------------------------------------------------
        ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self, scan_timeout=2,
                                                                  send_scan_request=True)
        self.assertEqual(obtained=ble_device.advertising_type,
                         expected=BleAdvertisingPduType.CONNECTABLE_UNDIRECTED,
                         msg=f"Advertising should be {BleAdvertisingPduType.CONNECTABLE_UNDIRECTED.name}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no HID event')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0012")
    # end def test_connection_long_press_from_crush_to_ble_pairing_with_ble_unpaired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_connection_long_press_from_ls2_pairing_sequence_to_ble_pairing_with_ble_paired(self):
        """
        While in the middle of the LS2 pairing sequence, the device shall move to BLE pairing
        when the user does a long key press on the connect or the Bluetooth button and the BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'Pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "In the middle of a LS2 Pairing sequence")
        # --------------------------------------------------------------------------------------------------------------
        # go into LS2 pairing mode
        self.enter_pairing_mode(protocol=self.PROTOCOL_LS2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE pairing')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_pairing_with_ble_paired()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0013")
    # end def test_connection_long_press_from_ls2_pairing_sequence_to_ble_pairing_with_ble_paired

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @features('LS2WakeUpByConnectButton')
    @level('Functionality')
    def test_connection_long_press_from_deep_sleep_mode_to_ble_pairing_with_ble_paired(self):
        """
        After entering deep sleep mode from LS2 Connected state, the device shall move to BLE pairing
        when the user does a long key press on the connect or the Bluetooth button and the BLE channel is paired.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on and connected')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enter deep sleep mode from LS2 connected state")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.wait_for_deep_sleep_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify BLE pairing')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ble_pairing_with_ble_paired()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0014")
    # end def test_connection_long_press_from_deep_sleep_mode_to_ble_pairing_with_ble_paired

    def verify_ls2_reconnection(self, target_port):
        """
        Verify LS2 reconnection from BLE to LS2 channel

        :param target_port: the port index to verify
        :type target_port: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Switch protocol to BLE')
        # --------------------------------------------------------------------------------------------------------------
        # switch to BLE channel
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE)
        self.reconnect_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Switch channel to target LS2 receiver index {target_port}')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, target_port)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'short key pressed on the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_LS2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connected')
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def verify_ls2_reconnection

    @features('LS2ProtocolSwitch')
    @features('Ls2ConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_ls2_connection_from_ble_to_crush_reconnection(self):
        """
        While connected in BLE, the device shall move to LS2 reconnection and connect to Crush
        when the user does a short key press on the connect or the Lightspeed button and LS2 channel is not in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[True, True, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_reconnection(target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0015_LS2")
    # end def test_ls2_connection_from_ble_to_crush_reconnection

    @features('LS2ProtocolSwitch')
    @features('UhsConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_uhs_connection_from_ble_to_crush_reconnection(self):
        """
        While connected in BLE, the device shall move to UHS reconnection and connect to Crush
        when the user does a short key press on the connect or the Lightspeed button and LS2 channel is not in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, True, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_reconnection(target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0015_UHS")
    # end def test_uhs_connection_from_ble_to_crush_reconnection

    @features('LS2ProtocolSwitch')
    @features('Ls2ConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_ls2_connection_from_ble_to_pre_paired_receiver_reconnection(self):
        """
        While connected in BLE, the device shall move to LS2 reconnection and connect to pre-paired receiver
        when the user does a short key press on the connect or the Lightspeed button and the LS2 channel is not in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.PRE_PAIRED_RECEIVER_PORT],
                                         port_settings=[True, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_reconnection(target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0016_LS2")
    # end def test_ls2_connection_from_ble_to_pre_paired_receiver_reconnection

    @features('LS2ProtocolSwitch')
    @features('UhsConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_uhs_connection_from_ble_to_pre_paired_receiver_reconnection(self):
        """
        While connected in BLE, the device shall move to LS2 reconnection and connect to pre-paired receiver
        when the user does a short key press on the connect or the Lightspeed button and the LS2 channel is not in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.PRE_PAIRED_RECEIVER_PORT],
                                         port_settings=[True, True, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_reconnection(target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0016_UHS")
    # end def test_uhs_connection_from_ble_to_pre_paired_receiver_reconnection

    @features('LS2ProtocolSwitch')
    @features('Ls2ConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_ls2_connection_from_ble_to_ls2_pairing_receiver_reconnection(self):
        """
        While connected in BLE, the device shall move to LS2 reconnection and connect to LS2-Pairing receiver
        when the user does a short key press on the connect or the Lightspeed button and the LS2 channel is not in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_reconnection(target_port=PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0017_LS2")
    # end def test_ls2_connection_from_ble_to_ls2_pairing_receiver_reconnection

    @features('LS2ProtocolSwitch')
    @features('UhsConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_uhs_connection_from_ble_to_ls2_pairing_receiver_reconnection(self):
        """
        While connected in BLE, the device shall move to LS2 reconnection and connect to LS2-Pairing receiver
        when the user does a short key press on the connect or the Lightspeed button and the LS2 channel is not in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_reconnection(target_port=PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0017_UHS")
    # end def test_uhs_connection_from_ble_to_ls2_pairing_receiver_reconnection

    def verify_ls2_oob_connection(self, target_port):
        """
        Verify LS2 pairing in OOB when doing protocol switch from BLE to LS2 channel

        :param target_port: the port index to verify
        :type target_port: ``int``
        """
        self.assertIn(member=target_port,
                      container=[PortConfiguration.PRE_PAIRED_RECEIVER_PORT,
                                 PortConfiguration.CRUSH_RECEIVER_PORT,
                                 PortConfiguration.LS2_RECEIVER_PORT],
                      msg="Invalid target port")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Set device OOB')
        # --------------------------------------------------------------------------------------------------------------
        new_channel = DeviceManagerUtils.get_channel(
            test_case=self,
            channel_id=ChannelIdentifier(port_index=PortConfiguration.PRE_PAIRED_RECEIVER_PORT, device_index=1))
        DeviceManagerUtils.set_channel(test_case=self, new_channel=new_channel)
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=self)
        self.power_supply_emulator.turn_off()

        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(test_case=self, desired=[False, False, False, False, False])
        self.power_supply_emulator.turn_on()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Pair BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ble_device()
        self.button_stimuli_emulator.user_action()
        self.check_hid_input(count=1, ble_notification_queue=self.ble_notification_queue)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Set the USB port power for the target receiver index {target_port}')
        # --------------------------------------------------------------------------------------------------------------
        if target_port == PortConfiguration.PRE_PAIRED_RECEIVER_PORT:
            Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, PortConfiguration.PRE_PAIRED_RECEIVER_PORT)
            Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(test_case=self,
                                                                desired=[True, False, False, False, False])
        elif target_port == PortConfiguration.CRUSH_RECEIVER_PORT:
            Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, receiver_usb_port=target_port)
            Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(test_case=self,
                                                                desired=[False, True, False, False, False])
        else:
            Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, receiver_usb_port=target_port)
            Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(
                self, receiver_usb_port=target_port,
                connect_devices=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)
            Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(test_case=self,
                                                                desired=[False, False, True, False, False])
        # end if

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        self.trigger_protocol_change(to_protocol=self.PROTOCOL_LS2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the device connected')
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def verify_ls2_oob_connection

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Business')
    def test_connection_oob_from_ble_to_crush(self):
        """
        While connected in BLE, the device shall move to LS2 OOB and connect to Crush
        when the user does a short key press on the connect or the Lightspeed button and LS2 channel is in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush never paired and powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Crush is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_oob_connection(target_port=PortConfiguration.CRUSH_RECEIVER_PORT)
        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0018")
    # end def test_connection_oob_from_ble_to_crush

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @level('Business')
    def test_ls2_connection_oob_from_ble_to_pre_paired_receiver(self):
        """
        While connected in BLE, the device shall move to LS2 OOB and connect to pre-paired receiver
        when the user does a short key press on the connect or the Lightspeed button and LS2 channel is in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Pre-paired receiver is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_oob_connection(target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)
        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0019")
    # end def test_ls2_connection_oob_from_ble_to_pre_paired_receiver

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @level('Business')
    def test_ls2_connection_oob_from_ble_to_ls2_pairing_receiver(self):
        """
        While connected in BLE, the device shall move to LS2 OOB and connect to LS2-Pairing receiver
        when the user does a short key press on the connect or the Lightspeed button and LS2 channel is in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired')
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Pre-paired receiver is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_oob_connection(target_port=PortConfiguration.LS2_RECEIVER_PORT)
        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0020")
    # end def test_ls2_connection_oob_from_ble_to_ls2_pairing_receiver

    def verify_ls2_connection_from_ble_deep_sleep_to_crush(self):
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Switch to BLE channel')
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Reconnect BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.reconnect_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Disconnect BLE device and wait device to deep sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.disconnect_device(test_case=self, ble_context_device=self.ble_device)
        sleep(10)  # Wait time to go to deep sleep mode

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch to LS2 channel by short press connect button')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, PortConfiguration.CRUSH_RECEIVER_PORT)
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_LS2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Crush is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def verify_ls2_connection_from_ble_deep_sleep_to_crush

    @features('LS2ProtocolSwitch')
    @features('Ls2ConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_ls2_connection_from_ble_deep_sleep_to_crush(self):
        """
        After entering deep sleep mode from BLE Connected,
        the device shall move to LS2 reconnection and connect to Crush
        when the user does a short key press on the connect or the Lightspeed button
        and the LS2 channel is not in OOB state.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired and connected')
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT,
                                                        PortConfiguration.PRE_PAIRED_RECEIVER_PORT],
                                         port_settings=[True, True, True, False, False])
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Crush is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_connection_from_ble_deep_sleep_to_crush()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0021_LS2")
    # end def test_ls2_connection_from_ble_deep_sleep_to_crush

    @features('LS2ProtocolSwitch')
    @features('UhsConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_uhs_connection_from_ble_deep_sleep_to_crush(self):
        """
        After entering deep sleep mode from BLE Connected,
        the device shall move to LS2 reconnection and connect to Crush
        when the user does a short key press on the connect or the Lightspeed button
        and the LS2 channel is not in OOB state.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired and connected')
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, True, True, False, False])
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Crush is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_connection_from_ble_deep_sleep_to_crush()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0021_UHS")
    # end def test_uhs_connection_from_ble_deep_sleep_to_crush

    @features('LS2ProtocolSwitch')
    @features('Ls2ConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_ls2_connection_oob_from_ble_deep_sleep_to_crush(self):
        """
        After entering deep sleep mode from BLE Connected,
        the device shall move to LS2 OOB and connect to Crush
        when the user does a short key press on the connect or the Lightspeed button
        and the LS2 channel is in OOB state.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired and connected')
        LogHelper.log_info(self, 'Crush never paired and powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[],
                                         port_settings=[True, True, False, False, False])

        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self,
                                                           receiver_usb_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Crush is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_connection_from_ble_deep_sleep_to_crush()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0022_LS2")
    # end def test_ls2_connection_oob_from_ble_deep_sleep_to_crush

    @features('LS2ProtocolSwitch')
    @features('UhsConnectionScheme')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_uhs_connection_oob_from_ble_deep_sleep_to_crush(self):
        """
        After entering deep sleep mode from BLE Connected,
        the device shall move to LS2 OOB and connect to Crush
        when the user does a short key press on the connect or the Lightspeed button
        and the LS2 channel is in OOB state.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired and connected')
        LogHelper.log_info(self, 'Crush never paired and powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[],
                                         port_settings=[False, True, False, False, False])

        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self,
                                                           receiver_usb_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Crush is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_ls2_connection_from_ble_deep_sleep_to_crush()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0022_UHS")
    # end def test_uhs_connection_oob_from_ble_deep_sleep_to_crush

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @features('ThreePairingSlots')
    @level('Functionality')
    def test_ls2_reconnection_from_ble_pairing_to_ls2_pairing_receiver(self):
        """
        While pairing mode in BLE, the device shall move to LS2 reconnection and connect to LS2-Pairing receiver
        when the user does a short key press on the connect or the Lightspeed button and the LS2 channel is not in OOB.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired and connected')
        LogHelper.log_info(self, 'Crush paired but powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[PortConfiguration.CRUSH_RECEIVER_PORT,
                                                        PortConfiguration.LS2_RECEIVER_PORT],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Switch to BLE protocol and connect BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE)
        self.reconnect_ble_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enter BLE pairing mode')
        # --------------------------------------------------------------------------------------------------------------
        self.enter_pairing_mode(protocol=self.PROTOCOL_BLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch to LS2 protocol')
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_LS2, pairing_mode=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'LS2-pairing receiver is connected')
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0023")
    # end def test_ls2_reconnection_from_ble_pairing_to_ls2_pairing_receiver

    @features('LS2ProtocolSwitch')
    @features('GamingDevice')
    @level('Functionality')
    def test_go_to_ls2_pairing_mode_from_ble(self):
        """
        While connected in BLE, the device shall move to LS2 pairing
        when the user does a long press on the Lightspeed button whatever the channel state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'BLE host paired and connected')
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.prerequisite_device_pairing(pair_ble=True,
                                         pair_ls_order=[],
                                         port_settings=[False, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Switch to BLE protocol and connect BLE device')
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_BLE)
        self.reconnect_ble_device()

        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)
        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Switch to LS2 protocol by long press the connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.trigger_protocol_change(to_protocol=self.PROTOCOL_LS2, long_press=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Device is in pairing mode and connect to LS2-pairing receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()

        self.testCaseChecked("BUS_PROTOCOL_SWITCH_0024")
    # end def test_go_to_ls2_pairing_mode_from_ble

# end class ProtocolSwitchTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
