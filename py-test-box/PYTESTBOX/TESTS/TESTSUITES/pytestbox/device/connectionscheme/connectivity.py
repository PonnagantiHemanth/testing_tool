#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.connectivity
:brief: Validate BLE Pro Connectivity flowcharts (BLE Connection Scheme feature)
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/08/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import perf_counter
from time import sleep

from pychannel.usbchannel import UsbReceiverChannel
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import CONNECTIVITY_STATUS_LEDS
from pylibrary.emulator.ledid import LED_ID
from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.connectionscheme.safeprepairedreceiver import ConnectionSchemeTestCaseMixin
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConnectivityTestCase(ConnectionSchemeTestCaseMixin):
    """
    Device BLE Pro Connectivity TestCases
    """
    ONE_SECOND = 1
    THREE_SECONDS = 3
    FIVE_SECONDS = 5
    SIX_SECONDS = 6
    TEN_SECONDS = 10
    TWENTY_SECONDS = 20

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_program_nvs = False
        self.post_requisite_power_on_usb_port = False
        self.post_requisite_unpair_all = False

        super().setUp()

        self.receiver_port_index = ChannelUtils.get_port_index(test_case=self)

        # Cleanup all receiver pairing slots except the first one
        DevicePairingTestUtils.NvsManager.clean_pairing_data(self)

        # Enable HID notification
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Stop LEDs monitoring')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(
                self, led_identifiers=CONNECTIVITY_STATUS_LEDS, build_timeline=False)
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_program_nvs and self.memory_manager is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_power_on_usb_port:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Turn on the initial receiver')
                # ------------------------------------------------------------------------------------------------------
                self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Switch the communication back to the initial receiver')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.change_host_by_link_state(self, DeviceConnection.LinkStatus.LINK_ESTABLISHED)
        # end with

        with self.manage_post_requisite():
            if self.gotthard_receiver_port_index is not None:
                # Remove all channels related to the gotthard receiver
                DeviceManagerUtils.remove_channel_from_cache(
                    test_case=self, port_index=self.gotthard_receiver_port_index)
            # end if
        # end with

        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Clean WirelessDeviceStatusBroadcastEvent messages")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Clean Battery Status messages")
            # ----------------------------------------------------------------------------------------------------------
            self.cleanup_battery_event_from_queue()
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_unpair_all:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Cleanup receiver pairing slots")
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.unpair_all(self)
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    @features('BLEProConnectionScheme')
    @level('Business')
    def test_power_on_pairing_mode_from_oob_state(self):
        """
        At power on, the device shall enter pairing mode in CH1 if it's in OOB state (no ConnectId chunk in NVS)
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in OOB state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.invalidate_connect_id_chunks(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        sleep(ConnectivityTestCase.ONE_SECOND)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.FAST_BLINKING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Verify Led1State is Fast blinking for at least 3s then Steady for 5s then Off")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0001#1")
    # end def test_power_on_pairing_mode_from_oob_state

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH1)
    @features('ConnectButton')
    @level('Functionality')
    @services('Debugger')
    def test_short_press_power_on_pairing_mode_from_oob_state(self):
        """
        At power on, the device shall enter pairing mode in CH1 if it's in OOB state
        While the user could switch from one channel to another by doing a short press on the connect button,
        the firmware shall detect the OOB state at the next power off/on.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in OOB state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.invalidate_connect_id_chunks(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode on CH2 with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)
        # Let some time for the device to process the short press
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        # Connectivity LED 1 shall be off for at least 1 second
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0001#2")
    # end def test_short_press_power_on_pairing_mode_from_oob_state

    @features('BLEProConnectionScheme')
    @level('Business', 'SmokeTests')
    def test_connected_pairing_mode_from_long_press(self):
        """
        While connected to a receiver, the device shall enter pairing mode in CH1 if the user do a long press on the
        connect button or easy switch CH1 button.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the CH1 button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.FAST_BLINKING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0002")
    # end def test_connected_pairing_mode_from_long_press

    @features('BLEProConnectionScheme')
    @level('Functionality')
    def test_power_on_pairing_mode_from_slot_ch1_unpaired(self):
        """
        At power on, the device shall enter pairing mode in CH1 if the ConnectId chunk refers to CH1 and this slot is
        unpaired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device first pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0003")
    # end def test_power_on_pairing_mode_from_slot_ch1_unpaired

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_power_on_pairing_mode_from_slot_ch2_unpaired(self):
        """
        [Multiple Channels] At power on, the device shall enter pairing mode in CH2 if the ConnectId chunk refers to
        CH2 and this slot is unpaired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device second pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0004")
    # end def test_power_on_pairing_mode_from_slot_ch2_unpaired

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    def test_power_on_pairing_mode_from_slot_ch3_unpaired(self):
        """
        [Multiple Channels] At power on, the device shall enter pairing mode in CH3 if the ConnectId chunk refers to
        CH3 and this channel is unpaired.
        While in pairing mode in CH3, the device shall finish in 'Connected' state in CH3 if the user performs the
        pairing sequence successfully.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)
        host_index = 2

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device third pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0005")
    # end def test_power_on_pairing_mode_from_slot_ch3_unpaired

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('ConnectButton')
    @level('Functionality')
    def test_connected_pairing_mode_ch2_from_long_press(self):
        """
        [Multiple Channels] [Connect Button] While connected to a receiver on CH2, the device shall enter pairing mode
        on the same channel if the user do a long press on the Connect button.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        # Check index = CH2 in NVS Connect Id chunk
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        # Let Connectivity LED 2 switch off
        sleep(ConnectivityTestCase.THREE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        # Connectivity LED 2 shall be off for at least 1 second
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, state=SchemeType.FAST_BLINKING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0006")
    # end def test_connected_pairing_mode_ch2_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('ConnectButton')
    @level('Functionality')
    def test_connected_pairing_mode_ch3_from_long_press(self):
        """
        [Multiple Channels] [Connect Button] While connected to a receiver on CH3, the device shall enter pairing mode
        on the same channel if the user do a long press on the Connect button.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        # Check index = CH3 in NVS Connect Id chunk
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        # Let Connectivity LED 3 switch off
        sleep(ConnectivityTestCase.THREE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        # Connectivity LED 3 shall be off for at least 1 second
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, state=SchemeType.FAST_BLINKING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0007")
    # end def test_connected_pairing_mode_ch3_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH1)
    @level('Functionality')
    def test_pairing_mode_ch1_long_press_ignored(self):
        """
        [Multiple Channels] While the device is in pairing mode on CH1, a long press on the Connect or the same H1
        EasySwitch button is ignored.
        """
        self.post_requisite_program_nvs = True
        host_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH1 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a pairing sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a long press on the Connect or H1 EasySwitch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0008")
    # end def test_pairing_mode_ch1_long_press_ignored

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @level('Functionality')
    @bugtracker("Pairing_Mode_Long_Press_Timeout_Reset")
    def test_pairing_mode_ch1_long_press_no_timeout_reset(self):
        """
        [Multiple Channels] While the device is in pairing mode on CH1, a long press on the Connect or the same H1
        EasySwitch button doesn't reset the pairing timeout.
        """
        self.post_requisite_program_nvs = True
        host_index = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH1 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {ConnectivityTestCase.TWENTY_SECONDS} seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.TWENTY_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a long press on the Connect or H1 EasySwitch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.FIVE_SECONDS)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Wait for another 5s where the LED1 shall be off')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for exactly 3 minutes then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0008#2")
    # end def test_pairing_mode_ch1_long_press_no_timeout_reset

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_pairing_mode_ch2_long_press_ignored(self):
        """
        [Multiple Channels] While the device is in pairing mode on CH2, a long press on the Connect or the same H2
        EasySwitch button is ignored.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a pairing sequence on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a long press on the Connect or H2 EasySwitch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0009#1")
    # end def test_pairing_mode_ch2_long_press_ignored

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @bugtracker("Pairing_Mode_Long_Press_Timeout_Reset")
    def test_pairing_mode_ch2_long_press_no_timeout_reset(self):
        """
        [Multiple Channels] While the device is in pairing mode on CH2, a long press on the Connect or the same H2
        EasySwitch button doesn't reset the pairing timeout.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for {ConnectivityTestCase.TWENTY_SECONDS} seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.TWENTY_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a long press on the Connect or H2 EasySwitch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.FIVE_SECONDS)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Wait another 5s to verify the LED2 goes off')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for exactly 3 minutes then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0009#2")
    # end def test_pairing_mode_ch2_long_press_no_timeout_reset

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('ConnectButton')
    @level('Functionality')
    def test_pairing_mode_ch3_long_press_ignored(self):
        """
        [Multiple Channels] While the device is in pairing mode on CH3, a long press on the Connect or the same H3
        EasySwitch button is ignored, the pairing timeout is not reset and the device shall stay in pairing mode
        in the same channel.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a pairing sequence on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a long press on the Connect or H3 EasySwitch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0009#3")
    # end def test_pairing_mode_ch3_long_press_ignored

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('ConnectButton')
    @level('Functionality')
    def test_disconnected_pairing_mode_ch1_from_short_press(self):
        """
        [Multiple Channels] While connected to a receiver on the last supported channel (i.e. CH3 or CH2 depending on
        the number of host supported by the device), the device shall enter pairing mode in CH1 if the user do a
        short press on the Connect button or the EasySwitch CH1 button and this slot is unpaired.
        """
        self.post_requisite_program_nvs = True
        host_index = self.f.PRODUCT.DEVICE.F_NbHosts - 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH1 and CH3 pairing channels in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0010")
    # end def test_disconnected_pairing_mode_ch1_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('ConnectButton')
    @level('Functionality')
    def test_connected_pairing_mode_ch2_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While connected to a receiver on CH1, the device shall enter pairing mode
        in CH2 if the user do a short press on the Connect button and this slot is unpaired.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0011")
    # end def test_connected_pairing_mode_ch2_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('ConnectButton')
    @level('Functionality')
    def test_connected_pairing_mode_ch3_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While connected to a receiver on CH2, the device shall enter pairing mode
        in CH3 if the user do a short press on the Connect button and this slot is unpaired.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        # Check index = CH2 in NVS Connect Id chunk
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 2
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0012")
    # end def test_connected_pairing_mode_ch3_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('ConnectButton')
    @level('Functionality')
    def test_pairing_ch3_pairing_mode_ch1_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode on the last supported channel (i.e. CH3 or CH2
        depending on the number of host supported by the device), the device shall enter pairing mode in CH1
        if the user does a short press on the Connect button and this channel is unpaired.
        """
        self.post_requisite_program_nvs = True
        host_index = self.f.PRODUCT.DEVICE.F_NbHosts - 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH1 and CH3 pairing channels in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0013")
    # end def test_pairing_ch3_pairing_mode_ch1_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('ConnectButton')
    @level('Functionality')
    def test_pairing_ch1_pairing_mode_ch2_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode on CH1, the device shall enter pairing mode in CH2
        if the user does a short press on the Connect button and this channel is unpaired.
        """
        self.post_requisite_program_nvs = True
        host_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH1 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0014")
    # end def test_pairing_ch1_pairing_mode_ch2_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('ConnectButton')
    @level('Functionality')
    def test_pairing_ch2_pairing_mode_ch3_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While connected to a receiver on CH2, the device shall enter pairing mode
        in CH3 if the user do a short press on the Connect button and this slot is unpaired.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 2
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0015")
    # end def test_pairing_ch2_pairing_mode_ch3_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('Debugger')
    def test_power_on_reconnection_to_ch1(self):
        """
        [Multiple Channels] At power on, the device shall enter reconnection mode in CH1 if the ConnectId chunk
        refers to CH1 and this slot is paired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH1 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Change Host to CH2')
        # --------------------------------------------------------------------------------------------------------------
        if self.f.PRODUCT.DEVICE.CONNECTION_SCHEME.F_MultipleEasySwitchButtons:
            self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)
        else:
            self.button_stimuli_emulator.change_host(host_index=HOST.CH2)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        # Connectivity LED 1 shall be off for at least 1 second
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Steady for exactly 5s then off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0029")
    # end def test_power_on_reconnection_to_ch1

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('Debugger')
    def test_power_on_reconnection_to_ch2(self):
        """
        [Multiple Channels] At power on, the device shall enter reconnection mode in CH2 if the ConnectId chunk
        refers to CH2 and this slot is paired.
        Note that CH1 pairing data shall be deleted to execute the test on a device supporting only 2 hosts!
        """
        self.post_requisite_program_nvs = True
        self.post_requisite_unpair_all = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force all device pairing channels in unpaired state if device supports only '
                                         '2 hosts else force only the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        oob = True if self.f.PRODUCT.DEVICE.F_NbHosts == 2 else False
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=oob)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        # Check index = CH2 in NVS Connect Id chunk
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        new_host_index = HOST.CH1 if self.f.PRODUCT.DEVICE.F_NbHosts == 2 else HOST.CH3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Change Host to CH{new_host_index}')
        # --------------------------------------------------------------------------------------------------------------
        if self.f.PRODUCT.DEVICE.CONNECTION_SCHEME.F_MultipleEasySwitchButtons:
            self.button_stimuli_emulator.enter_pairing_mode(host_index=new_host_index)
        else:
            self.button_stimuli_emulator.change_host(host_index=new_host_index)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        # Connectivity LED 2 shall be off for at least 1 second
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Steady for exactly 5s then off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0030")
    # end def test_power_on_reconnection_to_ch2

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    @services('Debugger')
    def test_power_on_reconnection_to_ch3(self):
        """
        [Multiple Channels] At power on, the device shall enter reconnection mode in CH3 if the ConnectId chunk
        refers to CH3 and this slot is paired.
        """
        self.post_requisite_program_nvs = True
        self.post_requisite_unpair_all = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        # Check index = CH3 in NVS Connect Id chunk
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Change Host to CH1 with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        if self.f.PRODUCT.DEVICE.CONNECTION_SCHEME.F_MultipleEasySwitchButtons:
            self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)
        else:
            self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        # Connectivity LED 3 shall be off for at least 1 second
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Steady for exactly 5s then off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0031")
    # end def test_power_on_reconnection_to_ch3

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_connected_reconnection_ch1_from_short_press(self):
        """
        [Multiple Channels] While connected to a receiver on the last supported channel (i.e. CH3 or CH2 depending on
        the number of host supported by the device), the device shall enter the reconnection mode in CH1
        if the user does a short press on the Connect button or the EasySwitch CH1 button and CH1 slot is paired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = self.f.PRODUCT.DEVICE.F_NbHosts - 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address)
        channel3 = ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel3)
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)
        # Check index = CH3 in NVS Connect Id chunk
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change Host to CH1 with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
        self.current_channel = self.backup_dut_channel

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the device is back on CH1 host")
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
            test_case=self, device_index=self.original_device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Steady for exactly 5s then off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0032")
    # end def test_connected_reconnection_ch1_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('ConnectButton')
    @level('Functionality')
    def test_connected_reconnection_ch2_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While connected to a receiver on CH1, the device shall enter the
        reconnection mode in CH2 if the user does a short press on the Connect button and CH2 slot is paired.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address,
                                                          hid_dispatcher_to_dump=self.current_channel.hid_dispatcher)
        channel2 = ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel2)
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force back the device in CH1')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, host_index)
        self.current_channel = self.backup_dut_channel

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Check that the device is back on CH1 host")
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
            test_case=self, device_index=self.original_device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change Host to CH2 with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the device is back on CH2 host")
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
            test_case=self, device_index=pairing_slot)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Steady for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0033")
    # end def test_connected_reconnection_ch2_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('ConnectButton')
    @level('Functionality')
    def test_connected_reconnection_ch3_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While connected to a receiver on CH2, the device shall enter the
        reconnection mode in CH3 if the user does a short press on the Connect button and CH3 slot is paired.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        pairing_slot3 = DevicePairingTestUtils.pair_device(self, bluetooth_address)
        channel3 = ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot3)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel3)
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force back the device in CH2')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        pairing_slot2 = DevicePairingTestUtils.pair_device(self, bluetooth_address)
        channel2 = ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot2)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel2)
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change Host to CH3 with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel3)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the device is back on CH3 host")
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
            test_case=self, device_index=pairing_slot3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Steady for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 2
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0034")
    # end def test_connected_reconnection_ch3_from_short_press

    @features('BLEProConnectionScheme')
    @features('SingleHost')
    @level('Functionality')
    def test_pairing_reconnection_ch1_from_short_press(self):
        """
        While in pairing mode on CH1, the device shall enter the reconnection mode in CH1 if the user does a
        short press on the Connect or EasySwitch CH1 button and CH1 slot is paired.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=True)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get back to CH1 Host with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Steady for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0035")
    # end def test_pairing_reconnection_ch1_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('ConnectButton')
    @level('Functionality')
    def test_pairing_change_host_ch2_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in a channel CH1, the device shall enter the
        reconnection mode in the next CH2 if the user does a short press on the Connect button and CH2 slot is paired.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address,
                                                          hid_dispatcher_to_dump=self.current_channel.hid_dispatcher)
        channel2 = ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel2)
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force back the device in CH1')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, host_index=0)
        self.current_channel = self.backup_dut_channel

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=True)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change Host to CH2 Host with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the device is back on CH2 host")
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
            test_case=self, device_index=pairing_slot)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Steady for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0036")
    # end def test_pairing_change_host_ch2_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('ConnectButton')
    @level('Functionality')
    def test_pairing_change_host_ch3_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in a channel CH2, the device shall enter the
        reconnection mode in the next CH3 if the user does a short press on the Connect button and CH3 slot is paired.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        pairing_slot3 = DevicePairingTestUtils.pair_device(self, bluetooth_address)
        channel3 = ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot3)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel3)
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force back the device in CH2')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, host_index=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change Host to CH3 Host with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel3)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the device is back on CH3 host")
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
            test_case=self, device_index=pairing_slot3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Steady for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0037")
    # end def test_pairing_change_host_ch3_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('ConnectButton')
    @level('Functionality')
    def test_pairing_change_host_ch1_from_short_press(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode on the last supported channel (i.e. CH3 or CH2
        depending on the number of host supported by the device), the device shall enter the
        reconnection mode in the next CH1 if the user does a short press on the Connect button and CH1 slot is paired.
        """
        self.post_requisite_program_nvs = True
        host_index = self.f.PRODUCT.DEVICE.F_NbHosts - 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        pairing_slot3 = DevicePairingTestUtils.pair_device(self, bluetooth_address)
        channel3 = ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=self), device_index=pairing_slot3)
        DeviceManagerUtils.set_channel(test_case=self, new_channel_id=channel3)
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent,
            check_first_message=False, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode with a long press on the Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change Host to CH1 Host with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
        self.current_channel = self.backup_dut_channel

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check that the device is back on CH1 host")
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(
            test_case=self, device_index=self.original_device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Steady for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0038")
    # end def test_pairing_change_host_ch1_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_pairing_ch2_reconnection_ch1_from_pairing_timeout(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH2 and the previous Host is CH1, the device
        shall enter reconnection mode in CH1 if the 3 minutes device pairing timeout occurs and CH2 channel is unpaired.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Force the device in pairing mode on CH2 with a short press on the Connect button')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Steady 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, reset=True,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0050")
    # end def test_pairing_ch2_reconnection_ch1_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('ReleaseCandidate')
    def test_pairing_ch3_reconnection_ch2_from_pairing_timeout(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode on the next supported channel (i.e. CH3 or CH1
        depending on the number of host supported by the device) and the previous Host is CH2, the device
        shall enter reconnection mode in CH2 if the 3 minutes device pairing timeout occurs and this next channel is
        unpaired.
        """
        self.post_requisite_program_nvs = True
        host_index = 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH3 with a short press on the Connect '
                                         'button')
        # --------------------------------------------------------------------------------------------------------------
        self._enter_discoverable_mode(channel_id=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Steady 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, reset=True,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0051")
    # end def test_pairing_ch3_reconnection_ch2_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('ReleaseCandidate')
    def test_pairing_ch1_reconnection_ch3_from_pairing_timeout(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH1 and the previous Host is CH3, the device
        shall enter reconnection mode in CH3 if the 3 minutes device pairing timeout occurs and CH1 channel is unpaired.
        """
        self.post_requisite_program_nvs = True

        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH1 with a short press on the Connect '
                                         'button')
        # --------------------------------------------------------------------------------------------------------------
        self._enter_discoverable_mode(channel_id=HOST.CH1)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Steady 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, reset=True,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 2
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0052")
    # end def test_pairing_ch1_reconnection_ch3_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @level('Functionality')
    def test_pairing_ch1_deep_sleep_from_pairing_timeout(self):
        """
        [Multiple Channels] While in pairing mode in CH1 and the no previous Host is defined, the device shall enter
        deep sleep if the 3 minutes device pairing timeout occurs.
        """
        self.post_requisite_program_nvs = True
        host_index = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in OOB state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start a discovery sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        sleep(ConnectivityTestCase.ONE_SECOND)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no HID report is received when a user action is performed')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for another {ConnectivityTestCase.FIVE_SECONDS}s where the LED1 shall be off')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.NONE)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0053")
    # end def test_pairing_ch1_deep_sleep_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('ReleaseCandidate')
    def test_pairing_ch2_deep_sleep_from_pairing_timeout(self):
        """
        [Multiple Channels] While in pairing mode in CH2 and the no previous Host is defined, the device shall enter
        deep sleep if the 3 minutes device pairing timeout occurs.
        """
        self.post_requisite_program_nvs = True
        host_index = 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        sleep(ConnectivityTestCase.ONE_SECOND)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no HID report is received when a user action is performed')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for another {ConnectivityTestCase.FIVE_SECONDS}s where the LED2 shall be off')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.NONE)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0054")
    # end def test_pairing_ch2_deep_sleep_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('ReleaseCandidate')
    def test_pairing_ch3_deep_sleep_from_pairing_timeout(self):
        """
        [Multiple Channels] While in pairing mode in CH3 and the no previous Host is defined, the device shall enter
        deep sleep if the 3 minutes device pairing timeout occurs.
        """
        self.post_requisite_program_nvs = True
        host_index = 2

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        sleep(ConnectivityTestCase.ONE_SECOND)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no HID report is received when a user action is performed')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait for another {ConnectivityTestCase.FIVE_SECONDS}s where the LED1 shall be off')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.NONE)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0055")
    # end def test_pairing_ch3_deep_sleep_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    def test_reconnection_ch1_deep_sleep_from_connect_failed(self):
        """
        While in reconnection mode in CH1, the device shall enter deep sleep mode in CH1 if the reconnection failed
        for the next 5 secondes.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring when device is off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring_when_device_is_off(
            self, led_identifiers=CONNECTIVITY_STATUS_LEDS, off_on_time=ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Verify the link is not re-established')
        # ----------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall not be established if device is in deep sleep mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Slow blinking for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.HUNDRED_MILLISECOND)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0056")
    # end def test_reconnection_ch1_deep_sleep_from_connect_failed

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    def test_reconnection_ch2_deep_sleep_from_connect_failed(self):
        """
        [Multiple Channels] While in reconnection mode in CH2, the device shall enter deep sleep mode in CH2
        if the reconnection failed for the next 5 secondes
        """
        self.post_requisite_program_nvs = True

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring when device is off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring_when_device_is_off(
            self, led_identifiers=CONNECTIVITY_STATUS_LEDS, off_on_time=ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.TEN_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Verify the link is not re-established')
        # ----------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall not be established if device is in deep sleep mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Slow blinking for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.HUNDRED_MILLISECOND)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0057")
    # end def test_reconnection_ch2_deep_sleep_from_connect_failed

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    def test_reconnection_ch3_deep_sleep_from_connect_failed(self):
        """
        [Multiple Channels] While in reconnection mode in CH3, the device shall enter deep sleep mode in CH3
        if the reconnection failed for the next 5 secondes
        """
        self.post_requisite_program_nvs = True

        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring when device is off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring_when_device_is_off(
            self, led_identifiers=CONNECTIVITY_STATUS_LEDS, off_on_time=ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.TEN_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Verify the link is not re-established')
        # ----------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall not be established if device is in deep sleep mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Slow blinking for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.HUNDRED_MILLISECOND)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0058")
    # end def test_reconnection_ch3_deep_sleep_from_connect_failed

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @level('Functionality')
    def test_pairing_ch1_reconnection_ch1_from_pairing_timeout(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH1 and the previous Host is CH1, the device
        shall enter reconnection mode in CH1 if the 3 minutes device pairing timeout occurs.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH1 with a long press on the Connect '
                                         'button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for 3min then Steady 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2 & Led 3 states are always Off')
        # --------------------------------------------------------------------------------------------------------------
        self._verify_leds_off(led_ids=[LED_ID.CONNECTIVITY_STATUS_LED_2, LED_ID.CONNECTIVITY_STATUS_LED_3],
                              duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_MINUTES)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0059")
    # end def test_pairing_ch1_reconnection_ch1_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_pairing_ch2_reconnection_ch2_from_pairing_timeout(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH2 and the previous Host is CH2, the device
        shall enter reconnection mode in CH2 if the 3 minutes device pairing timeout occurs.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH2 with a long press  on the Connect '
                                         'button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for 3min then Steady 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1 & Led 3 states are always Off')
        # --------------------------------------------------------------------------------------------------------------
        self._verify_leds_off(led_ids=[LED_ID.CONNECTIVITY_STATUS_LED_1, LED_ID.CONNECTIVITY_STATUS_LED_3],
                              duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_MINUTES)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0060")
    # end def test_pairing_ch2_reconnection_ch2_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    def test_pairing_ch3_reconnection_ch3_from_pairing_timeout(self):
        """
        [Multiple Channels] While in pairing mode in CH3 and the previous Host is CH3, the device
        shall enter reconnection mode in CH3 if the 3 minutes device pairing timeout occurs.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH3 with a long press on the Connect '
                                         'button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for 3min then Steady 5s then Off')
        # -------------------------------------------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1 & Led 2 states are always Off')
        # --------------------------------------------------------------------------------------------------------------
        self._verify_leds_off(led_ids=[LED_ID.CONNECTIVITY_STATUS_LED_1, LED_ID.CONNECTIVITY_STATUS_LED_2],
                              duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_MINUTES)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 2
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0061")
    # end def test_pairing_ch3_reconnection_ch3_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    def test_pairing_ch2_reconnection_ch1_from_reset(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH2 and the previous Host is CH1, the device
        shall enter reconnection mode in CH1 if the pairing sequence is stopped by a reset and CH2 channel is unpaired.
        """
        self.post_requisite_program_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH2 with a short press on the Connect '
                                         'button')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence but omit the end of sequence action')
        # --------------------------------------------------------------------------------------------------------------
        # Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)
        DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

        # Wait for a start pairing status notification
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # Wait for a display passkey notification
        passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # Wait for a 'Digit Start' passkey notification
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # Loop over passkey inputs list provided by the receiver
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=False)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0062")
    # end def test_pairing_ch2_reconnection_ch1_from_reset

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    def test_pairing_ch3_reconnection_ch2_from_reset(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH3 and the previous Host is CH2, the device
        shall enter reconnection mode in CH2 if the pairing sequence is stopped by a reset and CH3 channel is unpaired.
        """
        self.post_requisite_program_nvs = True

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH3 with a short press on the Connect '
                                         'button')
        # --------------------------------------------------------------------------------------------------------------
        self._enter_discoverable_mode(channel_id=HOST.CH3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence but omit the end of sequence action')
        # --------------------------------------------------------------------------------------------------------------
        # Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)
        DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

        # Wait for a start pairing status notification
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # Wait for a display passkey notification
        passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # Wait for a 'Digit Start' passkey notification
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # Loop over passkey inputs list provided by the receiver
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=False)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0063")
    # end def test_pairing_ch3_reconnection_ch2_from_reset

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    def test_pairing_ch1_reconnection_ch3_from_reset(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH1 and the previous Host is CH3, the device
        shall enter reconnection mode in CH3 if the pairing sequence is stopped by a reset and CH1 channel is unpaired.
        """
        self.post_requisite_program_nvs = True

        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH1 with a short press on the Connect '
                                         'button')
        # --------------------------------------------------------------------------------------------------------------
        self._enter_discoverable_mode(channel_id=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start the pairing sequence but omit the end of sequence action')
        # --------------------------------------------------------------------------------------------------------------
        # Send 'Perform device connection' request with Connect Devices = 1 (i.e Pairing)
        DevicePairingTestUtils.start_pairing_sequence(self, bluetooth_address)

        # Wait for a start pairing status notification
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # Wait for a display passkey notification
        passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # Wait for a 'Digit Start' passkey notification
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # Loop over passkey inputs list provided by the receiver
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=False)
        sleep(.05)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 2
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0064")
    # end def test_pairing_ch1_reconnection_ch3_from_reset

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @level('Functionality')
    @services('MultiHost')
    def test_pairing_ch2_deep_sleep_ch1_from_pairing_timeout(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH2 and the previous Host is CH1, the device
        shall try to reconnect in CH1 if the 3 minutes device pairing timeout occurs but ends in deep sleep if CH1
        receiver has been switched off.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH2')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Slow blinking for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY, reset=True)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0065")
    # end def test_pairing_ch2_deep_sleep_ch1_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    @services('MultiHost')
    def test_pairing_ch3_deep_sleep_ch2_from_pairing_timeout(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH3 and the previous Host is CH2, the device
        shall try to reconnect in CH2 if the 3 minutes device pairing timeout occurs but ends in deep sleep if CH2
        receiver has been switched off.
        """
        self.post_requisite_program_nvs = True
        host_index = 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH3')
        # --------------------------------------------------------------------------------------------------------------
        self._enter_discoverable_mode(channel_id=HOST.CH3)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Slow blinking for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY, reset=True)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 1
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0066")
    # end def test_pairing_ch3_deep_sleep_ch2_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @level('Functionality')
    @services('MultiHost')
    def test_pairing_ch1_deep_sleep_ch3_from_pairing_timeout(self):
        """
        [Multiple Channels] [Connect Button] While in pairing mode in CH1 and the previous Host is CH3, the device
        shall try to reconnect in CH3 if the 3 minutes device pairing timeout occurs but ends in deep sleep if CH3
        receiver has been switched off.
        """
        self.post_requisite_program_nvs = True

        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing channel in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH3 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH1')
        # --------------------------------------------------------------------------------------------------------------
        self._enter_discoverable_mode(channel_id=HOST.CH1)
        start_time = perf_counter()
        end_time = start_time + DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a discovery sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.FAST_BLINKING)
            sleep(ConnectivityTestCase.TEN_SECONDS)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.HUNDRED_MILLISECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Slow blinking for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY, reset=True)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        host_index = 2
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0067")
    # end def test_pairing_ch1_deep_sleep_ch3_from_pairing_timeout

    @features('BLEProConnectionScheme')
    @features('Mice')
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    @services('EmulatedKeys', (KEY_ID.MIDDLE_BUTTON,))
    def test_reconnection_ch1_at_reset_while_button_stuck(self):
        """
        The device shall stay in idle mode in CH1 after a device power off / on when the reconnection failed while a
        button / key is held down.
        When the receiver is re-plugged, the device shall reconnect to CH1.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Keep the middle button pressed')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.MIDDLE_BUTTON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring when device is off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring_when_device_is_off(
            self, led_identifiers=CONNECTIVITY_STATUS_LEDS, off_on_time=ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the link is re-established')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection, check_first_message=False)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall be established if device returned from idle mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Slow blinking for 5s then Off then steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # Key release
        self.button_stimuli_emulator.key_release(KEY_ID.MIDDLE_BUTTON)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0090")
    # end def test_reconnection_ch1_at_reset_while_button_stuck

    @features('BLEProConnectionScheme')
    @features('Mice')
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    def test_reconnection_ch1_from_idle_while_key_press_before_turn_off(self):
        """
        The device shall enter idle mode in CH1 when the reconnection failed
        but a button / key is held down before removing the receiver.
        When turning the receiver on, the device shall reconnect in CH1 and send its HID Mouse reports.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Keep the right button pressed')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.RIGHT_BUTTON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the link is re-established')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection, check_first_message=False)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall be established if device returned from idle mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # Key release
        self.button_stimuli_emulator.key_release(KEY_ID.RIGHT_BUTTON)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0091")
    # end def test_reconnection_ch1_from_idle_while_key_press_before_turn_off

    @features('BLEProConnectionScheme')
    @features('Mice')
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    def test_reconnection_ch1_from_idle_while_turn_off_before_key_press(self):
        """
        The device shall enter idle mode in CH1 when the reconnection failed
        but a button / key is held down after removing the receiver.
        When turning the receiver on, the device shall reconnect in CH1 and send its HID Mouse reports.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Keep the right button pressed')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.RIGHT_BUTTON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the link is re-established')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection, check_first_message=False)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall be established if device returned from idle mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # Right button released
        self.button_stimuli_emulator.key_release(KEY_ID.RIGHT_BUTTON)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0092")
    # end def test_reconnection_ch1_from_idle_while_turn_off_before_key_press

    @features('BLEProConnectionScheme')
    @features('Keyboard')
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    def test_reconnection_ch1_at_reset(self):
        """
        The device shall stay in idle mode in CH1 after a device power off / on when the reconnection failed while a
        button / key is held down.
        When the receiver is re-plugged, the device shall reconnect to CH1.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring when device is off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring_when_device_is_off(
            self, led_identifiers=CONNECTIVITY_STATUS_LEDS, off_on_time=ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a keystroke')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_RIGHT_ARROW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the link is re-established')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection, check_first_message=False)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall be established if device returned from idle mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.SIX_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Slow blinking for 5s then Off then steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0090#2")
    # end def test_reconnection_ch1_at_reset

    @features('BLEProConnectionScheme')
    @features('Keyboard')
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    def test_reconnection_ch3_from_idle(self):
        """
        The device shall enter idle mode in CH1 when the reconnection failed
        but a button / key is held down before removing the receiver.
        When turning the receiver on, the device shall reconnect in CH1 and send its HID Mouse reports.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a key stroke')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_RIGHT_ARROW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the link is re-established')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection, check_first_message=False)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall be established if device returned from idle mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0091#2")
    # end def test_reconnection_ch3_from_idle

    @features('BLEProConnectionScheme')
    @features('Keyboard')
    @level('Functionality')
    @services('MultiHost')
    @services('Debugger')
    def test_reconnection_ch1_from_idle(self):
        """
        The device shall enter idle mode in CH1 when the reconnection failed
        but a button / key is held down after removing the receiver.
        When turning the receiver on, the device shall reconnect in CH1 and send its HID Mouse reports.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_power_on_usb_port = True
        ChannelUtils.close_channel(test_case=self)
        self.channel_disable(self.receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the 5s device connection timeout to occur')
        # --------------------------------------------------------------------------------------------------------------
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn on the receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.channel_enable(self.receiver_port_index, wait_time=2.0, wait_device_notification=False)
        self.post_requisite_power_on_usb_port = False
        ChannelUtils.set_hidpp_reporting(test_case=self)
        sleep(DevicePairingTestUtils.RECONNECTION_TIMEOUT+DevicePairingTestUtils.TIMEOUT_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a key stroke')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_RIGHT_ARROW)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
                          report=set_register, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                          response_class_type=SetConnectionStateResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify the link is re-established')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT, class_type=DeviceConnection, check_first_message=False)
        device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        self.assertEqual(expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                         obtained=to_int(device_info.device_info_link_status),
                         msg="The link shall be established if device returned from idle mode")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0092#2")
    # end def test_reconnection_ch1_from_idle

    def _verify_leds_off(self, led_ids, duration):
        """
        Check LEDs are off for a given duration

        :param led_ids: List of LEDs to control
        :type led_ids: ``list[LED_ID]``
        :param duration: minimum duration in off state to enforce in ms
        :type duration: ``int``
        """
        for led_id in led_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Verify {led_id} state is Off during {duration} ms')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                self, led_id=led_id, reset=True, minimum_duration=duration,
                position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        # end for
    # end def _verify_leds_off

# end class ConnectivityTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
