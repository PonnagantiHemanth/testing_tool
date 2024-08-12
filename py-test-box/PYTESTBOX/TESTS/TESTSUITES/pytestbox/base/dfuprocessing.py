#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.base.dfuprocessing
:brief: common dfu processing module for device and receiver targets
        A description of the BaseTestCase hierarchy could be found here
        https://drive.google.com/drive/folders/1YiT7CYc_1UIFwVzOwVkcoIa8hH5oTkwi
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/03/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join

import pysetup
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd1or2
from pyhid.hidpp.features.common.dfu import DfuFactory
from pyhid.hidpp.features.common.dfu import DfuStartV0
from pyhid.hidpp.features.common.dfu import DfuStatusEvent
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.bootloadertest import CommonBootloaderTestCase
from pytestbox.base.bootloadertest import DeviceBootloaderTestCase
from pytestbox.base.bootloadertest import ReceiverBootloaderTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CommonDfuTestCase(CommonBootloaderTestCase):
    """
    Device and receiver common Dfu processing test case class.
    """
    DFU_APP = 'application'
    DFU_IMAGE = 'images'

    # WARNING: This class is reserved for the use of the python API.
    # It is NOT related to any specifications (feature 0x0003 for example)
    class DfuEntity:
        MAIN_APPLICATION = 1
        BOOTLOADER = 2
        SOFTDEVICE = 3
        LIGHTNING = (4, 5,)
        IMAGES = 6
    # end class DfuEntity

    dfu_entity_to_file_name = {
        DfuEntity.MAIN_APPLICATION: "Regular_application.dfu",
        DfuEntity.BOOTLOADER: "Regular_bootloader.dfu",
        DfuEntity.SOFTDEVICE: "Regular_softdevice.dfu",
        DfuEntity.LIGHTNING[0]: "Regular_lightning_configuration.dfu",
        DfuEntity.LIGHTNING[1]: "Regular_lightning_configuration.dfu",
        DfuEntity.IMAGES: "Regular_images.dfu",
    }

    def _interleave_x_command_1(self, number_of_command_1_to_interleave):
        """
        Validate DFU interleave X commands 1.

        :param number_of_command_1_to_interleave: The number of command 1 to interleave, cannot be 0
        :type number_of_command_1_to_interleave: ``int``
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(pysetup.TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        number_of_command_1_to_create = number_of_command_1_to_interleave - (len(dfu_file_parser.command_1) - 1)

        if number_of_command_1_to_create > 0:
            size_last_packet = 16 if int(Numeral(dfu_file_parser.command_1[0][0].size)) % 16 == 0 \
                else int(Numeral(dfu_file_parser.command_1[0][0].size)) % 16
            sizes_of_data_packet_to_send = [16] * number_of_command_1_to_create
            sizes_of_data_packet_to_send[-1] = size_last_packet
            sizes_of_data_packet_to_send.reverse()

            for size_new_command_1 in sizes_of_data_packet_to_send:
                # Change size
                dfu_file_parser.command_1[0][0].size = int(Numeral(dfu_file_parser.command_1[0][0].size)) - \
                    size_new_command_1
                # Create new command 1 and its associated data
                new_command_1 = DfuCmdDataXCmd1or2.fromHexList(HexList(dfu_file_parser.command_1[0][0]))
                new_command_1.address = int(Numeral(new_command_1.address)) + int(Numeral(new_command_1.size))
                new_command_1.size = size_new_command_1
                new_command_1_data = [dfu_file_parser.command_1[0][1][-1]]
                # Insert the new command 1 at the right place
                dfu_file_parser.command_1.insert(1, (new_command_1, new_command_1_data))
                # Remove new command 1 data from first command 1 data
                dfu_file_parser.command_1[0] = (dfu_file_parser.command_1[0][0],
                                                dfu_file_parser.command_1[0][1][:-1])
            # end for
        # end if

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1[:-number_of_command_1_to_interleave]:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is command 1 '
                           f'reducing the size by {number_of_command_1_to_interleave} packets '
                           f'({16 * number_of_command_1_to_interleave} bytes)')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 3: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        log_step = 4
        log_check = 4
        for (cmd_1, program_data_list) in dfu_file_parser.command_1[-number_of_command_1_to_interleave:]:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : send again command 1 with size to 1 packet '
                           '(16 bytes)')
            # ----------------------------------------------------------------------------------------------------------
            cmd_1.functionIndex = sequence_number % 4
            dfu_status_response = self.send_report_wait_response(report=cmd_1,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)
            log_step += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)
            log_check += 1

            sequence_number += 1

            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu '
                               f'file is program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                program_data_list[i].functionIndex = sequence_number % 4
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            log_step += 1
            log_check += 1
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                           'command 2')
            # ----------------------------------------------------------------------------------------------------------
            cmd_2.functionIndex = sequence_number % 4
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)
            log_step += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            log_check += 1
            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of check data packets to be sent = '
                           f'{len(check_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu '
                               f'file is check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                check_data_list[i].functionIndex = sequence_number % 4
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
            log_step += 1
            log_check += 1
        # end for

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                       f'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)
        log_step += 1

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)
        log_check += 1

        log_step, log_check = DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=log_step,
            log_check=log_check)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step, log_check)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False
    # end def _interleave_x_command_1

    def _abort_dfu_at_different_time(self, after_command_number, dfu_file_name=None):
        """
        Performing a DFU and aborting after command 1, 2 or 3.
        For command 1 and 2, the abort will occur after the associated data.

        :param after_command_number: After which command the DFU will be aborted, can be 1, 2 or 3
        :type after_command_number: ``int``
        """
        dfu_file_name = dfu_file_name if dfu_file_name is not None else join(
            pysetup.TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_name,
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuStart : 16 first bytes of Regular_application.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of MinAddress_softdevice.dfu file is '
                           'command 1')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 3: Send dfuCmdDatax : next 16 bytes of MinAddress_softdevice.dfu file is '
                               f'program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        # Abort after command 1
        if after_command_number == 1:
            self._abort_dfu(log_step=4, log_check=4)
            return
        # end if

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 4: Send dfuCmdDatax : next 16 bytes of MinAddress_softdevice.dfu file is '
                           'command 2')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of check data packets to be sent = '
                           f'{len(check_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 5: Send dfuCmdDatax : next 16 bytes of MinAddress_softdevice.dfu file is '
                               f'check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 5: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        # Abort after command 2
        if after_command_number == 2:
            self._abort_dfu(log_step=6, log_check=6)
            return
        # end if

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 6: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        log_step = 7
        log_check = 7
        # Abort after command 3
        if after_command_number == 3:
            log_step, log_check = self._abort_dfu(log_step=log_step, log_check=log_check)
            # At this point we finish the DFU so no return
        # end if

        log_step, log_check = DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=log_step,
            log_check=log_check)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step, log_check)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False
    # end def _abort_dfu_at_different_time

    def _stop_and_start_new_dfu(self, first_dfu_entity, second_dfu_entity):
        """
        Start a DFU and stop it after command 2 (and check data) and perform another complete DFU

        :param first_dfu_entity: This first DfuEntity to use (should be one of the constant in DfuEntity)
        :type first_dfu_entity: ``int``
        :param second_dfu_entity: This second DfuEntity to use (should be one of the constant in DfuEntity)
        :type second_dfu_entity: ``int``

        :return: The last DFU file parser
        :rtype: ``DfuFileParser``
        """
        f = self.getFeatures()
        # Get first DFU file path
        if first_dfu_entity == self.DfuEntity.MAIN_APPLICATION:
            first_dfu_file_path = join(pysetup.TESTS_PATH,
                                       "DFU_FILES",
                                       f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)
        elif first_dfu_entity == self.DfuEntity.BOOTLOADER:
            first_dfu_file_path = join(pysetup.TESTS_PATH,
                                       "DFU_FILES",
                                       f.PRODUCT.FEATURES.COMMON.DFU.F_BootloaderDfuFileName)
        elif first_dfu_entity == self.DfuEntity.SOFTDEVICE:
            first_dfu_file_path = join(pysetup.TESTS_PATH,
                                       "DFU_FILES",
                                       f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName)
        elif first_dfu_entity in self.DfuEntity.LIGHTNING:
            first_dfu_file_path = join(
                pysetup.TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_LightningDfuFilesName[
                    self.DfuEntity.LIGHTNING.index(first_dfu_entity)])
        else:
            assert False, "First DFU entity unknown"
        # end if

        # Get second DFU file path
        if second_dfu_entity == self.DfuEntity.MAIN_APPLICATION:
            second_dfu_file_path = join(pysetup.TESTS_PATH,
                                        "DFU_FILES",
                                        f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)
        elif second_dfu_entity == self.DfuEntity.BOOTLOADER:
            second_dfu_file_path = join(pysetup.TESTS_PATH,
                                        "DFU_FILES",
                                        f.PRODUCT.FEATURES.COMMON.DFU.F_BootloaderDfuFileName)
        elif second_dfu_entity == self.DfuEntity.SOFTDEVICE:
            second_dfu_file_path = join(pysetup.TESTS_PATH,
                                        "DFU_FILES",
                                        f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName)
        elif second_dfu_entity in self.DfuEntity.LIGHTNING:
            second_dfu_file_path = join(
                pysetup.TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_LightningDfuFilesName[
                    self.DfuEntity.LIGHTNING.index(second_dfu_entity)])
        else:
            assert False, "First DFU entity unknown"
        # end if

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=first_dfu_file_path,
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Send dfuStart : 16 first bytes of '
                       f'{self.dfu_entity_to_file_name[first_dfu_entity]} file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of '
                           f'{self.dfu_entity_to_file_name[first_dfu_entity]} file is command 1')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 3: Send dfuCmdDatax : next 16 bytes of '
                               f'{self.dfu_entity_to_file_name[first_dfu_entity]} file is program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 4: Send dfuCmdDatax : next 16 bytes of '
                           f'{self.dfu_entity_to_file_name[first_dfu_entity]} file is command 2')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of check data packets to be sent = '
                           f'{len(check_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 5: Send dfuCmdDatax : next 16 bytes of '
                               f'{self.dfu_entity_to_file_name[first_dfu_entity]} is check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 5: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=second_dfu_file_path,
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Step 6: Send dfuStart : 16 first bytes of '
                       f'{self.dfu_entity_to_file_name[second_dfu_entity]} file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 7: Send dfuCmdData1 : next 16 bytes of '
                           f'{self.dfu_entity_to_file_name[second_dfu_entity]} file is command 1')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 7: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 8: Send dfuCmdDatax : next 16 bytes of '
                               f'{self.dfu_entity_to_file_name[second_dfu_entity]} file is program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 8: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 9: Send dfuCmdDatax : next 16 bytes of '
                           f'{self.dfu_entity_to_file_name[second_dfu_entity]} file is command 2')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 9: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of check data packets to be sent = '
                           f'{len(check_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 10: Send dfuCmdDatax : next 16 bytes of '
                               f'{self.dfu_entity_to_file_name[second_dfu_entity]} is check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 10: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 11: RAM content for check data is the expected one')
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Step 11: Send dfuCmdDatax : next 16 bytes of '
                       f'{self.dfu_entity_to_file_name[second_dfu_entity]} file is command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 12: Wait for dfuStatus with status = 0x02 or 0x06 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ALL_DFU_SUCCESS)

        return dfu_file_parser
    # end def _stop_and_start_new_dfu

    def _abort_dfu(self, log_step=0, log_check=0):
        """
        Abort a DFU by sending DfuStart with fwEntity = 0xFF.

        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``

        :return: The new log_step and log_check
        :rtype: ``tuple``
        """
        if log_step > 0:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step {log_step}: Send dfuStart with fwEntity = 0xFF')
            # ----------------------------------------------------------------------------------------------------------
        # end if
        f = self.getFeatures()
        dfu_start_class = self.get_dfu_start_class()
        dfu_start = dfu_start_class(device_index=self.deviceIndex,
                                    feature_index=self.bootloader_dfu_feature_id,
                                    fw_entity=0xFF,
                                    encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                    magic_str=self.format_magic_string_hex_list(
                                                        f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                                    flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                    secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))

        dfu_status_response = self.send_report_wait_response(report=dfu_start,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        if log_check > 0:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = 0')
            # ----------------------------------------------------------------------------------------------------------
        # end if
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        return log_step + 1, log_check + 1
    # end def _abort_dfu

    def bootloader_dfu_processing(self, dfu_file_path, bootloader_dfu_feature_id, log_step=0, log_check=0,
                                  restart_all=False, encrypt_algorithm=None, is_ble_service_changed_required=None):
        """
        Perform a DFU, if log_step and log_check are <=0, there is no log message.

        :param dfu_file_path: The path of the DFU file to use
        :type dfu_file_path: ``str``
        :param bootloader_dfu_feature_id: The DFU feature index in bootloader
        :type bootloader_dfu_feature_id: ``int``
        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``
        :param restart_all: Restart all entities at the end (if True) or only the entity updated (if False)
        :type restart_all: ``bool``
        :param encrypt_algorithm: The encryption algorithm to use in Dfu.EncryptionMode, if None no encryption will
                                  be done
        :type encrypt_algorithm: ``int``
        :param is_ble_service_changed_required: Flag to enable ble service changed notification verification
                                                - True when switching back to application
                                                - False after a SoftDevice update (Device stays in Bootloader mode)
        :type is_ble_service_changed_required: ``bool``

        :return: The new log_step and log_check
        :rtype: ``tuple``
        """
        # Get the supported version
        dfu_feature_version = self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.DFU)

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)
        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        if encrypt_algorithm is not None:
            if log_step > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step {log_step}: Encrypt the program data from the good.dfu file using '
                               f'{Dfu.AES_ENCRYPTION_MODE_STR_MAPPING[encrypt_algorithm]} algorithm and the '
                               f'project-specific key')
                # ------------------------------------------------------------------------------------------------------
                log_step += 1
            # end if

            if dfu_file_parser.dfu_start_command.encrypt != encrypt_algorithm:
                dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)
                dfu_file_parser.dfu_start_command.encrypt = encrypt_algorithm
                dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)
            else:
                self.logTrace(msg="Already encrypted using the right algorithm")
            # end if
        # end if

        if log_step > 0:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step {log_step}: Send dfuStart : 16 first bytes of Regular_application.dfu file')
            # ----------------------------------------------------------------------------------------------------------
            log_step += 1
        # end if
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        if log_check > 0:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = 0')
            # ----------------------------------------------------------------------------------------------------------
            log_check += 1
        # end if
        timeout = 60 if (dfu_file_parser.dfu_start_command.magic_str.ascii_converter() ==
                         self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesMagicString) else 30
        # end if
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number,
                                 timeout=timeout)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            if log_step > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step {log_step}: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu '
                               f'file is command 1')
                # ------------------------------------------------------------------------------------------------------
                log_step += 1
            # end if
            dfu_status_response = self.send_report_wait_response(report=cmd_1,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            if log_check > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = 1')
                # ------------------------------------------------------------------------------------------------------
                log_check += 1
            # end if
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            if log_step > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2('Test Loop over the number of program data packets to be sent = '
                               f'{len(program_data_list)}, packet number should start at 1')
                # ------------------------------------------------------------------------------------------------------
            # end if
            for i in range(len(program_data_list)):
                if log_step > 0:
                    # --------------------------------------------------------------------------------------------------
                    self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : next 16 bytes of '
                                   f'Regular_application.dfu file is program data packet {i + 1}')
                    # --------------------------------------------------------------------------------------------------
                    log_step += 1
                # end if
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                if log_check > 0:
                    # --------------------------------------------------------------------------------------------------
                    self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) '
                                   f'and pktNb = {sequence_number}')
                    # --------------------------------------------------------------------------------------------------
                    log_check += 1
                # end if
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            if log_step > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2('End Test Loop')
                # ------------------------------------------------------------------------------------------------------
            # end if
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            if log_step > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu '
                               f'file is command 2')
                # ------------------------------------------------------------------------------------------------------
                log_step += 1
            # end if
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            if log_check > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                log_check += 1
            # end if
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            if log_step > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2('Test Loop over the number of check data packets to be sent = '
                               f'{len(check_data_list)}, packet number should start at 1')
                # ------------------------------------------------------------------------------------------------------
            # end if
            for i in range(len(check_data_list)):
                if log_step > 0:
                    # --------------------------------------------------------------------------------------------------
                    self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : next 16 bytes of '
                                   f'Regular_application.dfu file is check data packet {i + 1}')
                    # --------------------------------------------------------------------------------------------------
                    log_step += 1
                # end if
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                if log_check > 0:
                    # --------------------------------------------------------------------------------------------------
                    self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x01 (Packet success) '
                                   f'and pktNb = {sequence_number}')
                    # --------------------------------------------------------------------------------------------------
                    log_check += 1
                # end if
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            if log_step > 0:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2('End Test Loop')
                # ------------------------------------------------------------------------------------------------------
            # end if
        # end for

        if log_step > 0:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step {log_step}: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file '
                           f'is command 3')
            # ----------------------------------------------------------------------------------------------------------
            log_step += 1
        # end if
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        if log_check > 0:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Wait for dfuStatus with status = 0x02 (DFU success)')
            # ----------------------------------------------------------------------------------------------------------
            log_check += 1
        # end if
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ALL_DFU_SUCCESS)
        if is_ble_service_changed_required is None:
            is_ble_service_changed_required = self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled
        # end if
        return DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=bootloader_dfu_feature_id,
            restart_all=restart_all,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=is_ble_service_changed_required,
            log_step=log_step,
            log_check=log_check)
    # end def bootloader_dfu_processing

    @staticmethod
    def format_magic_string_hex_list(magic_string):
        """
        Format the magic string in a byte list of DfuStartV0.LEN.MAGIC_STR.

        :param magic_string: The magic string to format
        :type magic_string: ``str or list or HexList``

        :return: The HexList object containing the formatted magic string
        :rtype: ``HexList``
        """
        byte_list = [0] * (DfuStartV0.LEN.MAGIC_STR // 8)

        for i in range(len(magic_string)):
            byte_list[i] = ord(magic_string[i]) if isinstance(magic_string, str) else magic_string[i]
        # end for

        return HexList(byte_list)
    # end def format_magic_string_hex_list

    def get_dfu_start_class(self):
        """
        Get the DfuStart class according to the version.

        :return: The DfuStart class
        """
        # Get the supported DfuStart class
        dfu_main_cls = DfuFactory.create(self.get_dfu_version())

        return dfu_main_cls.dfu_start_cls
    # end def get_dfu_start_class

    def wait_for_dfu_status(self, dfu_status_response, status, packet_number=None, timeout=30):
        """
        Wait for a DFU status (an optionally a packet number) either from the given response or from an event
        received later.

        :param dfu_status_response: Current response of the request
        :type dfu_status_response: ``DfuStatusResponse``
        :param status: Expected status (see in DfuStatusResponse.StatusValue)
        :type status: ``tuple<int>``
        :param packet_number: Expected packet number (Optional)
        :type packet_number: ``int | HexList``
        :param timeout: The timeout to wait for the event
        :type timeout: ``int``
        """
        while int(Numeral(dfu_status_response.status)) in DfuStatusResponse.StatusValue.WAIT_FOR_EVENT:
            message = self.getMessage(queue=self.hidDispatcher.event_message_queue, timeout=timeout)
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
    # end def wait_for_dfu_status

    def get_dfu_version(self):
        """
        Get the Dfu supported version.

        :return: version
        :rtype: ``int``
        """
        # Get the supported version
        return self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.DFU)
    # end def get_dfu_version
# end class CommonDfuTestCase


class DeviceDfuTestCase(DeviceBootloaderTestCase):
    """
    Device dfu processing test case with
    - bootloader supporting HID++ 2.0 protocol
    - application supporting HID++ 1.0 protocol
    """
    def perform_dfu(self, dfu_file_path, bootloader_dfu_feature_id, log_step=0, log_check=0, restart_all=False,
                    encrypt_algorithm=None):
        """
        Perform a DFU, if log_step and log_check are <=0, there is no log message.

        :param dfu_file_path: The path of the DFU file to use
        :type dfu_file_path: ``str``
        :param bootloader_dfu_feature_id: The DFU feature index in bootloader
        :type bootloader_dfu_feature_id: ``int``
        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``
        :param restart_all: Restart all entities at the end (if True) or only the entity updated (if False)
        :type restart_all: ``bool``
        :param encrypt_algorithm: The encryption algorithm to use in Dfu.EncryptionMode, if None no encryption will be done
        :type encrypt_algorithm: ``int``

        :return: The new log_step and log_check
        :rtype: ``tuple``
        """
        # Bootloader DFU processing
        self.bootloader_dfu_processing(dfu_file_path, bootloader_dfu_feature_id, log_step, log_check,
                                       restart_all, encrypt_algorithm)

        if log_step > 0:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step {log_step}: Send Root.GetFeature(0x0003)')
            # ----------------------------------------------------------------------------------------------------------
            log_step += 1
        # end if

        if log_check > 0:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check {log_check}: Device shall be in Main Application mode')
            # ----------------------------------------------------------------------------------------------------------
            log_check += 1
        # end if

        DeviceInformationTestUtils.check_active_entity_type_is_main_app(
            test_case=self,
            device_index=ChannelUtils.get_device_index(test_case=self))

        self.post_requisite_program_mcu_initial_state = False

        return log_step, log_check
    # end def perform_dfu
# end class DeviceDfuTestCase


class ReceiverDfuTestCase(ReceiverBootloaderTestCase):
    """
    Receiver dfu processing  test case with
    - bootloader supporting HID++ 2.0 protocol
    - application supporting HID++ 1.0 protocol
    """
    def perform_dfu(self, dfu_file_path, bootloader_dfu_feature_id, log_step=0, log_check=0, restart_all=False,
                    encrypt_algorithm=None):
        """
        Perform a DFU on a receiver, if log_step and log_check are <=0, there is no log message.

        :param dfu_file_path: The path of the DFU file to use
        :type dfu_file_path: ``str``
        :param bootloader_dfu_feature_id: The DFU feature index in bootloader
        :type bootloader_dfu_feature_id: ``int``
        :param log_step: Log step number, if <= 0 no log printed
        :type log_step: ``int``
        :param log_check: Log check number, if <= 0 no log printed
        :type log_check: ``int``
        :param restart_all: Restart all entities at the end (if True) or only the entity updated (if False)
        :type restart_all: ``bool``
        :param encrypt_algorithm: The encryption algorithm to use in Dfu.EncryptionMode, if None no encryption will be done
        :type encrypt_algorithm: ``int``

        :return: The new log_step and log_check
        :rtype: ``tuple``
        """
        # Bootloader DFU processing
        self.bootloader_dfu_processing(dfu_file_path, bootloader_dfu_feature_id, log_step, log_check,
                                       restart_all, encrypt_algorithm)

        self.enable_hidpp_reporting()

        self.post_requisite_program_mcu_initial_state = False

        return log_step, log_check
    # end def perform_dfu
# end class ReceiverDfuTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
