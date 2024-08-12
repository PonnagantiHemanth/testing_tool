#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.force_pairing_test_cases
:brief: Validate LS2 connection scheme for Force Pairing test cases
:author: Zane Lu <zlu@logitech.com>
:date: 2021/06/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.features.common.forcepairing import ForcePairing
from pyhid.hidpp.features.common.forcepairing import GetCapabilities
from pyhid.hidpp.features.common.forcepairing import GetCapabilitiesResponse
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral, to_int
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.forcepairingutils import ForcePairingTestUtils
from pytestbox.device.ls2connectionscheme.forcepairing import ForcePairingBaseTestCase
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils
from pytestbox.receiver.base.receiverinfoutils import ReceiverInfoUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ForcePairingTestCases(ForcePairingBaseTestCase):
    """
    LS2 connection scheme - Force Pairing Test Cases
    """
    PAIRING_MODE_TIMEOUT = 1

    @features('Feature1500')
    @level('Interface')
    def test_validate_get_capabilities_api(self):
        """
        Validate getCapabilities API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1500.get_capabilities_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1500_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1500.get_capabilities_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate getCapabilities response format')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=report.deviceIndex,
                         obtained=response.deviceIndex,
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=report.featureIndex,
                         obtained=response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')
        self.assertEqual(expected=0,
                         obtained=to_int(response.force_pairing_timeout),
                         msg='The force pairing timeout shall be 0')
        self.assertEqual(expected=0,
                         obtained=to_int(response.force_pairing_action_type),
                         msg='The force pairing action type shall be 0 (no action)')

        self.testCaseChecked("INT_1500_0001")
    # end def test_validate_get_capabilities_api

    @features('Feature1500')
    @level('Interface')
    def test_validate_set_force_pairing_api(self):
        """
        Validate setForcePairing API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setForcePairing')
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1500.set_force_pairing_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1500_index,
            pairing_address=RandHexList(4))
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1500.set_force_pairing_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate setForcePairing response format')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=report.deviceIndex,
                         obtained=response.deviceIndex,
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=report.featureIndex,
                         obtained=response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')

        self.testCaseChecked("INT_1500_0002")
    # end def test_validate_set_force_pairing_api

    @features('Feature1500')
    @level('Business')
    def test_set_force_pairing_business_case_without_user_action(self):
        """
        Set Force Pairing business case on device without user action
        """
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.ls2_channel)
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'get the address of the keyboard receiver')
        # --------------------------------------------------------------------------------------------------------------
        equad_info_response = ReceiverInfoUtils.get_receiver_equad_info(self)
        rcv_base_address = equad_info_response.base_address

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'open lock the keyboard receiver (connect_devices=7)')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(
            self, PortConfiguration.LS2_RECEIVER_PORT,
            connect_devices=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'send setForcePairing request for the mouse receiver '
                                 'with the keyboard receiver address')
        # --------------------------------------------------------------------------------------------------------------
        channel_id = ChannelIdentifier(device_index=self.DUT_DEVICE_INDEX,
                                       port_index=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)
        device_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=channel_id)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=device_channel)
        ForcePairingTestUtils.HIDppHelper.set_force_pairing(test_case=self, pairing_address=rcv_base_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'check HID USB report from the keyboard receiver EP')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.ls2_channel)
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self,
            channel=self.current_channel,
            link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
            timeout=3)

        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("BUS_1500_0003")
    # end def test_set_force_pairing_business_case_without_user_action

    @features('Feature1500')
    @level('Business')
    def test_check_the_mouse_is_immediately_disconnected_from_mouse_receiver(self):
        """
        [w/o User Action] Check the mouse is immediately disconnected from the mouse receiver
        by generating some user actions (button pressed, XY displacement, wheel rotation, ...)
        and no HID report is sent back to the SW.
        """
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.ls2_channel)
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'get the address of the keyboard receiver')
        # --------------------------------------------------------------------------------------------------------------
        equad_info_response = ReceiverInfoUtils.get_receiver_equad_info(self)
        rcv_base_address = equad_info_response.base_address

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'open lock the keyboard receiver (connect_devices=7)')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(
            self, PortConfiguration.LS2_RECEIVER_PORT,
            connect_devices=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'send setForcePairing request for the mouse receiver '
                                 'with the keyboard receiver address')
        # --------------------------------------------------------------------------------------------------------------
        channel_id = ChannelIdentifier(device_index=self.DUT_DEVICE_INDEX,
                                       port_index=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)
        device_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=channel_id)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=device_channel)
        ForcePairingTestUtils.HIDppHelper.set_force_pairing(test_case=self, pairing_address=rcv_base_address)
        sleep(5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'check no HID USB report from the mouse receiver '
                                  'when clicking the mouse left button')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.pre_paired_channel)

        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)

        self.testCaseChecked("BUS_1500_0004")
    # end def test_check_the_mouse_is_immediately_disconnected_from_mouse_receiver

    @features('Feature1500')
    @features('NoHasImmersiveLighting')
    @level('Functionality')
    def test_check_the_mouse_shall_exit_the_pairing_mode_after_a_1_second_timeout(self):
        """
        [w/o User Action] The mouse shall exit the pairing mode after a 1 second timeout
        and go into deep sleep if no keyboard receiver is in range.
        """
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.ls2_channel)
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'get the address of the keyboard receiver')
        # --------------------------------------------------------------------------------------------------------------
        equad_info_response = ReceiverInfoUtils.get_receiver_equad_info(self)
        rcv_base_address = equad_info_response.base_address

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'power off the LS2 receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(self, channel=self.ls2_channel)
        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[True, False, False, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'send setForcePairing request for the mouse receiver '
                                 f'with the keyboard receiver address={rcv_base_address}')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.pre_paired_channel)
        ForcePairingTestUtils.HIDppHelper.set_force_pairing(test_case=self,
                                                            pairing_address=rcv_base_address,
                                                            device_index=self.DUT_DEVICE_INDEX)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 1 second')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.PAIRING_MODE_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'power on the LS2 receiver')
        # --------------------------------------------------------------------------------------------------------------
        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[True, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'check the mouse goes into deep sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_deep_sleep_current_consumption()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'check no USB HID report from the keyboard receiver')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.ls2_channel)
        DeviceBaseTestUtils.ButtonHelper.check_no_hid_report(self)

        self.testCaseChecked("FUN_1500_0005")
    # end def test_check_the_mouse_shall_exit_the_pairing_mode_after_a_1_second_timeout

    @features('Feature1500')
    @level('Functionality')
    def test_check_the_mouse_shall_reconnects_immediately_to_the_mouse_receiver_with_valid_pairing_address(self):
        """
        [w/o User Action] Check the mouse is no more in pairing mode when waking up the device after a pairing timeout
        and reconnects immediately to the mouse receiver.
        """
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.ls2_channel)
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'get the address of the keyboard receiver')
        # --------------------------------------------------------------------------------------------------------------
        equad_info_response = ReceiverInfoUtils.get_receiver_equad_info(self)
        rcv_base_address = equad_info_response.base_address

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'power off the LS2 receiver')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(self, channel=self.ls2_channel)
        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[True, False, False, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'send setForcePairing request for the mouse receiver '
                                 'with the keyboard receiver address')
        # --------------------------------------------------------------------------------------------------------------
        channel_id = ChannelIdentifier(device_index=self.DUT_DEVICE_INDEX,
                                       port_index=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)
        device_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=channel_id)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=device_channel)
        ForcePairingTestUtils.HIDppHelper.set_force_pairing(test_case=self,
                                                            pairing_address=rcv_base_address,
                                                            device_index=self.DUT_DEVICE_INDEX)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 1 second')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.PAIRING_MODE_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'power on the LS2 receiver')
        # --------------------------------------------------------------------------------------------------------------
        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[True, False, True, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'click the mouse button')
        LogHelper.log_check(self, 'check HID USB report from the mouse receiver')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.pre_paired_channel)
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FUN_1500_0006")
    # end def test_check_the_mouse_shall_reconnects_immediately_to_the_mouse_receiver_with_valid_pairing_address

    @features('Feature1500')
    @features('NoHasImmersiveLighting')
    @level('Functionality')
    def test_check_the_mouse_shall_enter_into_deep_sleep_mode_if_pairing_fails(self):
        """
        [w/o User Action] The mouse shall enter into deep sleep mode if the pairing procedure fails.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'send setForcePairing request for the mouse receiver '
                                 'with the invalid receiver address')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.MAX_WAIT_FOR_LED_OFF)

        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.pre_paired_channel)
        ForcePairingTestUtils.HIDppHelper.set_force_pairing(test_case=self,
                                                            pairing_address=RandHexList(4),
                                                            device_index=self.DUT_DEVICE_INDEX)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 1 second')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.PAIRING_MODE_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'the device shall go to deep sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_deep_sleep_current_consumption()

        self.testCaseChecked("FUN_1500_0007")
    # end def test_check_the_mouse_shall_enter_into_deep_sleep_mode_if_pairing_fails

    @features('Feature1500')
    @level('Functionality')
    def test_check_the_mouse_shall_reconnects_immediately_to_the_mouse_receiver_with_invalid_pairing_address(self):
        """
        [w/o User Action] Check the mouse is no more in pairing mode when waking up the device after a pairing failure
        and reconnects immediately to the mouse receiver.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'send setForcePairing request for the mouse receiver '
                                 'with the invalid receiver address')
        # --------------------------------------------------------------------------------------------------------------
        channel_id = ChannelIdentifier(device_index=self.DUT_DEVICE_INDEX,
                                       port_index=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)
        device_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=channel_id)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=device_channel)
        ForcePairingTestUtils.HIDppHelper.set_force_pairing(test_case=self, pairing_address=RandHexList(4))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'wait 1 second')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.PAIRING_MODE_TIMEOUT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'click the mouse button and check HID USB report from the mouse receiver')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.pre_paired_channel)

        self.button_stimuli_emulator.user_action()
        sleep(10)
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("FUN_1500_0008")
    # end def test_check_the_mouse_shall_reconnects_immediately_to_the_mouse_receiver_with_invalid_pairing_address

    @features('Feature1500')
    @level('ErrorHandling')
    def test_verify_invalid_function_index_error(self):
        """
        Validate Force Pairing robustness processing (Feature 0x1500)

        Tests function index error range [2..0xF]
        """
        for invalid_function_index in compute_wrong_range(
                [x for x in range(ForcePairing.MAX_FUNCTION_INDEX + 1)], max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetCapabilities with a wrong function index value')
            # ----------------------------------------------------------------------------------------------------------
            get_capabilities = self.feature_1500.get_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1500_index)
            get_capabilities.functionIndex = invalid_function_index

            get_capabilities_response = ChannelUtils.send(
                test_case=self,
                report=get_capabilities,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check InvalidFunctionId (0x07) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_capabilities_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for

        self.testCaseChecked("ERR_1500_0001")
    # end def test_verify_invalid_function_index_error

    @features('Feature1500')
    @level('Robustness')
    def test_verify_software_id_input_is_ignored_by_fw(self):
        """
        Validate getCapabilities softwareId are ignored
        """
        for software_id in compute_inf_values(GetCapabilities.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetCapabilities with a different software id')
            # ----------------------------------------------------------------------------------------------------------
            get_capabilities = self.feature_1500.get_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1500_index)
            get_capabilities.softwareId = software_id

            get_capabilities_response = ChannelUtils.send(
                test_case=self,
                report=get_capabilities,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=GetCapabilitiesResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetCapabilities response received')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_capabilities.deviceIndex,
                             obtained=get_capabilities_response.deviceIndex,
                             msg='The deviceIndex parameter differs from the one expected')
            self.assertEqual(expected=get_capabilities.featureIndex,
                             obtained=get_capabilities_response.featureIndex,
                             msg='The featureIndex parameter differs from the one expected')
            self.assertEqual(expected=0,
                             obtained=to_int(get_capabilities_response.force_pairing_timeout),
                             msg='The force pairing timeout shall be 0')
            self.assertEqual(expected=0,
                             obtained=to_int(get_capabilities_response.force_pairing_action_type),
                             msg='The force pairing action type shall be 0 (no action)')
        # end for

        self.testCaseChecked("ROB_1500_0002")
    # end def test_verify_software_id_input_is_ignored_by_fw

    @features('Feature1500')
    @level('Robustness')
    def test_verify_padding_bytes_shall_be_ignored_by_fw(self):
        """
        Validate getCapabilities padding bytes are ignored
        """
        for padding_byte in compute_sup_values(HexList(Numeral(GetCapabilities.DEFAULT.PADDING,
                                                               GetCapabilities.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetCapabilities with different value for padding')
            # ----------------------------------------------------------------------------------------------------------
            get_capabilities = self.feature_1500.get_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1500_index)
            get_capabilities.padding = padding_byte

            get_capabilities_response = ChannelUtils.send(
                test_case=self,
                report=get_capabilities,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=GetCapabilitiesResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetCapabilities response received')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_capabilities.deviceIndex,
                             obtained=get_capabilities_response.deviceIndex,
                             msg='The deviceIndex parameter differs from the one expected')
            self.assertEqual(expected=get_capabilities.featureIndex,
                             obtained=get_capabilities_response.featureIndex,
                             msg='The featureIndex parameter differs from the one expected')
            self.assertEqual(expected=0,
                             obtained=to_int(get_capabilities_response.force_pairing_timeout),
                             msg='The force pairing timeout shall be 0')
            self.assertEqual(expected=0,
                             obtained=to_int(get_capabilities_response.force_pairing_action_type),
                             msg='The force pairing action type shall be 0 (no action)')
        # end for

        self.testCaseChecked("ROB_1500_0003")
    # end def test_verify_padding_bytes_shall_be_ignored_by_fw

# end class ForcePairingTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
