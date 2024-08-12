#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.hidpp20.common.feature_00D0_change_flag
:brief: Shared HID++ 2.0 Common feature 0x00D0
:author: Stanislas Cottard
:date: 2019/09/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join

# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.bootloadertest import CommonBootloaderTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.dfuprocessing import CommonDfuTestCase
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedDfuTestCaseChangeFlag(CommonDfuTestCase):
    """
    Validate DFU TestCases that needs to change the DFU flag
    """

    def setUp(self):
        """
        Handle test setup, prerequisites will be done separately.
        """
        # We do only the setup of the great-grandparent class and skip the one of the parent to prevent the switch to
        # bootloader mode
        super(CommonBootloaderTestCase, self).setUp()

        if self.debugger is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Backup initial NVS')
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.read_nvs(backup=True)
        # end if
    # end def setUp

    def pre_requisite(self, flag):
        """
        Handle test prerequisites.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Program the DFU Flags with a dfuStart.flag = {hex(flag)}')
        # --------------------------------------------------------------------------------------------------------------
        f = self.getFeatures()
        hex_to_load = HexList()

        for i in range(8):
            if ((flag >> i) & 0x01) != 0:
                hex_to_load += HexList(Numeral(f.PRODUCT.FEATURES.COMMON.DFU.F_FlagBitSetValueInNvs, 4))
            else:
                hex_to_load += HexList(Numeral(f.PRODUCT.FEATURES.COMMON.DFU.F_FlagBitClearedValueInNvs, 4))
            # end if
        # end for

        self.debugger.stop()
        self.debugger.writeMemory(f.PRODUCT.FEATURES.COMMON.DFU.F_AddressForFlagInNvs, hex_to_load)
        self.debugger.reset()
        self.reset()

        self.dut_jump_on_bootloader()

    # end def pre_requisite

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Program the DFU Flags back to its initial state')
            # ----------------------------------------------------------------------------------------------------------
            f = self.getFeatures()
            self.debugger.stop()
            self.debugger.writeMemory(f.PRODUCT.FEATURES.COMMON.DFU.F_AddressForFlagInNvs, HexList("FF" * 32))
            self.debugger.reset()
        # end with
        super().tearDown()
    # end def tearDown

    @features('Feature00D0V1+')
    @features('Feature00D0VerifyFlag')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationFlag0x00To0x01(self):
        """
        Create a DFU with the flag parameter set to 0x01 to update a firmware with flag = 0x00.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(flag=0x00)

        # This function does all steps and checks
        self._load_app_dfu_with_requested_flag(0x01)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0024")
    # end def test_ApplicationFlag0x00To0x01

    @features('Feature00D0V1+')
    @features('Feature00D0VerifyFlag')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationFlag0x01To0x01(self):
        """
        Create a DFU with the flag parameter set to 0x01 to update a firmware with flag = 0x01.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(flag=0x01)

        # This function does all steps and checks
        self._load_app_dfu_with_requested_flag(0x01)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0025")
    # end def test_ApplicationFlag0x01To0x01

    @features('Feature00D0V1+')
    @features('Feature00D0VerifyFlag')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationFlag0x00To0xFF(self):
        """
        Create a DFU with the flag parameter set to 0xFF to update a firmware with flag = 0x00.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(flag=0x00)

        # This function does all steps and checks
        self._load_app_dfu_with_requested_flag(0xFF)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0026")
    # end def test_ApplicationFlag0x00To0xFF

    @features('Feature00D0V1+')
    @features('Feature00D0VerifyFlag')
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_ApplicationFlag0x55To0x55(self):
        """
        Check the device accepts to process a DFU when all the bits set in the bootloader copy of the
                        flag are also set in the DfuStart flag parameter.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(flag=0x55)

        # This function does all steps and checks
        self._load_app_dfu_with_requested_flag(0x55)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0027")
    # end def test_ApplicationFlag0x55To0x55

    @features('Feature00D0V1+')
    @features('Feature00D0VerifyFlag')
    @level('ErrorHandling')
    @services('Debugger')
    def test_ApplicationFlag0x55To0x54(self):
        """
        Check the device refuses to process a DFU when some bit of the flag parameter have been reset
                        compared to the one already installed

        [event0] dfuStatus() -> pktNb, status, param


        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(flag=0x55)

        # This function does all steps and checks
        self._load_app_dfu_with_requested_flag(0x54, True)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("ROT_00D0_0002")
    # end def test_ApplicationFlag0x55To0x54

    @features('Feature00D0V1+')
    @features('Feature00D0VerifyFlag')
    @features('Feature00D0SoftDevice')
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_SoftDeviceFlag0x00_ApplicationFlag0x55To0x55(self):
        """
        Check the UICR.Flags are ignored when processing a SoftDevice update

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(flag=0x55)

        # SoftDevice DFU sequence
        self._load_sd_dfu_with_requested_flag(0x00)

        self.reset(hardware_reset=True)

        # Application DFU sequence
        self._load_app_dfu_with_requested_flag(0x55)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0043")
    # end def test_SoftDeviceFlag0x00_ApplicationFlag0x55To0x55

    @features('Feature00D0V1+')
    @features('Feature00D0VerifyFlag')
    @features('Feature00D0SoftDevice')
    @level('Time-consuming')
    @services('Debugger')
    def test_SoftDeviceFlag0x01(self):
        """
        Check the SoftDevice DFU Flag shall be 0x00

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(flag=0x00)

        # SoftDevice DFU sequence
        self._load_sd_dfu_with_requested_flag(0x01, True)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0044")
    # end def test_SoftDeviceFlag0x01

    def _load_app_dfu_with_requested_flag(self, flag_for_dfu, error_expected=False):

        # Get the supported version
        f = self.getFeatures()
        dfu_feature_version = self.get_dfu_version()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Change dfuStart.flag of Regular_application.dfu file to {hex(flag_for_dfu)} and '
                                 f'sign it to create flag{hex(flag_for_dfu)}_application.dfu file')
        # ---------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=ChannelUtils.get_device_index(test_case=self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        dfu_file_parser.dfu_start_command.flag = flag_for_dfu

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self._perform_dfu(dfu_file_parser, error_expected)
    # end def _load_dfu_with_requested_flag

    def _load_sd_dfu_with_requested_flag(self, flag_for_dfu, error_expected=False):

        # Get the supported version
        f = self.getFeatures()
        dfu_feature_version = self.get_dfu_version()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Change dfuStart.flag of Regular_softdevice.dfu file to {hex(flag_for_dfu)} and '
                                 f'sign it to create flag{hex(flag_for_dfu)}_softdevice.dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=ChannelUtils.get_device_index(test_case=self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        dfu_file_parser.dfu_start_command.flag = flag_for_dfu

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                        key_file,
                                        max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                        min_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress,
                                        additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self._perform_dfu(dfu_file_parser, error_expected)
    # end def _load_sd_dfu_with_requested_flag

    def _perform_dfu(self, dfu_file_parser, error_expected):

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuStart : 16 first bytes of the .dfu file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(test_case=self, report=dfu_file_parser.dfu_start_command,
                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        if error_expected:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x24 (Bad/incompatible flag field)')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.BAD_INCOMPATIBLE_FLAG_FIELD)
            return

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send dfuCmdData1 : next 16 bytes of file is command 1')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(test_case=self, report=cmd_1,
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over the number of program data packets to be sent = '
                                     f'{len(program_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send dfuCmdDatax : next 16 bytes of .dfu file is program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(test_case=self, report=program_data_list[i],
                                                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                        response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and '
                                          f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send dfuCmdDatax : next 16 bytes of file is command 2')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(test_case=self, report=cmd_2,
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and '
                                      f'pktNb = {sequence_number}')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over the number of check data packets to be sent = '
                                     f'{len(check_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send dfuCmdDatax : next 16 bytes of file is check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(test_case=self, report=check_data_list[i],
                                                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                        response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and '
                                          f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuCmdDatax : next 16 bytes of .dfu file is command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(test_case=self, report=dfu_file_parser.command_3,
                                                response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x02 or 0x06 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ALL_DFU_SUCCESS)
    # end def _perform_dfu
# end class SharedDfuTestCaseChangeFlag

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
