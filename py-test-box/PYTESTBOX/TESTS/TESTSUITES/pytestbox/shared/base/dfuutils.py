#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.dfuutils
:brief:  Helpers for DFU feature
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2020/09/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import perf_counter_ns
from time import sleep

from pychannel.channelinterfaceclasses import ChannelException
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.features.common.dfu import Restart
from pyhid.hidpp.features.common.dfu import RestartResponse
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytransport.transportcontext import TransportContextException


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on DFU feature
    """

    @staticmethod
    def send_dfu_restart_function(test_case, bootloader_dfu_feature_id=None, restart_all=True, dfu_file_parser=None,
                                  ble_service_changed_required=True, log_step=-1, log_check=-1,
                                  check_device_reconnection=True):
        """
        Send DFU restart and optionally verify device disconnection and reconnection.

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param bootloader_dfu_feature_id: The DFU feature id in bootloader - OPTIONAL
        :type bootloader_dfu_feature_id: ``int`` or ``None``
        :param restart_all: Enable restart of all supported entities - OPTIONAL
        :type restart_all: ``bool``
        :param dfu_file_parser: The DFU file parser, to get the target entity if restart_all is not enabled - OPTIONAL
        :type dfu_file_parser: ``DFUFileParser`` or ``None``
        :param ble_service_changed_required: Flag indicating if it is required to check if service changed
                                             notifications are received.
                                             This only applies to the BLE Pro protocol - OPTIONAL
        :type ble_service_changed_required: ``bool``
        :param log_step: Log step number, if <= 0 no log printed - OPTIONAL
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed - OPTIONAL
        :type log_check: ``int``
        :param check_device_reconnection: Does it wait for the device to reconnect or not - OPTIONAL
        :type check_device_reconnection: ``bool``
        """
        if bootloader_dfu_feature_id is None:
            if log_step > 0:
                # ---------------------------------------------------------------------------
                test_case.logTitle2(f'Test Step {log_step}: Send Root.GetFeature(0x00D0)')
                # ---------------------------------------------------------------------------
                log_step += 1
            # end if
            bootloader_dfu_feature_id = test_case.updateFeatureMapping(feature_id=Dfu.FEATURE_ID)
        # end if

        if log_step > 0:
            # ---------------------------------------------------------------------------
            test_case.logTitle2(f'Test Step {log_step}: Send restart with fwEntity = '
                                f'{0xFF if restart_all else int(Numeral(dfu_file_parser.dfu_start_command.fw_entity))}')
            # ---------------------------------------------------------------------------
            log_step += 1
        # end if

        # All the device connection event must be cleaned to get only the ones associated to the restart
        test_case.clean_message_type_in_queue(queue=test_case.hidDispatcher.receiver_connection_event_queue,
                                              class_type=DeviceConnection)

        restart = Restart(device_index=test_case.deviceIndex,
                          feature_index=bootloader_dfu_feature_id,
                          fw_entity=0xFF if restart_all else dfu_file_parser.dfu_start_command.fw_entity)
        try:
            test_case.send_report_to_device(report=restart)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        if log_check > 0:
            # ---------------------------------------------------------------------------
            test_case.logTitle2(f'Test Check {log_check}: This function may return an empty response or no response '
                                f'but no error. It will also trigger a disconnection and a reconnection of the '
                                f'communication, regardless of the protocol')
            # ---------------------------------------------------------------------------
            log_check += 1
        # end if
        # According to StartDfu specification:
        # "This function may return an empty response or no response (device reset)."
        # So we check that if there is a message it is a RestartResponse
        # (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;hb=HEAD;f=doc/hidpp20/x00d0_dfu.ad)
        test_case.get_first_message_type_in_queue(
            queue=test_case.hidDispatcher.common_message_queue,
            class_type=RestartResponse,
            timeout=0.4,
            allow_no_message=True)

        # This distinction is only to be done here because this part will happen for all protocols except Unifying.
        # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
        #  interesting to investigate a better solution
        if not check_device_reconnection:
            pass
        elif test_case.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
            DfuTestUtils.verify_communication_disconnection_then_reconnection(
                test_case=test_case,
                ble_service_changed_required=ble_service_changed_required)
        else:
            sleep(2)
        # end if

        return log_step, log_check
    # end def send_dfu_restart_function

    @staticmethod
    def is_main_app(test_case):
        """
        Check if firmware type is main application

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``

        :return: True if target is in main application
        :rtype: ``bool``
        """
        try:
            return (
                (test_case.config_manager.current_target == ConfigurationManager.TARGET.DEVICE and
                 DfuTestUtils.verify_device_on_fw_type(test_case=test_case,
                                                       fw_type=DeviceInformation.EntityTypeV1.MAIN_APP))
                or (test_case.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER and
                    DfuTestUtils.verify_receiver_on_fw_type(test_case=test_case,
                                                            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP))
            )
        except ChannelException as e:
            if e.get_cause() == ChannelException.Cause.ERROR_MESSAGE_RECEIVED:
                return False
            # end if
        # end try
    # end def is_main_app

    @classmethod
    def force_target_on_application(cls, test_case, check_required=False, hard_force=False):
        """
        Get the device to jump on the application. If it is already on the application (using feature 0x0003), nothing
        will be done.

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param check_required: Flag indicating to verify (assert) that the device is on application is done - OPTIONAL
        :type check_required: ``bool``
        :param hard_force: Flag indicating that the debugger will be used to force the device on application - OPTIONAL
                           Leverage the debugger method if ``True``, HID++ pipe otherwise (default)
        :type hard_force: ``bool``
        """
        if hard_force:
            is_main_app = False
        else:
            # noinspection PyBroadException
            try:
                with ChannelUtils.channel_open_state(test_case=test_case):
                    is_main_app = cls.is_main_app(test_case)
                    if not is_main_app:
                        cls.send_dfu_restart_function(test_case=test_case)
                        is_main_app = cls.is_main_app(test_case)
                    # end if
                # end with
            except Exception:
                # If the type cannot be verified, try the debugger method
                test_case.log_traceback_as_warning(
                    supplementary_message="The fw type cannot be verified, try the debugger method")
                is_main_app = False
            # end try
        # end if

        if not is_main_app:
            assert test_case.debugger is not None, "Could not jump on application with DFU restart function and no " \
                                                   "debugger present to force the jump on the application"
            if not hard_force:
                test_case.log_warning(message="Could not jump on application with DFU restart function. Force the jump "
                                              "on the application with debugger")
            # end if

            if test_case.config_manager.current_protocol == LogitechProtocol.USB and test_case.current_channel.is_open:
                ChannelUtils.close_channel(test_case=test_case)
            # end if

            # If the protocol is BLE, it is important not te reset the device after setting the application bit so that
            # a force service changed can be requested. This would then trigger the reset and multiple reset is avoided.
            is_ble = test_case.config_manager.current_protocol in [LogitechProtocol.BLE_PRO, LogitechProtocol.BLE]

            if test_case.companion_debugger is None:
                test_case.debugger.set_application_bit(no_reset=is_ble)
                if is_ble:
                    # In BLE, a service changed is forced to be sure to have the right state of the receiver
                    CommonBaseTestUtils.NvsHelper.force_service_changed(test_case=test_case)
                # end if
            else:
                test_case.debugger.stop()
                test_case.companion_debugger.stop()
                test_case.debugger.set_application_bit(no_reset=True)
                test_case.companion_debugger.writeMemory(test_case.companion_debugger.FMM_NOINIT_START_ADDR,
                                                         test_case.companion_debugger.DFU_NOT_REQUESTED)
                test_case.debugger.reset()
                test_case.companion_debugger.reset()
            # end if

            # This distinction is only to be done here because this part will happen for all protocols except Unifying.
            # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
            #  interesting to investigate a better solution
            if test_case.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=test_case, ble_service_changed_required=True)
            # end if
        # end if

        with ChannelUtils.channel_open_state(test_case=test_case):
            is_main_app = cls.is_main_app(test_case)
        # end with
        if check_required:
            test_case.assertTrue(expr=is_main_app, msg="Could not jump on application")
        elif not is_main_app:
            test_case.log_warning(message="Could not jump on application")
        # end if
    # end def force_target_on_application

    @staticmethod
    def verify_target_on_fw_type(test_case, fw_type):
        """
        Verify that the active entity type of the target is the wanted one.

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param fw_type: The wanted entity type
        :type fw_type: ``int``

        :return: True if the target is on the desired FW type
        :rtype: ``bool``
        """
        assert fw_type == DeviceInformation.EntityTypeV1.MAIN_APP or \
               fw_type == DeviceInformation.EntityTypeV1.BOOTLOADER, f"Unknown fw_type: {fw_type}"

        if test_case.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            to_return = DfuTestUtils.verify_device_on_fw_type(test_case=test_case, fw_type=fw_type)
        elif test_case.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            to_return = DfuTestUtils.verify_receiver_on_fw_type(test_case=test_case, fw_type=fw_type)
        else:
            raise ValueError(f'Unknown target configuration: {test_case.config_manager.current_target}')
        # end if

        if to_return:
            if fw_type == DeviceInformation.EntityTypeV1.MAIN_APP:
                # Update configuration manager current expected mode
                test_case.config_manager.current_mode = test_case.config_manager.MODE.APPLICATION
            elif fw_type == DeviceInformation.EntityTypeV1.BOOTLOADER:
                # Update configuration manager current expected mode
                test_case.config_manager.current_mode = test_case.config_manager.MODE.BOOTLOADER
            else:
                test_case.log_warning(message=f"Unknown fw_type: {fw_type}, should have assert")
            # end if
        # end if

        return to_return
    # end def verify_target_on_fw_type

    @staticmethod
    def verify_device_on_fw_type(test_case, fw_type):
        """
        Verify that the active entity type of the device is the wanted one.
        Values of entity type can be found in pyhid.hidpp.features.common.deviceinformation.DeviceInformation.

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param fw_type: The wanted entity type
        :type fw_type: ``int``

        :return: True if the device is on the desired FW type
        :rtype: ``bool``
        """
        active_entity_type = DeviceInformationTestUtils.get_active_entity_type(
            test_case=test_case, device_index=test_case.deviceIndex)

        if active_entity_type != fw_type:
            return False
        # end if

        return True
    # end def verify_device_on_fw_type

    @staticmethod
    def verify_receiver_on_fw_type(test_case, fw_type):
        """
        Verify that the active entity type of the receiver is the wanted one.
        Values of entity type can be found in pyhid.hidpp.features.common.deviceinformation.DeviceInformation.
        For now, only MAIN_APP and BOOTLOADER can be verified.

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param fw_type: The wanted entity type
        :type fw_type: ``int``

        :return: True if the device is on the desired FW type
        :rtype: ``bool``
        """
        if fw_type == DeviceInformation.EntityTypeV1.MAIN_APP:
            try:
                ChannelUtils.set_hidpp_reporting(test_case, force_send_unknown_channel_type=True)

                return True
            except (AssertionError, QueueEmpty):
                test_case.clean_message_type_in_queue(queue=test_case.hidDispatcher.receiver_error_message_queue,
                                                      class_type=object)
                return False
            # end try
        elif fw_type == DeviceInformation.EntityTypeV1.BOOTLOADER:
            return DfuTestUtils.verify_device_on_fw_type(test_case=test_case, fw_type=fw_type)
        else:
            raise ValueError("Entity type requested unknown: {fw_type}. "
                             "For now, only MAIN_APP and BOOTLOADER can be verified.")
        # end if
    # end def verify_receiver_on_fw_type

    @classmethod
    def send_dfu_start(cls, test_case, dfu_start_command, sequence_number=0):
        """
        Send DFU start command

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param dfu_start_command: The DFU Start command
        :type dfu_start_command: ``DfuStart command``
        :param sequence_number: Sequence number
        :type sequence_number: ``int``

        :return: Sequence number
        :rtype: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Send DFU start")
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=test_case,
            report=dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case,
                           msg=f"Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = {sequence_number}")
        # --------------------------------------------------------------------------------------------------------------
        test_case.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                      status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                      packet_number=sequence_number)
        sequence_number += 1
        return sequence_number
    # end def send_dfu_start

    @classmethod
    def send_program_data(cls, test_case, program_data_blocks, sequence_number):
        """
        Send program data

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param program_data_blocks: The program data blocks
        :type program_data_blocks: ``list[tuple]``
        :param sequence_number: Sequence number
        :type sequence_number: ``int``

        :return: Sequence number
        :rtype: ``int``
        """
        for (command_1, program_data_packets) in program_data_blocks:
            sequence_number = cls.send_program_data_block(test_case=test_case,
                                                          command_1=command_1,
                                                          data_packets=program_data_packets,
                                                          sequence_number=sequence_number)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="End program data blocks loop")
        # --------------------------------------------------------------------------------------------------------------
        return sequence_number
    # end def send_program_data

    @classmethod
    def send_program_data_block(cls, test_case, command_1, data_packets, sequence_number):
        """
        Send program data block

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param command_1: The command 1
        :type command_1: ``DFU command 1``
        :param data_packets: Data packets
        :type data_packets: ``list``
        :param sequence_number: Sequence number
        :type sequence_number: ``int``

        :return: Sequence number
        :rtype: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Send dfuCmdData - Command 1 - Supply program data")
        # --------------------------------------------------------------------------------------------------------------
        return cls.send_data_block(
            test_case=test_case, command=command_1, data_packets=data_packets, sequence_number=sequence_number)
    # end def send_program_data_block

    @classmethod
    def send_check_data(cls, test_case, check_data_blocks, sequence_number):
        """
        Send check data

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param check_data_blocks: The check data blocks
        :type check_data_blocks: ``list[tuple]``
        :param sequence_number: Sequence number
        :type sequence_number: ``int``

        :return: Sequence number
        :rtype: ``int``
        """
        for (command_2, check_data_packets) in check_data_blocks:
            sequence_number = cls.send_check_data_block(test_case=test_case,
                                                        command_2=command_2,
                                                        data_packets=check_data_packets,
                                                        sequence_number=sequence_number)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="End check data blocks loop")
        # --------------------------------------------------------------------------------------------------------------
        return sequence_number
    # end def send_check_data

    @classmethod
    def send_check_data_block(cls, test_case, command_2, data_packets, sequence_number):
        """
        Send check data block

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param command_2: The command 2
        :type command_2: ``DFU command 2``
        :param data_packets: Data packets
        :type data_packets: ``list``
        :param sequence_number: Sequence number
        :type sequence_number: ``int``

        :return: Sequence number
        :rtype: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Send dfuCmdData - Command 2 - Supply check data")
        # --------------------------------------------------------------------------------------------------------------
        return cls.send_data_block(
            test_case=test_case, command=command_2, data_packets=data_packets, sequence_number=sequence_number)
    # end def send_check_data_block

    @classmethod
    def send_data_block(cls, test_case, command, data_packets, sequence_number):
        """
        Send data block

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param command: The command (1 or 2)
        :type command: ``DFU command (1 or 2)``
        :param data_packets: Data packets
        :type data_packets: ``list``
        :param sequence_number: Sequence number
        :type sequence_number: ``int``

        :return: Sequence number
        :rtype: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Send dfuCmdData")
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=test_case,
            report=command,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case,
                           msg=f"Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = {sequence_number}")
        # --------------------------------------------------------------------------------------------------------------
        test_case.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                      status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                      packet_number=sequence_number)
        sequence_number += 1

        sequence_number = cls.send_data_packets(
            test_case=test_case, data_packets=data_packets, sequence_number=sequence_number)

        return sequence_number
    # end def send_data_block

    @classmethod
    def send_data_packets(cls, test_case, data_packets, sequence_number):
        """
        Send data packets

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param data_packets: Data packets
        :type data_packets: ``list``
        :param sequence_number: Sequence number
        :type sequence_number: ``int``

        :return: Sequence number
        :rtype: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg=f"Send {len(data_packets)} data packets")
        # --------------------------------------------------------------------------------------------------------------
        for index, data_packet in enumerate(data_packets):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f"Send data packet {index}")
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=test_case,
                report=data_packet,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse
            )

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case=test_case,
                msg=f"Wait for dfuStatus with status = Packet success (0x01) and pktNb = {sequence_number}")
            # ----------------------------------------------------------------------------------------------------------
            test_case.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                          status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                          packet_number=sequence_number)

            sequence_number += 1
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="End data packets loop")
        # --------------------------------------------------------------------------------------------------------------

        return sequence_number
    # end def send_data_packets

    @classmethod
    def send_check_and_validate_fw(cls, test_case, command_3, expected_status, sequence_number, status_time_limit=None):
        """
        Send check and validate firmware

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param command_3: The command 3
        :type command_3: ``DFU Command 3``
        :param expected_status: The expected status
        :type expected_status: ``DfuStatusResponse.StatusValue``
        :param sequence_number: Sequence number
        :type sequence_number: ``int``
        :param status_time_limit: Time limit to get DFU status - OPTIONAL
        :type status_time_limit: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Send dfuCmdData - Command 3 - Check and validate firmware")
        # --------------------------------------------------------------------------------------------------------------
        start_time = perf_counter_ns()
        dfu_status_response = ChannelUtils.send(
            test_case=test_case,
            report=command_3,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg=f"Wait for dfuStatus with status = {expected_status}")
        # --------------------------------------------------------------------------------------------------------------
        test_case.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                      status=expected_status,
                                      packet_number=sequence_number)
        end_time = perf_counter_ns()
        status_time = (end_time - start_time) * 1e-6
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, f"DFU Status time : {status_time}")
        # --------------------------------------------------------------------------------------------------------------

        if status_time_limit:
            test_case.assertLess(status_time, status_time_limit, "Time to get the status should stay under the limit")
        # end if
    # end def send_check_and_validate_firmware

    @classmethod
    def perform_device_firmware_update(cls, test_case, dfu_start_command, program_data, check_data, command_3,
                                       expected_status, status_time_limit=None):
        """
        Perform DFU

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param dfu_start_command: DFU Start command
        :type dfu_start_command: ``DFU Start command``
        :param program_data: Program data
        :type program_data: ``Command 1 program data``
        :param check_data: Check data
        :type check_data: ``Command 1 check data``
        :param command_3: DFU command 3
        :type command_3: ``DFU command 3``
        :param expected_status: The expected status
        :type expected_status: ``DfuStatusResponse.StatusValue``
        :param status_time_limit: Time limit to get DFU status - OPTIONAL
        :type status_time_limit: ``int``
        """
        sequence_number = cls.send_dfu_start(test_case=test_case, dfu_start_command=dfu_start_command)
        sequence_number = cls.send_program_data(
            test_case=test_case, program_data_blocks=program_data, sequence_number=sequence_number)
        sequence_number = cls.send_check_data(
            test_case=test_case, check_data_blocks=check_data, sequence_number=sequence_number)
        cls.send_check_and_validate_fw(test_case=test_case,
                                       command_3=command_3,
                                       expected_status=expected_status,
                                       sequence_number=sequence_number,
                                       status_time_limit=status_time_limit)
    # end def perform_device_firmware_update
# end class DfuTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
