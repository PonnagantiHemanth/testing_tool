#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8101.robustness
:brief: HID++ 2.0 ``ProfileManagement`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.gaming.profilemanagement import ReadBufferResponse
from pyhid.hidpp.features.gaming.profilemanagement import WriteBuffer
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.mcu.profileformat import MacroEndCommand
from pylibrary.mcu.profileformat import PresetMacroEntry
from pylibrary.mcu.profileformat import StandardKeyCommand
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
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
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class ProfileManagementRobustnessTestCase(ProfileManagementTestCase):
    """
    Validate ``ProfileManagement`` robustness test cases
    """

    @features("Feature8101")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> fileSystemVer, profileTagVer, maxSectorSize, ramBufferSize, maxSectorId,
        maxFileId, maxDirectorySectorId, totalFlashSizeKb, flashEraseCounter, flashLifeExpect, numOnboardProfiles,
        editBufferCapabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_8101.get_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_get_profile_tag_list_software_id(self):
        """
        Validate ``GetProfileTagList`` software id field is ignored by the firmware

        [1] getProfileTagList(offsetBytes) -> partialTagList

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.OffsetBytes.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetProfileTagList request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_profile_tag_list(
                test_case=self,
                offset_bytes=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetProfileTagListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetProfileTagListResponseChecker.check_fields(
                self, response, self.feature_8101.get_profile_tag_list_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#2", _AUTHOR)
    # end def test_get_profile_tag_list_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_start_write_buffer_software_id(self):
        """
        Validate ``StartWriteBuffer`` software id field is ignored by the firmware

        [2] startWriteBuffer(count) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Count.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartWriteBuffer request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
                test_case=self,
                count=1,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StartWriteBufferResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.start_write_buffer_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#3", _AUTHOR)
    # end def test_start_write_buffer_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_write_buffer_software_id(self):
        """
        Validate ``WriteBuffer`` software id field is ignored by the firmware

        [3] writeBuffer(data) -> frameNum

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Data

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        sw_ids = compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=len(sw_ids) * (WriteBuffer.LEN.DATA // 8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for index, software_id in enumerate(sw_ids):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteBuffer request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.write_buffer(
                test_case=self,
                data=RandHexList(16),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check WriteBufferResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.WriteBufferResponseChecker
            check_map = checker.get_check_map(frame_num=index+1)
            checker.check_fields(self, response, self.feature_8101.write_buffer_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#4", _AUTHOR)
    # end def test_write_buffer_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_get_error_software_id(self):
        """
        Validate ``GetError`` software id field is ignored by the firmware

        [4] getError() -> fsErrorCode, fsErrorParam1, fsErrorParam2

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetError request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_error(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetErrorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetErrorResponseChecker.check_fields(
                self, response, self.feature_8101.get_error_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#5", _AUTHOR)
    # end def test_get_error_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_edit_buffer_software_id(self):
        """
        Validate ``EditBuffer`` software id field is ignored by the firmware

        [5] editBuffer(editBufferOperation, address, data) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.EditBufferOperation.Address.Data

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Load request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self,
            first_sector_id=ProfileManagement.Partition.SectorId.OOB,
            count=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send EditBuffer request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.edit_buffer(
                test_case=self,
                count=0,
                opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE,
                address=0,
                data=RandHexList(13),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check EditBufferResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.edit_buffer_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#6", _AUTHOR)
    # end def test_edit_buffer_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_get_set_mode_software_id(self):
        """
        Validate ``GetSetMode`` software id field is ignored by the firmware

        [6] getSetMode(operatingMode) -> operatingModeResponse, currProfileFileId

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.OperatingMode.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSetMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_set_mode(
                test_case=self,
                onboard_mode=ProfileManagement.Mode.ONBOARD_MODE,
                set_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSetModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetSetModeResponseChecker.check_fields(
                self, response, self.feature_8101.get_set_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#7", _AUTHOR)
    # end def test_get_set_mode_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_save_software_id(self):
        """
        Validate ``Save`` software id field is ignored by the firmware

        [7] save(firstSectorId, count, hash32) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.FirstSectorId.Count.Hash32.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
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
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Save request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.save(
                test_case=self,
                first_sector_id=ProfileManagement.SpecialFileId.FILE_ID_START,
                count=len(data),
                hash32=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(data),
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SaveResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.save_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#8", _AUTHOR)
    # end def test_save_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_load_software_id(self):
        """
        Validate ``Load`` software id field is ignored by the firmware

        [8] load(firstSectorId, count) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.FirstSectorId.Count.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Load request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.load(
                test_case=self,
                first_sector_id=ProfileManagement.Partition.SectorId.OOB,
                count=0xFFFF,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check LoadResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.load_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#9", _AUTHOR)
    # end def test_load_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_configure_software_id(self):
        """
        Validate ``Configure`` software id field is ignored by the firmware

        [9] configure(featureId, configureAction, count, hash) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.FeatureId.ConfigureAction.FileId.Count.Hash.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        _, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Configure request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.configure(
                test_case=self,
                feature_id=ProfileManagement.FEATURE_ID,
                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                file_id=profile.file_id_lsb,
                count=len(HexList(profile)),
                hash_key=profile.crc_32,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ConfigureResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.configure_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#10", _AUTHOR)
    # end def test_configure_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_get_set_power_on_params_software_id(self):
        """
        Validate ``GetSetPowerOnParams`` software id field is ignored by the firmware

        [10] getSetPowerOnParams(powerOnProfileAction, powerOnProfile) -> powerOnProfile

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PowerOnProfileAction.PowerOnProfile

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSetPowerOnParams request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_set_power_on_params(
                test_case=self,
                set_power_on_profile=ProfileManagementTestUtils.RequestType.GET,
                power_on_profile=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSetPowerOnParamsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetSetPowerOnParamsResponseChecker.check_fields(
                self, response, self.feature_8101.get_set_power_on_params_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#11", _AUTHOR)
    # end def test_get_set_power_on_params_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_get_hashes_software_id(self):
        """
        Validate ``GetHashes`` software id field is ignored by the firmware

        [11] getHashes(getHashAction, fileId0, fileId1, fileId2, fileId3) -> hash0, hash1, hash2, hash3

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.GetHashAction.FileId0.FileId1.FileId2.FileId3.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetHashes request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_hashes(
                test_case=self,
                compute=0,
                file_id_0=0,
                file_id_1=0,
                file_id_2=0,
                file_id_3=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetHashesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetHashesResponseChecker.check_fields(
                self, response, self.feature_8101.get_hashes_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#12", _AUTHOR)
    # end def test_get_hashes_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_read_buffer_software_id(self):
        """
        Validate ``ReadBuffer`` software id field is ignored by the firmware

        [12] readBuffer(offsetBytes) -> data

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.OffsetBytes.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
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
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ProfileManagement.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadBuffer request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.read_buffer(
                test_case=self,
                offset_bytes=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadBufferResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.ReadBufferResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "data": (checker.check_data, data)
            })
            checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0001#13", _AUTHOR)
    # end def test_read_buffer_software_id

    @features("Feature8101")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [0] getCapabilities() -> fileSystemVer, profileTagVer, maxSectorSize, ramBufferSize, maxSectorId,
        maxFileId, maxDirectorySectorId, totalFlashSizeKb, flashEraseCounter, flashLifeExpect, numOnboardProfiles,
        editBufferCapabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_8101.get_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#1", _AUTHOR)
    # end def test_get_capabilities_padding

    @features("Feature8101")
    @level("Robustness")
    def test_get_profile_tag_list_padding(self):
        """
        Validate ``GetProfileTagList`` padding bytes are ignored by the firmware

        [1] getProfileTagList(offsetBytes) -> partialTagList

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.OffsetBytes.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.get_profile_tag_list_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetProfileTagList request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_profile_tag_list(
                test_case=self,
                offset_bytes=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetProfileTagListResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetProfileTagListResponseChecker.check_fields(
                self, response, self.feature_8101.get_profile_tag_list_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#2", _AUTHOR)
    # end def test_get_profile_tag_list_padding

    @features("Feature8101")
    @level("Robustness")
    def test_start_write_buffer_padding(self):
        """
        Validate ``StartWriteBuffer`` padding bytes are ignored by the firmware

        [2] startWriteBuffer(count) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.Count.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.start_write_buffer_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send StartWriteBuffer request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
                test_case=self,
                count=1,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check StartWriteBufferResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.start_write_buffer_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#3", _AUTHOR)
    # end def test_start_write_buffer_padding

    @features("Feature8101")
    @level("Robustness")
    def test_get_error_padding(self):
        """
        Validate ``GetError`` padding bytes are ignored by the firmware

        [4] getError() -> fsErrorCode, fsErrorParam1, fsErrorParam2

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.get_error_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetError request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_error(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetErrorResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetErrorResponseChecker.check_fields(
                self, response, self.feature_8101.get_error_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#4", _AUTHOR)
    # end def test_get_error_padding

    @features("Feature8101")
    @level("Robustness")
    def test_get_set_mode_padding(self):
        """
        Validate ``GetSetMode`` padding bytes are ignored by the firmware

        [6] getSetMode(operatingMode) -> operatingModeResponse, currProfileFileId

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.OperatingMode.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.get_set_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSetMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_set_mode(
                test_case=self,
                onboard_mode=ProfileManagement.Mode.ONBOARD_MODE,
                set_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSetModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetSetModeResponseChecker.check_fields(
                self, response, self.feature_8101.get_set_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#5", _AUTHOR)
    # end def test_get_set_mode_padding

    @features("Feature8101")
    @level("Robustness")
    def test_save_padding(self):
        """
        Validate ``Save`` padding bytes are ignored by the firmware

        [7] save(firstSectorId, count, hash32) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.FirstSectorId.Count.Hash32.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
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
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.save_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Save request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.save(
                test_case=self,
                first_sector_id=ProfileManagement.SpecialFileId.FILE_ID_START,
                count=len(data),
                hash32=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(data),
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SaveResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.save_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#6", _AUTHOR)
    # end def test_save_padding

    @features("Feature8101")
    @level("Robustness")
    def test_load_padding(self):
        """
        Validate ``Load`` padding bytes are ignored by the firmware

        [8] load(firstSectorId, count) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.FirstSectorId.Count.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.load_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Load request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.load(
                test_case=self,
                first_sector_id=ProfileManagement.Partition.SectorId.OOB,
                count=0xFFFF,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check LoadResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.load_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#7", _AUTHOR)
    # end def test_load_padding

    @features("Feature8101")
    @level("Robustness")
    def test_configure_padding(self):
        """
        Validate ``Configure`` padding bytes are ignored by the firmware

        [9] configure(featureId, configureAction, count, hash) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.FeatureId.ConfigureAction.FileId.Count.Hash.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        _, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.configure_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Configure request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.configure(
                test_case=self,
                feature_id=ProfileManagement.FEATURE_ID,
                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                file_id=profile.file_id_lsb,
                count=len(HexList(profile)),
                hash_key=profile.crc_32,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ConfigureResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.MessageChecker.check_fields(
                self, response, self.feature_8101.configure_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#8", _AUTHOR)
    # end def test_configure_padding

    @features("Feature8101")
    @level("Robustness")
    def test_get_hashes_padding(self):
        """
        Validate ``GetHashes`` padding bytes are ignored by the firmware

        [11] getHashes(getHashAction, fileId0, fileId1, fileId2, fileId3) -> hash0, hash1, hash2, hash3

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.GetHashAction.FileId0.FileId1.FileId2.FileId3.0xPP.
        0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.get_hashes_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetHashes request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_hashes(
                test_case=self,
                compute=0,
                file_id_0=0,
                file_id_1=0,
                file_id_2=0,
                file_id_3=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetHashesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.GetHashesResponseChecker.check_fields(
                self, response, self.feature_8101.get_hashes_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#9", _AUTHOR)
    # end def test_get_hashes_padding

    @features("Feature8101")
    @level("Robustness")
    def test_read_buffer_padding(self):
        """
        Validate ``ReadBuffer`` padding bytes are ignored by the firmware

        [12] readBuffer(offsetBytes) -> data

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.OffsetBytes.0xPP

        Padding (PP) boundary values [00..FF]
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
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8101.read_buffer_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadBuffer request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.read_buffer(
                test_case=self,
                offset_bytes=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadBufferResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.ReadBufferResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "data": (checker.check_data, data)
            })
            checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8101_0002#10", _AUTHOR)
    # end def test_read_buffer_padding

    @features("Feature8101")
    @level("Robustness")
    def test_save_file_with_max_file_id(self):
        """
        Validate the profiles saved in the NVS can reach the max_file_id
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over index in range({self.config.F_NumOnboardProfiles})")
        # --------------------------------------------------------------------------------------------------------------
        profiles = []
        for index in range(self.config.F_NumOnboardProfiles):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a new onboard profile")
            # ----------------------------------------------------------------------------------------------------------
            profiles.append(ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE))
            profiles[index].update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.PROFILE_IDENTIFIER: index})
        # end for
        possible_host_profile_num = [
            self.config.F_MaxFileId - self.config.F_NumOnboardProfiles,
            self.config.F_MaxSectorId - directory.id_manager.get_next_sector_id_lsb() + 1,
            ((((self.config.F_MaxDirectorySectorId + 1) * self.config.F_MaxSectorSize)
              - directory.HEADER_LENGTH - directory.EOF_LENGTH) // directory.FILE_LENGTH)
            - self.config.F_NumOnboardProfiles]
        possible_host_profile_num.sort()
        host_profiles_num = possible_host_profile_num[0]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over index in range({host_profiles_num})")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(host_profiles_num):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a new host profile")
            # ----------------------------------------------------------------------------------------------------------
            profiles.append(ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE))
            profiles[index].update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.PROFILE_IDENTIFIER: self.config.F_NumOnboardProfiles + index})
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over index in range({len(profiles)})")
        # --------------------------------------------------------------------------------------------------------------
        for index, profile in enumerate(profiles):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            if index == len(profiles) - 1:
                directory.files[profiles[index].file_id_lsb].file_id_lsb = HexList(self.config.F_MaxFileId)
                directory.crc_32 = directory.calculate_crc32(data=directory._get_hexlist_for_crc32_calculation())
            # end if
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send load request with first_sector_id={directory.first_sector_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(test_case=self,
                                                    first_sector_id=directory.first_sector_id_lsb,
                                                    count=len(HexList(directory)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ram_buffer_data = ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(
            self, len(HexList(directory)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the directory data is as expected")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range((len(ram_buffer_data) // (ReadBufferResponse.LEN.DATA // 8)) + 1):
            self.assertEqual(
                expected=HexList(directory)[offset * (ReadBufferResponse.LEN.DATA // 8):
                                            (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                obtained=ram_buffer_data[offset * (ReadBufferResponse.LEN.DATA // 8):
                                         (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                msg=f"The data parameter differs found at offset {offset * (ReadBufferResponse.LEN.DATA // 8)}, "
                    f"(expected:{HexList(directory)}, obtained:{ram_buffer_data})")
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send load request with first_sector_id={profiles[-1].first_sector_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(test_case=self,
                                                    first_sector_id=profiles[-1].first_sector_id_lsb,
                                                    count=directory.files[profiles[-1].file_id_lsb].n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ram_buffer_data = ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(
            self, count=directory.files[profiles[-1].file_id_lsb].n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the last profile's data is as expected")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range((len(ram_buffer_data) // (ReadBufferResponse.LEN.DATA // 8)) + 1):
            self.assertEqual(
                expected=HexList(profiles[-1])[offset * (ReadBufferResponse.LEN.DATA // 8):
                                              (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                obtained=ram_buffer_data[offset * (ReadBufferResponse.LEN.DATA // 8):
                                         (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                msg=f"The data parameter differs found at offset {offset * (ReadBufferResponse.LEN.DATA // 8)}, "
                    f"(expected:{HexList(directory)}, obtained:{ram_buffer_data})")
        # end for

        self.testCaseChecked("ROB_8101_0003", _AUTHOR)
    # end def test_save_file_with_max_file_id

    @features("Feature8101")
    @level("Robustness")
    def test_write_data_with_ram_buffer_size(self):
        """
        Validate the data written in the RAM can reach the ram_buffer_size
        """
        data = HexList()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send startWriteBuffer request with count=getCapabilities.ram_buffer_size")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(test_case=self,
                                                                  count=int(self.config.F_RamBufferSize))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: while writeBuffer.frame_num < (getCapabilities.ram_buffer_size/16)")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(int(self.config.F_RamBufferSize) // int(WriteBuffer.LEN.DATA / 8)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send writeBuffer request with data=[Macro.NoOperation]*16")
            # ----------------------------------------------------------------------------------------------------------
            data_to_write = RandHexList(int(WriteBuffer.LEN.DATA / 8))
            data += data_to_write
            response = ProfileManagementTestUtils.HIDppHelper.write_buffer(
                test_case=self, data=data_to_write)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait writeBuffer response and check the frame_num is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.WriteBufferResponseChecker
            check_map = checker.get_check_map(frame_num=index + 1)
            checker.check_fields(self, response, self.feature_8101.write_buffer_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ram_buffer_data = ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(
            self, int(self.config.F_RamBufferSize))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the directory data is as expected")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range((len(ram_buffer_data) // (ReadBufferResponse.LEN.DATA // 8)) + 1):
            self.assertEqual(
                expected=data[offset * (ReadBufferResponse.LEN.DATA // 8):
                              (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                obtained=ram_buffer_data[offset * (ReadBufferResponse.LEN.DATA // 8):
                                         (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                msg=f"The data parameter differs found at offset {offset * (ReadBufferResponse.LEN.DATA // 8)}, "
                    f"(expected:{data}, obtained:{ram_buffer_data})")
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Save request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.save(
            test_case=self,
            first_sector_id=int(self.config.F_MaxDirectorySectorId),
            count=len(data),
            hash32=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SaveResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        }
        checker.check_fields(self, response, self.feature_8101.save_response_cls, check_map)

        self.testCaseChecked("ROB_8101_0004", _AUTHOR)
    # end def test_write_data_with_ram_buffer_size

    # noinspection PyTypeChecker
    @features("Feature8101")
    @level("Robustness")
    def test_write_data_to_exceed_the_total_flash_size(self):
        """
        Validate the data written in the NVS can exceed the total_flash_size
        (This test is designed for testing the bank switching mechanism, when the data written in the NVS exceed the
        total_flash_size, FW should handle it as expected.)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over index in range({self.config.F_NumOnboardProfiles})")
        # --------------------------------------------------------------------------------------------------------------
        profiles = []
        for index in range(self.config.F_NumOnboardProfiles):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a new onboard profile")
            # ----------------------------------------------------------------------------------------------------------
            profiles.append(ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE))
            profiles[index].update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.PROFILE_IDENTIFIER: index})
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profiles[index]),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profiles[index].first_sector_id_lsb,
                                             crc_32=profiles[index].crc_32)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform keystrokes on all of standard keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries_in_key_id = [PresetMacroEntry(
            commands=[StandardKeyCommand(key_id=key_id) for key_id in list(STANDARD_KEYS.keys())] * 2 +
                     [MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries_in_key_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap a key to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings,
                                                              macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profiles[0].update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profiles[0]),
                                         store_in_nvs=True, first_sector_id_lsb=profiles[0].first_sector_id_lsb,
                                         crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self,
            f"Test Loop: Loop over index in range({((self.config.F_TotalFlashSizeKb * 1024) // macro.n_bytes) + 1})")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(((self.config.F_TotalFlashSizeKb * 1024) // macro.n_bytes) + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x1B05 macro file to NVS\n{macro}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(macro),
                                             store_in_nvs=True, first_sector_id_lsb=macro.first_sector_id_lsb,
                                             crc_32=macro.crc_32)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Send configure request with file_id={profiles[0].file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profiles[0].file_id_lsb,
                                            count=directory.files[profiles[0].file_id_lsb].n_bytes,
                                            crc_32=directory.files[profiles[0].file_id_lsb].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                  fkc_enabled=1, set_toggle_keys_enabled=0)
        remapped_keys = FullKeyCustomizationTestUtils.FkcTableHelper.convert_to_remapped_keys(
            test_case=self, fkc_main_tables=main_tables, macro=macro, os_variant=OS.WINDOWS)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a keystroke on the remapping key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=self.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the received HID keyboard input and check the button flags.")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send load request with first_sector_id={macro.first_sector_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(test_case=self,
                                                    first_sector_id=macro.first_sector_id_lsb,
                                                    count=macro.n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ram_buffer_data = ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(self, macro.n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the directory data is as expected")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range((len(ram_buffer_data) // (ReadBufferResponse.LEN.DATA // 8)) + 1):
            self.assertEqual(
                expected=HexList(macro)[offset * (ReadBufferResponse.LEN.DATA // 8):
                                        (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                obtained=ram_buffer_data[offset * (ReadBufferResponse.LEN.DATA // 8):
                                         (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                msg=f"The data parameter differs found at offset {offset * (ReadBufferResponse.LEN.DATA // 8)}, "
                    f"(expected:{HexList(directory)}, obtained:{ram_buffer_data})")
        # end for

        self.testCaseChecked("ROB_8101_0005", _AUTHOR)
    # end def test_write_data_to_exceed_the_total_flash_size

    @features("Feature8101")
    @level("Robustness")
    def test_create_onboard_profiles_less_than_device_supported(self):
        """
        Validate the user can create onboard profiles with numbers less than the device supported.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create valid 0x8101 feature setting file")
        # --------------------------------------------------------------------------------------------------------------
        profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(self, directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Check FW doesn't return an error when writing a 0x8101 directory to NVS with onboard profile "
                  "number less than device supported")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        self.testCaseChecked("ROB_8101_0006", _AUTHOR)
    # end def test_create_onboard_profiles_less_than_device_supported
# end class ProfileManagementRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
