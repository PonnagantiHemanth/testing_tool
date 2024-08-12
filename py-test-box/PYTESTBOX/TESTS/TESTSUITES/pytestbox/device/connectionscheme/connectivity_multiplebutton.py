#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.connectivity_multiplebutton
:brief: Validate BLE Pro Connectivity flowcharts with Easyswitch buttons (BLE Connection Scheme feature)
:author: Christophe Roquebert
:date: 2020/08/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import CONNECTIVITY_STATUS_LEDS
from pylibrary.emulator.ledid import LED_ID
from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.connectionscheme.connectivity import ConnectivityTestCase
from pytestbox.device.connectionscheme.safeprepairedreceiver import ConnectionSchemeTestCaseMixin
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConnectivityMultipleButtonTestCase(ConnectionSchemeTestCaseMixin):
    """
    Device BLE Pro Connectivity Multiple Button Supported TestCases
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_program_nvs = False

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
            LogHelper.log_post_requisite(self, 'Stop I2C monitoring')
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
        # end with
        super().tearDown()
    # end def tearDown

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('Debugger')
    def test_pairing_ch2_pairing_ch1_from_oob_state(self):
        """
        While the user could change channel by doing a long press on the easyswitch H2 button,
        the firmware shall stay in OOB state.
        At next power off /on, the device shall always enter pairing mode in CH1.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in OOB state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.invalidate_connect_id_chunks(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H2 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

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
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0098")
    # end def test_pairing_ch2_pairing_ch1_from_oob_state

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('Debugger')
    def test_pairing_ch3_pairing_ch1_from_oob_state(self):
        """
        While the user could change channel by doing a long press on the easyswitch H3 button,
        the firmware shall stay in OOB state.
        At next power off /on, the device shall always enter pairing mode in CH1 and connect in CH1 if the
        pairing sequence succeded.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in OOB state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.invalidate_connect_id_chunks(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H3 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)

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
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0099")
    # end def test_pairing_ch3_pairing_ch1_from_oob_state

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_connected_ch2_pairing_mode_ch1_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH2, the device
        shall enter pairing mode in CH1 if the user does a long press on the EasySwitch CH1 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
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
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H1 Easy switch button')
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
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0100")
    # end def test_connected_ch2_pairing_mode_ch1_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_connected_ch3_pairing_mode_ch1_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH3, the device
        shall enter pairing mode in CH1 if the user does a long press on the EasySwitch CH1 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
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
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H1 Easy switch button')
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
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0101")
    # end def test_connected_ch3_pairing_mode_ch1_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch1_pairing_mode_ch2_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH1, the device
        shall enter pairing mode in CH2 if the user does a long press on the EasySwitch H2 button.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H2 Easy switch button')
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
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0102")
    # end def test_connected_ch1_pairing_mode_ch2_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch3_pairing_mode_ch2_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH3, the device
        shall enter pairing mode in CH2 if the user does a long press on the EasySwitch H2 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
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
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H2 Easy switch button')
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
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0103")
    # end def test_connected_ch3_pairing_mode_ch2_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch1_pairing_mode_ch3_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH1, the device
        shall enter pairing mode in CH3 if the user does a long press on the EasySwitch H3 button.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H3 Easy switch button')
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
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0104")
    # end def test_connected_ch1_pairing_mode_ch3_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch2_pairing_mode_ch3_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH2, the device
        shall enter pairing mode in CH3 if the user does a long press on the EasySwitch H3 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
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
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H3 Easy switch button')
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
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0105")
    # end def test_connected_ch2_pairing_mode_ch3_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_pairing_mode_ch2_pairing_mode_ch1_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH2, the device shall enter
        pairing mode on CH1 if the user does a long press on the EasySwitch H1 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H1 Easy switch button')
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
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, reset=True,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0106")
    # end def test_pairing_mode_ch2_pairing_mode_ch1_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_pairing_mode_ch3_pairing_mode_ch1_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH3, the device shall enter
        pairing mode on CH1 if the user does a long press on the EasySwitch H1 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H1 Easy switch button')
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
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, reset=True,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0107")
    # end def test_pairing_mode_ch3_pairing_mode_ch1_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_pairing_mode_ch1_pairing_mode_ch2_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH1, the device
        shall enter pairing mode in CH2 if the user does a long press on the EasySwitch H2 button.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH1')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H2 Easy switch button')
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
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, reset=True,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0108")
    # end def test_pairing_mode_ch1_pairing_mode_ch2_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_pairing_mode_ch3_pairing_mode_ch2_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH3, the device
        shall enter pairing mode in CH2 if the user does a long press on the EasySwitch H2 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H2 Easy switch button')
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
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, reset=True,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0109")
    # end def test_pairing_mode_ch3_pairing_mode_ch2_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_pairing_mode_ch1_pairing_mode_ch3_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH1, the device
        shall enter pairing mode in CH3 if the user does a long press on the EasySwitch H3 button.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device in pairing mode on CH1')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H3 Easy switch button')
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
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, reset=True,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0110")
    # end def test_pairing_mode_ch1_pairing_mode_ch3_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_pairing_mode_ch2_pairing_mode_ch3_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH2, the device
        shall enter pairing mode in CH3 if the user does a long press on the EasySwitch H3 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H3 Easy switch button')
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
        sleep(ConnectivityTestCase.FIVE_SECONDS)
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is Fast blinking for at least 1s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led3State is Fast blinking for at least 3s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, reset=True,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.THREE_SECONDS,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0111")
    # end def test_pairing_mode_ch2_pairing_mode_ch3_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH1)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch1_pairing_mode_ch1_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH1, the device shall
        enter pairing mode on the same channel if the user does a long press on the EasySwitch H1 button.
        """
        self.post_requisite_program_nvs = True
        # Let Connectivity LED 1 switch off
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H1 Easy switch button')
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
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        sleep(ConnectivityTestCase.FIVE_SECONDS)
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
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0112")
    # end def test_connected_ch1_pairing_mode_ch1_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch2_pairing_mode_ch2_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH2, the device shall
        enter pairing mode on the same channel if the user does a long press on the EasySwitch H2 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
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
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H2 Easy switch button')
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

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0113")
    # end def test_connected_ch2_pairing_mode_ch2_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch3_pairing_mode_ch3_from_long_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH3, the device shall
        enter pairing mode on the same channel if the user does a long press on the EasySwitch H3 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
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

        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the H3 Easy switch button')
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

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0114")
    # end def test_connected_ch3_pairing_mode_ch3_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH1)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch1_connected_ch1_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH1, the device shall
        stay connected on the same channel if the user does a short press on the same EasySwitch button.
        """
        self.post_requisite_program_nvs = True
        # Let Connectivity LED 1 switch off
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on the same H1 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH1 is steady for 5s')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0115")
    # end def test_connected_ch1_connected_ch1_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch2_connected_ch2_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH2, the device shall
        stay connected on the same channel if the user does a short press on the same EasySwitch button.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
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
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on the same H2 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)

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
        LogHelper.log_check(self, 'Verify Led2State is Steady then Off for at least 1s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0116")
    # end def test_connected_ch2_connected_ch2_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch3_connected_ch3_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH3, the device shall
        stay connected on the same channel if the user does a short press on the same EasySwitch button.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
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
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on the same H3 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)

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
        LogHelper.log_check(self, 'Verify Led3State is Steady then Off for at least 1s then Steady for 5s then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0117")
    # end def test_connected_ch3_pairing_mode_ch3_from_long_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch1_connected_ch1_from_short_press_another_ch(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH1, the device stay
        connected on CH1 if the user does a short press on another EasySwitch button and this slot is unpaired.
        """
        self.post_requisite_program_nvs = True
        # Let Connectivity LED 1 switch off
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        # Connectivity LED 1 shall be off for at least 1 second
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H2 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH1 is steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.STEADY)
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H3 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH1 is off then steady for 5s when pressing '
                                  'the Easyswitch Host 2')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH1 is off then steady for 5s when pressing '
                                  'the Easyswitch Host 3')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0118")
    # end def test_connected_ch1_connected_ch1_from_short_press_another_ch

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH3)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch2_connected_ch2_from_short_press_another_ch(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH2, the device stay
        connected on CH2 if the user does a short press on another EasySwitch button and this slot is unpaired.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index, oob=True)

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
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H1 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH2 is steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, state=SchemeType.STEADY)
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H3 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH2 is steady then off then steady again for '
                                  '5s when pressing the Easyswitch Host 1')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH2 is off then steady for 5s when pressing '
                                  'the Easyswitch Host 3')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0119")
    # end def test_connected_ch2_connected_ch2_from_short_press_another_ch

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_connected_ch3_connected_ch3_from_short_press_another_ch(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH3, the device stay
        connected on CH3 if the user does a short press on another EasySwitch button and this slot is unpaired.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
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
        LogHelper.log_step(self, 'Short press on another H1 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH3 is steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, state=SchemeType.STEADY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H2 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH3 is steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, reset=True,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0120")
    # end def test_connected_ch3_connected_ch3_from_short_press_another_ch

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_connected_ch2_reconnection_ch1_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected on CH2, the device shall enter the
        reconnection mode in CH1 channel if the user does a short press on the EasySwitch H1 button
        and CH1 slot is paired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
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
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H1 Easy switch button')
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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH1 is steady')
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
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0121")
    # end def test_connected_ch2_reconnection_ch1_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_connected_ch1_reconnection_ch2_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected on CH1, the device shall enter the
        reconnection mode in CH2 channel if the user does a short press on the EasySwitch H2 button
        and CH2 slot is paired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
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
        LogHelper.log_prerequisite(self, 'Force back the device in CH1')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H2 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH2 is steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0122")
    # end def test_connected_ch1_reconnection_ch2_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_connected_ch3_reconnection_ch2_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected on CH3, the device shall enter the
        reconnection mode in CH2 channel if the user does a short press on the EasySwitch H2 button
        and CH2 slot is paired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
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
        LogHelper.log_prerequisite(self, 'Force back the device in CH3')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, host_index)

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
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H2 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH2 is steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 1
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0123")
    # end def test_connected_ch3_reconnection_ch2_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_connected_ch1_reconnection_ch3_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected on CH1, the device shall enter the
        reconnection mode in CH3 channel if the user does a short press on the EasySwitch H3 button
        and CH3 slot is paired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
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
        LogHelper.log_prerequisite(self, 'Force back the device in CH1')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 0
        DeviceBaseTestUtils.NvsHelper.change_host(self, self.memory_manager, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H3 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH3 is steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0124")
    # end def test_connected_ch1_reconnection_ch3_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_connected_ch2_reconnection_ch3_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected on CH2, the device shall enter the
        reconnection mode in CH3 channel if the user does a short press on the EasySwitch H3 button
        and CH3 slot is paired.
        """
        self.post_requisite_program_nvs = True
        BacklightTestUtils.HIDppHelper.disable_backlight_wow_effect(test_case=self)

        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
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
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on another H3 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH3)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH3 is steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        host_index = 2
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0125")
    # end def test_connected_ch2_reconnection_ch3_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_pairing_ch1_reconnection_ch1_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH1, the device shall enter the
        reconnection mode in CH1 if the user does a short press on the EasySwitch H1 button and CH1 slot is paired.
        """
        self.post_requisite_program_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'start a discovery sequence on this CH1 slot')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1)
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on H1 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.HOST_1)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH1 is Fast blinking then steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
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
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0126")
    # end def test_pairing_ch1_reconnection_ch1_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_pairing_ch2_reconnection_ch2_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH2, the device shall enter the
        reconnection mode in CH2 if the user does a short press on the EasySwitch H2 button and CH2 slot is paired.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
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
        LogHelper.log_prerequisite(self, 'Emulate a long press on the H2 EasySwitch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start a pairing sequence on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=(DeviceDiscovery, DiscoveryStatus))
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on H2 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.HOST_2)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH2 is Fast blinking then steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0127")
    # end def test_pairing_ch2_reconnection_ch2_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels')
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    @services('MultiHost')
    def test_pairing_ch3_reconnection_ch3_from_short_press(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While in pairing mode on CH3, the device shall enter the
        reconnection mode in CH3 if the user does a short press on the EasySwitch H3 button and CH3 slot is paired.
        """
        self.post_requisite_program_nvs = True
        host_index = 2
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH3 pairing slot in unpaired state')
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
        LogHelper.log_prerequisite(self, 'Emulate a long press on the H3 EasySwitch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH3)

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
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Short press on H3 Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.HOST_3)

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
        LogHelper.log_check(self, 'Check the Connectivity Status LED on CH3 is Fast blinking then steady')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3,
            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)
        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0128")
    # end def test_pairing_ch3_reconnection_ch3_from_short_press

    @features('BLEProConnectionScheme')
    @features('MultipleChannels', HOST.CH2)
    @features('MultipleEasySwitchButtons')
    @level('Functionality')
    def test_connected_ch1_searching_ch2(self):
        """
        [Multiple Channels] [Multiple EasySwitch Buttons] While connected to a receiver on CH2, the device shall
        enter pairing mode on the same channel if the user does a long press on the EasySwitch H2 button.
        """
        self.post_requisite_program_nvs = True
        host_index = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the device CH2 pairing slot in unpaired state')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Pair the device on this CH2 slot')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
        ChannelUtils.clean_messages(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                    channel=ChannelUtils.get_receiver_channel(test_case=self),
                                    class_type=DeviceConnection)
        pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reconnect the device on Host 1')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        sleep(ConnectivityTestCase.ONE_SECOND)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify an HID report can be received')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Unpair the new pairing slot in the receiver')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_slot(self, pairing_slot, ignore_notification=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "For the device in 'Searching' state on Host 2")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH2)
        sleep(ConnectivityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led2State is off then slow blinking for 5s then off again')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Connect Id chunk in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        DeviceBaseTestUtils.NvsHelper.check_connect_id(
            self, self.memory_manager, host_index, ConnectIdChunkData.PairingSrc.USR)

        self.testCaseChecked("FNT_BLE_PRO_CONNECT_0130")
    # end def test_slow_blinking_ch2


# end class ConnectivityMultipleButtonTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
