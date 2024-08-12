#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8101.errorhandling
:brief: HID++ 2.0 ``ProfileManagement`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import random
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.gaming.profilemanagement import EditBuffer
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import DirectoryFile
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.mcu.profileformat import KeyAction
from pylibrary.mcu.profileformat import MacroEndCommand
from pylibrary.mcu.profileformat import MouseButtonCommand
from pylibrary.mcu.profileformat import PresetMacroEntry
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hidpp20.gaming.feature_8101.profilemanagement import ProfileManagementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class ProfileManagementErrorHandlingTestCase(ProfileManagementTestCase):
    """
    Validate ``ProfileManagement`` errorhandling test cases
    """

    @features("Feature8101")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_8101.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.get_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index)
            report.function_index = function_index

            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature8101")
    @level("ErrorHandling")
    def test_get_profile_tag_list_with_invalid_offset_byte(self):
        """
        getProfileTagList.offset_bytes equals or exceeds the length of the profile tag list shall raise an error
        """
        length_of_tag_list = ProfileManagementTestUtils.get_len_of_tag_list_from_settings(test_case=self)
        invalid_offset_list = [random.randint(length_of_tag_list, 0xFFFF) for _ in range(10)] \
            + [length_of_tag_list, 0xFFFF]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over invalid_offset_bytes in {invalid_offset_list}")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_offset in invalid_offset_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getProfileTagList request with offset_bytes={invalid_offset}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.get_profile_tag_list_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                offset_bytes=invalid_offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0002", _AUTHOR)
    # end def test_get_profile_tag_list_with_invalid_offset_byte

    @features("Feature8101")
    @level("ErrorHandling")
    def test_start_write_buffer_with_invalid_count(self):
        """
        startWriteBuffer.count exceeds RAM buffer size shall raise an error
        """
        invalid_count_list = [random.randint(self.config.F_RamBufferSize + 1, 0xFFFF) for _ in range(10)] \
            + [self.config.F_RamBufferSize + 1, 0xFFFF]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over invalid_count in {invalid_count_list}")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_count in invalid_count_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send startWriteBuffer request with count={invalid_count}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.start_write_buffer_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                count=invalid_count)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getError request")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is 0x03(NVS error)")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.GetErrorResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "fs_error_code": (checker.check_fs_error_code,
                                  ProfileManagement.FileSystemErrorCode.SIZE_EXCEEDS_BUFFER_CAPACITY),
                "fs_error_param_1": (checker.check_fs_error_param_1, invalid_count),
                "fs_error_param_2": (checker.check_fs_error_param_2,
                                     ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
            })
            checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0003", _AUTHOR)
    # end def test_start_write_buffer_with_invalid_count

    @features("Feature8101")
    @level("ErrorHandling")
    def test_address_to_write_beyond_end_of_ram_buffer(self):
        """
        Address to write is beyond end of RAM buffer shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send startWriteBuffer request with count={self.config.F_RamBufferSize}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(test_case=self, count=self.config.F_RamBufferSize)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop in range({int(self.config.F_RamBufferSize/16)})")
        # --------------------------------------------------------------------------------------------------------------
        for i in range(int(self.config.F_RamBufferSize/16)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send writeBuffer request")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.write_buffer(test_case=self, data=RandHexList(16))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send writeBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.write_buffer_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            data=RandHexList(16))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_8101_0004", _AUTHOR)
    # end def test_address_to_write_beyond_end_of_ram_buffer

    @features("Feature8101")
    @level("ErrorHandling")
    def test_edit_buffer_with_invalid_opcode(self):
        """
        Invalid editBuffer.opcode shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=16)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=RandHexList(16))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over invalid_opcode in [0b000, 0b011, 0b101, 0b110, 0b111]")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_opcode in [0b000, 0b011, 0b101, 0b110, 0b111]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send editBuffer request with opcode={invalid_opcode} and all other inputs with"
                                     "valid value")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.edit_buffer_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                count=1,
                opcode=invalid_opcode,
                address=0,
                data=RandHexList(13))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0005", _AUTHOR)
    # end def test_edit_buffer_with_invalid_opcode

    @features("Feature8101")
    @level("ErrorHandling")
    def test_edit_buffer_with_invalid_count(self):
        """
        Invalid editBuffer.count shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=16)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=RandHexList(16))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over invalid_count in [0x0E, 0x0F]")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_count in [0x0E, 0x0F]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send editBuffer request with count={invalid_count} and all other inputs with"
                                     "valid value")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.edit_buffer_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                count=invalid_count,
                opcode=1,
                address=0,
                data=RandHexList(13))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0006", _AUTHOR)
    # end def test_edit_buffer_with_invalid_count

    @features("Feature8101")
    @level("ErrorHandling")
    def test_edit_buffer_with_invalid_address(self):
        """
        Invalid editBuffer.address shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=16)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=RandHexList(16))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over invalid_count in [0x0E, 0x0F]")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_address in [0x0E, 0x0F]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send editBuffer request with address={invalid_address} and all other inputs with valid value")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.edit_buffer_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                count=13,
                opcode=1,
                address=invalid_address,
                data=RandHexList(13))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0007", _AUTHOR)
    # end def test_edit_buffer_with_invalid_address

    @features("Feature8101")
    @level("ErrorHandling")
    def test_save_with_invalid_first_sector_id(self):
        """
        Invalid save.first_sector_id shall raise an error
        """
        self.post_requisite_reload_nvs = True
        data = RandHexList(16)
        invalid_first_sector_id_list = [random.randint(self.config.F_MaxSectorId + 1, 0xFFFF) for _ in range(10)] \
            + [self.config.F_MaxSectorId + 1, 0xFFFF]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over invalid_sector_id in {invalid_first_sector_id_list}")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_first_sector_id in invalid_first_sector_id_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send save request with first_sector_id={invalid_first_sector_id_list} and all "
                                     "other inputs with valid value")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.save_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                first_sector_id=invalid_first_sector_id,
                count=len(data),
                hash32=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(data))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0008", _AUTHOR)
    # end def test_save_with_invalid_first_sector_id

    @features("Feature8101")
    @level("ErrorHandling")
    def test_save_with_invalid_count(self):
        """
        Invalid save.count shall raise an error
        """
        self.post_requisite_reload_nvs = True
        data = RandHexList(16)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send save request with count=0")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.save_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            first_sector_id=ProfileManagement.SpecialFileId.FILE_ID_START,
            count=0x00,
            hash32=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_8101_0009", _AUTHOR)
    # end def test_save_with_invalid_count

    @features("Feature8101")
    @level("ErrorHandling")
    def test_save_with_incorrect_hash(self):
        """
        Invalid save.hash shall raise an error
        """
        self.post_requisite_reload_nvs = True
        data = RandHexList(16)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=data)

        hash32 = ProfileManagementTestUtils.ProfileHelper.calculate_crc32(data)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over incorrect hashes in range({len(hash32)})")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(len(hash32)):
            hash32[index] = 0xFF - hash32[index]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send save request with hash={hash32} and all other inputs with valid value")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.save_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                first_sector_id=ProfileManagement.SpecialFileId.FILE_ID_START,
                count=len(data),
                hash32=hash32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0010", _AUTHOR)
    # end def test_save_with_incorrect_hash

    @features("Feature8101")
    @level("ErrorHandling")
    def test_invalid_save_request_cause_hw_error(self):
        """
        HW_ERROR shall be raised when sending save command caused filesystem error
        
        NB: This error shall be able to be retrieved via [4]getError
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Send load request with first_sector_id={directory.first_sector_id_lsb} to load NVS "
                           "profile directory")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self, first_sector_id=directory.first_sector_id_lsb, count=len(HexList(directory)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send editBuffer request with address={DirectoryFile.HEADER_LENGTH - 1}, "
                                 f"data={HexList(self.config.F_MaxFileId + 1)}")
        # --------------------------------------------------------------------------------------------------------------
        directory_hex = HexList(directory)
        directory_hex[DirectoryFile.HEADER_LENGTH - 1] = HexList(self.config.F_MaxFileId + 1)
        directory_hex = directory.calculate_crc32(directory_hex[DirectoryFile.HEADER_LENGTH - 1:]) + \
            directory_hex[DirectoryFile.HEADER_LENGTH - 1:]
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=DirectoryFile.HEADER_LENGTH,
            opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE, address=0,
            data=directory_hex[:(EditBuffer.LEN.DATA // 8)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Send save request and check the HW_ERROR(0x04) is received")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.save_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            first_sector_id=directory.first_sector_id_lsb,
            count=len(HexList(directory)),
            hash32=directory_hex[:DirectoryFile.HEADER_LENGTH - 1])
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is 0x03(NVS error)")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code, ProfileManagement.FileSystemErrorCode.NVS_ERROR),
            "fs_error_param_1": (checker.check_fs_error_param_1, ProfileManagement.Partition.SectorId.NVS),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0011", _AUTHOR)
    # end def test_invalid_save_request_cause_hw_error

    @features("Feature8101")
    @level("ErrorHandling")
    def test_configure_with_invalid_feature_id(self):
        """
        Invalid configure.feature_id shall raise an error
        """
        data = RandHexList(16)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over invalid_feature_id in [0x0000, 0x1b04, 0x4522, 0x4523, 0xFFFF]")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_feature_id in [0x0000, 0x1b04, 0x4522, 0x4523, 0xFFFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send configure request with feature_id={invalid_feature_id} and all other"
                                     "inputs with valid value")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.configure_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                feature_id=invalid_feature_id,
                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                file_id=ProfileManagement.SpecialFileId.FILE_ID_START,
                count=0,
                hash_key=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(data))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getError request")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is "
                                      f"{ProfileManagement.FileSystemErrorCode.INVALID_FEATURE_ID_FILETYPE_ID}")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.GetErrorResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "fs_error_code": (checker.check_fs_error_code,
                                  ProfileManagement.FileSystemErrorCode.INVALID_FEATURE_ID_FILETYPE_ID),
                "fs_error_param_1": (checker.check_fs_error_param_1, invalid_feature_id),
                "fs_error_param_2": (checker.check_fs_error_param_2,
                                     ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
            })
            checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0012", _AUTHOR)
    # end def test_configure_with_invalid_feature_id

    @features("Feature8101")
    @level("ErrorHandling")
    def test_configure_with_invalid_file_type_id(self):
        """
        Invalid configure.file_type_id shall raise an error
        """
        invalid_file_type_id_of_features = \
            {ProfileManagement.FEATURE_ID: range(ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE + 1, 4)}
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create valid 0x8101 feature setting files")
        # --------------------------------------------------------------------------------------------------------------
        profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(self, directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Test Loop: Loop over supported_feature_id, invalid_file_type_ids "
                  f"in {invalid_file_type_id_of_features}")
        # --------------------------------------------------------------------------------------------------------------
        for supported_feature_id in invalid_file_type_id_of_features.keys():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: Loop over invalid_file_type_id "
                                     f"in {invalid_file_type_id_of_features[supported_feature_id]}")
            # ----------------------------------------------------------------------------------------------------------
            for invalid_file_type_id in invalid_file_type_id_of_features[supported_feature_id]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send configure request with file_type_id={invalid_file_type_id},"
                                         "feature_id=supported_feature_id and all other inputs with valid value")
                # ------------------------------------------------------------------------------------------------------
                report = self.feature_8101.configure_cls(
                    device_index=ChannelUtils.get_device_index(test_case=self),
                    feature_index=self.feature_8101_index,
                    feature_id=supported_feature_id,
                    file_type_id=invalid_file_type_id,
                    file_id=ProfileManagement.SpecialFileId.FILE_ID_START,
                    count=0,
                    hash_key=profile.crc_32)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                    test_case=self,
                    report=report,
                    error_codes=[ErrorCodes.INVALID_ARGUMENT])
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0013", _AUTHOR)
    # end def test_configure_with_invalid_file_type_id

    @features("Feature8101")
    @level("ErrorHandling")
    def test_configure_with_invalid_file_id(self):
        """
        Invalid configure.file_id shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create valid 0x8101 feature setting files")
        # --------------------------------------------------------------------------------------------------------------
        profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(self, directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb + 1} and all other inputs "
                                 "with valid value")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.configure_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=profile.file_id_lsb + 1,
            count=len(HexList(profile)),
            hash_key=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is "
                                  f"{ProfileManagement.FileSystemErrorCode.MISSING_FILE_REFERENCE_IN_DIRECTORY}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code,
                              ProfileManagement.FileSystemErrorCode.MISSING_FILE_REFERENCE_IN_DIRECTORY),
            "fs_error_param_1": (checker.check_fs_error_param_1, profile.file_id_lsb + 1),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0014", _AUTHOR)
    # end def test_configure_with_invalid_file_id

    @features("Feature8101")
    @level("ErrorHandling")
    def test_configure_with_invalid_count(self):
        """
        Invalid configure.count shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create valid 0x8101 feature setting files")
        # --------------------------------------------------------------------------------------------------------------
        profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(self, directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send configure request with count=0 and all other inputs with valid value")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.configure_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=profile.file_id_lsb,
            count=0,
            hash_key=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is "
                                  f"{ProfileManagement.FileSystemErrorCode.FILE_DETAIL_MISMATCH}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code, ProfileManagement.FileSystemErrorCode.FILE_DETAIL_MISMATCH),
            "fs_error_param_1": (checker.check_fs_error_param_1, profile.file_id_lsb),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0015", _AUTHOR)
    # end def test_configure_with_invalid_count

    @features("Feature8101")
    @level("ErrorHandling")
    def test_configure_with_invalid_hash(self):
        """
        Invalid configure.hash shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create valid 0x8101 feature setting files")
        # --------------------------------------------------------------------------------------------------------------
        profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(self, directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send configure request with hash=invalid_hash and all other inputs with valid value")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.configure_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=profile.file_id_lsb,
            count=len(HexList(profile)),
            hash_key=HexList([0xFF - to_int(crc_8) for crc_8 in profile.crc_32]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is "
                                  f"{ProfileManagement.FileSystemErrorCode.FILE_DETAIL_MISMATCH}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code, ProfileManagement.FileSystemErrorCode.FILE_DETAIL_MISMATCH),
            "fs_error_param_1": (checker.check_fs_error_param_1, profile.file_id_lsb),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0016", _AUTHOR)
    # end def test_configure_with_invalid_hash

    @features("Feature8101")
    @level("ErrorHandling")
    def test_invalid_configure_request_cause_hw_error(self):
        """
        HW_ERROR shall be raised when sending configure command caused filesystem error
        
        NB: This error shall be able to be retrieved via [4]getError
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load request to load the profile directory of OOB")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(test_case=self,
                                                    first_sector_id=ProfileManagement.Partition.SectorId.OOB,
                                                    count=self.config.F_RamBufferSize)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.configure_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=ProfileManagement.Partition.FileId.RAM,
            count=to_int(self.config.OOB_PROFILE_DIRECTORY.F_Length[0]),
            hash_key=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(
                        ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(
                            test_case=self, count=to_int(self.config.OOB_PROFILE_DIRECTORY.F_Length[0]))))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is Feature Configuration Error "
                                  f"check error({ProfileManagement.FileSystemErrorCode.FEATURE_CONFIGURATION_ERROR})")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code,
                              ProfileManagement.FileSystemErrorCode.FEATURE_CONFIGURATION_ERROR),
            "fs_error_param_1": (checker.check_fs_error_param_1, ProfileManagement.FEATURE_ID),
            "fs_error_param_2": (checker.check_fs_error_param_2,
                                 ProfileManagement.CfgErrorCode.X8101.GENERIC_CONFIGURATION_ERROR),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0017", _AUTHOR)
    # end def test_invalid_configure_request_cause_hw_error

    @features("Feature8101")
    @level("ErrorHandling")
    def test_invalid_power_on_profile(self):
        """
        Invalid getSetPowerOnParams.power_on_profile shall raise an error
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSetPowerOnParams request with power_on_profile=inexist_file_id and all"
                                 "other inputs with valid value")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.get_set_power_on_params_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            set_power_on_profile=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=ProfileManagement.SpecialFileId.FILE_ID_START)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            "Wait getError response and check the fsErrorCode is Feature Configuration Error "
                            f"check error({ProfileManagement.FileSystemErrorCode.MISSING_FILE_REFERENCE_IN_DIRECTORY})")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code,
                              ProfileManagement.FileSystemErrorCode.MISSING_FILE_REFERENCE_IN_DIRECTORY),
            "fs_error_param_1": (checker.check_fs_error_param_1, ProfileManagement.SpecialFileId.FILE_ID_START),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0018", _AUTHOR)
    # end def test_invalid_power_on_profile

    @features("Feature8101")
    @level("ErrorHandling")
    def test_set_oob_profile_as_power_on_profile(self):
        """
        Validate the OOB profile can't be set as power-on profile thru getSetPowerOnParams.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           "Send getSetPowerOnParams request with power_on_profile="
                           f"{ProfileManagement.Partition.FileId.OOB | ProfileManagement.SpecialFileId.FILE_ID_START} "
                           "and all other inputs with valid value")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.get_set_power_on_params_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            set_power_on_profile=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=ProfileManagement.Partition.FileId.OOB | ProfileManagement.SpecialFileId.FILE_ID_START)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_8101_0019", _AUTHOR)
    # end def test_set_oob_profile_as_power_on_profile

    @features("Feature8101")
    @level("ErrorHandling")
    def test_invalid_get_set_power_on_params_request_cause_hw_error(self):
        """
        HW_ERROR shall be raised when sending getSetPowerOnParams command caused filesystem error
        
        
        NB: This error shall be able to be retrieved via [4]getError
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSetPowerOnParams request with power_on_profile="
                                 f"{ProfileManagement.SpecialFileId.PROFILE_DIRECTORY}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.get_set_power_on_params_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            set_power_on_profile=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=ProfileManagement.SpecialFileId.PROFILE_DIRECTORY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            "Wait getError response and check the fsErrorCode is Feature Configuration Error "
                            f"check error({ProfileManagement.FileSystemErrorCode.MISSING_FILE_REFERENCE_IN_DIRECTORY})")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code,
                              ProfileManagement.FileSystemErrorCode.MISSING_FILE_REFERENCE_IN_DIRECTORY),
            "fs_error_param_1": (checker.check_fs_error_param_1, ProfileManagement.SpecialFileId.PROFILE_DIRECTORY),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0020", _AUTHOR)
    # end def test_invalid_get_set_power_on_params_request_cause_hw_error

    @features("Feature8101")
    @level("ErrorHandling")
    def test_get_hashes_with_invalid_file_id(self):
        """
        Invalid getHashes.file_id shall raise an error
        """
        file_id_list = [0xFE, 0, 0, 0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over file_index in range(4)")
        # --------------------------------------------------------------------------------------------------------------
        for file_index in range(4):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHashes request with file_id[{file_index}]=inexist_file_id and all other"
                                     "inputs with valid value")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.get_hashes_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                compute=0,
                file_id_0=file_id_list[0],
                file_id_1=file_id_list[1],
                file_id_2=file_id_list[2],
                file_id_3=file_id_list[3])

            if file_index < 3:
                file_id_list[file_index], file_id_list[file_index + 1] = \
                    file_id_list[file_index + 1], file_id_list[file_index]
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0021", _AUTHOR)
    # end def test_get_hashes_with_invalid_file_id

    @features("Feature8101")
    @level("ErrorHandling")
    def test_read_buffer_with_invalid_offset_bytes(self):
        """
        readBuffer.offset_bytes equals or exceeds the RAM buffer size shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Load request to load OOB profile directory")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self,
            first_sector_id=ProfileManagement.Partition.SectorId.OOB,
            count=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send readBuffer request with offset_bytes={self.config.F_RamBufferSize + 1}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.read_buffer_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            offset_bytes=self.config.F_RamBufferSize + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is 0x03(NVS error)")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code,
                              ProfileManagement.FileSystemErrorCode.RAM_BUFFER_CHECK_ERROR),
            "fs_error_param_1": (checker.check_fs_error_param_1, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0022", _AUTHOR)
    # end def test_read_buffer_with_invalid_offset_bytes

    @features("Feature8101")
    @level("ErrorHandling")
    def test_load_with_invalid_first_sector_id(self):
        """
        Invalid load.first_sector_id shall raise an error
        """
        invalid_first_sector_ids = [random.randint(self.config.F_MaxSectorId + 1, 0xFFFF) for _ in range(10)] \
            + [self.config.F_MaxSectorId + 1, 0xFFFF]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over invalid_sector_id in {invalid_first_sector_ids}")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_sector_id in invalid_first_sector_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send load request with first_sector_id={invalid_sector_id} and all other inputs"
                                     "with valid value")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8101.load_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8101_index,
                first_sector_id=invalid_sector_id,
                count=1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getError request")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is 0x03(NVS error)")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.GetErrorResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "fs_error_code": (checker.check_fs_error_code, ProfileManagement.FileSystemErrorCode.INVALID_SECTOR_ID),
                "fs_error_param_1": (checker.check_fs_error_param_1, invalid_sector_id),
                "fs_error_param_2": (checker.check_fs_error_param_2,
                                     ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
            })
            checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0023", _AUTHOR)
    # end def test_load_with_invalid_first_sector_id

    @features("Feature8101")
    @level("ErrorHandling")
    def test_load_with_invalid_count(self):
        """
        Invalid load.count shall raise an error
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send load request with count={self.config.F_RamBufferSize + 1}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.load_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            first_sector_id=ProfileManagement.Partition.SectorId.OOB | 0x0001,
            count=self.config.F_RamBufferSize + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_8101_0024", _AUTHOR)
    # end def test_load_with_invalid_count

    @features("Feature8101")
    @level("ErrorHandling")
    def test_invalid_load_request_cause_hw_error(self):
        """
        Validate the FW generates 'NVS Error' when the FW executed load() function
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send load request with first_sector_id = {ProfileManagement.Partition.SectorId.NVS}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.load_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            first_sector_id=ProfileManagement.Partition.SectorId.NVS,
            count=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is 0x03(NVS error)")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code, ProfileManagement.FileSystemErrorCode.NVS_ERROR),
            "fs_error_param_1": (checker.check_fs_error_param_1, ProfileManagement.Partition.SectorId.NVS),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0025", _AUTHOR)
    # end def test_invalid_load_request_cause_hw_error

    @features("Feature8101")
    @level("ErrorHandling")
    def test_file_system_integrity_check_for_hash(self):
        """
        Validate the FW shall conduct a file system integrity check each time the SW modifies the directory(Hash/CRC
        error)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load request with first_sector_id=0x0000 to load NVS profile directory")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self, first_sector_id=directory.first_sector_id_lsb, count=len(HexList(directory)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send editBuffer request with address=0, "
                                 f"data={HexList((0xFFFFFFFF - to_int(directory.crc_32)).to_bytes(4, 'big'))}")
        # --------------------------------------------------------------------------------------------------------------
        correct_crc_32 = directory.crc_32
        directory.crc_32 = HexList((0xFFFFFFFF - to_int(directory.crc_32)).to_bytes(4, 'big'))
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=len(directory.crc_32), opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE,
            address=0, data=HexList(directory)[:(EditBuffer.LEN.DATA // 8)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Send save request and check HW_ERROR(0x04) is received")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.save_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            first_sector_id=directory.first_sector_id_lsb,
            count=len(HexList(directory)),
            hash32=correct_crc_32)
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is 0x04(Hash/CRC error)")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code, ProfileManagement.FileSystemErrorCode.CRC_CHECK_ERROR),
            "fs_error_param_1": (checker.check_fs_error_param_1, ProfileManagement.SpecialFileId.PROFILE_DIRECTORY),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("ERR_8101_0026", _AUTHOR)
    # end def test_file_system_integrity_check_for_hash

    @features("Feature8101")
    @level("ErrorHandling")
    def test_switch_to_a_missing_onboard_profiles(self):
        """
        Validate the FW returns an filesystem error "MISSING ONBOARD PROFILE"(0x0E) if the user switches to an undefined
        onboard profile.
        """
        standard_keys = list(STANDARD_KEYS.keys())
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2, KEY_ID.BUTTON_3, KEY_ID.BUTTON_4] \
            if self.f.PRODUCT.F_IsMice else standard_keys[standard_keys.index(KEY_ID.KEYBOARD_A):
                                                          standard_keys.index(KEY_ID.KEYBOARD_A) +
                                                          self.config.F_NumOnboardProfiles] + [KEY_ID.KEYBOARD_D]
        profile_switch_keys = ProfileManagementTestUtils.get_onboard_profiles_selection_keys(test_case=self)
        number_of_ways_to_select_onboard_profiles = 3
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Create a FKC base layer to remap ' + {trigger_keys} to 'Switch onboard profile X' and "
                           "'Cycle thru onboard profile'")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = []
        for index in range(self.config.F_NumOnboardProfiles):
            remapped_key_settings.append(RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                                                     trigger_key=trigger_keys[index],
                                                     action_key=KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE,
                                                     profile_number=index + 1))
        # end for
        remapped_key_settings.append(RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                                                 trigger_key=trigger_keys[-1],
                                                 action_key=KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE))
        main_tables = self.create_main_tables_and_save_in_nvs(
            test_case=self, directory=directory, preset_remapped_keys=remapped_key_settings, save_in_nvs=False)

        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over range({self.config.F_NumOnboardProfiles} "
                                 f"* {number_of_ways_to_select_onboard_profiles})")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(self.config.F_NumOnboardProfiles * number_of_ways_to_select_onboard_profiles):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(
                test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
                file_id=ProfileManagement.Partition.FileId.RAM,
                count=main_tables[FkcMainTable.Layer.BASE].n_bytes,
                crc_32=main_tables[FkcMainTable.Layer.BASE].crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
                test_case=self,
                set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
                fkc_enabled=FullKeyCustomization.FKCStatus.ENABLE,
                set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
                toggle_keys_enabled=FullKeyCustomization.ToggleKeyStatus.DISABLE)
            # Wait all key release events
            sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            if index < self.config.F_NumOnboardProfiles:
                if len(profile_switch_keys) > 0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Emulate a key combination on the FN + {profile_switch_keys[index]!s}')
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
                    sleep(0.05)
                    self.button_stimuli_emulator.keystroke(key_id=profile_switch_keys[index], delay=1)
                    self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
                else:
                    continue
                # end if
            elif index in range(self.config.F_NumOnboardProfiles, self.config.F_NumOnboardProfiles * 2):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Emulate a keystroke on the '
                                         f'{trigger_keys[index % self.config.F_NumOnboardProfiles]!s}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(
                    key_id=trigger_keys[index % self.config.F_NumOnboardProfiles], delay=1)
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keystroke on the {trigger_keys[-1]!s}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=trigger_keys[-1], delay=1)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait profileChangeEvent and check the profile_change_result is failure.")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            profile_change_result_checker = ProfileManagementTestUtils.ProfileChangeResultResponseChecker
            profile_change_result_check_map = profile_change_result_checker.get_default_check_map(self)
            profile_change_result_check_map.update({'failure': (
                profile_change_result_checker.check_failure, ProfileManagement.ProfileChangeResult.Result.FAILURE)})
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({'new_profile': (checker.check_new_profile,
                                              ProfileManagement.SpecialFileId.FILE_ID_START),
                              'profile_change_result': (checker.check_profile_change_result,
                                                        profile_change_result_check_map)})
            checker.check_fields(self, response, self.feature_8101.profile_change_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getError request")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is "
                                      f"{ProfileManagement.FileSystemErrorCode.MISSING_ONBOARD_PROFILE}")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.GetErrorResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "fs_error_code": (checker.check_fs_error_code,
                                  ProfileManagement.FileSystemErrorCode.MISSING_ONBOARD_PROFILE),
                "fs_error_param_1": (checker.check_fs_error_param_1,
                                     (index % self.config.F_NumOnboardProfiles) + 1 if
                                     index < number_of_ways_to_select_onboard_profiles * 2 else
                                     ProfileManagement.SpecialFileId.FILE_ID_START),
                "fs_error_param_2": (checker.check_fs_error_param_2,
                                     ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
            })
            checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8101_0027", _AUTHOR)
    # end def test_switch_to_a_missing_onboard_profiles

    @features("Feature8101")
    @features("Feature1B05")
    @level("ErrorHandling")
    def test_configure_macro_file(self):
        """
        Validate the FW returns an error "INVALID_ARGUMENT" (0x02) when the user is attempting to configure a macro file
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform keystrokes on all of mouse keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries_in_key_id = []
        for key_id in list(ProfileButton.KEY_ID_TO_MOUSE_BUTTON_MASK.keys()):
            macro_entries_in_key_id.append(MouseButtonCommand(key_id=key_id, action=KeyAction.PRESS))
            macro_entries_in_key_id.append(MouseButtonCommand(key_id=key_id, action=KeyAction.RELEASE))
        # end for
        macro_entries_in_key_id = [PresetMacroEntry(commands=macro_entries_in_key_id + [MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries_in_key_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={macro.file_id_lsb}, feature_id=0x1b05")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.configure_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            feature_id=FullKeyCustomization.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B05.MACRO_DEFINITION_FILE,
            file_id=macro.file_id_lsb,
            count=directory.files[macro.file_id_lsb].n_bytes,
            hash_key=directory.files[macro.file_id_lsb].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_8101_0028", _AUTHOR)
    # end def test_configure_macro_file
# end class ProfileManagementErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
