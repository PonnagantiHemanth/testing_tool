#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
    :package: pytestbox.hidpp20.common.feature_00D0_functionality
    :brief: Shared HID++ 2.0 Common feature 0x00D0
    :author: Stanislas Cottard
    :date: 2019/09/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import random
from os.path import join
from time import sleep

# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd1or2
from pyhid.hidpp.features.common.dfu import DfuCmdDataXData
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.features.common.dfu import Restart
from pyhid.hidpp.features.common.dfu import RestartResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.dfuprocessing import CommonDfuTestCase
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.transportcontext import TransportContextException


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedDfuTestCaseFunctionality(CommonDfuTestCase):
    """
    Validates DFU Functionality TestCases
    """

    @features('Feature00D0')
    @features('NoGamingDevice')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationMaxSize(self):
        """
        @tc_synopsis    DFU with maximum number of CmdData blocks validation.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Add padding to Regular_application.dfu file to maximum program data size and '
                       'sign it to create MaxSize_application.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        app_size = 0
        for (cmd_1, _) in dfu_file_parser.command_1:
            app_size += int(Numeral(cmd_1.size))
        # end for

        # If the size of the last command 1 is not a multiple of the packet size, then the last packet has to be
        # padded with random values
        if int(Numeral(dfu_file_parser.command_1[-1][0].size)) % 16 != 0:
            for i in range(int(Numeral(dfu_file_parser.command_1[-1][0].size)) % 16, 16):
                dfu_file_parser.command_1[-1][1][-1].data[i] = random.randint(0, 255)
            # end for
            padding_last_block = 16 - (int(Numeral(dfu_file_parser.command_1[-1][0].size)) % 16)
        else:
            padding_last_block = 0
        # end if

        size_to_add = f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress - app_size - padding_last_block - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationValidityFlagSize

        packet_bytes = HexList([Dfu.DEFAULT.REPORT_ID_LONG, int(Numeral(self.deviceIndex)),
                                int(Numeral(self.bootloader_dfu_feature_id)), 0x0F] + [0]*16)

        # We chose to increase the first command 1 instead of creating a new one to avoid sending more command 1 than
        # the business case.
        dfu_file_parser.command_1[0][0].size = int(Numeral(dfu_file_parser.command_1[0][0].size)) + size_to_add + \
            padding_last_block

        for _ in range(size_to_add // 16):
            new_data_object = DfuCmdDataXData.fromHexList(packet_bytes)
            new_data_object.functionIndex = (dfu_file_parser.command_1[0][1][-1].functionIndex + 1) % 4
            for i in range(16):
                new_data_object.data[i] = random.randint(0, 255)
            # end for
            dfu_file_parser.command_1[0][1].append(new_data_object)
        # end for

        # If the now size of the first command 1 is not a multiple of the packet size, then a last packet with the last
        # byte(s) should be added
        if int(Numeral(dfu_file_parser.command_1[0][0].size)) % 16 != 0:
            new_data_object = DfuCmdDataXData.fromHexList(packet_bytes)
            new_data_object.functionIndex = (dfu_file_parser.command_1[0][1][-1].functionIndex + 1) % 4
            for i in range(size_to_add % 16):
                new_data_object.data[i] = random.randint(0, 255)
            # end for
            dfu_file_parser.command_1[0][1].append(new_data_object)
        # end if

        check_sequence = (dfu_file_parser.command_1[0][1][-1].functionIndex + 1) % 4

        if len(dfu_file_parser.command_1) > 1:
            dfu_file_parser.command_1[1][0].functionIndex = check_sequence
            check_sequence = (check_sequence + 1) % 4
            for program_data in dfu_file_parser.command_1[1][1]:
                program_data.functionIndex = check_sequence
                check_sequence = (check_sequence + 1) % 4
            # end for
        # end if

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            cmd_2.functionIndex = check_sequence
            check_sequence = (check_sequence + 1) % 4

            for check_data in check_data_list:
                check_data.functionIndex = check_sequence
                check_sequence = (check_sequence + 1) % 4

        dfu_file_parser.command_3.functionIndex = check_sequence

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_erase_and_flash = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of MaxSize_application.dfu file')
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
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is '
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
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'program data packet {i + 1}')
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
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'check data packet {i + 1}')
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of MaxSize_application.dfu file is '
                       'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=8,
            log_check=7)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=9, log_check=8)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0006")
    # end def test_ApplicationMaxSize

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationLowerSize(self):
        """
        @tc_synopsis    DFU with a fewer number of CmdData block (compared to the initial application).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Reduce program size of Regular_application.dfu file by 1 program quantum and sign '
                       'it to create MinSize_application.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        number_of_packet = DfuFileParser.get_number_of_program_data_packets(dfu_file_parser.dfu_start_command,
                                                                            dfu_file_parser.command_1[-1][0])
        dfu_file_parser.command_1[-1][0].size = int(Numeral(dfu_file_parser.command_1[-1][0].size)) - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram

        delta_number_of_packet = number_of_packet - \
            DfuFileParser.get_number_of_program_data_packets(dfu_file_parser.dfu_start_command,
                                                             dfu_file_parser.command_1[-1][0])

        assert delta_number_of_packet >= 0, "Since we are reducing the size, there cannot be more packets to be sent"

        # Delete unwanted packets after reducing the size
        for i in range(delta_number_of_packet):
            del dfu_file_parser.command_1[-1][1][-1]
        # end for

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of MinSize_application.dfu file')
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
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is '
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
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'program data packet {i + 1}')
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
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                           'command 2')
            # ----------------------------------------------------------------------------------------------------------
            cmd_2.functionIndex = sequence_number % 4
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is '
                               f'check data packet {i + 1}')
                # ------------------------------------------------------------------------------------------------------
                check_data_list[i].functionIndex = sequence_number % 4
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of MinSize_application.dfu file is '
                       'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0007")
    # end def test_ApplicationLowerSize

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_Interleave1Command1(self):
        """
        @tc_synopsis    Validate DFU interleave 1 commands 1.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has all steps and checks
        self._interleave_x_command_1(number_of_command_1_to_interleave=1)

        self.testCaseChecked("FNT_00D0_0008")
    # end def test_Interleave1Command1

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_Interleave2Command1(self):
        """
        @tc_synopsis    Validate DFU interleave 2 commands 1.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has all steps and checks
        self._interleave_x_command_1(number_of_command_1_to_interleave=2)

        self.testCaseChecked("FNT_00D0_0009")
    # end def test_Interleave2Command1

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_Interleave3Command1(self):
        """
        @tc_synopsis    Validate DFU interleave 3 commands 1.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has all steps and checks
        self._interleave_x_command_1(number_of_command_1_to_interleave=3)

        self.testCaseChecked("FNT_00D0_0010")
    # end def test_Interleave3Command1

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_Interleave4Command1(self):
        """
        @tc_synopsis    Validate DFU interleave 4 commands 1.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has all steps and checks
        self._interleave_x_command_1(number_of_command_1_to_interleave=4)

        self.testCaseChecked("FNT_00D0_0011")
    # end def test_Interleave4Command1

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationLowestAddress(self):
        """
        @tc_synopsis    DFU with lowest authorized address validation.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change program address of Regular_application.dfu file to lowest authorized '
                       'address and sign it to create MinAddress_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        dfu_file_parser.command_1[0][0].address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of MinAddress_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of MinAddress_application.dfu file is '
                           'command 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list)}, packet number should start at 1')
            # ---------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
                               f'program data packet {i+1}')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ---------------------------------------------------------------------------
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
                           'command 2')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and '
                           f'pktNb = {sequence_number}')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop over the number of check data packets to be sent = '
                           f'{len(check_data_list)}, packet number should start at 1')
            # ---------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
                               f'check data packet {i+1}')
                # ---------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Check 5: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ---------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('End Test Loop')
            # ---------------------------------------------------------------------------
        # end for

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
                       'command 3')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x02 (DFU success)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0012")
    # end def test_ApplicationLowestAddress

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationHighestAddress(self):
        """
        @tc_synopsis    DFU with highest authorized address validation.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change program address of Regular_application.dfu file to highest authorized '
                       'address, Reduce program size of Regular_application.dfu file to minimum program data size '
                       '(1 program quantum) and sign it to create MaxAddress_application.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        new_cmd_1 = dfu_file_parser.command_1[0][0]
        new_cmd_1.address = f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress - \
            f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram - f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationValidityFlagSize
        new_cmd_1.size = f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
        new_program_data = dfu_file_parser.command_1[0][1][:(f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram // 16)]
        if f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram % 16 != 0:
            new_program_data.append(
                dfu_file_parser.command_1[0][1][(f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram // 16)])
        # end if

        dfu_file_parser.command_1 = [(new_cmd_1, new_program_data)]

        if f.PRODUCT.FEATURES.COMMON.DFU.F_DfuInPlace:
            reset_vector_written_command_1 = DfuCmdDataXCmd1or2.fromHexList(HexList(dfu_file_parser.command_1[0][0]))
            # Load only the first 8 bytes of the soft device to ensure the reset vector is written
            reset_vector_written_command_1.address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress
            reset_vector_written_command_1.size = 8
            reset_vector_written_program_data = DfuCmdDataXData.fromHexList(HexList(dfu_file_parser.command_1[0][1][0]))
            # Append this block at the first place
            dfu_file_parser.command_1.insert(0, (reset_vector_written_command_1, [reset_vector_written_program_data]))
        # end if

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            min_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of MaxAddress_application.dfu file')
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
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of MaxAddress_application.dfu file is '
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
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of MaxAddress_application.dfu file is '
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

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of MaxAddress_application.dfu file is '
                           'command 2')
            # ----------------------------------------------------------------------------------------------------------
            cmd_2.functionIndex = sequence_number % 4
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of MaxAddress_application.dfu file is '
                               f'check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                check_data_list[i].functionIndex = sequence_number % 4
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of MaxAddress_application.dfu file is '
                       'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0013")
    # end def test_ApplicationHighestAddress

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_AllDataPacketDoubled(self):
        """
        @tc_synopsis    Sending a DFU with every data block sent twice to validate the sliding window mechanism
                        ('make it possible to re-send packets after a transmission error').

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
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
            self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of MinAddress_application.dfu file is '
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
                self.logTitle2(f'Test Step 3: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
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

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 4: Send again the same dfuCmdDatax : program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and '
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
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
                           'command 2')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 5: Wait for dfuStatus with status = 0x01 (Packet success) and '
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
                               f'check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 6: Wait for dfuStatus with status = 0x01 (Packet success) and '
                               f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Step 7: Send again the same dfuCmdDatax : check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 7: Wait for dfuStatus with status = 0x01 (Packet success) and '
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
        self.logTitle2('Test Step 8: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 8: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=9,
            log_check=9)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=10, log_check=10)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("FNT_00D0_0017")
    # end def test_AllDataPacketDoubled

    @features('Feature00D0')
    @features('Feature00D0MaxProgramQuantum', 16)
    @level('Time-consuming')
    @services('Debugger')
    def test_EachData1ProgramQuantum(self):
        """
        @tc_synopsis    Sending a DFU interleaving a command 1 with size = 1 program quantum bytes before each 1
                        program quantum bytes data block. 1 program quantum is supposedly lower or equal to a packet
                        size (16 bytes).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Reformat command 1 and program data of Regular_application.dfu file to a sequence '
                       'of command 1 with size 1 program quantum followed by program data with padding if needed to '
                       'create 1QuantumSequence_application.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        all_new_command_1 = []
        function_index = 1
        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            address_packet = int(Numeral(cmd_1.address))
            current_size = int(Numeral(cmd_1.size))
            for program_data in program_data_list:
                packet_size = 16 if current_size > 16 else current_size
                # logically a packet size should be dividable by the program quantum
                for i in range(packet_size // f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram):
                    new_cmd_1 = DfuCmdDataXCmd1or2.fromHexList(HexList(cmd_1))
                    new_cmd_1.address = address_packet
                    new_cmd_1.size = f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                    new_cmd_1.functionIndex = function_index
                    address_packet += f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                    current_size -= f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                    function_index = (function_index + 1) % 4
                    new_program_data = DfuCmdDataXData.fromHexList(HexList(program_data))
                    new_program_data.data = program_data.data[
                                                    i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram:
                                                    (i + 1) * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram] + \
                        HexList([0] * (16 - f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram))
                    new_program_data.functionIndex = function_index
                    function_index = (function_index + 1) % 4
                    all_new_command_1.append((new_cmd_1, [new_program_data]))
                # end for
            # end for
        # end for
        dfu_file_parser.command_1 = all_new_command_1

        # Change function index for the sliding window in command 2
        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            cmd_2.functionIndex = function_index
            function_index = (function_index + 1) % 4
            for check_data in check_data_list:
                check_data.functionIndex = function_index
                function_index = (function_index + 1) % 4
            # end for
        # end for

        # Change function index for the sliding window in command 3
        dfu_file_parser.command_3.functionIndex = function_index

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of 1QuantumSequence_application.dfu file')
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over the number of program quantum packets to be sent = '
                       f'{len(dfu_file_parser.command_1)}')
        # --------------------------------------------------------------------------------------------------------------
        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of 1QuantumSequence_application.dfu file is '
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

            for program_data in program_data_list:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2('Test Step 4: Send dfuCmdDatax : next 16 bytes of 1QuantumSequence_application.dfu file '
                               'is program data packet 1')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data,
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
        # end for
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of 1QuantumSequence_application.dfu file is '
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of 1QuantumSequence_application.dfu '
                               f'file is check data packet {i+1}')
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of 1QuantumSequence_application.dfu file is '
                       'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=8,
            log_check=7)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=9, log_check=8)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("FNT_00D0_0018")
    # end def test_EachData1ProgramQuantum

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_EachData1PacketInReverseOrder(self):
        """
        @tc_synopsis    Sending a DFU interleaving a command 1 with size = 1 packet (16 bytes) before each data block
                        and data block sequenced in a reversed address order.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Reformat command 1 and program data of Regular_application.dfu file to a '
                       'sequence of command 1 with size = 16 followed by program data in reverse order to create '
                       'ReverseProgramData_application.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        all_new_command_1 = []
        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            address_packet = int(Numeral(cmd_1.address))
            current_size = int(Numeral(cmd_1.size))
            for program_data in program_data_list:
                new_cmd_1 = DfuCmdDataXCmd1or2.fromHexList(HexList(cmd_1))
                new_cmd_1.address = address_packet
                new_cmd_1.size = 16 if current_size > 16 else current_size
                address_packet += int(Numeral(new_cmd_1.size))
                current_size -= int(Numeral(new_cmd_1.size))
                all_new_command_1.append((new_cmd_1, [program_data]))
            # end for
        # end for
        all_new_command_1.reverse()
        # Change the function index after the list is reversed
        function_index = 1
        for (cmd_1, program_data_list) in all_new_command_1:
            cmd_1.functionIndex = function_index
            function_index = (function_index + 1) % 4
            program_data_list[0].functionIndex = function_index
            function_index = (function_index + 1) % 4
        # end for

        dfu_file_parser.command_1 = all_new_command_1

        # Change function index for the sliding window in command 2
        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            cmd_2.functionIndex = function_index
            function_index = (function_index + 1) % 4
            for check_data in check_data_list:
                check_data.functionIndex = function_index
                function_index = (function_index + 1) % 4
            # end for
        # end for

        # Change function index for the sliding window in command 3
        dfu_file_parser.command_3.functionIndex = function_index

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of ReverseProgramData_application.dfu file')
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Loop over the number of program quantum packets to be sent = '
                       f'{len(dfu_file_parser.command_1)}')
        # --------------------------------------------------------------------------------------------------------------
        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of ReverseProgramData_application.dfu file '
                           'is command 1')
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

            for program_data in program_data_list:
                # ------------------------------------------------------------------------------------------------------
                self.logTitle2('Test Step 4: Send dfuCmdDatax : next 16 bytes of ReverseProgramData_application.dfu '
                               'file is program data packet 1')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data,
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
        # end for
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of ReverseProgramData_application.dfu file '
                           'is command 2')
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of ReverseProgramData_application.dfu '
                               f'file is check data packet {i+1}')
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of ReverseProgramData_application.dfu file is '
                       'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=8,
            log_check=7)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=9, log_check=8)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("FNT_00D0_0019")
    # end def test_EachData1PacketInReverseOrder

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_DuplicateCommand2(self):
        """
        @tc_synopsis    Sending a DFU duplicating the command 2 + data blocks requests (only one block of data)

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
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
            self.logTitle2('Test Step 2: Send dfuCmdData1 : next 16 bytes of MinAddress_application.dfu file is '
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
                self.logTitle2(f'Test Step 3: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is command 2 '
                       'with size changed to 1 packet (16 bytes)')
        # --------------------------------------------------------------------------------------------------------------
        current_size_command_2 = dfu_file_parser.command_2[0][0].size
        dfu_file_parser.command_2[0][0].size = 16
        dfu_status_response = self.send_report_wait_response(
            report=dfu_file_parser.command_2[0][0],
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and '
                       f'pktNb = {sequence_number}')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1
        dfu_file_parser.command_2[0][0].size = current_size_command_2

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of data all equal to 0')
        # --------------------------------------------------------------------------------------------------------------
        current_data = dfu_file_parser.command_2[0][1][0].data
        dfu_file_parser.command_2[0][1][0].data = HexList([0] * 16)
        dfu_status_response = self.send_report_wait_response(
            report=dfu_file_parser.command_2[0][1][0],
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Check 5: Wait for dfuStatus with status = 0x01 (Packet success) and '
                       f'pktNb = {sequence_number}')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1
        dfu_file_parser.command_2[0][1][0].data = current_data

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 6: Send dfuCmdDatax : Send again command 2 but with the regular size')
            # ----------------------------------------------------------------------------------------------------------
            cmd_2.functionIndex = sequence_number % 4
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 6: Wait for dfuStatus with status = 0x01 (Packet success) and '
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
                self.logTitle2(f'Test Step 7: Send dfuCmdDatax : next 16 bytes of MinAddress_application.dfu file is '
                               f'check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                check_data_list[i].functionIndex = sequence_number % 4
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
                    response_queue=self.hidDispatcher.common_message_queue,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                self.logTitle2(f'Test Check 7: Wait for dfuStatus with status = 0x01 (Packet success) and '
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
        self.logTitle2('Test Step 8: Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 8: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=9,
            log_check=9)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=10, log_check=10)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("FNT_00D0_0020")
    # end def test_DuplicateCommand2

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_AbortingAfterCommand1(self):
        """
        @tc_synopsis    Aborting a DFU in progress using dfuStart with fwEntity = 0xFF while the program data have
                        been provided thru command 1.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has all steps and checks
        self._abort_dfu_at_different_time(after_command_number=1)

        self.testCaseChecked("FNT_00D0_0021")
    # end def test_AbortingAfterCommand1

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_AbortingAfterCommand2(self):
        """
        @tc_synopsis    Aborting a DFU in progress using dfuStart with fwEntity = 0xFF while the program and check data
                        have been provided thru commands 1 & 2.
.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has all steps and checks
        self._abort_dfu_at_different_time(after_command_number=2)

        self.testCaseChecked("FNT_00D0_0022")
    # end def test_AbortingAfterCommand2

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_AbortingAfterCommand3(self):
        """
        @tc_synopsis    Aborting a DFU using dfuStart with fwEntity = 0xFF while all the commands 1, 2 & 3 sequence
                        have been executed shall do nothing.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has all steps and checks
        self._abort_dfu_at_different_time(after_command_number=3)

        self.testCaseChecked("FNT_00D0_0023")
    # end def test_AbortingAfterCommand3

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_AbortingAndRestartAppDfu(self):
        """
        @tc_synopsis    Re-send DfuStart on the same entity while a DFU was already in progress then proceed with the
                        current installation from scratch.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has step 1 to 11 and check 1 to 12
        dfu_file_parser = self._stop_and_start_new_dfu(first_dfu_entity=self.DfuEntity.MAIN_APPLICATION,
                                                       second_dfu_entity=self.DfuEntity.MAIN_APPLICATION)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=12,
            log_check=13)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=13, log_check=14)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("FNT_00D0_0028#1")
    # end def test_AbortingAndRestartAppDfu

    @features('Feature00D0')
    @features('ImageDFU')
    @level('Time-consuming')
    @services('Debugger')
    def test_AbortingAndRestartImageDfu(self):
        """
        @tc_synopsis    Re-send DfuStart on the same entity while a DFU was already in progress then proceed with the
                        current installation from scratch.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has step 1 to 11 and check 1 to 12
        dfu_file_parser = self._stop_and_start_new_dfu(first_dfu_entity=self.DfuEntity.IMAGES,
                                                       second_dfu_entity=self.DfuEntity.IMAGES)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=12,
            log_check=13)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=13, log_check=14)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("FNT_00D0_0028#2")
    # end def test_AbortingAndRestartImageDfu

    @features('Feature00D0')
    @features('Feature00D0SoftDevice')
    @level('Time-consuming')
    @services('Debugger')
    def test_AbortingAppAndStartSoftdevice(self):
        """
        @tc_synopsis    Re-send DfuStart on a different entity while a DFU was already in progress then proceed with
                        the new entity installation.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has all steps and checks
        self._stop_and_start_new_dfu(first_dfu_entity=self.DfuEntity.MAIN_APPLICATION,
                                     second_dfu_entity=self.DfuEntity.SOFTDEVICE)

        self.reset(hardware_reset=True)

        f = self.getFeatures()
        self.perform_dfu(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=12,
            log_check=13)

        self.testCaseChecked("FNT_00D0_0029")
    # end def test_AbortingAppAndStartSoftdevice

    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_CompleteDfuBusinessRestartAll_app(self):
        """
        @tc_synopsis    Sending a normal App Dfu sequence and finalizing it by calling 'restart' with fwEntity = 0xFF
                        shall be equivalent to the business case.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        f = self.getFeatures()

        self.perform_dfu(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1,
            log_check=1,
            restart_all=True)

        self.testCaseChecked("FNT_00D0_0030#1")
    # end def test_CompleteDfuBusinessRestartAll_app
    
    @features('Feature00D0')
    @features('ImageDFU')
    @level('Time-consuming')
    @services('Debugger')
    def test_CompleteDfuBusinessRestartAll_img(self):
        """
        @tc_synopsis    Sending an Image Dfu sequence and finalizing it by calling 'restart' with fwEntity = 0xFF
                        shall be equivalent to the business case.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        f = self.getFeatures()
        self.perform_dfu(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesDfuFileName),
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1,
            log_check=1,
            restart_all=True)

        self.testCaseChecked("FNT_00D0_0030#2")
    # end def test_CompleteDfuBusinessRestartAll_img

    @features('Feature00D0')
    @level('Functionality')
    @services('Debugger')
    def test_RestartOnApp(self):
        """
        @tc_synopsis    Sending 'restart' with fwEntity = "Main Application" while no dfu was in progress, enable the
                        device to jump back into the application.

        [5] restart(fwEntity) -> pktNb, status, param
        """

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send restart with fwEntity for which getFwInfo(fwEntity) = '
                       '"Main Application"')
        # --------------------------------------------------------------------------------------------------------------
        fw_entity_application = None
        for entity_index in range(self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount):
            get_fw_info_response = DeviceInformationTestUtils.HIDppHelper.get_fw_info(
                test_case=self, entity_index=entity_index)

            if int(Numeral(get_fw_info_response.fw_type)) == DeviceInformation.EntityTypeV1.MAIN_APP:
                fw_entity_application = entity_index
                break
            # end if
        # end for
        restart = Restart(device_index=self.deviceIndex,
                          feature_index=self.bootloader_dfu_feature_id,
                          fw_entity=fw_entity_application)
        try:
            self.send_report_to_device(report=restart)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 1: This function may return an empty response or no response but no error')
        # --------------------------------------------------------------------------------------------------------------
        """
        According to StartDfu specification: 
        "This function may return an empty response or no response (device reset)."
        So we check that if there is a message it is a RestartResponse
        (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;hb=HEAD;f=doc/hidpp20/x00d0_dfu.ad)
        """
        self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.common_message_queue,
            class_type=RestartResponse,
            timeout=0.4,
            allow_no_message=True)

        # This distinction is only to be done here because this part will happen for all protocols except Unifying.
        # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
        #  interesting to investigate a better solution
        if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
            DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
        else:
            sleep(2)
        # end if

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=2, log_check=2)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_restart_in_main_application = False

        self.testCaseChecked("FNT_00D0_0031")
    # end def test_RestartOnApp
    
    @features('Feature00D0')
    @level('Time-consuming')
    @services('Debugger')
    def test_SwapCmd1Cmd2(self):
        """
        @tc_synopsis    Change the DFU sequence to provide check data first then the program data and finally verify
                        installation is successful.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send dfuCmdData1 : Change command 1 (and data) and command 2 (and data) order '
                       'of Regular_application.dfu file to create SwapCmd1Cmd2_application.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        sequence_number = 1

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            cmd_2.functionIndex = sequence_number % 4
            sequence_number += 1
            for check_data in check_data_list:
                check_data.functionIndex = sequence_number % 4
                sequence_number += 1
            # end for
        # end for

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            cmd_1.functionIndex = sequence_number % 4
            sequence_number += 1
            for program_data in program_data_list:
                program_data.functionIndex = sequence_number % 4
                sequence_number += 1
            # end for
        # end for

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of SwapCmd1Cmd2_application.dfu file')
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

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Send dfuCmdDatax : next 16 bytes of SwapCmd1Cmd2_application.dfu file is '
                           'command 2')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_2,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and '
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
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of SwapCmd1Cmd2_application.dfu file is '
                               f'check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=check_data_list[i],
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

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2('Test Step 5: Send dfuCmdData1 : next 16 bytes of SwapCmd1Cmd2_application.dfu file is '
                           'command 1')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(
                report=cmd_1,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Check 4: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of SwapCmd1Cmd2_application.dfu file is '
                               f'program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = self.send_report_wait_response(
                    report=program_data_list[i],
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of SwapCmd1Cmd2_application.dfu file is '
                       'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x02 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=8,
            log_check=7)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=9, log_check=8)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("FNT_00D0_0032")
    # end def test_SwapCmd1Cmd2

    @features('Feature00D0SoftDevice')
    @level('Time-consuming')
    @services('Debugger')
    def test_SoftDeviceLowestAddress(self):
        """
        @tc_synopsis    SoftDevice DFU with lowest authorized address validation.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change program address of Regular_softdevice.dfu file to lowest authorized '
                       'address and sign it to create MinAddress_softdevice.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        # Test start address at lowest range of the soft device area
        if f.PRODUCT.FEATURES.COMMON.DFU.F_DfuInPlace:
            dfu_file_parser.command_1[0][0].address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestSoftDeviceAddress
        else:
            dfu_file_parser.command_1[0][0].address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress
        # end if

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            min_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of MinAddress_softdevice.dfu file')
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
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of MinAddress_softdevice.dfu file is '
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
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of MinAddress_softdevice.dfu file is '
                               f'program data packet { i +1}')
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
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of MinAddress_softdevice.dfu file is '
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of MinAddress_softdevice.dfu file is '
                               f'check data packet { i +1}')
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of MinAddress_softdevice.dfu file is '
                       'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x06 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ALL_DFU_SUCCESS)

        self.reset(hardware_reset=True)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0041")
    # end def test_SoftDeviceLowestAddress

    @features('Feature00D0SoftDevice')
    @level('Functionality')
    @services('Debugger')
    def test_SoftDeviceHighestAddress(self):
        """
        @tc_synopsis    DFU with highest authorized address validation.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        f = self.getFeatures()
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Change program address of Regular_softdevice.dfu file to highest authorized '
                       'address')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        last_command_1_index = 0
        if f.PRODUCT.FEATURES.COMMON.DFU.F_DfuInPlace:
            reset_vector_written_command_1 = DfuCmdDataXCmd1or2.fromHexList(HexList(dfu_file_parser.command_1[0][0]))
            # Load only the first 8 bytes of the soft device to ensure the reset vector is written
            reset_vector_written_command_1.size = 8
            reset_vector_written_program_data = DfuCmdDataXData.fromHexList(HexList(dfu_file_parser.command_1[0][1][0]))
            # Append this block at the first place
            dfu_file_parser.command_1.insert(0, (reset_vector_written_command_1, [reset_vector_written_program_data]))
            # increase the index counter
            last_command_1_index += 1
        # end if

        # Test start address at the highest possible location in the application area
        dfu_file_parser.command_1[last_command_1_index][0].address = (
                f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress -
                int(Numeral(dfu_file_parser.command_1[last_command_1_index][0].size)) -
                f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationValidityFlagSize)

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            min_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send dfuStart : 16 first bytes of MaxAddress_softdevice.dfu file')
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
            self.logTitle2('Test Step 3: Send dfuCmdData1 : next 16 bytes of MaxAddress_softdevice.dfu file is '
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
                self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of MaxAddress_softdevice.dfu file is '
                               f'program data packet { i +1}')
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
            self.logTitle2('Test Step 5: Send dfuCmdDatax : next 16 bytes of MaxAddress_softdevice.dfu file is '
                           'command 2')
            # ----------------------------------------------------------------------------------------------------------
            cmd_2.functionIndex = sequence_number % 4
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
                self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of MaxAddress_softdevice.dfu file is '
                               f'check data packet { i +1}')
                # ------------------------------------------------------------------------------------------------------
                check_data_list[i].functionIndex = sequence_number % 4
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

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Send dfuCmdDatax : next 16 bytes of MaxAddress_softdevice.dfu file is '
                       'command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x06 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ALL_DFU_SUCCESS)

        # If the target supports the 'Dfu in place' feature, the Soft Device is NOT functional
        if not f.PRODUCT.FEATURES.COMMON.DFU.F_DfuInPlace:
            self.reset(hardware_reset=True)
        # end if

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0042")
    # end def test_SoftDeviceHighestAddress

    @features('Feature00D0')
    @features('Feature00D0SoftDevice')
    @level('Time-consuming')
    @services('Debugger')
    def test_AbortingAndRestartSoftDeviceDfu(self):
        """
        @tc_synopsis    Re-send DfuStart on the soft device entity while a DFU was already in progress then proceed
                        with the current installation from scratch.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [5] restart(fwEntity) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function has step 1 to 11 and check 1 to 12
        dfu_file_parser = self._stop_and_start_new_dfu(first_dfu_entity=self.DfuEntity.SOFTDEVICE,
                                                       second_dfu_entity=self.DfuEntity.SOFTDEVICE)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Step 12: Send restart with fwEntity = '
                       f'{int(Numeral(dfu_file_parser.dfu_start_command.fw_entity))}')
        # --------------------------------------------------------------------------------------------------------------
        restart = Restart(device_index=self.deviceIndex,
                          feature_index=self.bootloader_dfu_feature_id,
                          fw_entity=dfu_file_parser.dfu_start_command.fw_entity)
        try:
            self.send_report_to_device(report=restart)
        except TransportContextException as e:
            if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                pass
            else:
                raise
            # end if
        # end try

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 13: This function may return an empty response or no response but no error')
        # --------------------------------------------------------------------------------------------------------------
        """
        According to StartDfu specification: 
        "This function may return an empty response or no response (device reset)."
        So we check that if there is a message it is a RestartResponse
        (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;hb=HEAD;f=doc/hidpp20/x00d0_dfu.ad)
        """
        self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.common_message_queue,
            class_type=RestartResponse,
            timeout=0.4,
            allow_no_message=True)

        self.reset(hardware_reset=True)

        self.testCaseChecked("FNT_00D0_0045")
    # end def test_AbortingAndRestartSoftDeviceDfu

    def _interleave_x_command_1(self, number_of_command_1_to_interleave):
        """
        Validate DFU interleave X commands 1.

        @param number_of_command_1_to_interleave: The number of command 1 to interleave, cannot be 0
        @type number_of_command_1_to_interleave: int
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
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

    def _abort_dfu_at_different_time(self, after_command_number):
        """
        Performing a DFU and aborting after command 1, 2 or 3.
        For command 1 and 2, the abort will occur after the associated data.

        @param after_command_number: After which command the DFU will be aborted, can be 1, 2 or 3
        @type after_command_number: int
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
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
        # end for
        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

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
        Start an incomplete DFU then perform another complete DFU

        :param first_dfu_entity: This first DfuEntity to use (should be one of the constant in DfuEntity)
        :type first_dfu_entity: ``int``
        :param second_dfu_entity: This second DfuEntity to use (should be one of the constant in DfuEntity)
        :type second_dfu_entity: ``int``

        :return: The last DFU file parser
        :rtype: ``DfuFileParser``
        """
        entity_to_file = {
            self.DfuEntity.MAIN_APPLICATION: self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName,
            self.DfuEntity.BOOTLOADER: self.f.PRODUCT.FEATURES.COMMON.DFU.F_BootloaderDfuFileName,
            self.DfuEntity.SOFTDEVICE: self.f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName,
            self.DfuEntity.IMAGES: self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesDfuFileName,
            **{entity: filename
               for entity, filename in zip(self.DfuEntity.LIGHTNING,
                                           self.f.PRODUCT.FEATURES.COMMON.DFU.F_LightningDfuFilesName)}
        }
        first_dfu_file_path = str(join(TESTS_PATH, "DFU_FILES", entity_to_file[first_dfu_entity]))
        second_dfu_file_path = str(join(TESTS_PATH, "DFU_FILES", entity_to_file[second_dfu_entity]))

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=first_dfu_file_path,
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        timeout = 60 if (dfu_file_parser.dfu_start_command.magic_str.ascii_converter() ==
                         self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesMagicString) else 30
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
                                 packet_number=sequence_number,
                                 timeout=timeout)
        sequence_number += 1

        (cmd_1, program_data_list) = dfu_file_parser.command_1[0]

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

        # ------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Step 3: Send first dfuCmdDatax')
        # ------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(
            report=program_data_list[0],
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

        if first_dfu_file_path != second_dfu_file_path:
            dfu_file_parser = DfuFileParser.parse_dfu_file(
                dfu_file_path=second_dfu_file_path,
                device_index=int(Numeral(self.deviceIndex)),
                dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
                dfu_feature_version=self.get_dfu_version())
        # end if

        timeout = 60 if (dfu_file_parser.dfu_start_command.magic_str.ascii_converter() ==
                         self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesMagicString) else 30
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2(f'Test Step 6: Send dfuStart : 16 first bytes of {self.dfu_entity_to_file_name[second_dfu_entity]} '
                       f'file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number,
                                 timeout=timeout)
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
        self.logTitle2(f'Test Step 11: Send dfuCmdDatax : next 16 bytes of {self.dfu_entity_to_file_name[second_dfu_entity]}'
                       f' file is command 3')
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

        @param log_step: Log step number, if <= 0 no log printed
        @type log_step: int
        @param log_check: Log check number, if <= 0 no log printed
        @type log_check: int

        @return: The new log_step and log_check
        @rtype: tuple
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
# end class SharedDfuTestCaseFunctionality

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
