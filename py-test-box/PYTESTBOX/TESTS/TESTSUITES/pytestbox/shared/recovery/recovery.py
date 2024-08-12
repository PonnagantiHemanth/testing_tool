#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.recovery.recovery
:brief: Validate device Recovery feature
:author: Stanislas Cottard
:date: 2020/07/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from os.path import join
from time import sleep

from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuStatusEvent
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.features.common.dfu import Restart
from pyhid.hidpp.features.common.dfu import RestartResponse
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.devicerecovery import DeviceRecovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.recoveryutils import DisconnectMethod
from pytestbox.shared.base.recoveryutils import RecoveryTestUtils
from pytransport.transportcontext import TransportContextException


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedCommonRecoveryTestCase(CommonBaseTestCase, ABC):
    """
    Shared Common Recovery TestCase class
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        self.post_requisite_program_device_mcu_initial_state = False
        self.post_requisite_device_restart_in_main_application = False
        self.post_requisite_unpairing = False
        self.device_bootloader_dfu_feature_id = 0
        self.current_nvs_hex_file = None
        self.recovery_device_index = None

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS and UICR")
        # --------------------------------------------------------------------------------------------------------------
        memory_manager = self.device_memory_manager
        self.assertNotNone(obtained=memory_manager, msg="Device memory manager cannot be None for recovery tests")
        memory_manager.read_nvs(backup=True)

        # Enable HID notification
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

        if not self.f.PRODUCT.F_IsGaming:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Cancel all ongoing discovery')
            # ----------------------------------------------------------------------------------------------------------
            DiscoveryTestUtils.cancel_discovery(test_case=self)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Empty notification queue')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
            class_type=(DeviceDiscovery, DiscoveryStatus, DeviceRecovery, DeviceConnection, DeviceDisconnection))
        ChannelUtils.clean_messages(
            test_case=self,
            channel=ChannelUtils.get_receiver_channel(test_case=self),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))
    # end def setUp

    def tearDown(self):
        """
        Handle test post requisites
        """
        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            firmware_hex_file = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            firmware_hex_file = join(TESTS_PATH, "DFU_FILES", self.f.SHARED.DEVICES.F_DeviceHexFile)
        else:
            self.log_warning(message="Unknown target in ConfigurationManager")
            firmware_hex_file = None
        # end if

        # noinspection PyBroadException
        try:
            RecoveryTestUtils.tear_down_clean_up(test_case=self)
            sleep(.5)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            if not self.f.PRODUCT.F_IsGaming:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Cancel all ongoing discovery')
                # ------------------------------------------------------------------------------------------------------
                DiscoveryTestUtils.cancel_discovery(self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Empty notification queue')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.clean_messages(
                test_case=self,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=(DeviceDiscovery, DiscoveryStatus, DeviceRecovery, DeviceConnection, DeviceDisconnection))
            ChannelUtils.clean_messages(
                test_case=self,
                channel=ChannelUtils.get_receiver_channel(test_case=self),
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=(DeviceConnection, DeviceDisconnection))

            if self.post_requisite_unpairing:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Clean-up receiver pairing slot')
                # ------------------------------------------------------------------------------------------------------
                DevicePairingTestUtils.unpair_all(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel,
                                               open_channel=False, dump_current_hid_dispatcher=False)
                ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)
            # end if

            if self.post_requisite_program_device_mcu_initial_state:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Program the MCU back to its initial state')
                # ------------------------------------------------------------------------------------------------------
                if self.device_debugger is None:
                    self.log_warning(
                        message="Cannot perform \"Post-requisite#{post_requisite_number}: Program the MCU back to "
                                "its initial state\" because not debugger is present")
                else:
                    self.device_debugger.reload_file(
                        firmware_hex_file=firmware_hex_file,
                        nvs_hex_file=self.device_memory_manager.backup_nvs_parser.to_hex_file(), no_reset=True)
                    self.device_debugger.set_application_bit()
                    DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel,
                                                   open_channel=False, dump_current_hid_dispatcher=False)
                    ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)
                    CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(test_case=self)

                    # Empty hid_message_queue from HidMouse and HidKeyboard notifications generated by the reload_file
                    # call
                    ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    if not self._check_device_on_application():
                        self.post_requisite_device_restart_in_main_application = True
                    # end if
                    self.post_requisite_program_device_mcu_initial_state = False
                # end if
            # end if

            if self.post_requisite_device_restart_in_main_application:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Restart in Main Application mode')
                # ------------------------------------------------------------------------------------------------------
                self._device_jump_on_application()
            # end if

        except Exception:
            self.log_traceback_as_warning(supplementary_message=f"Error in {self.__class__.__name__}.tearDown:")
            # noinspection PyBroadException
            try:
                # Reload if an exception occurred to be sure to go back on the initial state
                if self.device_debugger is not None:
                    self.device_debugger.reload_file(
                        firmware_hex_file=firmware_hex_file,
                        nvs_hex_file=self.device_memory_manager.backup_nvs_parser.to_hex_file(), no_reset=True)
                    self.device_debugger.set_application_bit()
                    # Add time to let the device recover
                    sleep(2)

                    DeviceManagerUtils.set_channel(
                        test_case=self, new_channel=self.backup_dut_channel, dump_current_hid_dispatcher=False)
                else:
                    self.log_warning(
                        message=f"Could not even reload the hex file in the device: no debugger is present")
                # end if
            except Exception:
                self.log_traceback_as_warning(supplementary_message="Could not even reload the hex file in the device:")
            # end try
        # end try

        # End with super tearDown()
        super().tearDown()
    # end def tearDown

    def _device_jump_on_recovery_bootloader(self, discover_and_connect=True, pairing=False):
        """
        Get the device to jump on the recovery bootloader

        :param discover_and_connect: If True, the device in recovery is discovered and connected to
        :type discover_and_connect: ``bool``
        :param pairing: If True, perform pairing after connection. Only used if discover_and_connect = True
        :type pairing: ``bool``
        """
        self.post_requisite_device_restart_in_main_application = True
        RecoveryTestUtils.perform_user_actions_for_recovery(
            test_case=self, current_device_index=ChannelUtils.get_device_index(test_case=self))

        if discover_and_connect:
            if self.f.PRODUCT.F_IsGaming:
                entity_type = DeviceInformationTestUtils.get_active_entity_type(
                    test_case=self, device_index=ChannelUtils.get_device_index(test_case=self))
            else:
                RecoveryTestUtils.discover_and_connect_recovery_bootloader(test_case=self, pairing=pairing)
            # end if
            self.recovery_device_index = self.current_channel.device_index
        # end if
    # end def _device_jump_on_recovery_bootloader

    def _device_jump_on_application(self):
        """
        Get the device to jump on the application. If it is already on the application (using feature 0x0003), nothing
        will be done
        """
        if self._check_device_on_application(skip_warning=True):
            return
        # end if

        self.device_bootloader_dfu_feature_id = -1
        counter = 0
        while self.device_bootloader_dfu_feature_id != 0 and counter < 3:
            self.device_debugger.set_application_bit(no_reset=True)
            self.device_debugger.reset(soft_reset=False)

            DeviceManagerUtils.switch_channel(test_case=self, new_channel=self.backup_dut_channel)

            # We check again if the device is on the application
            if self._check_device_on_application():
                self.device_bootloader_dfu_feature_id = 0
                break
            else:
                counter += 1
            # end if
        # end while

        self.assertTrue(expr=self.device_bootloader_dfu_feature_id == 0, msg="Could not jump on application")
    # end def _device_jump_on_application

    def _check_device_on_application(self, skip_warning=False):
        """
        Check if the device is on application using feature 0x0003

        :param skip_warning: Flag to skip logging a warning - OPTIONAL
        :type skip_warning: ``bool``

        :return: True if on application, False otherwise
        """
        if isinstance(self.backup_dut_channel, UsbReceiverChannel):
            if not isinstance(self.current_channel, ThroughReceiverChannel):
                assert self.backup_through_receiver_channel is not None, \
                    "Cannot automatically switch to the right channel if it is not known"
                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_through_receiver_channel)
            # end if
        elif not isinstance(self.current_channel, type(self.backup_dut_channel)):
            DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        # end if

        # noinspection PyBroadException
        try:
            DeviceInformationTestUtils.check_active_entity_type_is_main_app(
                test_case=self,
                device_index=self.current_channel.device_index)
        except Exception:
            if not skip_warning:
                self.log_traceback_as_warning(
                    supplementary_message=f"Error in {self.__class__.__name__}.check_target_on_application:")
            # end if
            return False
        # end try

        # Update configuration manager current expected mode
        self.config_manager.current_mode = self.config_manager.MODE.APPLICATION
        self.post_requisite_device_restart_in_main_application = False
        self.post_requisite_program_device_mcu_initial_state = False
        return True
    # end def _check_device_on_application

    def _disconnect_device(self, disconnect_method, pairing_slot=None):
        """
        Validates the business case

        :param disconnect_method: Disconnect method to use
        :type disconnect_method: ``DisconnectMethod``
        :param pairing_slot: Pairing slot to use if disconnect method is
                             DISCONNECT_METHOD.PERFORM_DEVICE_PAIRING_AND_UNPAIRING
                             if None, the current device_index in recovery utils will be used
        :type pairing_slot: ``HexList`` or ``int``
        """
        if disconnect_method == DisconnectMethod.DFU_RESTART:
            # We check again the feature ID of 00D0 because if the device is on the application it won't have
            # this feature
            device_bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(
                test_case=self, feature_id=Dfu.FEATURE_ID)
            restart = Restart(device_index=self.current_channel.device_index,
                              feature_index=device_bootloader_dfu_feature_id,
                              fw_entity=0xFF)
            try:
                ChannelUtils.send_only(test_case=self, report=restart)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try

            """
            According to Restart specification:
            "This function may return an empty response or no response (device reset)."
            So we check that if there is a message it is a RestartResponse
            (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;hb=HEAD;f=doc/hidpp20/x00d0_dfu.ad)
            """
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.COMMON, class_type=RestartResponse,
                allow_no_message=True, timeout=.4)
        elif disconnect_method == DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING:
            if pairing_slot is None:
                pairing_slot = self.current_channel.device_index
            # end if
            request = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING,
                pairing_slot_to_be_unpaired=pairing_slot)

            ChannelUtils.send(
                test_case=self, report=request, response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetPerformDeviceConnectionResponse, channel=self.current_channel.receiver_channel)
        elif disconnect_method == DisconnectMethod.DEVICE_OFF_ON:
            RecoveryTestUtils.perform_restart_action_for_recovery(test_case=self)
        # end if
    # end def _disconnect_device

    def _wait_for_dfu_status(self, dfu_status_response, status, packet_number=None):
        """
        Wait for a DFU status (an optionally a packet number) either from the given response or from an event
        received later.

        :param dfu_status_response: Current response of the request
        :type dfu_status_response: ``DfuStatusResponse``
        :param status: Expected status (see in DfuStatusResponse.StatusValue)
        :type status: ``tuple[int]``
        :param packet_number: Expected packet number (Optional)
        :type packet_number: ``int`` or ``HexList``
        """
        while int(Numeral(dfu_status_response.status)) in DfuStatusResponse.StatusValue.WAIT_FOR_EVENT:
            message = ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, timeout=30)
            if isinstance(message, DfuStatusEvent):
                dfu_status_response = message
            # end if
        # end while

        self.assertTrue(expr=int(Numeral(dfu_status_response.status)) in status,
                        msg="The Dfu status differs from the expected one, received "
                            f"{int(Numeral(dfu_status_response.status))} and expected {status}")

        if packet_number is not None:
            self.assertEqual(expected=int(Numeral(packet_number)),
                             obtained=int(Numeral(dfu_status_response.pkt_nb)),
                             msg="The Dfu packet_number differs from the expected one")
        # end if
    # end def _wait_for_dfu_status

    def _perform_first_command_of_dfu(self, dfu_file_path=None):
        """
        Perform the first command of DFU: DfuStart. It will also create the DFU file parser objet

        :param dfu_file_path: The path of the DFU file to use - OPTIONAL
        :type dfu_file_path: ``str | None``

        :return: The DFU file parser object created
        :rtype: ``DfuFileParser``
        """
        # Get the supported version
        if self.f.PRODUCT.FEATURES.COMMON.DFU.F_Version_0:
            dfu_feature_version = 0
        elif self.f.PRODUCT.FEATURES.COMMON.DFU.F_Version_1:
            dfu_feature_version = 1
        elif self.f.PRODUCT.FEATURES.COMMON.DFU.F_Version_2:
            dfu_feature_version = 2
        elif self.f.PRODUCT.FEATURES.COMMON.DFU.F_Version_3:
            dfu_feature_version = 3
        else:
            assert False, "Version not specified"
        # end if

        self.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(test_case=self, feature_id=Dfu.FEATURE_ID)

        if dfu_file_path is None:
            if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
                dfu_file_name = self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName
            elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
                dfu_file_name = self.f.SHARED.DEVICES.F_DeviceApplicationDfuFileName
            else:
                raise ValueError(f"Unknown target type: {self.config_manager.current_target}")
            # end if
            dfu_file_path = join(TESTS_PATH, "DFU_FILES", dfu_file_name)
        # end if

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(self.current_channel.device_index)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)

        self.device_memory_manager.read_nvs()
        self.post_requisite_program_device_mcu_initial_state = True
        self.post_requisite_device_restart_in_main_application = False

        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)

        self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                  status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                  packet_number=0)

        return dfu_file_parser
    # end def _perform_first_command_of_dfu

    def _perform_dfu(self, skip_restart=False, dfu_file_path=None,
                     check_device_reconnection=True,
                     dfu_status=DfuStatusResponse.StatusValue.DFU_SUCCESS):
        """
        Perform a DFU

        :param skip_restart: Flag indicating to skip DFU restart procedure - OPTIONAL
        :type skip_restart: ``bool``
        :param dfu_file_path: The path of the DFU file to use - OPTIONAL
        :type dfu_file_path: ``str | None``
        :param check_device_reconnection: Flag indicating to check the device reconnection - OPTIONAL
        :type check_device_reconnection: ``bool``
        :param dfu_status: Expected status (see in DfuStatusResponse.StatusValue) - OPTIONAL
        :type dfu_status: ``tuple[int]``
        """
        dfu_file_parser = self._perform_first_command_of_dfu(dfu_file_path=dfu_file_path)
        sequence_number = 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=cmd_1, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                      status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                      packet_number=sequence_number)

            sequence_number += 1

            for i in range(len(program_data_list)):
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=program_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                          status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                          packet_number=sequence_number)

                sequence_number += 1
            # end for
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=cmd_2, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                      status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                      packet_number=sequence_number)

            sequence_number += 1

            for i in range(len(check_data_list)):
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=check_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                          status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                          packet_number=sequence_number)

                sequence_number += 1
            # end for
        # end for

        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.command_3, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                  status=dfu_status)

        if not skip_restart:
            # Clean DeviceConnection to avoid errors in next call to verify_recovery_disconnection due to
            # previous events
            ChannelUtils.clean_messages(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=DeviceConnection,
                channel=self.current_channel.receiver_channel)
            restart = Restart(device_index=self.current_channel.device_index,
                              feature_index=self.bootloader_dfu_feature_id,
                              fw_entity=dfu_file_parser.dfu_start_command.fw_entity)
            try:
                ChannelUtils.send_only(test_case=self, report=restart)
            except TransportContextException as e:
                if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                     TransportContextException.Cause.CONTEXT_ERROR_IO,
                                     TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                else:
                    raise
                # end if
            # end try

            """
            According to Restart specification:
            "This function may return an empty response or no response (device reset)."
            So we check that if there is a message it is a RestartResponse
            (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;hb=HEAD;f=doc/hidpp20/x00d0_dfu.ad)
            """
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.COMMON, class_type=RestartResponse,
                allow_no_message=True, timeout=.4)

            if check_device_reconnection:
                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.current_channel.receiver_channel)

                # Reload NVS for pairing keys
                self.device_debugger.reload_file(
                    nvs_hex_file=self.device_memory_manager.backup_nvs_parser.to_hex_file())

                RecoveryTestUtils.verify_recovery_disconnection(
                    test_case=self,
                    disconnection_method_used=DisconnectMethod.DFU_RESTART,
                    recovery_device_index=self.recovery_device_index,
                    application_device_index=self.original_device_index)

                DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
            # end if
        # end if
    # end def _perform_dfu

    def _perform_sd_and_app_dfu(self):
        """
        Validate a full DFU including the SoftDevice and the Application entities.
        """
        f = self.getFeatures()

        # SoftDevice DFU processing
        self._perform_dfu(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            check_device_reconnection=self.f.PRODUCT.F_IsGaming,
            dfu_status=DfuStatusResponse.StatusValue.ALL_DFU_SUCCESS)

        if not self.f.PRODUCT.F_IsGaming:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Clean-up receiver pairing slot and discover the device')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_all(self)
            RecoveryTestUtils.discover_and_connect_recovery_bootloader(test_case=self)
            self.recovery_device_index = self.current_channel.device_index
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Root.GetFeature(0x0003)')
        LogHelper.log_check(self, 'Device shall be in Bootloader mode')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=DeviceInformation.FEATURE_ID)
        DeviceInformationTestUtils.check_active_entity_type(
            test_case=self,
            device_index=ChannelUtils.get_device_index(test_case=self),
            entity_type=DeviceInformation.EntityTypeV1.BOOTLOADER)

        # Application DFU processing
        self._perform_dfu(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName))
    # end def _perform_sd_and_app_dfu
# end class SharedCommonRecoveryTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
