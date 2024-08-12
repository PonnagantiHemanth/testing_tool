#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8101.interface
:brief: HID++ 2.0 ``ProfileManagement`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hidpp20.gaming.feature_8101.profilemanagement import ProfileManagementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class ProfileManagementInterfaceTestCase(ProfileManagementTestCase):
    """
    Validate ``ProfileManagement`` interface test cases
    """

    @features("Feature8101")
    @level("Interface")
    def test_get_capabilities_api(self):
        """
        Validate ``GetCapabilities`` normal processing

        [0] getCapabilities() -> fileSystemVer, profileTagVer, maxSectorSize, ramBufferSize, maxSectorId,
        maxFileId, maxDirectorySectorId, totalFlashSizeKb, flashEraseCounter, flashLifeExpect, numOnboardProfiles,
        editBufferCapabilities
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        })
        checker.check_fields(self, response, self.feature_8101.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_8101_0001", _AUTHOR)
    # end def test_get_capabilities_api

    @features("Feature8101")
    @level("Interface")
    def test_get_profile_tag_list_api(self):
        """
        Validate ``GetProfileTagList`` normal processing

        [1] getProfileTagList(offsetBytes) -> partialTagList
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetProfileTagList request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_profile_tag_list(
            test_case=self,
            offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetProfileTagListResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetProfileTagListResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        })
        checker.check_fields(self, response, self.feature_8101.get_profile_tag_list_response_cls, check_map)

        self.testCaseChecked("INT_8101_0002", _AUTHOR)
    # end def test_get_profile_tag_list_api

    @features("Feature8101")
    @level("Interface")
    def test_start_write_buffer_api(self):
        """
        Validate ``StartWriteBuffer`` normal processing

        [2] startWriteBuffer(count) -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check StartWriteBufferResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        }
        checker.check_fields(self, response, self.feature_8101.start_write_buffer_response_cls, check_map)

        self.testCaseChecked("INT_8101_0003", _AUTHOR)
    # end def test_start_write_buffer_api

    @features("Feature8101")
    @level("Interface")
    def test_write_buffer_api(self):
        """
        Validate ``WriteBuffer`` normal processing

        [3] writeBuffer(data) -> frameNum
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=RandHexList(16))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WriteBufferResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.WriteBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        })
        checker.check_fields(self, response, self.feature_8101.write_buffer_response_cls, check_map)

        self.testCaseChecked("INT_8101_0004", _AUTHOR)
    # end def test_write_buffer_api

    @features("Feature8101")
    @level("Interface")
    def test_get_error_api(self):
        """
        Validate ``GetError`` normal processing

        [4] getError() -> fsErrorCode, fsErrorParam1, fsErrorParam2
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetErrorResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("INT_8101_0005", _AUTHOR)
    # end def test_get_error_api

    @features("Feature8101")
    @level("Interface")
    def test_edit_buffer_api(self):
        """
        Validate ``EditBuffer`` normal processing

        [5] editBuffer(editBufferOperation, address, data) -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Load request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self,
            first_sector_id=ProfileManagement.Partition.SectorId.OOB,
            count=0xFFFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send EditBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self,
            count=0,
            opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE,
            address=0,
            data=RandHexList(13))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check EditBufferResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        }
        checker.check_fields(self, response, self.feature_8101.edit_buffer_response_cls, check_map)

        self.testCaseChecked("INT_8101_0006", _AUTHOR)
    # end def test_edit_buffer_api

    @features("Feature8101")
    @level("Interface")
    def test_get_set_mode_api(self):
        """
        Validate ``GetSetMode`` normal processing

        [6] getSetMode(operatingMode) -> operatingModeResponse, currProfileFileId
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSetMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_set_mode(
            test_case=self,
            onboard_mode=ProfileManagement.Mode.ONBOARD_MODE,
            set_onboard_mode=ProfileManagementTestUtils.RequestType.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSetModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetSetModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        })
        checker.check_fields(self, response, self.feature_8101.get_set_mode_response_cls, check_map)

        self.testCaseChecked("INT_8101_0007", _AUTHOR)
    # end def test_get_set_mode_api

    @features("Feature8101")
    @level("Interface")
    def test_save_api(self):
        """
        Validate ``Save`` normal processing

        [7] save(firstSectorId, count, hash32) -> None
        """
        self.post_requisite_reload_nvs = True
        data = RandHexList(16)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Save request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.save(
            test_case=self,
            first_sector_id=ProfileManagement.SpecialFileId.FILE_ID_START,
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

        self.testCaseChecked("INT_8101_0008", _AUTHOR)
    # end def test_save_api

    @features("Feature8101")
    @level("Interface")
    def test_load_api(self):
        """
        Validate ``Load`` normal processing

        [8] load(firstSectorId, count) -> None
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Load request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self,
            first_sector_id=ProfileManagement.Partition.SectorId.OOB,
            count=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check LoadResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        }
        checker.check_fields(self, response, self.feature_8101.load_response_cls, check_map)

        self.testCaseChecked("INT_8101_0009", _AUTHOR)
    # end def test_load_api

    @features("Feature8101")
    @level("Interface")
    def test_get_set_power_on_params_api(self):
        """
        Validate ``GetSetPowerOnParams`` normal processing

        [10] getSetPowerOnParams(powerOnProfileAction, powerOnProfile) -> powerOnProfile
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSetPowerOnParams request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self,
            set_power_on_profile=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSetPowerOnParamsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetSetPowerOnParamsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        })
        checker.check_fields(self, response, self.feature_8101.get_set_power_on_params_response_cls, check_map)

        self.testCaseChecked("INT_8101_0010", _AUTHOR)
    # end def test_get_set_power_on_params_api

    @features("Feature8101")
    @level("Interface")
    def test_get_hashes_api(self):
        """
        Validate ``GetHashes`` normal processing

        [11] getHashes(getHashAction, fileId0, fileId1, fileId2, fileId3) -> hash0, hash1, hash2, hash3
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHashes request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_hashes(
            test_case=self,
            compute=0,
            file_id_0=0,
            file_id_1=0,
            file_id_2=0,
            file_id_3=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetHashesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetHashesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index))
        })
        checker.check_fields(self, response, self.feature_8101.get_hashes_response_cls, check_map)

        self.testCaseChecked("INT_8101_0011", _AUTHOR)
    # end def test_get_hashes_api

    @features("Feature8101")
    @level("Interface")
    def test_read_buffer_api(self):
        """
        Validate ``ReadBuffer`` normal processing

        [12] readBuffer(offsetBytes) -> data
        """
        data = RandHexList(16)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send StartWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(
            test_case=self,
            count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(
            test_case=self,
            data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(
            test_case=self,
            offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ReadBufferResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(test_case=self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_8101_index)),
            "data": (checker.check_data, data)
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        self.testCaseChecked("INT_8101_0012", _AUTHOR)
    # end def test_read_buffer_api
# end class ProfileManagementInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
