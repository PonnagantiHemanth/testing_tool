#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.connectionscheme.discovery
    :brief: Validates device discovery feature
    :author: Martin Cryonnet
    :date: 2020/03/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import time

from warnings import warn

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyharness.selector import features
from pyharness.extensions import level
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.connectionscheme.discovery import SharedDiscoveryTestCase
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import PerformDeviceDiscovery
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import GetPerformDeviceDiscoveryRequest
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import GetPerformDeviceDiscoveryResponse
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import SetPerformDeviceDiscoveryRequest
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import SetPerformDeviceDiscoveryResponse
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DiscoveryTestCase(SharedDiscoveryTestCase, ReceiverBaseTestCase):
    """
    Discovery TestCases
    """
    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_get_discovery_api(self):
        """
        Test Perform Device Discovery read short register command API
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Perform Device Discovery read request and wait for response')
        # ---------------------------------------------------------------------------
        perform_device_discovery = GetPerformDeviceDiscoveryRequest()

        perform_device_discovery_resp = self.send_report_wait_response(
            report=perform_device_discovery,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=GetPerformDeviceDiscoveryResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check response format')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.GetPerformDeviceDiscoveryResponseChecker.check_fields(
            self,
            perform_device_discovery_resp,
            GetPerformDeviceDiscoveryResponse,
            DiscoveryTestUtils.GetPerformDeviceDiscoveryResponseChecker.get_range_check_map()
        )

        self.testCaseChecked("FNT_DEV_DISC_0001")
    # end def test_discovery

    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_set_discovery_api(self):
        """
        Test Perform Device Discovery write short register command API with valid parameters values
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Perform Device Discovery read request and wait for the response')
        # ---------------------------------------------------------------------------
        perform_device_discovery = SetPerformDeviceDiscoveryRequest(
            discovery_timeout=PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
            discover_devices=PerformDeviceDiscovery.DiscoverDevices.NO_CHANGE)

        perform_device_discovery_resp = self.send_report_wait_response(
            report=perform_device_discovery,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetPerformDeviceDiscoveryResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Check response format')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=int(Numeral(perform_device_discovery_resp.padding)),
                         msg="Padding should be 0")

        self.testCaseChecked("FNT_DEV_DISC_0002")
    # end def test_set_discovery

    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_device_discovery_timeout_status_notification(self):
        """
        Perform Device Discovery with Discovery Timeout in valid range. Check Discovery Status Timeout notification
        is received at the end of the discovery timeout.

        Sequence diagram:
            SW -> Receiver: Perform Device Discovery (Discover HID Devices)
            SW <- Receiver: Discovery Status Notification (Discovery Start, No Error)
            ... Discovery Timeout ...
            SW <- Receiver: Discovery Status Notification (Stop, Timeout)
        """
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over discovery timeout significant values')
        # ----------------------------------------------------------------------------
        for discovery_timeout in [PerformDeviceDiscovery.DiscoveryTimeout.MIN,
                                  PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
                                  PerformDeviceDiscovery.DiscoveryTimeout.MAX]:

            if discovery_timeout == PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT:
                discovery_timeout_value = PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE
            else:
                discovery_timeout_value = discovery_timeout
            # end if

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send "Perform Device Discovery" write request with Discovery Timeout = '
                           f'{discovery_timeout}')
            # ---------------------------------------------------------------------------
            DiscoveryTestUtils.start_discovery(self, discovery_timeout)
            start_time = time.perf_counter()

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 1: Check Discovery Status notification is received with Start status')
            # ---------------------------------------------------------------------------
            DiscoveryTestUtils.check_status_notification(
                self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Wait until end of timeout and '
                           f'Test Check 2: Check Discovery Status notification is received only at the end of timeout')
            # ---------------------------------------------------------------------------
            DiscoveryTestUtils.check_timeout_discovery_status_notification(
                self,
                start_time + float(discovery_timeout_value),
                0.5,
                discovery_timeout_value * 5 / 100)
        # end for
        # ----------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("FNT_DEV_DISC_0005")
    # end def test_device_discovery_timeout_status_notification

    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_device_discovery_no_change_status_notification(self):
        """
        Perform Device Discovery Write command to start discovering then send command again with No Change.
        Discovery Status notification should be received at the end of initial timeout

        Sequence diagram:
            SW -> Receiver: Perform Device Discovery (Discover HID Devices)
            SW <- Receiver: Discovery Status Notification (Discovery Start, No Error)
            ... Wait ...
            SW -> Receiver: Perform Device Discovery (No Change)
            ... Discovery Timeout ...
            SW <- Receiver: Discovery Status Notification (Stop, Timeout)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send "Perform Device Discovery" write request to start discovery')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT)
        start_time = time.perf_counter()

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 1: Check Discovery Status notification is received with Start status')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Wait to let discovery start')
        # ---------------------------------------------------------------------------
        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.MIN))

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check no other discovery status are received')
        # ---------------------------------------------------------------------------
        disc_status = self.clean_message_type_in_queue(self.hidDispatcher.receiver_event_queue, DiscoveryStatus)
        self.assertListEqual(disc_status, [], f'No discovery status should be received since start discovery')

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 3: Wait until end of timeout and '
                       f'Test Check 3: Check Discovery Status notification is received only at the end of timeout')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.check_timeout_discovery_status_notification(
            self,
            start_time + float(PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE),
            0.5,
            PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE * 5 / 100)

        self.testCaseChecked("FNT_DEV_DISC_0007")
    # end def test_device_discovery_no_change_status_notification

    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_device_discovery_cancel_status_notification(self):
        """
        Perform Device Discovery Write command to start discovering then send command again to cancel discovery.
        Discovery Status Notification should be received with status Cancel and No error.

        Sequence diagram:
            SW -> Receiver: Perform Device Discovery (Discover HID Devices)
            SW <- Receiver: Discovery Status Notification (Discovery Start, No Error)
            ... Wait ...
            SW -> Receiver: Perform Device Discovery (Cancel Discovery)
            SW <- Receiver: Discovery Status Notification (Discovery Cancel, No Error)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send "Perform Device Discovery" write request')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 1: Check Discovery Status notification is received with Start status')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Wait to let discovery start')
        # ---------------------------------------------------------------------------
        time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.MIN))

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 2: Check no other discovery status is received so far')
        # ---------------------------------------------------------------------------
        disc_status = self.clean_message_type_in_queue(self.hidDispatcher.receiver_event_queue, DiscoveryStatus)
        self.assertListEqual(disc_status, [], f'No discovery status should be received since start discovery')

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 3: Send Perform Device Discovery to cancel discovery')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)
        self.clean_message_type_in_queue(self.hidDispatcher.receiver_event_queue, DeviceDiscovery)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 3: Check Discovery Status notification is received with status Cancel and '
                       f'No Error error type')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.CANCEL, DiscoveryStatus.ErrorType.NO_ERROR)

        self.testCaseChecked("FNT_DEV_DISC_0009")
    # end def test_device_discovery_cancel_status_notification

    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_restart_discovering_status_notification(self):
        """
        Press EasySwitch button to start advertising. Perform Device Discovery Write command to start discovering then
        send command again to restart discovering with a new timeout (shorter, equal or longer than initial one).
        Discovery Status notification should be received at start, restart and end of timeout.

        Sequence diagram:
            SW -> Receiver: Perform Device Discovery (Initial Timeout, Discover HID Devices)
            SW <- Receiver: Discovery Status Notification (Discovery Start, No Error)
            ... Wait ...
            SW -> Receiver: Perform Device Discovery (New Timeout, Discover HID Devices)
            SW <- Receiver: Discovery Status Notification (Discovery Start, No Error)
            ... New Discovery Timeout ...
            SW <- Receiver: Discovery Status Notification (Stop, Timeout)
        """
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over timeout significant values')
        # ----------------------------------------------------------------------------
        for new_discovery_timeout in [PerformDeviceDiscovery.DiscoveryTimeout.MIN,
                                      PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
                                      PerformDeviceDiscovery.DiscoveryTimeout.MAX]:

            if new_discovery_timeout == PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT:
                new_discovery_timeout_value = PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE
            else:
                new_discovery_timeout_value = new_discovery_timeout
            # end if

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send "Perform Device Discovery" write request to start discovery')
            # ---------------------------------------------------------------------------
            DiscoveryTestUtils.start_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT)
            initial_timeout_value = PerformDeviceDiscovery.DiscoveryTimeout.DEFAULT_VALUE

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 1: Check Discovery Status notification is received with Start status')
            # ---------------------------------------------------------------------------
            DiscoveryTestUtils.check_status_notification(
                self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Wait to let discovery start')
            # ---------------------------------------------------------------------------
            time.sleep(float(PerformDeviceDiscovery.DiscoveryTimeout.MIN))

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Check no other discovery is received so far')
            # ---------------------------------------------------------------------------
            disc_status = self.clean_message_type_in_queue(self.hidDispatcher.receiver_event_queue, DiscoveryStatus)
            self.assertListEqual(disc_status, [], f'No discovery status should be received since start discovery')

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send "Perform Device Discovery" write request')
            # ---------------------------------------------------------------------------
            DiscoveryTestUtils.start_discovery(self, new_discovery_timeout_value)
            start_time = time.perf_counter()

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 3: Check Discovery Status notification is received with Start status')
            # ---------------------------------------------------------------------------
            DiscoveryTestUtils.check_status_notification(
                self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 4: Wait until end of timeout and '
                           f'Test Check 4: Check Discovery Status notification is received only at the end of '
                           f'new timeout')
            # ---------------------------------------------------------------------------
            DiscoveryTestUtils.check_timeout_discovery_status_notification(
                self,
                start_time + float(new_discovery_timeout_value),
                0.5,
                new_discovery_timeout_value * 5 / 100)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 5: Wait until end of initial timeout')
            # ---------------------------------------------------------------------------
            time.sleep(float(initial_timeout_value))

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 5: Check no other Discovery Status notification is received')
            # ---------------------------------------------------------------------------
            disc_status = self.clean_message_type_in_queue(self.hidDispatcher.receiver_event_queue, DiscoveryStatus)
            self.assertListEqual(disc_status, [], f'No discovery status should be received since start discovery')
        # end for
        # ----------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("FNT_DEV_DISC_0011")
    # end def test_restart_discovering_status_notification

    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_disable_notifications_status_notifications(self):
        """
        No status notification should be sent if notifications are disabled
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Disable HID++ reporting')
        # ---------------------------------------------------------------------------
        self.enable_hidpp_reporting(False)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send multiple "Perform Device Discovery" which can create notifications')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self)
        DiscoveryTestUtils.perform_device_discovery(
            self, PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT, PerformDeviceDiscovery.DiscoverDevices.NO_CHANGE)
        DiscoveryTestUtils.cancel_discovery(self)
        DiscoveryTestUtils.start_discovery(self, PerformDeviceDiscovery.DiscoveryTimeout.MIN)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check no Discovery Status notification is received')
        # ---------------------------------------------------------------------------
        disc_status = self.clean_message_type_in_queue(self.hidDispatcher.receiver_event_queue, DiscoveryStatus)
        self.assertListEqual(disc_status, [], f'No discovery status should be received since start discovery')

        # Re-enable HID++ reporting
        self.enable_hidpp_reporting(True)

        self.testCaseChecked("FNT_DEV_DISC_0015")
    # end def test_disable_notifications_status_notifications

    @features('BLEDeviceDiscovery')
    @level('Functionality')
    def test_start_pairing_while_discovering(self):
        """
        When a PerformDevicePairing.Pairing is received, and the command is processed, it stops the on-going Discovery.
        When a PerformDevicePairing.Pairing is received, it stops the on-going Discovery, i.e. Discovery Status
        Notification is sent with values Discovery Stop & No Error when a PerformDevicePairing.Pairing is sent while
        a discovery is started.
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Send Start Discovery')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.start_discovery(self)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 1: Check Start Discovery notification')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.START, DiscoveryStatus.ErrorType.NO_ERROR)

        # ---------------------------------------------------------------------------
        self.logTitle2("Test Step 2: Send 'Perform device connection' request")
        # ---------------------------------------------------------------------------
        write_device_connect_response = self.send_report_wait_response(
            report=SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=HexList('00' * 6),
                emu_2buttons_auth_method=True
            ),
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetPerformDeviceConnectionResponse
        )

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check device connect response')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
            self, write_device_connect_response, SetPerformDeviceConnectionResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Check discovery status notification : Discovery Stop and No Error')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.check_status_notification(
            self, DiscoveryStatus.DeviceDiscoveryStatus.STOP, DiscoveryStatus.ErrorType.NO_ERROR)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Check Pairing Status notification is received after Discovery Status '
                       'notification')
        # ---------------------------------------------------------------------------
        pairing_status = self.getMessage(self.hidDispatcher.receiver_event_queue, PairingStatus)
        self.assertEqual(expected=PairingStatus.STATUS.PAIRING_START,
                         obtained=int(Numeral(pairing_status.device_pairing_status)),
                         msg='Device Pairing Status should be Start')
        self.assertEqual(expected=PairingStatus.ERROR_TYPE.NO_ERROR,
                         obtained=int(Numeral(pairing_status.error_type)),
                         msg='Error Type should be No Error')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Perform device connection request with Connect Devices = Cancel Pairing")
        # --------------------------------------------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.CANCEL_PAIRING)
        ChannelUtils.send(
            test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self), report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPerformDeviceConnectionResponse)

        self.testCaseChecked("FNT_DEV_DISC_0018")
    # end def test_start_pairing_while_discovering

    @features('BLEDeviceDiscovery')
    @level('Robustness')
    def test_set_discovery_timeout_out_of_range(self):
        """
        Test Perform Device Discovery write short register command with Discovery Timeout out of range
        """
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over timeout significant values')
        # ----------------------------------------------------------------------------
        for timeout in compute_sup_values(int(PerformDeviceDiscovery.DiscoveryTimeout.MAX)):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send Perform Device Discovery write request with timeout = {timeout}')
            # ---------------------------------------------------------------------------
            perform_device_discovery = SetPerformDeviceDiscoveryRequest(
                discovery_timeout=timeout,
                discover_devices=PerformDeviceDiscovery.DiscoverDevices.DISCOVER_HID_DEVICES)

            error_response = self.send_report_wait_response(
                report=perform_device_discovery,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------
            self.logTitle2(
                'Test Check 1: Check error ERR_INVALID_PARAM_VALUE returned by the device')
            # ----------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                             msg="The error_code parameter should be as expected")
        # end for
        # ----------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ----------------------------------------------------------------------------
        
        self.testCaseChecked("ROT_DEV_DISC_0001")
    # end def test_set_discovery_timeout_out_of_range

    @features('BLEDeviceDiscovery')
    @level('Robustness')
    def test_set_discover_devices_out_of_range(self):
        """
        Test Perform Device Discovery write short register with Discover Devices out of range
        """
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over discover devices significant values')
        # ----------------------------------------------------------------------------
        for discover_devices in compute_sup_values(int(max(PerformDeviceDiscovery.DiscoverDevices))):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send Perform Device Discovery write request with Discover Devices ='
                           f' {discover_devices}')
            # ---------------------------------------------------------------------------
            perform_device_discovery = SetPerformDeviceDiscoveryRequest(
                discovery_timeout=PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
                discover_devices=discover_devices)

            error_response = self.send_report_wait_response(
                report=perform_device_discovery,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------
            self.logTitle2(
                'Test Check 1: Check error ERR_INVALID_PARAM_VALUE returned by the device')
            # ----------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE,
                             msg="The error_code parameter should be as expected")
        # end for
        # ----------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_DEV_DISC_0002")
    # end def test_set_discover_devices_out_of_range

    @features('BLEDeviceDiscovery')
    @level('Robustness')
    def test_write_perform_device_discovery_p2_ignored(self):
        """
        Test Perform Device Discovery write short register command padding ignored
        """
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over padding significant values')
        # ----------------------------------------------------------------------------
        for p2 in compute_sup_values(HexList(Numeral(SetPerformDeviceDiscoveryRequest.DEFAULT.P2,
                                                   SetPerformDeviceDiscoveryRequest.LEN.P2 // 8))):
            # ----------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send Perform Device Discovery request with p2 = {p2}')
            # ----------------------------------------------------------------------------
            perform_device_discovery = SetPerformDeviceDiscoveryRequest(
                discovery_timeout=PerformDeviceDiscovery.DiscoveryTimeout.MIN,
                discover_devices=PerformDeviceDiscovery.DiscoverDevices.NO_CHANGE)

            perform_device_discovery.p2 = p2

            perform_device_discovery_response = self.send_report_wait_response(
                report=perform_device_discovery,
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=SetPerformDeviceDiscoveryResponse)

            # ----------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check padding is zero in response')
            # ----------------------------------------------------------------------------
            DiscoveryTestUtils.MessageChecker.check_padding_is_zero(self, perform_device_discovery_response)
        # end for
        # ----------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_DEV_DISC_0003")
    # end def test_write_perform_device_discovery_p2_ignored

    @features('BLEDeviceDiscovery')
    @level('Robustness')
    def test_read_perform_device_discovery_r0_ignored(self):
        """
        Test Perform Device Discovery read short register command padding ignored
        """
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over padding significant values')
        # ----------------------------------------------------------------------------
        for r0 in compute_sup_values(
                HexList(Numeral(GetPerformDeviceDiscoveryRequest.DEFAULT.R0,
                                GetPerformDeviceDiscoveryRequest.LEN.R0 // 8))):
            # ----------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send Perform Device Discovery request with r0 = {r0}')
            # ----------------------------------------------------------------------------
            perform_device_discovery = GetPerformDeviceDiscoveryRequest()
            perform_device_discovery.r0 = r0

            perform_device_discovery_response = self.send_report_wait_response(
                report=perform_device_discovery,
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=GetPerformDeviceDiscoveryResponse)

            # ----------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check padding is zero in response')
            # ----------------------------------------------------------------------------
            DiscoveryTestUtils.GetPerformDeviceDiscoveryResponseChecker.check_fields(
                self,
                perform_device_discovery_response,
                GetPerformDeviceDiscoveryResponse,
                DiscoveryTestUtils.GetPerformDeviceDiscoveryResponseChecker.get_range_check_map()
            )
        # end for
        # ----------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_DEV_DISC_0004")
    # end def test_read_perform_device_discovery_r0_ignored

    @features('BLEDeviceDiscovery')
    @level('Robustness')
    def test_perform_device_discovery_sub_id_out_of_range(self):
        """
        Test Perform Device Discovery with invalid Sub Id raises an error
        """
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over sub id significant values')
        # ----------------------------------------------------------------------------
        for sub_id in [Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER]:
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send Perform Device Discovery request with Sub Id = {sub_id}')
            # ---------------------------------------------------------------------------
            perform_device_discovery = SetPerformDeviceDiscoveryRequest(
                discovery_timeout=PerformDeviceDiscovery.DiscoveryTimeout.MIN,
                discover_devices=PerformDeviceDiscovery.DiscoverDevices.NO_CHANGE)
            perform_device_discovery.sub_id = sub_id

            error_response = self.send_report_wait_response(
                report=perform_device_discovery,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error code returned by the device')
            # ----------------------------------------------------------------------------
            if sub_id in [Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER]:
                self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                                 expected=Hidpp1ErrorCodes.ERR_INVALID_ADDRESS,
                                 msg=f'The error_code parameter differs from the one expected (sub id = {sub_id})')
            else:
                self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                                 expected=Hidpp1ErrorCodes.ERR_INVALID_SUBID,
                                 msg=f'The error_code parameter differs from the one expected (sub id = {sub_id})')
        # end for
        # ----------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_DEV_DISC_0005")
    # end def test_perform_device_discovery_sub_id_out_of_range

    @features('BLEDeviceDiscovery')
    @level('Robustness')
    def test_perform_device_discovery_device_index_out_of_range(self):
        """
        Perform Device Discovery with Device Index greater than number of pairing slots shall raise an error
        """
        # ----------------------------------------------------------------------------
        self.logTitle2(f'Test Loop over device index significant values')
        # ----------------------------------------------------------------------------
        test_list = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        test_list.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        for device_index in test_list:
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send Perform Device Discovery write request with Device Index ='
                           f' {device_index}')
            # ---------------------------------------------------------------------------
            perform_device_discovery = SetPerformDeviceDiscoveryRequest(
                discovery_timeout=PerformDeviceDiscovery.DiscoveryTimeout.MIN,
                discover_devices=PerformDeviceDiscovery.DiscoverDevices.NO_CHANGE)
            perform_device_discovery.device_index = device_index

            error_response = ChannelUtils.send(
                test_case=self,
                report=perform_device_discovery,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------
            self.logTitle2(
                'Test Check 1: Check error ERR_UNKNOWN_DEVICE returned by the device')
            # ----------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                             msg="The error_code parameter differs from the one expected")
        # end for
        # ----------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_DEV_DISC_0006")
    # end def test_perform_device_discovery_device_index_out_of_range

    @features('BLEDeviceDiscovery')
    @features('BLEDevicePairing')
    @level('Robustness')
    def test_perform_device_discovery_while_pairing(self):
        """
        Perform Device Discovery while Perform Device Pairing is on going. The Discovery should be rejected with error
        code ERR_BUSY.
        """
        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send Perform Device Connection write request')
        # ----------------------------------------------------------------------------
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            emu_2buttons_auth_method=True)

        self.send_report_wait_response(report=write_device_connect,
                                       response_queue=self.hidDispatcher.receiver_response_queue,
                                       response_class_type=SetPerformDeviceConnectionResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for a start pairing status notification')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send Perform Device Discovery write request')
        # ----------------------------------------------------------------------------
        perform_device_discovery = SetPerformDeviceDiscoveryRequest(
            discovery_timeout=PerformDeviceDiscovery.DiscoveryTimeout.USE_DEFAULT,
            discover_devices=PerformDeviceDiscovery.DiscoverDevices.DISCOVER_HID_DEVICES)

        error_response = self.send_report_wait_response(
            report=perform_device_discovery,
            response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)

        # ----------------------------------------------------------------------------
        self.logTitle2(
            'Test Check 2: Check error ERR_BUSY returned by the device')
        # ----------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                         expected=Hidpp1ErrorCodes.ERR_BUSY,
                         msg="The error_code parameter differs from the one expected")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Perform device connection request with Connect Devices = Cancel Pairing")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.cancel_pairing(self)

        self.testCaseChecked("ROT_DEV_DISC_0007")
    # end def test_perform_device_discovery_while_pairing
# end class DiscoveryTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
