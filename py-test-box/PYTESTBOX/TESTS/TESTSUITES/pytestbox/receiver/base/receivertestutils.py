#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.base.receivertestutils
:brief:  Unified interface for helpers requiring multiple features for receiver
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/05/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import perf_counter
from time import sleep

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pychannel.channelinterfaceclasses import LogitechReportType
from pychannel.throughreceiverchannel import ThroughGotthardReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesGetInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceExtendedPairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformationResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetGothardDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetGothardDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetQuadDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetQuadDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.reset import SetResetRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.basetestutils import CommonTestUtilsInterface
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils
from pytestbox.receiver.base.receiverinfoutils import ReceiverInfoUtils
from pytestbox.receiver.base.receivermanagedeactivatablefeaturesauthutils import \
    ReceiverManageDeactivatableFeaturesAuthTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils
from pytransport.transportcontext import TransportContextException
from pyusb.libusbdriver import ChannelIdentifier
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReceiverTestUtils(ReceiverBaseTestUtils, CommonTestUtilsInterface):
    """
    Class to provide a unique interface for methods requiring multiple features utils.

    This is based on the facade design pattern idea.
    """
    RECEIVER_SWITCHING_TIME = 3.0

    # Logitech receivers PID
    USB_PID_GOTTHARD = LibusbDriver.USB_PID_GOTTHARD
    USB_PID_GRAVITY_BLE_PRO = 0xC546
    USB_PID_MEZZY_BLE_PRO = 0xC548

    class HIDppHelper(ReceiverBaseTestUtils.HIDppHelper, CommonTestUtilsInterface.HIDppHelper):
        # See ``ReceiverBaseTestUtils.HIDppHelper``
        @classmethod
        def activate_features(cls, test_case, manufacturing=False, compliance=False, gotthard=False,
                              device_index=None, port_index=None):
            # See ``CommonTestUtilsInterface.HIDppHelper.activate_features``
            if isinstance(test_case.current_channel, ThroughReceiverChannel):
                previous_channel = test_case.current_channel
                DeviceManagerUtils.set_channel(
                    test_case=test_case, new_channel=test_case.current_channel.receiver_channel)
            else:
                previous_channel = None
            # end if

            try:
                # Send 0xD0 Enable Test Mode Control
                TDETestUtils.set_check_test_mode(
                    test_case, test_mode_enable=TestModeControl.TestModeEnable.ENABLE_MANUFACTURING_TEST_MODE)

                # Send Manage Deactivatable Features Get Info to check if the manage deactivatable features feature is
                # supported, i.e. F9 & FA registers are supported
                if manufacturing or compliance or gotthard:
                    try:
                        test_case.clean_message_type_in_queue(
                            test_case.hidDispatcher.receiver_error_message_queue, Hidpp1ErrorCodes)
                        ReceiverManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_info(test_case)
                    except (AssertionError, QueueEmpty):
                        err_resp = test_case.getMessage(queue=test_case.hidDispatcher.receiver_error_message_queue,
                                                        class_type=Hidpp1ErrorCodes)
                        ReceiverBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                            test_case,
                            err_resp,
                            to_int(ManageDeactivatableFeaturesGetInfoRequest().sub_id),
                            to_int(ManageDeactivatableFeaturesGetInfoRequest().address),
                            [Hidpp1ErrorCodes.ERR_INVALID_ADDRESS, Hidpp1ErrorCodes.ERR_INVALID_SUBID])
                        return
                    # end try

                    # Start a session, send the password and enable the deactivatable features
                    ReceiverManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(
                        test_case,
                        manufacturing=manufacturing,
                        compliance=compliance,
                        gotthard=gotthard,
                        start_session=True,
                        device_index=device_index,
                        port_index=port_index)
                # end if
            finally:
                if previous_channel is not None:
                    DeviceManagerUtils.set_channel(test_case=test_case, new_channel=previous_channel)
                # end if
            # end try
        # end def activate_features
    # end class HIDppHelper

    class GotthardReceiver:
        """
        Class to provide interface to Gotthard receiver
        """
        GOTTHARD_TASK_ENABLER = BitStruct(Numeral(LinkEnablerInfo.ALL_MASK -
                                                  LinkEnablerInfo.KEYBOARD_MASK -
                                                  LinkEnablerInfo.MOUSE_MASK))
        CONNECTION_TIMEOUT = 1.0

        @classmethod
        def init_connection(cls, test_case, gotthard_device_index=1, assert_connection=True):
            """
            Connect device to Gotthard receiver

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param gotthard_device_index: Expected device index on Gotthard receiver - OPTIONAL
            :type gotthard_device_index: ``int``
            :param assert_connection: Flag to enable waiting for Device Connection notification - OPTIONAL
            :type assert_connection: ``bool``
            """
            device_connection_req = SetGothardDeviceConnectionRequest(
                connect_devices=0x07,
                device_number=0x00,
                open_lock_timeout=0x08,
                rssi_threshold=0x0A,
                lna_gain=0x00,
                aaf_gain=0x00,
                device_quad_id=HexList(test_case.f.PRODUCT.F_EQuadPID),
                device_quad_id_mask=0xFFFF,
                debug_mode=0x00,
                consecutives_messages_count=0x00,
                output_power=0x00,
                protocol=to_int(HexList(test_case.f.PRODUCT.F_IsGaming)))

            ChannelUtils.send(
                test_case=test_case,
                report=device_connection_req,
                channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetGothardDeviceConnectionResponse
            )

            ChannelUtils.clean_messages(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=DeviceConnection
            )

            # Reset device
            test_case.device_debugger.reset(soft_reset=False)

            if assert_connection:
                cls.assert_connection(test_case, gotthard_device_index)
            # end if

            through_gotthard_channels = DeviceManagerUtils.get_channels(
                test_case=test_case,
                channel_id=ChannelIdentifier(port_index=ChannelUtils.get_port_index(
                    test_case=test_case), device_index=gotthard_device_index))

            assert len(through_gotthard_channels) < 2, \
                "Cannot have 2 channels on the same port index and same device index"

            if len(through_gotthard_channels) == 0:
                new_channel = ThroughGotthardReceiverChannel(
                    receiver_channel=test_case.current_channel, device_index=gotthard_device_index)
                DeviceManagerUtils.add_channel_to_cache(test_case=test_case, channel=new_channel)
            else:
                # This means that there was just one channel found because of the assert before the if
                new_channel = through_gotthard_channels[0]
            # end if

            DeviceManagerUtils.set_channel(
                test_case=test_case, new_channel=new_channel, open_associated_channel=False)
        # end def init_connection

        @classmethod
        def assert_connection(cls, test_case, gotthard_device_index=1):
            """
            Assert connection is established

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param gotthard_device_index: Expected device index on Gotthard receiver - OPTIONAL
            :type gotthard_device_index: ``int``

            :raise: ``TestException`` if connection is not established
            """
            connected = False
            connection_timeout = cls.CONNECTION_TIMEOUT + test_case.config_manager.get_feature(
                test_case.config_manager.ID.STARTUP_TIME_COLD_BOOT) / 1000
            start_time = perf_counter()
            while not connected and perf_counter() - start_time < connection_timeout:
                device_connections = ChannelUtils.clean_messages(
                    test_case=test_case,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                    class_type=DeviceConnection)
                for device_connection in device_connections:
                    if int(Numeral(device_connection.pairing_slot)) == gotthard_device_index:
                        device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(
                            device_connection)
                        if int(Numeral(device_info_class.fromHexList(HexList(
                                device_connection.information)).device_info_link_status)) == \
                                DeviceConnection.LinkStatus.LINK_ESTABLISHED:
                            connected = True
                            break
                        # end if
                    # end if
                # end for
            # end while
            test_case.assertTrue(connected, "Connection should be established")
        # end def assert_connection
    # end class GotthardReceiver

    class EQuadReceiver:
        """
        Class to provide interface to EQuad receiver
        """

        @classmethod
        def get_paired_device_name(cls, test_case, receiver_usb_port, device_index):
            """
            Get the paired device name on the specific receiver

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param receiver_usb_port: The receiver usb port
            :type receiver_usb_port: ``int``
            :param device_index: The device index
            :type device_index: ``int``

            :return: The paired device name
            :rtype: ``str | None``
            """
            DeviceManagerUtils.switch_channel(test_case=test_case,
                                              new_channel_id=ChannelIdentifier(port_index=receiver_usb_port))
            device_name_req = GetEQuadDeviceNameRequest(NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN
                                                        + device_index)
            test_case.send_report_to_device(device_name_req)
            sleep(0.5)
            resp = test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_response_queue,
                                                         GetEQuadDeviceNameResponse)
            err_resp = test_case.clean_message_type_in_queue(
                test_case.hidDispatcher.receiver_error_message_queue, Hidpp1ErrorCodes)
            if len(err_resp) != 0 or len(resp) == 0:
                return None
            else:
                return resp[0].name_string
            # end if
        # end def get_paired_device_name

        @classmethod
        def unpair_equad_receiver(cls, test_case, receiver_usb_port, device_index=0x01):
            """
            Unpair an EQUAD receiver

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param receiver_usb_port: The receiver usb port
            :type receiver_usb_port: ``int``
            :param device_index: The device index - OPTIONAL
            :type device_index: ``int``
            """
            DeviceManagerUtils.switch_channel(test_case=test_case,
                                              new_channel_id=ChannelIdentifier(port_index=receiver_usb_port))
            if cls.get_paired_device_name(test_case, receiver_usb_port, device_index - 1) is not None:
                device_connection_req = SetQuadDeviceConnectionRequest(
                    connect_devices=QuadDeviceConnection.ConnectDevices.DISCONNECT_UNPLUG,
                    device_number=device_index,
                    open_lock_timeout=QuadDeviceConnection.OpenLockTimeout.USE_DEFAULT
                )

                test_case.send_report_wait_response(
                    report=device_connection_req,
                    response_queue=test_case.hidDispatcher.receiver_response_queue,
                    response_class_type=SetQuadDeviceConnectionResponse)
            # end if
        # end def unpair_equad_receiver
    # end class EQuadReceiver

    class CrushReceiver(EQuadReceiver):
        """
        Class to provide interface to Crush receiver
        """

        equad_info: GetTransceiverEQuadInformationResponse = None
        pairing_info: GetEQuadDevicePairingInfoResponse = None
        extended_pairing_info: GetEQuadDeviceExtendedPairingInfoResponse = None
        equad_name: GetEQuadDeviceNameResponse = None
        fw_information: GetFwVersionResponse = None

        @classmethod
        def pairing(cls, test_case):
            """
            Pair to a gaming mouse

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(
                test_case=test_case, text="Fetch pairing info from crush receiver to enable mimic_close_lock()")
            # ----------------------------------------------------------------------------------------------------------
            cls.fetch_pairing_info(test_case=test_case)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg="Unpair the crush receiver to open lock")
            # ----------------------------------------------------------------------------------------------------------
            cls.unpair_equad_receiver(
                test_case=test_case, receiver_usb_port=PortConfiguration.CRUSH_RECEIVER_PORT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg="Power off-on the DUT")
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.power_off_device(test_case=test_case)
            DeviceBaseTestUtils.UsbHubHelper.turn_off_all_generic_usb_ports(
                test_case=test_case, ports_to_turn_on=(PortConfiguration.CRUSH_RECEIVER_PORT,))

            DeviceBaseTestUtils.power_on_device(test_case=test_case)
            # Wait device connected to crush receiver
            sleep(3)

            DeviceBaseTestUtils.UsbHubHelper.turn_on_all_generic_usb_ports(test_case=test_case)

            # The test environment setup requires crush receiver had been paired and without connection to the paired
            # device.
            channel = DeviceManagerUtils.get_channel(
                test_case=test_case,
                channel_id=ChannelIdentifier(port_index=PortConfiguration.CRUSH_RECEIVER_PORT, device_index=1))
            try:
                channel.is_device_connected()
                test_case.current_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(channel.hid_dispatcher)
            except Exception:
                del channel
                raise
            # end try

            DeviceManagerUtils.set_channel(test_case=test_case, new_channel=channel)
        # end def pairing

        @classmethod
        def fetch_pairing_info(cls, test_case):
            """
            Fetch crush receiver pairing information to enable mimic_close_lock()

            Note:
            The test environment requires the crush receiver had been paired before using the method

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Fetch crush receiver pairing information")
            # ----------------------------------------------------------------------------------------------------------
            equad_info, pairing_info, extended_pairing_info, equad_name, fw_information = \
                ReceiverTestUtils.get_receiver_nv_pairing_info(test_case=test_case)

            cls.equad_info = equad_info
            cls.pairing_info = pairing_info
            cls.extended_pairing_info = extended_pairing_info
            cls.equad_name = equad_name
            cls.fw_information = fw_information
        # end def fetch_pairing_info

        @classmethod
        def force_close_lock(cls, test_case):
            """
            Write pairing information with a corrupted LTK to force lock state closure

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``

            :raise ``AssertionError``: If the fetch_pairing_info method was not called before
            """
            assert cls.equad_info is not None

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Restore pairing information to close lock")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverTestUtils.perform_receiver_pre_pairing_sequence(test_case=test_case,
                                                                    equad_info=cls.equad_info,
                                                                    pairing_info=cls.pairing_info,
                                                                    extended_pairing_info=cls.extended_pairing_info,
                                                                    equad_name=cls.equad_name,
                                                                    long_term_key=HexList([0] * 16),
                                                                    skip_link_established_verification=True)
        # end def force_close_lock
    # end class CrushReceiver

    @staticmethod
    def reset_receiver(test_case, skip_link_established_verification=False):
        """
        Reset receiver with HID++ command

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param skip_link_established_verification: Flag indicating that the method bypasses the link established
                                                   notification verification
        :type skip_link_established_verification: ``bool``

        :raise ``AssertionError``: If no receiver channel is available
        """
        assert isinstance(test_case.current_channel, (UsbReceiverChannel, ThroughReceiverChannel)), \
               "No Receiver channel available"
        backup_channel = None
        if isinstance(test_case.current_channel, ThroughReceiverChannel):
            backup_channel = test_case.current_channel
            DeviceManagerUtils.set_channel(test_case=test_case, new_channel=test_case.current_channel.receiver_channel)
        # end if

        if not test_case.current_channel.is_link_enabled(link_report_type=LogitechReportType.HIDPP):
            ChannelUtils.close_channel(test_case=test_case)
            ChannelUtils.open_channel(test_case=test_case, link_enabler=BitStruct(Numeral(LinkEnablerInfo.HID_PP_MASK)))
        # end if
        reset_req = SetResetRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        try:
            ChannelUtils.send_only(test_case=test_case, report=reset_req)
        except TransportContextException as e:
            if e.get_cause() not in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                raise
            # end if
        # end try

        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=test_case)
        ChannelUtils.set_idle(test_case=test_case)
        ChannelUtils.set_hidpp_reporting(test_case=test_case, enable=True)

        if backup_channel:
            DeviceManagerUtils.set_channel(test_case=test_case, new_channel=backup_channel)
        # end if

        if not skip_link_established_verification:
            # Add some time to let the receiver enter discovery mode
            sleep(0.5)

            # Add a device reconnection retry mechanism
            retry_counter = 5
            for count in range(retry_counter):
                try:
                    test_case.button_stimuli_emulator.user_action()
                    ChannelUtils.wait_through_receiver_channel_link_status(
                        test_case=test_case, channel=test_case.current_channel,
                        link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED)
                    break
                except (AssertionError, QueueEmpty):
                    if count == retry_counter - 1:
                        raise
                    # end if
                # end try
            # end for
        # end if
    # end def reset_receiver

    @staticmethod
    def get_receiver_port_indexes(test_case, pid, skip=None):
        """
        Get receiver port indexes from PID

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param pid: Receiver PID to search
        :type pid: ``int``
        :param skip: Port indexes to skip - OPTIONAL
        :type skip: list of ``int``

        :return: Receiver port indexes
        :rtype: ``list``
        """
        skip = [] if skip is None else skip
        receiver_port_indexes = []
        for port in test_case.device.USB_CHANNEL_MAPPING:
            if test_case.device.USB_CHANNEL_MAPPING[port].get_usb_pid() == pid and port not in skip:
                receiver_port_indexes.append(port)
            # end if
        # end for
        return receiver_port_indexes
    # end def get_receiver_port_indexes

    @classmethod
    def get_receiver_port_index(cls, test_case, pid, skip=None):
        """
        Get receiver port index from PID

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param pid: Receiver PID to search
        :type pid: ``int``
        :param skip: Port indexes to skip
        :type skip: list of ``int``

        :return: Receiver port index
        :rtype: ``int``
        """
        receiver_port_index = None
        receiver_port_indexes = cls.get_receiver_port_indexes(test_case, pid, skip)
        if len(receiver_port_indexes) > 0:
            receiver_port_index = receiver_port_indexes[0]
        # end if

        return receiver_port_index
    # end def get_receiver_port_index

    @classmethod
    def switch_to_receiver(
            cls, test_case, receiver_port_index, task_enabler=BitStruct(Numeral(LinkEnablerInfo.ALL_MASK))):
        """
        Switch to another receiver

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param receiver_port_index: Port index of the receiver to enable
        :type receiver_port_index: ``int``
        :param  task_enabler: Bitmap of polling tasks to be enabled - OPTIONAL
        :type task_enabler: ``BitStruct``
        """
        receiver_channel = DeviceManagerUtils.get_channel(
            test_case=test_case,
            channel_id=ChannelIdentifier(
                port_index=receiver_port_index, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER))

        assert receiver_channel is not None, f'Receiver channel not found for port index {receiver_port_index}'
        assert isinstance(receiver_channel, UsbChannel), \
            f'Wrong channel type for port index {receiver_port_index}. ' \
            f'It should be a UsbChannel, found a {type(receiver_channel)}'

        # Wait for the device to be connected
        ChannelUtils.wait_usb_ble_channel_connection_state(
            test_case=test_case, channel=receiver_channel, connection_state=True)

        if receiver_channel != test_case.current_channel:
            close_associated_channel = False if \
                isinstance(test_case.current_channel, ThroughReceiverChannel) and \
                receiver_channel == test_case.current_channel.receiver_channel else True

            ChannelUtils.close_channel(test_case=test_case, close_associated_channel=close_associated_channel)

            DeviceManagerUtils.set_channel(test_case=test_case, new_channel=receiver_channel, open_channel=False)
        # end if

        if not receiver_channel.is_open:
            receiver_channel.open(link_enabler=task_enabler)
            # Increase delay to enable the BLE Pro Attributes and the OS detection mechanisms to occur
            sleep(cls.RECEIVER_SWITCHING_TIME)
            ChannelUtils.set_hidpp_reporting(test_case=test_case, enable=True)
            ChannelUtils.set_idle(test_case=test_case)
        # end if
    # end def switch_to_receiver

    @classmethod
    def jump_on_bootloader(cls, test_case):
        """
        Request the receiver to jump on the bootloader (if it is not already in bootloader mode).

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        """
        # Write enter USB firmware upgrade mode
        try_counter = 0
        wanted_state = False
        while not wanted_state and try_counter < cls.ENTER_BTLDR_MAX_TRY:
            # noinspection PyBroadException
            try:
                DfuControlTestUtils.target_enter_into_dfu_mode(test_case=test_case)

                test_case.post_requisite_restart_in_main_application = True

                # We check again if the receiver is in bootloader mode
                test_case.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(
                    test_case=test_case, feature_id=Dfu.FEATURE_ID)
            except Exception:
                if try_counter >= cls.ENTER_BTLDR_MAX_TRY:
                    raise
                # end if
            # end try

            if test_case.bootloader_dfu_feature_id != 0:
                wanted_state = True
            else:
                try_counter += 1
            # end if
        # end while

        test_case.assertTrue(expr=wanted_state,
                             msg="Device did not jump on bootloader, tried {cls.ENTER_BTLDR_MAX_TRY} times")

        if try_counter > 0:
            test_case.log_warning(message=f"It took multiple tries to jump on bootloader: {try_counter}")
        # end if

        # Update configuration manager current expected mode
        test_case.config_manager.current_mode = test_case.config_manager.MODE.BOOTLOADER
    # end def jump_on_bootloader

    @classmethod
    def get_receiver_nv_pairing_info(cls, test_case, port_index=None):
        """
        Get Non-volatile and pairing information from receiver

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: (EQuadInfo, PairingInfo, ExtendedPairingInfo, EQuadName, FwInfo)
        :rtype: ``tuple[GetTransceiverEQuadInformationResponse, GetEQuadDevicePairingInfoResponse,
                        GetEQuadDeviceExtendedPairingInfoResponse, GetEQuadDeviceNameResponse, GetFwVersionResponse]``
        """
        port_index = port_index if port_index is not None else ChannelUtils.get_port_index(test_case=test_case)

        # switch to the receiver channel
        initial_device_index = ChannelUtils.get_device_index(test_case=test_case)
        ChannelUtils.close_channel(test_case=test_case)
        new_channel = DeviceManagerUtils.get_channel(
            test_case=test_case,
            channel_id=ChannelIdentifier(port_index=port_index, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER))
        DeviceManagerUtils.set_channel(test_case=test_case, new_channel=new_channel)

        # Get receiver pairing information
        equad_info = ReceiverInfoUtils.get_receiver_equad_info(test_case=test_case)
        pairing_info = ReceiverInfoUtils.get_receiver_pairing_info(test_case=test_case)
        extended_pairing_info = ReceiverInfoUtils.get_receiver_extended_pairing_info(test_case=test_case)
        equad_name = ReceiverInfoUtils.get_equad_device_name(test_case=test_case)
        fw_information = ReceiverInfoUtils.get_receiver_fw_information(test_case=test_case)

        # switch to the device channel
        ChannelUtils.close_channel(test_case=test_case)
        new_channel = DeviceManagerUtils.get_channel(
            test_case=test_case,
            channel_id=ChannelIdentifier(port_index=port_index, device_index=initial_device_index))
        DeviceManagerUtils.set_channel(test_case=test_case, new_channel=new_channel)

        return equad_info, pairing_info, extended_pairing_info, equad_name, fw_information
    # end def get_receiver_nv_pairing_info

    @classmethod
    def perform_receiver_pre_pairing_sequence(cls, test_case, equad_info, pairing_info,
                                              extended_pairing_info, equad_name, long_term_key,
                                              skip_link_established_verification=False):
        """
        Perform receiver pre-pairing for Unifying and Lightspeed receivers

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param equad_info: EQuad information
        :type equad_info: ``GetTransceiverEQuadInformationResponse``
        :param pairing_info: EQuad pairing information
        :type pairing_info: ``GetEQuadDevicePairingInfoResponse``
        :param extended_pairing_info: EQuad extended pairing information
        :type extended_pairing_info: ``GetEQuadDeviceExtendedPairingInfoResponse``
        :param equad_name: EQuad name information
        :type equad_name: ``GetEQuadDeviceNameResponse``
        :param long_term_key: Long term key
        :type long_term_key: ``HexList``
        :param skip_link_established_verification: Flag indicating that the method bypasses the link established
                                                   notification verification
        :type skip_link_established_verification: ``bool``
        """
        port_index = ChannelUtils.get_port_index(test_case=test_case)

        # switch to the receiver channel
        initial_device_index = ChannelUtils.get_device_index(test_case=test_case)
        ChannelUtils.close_channel(test_case=test_case)
        new_channel = DeviceManagerUtils.get_channel(
            test_case=test_case,
            channel_id=ChannelIdentifier(port_index=port_index, device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER))
        DeviceManagerUtils.set_channel(test_case=test_case, new_channel=new_channel)

        # Enable Manufacturing Test Mode
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=test_case, manufacturing=True)

        # Erase receiver pairing information
        ReceiverInfoUtils.erase_receiver_pairing_info(test_case=test_case)

        # Set receiver pairing information
        ReceiverInfoUtils.set_equad_info_to_receiver(test_case=test_case,
                                                     base_address=equad_info.base_address,
                                                     rf_channel_index=equad_info.rf_channel_index,
                                                     number_of_pairing_slots=equad_info.number_of_pairing_slots,
                                                     last_dest_id=equad_info.last_dest_id)
        ReceiverInfoUtils.set_device_pairing_info_to_receiver(
            test_case=test_case,
            destination_id=pairing_info.destination_id,
            default_report_interval=pairing_info.default_report_interval,
            device_quid=pairing_info.device_quid,
            equad_major_version=pairing_info.equad_major_version,
            equad_minor_version=pairing_info.equad_minor_version,
            equad_device_subclass=pairing_info.equad_device_subclass,
            equad_attributes=pairing_info.equad_attributes)
        ReceiverInfoUtils.set_device_extended_pairing_info_to_receiver(
            test_case=test_case,
            serial_number=extended_pairing_info.serial_number,
            report_types=extended_pairing_info.report_types,
            usability_info=extended_pairing_info.usability_info)
        ReceiverInfoUtils.set_device_name_to_receiver(test_case=test_case,
                                                      segment_length=equad_name.segment_length,
                                                      name_string=equad_name.name_string)
        ReceiverInfoUtils.set_ltk_to_receiver(test_case=test_case,
                                              aes_encryption_key_byte_1_to_6=long_term_key[0:6],
                                              aes_encryption_key_byte_9_to_16=long_term_key[8:])

        # Reset Receiver
        ReceiverTestUtils.reset_receiver(test_case=test_case,
                                         skip_link_established_verification=skip_link_established_verification)

        # switch to the device channel
        ChannelUtils.close_channel(test_case=test_case)
        new_channel = DeviceManagerUtils.get_channel(
            test_case=test_case,
            channel_id=ChannelIdentifier(port_index=port_index, device_index=initial_device_index))
        DeviceManagerUtils.set_channel(test_case=test_case, new_channel=new_channel)
    # end def perform_receiver_pre_pairing_sequence
# end class ReceiverTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# End of file
# ----------------------------------------------------------------------------------------------------------------------
