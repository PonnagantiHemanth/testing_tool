#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.hidpp20.common.feature_00D0_robustness
:brief: Shared HID++ 2.0 Common feature 0x00D0
:author: Stanislas Cottard
:date: 2019/09/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join
from random import randint
from time import sleep

from pylink import JLinkReadException

# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd1or2
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd3
from pyhid.hidpp.features.common.dfu import DfuCmdDataXData
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.features.common.dfu import Restart
from pyhid.hidpp.features.common.dfu import RestartResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.dfuprocessing import CommonDfuTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.transportcontext import TransportContextException
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedDfuTestCaseRobustness(CommonDfuTestCase):
    """
    Validates DFU Robustness TestCases
    """
    ERASED_PATTERN = "FF"
    PAGE_SIZE = 0x1000

    @features("Feature00D0")
    @level("Robustness")
    def test_DfuStartSoftwareIdIgnored(self):
        """
        @tc_synopsis    SoftwareId input is ignored by the firmware

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        f = self.getFeatures()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over padding range (several interesting values)")
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(dfu_start_class.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send dfuStart with fwEntity = 0xFF and softwareId = {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            dfu_start = dfu_start_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                        feature_index=self.bootloader_dfu_feature_id,
                                        fw_entity=0xFF,
                                        encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                        magic_str=self.format_magic_string_hex_list(
                                            f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                                        flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                        secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
            dfu_start.softwareId = software_id
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=dfu_start, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=dfu_start.softwareId,
                             obtained=dfu_status_response.softwareId,
                             msg="The softwareId parameter differs from the one expected")
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0004")
    # end def test_DfuStartSoftwareIdIgnored

    @features("Feature00D0")
    @features("Feature00D0MaxProgramQuantum", 16)
    @level("ReleaseCandidate")
    @services("Debugger")
    def test_Command1Command2ReservedBytes(self):
        """
        @tc_synopsis    dfuCmdData_reserved bytes shall be ignored by the firmware.

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
            device_index=int(Numeral(ChannelUtils.get_device_index(test_case=self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        # To avoid making as many dfu as there are reserved values, every reserved value will be done with a data_
        # packet of program or check quantum. Therefore, it is needed to reformat the packets.
        reserved_bytes_command_1_2 = compute_sup_values(HexList([0] * (DfuCmdDataXCmd1or2.LEN.RESERVED // 8)))

        # Add enough command 1 if necessary
        if len(dfu_file_parser.command_1) < len(reserved_bytes_command_1_2):
            all_new_command_1 = []
            command_1_treated = 0
            # Parse all packets in reverse order to create the new commands 1 from the last packets
            for (cmd_1, program_data_list) in reversed(dfu_file_parser.command_1):
                if (len(all_new_command_1) + len(dfu_file_parser.command_1) - command_1_treated) >= \
                        len(reserved_bytes_command_1_2):
                    # No need to create more
                    all_new_command_1.insert(0, (cmd_1, program_data_list))
                else:
                    last_address_packet = int(Numeral(cmd_1.address)) + int(Numeral(cmd_1.size))
                    current_size = int(Numeral(cmd_1.size))
                    program_data_list_rest = []
                    program_data_size_rest = 0
                    for program_data in reversed(program_data_list):
                        packet_size = 16 if current_size % 16 == 0 else current_size % 16
                        # logically a packet size should be dividable by the program quantum
                        for i in reversed(range(1, (packet_size // f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram)+1)):
                            new_cmd_1 = DfuCmdDataXCmd1or2.fromHexList(HexList(cmd_1))
                            new_program_data = DfuCmdDataXData.fromHexList(HexList(program_data))
                            if (len(all_new_command_1) + len(dfu_file_parser.command_1) -
                                    command_1_treated - 1) >= len(reserved_bytes_command_1_2):
                                # Enough commands 1 have been created, all other packets will remain the same
                                program_data_size_rest += i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                                current_size -= i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                                last_address_packet -= i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                                program_data.data = \
                                    program_data.data[:i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram] + \
                                    HexList([0] * (16 - i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram))
                                program_data_list_rest.insert(0, program_data)
                                break
                            else:
                                last_address_packet -= f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                                new_cmd_1.size = f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                                new_cmd_1.address = last_address_packet
                                current_size -= f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram
                                new_program_data.data = \
                                    program_data.data[(i - 1) * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram:
                                                      i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram] + \
                                    HexList([0] * (16 - f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram))
                                # Using insert with current_index permit to keep the right order of the
                                # all_new_command_1 list regarding addresses
                                all_new_command_1.insert(0, (new_cmd_1, [new_program_data]))
                            # end if
                        # end for
                    # end for

                    if len(program_data_list_rest) != 0:
                        cmd_1.size = program_data_size_rest
                        # Using insert with current_index permit to keep the right order of the all_new_command_1 list
                        # regarding addresses
                        all_new_command_1.insert(0, (cmd_1, program_data_list_rest))
                    # end if
                # end if
                command_1_treated += 1
            # end for
            dfu_file_parser.command_1 = all_new_command_1
        # end if

        # Add enough command 2 if necessary
        if len(dfu_file_parser.command_2) < len(reserved_bytes_command_1_2):
            all_new_command_2 = []
            command_2_treated = 0
            # Parse all packets in reverse order to create the new commands 2 from the last packets
            for (cmd_2, check_data_list) in reversed(dfu_file_parser.command_2):
                if (len(all_new_command_2) + len(dfu_file_parser.command_2) - command_2_treated) >= \
                        len(reserved_bytes_command_1_2):
                    # No need to create more
                    all_new_command_2.insert(0, (cmd_2, check_data_list))
                else:
                    last_address_packet = int(Numeral(cmd_2.address)) + int(Numeral(cmd_2.size))
                    current_size = int(Numeral(cmd_2.size))
                    check_data_list_rest = []
                    check_data_size_rest = 0
                    for check_data in reversed(check_data_list):
                        packet_size = 16 if current_size % 16 == 0 else current_size % 16
                        # logically a packet size should be dividable by the check quantum
                        for i in reversed(range(1, (packet_size // f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck) + 1)):
                            new_cmd_2 = DfuCmdDataXCmd1or2.fromHexList(HexList(cmd_2))
                            new_check_data = DfuCmdDataXData.fromHexList(HexList(check_data))
                            if (len(all_new_command_2) + len(dfu_file_parser.command_2) -
                                    command_2_treated - 1) >= len(reserved_bytes_command_1_2):
                                # Enough commands 2 have been created, all other packets will remain the same
                                check_data_size_rest += i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck
                                current_size -= i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck
                                last_address_packet -= i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck
                                check_data.data = check_data.data[:i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck] + \
                                    HexList([0] * (16 - i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck))
                                check_data_list_rest.insert(0, check_data)
                                break
                            else:
                                last_address_packet -= f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck
                                new_cmd_2.size = f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck
                                new_cmd_2.address = last_address_packet
                                current_size -= f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck
                                new_check_data.data = \
                                    check_data.data[(i - 1) * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck:
                                                    i * f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck] + \
                                    HexList([0] * (16 - f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck))
                                # Using insert with current_index permit to keep the right order of the
                                # all_new_command_1 list regarding addresses
                                all_new_command_2.insert(0, (new_cmd_2, [new_check_data]))
                            # end if
                        # end for
                    # end for

                    if len(check_data_list_rest) != 0:
                        cmd_2.size = check_data_size_rest
                        # Using insert with current_index permit to keep the right order of the all_new_command_1 list
                        # regarding addresses
                        all_new_command_2.insert(0, (cmd_2, check_data_list_rest))
                    # end if
                # end if
                command_2_treated += 1
            # end for
            dfu_file_parser.command_2 = all_new_command_2
        # end if

        # Add the reserved bytes
        for i in range(len(reserved_bytes_command_1_2)):
            dfu_file_parser.command_1[-1-i][0].reserved = reserved_bytes_command_1_2[i]
            dfu_file_parser.command_2[-1-i][0].reserved = reserved_bytes_command_1_2[i]
        # end for

        # put back all the function indexes in right order
        function_index = 1
        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            cmd_1.functionIndex = function_index
            function_index = (function_index + 1) % 4
            for program_data in program_data_list:
                program_data.functionIndex = function_index
                function_index = (function_index + 1) % 4
            # end for
        # end for
        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            cmd_2.functionIndex = function_index
            function_index = (function_index + 1) % 4
            for check_data in check_data_list:
                check_data.functionIndex = function_index
                function_index = (function_index + 1) % 4
            # end for
        # end for
        dfu_file_parser.command_3.functionIndex = function_index

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of Regular_application.dfu file") 
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0") 
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1[:-len(reserved_bytes_command_1_2)]: 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is command 1 "
                                     "reducing size to permit test of reserved bytes later") 
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=cmd_1, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1") 
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over the number of program data packets to be sent = "
                                     f"{len(program_data_list)}, packet number should start at 1") 
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is "
                                         f"program data packet {i+1}")
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=program_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and "
                                          f"pktNb = {sequence_number}")
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop") 
            # ----------------------------------------------------------------------------------------------------------
        # end for
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over the number of command 1 reserved bytes possibility") 
        # --------------------------------------------------------------------------------------------------------------
        for (cmd_1, program_data_list) in dfu_file_parser.command_1[-len(reserved_bytes_command_1_2):]: 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send dfuCmdData1 : Send again command 1 changing size = "
                                     f"{f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram} reserved "
                                     f"bytes = {cmd_1.reserved}") 
            # ----------------------------------------------------------------------------------------------------------
            if int(Numeral(cmd_1.size)) != f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram:
                LogHelper.log_trace(
                    self, f"The real size = {cmd_1.size}, it is like that because since the dfu file given can "
                          "have multiple command 1, we add only the necessary number and keep the one already "
                          "there. Therefore, there can be command 1 with a size not equal to the program "
                          "quantum. Since the test is not dependant on this size, it is not a problem.")
            # end if
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=cmd_1, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1")
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send dfuCmdDatax : next {f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram} "
                                         f"bytes of Regular_application.dfu file is program data packet {i+1}")
                # ------------------------------------------------------------------------------------------------------
                if int(Numeral(cmd_1.size)) != f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumProgram:
                    LogHelper.log_trace(self, "Again, the number of bytes can differ from the program quantum")
                # end if
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=program_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and "
                                          f"pktNb = {sequence_number}")
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop") 
        # --------------------------------------------------------------------------------------------------------------

        for (cmd_2, check_data_list) in dfu_file_parser.command_2[:-len(reserved_bytes_command_1_2)]: 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is command 2 "
                                     "reducing size to permit test of reserved bytes later")
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=cmd_2, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1") 
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over the number of check data packets to be sent = "
                                     f"{len(check_data_list)}, packet number should start at 1")
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is "
                                         f"check data packet {i+1}")
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=check_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and "
                                          f"pktNb = {sequence_number}")
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop") 
            # ----------------------------------------------------------------------------------------------------------
        # end for
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over the number of command 2 reserved bytes possibility") 
        # --------------------------------------------------------------------------------------------------------------
        for (cmd_2, check_data_list) in dfu_file_parser.command_2[-len(reserved_bytes_command_1_2):]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send dfuCmdData1 : Send again command 1 changing size = "
                                     f"{f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck} reserved bytes = "
                                     f"{cmd_2.reserved}") 
            # ----------------------------------------------------------------------------------------------------------
            if int(Numeral(cmd_2.size)) != f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck:
                LogHelper.log_trace(
                    self, f"The real size = {cmd_2.size}, it is like that because since the dfu file given can "
                          "have multiple command 2, we add only the necessary number and keep the one already "
                          "there. Therefore, there can be command 2 with a size not equal to the check "
                          "quantum. Since the test is not dependant on this size, it is not a problem.")
            # end if
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=cmd_2, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1")
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            for i in range(len(check_data_list)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send dfuCmdDatax : next {f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck}"
                                         f" bytes of Regular_application.dfu file is check data packet {i+1}")
                # ------------------------------------------------------------------------------------------------------
                if int(Numeral(cmd_2.size)) != f.PRODUCT.FEATURES.COMMON.DFU.F_QuantumCheck:
                    LogHelper.log_trace(self, "Again, the number of bytes can differ from the check quantum")
                # end if
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=check_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and "
                                          f"pktNb = {sequence_number}")
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop") 
        # --------------------------------------------------------------------------------------------------------------
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is command 3")
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser.command_3.functionIndex = sequence_number % 4
        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.command_3, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x02 (DFU success)") 
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=11,
            log_check=11)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=12, log_check=12)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("ROT_00D0_0006")
    # end def test_Command1Command2ReservedBytes

    @features("Feature00D0")
    @level("Time-consuming")
    @services("Debugger")
    def test_Command3ReservedBytes(self):
        """
        @tc_synopsis    dfuCmd3Data_reserved bytes shall be ignored by the firmware.

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
            device_index=int(Numeral(ChannelUtils.get_device_index(test_case=self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        reserved_bytes_command_3 = [[0xFF] * (DfuCmdDataXCmd3.LEN.RESERVED // 8),
                                    [0] * (DfuCmdDataXCmd3.LEN.RESERVED // 8)]

        random_bit = randint(0, DfuCmdDataXCmd3.LEN.RESERVED - 1)
        reserved_bytes_command_3[1][random_bit//8] = 1 << (random_bit % 8)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over cmd3 reserved bytes range (2 interesting values : "
                                 "all 0xFF, one random bit to 1)")
        # --------------------------------------------------------------------------------------------------------------
        for reserved_command_3 in reserved_bytes_command_3:
            sequence_number = 0
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send dfuStart : 16 first bytes of Regular_application.dfu file") 
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=dfu_file_parser.dfu_start_command,
                response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0") 
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            for (cmd_1, program_data_list) in dfu_file_parser.command_1:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send dfuCmdData1 : next 16 bytes of Regular_application.dfu file is "
                                         "command 1")
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=cmd_1, response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1")
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Test Loop over the number of program data packets to be sent = "
                                         f"{len(program_data_list)}, packet number should start at 1")
                # ------------------------------------------------------------------------------------------------------
                for i in range(len(program_data_list)):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is "
                                             f"program data packet {i+1}")
                    # --------------------------------------------------------------------------------------------------
                    dfu_status_response = ChannelUtils.send(
                        test_case=self, report=program_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=DfuStatusResponse)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and "
                                              f"pktNb = {sequence_number}")
                    # --------------------------------------------------------------------------------------------------
                    self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                             status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                             packet_number=sequence_number)

                    sequence_number += 1
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for

            for (cmd_2, check_data_list) in dfu_file_parser.command_2:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is "
                                         "command 2")
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=cmd_2, response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and "
                                          f"pktNb = {sequence_number}")
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Test Loop over the number of check data packets to be sent = "
                                         f"{len(check_data_list)}, packet number should start at 1")
                # ------------------------------------------------------------------------------------------------------
                for i in range(len(check_data_list)):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is "
                                             f"check data packet {i+1}")
                    # --------------------------------------------------------------------------------------------------
                    dfu_status_response = ChannelUtils.send(
                        test_case=self, report=check_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=DfuStatusResponse)
 
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and "
                                              f"pktNb = {sequence_number}")
                    # --------------------------------------------------------------------------------------------------
                    self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                             status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                             packet_number=sequence_number)

                    sequence_number += 1
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "End Test Loop")
                # ------------------------------------------------------------------------------------------------------
            # end for
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send dfuCmdDatax : next 16 bytes of Regular_application.dfu file is command "
                                     f"3 changing reserved bytes = {HexList(reserved_command_3)}")
            # ----------------------------------------------------------------------------------------------------------
            dfu_file_parser.command_3.reserved = HexList(reserved_command_3)
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=dfu_file_parser.command_3, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for dfuStatus with status = 0x02 (DFU success)") 
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.DFU_SUCCESS)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop") 
        # --------------------------------------------------------------------------------------------------------------

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            restart_all=False,
            dfu_file_parser=dfu_file_parser,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled,
            log_step=7,
            log_check=7)

        # Call target-agnostic function checking the receiver switches in application mode
        self.check_application_mode(log_step=8, log_check=8)

        # If the test is successful, there is no need to restart in main application
        self.post_requisite_program_mcu_initial_state = False

        self.testCaseChecked("ROT_00D0_0007")
    # end def test_Command3ReservedBytes

    @features("Feature00D0")
    @level("Robustness")
    def test_DfuStartReservedIgnored(self):
        """
        dfuStart_reserved bytes shall be ignored by the firmware

        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        dfu_start_class = self.get_dfu_start_class()

        f = self.getFeatures()
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over dfuStart.reserved range (several interesting values)") 
        # --------------------------------------------------------------------------------------------------------------
        for reserved_bytes in compute_sup_values(HexList(Numeral(dfu_start_class.DEFAULT.PADDING,
                                                                 dfu_start_class.LEN.RESERVED // 8))): 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send dfuStart with fwEntity = 0xFF and reserved = {reserved_bytes}") 
            # ----------------------------------------------------------------------------------------------------------
            dfu_start = dfu_start_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                        feature_index=self.bootloader_dfu_feature_id,
                                        fw_entity=0xFF,
                                        encrypt=int(f.PRODUCT.FEATURES.COMMON.DFU.F_EncryptCapabilities[0]),
                                        magic_str=self.format_magic_string_hex_list(
                                            f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                                        flag=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                        secur_lvl=int(f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))
            dfu_start.reserved = reserved_bytes
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=dfu_start, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0") 
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=dfu_start.softwareId,
                             obtained=dfu_status_response.softwareId,
                             msg="The softwareId parameter differs from the one expected")
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop") 
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0005")
        self.testCaseChecked("ROT_00D0_0008")
    # end def test_DfuStartReservedIgnored

    @features("Feature00D0")
    @level("Robustness")
    def test_RestartReservedIgnored(self):
        """
        restart_reserved bytes shall be ignored by the firmware

        [5] restart(fwEntity) -> pktNb, status, param
        """
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over restart.reserved range (several interesting values)") 
        # --------------------------------------------------------------------------------------------------------------
        reserved_values = compute_sup_values(HexList(Numeral(Restart.DEFAULT.PADDING, Restart.LEN.RESERVED // 8)))
        # This test is too time-consuming if we keep all the reserved value
        reserved_values_light = [reserved_values[0],
                                 reserved_values[len(reserved_values) // 4],
                                 reserved_values[2 * (len(reserved_values) // 4)],
                                 reserved_values[3 * (len(reserved_values) // 4)],
                                 reserved_values[-1]]
        for reserved_byte in reserved_values_light: 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send restart with fwEntity = 0xFF and reserved = {reserved_byte}") 
            # ----------------------------------------------------------------------------------------------------------
            restart = Restart(device_index=ChannelUtils.get_device_index(test_case=self),
                              feature_index=self.bootloader_dfu_feature_id,
                              fw_entity=0xFF)
            restart.reserved = reserved_byte
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
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "This function may return an empty response or no response but no error") 
            # ----------------------------------------------------------------------------------------------------------
            """
            According to StartDfu specification: 
            "This function may return an empty response or no response (device reset)."
            So we check that if there is a message it is a RestartResponse
            (http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;hb=HEAD;f=doc/hidpp20/x00d0_dfu.ad)
            """
            ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.COMMON, class_type=RestartResponse, timeout=.4,
                check_first_message=False, allow_no_message=True)

            # This distinction is only to be done here because this part will happen for all protocols except Unifying.
            # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
            #  interesting to investigate a better solution
            if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
                DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
            else:
                sleep(2)
            # end if
 
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send DFU Control.startDfu to switch in bootloader") 
            # ----------------------------------------------------------------------------------------------------------
            self.dut_jump_on_bootloader()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop") 
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROT_00D0_0009")
    # end def test_RestartReservedIgnored

    @features("Feature00D0SoftDevice")
    @features("Feature00D0DfuInPlace")
    @level("Robustness")
    @services("Debugger")
    def test_softdevice_not_installed(self):
        """
        "DFU in place" feature: Send a dfuStart with fwEntity matching the application
        while the SoftDevice is not installed
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=int(Numeral(ChannelUtils.get_device_index(test_case=self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of Regular_softdevice.dfu file") 
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0") 
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(ChannelUtils.get_device_index(test_case=self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of Regular_application.dfu file") 
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x28 (Missing Pre-requisite)") 
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.MISSING_PRE_REQUISITE,
                                 packet_number=0)

        self.testCaseChecked("ROT_00D0_0052")
    # end def test_softdevice_not_installed

    @features("Feature00D0")
    @level("Robustness")
    @services("Debugger")
    def test_application_memory_range_wiped_while_app_dfu(self):
        """
        Check Application memory address range is wiped out when starting the application update
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=int(Numeral(ChannelUtils.get_device_index(test_case=self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of Regular_application.dfu file")
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0")
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Application memory address range is wiped out") 
        # --------------------------------------------------------------------------------------------------------------
        self._check_dump_memory_range()
        self.reset()

        self.testCaseChecked("ROT_00D0_0053")
    # end def test_application_memory_range_wiped_while_app_dfu

    @features("Feature00D0SoftDevice")
    @features("NoFeature00D0DfuInPlace")
    @level("Robustness")
    @services("Debugger")
    def test_application_memory_range_wiped_while_sd_dfu(self):
        """
        Check Application memory address range is wiped out when starting the SoftDevice update.
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=int(Numeral(ChannelUtils.get_device_index(test_case=self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of Regular_softdevice.dfu file") 
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0") 
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Application memory address range is wiped out") 
        # --------------------------------------------------------------------------------------------------------------
        self._check_dump_memory_range()
        self.reset()

        self.testCaseChecked("ROT_00D0_0054")
    # end def test_application_memory_range_wiped_while_sd_dfu

    @features("Feature00D0SoftDevice")
    @features("Feature00D0DfuInPlace")
    @level("Robustness")
    @services("Debugger")
    def test_softdevice_memory_range_wiped_while_sd_dfu(self):
        """
        "DFU in place" feature: Check SoftDevice and Application memory address ranges are wiped out
        when starting the SoftDevice update
        """
        f = self.getFeatures()
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=int(Numeral(ChannelUtils.get_device_index(test_case=self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of Regular_softdevice.dfu file") 
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0") 
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=0)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SoftDevice and Application memory address ranges are wiped out") 
        # --------------------------------------------------------------------------------------------------------------
        self._check_dump_memory_range(include_soft_device_range=True)
        self.reset()

        self.testCaseChecked("ROT_00D0_0055")
    # end def test_softdevice_memory_range_wiped_while_sd_dfu

    @features("Feature00D0")
    @features("Feature00D0SoftDevice")
    @features("NoFeature00D0DfuInPlace")
    @level("Time-consuming")
    @services("Debugger")
    def test_app_memory_wiped_at_restart_validity_flag_erased(self):
        """
        Check Application memory address range is wiped out at restart if application entity is not valid
        """
        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Force Application validity flag to erased state") 
        # --------------------------------------------------------------------------------------------------------------
        self._erased_entity_valid_flag()
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device") 
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, recover_time_needed=True)
        sleep(2)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Application memory address range is wiped out") 
        # --------------------------------------------------------------------------------------------------------------
        self._check_dump_memory_range()
        self.reset()

        self.testCaseChecked("ROT_00D0_0056")
    # end def test_app_memory_wiped_at_restart_validity_flag_erased

    @features("Feature00D0")
    @features("Feature00D0SoftDevice")
    @features("Feature00D0DfuInPlace")
    @level("Time-consuming")
    @services("Debugger")
    def test_app_memory_wiped_at_restart_reset_vector_erased(self):
        """
        Check Application memory address range is wiped out at restart if application entity is not valid
        """
        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Force Application reset vector to erased state") 
        # --------------------------------------------------------------------------------------------------------------
        self._erased_entity_valid_flag(reset_last_app_word=False, reset_vector_app_word=True)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device") 
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Application memory address range is wiped out") 
        # --------------------------------------------------------------------------------------------------------------
        self._check_dump_memory_range()
        self.reset()

        self.testCaseChecked("ROT_00D0_0057")
    # end def test_app_memory_wiped_at_restart_reset_vector_erased

    @features("Feature00D0")
    @features("Feature00D0SoftDevice")
    @features("Feature00D0DfuInPlace")
    @level("Time-consuming")
    @services("Debugger")
    def test_sd_app_memory_wiped_at_restart_reset_vector_erased(self):
        """
        Check SoftDevice and Application memory address ranges are wiped out at restart if soft device entity is not
        valid
        """
        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Force SoftDevice reset vector to erased state") 
        # --------------------------------------------------------------------------------------------------------------
        self._erased_entity_valid_flag(reset_last_app_word=False, reset_vector_sd_word=True)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device") 
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, recover_time_needed=True)
 
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SoftDevice and Application memory address ranges are wiped out") 
        # --------------------------------------------------------------------------------------------------------------
        self._check_dump_memory_range(include_soft_device_range=True)
        self.reset()

        self.testCaseChecked("ROT_00D0_0058")
    # end def test_sd_app_memory_wiped_at_restart_reset_vector_erased

    @features("Feature00D0")
    @level("Robustness")
    @services("Debugger")
    def test_reset_while_dfu_and_restart(self):
        """
        Stop an in-progress DFU by applying a DUT power off / on then restart DFU installation from scratch
        """
        # noinspection PyUnresolvedReferences
        dfu_file = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file,
            device_index=int(Numeral(ChannelUtils.get_device_index(self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        self.post_requisite_program_mcu_initial_state = True
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of Regular_application.dfu file")
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(self,
                                                dfu_file_parser.dfu_start_command,
                                                HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0")
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)
        sequence_number += 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Restart DFU")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_dfu(
            dfu_file_path=dfu_file,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1,
            log_check=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device is in main application")
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(DfuTestUtils.is_main_app(self), "The device should be in main application")

        self.testCaseChecked("ROB_00D0_0060")
    # end def test_reset_while_dfu_and_restart

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Robustness')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_app_erased_at_dfu_start(self):
        """
        Validate the companion application is erased at DFU start.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Read companion memory at application addresses (from start to end) and '
                                         'check it is not erased before the DFU')
        # --------------------------------------------------------------------------------------------------------------
        app_memory = self.companion_debugger.readMemory(
            self.companion_debugger.FMM_APP_START_ADDR,
            self.companion_debugger.FMM_APP_END_ADDR - self.companion_debugger.FMM_APP_START_ADDR - 1)
        self.assertNotEquals(app_memory, [0xFF] * len(app_memory), 'Companion application should not be erased')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Parse DFU file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file,
            device_index=int(Numeral(ChannelUtils.get_device_index(self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU start command')
        # --------------------------------------------------------------------------------------------------------------
        sequence_number = 0
        dfu_status_response = ChannelUtils.send(self,
                                                dfu_file_parser.dfu_start_command,
                                                HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait DFU status (Status = 1 (success) and packet number = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)
        sequence_number += 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read companion memory at application addresses (from start to end)')
        # --------------------------------------------------------------------------------------------------------------
        app_memory = self.companion_debugger.readMemory(
            self.companion_debugger.FMM_APP_START_ADDR,
            self.companion_debugger.FMM_APP_END_ADDR - self.companion_debugger.FMM_APP_START_ADDR - 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check companion application is erased')
        # --------------------------------------------------------------------------------------------------------------
        self.assertListEqual(app_memory, [0xFF] * len(app_memory), 'Companion application should be erased')

        self.testCaseChecked("ROB_00D0_0061")
    # end def test_companion_app_erased_at_dfu_start

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Robustness')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_main_app_dfu_companion_app_erased(self):
        """
        Validate the main application can be DFUed when the companion application is erased.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Erase companion application')
        # --------------------------------------------------------------------------------------------------------------
        self.companion_debugger.writeMemory(
            self.companion_debugger.FMM_APP_START_ADDR,
            [0xFF] * (self.companion_debugger.FMM_APP_END_ADDR - self.companion_debugger.FMM_APP_START_ADDR - 1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore main application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_program_mcu_initial_state = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform DFU for the main application entity')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES",
                             self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)
        self.bootloader_dfu_processing(
            dfu_file_path=dfu_file_path,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1,
            log_check=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check main application is written')
        # --------------------------------------------------------------------------------------------------------------
        start_address = self.f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress
        memory_size = self.f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress - start_address
        # self.debugger.stop()
        main_app = self.debugger.readMemory(start_address, memory_size)
        # self.debugger.run()
        self.assertNotEquals(main_app, [0xFF] * len(main_app), 'Main application should be written')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Check companion application is still erased')
        # --------------------------------------------------------------------------------------------------------------
        app_memory = self.companion_debugger.readMemory(
            self.companion_debugger.FMM_APP_START_ADDR,
            self.companion_debugger.FMM_APP_END_ADDR - self.companion_debugger.FMM_APP_START_ADDR - 1)
        self.assertListEqual(app_memory, [0xFF] * len(app_memory), 'Companion application should be erased')

        self.testCaseChecked("ROB_00D0_0062")
    # end def test_main_app_dfu_companion_app_erased

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Robustness')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_app_dfu_main_app_erased(self):
        """
        Validate the companion application can be DFUed when the main application is erased.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore main application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_program_mcu_initial_state = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Erase main application')
        # --------------------------------------------------------------------------------------------------------------
        start_address = self.f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress
        memory_size = self.f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress - start_address
        self.debugger.writeMemory(start_address, [0xFF] * memory_size)
        main_app = self.debugger.readMemory(start_address, memory_size)
        self.assertListEqual(main_app, [0xFF] * len(main_app), 'Main application should be erased')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform DFU for the companion application entity')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        self.bootloader_dfu_processing(
            dfu_file_path=dfu_file_path,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1,
            log_check=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check companion application is written')
        # --------------------------------------------------------------------------------------------------------------
        app_memory = self.companion_debugger.readMemory(
            self.companion_debugger.FMM_APP_START_ADDR,
            self.companion_debugger.FMM_APP_END_ADDR - self.companion_debugger.FMM_APP_START_ADDR - 1)
        self.assertNotEquals(app_memory, [0xFF] * len(app_memory), 'Companion application should be written')

        self.testCaseChecked("ROB_00D0_0063")
    # end def test_companion_app_dfu_main_app_erased

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Robustness')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_reset_while_companion_dfu(self):
        """
        Validate the device can be reset while DFUing, and DFU restarted.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Parse DFU file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(ChannelUtils.get_device_index(self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send dfuStart : 16 first bytes of DFU file")
        # --------------------------------------------------------------------------------------------------------------
        sequence_number = 0
        dfu_status_response = ChannelUtils.send(self,
                                                dfu_file_parser.dfu_start_command,
                                                HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0")
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)
        sequence_number += 1

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset companion CPU")
        # --------------------------------------------------------------------------------------------------------------
        self.companion_debugger.reset()
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Restart DFU")
        # --------------------------------------------------------------------------------------------------------------
        self.perform_dfu(
            dfu_file_path=dfu_file_path,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            log_step=1,
            log_check=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device is in main application")
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(DfuTestUtils.is_main_app(self), "The device should be in main application")

        self.testCaseChecked("ROB_00D0_0064#1")
    # end def test_companion_reset_while_companion_dfu

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Robustness')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_hardware_reset_while_companion_dfu(self):
        """
        Validate the device can be reset while DFUing, and DFU restarted.
        """
        with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=self.debugger):
            with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=self.companion_debugger):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Parse DFU file')
                # ------------------------------------------------------------------------------------------------------
                dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
                dfu_file_parser = DfuFileParser.parse_dfu_file(
                    dfu_file_path=dfu_file_path,
                    device_index=int(Numeral(ChannelUtils.get_device_index(self))),
                    dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
                    dfu_feature_version=self.get_dfu_version())

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
                # ------------------------------------------------------------------------------------------------------
                self.post_requisite_restore_companion = True

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send dfuStart : 16 first bytes of DFU file")
                # ------------------------------------------------------------------------------------------------------
                sequence_number = 0
                dfu_status_response = ChannelUtils.send(self,
                                                        dfu_file_parser.dfu_start_command,
                                                        HIDDispatcher.QueueName.COMMON,
                                                        response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0")
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)
                sequence_number += 1

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Hardware Reset")
                # ------------------------------------------------------------------------------------------------------
                try:
                    LibusbDriver.disable_usb_port(port_index=ChannelUtils.get_port_index(
                        test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self)))
                finally:
                    LibusbDriver.enable_usb_port(port_index=ChannelUtils.get_port_index(
                        test_case=self, channel=ChannelUtils.get_receiver_channel(test_case=self)))
                # end try
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Restart DFU")
                # ------------------------------------------------------------------------------------------------------
                self.perform_dfu(
                    dfu_file_path=dfu_file_path,
                    bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
                    log_step=1,
                    log_check=1)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the device is in main application")
                # ------------------------------------------------------------------------------------------------------
                self.assertTrue(DfuTestUtils.is_main_app(self), "The device should be in main application")
            # end with
        # end with

        self.testCaseChecked("ROB_00D0_0064#2")
    # end def test_hardware_reset_while_companion_dfu

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Robustness')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_abort_while_dfu_after_command_1(self):
        """
        Validate DFU can be aborted and restarted.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform DFU for the companion application entity and abort after command 1')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        self._abort_dfu_at_different_time(after_command_number=1, dfu_file_name=dfu_file_path)

        self.testCaseChecked("ROB_00D0_0065#1")
    # end def test_companion_abort_while_dfu_after_command_1

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Robustness')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_abort_while_dfu_after_command_2(self):
        """
        Validate DFU can be aborted and restarted.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform DFU for the companion application entity and abort after command 2')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        self._abort_dfu_at_different_time(after_command_number=2, dfu_file_name=dfu_file_path)

        self.testCaseChecked("ROB_00D0_0065#2")
    # end def test_companion_abort_while_dfu_after_command_2

    @features('Feature00D0')
    @features('CompanionMCU')
    @level('Robustness')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_abort_while_dfu_after_command_3(self):
        """
        Validate DFU can be aborted and restarted.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform DFU for the companion application entity and abort after command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        self._abort_dfu_at_different_time(after_command_number=3, dfu_file_name=dfu_file_path)

        self.testCaseChecked("ROB_00D0_0065#3")
    # end def test_companion_abort_while_dfu_after_command_3

    def _check_dump_memory_range(self, include_soft_device_range=False, check_memory_erased=True):
        """
        Dump and optionally check the memory content
        :param include_soft_device_range: Extend the parsed address range with the SoftDevice upgradable one - OPTIONAL
        :type include_soft_device_range: ``bool``
        :param check_memory_erased: Enable the verification - OPTIONAL
        :type check_memory_erased: ``bool``

        :return: memory buffer
        :rtype: ``HexList``
        """
        f = self.getFeatures()
        if not include_soft_device_range:
            start_address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress
        else:
            start_address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestSoftDeviceAddress
        # end if
        memory_size = f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress - start_address
        # Empty message queue before power reset
        ChannelUtils.empty_queues(test_case=self)
        self.debugger.stop()
        try:
            buffer = self.debugger.readMemory(start_address, memory_size)
        except JLinkReadException:
            # Reconnect the debugger and retry
            self.debugger.close()
            sleep(0.7)
            self.debugger.open()
            buffer = self.debugger.readMemory(start_address, memory_size)
        # end try
        self.debugger.reset()
        if check_memory_erased:
            error_message = ""
            erased_page = HexList(self.ERASED_PATTERN * self.PAGE_SIZE)
            for page_index in range(memory_size // self.PAGE_SIZE):
                dumped_memory_page = buffer[page_index * self.PAGE_SIZE : (page_index + 1) * self.PAGE_SIZE]
                if dumped_memory_page != erased_page:
                    error_message += f"Dumped memory page index {page_index} is not in erased state !/n"
                # end if
            # end for
            self.assertTrue(error_message == "", error_message)
        # end if
        return buffer
    # end def _check_dump_memory_range

    def _erased_entity_valid_flag(self, reset_last_app_word=True,
                                  reset_vector_app_word=False, reset_vector_sd_word=False):
        """
        Force some memory addresses matching entity validity flag to an erased state

        :param reset_last_app_word: Set 0xFFFFFFFF at the Application Validity Flag Address (DFU Legacy) - OPTIONAL
        :type reset_last_app_word: ``bool``
        :param reset_vector_app_word: Set 0xFFFFFFFF at the Application Reset Vector Address (DFU In Place) - OPTIONAL
        :type reset_vector_app_word: ``bool``
        :param reset_vector_sd_word: Set 0xFFFFFFFF at the SoftDevice Reset Vector Address (DFU In Place) - OPTIONAL
        :type reset_vector_sd_word: ``bool``

        """
        word_size = self.memory_manager.chunk_id_map["NVS_WORD_SIZE"]
        block_size = 1024
        f = self.getFeatures()
        start_address = None
        self.debugger.stop()
        if reset_vector_app_word:
            # Get the first 1024 bytes of the application memory range including the Application Reset Vector Address
            # It's a workaround to a JLink dll issue which prevent to erase a word which is already programmed
            start_address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress
            first_block = self.debugger.readMemory(start_address, block_size)
            first_block[:word_size * 2] = HexList(self.ERASED_PATTERN * (word_size * 2))
            self.debugger.writeMemory(start_address, first_block)
        # end if
        if reset_last_app_word:
            # Get the last 1024 bytes of the application memory range including the Application Validity Flag Address
            # It's a workaround to a JLink dll issue which prevent to erase a word which is already programmed
            start_address = (f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress - block_size)
            last_block = self.debugger.readMemory(start_address, block_size)
            last_block[-word_size:] = HexList(self.ERASED_PATTERN * word_size)
            self.debugger.writeMemory(start_address, last_block)
        # end if
        if reset_vector_sd_word:
            # Get the first 1024 bytes of the application memory range including the SoftDevice Reset Vector Address
            # It's a workaround to a JLink dll issue which prevent to erase a word which is already programmed
            start_address = f.PRODUCT.FEATURES.COMMON.DFU.F_LowestSoftDeviceAddress
            first_block = self.debugger.readMemory(start_address, block_size)
            first_block[:word_size * 2] = HexList(self.ERASED_PATTERN * (word_size * 2))
            self.debugger.writeMemory(start_address, first_block)
        # end if
        self.debugger.exclude_flash_cache_range(start_address,
                                                f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress)
        self.debugger.run()
    # end def _erased_entity_valid_flag
# end class SharedDfuTestCaseRobustness

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
