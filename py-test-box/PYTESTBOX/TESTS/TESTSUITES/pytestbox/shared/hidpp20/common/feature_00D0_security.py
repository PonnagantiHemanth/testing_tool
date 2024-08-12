#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hidpp20.common.feature_00D0_security
:brief: Shared HID++ 2.0 Common feature 0x00D0
:author: Stanislas Cottard
:date: 2019/09/05
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from os.path import join
from random import randint

# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pyhid.tools.lexenddfufileparser import LexendDfuFileParser
from pyhid.tools.lexenddfufileparser import SECP256R1Parameters
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.dfuprocessing import CommonDfuTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedDfuTestCaseSecurity(CommonDfuTestCase):
    """
    Validates DFU Security TestCases
    """

    def _test_bad_program_data(self, command_1_index, packet_index, dfu_file_parser=None):
        """
        Goal: Check signature verification fails when signature is valid but firmware is modified.

        Synopsis:
         * Get signature corresponding to correct firmware
         * Invert a single bit in firmware
         * Generate DFU
         * Perform DFU
         * Check signature verification fails
         * Loop over different bits in different section of the firmware

        Note: this method is made to select any packet in any command 1 of a dfu file parser

        :param command_1_index: Index of the command 1
        :type command_1_index: ``int``
        :param packet_index: Index of the packet to modify
        :type packet_index: ``int``
        :param dfu_file_parser: DFU file parser
        :type dfu_file_parser: ``DfuFileParser``
        """
        if dfu_file_parser is None:
            dfu_file_path = str(join(
                TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName))
            dfu_file_parser = DfuFileParser.parse_dfu_file(
                dfu_file_path=dfu_file_path,
                device_index=ChannelUtils.get_device_index(self),
                dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
                dfu_feature_version=self.get_dfu_version())
        # end if

        program_data_packets = dfu_file_parser.command_1[command_1_index][1]
        data_size = to_int(dfu_file_parser.command_1[command_1_index][0].size)
        selected_packet = program_data_packets[packet_index]
        max_range = len(selected_packet.data) * 8 - 1
        min_range = (max_range
                     - (max_range if packet_index != len(program_data_packets) - 1
                        else (data_size % len(selected_packet.data)) * 8 - 1))
        bit_index = randint(min_range, max_range)
        # end if
        selected_packet.data.invertBit(bit_index)

        self.post_requisite_program_mcu_initial_state = True
        DfuTestUtils.perform_device_firmware_update(
            test_case=self,
            dfu_start_command=dfu_file_parser.dfu_start_command,
            program_data=dfu_file_parser.command_1,
            check_data=dfu_file_parser.command_2,
            command_3=dfu_file_parser.command_3,
            expected_status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE)

        # Revert last change
        selected_packet.data.invertBit(bit_index)
    # end def _test_bad_program_data

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_bad_valid_flag(self):
        """
        Goal: Check signature verification fails when signature is valid but firmware is modified (modify valid flag
        data)

        Synopsis:
         * Get signature corresponding to correct firmware
         * Invert a single bit in firmware
         * Generate DFU
         * Perform DFU
         * Check signature verification fails
         * Loop over different bits in different section of the firmware
        """
        dfu_file_path = str(join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName))
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=ChannelUtils.get_device_index(self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())
        valid_flag_data_packets = dfu_file_parser.command_1[
            LexendDfuFileParser.PROGRAM_DATA_VALID_FLAG_INDEX][LexendDfuFileParser.COMMAND_1_OR_2_DATA_PACKETS_INDEX]
        assert len(valid_flag_data_packets) == 1
        self._test_bad_program_data(LexendDfuFileParser.PROGRAM_DATA_VALID_FLAG_INDEX, 0, dfu_file_parser)

        self.testCaseChecked("SEC_00D0_0021")
    # end def test_bad_valid_flag

    def _test_bad_fw(self, part_index, n_parts=3):
        """
        Goal: Check signature verification fails when signature is valid but firmware is modified.

        Synopsis:
         * Get signature corresponding to correct firmware
         * Invert a single bit in firmware
         * Generate DFU
         * Perform DFU
         * Check signature verification fails
         * Loop over different bits in different section of the firmware

        Note: With this method, it is possible to choose to split the data in `n_parts` parts and to select the
        `part_index` part.

        :param part_index: Part to test
        :type part_index: ``int``
        :n_parts : Number of parts to split the data
        :type n_parts: ``int``
        """
        dfu_file_path = str(join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName))
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=ChannelUtils.get_device_index(self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        program_data_packets = dfu_file_parser.command_1[
            LexendDfuFileParser.PROGRAM_DATA_APPLICATION_INDEX][LexendDfuFileParser.COMMAND_1_OR_2_DATA_PACKETS_INDEX]
        range_begin = part_index * len(program_data_packets) // n_parts
        range_end = min((part_index + 1) * len(program_data_packets) // n_parts, len(program_data_packets))
        packet_index = randint(range_begin, range_end - 1)
        self._test_bad_program_data(LexendDfuFileParser.PROGRAM_DATA_APPLICATION_INDEX, packet_index, dfu_file_parser)
    # end def _test_bad_fw

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_bad_fw_part_0(self):
        """
        Goal: Check signature verification fails when signature is valid but firmware is modified (modify first part
        of the firmware data)

        Synopsis:
         * Get signature corresponding to correct firmware
         * Invert a single bit in firmware
         * Generate DFU
         * Perform DFU
         * Check signature verification fails
         * Loop over different bits in different section of the firmware
        """
        self._test_bad_fw(part_index=0)
        self.testCaseChecked("SEC_00D0_0001#2")
    # end def test_bad_fw_part_0

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_bad_fw_part_1(self):
        """
        Goal: Check signature verification fails when signature is valid but firmware is modified (modify second part
        of the firmware data)

        Synopsis:
         * Get signature corresponding to correct firmware
         * Invert a single bit in firmware
         * Generate DFU
         * Perform DFU
         * Check signature verification fails
         * Loop over different bits in different section of the firmware
        """
        self._test_bad_fw(part_index=1)
        self.testCaseChecked("SEC_00D0_0002#2")
    # end def test_bad_fw_part_1

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_bad_fw_part_2(self):
        """
        Goal: Check signature verification fails when signature is valid but firmware is modified (modify third part
        of the firmware data)

        Synopsis:
         * Get signature corresponding to correct firmware
         * Invert a single bit in firmware
         * Generate DFU
         * Perform DFU
         * Check signature verification fails
         * Loop over different bits in different section of the firmware
        """
        self._test_bad_fw(part_index=2)
        self.testCaseChecked("SEC_00D0_0003#2")
    # end def test_bad_fw_part_2

    def _test_signature_component_out_of_range(self, component, value):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF..FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.

        Note: With this method, it is possible to select the component and the value for the test

        :param component: Signature component (r or s)
        :type component: ``str``
        :param value: Value of the component
        :type value: ``HexList``
        """
        dfu_file_path = str(join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName))
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=ChannelUtils.get_device_index(self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        signature = dfu_file_parser.signature_from_check_data()
        if component == "r":
            signature[:(len(signature) // 2)] = value
        elif component == "s":
            signature[(len(signature) // 2):] = value
        else:
            raise ValueError("Invalid component name")
        # end if
        check_data = dfu_file_parser.signature_to_check_data(signature)

        self.post_requisite_program_mcu_initial_state = True
        DfuTestUtils.perform_device_firmware_update(
            test_case=self,
            dfu_start_command=dfu_file_parser.dfu_start_command,
            program_data=dfu_file_parser.command_1,
            check_data=check_data,
            command_3=dfu_file_parser.command_3,
            expected_status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE,
            status_time_limit=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CheckValidateStatusFailAtInitTimeLimit
        )
    # end def _test_signature_component_out_of_range

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_signature_r_out_of_range_zero(self):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid (r = 0)

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF..FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.
        """
        self._test_signature_component_out_of_range("r", HexList("00" * (LexendDfuFileParser.SIGNATURE_SIZE // 2)))
        self.testCaseChecked("SEC_00D0_0020#1")
    # end def test_ecdsap256_signature_r_out_of_range_zero

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_signature_s_out_of_range_zero(self):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid (s = 0)

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF..FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.
        """
        self._test_signature_component_out_of_range("s", HexList("00" * (LexendDfuFileParser.SIGNATURE_SIZE // 2)))
        self.testCaseChecked("SEC_00D0_0020#2")
    # end def test_ecdsap256_signature_s_out_of_range_zero

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_signature_r_out_of_range_all_FF(self):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid (r = FF...FF)

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF...FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.
        """
        self._test_signature_component_out_of_range("r", HexList("FF" * (LexendDfuFileParser.SIGNATURE_SIZE // 2)))
        self.testCaseChecked("SEC_00D0_0020#3")
    # end def test_ecdsap256_signature_r_out_of_range_all_FF

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_signature_s_out_of_range_all_FF(self):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid (s = FF...FF)

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF...FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.
        """
        self._test_signature_component_out_of_range("s", HexList("FF" * (LexendDfuFileParser.SIGNATURE_SIZE // 2)))
        self.testCaseChecked("SEC_00D0_0020#4")
    # end def test_ecdsap256_signature_s_out_of_range_all_FF

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_signature_r_out_of_range_n(self):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid (r = n)

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF...FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.
        """
        self._test_signature_component_out_of_range("r", SECP256R1Parameters.n)
        self.testCaseChecked("SEC_00D0_0020#5")
    # end def test_ecdsap256_signature_r_out_of_range_n

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_signature_s_out_of_range_n(self):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid (s = n)

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF...FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.
        """
        self._test_signature_component_out_of_range("s", SECP256R1Parameters.n)
        self.testCaseChecked("SEC_00D0_0020#6")
    # end def test_ecdsap256_signature_s_out_of_range_n

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_signature_r_out_of_range_random(self):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid (r = random value)

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF...FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.
        """
        random_value = HexList(Numeral(
            randint(to_int(SECP256R1Parameters.n), to_int(HexList("FF" * (LexendDfuFileParser.SIGNATURE_SIZE // 2)))),
            LexendDfuFileParser.SIGNATURE_SIZE // 2))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Random value: {random_value}")
        # --------------------------------------------------------------------------------------------------------------
        self._test_signature_component_out_of_range("r", random_value)
        self.testCaseChecked("SEC_00D0_0020#7")
    # end def test_ecdsap256_signature_r_out_of_range_random

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_signature_s_out_of_range_random(self):
        """
        Goal: Check signature verification fails when either component of the signature is out of range but firmware
        is valid (s = random value)

        Synopsis:
         * Get signature with "out of range" components (r and/or s = 0, r and/or s >= modulus in ECDSA P256 algorithm)
         * Perform DFU
         * Check signature verification fails
         * Loop over multiple signatures with "out of range" components values in range from modulus value to FF...FF,
         and 0

        Note: This MUST fail at the initialization, before the computation by the algorithm.
        """
        random_value = HexList(Numeral(
            randint(to_int(SECP256R1Parameters.n), to_int(HexList("FF" * (LexendDfuFileParser.SIGNATURE_SIZE // 2)))),
            LexendDfuFileParser.SIGNATURE_SIZE // 2))
        self._test_signature_component_out_of_range("s", random_value)
        self.testCaseChecked("SEC_00D0_0020#8")
    # end def test_ecdsap256_signature_s_out_of_range_random

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'ECDSA-P256')
    @level('Security')
    @services('Debugger')
    def test_ecdsap256_wrong_signature_modified_hash(self):
        """
        Goal: Check signature verification fails when signature is wrong but firmware is valid

        Synopsis:
         * Get SHA256 hash (before signature)
         * Invert a single bit in hash
         * Get wrong signature applying signature algorithm with modified digest
         * Generate DFU
         * Perform DFU
         * Check signature verification fails
         * Loop over different bits the hash
        """
        dfu_file_path = str(join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName))
        prv_key_path = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')

        # Init DFU file parser
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=ChannelUtils.get_device_index(self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())
        dfu_file_parser.init_prv_key(prv_key_path=prv_key_path)

        # Get data to sign
        data_to_sign = dfu_file_parser.get_data_to_sign(
            app_start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress,
            app_end_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress)

        # Prehash
        data_hash = dfu_file_parser.get_hash(data_to_sign)

        # Modify hash
        bit_index = randint(0, len(data_hash) * 8 - 1)
        data_hash.invertBit(bit_index)

        # Sign and get check data
        signature = dfu_file_parser.sign(data=data_hash, prehashed=True)
        signature = dfu_file_parser.signature_to_raw(signature)
        check_data = dfu_file_parser.signature_to_check_data(signature)

        self.post_requisite_program_mcu_initial_state = True
        DfuTestUtils.perform_device_firmware_update(
            test_case=self,
            dfu_start_command=dfu_file_parser.dfu_start_command,
            program_data=dfu_file_parser.command_1,
            check_data=check_data,
            command_3=dfu_file_parser.command_3,
            expected_status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE)

        self.testCaseChecked("SEC_00D0_0022")
    # end def test_ecdsap256_wrong_signature_modified_hash

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadFw01(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on the 'bad_fw01.dfu' file.
                        Inverted firmware bit:  Bit n flipped in the middle part of the message body.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_fw01.dfu"),
            dfu_file_name_in_log="bad_fw01.dfu")

        self.testCaseChecked("SEC_00D0_0001")
    # end def test_BadFw01

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadFw02(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on the 'bad_fw02.dfu' file.
                        Inverted firmware bit:  Bit n flipped in the first part of the message body.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_fw02.dfu"),
            dfu_file_name_in_log="bad_fw02.dfu")

        self.testCaseChecked("SEC_00D0_0002")
    # end def test_BadFw02

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadFw03(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on the 'bad_fw03.dfu' file.
                        Inverted firmware bit:  Bit n flipped in the last part of the message body.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_fw03.dfu"),
            dfu_file_name_in_log="bad_fw03.dfu")

        self.testCaseChecked("SEC_00D0_0003")
    # end def test_BadFw03

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadPkcs1Dgst(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on the 'bad_pkcs1_dgst.dfu' file.
                        Shifted PKCS #1 digest: Simulation of Bleichenbacher attack (LSB = 22).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_pkcs1_dgst.dfu"),
            dfu_file_name_in_log="bad_pkcs1_dgst.dfu")

        self.testCaseChecked("SEC_00D0_0004")
    # end def test_BadPkcs1Dgst

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadPkcs1Hdr01(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on the 'bad_pkcs1_hdr01.dfu' file.
                        Inverted PKCS #1 digest bit: Bit 1648 (byte 206, bit 7, header: [1640, 1791]).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_pkcs1_hdr01.dfu"),
            dfu_file_name_in_log="bad_pkcs1_hdr01.dfu")

        self.testCaseChecked("SEC_00D0_0005")
    # end def test_BadPkcs1Hdr01

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadPkcs1Hdr02(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on the 'bad_pkcs1_hdr02.dfu' file.
                        Inverted PKCS #1 digest bit: Bit 1696 (byte 212, bit 7, header: [1640, 1791]).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_pkcs1_hdr02.dfu"),
            dfu_file_name_in_log="bad_pkcs1_hdr02.dfu")

        self.testCaseChecked("SEC_00D0_0006")
    # end def test_BadPkcs1Hdr02

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadPkcs1Pad01(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on 'bad_pkcs1_pad01.dfu' file
                        Inverted PKCS #1 digest bit: Bit 15 (byte 1, bit 0, 2nd padding byte: [8, 15]).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_pkcs1_pad01.dfu"),
            dfu_file_name_in_log="bad_pkcs1_pad01.dfu")

        self.testCaseChecked("SEC_00D0_0007")
    # end def test_BadPkcs1Pad01

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadPkcs1Pad02(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on 'bad_pkcs1_pad02.dfu' file
                        Inverted PKCS #1 digest bit: Bit 265 (byte 33, bit 6, one padding: [16, 1631]).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_pkcs1_pad02.dfu"),
            dfu_file_name_in_log="bad_pkcs1_pad02.dfu")

        self.testCaseChecked("SEC_00D0_0008")
    # end def test_BadPkcs1Pad02

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadPkcs1Pad03(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on 'bad_pkcs1_pad03.dfu' file
                        Inverted PKCS #1 digest bit: Bit 1028 (byte 128, bit 3, one padding: [16, 1631]).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_pkcs1_pad03.dfu"),
            dfu_file_name_in_log="bad_pkcs1_pad03.dfu")

        self.testCaseChecked("SEC_00D0_0009")
    # end def test_BadPkcs1Pad03

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadPkcs1Pad04(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on 'bad_pkcs1_pad04.dfu' file
                        Inverted PKCS #1 digest bit: Bit 1636 (byte 204, bit 3, last padding byte: [1632, 1639]).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_pkcs1_pad04.dfu"),
            dfu_file_name_in_log="bad_pkcs1_pad04.dfu")

        self.testCaseChecked("SEC_00D0_0010")
    # end def test_BadPkcs1Pad04

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadRsaVal1(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on 'bad_rsa_val01.dfu' file
                        Invalid RSA value: Signature = RSA modulus.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_rsa_val01.dfu"),
            dfu_file_name_in_log="bad_rsa_val01.dfu")

        self.testCaseChecked("SEC_00D0_0011")
    # end def test_BadRsaVal1

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadRsaVal2(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on 'bad_rsa_val02.dfu' file
                        Invalid RSA value: Signature = 2^2048 - 1 (all 1's).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_rsa_val02.dfu"),
            dfu_file_name_in_log="bad_rsa_val02.dfu")

        self.testCaseChecked("SEC_00D0_0012")
    # end def test_BadRsaVal2

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadSha1(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on 'bad_sha01.dfu' file
                        Inverted PKCS #1 digest bit: Bit 2002 (byte 250, bit 5, SHA-256: [1792, 2047]).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_sha01.dfu"),
            dfu_file_name_in_log="bad_sha01.dfu")

        self.testCaseChecked("SEC_00D0_0013")
    # end def test_BadSha1

    @features('Feature00D0')
    @features('DFUSignatureAlgorithm', 'RSA')
    @level('Security')
    @services('Debugger')
    def test_BadSha2(self):
        """
        @tc_synopsis    Execute dfu cryptographic test based on 'bad_sha02.dfu' file
                        Inverted PKCS #1 digest bit: Bit 1957 (byte 244, bit 2, SHA-256: [1792, 2047]).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_dfu_with_error(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", "bad_sha02.dfu"),
            dfu_file_name_in_log="bad_sha02.dfu")

        self.testCaseChecked("SEC_00D0_0014")
    # end def test_BadSha2

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_CBC)
    @level('Security')
    @services('Debugger')
    def test_CorruptedIvAesCbc(self):
        """
        @tc_synopsis    Decryption failure due to IV corruption when data are encrypted with AES algorithm in CBC
                        (Test 16, 24 and 32 bytes long keys).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_encrypted_dfu_with_error(algorithm=Dfu.EncryptionMode.AES_CBC,
                                              corrupted_iv=True,
                                              corrupted_program_data=False)

        self.testCaseChecked("SEC_00D0_0015")
    # end def test_CorruptedIvAesCbc

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_CFB)
    @level('Security')
    @services('Debugger')
    def test_CorruptedIvAesCfb(self):
        """
        @tc_synopsis    Decryption failure due to IV corruption when data are encrypted with AES algorithm in CFB
                        (Test 16, 24 and 32 bytes long keys).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_encrypted_dfu_with_error(algorithm=Dfu.EncryptionMode.AES_CFB,
                                              corrupted_iv=True,
                                              corrupted_program_data=False)

        self.testCaseChecked("SEC_00D0_0016")
    # end def test_CorruptedIvAesCfb

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_OFB)
    @level('Security')
    @services('Debugger')
    def test_CorruptedIvAesOfb(self):
        """
        @tc_synopsis    Decryption failure due to IV corruption when data are encrypted with AES algorithm in OFB
                        (Test 16, 24 and 32 bytes long keys).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_encrypted_dfu_with_error(algorithm=Dfu.EncryptionMode.AES_OFB,
                                              corrupted_iv=True,
                                              corrupted_program_data=False)

        self.testCaseChecked("SEC_00D0_0017")
    # end def test_CorruptedIvAesOfb

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_CBC)
    @level('Security')
    @services('Debugger')
    def test_CorruptedDataAesCbc(self):
        """
        @tc_synopsis    Decryption failure due to program data corruption (first and last blocks) when data are
                        encrypted with AES algorithm in CBC (Test 16, 24 and 32 bytes long keys).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_encrypted_dfu_with_error(algorithm=Dfu.EncryptionMode.AES_CBC,
                                              corrupted_iv=False,
                                              corrupted_program_data=True)

        self.testCaseChecked("SEC_00D0_0018")
    # end def test_CorruptedDataAesCbc

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_CFB)
    @level('Security')
    @services('Debugger')
    def test_CorruptedDataAesCfb(self):
        """
        @tc_synopsis    Decryption failure due to program data corruption (first and last blocks) when data are
                        encrypted with AES algorithm in CFB (Test 16, 24 and 32 bytes long keys).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_encrypted_dfu_with_error(algorithm=Dfu.EncryptionMode.AES_CFB,
                                              corrupted_iv=False,
                                              corrupted_program_data=True)

        self.testCaseChecked("SEC_00D0_0019")
    # end def test_CorruptedDataAesCfb

    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_OFB)
    @level('Security')
    @services('Debugger')
    def test_CorruptedDataAesOfb(self):
        """
        @tc_synopsis    Decryption failure due to program data corruption (first and last blocks) when data are
                        encrypted with AES algorithm in OFB (Test 16, 24 and 32 bytes long keys).

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        """

        # This function does all test step and checks
        self.perform_encrypted_dfu_with_error(algorithm=Dfu.EncryptionMode.AES_OFB,
                                              corrupted_iv=False,
                                              corrupted_program_data=True)

        self.testCaseChecked("SEC_00D0_0015")
    # end def test_CorruptedDataAesOfb

    def perform_dfu_with_error(self, dfu_file_path: str, dfu_file_name_in_log: str):
        """
        Perform a DFU that is suppose to fail on command 3, if log_step and log_check are <=0, there is no log message.

        @param dfu_file_path: The path of the DFU file to use
        @type dfu_file_path: str
        @param dfu_file_name_in_log: The name of the dfu file to print in the log
        @type dfu_file_name_in_log: str
        """
        # Get the supported version
        dfu_feature_version = self.get_dfu_version()

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Send dfuStart : 16 first bytes of {dfu_file_name_in_log} file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send dfuCmdData1 : next 16 bytes of {dfu_file_name_in_log} file is command 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=cmd_1,
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
                self.logTitle2(f'Test Step 3: Send dfuCmdDatax : next 16 bytes of {dfu_file_name_in_log} file is '
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
            self.logTitle2(f'Test Step 4: Send dfuCmdDatax : next 16 bytes of {dfu_file_name_in_log} file is command 2')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=cmd_2,
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
                self.logTitle2(f'Test Step 5: Send dfuCmdDatax : next 16 bytes of {dfu_file_name_in_log} file is check '
                               f'data packet {i+1}')
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
        self.logTitle2(f'Test Step 6: Send dfuCmdDatax : next 16 bytes of {dfu_file_name_in_log} file is command 3')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 6: Wait for dfuStatus with status = 0x22 (Firmware check failure)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE)
    # end def perform_dfu_with_error

    def perform_encrypted_dfu_with_error(self, algorithm: int, corrupted_iv: bool, corrupted_program_data: bool):
        """
        Perform a DFU that is supposed to fail on command 3, if log_step and log_check are <=0, there is no log message.

        :param algorithm: The encryption algorithm to use in Dfu.EncryptionMode
        :type algorithm: ``int``
        :param corrupted_iv: Corrupt the Initialization Vector
        :type corrupted_iv: ``bool``
        :param corrupted_program_data: Corrupt the program data
        :type corrupted_program_data: ``bool``
        """
        assert corrupted_iv or corrupted_program_data, \
            "This method is used for corrupted DFU and no corruption is requested"

        # Get the supported version
        f = self.getFeatures()
        dfu_feature_version = self.get_dfu_version()

        dfu_file_path = join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(self.deviceIndex)),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)

        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Send Encrypt the program data from the good.dfu file using '
                       f'{Dfu.AES_ENCRYPTION_MODE_STR_MAPPING[algorithm]} algorithm and the project-specific key')
        # ---------------------------------------------------------------------------
        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)
        dfu_file_parser.dfu_start_command.encrypt = algorithm
        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Send dfuStart : 16 first bytes of dfu file')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.dfu_start_command,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 1: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1
        step_number = 3

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 3: Send dfuCmdData1 : next 16 bytes of dfu file is command 1')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=cmd_1,
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 2: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            if corrupted_iv:
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 4: Send a corrupted IV by change 1 bit in the next 16 bytes block from '
                               f'program data list')
                # ---------------------------------------------------------------------------
                program_data_list[0].data[0] ^= 0x01
            else:
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 4: Send the IV: next 16 bytes block from program data list')
                # ---------------------------------------------------------------------------
            # end if
            dfu_status_response = self.send_report_wait_response(report=program_data_list[0],
                                                                 response_queue=self.hidDispatcher.common_message_queue,
                                                                 response_class_type=DfuStatusResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Check 3: Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ---------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            if corrupted_program_data:
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step 5: Corrupt the first and last packets of encrypted program data by flipping '
                               f'one bit')
                # ---------------------------------------------------------------------------
                program_data_list[1].data[0] ^= 0x01
                program_data_list[-1].data[0] ^= 0x01
                step_number = 6
            else:
                step_number = 5
            # end if

            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Loop over the number of program data packets to be sent = '
                           f'{len(program_data_list) - 1}, packet number should start at 2')
            # ---------------------------------------------------------------------------
            for i in range(1, len(program_data_list)):
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Test Step {step_number}: Send dfuCmdDatax : next 16 bytes of dfu file is program '
                               f'data packet {i+1}')
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

        step_number += 1

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step {step_number}: Send dfuCmdDatax : next 16 bytes of dfu file is command 2')
            # ---------------------------------------------------------------------------
            dfu_status_response = self.send_report_wait_response(report=cmd_2,
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
                self.logTitle2(f'Test Step {step_number + 1}: Send dfuCmdDatax : next 16 bytes of dfu file is check '
                               f'data packet {i+1}')
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

        step_number += 2

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step {step_number}: Send dfuCmdDatax : next 16 bytes of dfu file is command 3')
        # ---------------------------------------------------------------------------
        dfu_status_response = self.send_report_wait_response(report=dfu_file_parser.command_3,
                                                             response_queue=self.hidDispatcher.common_message_queue,
                                                             response_class_type=DfuStatusResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 6: Wait for dfuStatus with status = 0x22 (Firmware check failure)')
        # ---------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.FIRMWARE_CHECK_FAILURE)
    # end def perform_encrypted_dfu_with_error
# end class SharedDfuTestCaseSecurity


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
