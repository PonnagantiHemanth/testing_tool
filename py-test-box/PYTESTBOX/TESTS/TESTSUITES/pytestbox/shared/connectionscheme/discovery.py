#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.connectionscheme.discovery
:brief: Validate device discovery feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/04/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from time import perf_counter
from time import sleep
from unittest import expectedFailure

from pyharness.core import TYPE_SUCCESS
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedCommonDiscoveryTestCase(CommonBaseTestCase, ABC):
    """
    Shared Common Discovery TestCase class
    """
    def setUp(self):
        """
        Handle test prerequisites
        """
        self.post_requisite_program_nvs = False

        super().setUp()

        if self.device_memory_manager is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Backup initial NVS')
            # ----------------------------------------------------------------------------------------------------------
            self.device_memory_manager.read_nvs(backup=True)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Device not connected and in non-discoverable mode')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.NvsManager.clean_pairing_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'No discovery ongoing')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable HID++ notifications')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Clean discovery notifications')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus))

        # Initialize the authentication method parameter
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
    # end def setUp

    def tearDown(self):
        """
        Handle test post requisites
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Cancel any ongoing discovery')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.cancel_discovery(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Clean discovery notifications')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.clean_messages(
                test_case=self,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=(DeviceDiscovery, DiscoveryStatus))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Switch back connection to Host 0')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.change_host_by_link_state(self)
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with

        with self.manage_post_requisite():
            if self.device_memory_manager is not None and (self.post_requisite_program_nvs or
                                                           self.status != TYPE_SUCCESS):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reload initial NVS state')
                # ------------------------------------------------------------------------------------------------------
                self.device_memory_manager.load_nvs(backup=True)
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class SharedCommonDiscoveryTestCase(CommonBaseTestCase):


class SharedDiscoveryTestCase(SharedCommonDiscoveryTestCase, ABC):
    """
    Shared Discovery TestCases
    """
    def _setup_rcv_with_device(self):
        """
        Basic button emulator and device setup only for Receiver with Device tests
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Use Easy Switch button to select host on device')
        # --------------------------------------------------------------------------------------------------------------
        # Double click on the easy switch button to switch to host with link not established
        DevicePairingTestUtils.change_host_by_link_state(
            self, link_state=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
    # end def _setup_rcv_with_device

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @level('Business', 'SmokeTests')
    def test_device_discovery_business_case(self):
        """
        Test Device Discovery business case

        Sequence diagram:
            SW -> Receiver: Perform Device Discovery (Discover HID Devices)
            SW <- Receiver: Discovery Status Notification (Discovery Start)
            Device <- User: Put in Pairing Mode
            Receiver <- Device: Advertising
            Receiver -> Device: SCAN_REQ
            Receiver <- Device : SCAN_RSP
            SW <- Receiver: Device Discovery Notification
            SW -> Receiver: Perform Device Discovery (Cancel)
            SW <- Receiver: Discovery Status Notification (Discovery Cancel)
        """
        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enumeration sequence successfully executed')
        # --------------------------------------------------------------------------------------------------------------
        EnumerationTestUtils.paired_device_enumeration_sequence(self)
        EnumerationTestUtils.connected_device_enumeration_sequence(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send "Perform Device Discovery" write request')
        LogHelper.log_check(self, 'Validate response')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Discovery status notification is received with valid parameters')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Discovery Notification is received')
        # --------------------------------------------------------------------------------------------------------------
        device_discovery = DiscoveryTestUtils.get_first_device_discovery_notification(
            self, PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE)

        self.assertNotNone(device_discovery[DeviceDiscovery.PART.CONFIGURATION],
                           "Part 0 (configuration) should always be received")
        self.assertNotNone(device_discovery[DeviceDiscovery.PART.NAME_1],
                           "Part 1 (Device name first part) should always be received")

        # TODO : check LED #3 is blinking fast, LEDs #1 and #2 are off

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)

        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=DeviceDiscovery)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Discovery status notification is received with valid parameters')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.CANCEL, DiscoveryStatus.ErrorType.NO_ERROR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check "Device Discovery Notifications" valid values')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.DeviceDiscoveryNotificationChecker.check_fields(
            self, device_discovery[DeviceDiscovery.PART.CONFIGURATION], DeviceDiscovery)

        DiscoveryTestUtils.DeviceDiscoveryNotificationChecker.DataChecker.check_fields(
            self, device_discovery[DeviceDiscovery.PART.CONFIGURATION].data, DeviceDiscovery.DeviceDiscoveryPart0)

        DiscoveryTestUtils.DeviceDiscoveryNotificationChecker.check_name(self, device_discovery)

        # TODO : check LEDs #1, #2 and #3 are off

        self.testCaseChecked("FNT_DEV_DISC_0003")
    # end def test_device_discovery_business_case

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @level('Functionality')
    def test_device_discovery_timeout_discovery_notification(self):
        """
        Perform Device Discovery with Discovery Timeout in valid range. Devices shall be discovered until end of
        timeout and not after.

        Sequence diagram:
            SW -> Receiver: Perform Device Discovery (Discover HID Devices)
            SW <- Receiver: Discovery Status Notification (Discovery Start, No Error)
            Device <- User: Put in Pairing Mode
            group Until end of Discovery Timeout
                Receiver <- Device: Advertising
                SW <- Receiver: Device Discovery Notification
            end
        """
        self._setup_rcv_with_device()

        if PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN > PerformDeviceDiscovery.DiscoveryTimeout.MIN:
            self.log_warning("Minimum Discovery Timeout can not be tested")
        # end if

        for discovery_timeout in [PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN,
                                  PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
                                  PerformDeviceDiscovery.DiscoveryTimeout.MAX]:

            if discovery_timeout == PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT:
                discovery_timeout_value = PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE
            else:
                discovery_timeout_value = discovery_timeout
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Force the device in pairing mode with a long press on Easy Switch button')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.change_host_by_link_state(self, DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            self.button_stimuli_emulator.enter_pairing_mode()

            # TODO : check LED #3 is blinking fast, LEDs #1 and #2 are off

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send "Perform Device Discovery" write request with Discovery Timeout = '
                                     f'{discovery_timeout}')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.start_discovery(self, discovery_timeout)
            start_time = perf_counter()
            ChannelUtils.clean_messages(
                test_case=self,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=DiscoveryStatus)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait until end of timeout')
            LogHelper.log_check(self, 'Check Device Discovery notification are received during this time')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.check_device_discovery_notifications_until_timeout(
                self,
                start_time + float(discovery_timeout_value),
                float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
                float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no more discovery notifications are received after discovery timeout')
            # ----------------------------------------------------------------------------------------------------------
            sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            # TODO : check LED #3 is still blinking fast, LEDs #1 and #2 are off
            self.assertEqual(obtained=len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)),
                             expected=0,
                             msg='No more discovery notifications should have been received after discovery '
                                 'timeout')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press Easy Switch button to exit pairing mode')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host()

            # TODO : check all LEDs are off
        # end for

        self.testCaseChecked("FNT_DEV_DISC_0004")
    # end def test_device_discovery_timeout_discovery_notification

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @level('Functionality')
    def test_device_discovery_no_change_discovery_notification(self):
        """
        Press EasySwitch button to start advertising. Perform Device Discovery Write command to start discovering
        then send command again with No Change. Device Discovery Notification should be received until end of initial
        timeout. No more Device Discovery notification should be received after the end of initial timeout.

        Sequence diagram:
            Device <- User: Put in Pairing Mode
            SW -> Receiver: Perform Device Discovery (Discover HID Devices)
            group During wait time
                Receiver <- Device: Advertising
                SW <- Receiver: Device Discovery Notification
            end
            SW -> Receiver: Perform Device Discovery (No Change)
            group Until end of timeout
                Receiver <- Device: Advertising
                SW <- Receiver: Device Discovery Notification
            end
        """
        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode()

        # TODO : check LED #3 is blinking fast, LEDs #1 and #2 are off

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send "Perform Device Discovery" write request to start discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT)
        start_time = perf_counter()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait to let the discovery start')
        # --------------------------------------------------------------------------------------------------------------
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=DiscoveryStatus)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Discovery notification are received at start of discovery')
        # --------------------------------------------------------------------------------------------------------------
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        self.assertGreater(len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)), 0,
                           'Discovery notifications should have been received after at start of discovery')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform Device Discovery write request with "No Change"')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.perform_device_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
                                                    PerformDeviceDiscovery.DiscoverDevices.NO_CHANGE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Discovery notifications are received until end of initial timeout')
        # --------------------------------------------------------------------------------------------------------------
        discovery_timeout_value = PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE
        end_time = start_time + float(discovery_timeout_value)
        step_time = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        tolerance = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        DiscoveryTestUtils.check_device_discovery_notifications_until_timeout(self, end_time, step_time, tolerance)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no more Discovery notifications are received after end of initial timeout')
        # --------------------------------------------------------------------------------------------------------------
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        # TODO : check LED #3 is still blinking fast, LEDs #1 and #2 are off
        self.assertEqual(len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)), 0,
                         'No more discovery notifications should have been received after the end of initial '
                         'timeout')

        self.testCaseChecked("FNT_DEV_DISC_0006")
    # end def test_device_discovery_no_change_discovery_notification

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @level('Functionality')
    def test_device_discovery_cancel_discovery_notification(self):
        """
        Press EasySwitch button to start advertising. Perform Device Discovery Write command to start discovering
        then send command again to cancel discovery. Device Discovery Notification shoul be received until
        discovering is canceled. No more Device Discovery Notification should be received after discovering is canceled.

        Sequence diagram:
            Device <- User: Put in Pairing Mode
            SW -> Receiver: Perform Device Discovery (Discover HID Devices)
            group During wait time
                Receiver <- Device: Advertising
                SW <- Receiver: Device Discovery Notification
            end
            SW -> Receiver: Perform Device Discovery (Cancel Discovery)
        """
        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode()
        # TODO : check LED #3 is blinking fast, LEDs #1 and #2 are off

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send "Perform Device Discovery" write request')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait to let the Discovery start')
        # --------------------------------------------------------------------------------------------------------------
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=DiscoveryStatus)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Discovery notifications are received at start of discovery')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)), 0,
                           'Discovery notifications should have been received')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform Device Discovery to Cancel discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no more discovery notifications are received after discovery cancel')
        # --------------------------------------------------------------------------------------------------------------
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        # TODO : check LED #3 is still blinking fast, LEDs #1 and #2 are off
        self.assertEqual(obtained=len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)), expected=0,
                         msg='No more discovery notifications should have been received after discovery cancel')

        self.testCaseChecked("FNT_DEV_DISC_0008")
    # end def test_device_discovery_cancel_discovery_notification

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @level('ReleaseCandidate')
    def test_restart_discovering_discovery_notification(self):
        """
        Press EasySwitch button to start advertising. Perform Device Discovery Write command to start discovering then
        send command again to restart discovering with a new timeout (shorter, equal or longer than initial one).
        Device Discovery Notification should be received until end of new timeout.

        Sequence diagram:
            Device <- User: Put in Pairing Mode
            SW -> Receiver: Perform Device Discovery (Initial Timeout, Discover HID Devices)
            group During wait time
                Receiver <- Device: Advertising
                SW <- Receiver: Device Discovery Notification
            end
            SW -> Receiver: Perform Device Discovery (New Timeout, Discover HID Devices)
            group Until end of Discovery Timeout
                Receiver <- Device: Advertising
                SW <- Receiver: Device Discovery Notification
            end
        """
        self._setup_rcv_with_device()

        if PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN > PerformDeviceDiscovery.DiscoveryTimeout.MIN:
            self.log_warning("Minimum Discovery Timeout can not be tested")
        # end if

        for new_discovery_timeout in [PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN,
                                      PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
                                      PerformDeviceDiscovery.DiscoveryTimeout.MAX]:

            if new_discovery_timeout == PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT:
                new_discovery_timeout_value = PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE
            else:
                new_discovery_timeout_value = new_discovery_timeout
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy Switch button')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.change_host_by_link_state(self, DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            self.button_stimuli_emulator.enter_pairing_mode()
            # TODO : check LED #3 is blinking fast, LEDs #1 and #2 are off

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send "Perform Device Discovery" write request')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.start_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT)
            initial_timeout_value = PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Wait to let discovery start')
            # ----------------------------------------------------------------------------------------------------------
            sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            ChannelUtils.clean_messages(
                test_case=self,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=DiscoveryStatus)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Discovery notifications are received at discovery start')
            # ----------------------------------------------------------------------------------------------------------
            sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
            self.assertGreater(len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)), 0,
                               'Discovery notifications should have been received after discovery start')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send "Perform Device Discovery" write request with new timeout')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.start_discovery(self, new_discovery_timeout)
            start_time = perf_counter()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Discovery notifications are received until end of timeout')
            # ----------------------------------------------------------------------------------------------------------
            end_time = start_time + float(new_discovery_timeout_value)
            step_time = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            tolerance = float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
            DiscoveryTestUtils.check_device_discovery_notifications_until_timeout(
                self, end_time, step_time, tolerance)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no more Discovery notifications are received after timeout')
            # ----------------------------------------------------------------------------------------------------------
            sleep(float(initial_timeout_value))
            # TODO : check LED #3 is still blinking fast, LEDs #1 and #2 are off
            self.assertEqual(len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)), 0,
                             'No more discovery notifications should have been received')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Press Easy Switch button to exit pairing mode')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host()
            # TODO : check all LEDs are off
        # end for

        self.testCaseChecked("FNT_DEV_DISC_0010")
    # end def test_restart_discovering_discovery_notification

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_discovery_with_all_pairing_slots_used(self):
        """
        Perform Device Discovery when all pairing slots are used. Discovery should be accepted and started.
        """
        self._setup_rcv_with_device()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair device on all pairing slots')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_program_nvs = True
        DevicePairingTestUtils.pair_all_slots(self)
        self.button_stimuli_emulator.enter_pairing_mode()
        # TODO : check LED #3 is blinking fast, LEDs #1 and #2 are off

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start Discovery')
        LogHelper.log_check(self, 'Check valid response is received')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Start Discovery notification is received')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Discovery notifications are received at discovery start')
        # --------------------------------------------------------------------------------------------------------------
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        # TODO : check LED #3 is still blinking fast, LEDs #1 and #2 are off
        self.assertGreater(len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)), 0,
                           'Discovery notifications should have been received after discovery start')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Cleanup all pairing slots in the receiver except the first one')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(test_case=self)

        self.testCaseChecked("FNT_DEV_DISC_0013")
    # end def test_discovery_with_all_pairing_slots_used

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @level('Functionality')
    def test_disable_notifications_discovery_notifications(self):
        """
        No notification should be sent if notifications are disabled
        """
        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable HID++ reporting')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device in pairing mode with a long press on the Easy switch button')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.enter_pairing_mode()
        # TODO : check LED #3 is blinking fast, LEDs #1 and #2 are off

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send multiple "Perform Device Discovery" which can create notifications')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self)
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        DiscoveryTestUtils.perform_device_discovery(self,
                                                    PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
                                                    PerformDeviceDiscovery.DiscoverDevices.NO_CHANGE)
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        DiscoveryTestUtils.cancel_discovery(self)
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))
        DiscoveryTestUtils.start_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN)
        sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no discovery notifications are received')
        # --------------------------------------------------------------------------------------------------------------
        # TODO : check LED #3 is still blinking fast, LEDs #1 and #2 are off
        self.assertEqual(obtained=len(DiscoveryTestUtils.get_all_device_discovery_notifications(self)), expected=0,
                         msg='No discovery notifications should be received')

        self.testCaseChecked("FNT_DEV_DISC_0014")
    # end def test_disable_notifications_discovery_notifications
    
    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @features('BLEDevicePairing')
    @features("Feature1807")
    @level('Functionality')
    def test_device_discovery_extended_model_id(self):
        """
        Extended Model Id field in Device Discovery Notification should reflect the extended model id of the device.
        Extended Model Id field in Device Discovery Notification should match Configurable Properties
        (feature 0x1807)
        """

        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair with device and get device index')
        # --------------------------------------------------------------------------------------------------------------
        ble_addr = DiscoveryTestUtils.discover_device(self)
        self.post_requisite_program_nvs = True
        device_index = DevicePairingTestUtils.pair_device(self, ble_addr)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over extended model id significant values')
        # --------------------------------------------------------------------------------------------------------------
        for extended_model_id in reversed(compute_sup_values(HexList('00'), True)):
            self.current_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
                port_index=ChannelUtils.get_port_index(test_case=self), device_index=device_index))
            ChannelUtils.open_channel(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enable Manufacturing Features')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True, device_index=device_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set extended model id (using 1807)")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.select_property(
                self, ConfigurableProperties.PropertyId.EXTENDED_MODEL_ID)
            ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, extended_model_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Pair with device and get device index')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, device_index)
            discovery_notifications = DiscoveryTestUtils.device_discovery_sequence(self)
            ble_addr = discovery_notifications[DeviceDiscovery.PART.CONFIGURATION].data.bluetooth_address

            self.assertEqual(
                expected=extended_model_id,
                obtained=discovery_notifications[DeviceDiscovery.PART.CONFIGURATION].data.extended_model_id,
                msg="Device Discovery Notification Extended Model Id should match Configurable Device Properties "
                    "Extended Model Id")

            self.current_channel = ChannelUtils.get_receiver_channel(test_case=self)
            device_index = DevicePairingTestUtils.pair_device(self, ble_addr)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FNT_DEV_DISC_0016")
    # end def test_device_discovery_extended_model_id

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @level('Functionality')
    @expectedFailure  # https://jira.logitech.io/browse/BPRO-39
    def test_unpairing_while_discovering(self):
        """
        When a PerformDevicePairing.Pairing is received, and the command is processed, it stops the on-going Discovery.
        When a PerformDevicePairing.Unpairing is received, the on-going Discovery should continue and not be changed
        # TODO : follow https://jira.logitech.io/projects/BPRO/issues/BPRO-39?filter=allissues status
        """
        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair with device and get device index')
        # --------------------------------------------------------------------------------------------------------------
        ble_addr = DiscoveryTestUtils.discover_device(self)
        self.post_requisite_program_nvs = True
        device_index = DevicePairingTestUtils.pair_device(self, ble_addr)

        # TODO :
        #  - device enter pairing mode
        #  - check LED #3 is blinking fast, LEDs #1 and #2 are off

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Start Discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self)
        start_time = perf_counter()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Start Discovery notification')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait before sending perform device connection request')
        # --------------------------------------------------------------------------------------------------------------
        sleep(PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE / 2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request')
        # --------------------------------------------------------------------------------------------------------------
        write_device_connect_response = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            report=SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING,
                pairing_slot_to_be_unpaired=device_index),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device connect response')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
            self, write_device_connect_response, SetPerformDeviceConnectionResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Device Disconnection notification is received')
        # --------------------------------------------------------------------------------------------------------------
        device_disconnection = ChannelUtils.get_only(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceDisconnection,
            check_first_message=False)
        self.assertEqual(obtained=int(Numeral(device_disconnection.disconnection_type)),
                         expected=DeviceDisconnection.PERMANENT_DISCONNECTION,
                         msg='Disconnection type in Device Disconnection notification is not as expected')
        self.assertEqual(obtained=int(Numeral(device_disconnection.pairing_slot)),
                         expected=device_index,
                         msg='Pairing Slot in Device Disconnection notification is not as expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Discovery Status notification is received only at the end of timeout')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_timeout_discovery_status_notification(
            self,
            start_time + float(PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE),
            0.5,
            PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE * 5 / 100)

        # TODO :
        #  check device discovery notification received until end of timeout
        #  check LED #3 is still blinking fast, LEDs #1 and #2 are off

        self.testCaseChecked("FNT_DEV_DISC_0019")
    # end def test_unpairing_while_discovering

    @features('BLEDeviceDiscovery')
    @features('RcvWithDevice')
    @features('BLEDevicePairing')
    @level('Functionality')
    @expectedFailure  # https://jira.logitech.io/browse/BPRO-39
    def test_perform_device_pairing_rejected_while_discovering(self):
        """
        When a PerformDevicePairing.Pairing is received, and the command is processed, it stops the on-going Discovery.
        When all pairing slots are used, the PerformDevicePairing.Pairing is rejected (ERR_TOO_MANY_DEVICES). If a
        discovery is on-going, discovery should stop because pairing has been processed.
        """
        self._setup_rcv_with_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Pair all slots')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_program_nvs = True
        DevicePairingTestUtils.pair_all_slots(self)

        # TODO :
        #  - device enter pairing mode
        #  - check LED #3 is blinking fast, LEDs #1 and #2 are off

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Start Discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Start Discovery notification')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Perform device connection request')
        # --------------------------------------------------------------------------------------------------------------
        perform_device_connect_req = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=HexList('00' * 6),
                emu_2buttons_auth_method=True)
        err_resp = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            report=perform_device_connect_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_CONNECTION_DISCONNECTION,
            [Hidpp1ErrorCodes.ERR_TOO_MANY_DEVICES])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check discovery status notification : Discovery Stop and No Error')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.STOP, DiscoveryStatus.ErrorType.NO_ERROR)

        # TODO :
        #  check device discovery notification are not received until end of timeout
        #  check LED #3 is still blinking fast, LEDs #1 and #2 are off

        self.testCaseChecked("FNT_DEV_DISC_0020")
    # end def test_perform_device_pairing_rejected_while_discovering

    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_perform_device_pairing_with_error_while_discovering(self):
        """
        When a PerformDevicePairing.Pairing is received, and the command is processed, it stops the on-going Discovery.
        When a PerformDevicePairing is received with several authentication methods at the same time, the
        PerformDevicePairing.Pairing is rejected (ERR_INVALID_PARAM_VALUE). If a discovery is on-going,
        discovery should continue because pairing command is not processed.
        """
        self._setup_rcv_with_device()

        self.button_stimuli_emulator.enter_pairing_mode()
        # TODO :
        #  - check LED #3 is blinking fast, LEDs #1 and #2 are off

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Start Discovery')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self)
        start_time = perf_counter()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Start Discovery notification')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 'Perform device connection' request with error (several authentication method "
                                 "at the same time)")
        # --------------------------------------------------------------------------------------------------------------
        perform_device_connection_req = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            bluetooth_address=HexList('00' * 6),
            emu_2buttons_auth_method=True,
            passkey_auth_method=True,
        )
        err_resp = ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self),
            report=perform_device_connection_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_CONNECTION_DISCONNECTION,
            [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE]
        )

        DiscoveryTestUtils.check_discovery_notifications_until_timeout(
            self,
            start_time + float(PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE),
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            float(PerformDeviceDiscovery.DiscoveryTimeout.TESTABLE_MIN),
            log_check=3
        )

        # TODO :
        #  check LED #3 is still blinking fast, LEDs #1 and #2 are off

        self.testCaseChecked("FNT_DEV_DISC_0021")
    # end def test_perform_device_pairing_with_error_while_discovering
    
# end class SharedDiscoveryTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
