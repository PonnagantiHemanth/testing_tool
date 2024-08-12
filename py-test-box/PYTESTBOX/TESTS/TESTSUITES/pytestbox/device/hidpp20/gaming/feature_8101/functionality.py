#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8101.functionality
:brief: HID++ 2.0 ``ProfileManagement`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import os
from os.path import join
from time import sleep

# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuStatusEvent
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.gaming.profilemanagement import EditBuffer
from pyhid.hidpp.features.gaming.profilemanagement import GetProfileTagListResponse
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.gaming.profilemanagement import ReadBufferResponse
from pyhid.hidpp.features.gaming.profilemanagement import WriteBuffer
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.mcu.profileformat import MacroEndCommand
from pylibrary.mcu.profileformat import PresetMacroEntry
from pylibrary.mcu.profileformat import StandardKeyCommand
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hidpp20.gaming.feature_8101.profilemanagement import ProfileManagementTestCase
from pytestbox.shared.base.dfuutils import DfuTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProfileManagementFunctionalityTestCase(ProfileManagementTestCase):
    """
    Validate ``ProfileManagement`` functionality test cases
    """

    @features("Feature8101")
    @level("Functionality")
    def test_set_onboard_mode_and_host_mode(self):
        """
        Validate the device's mode can be switched to onboard mode and host mode
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send getSetMode request and check the response")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.SET,
            onboard_mode=ProfileManagement.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send getSetMode request and check the response")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.SET,
            onboard_mode=ProfileManagement.Mode.ONBOARD_MODE)

        self.testCaseChecked("FUN_8101_0001", _AUTHOR)
    # end def test_set_onboard_mode_and_host_mode

    @features("Feature8101")
    @level("Functionality")
    @services("HardwareReset")
    def test_reset_device_onboard_mode_after_power_cycle(self):
        """
        Validate the device's mode will be reset to onboard mode after power reset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send getSetMode request and check the response")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.SET,
            onboard_mode=ProfileManagement.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request and check onboard_mode is {ProfileManagement.Mode.ONBOARD_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(test_case=self, onboard_mode=ProfileManagement.Mode.ONBOARD_MODE)

        self.testCaseChecked("FUN_8101_0002", _AUTHOR)
    # end def test_reset_device_onboard_mode_after_power_cycle

    @features("Feature8101")
    @features('Feature1830powerMode', 3)
    @level("Functionality")
    def test_reset_device_onboard_mode_after_depp_sleep(self):
        """
        Validate the device's mode will be reset to onboard mode after waking up from the deep-sleep
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send getSetMode request and check the response")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.SET,
            onboard_mode=ProfileManagement.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake-up the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request and check onboard_mode is {ProfileManagement.Mode.ONBOARD_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(test_case=self, onboard_mode=ProfileManagement.Mode.ONBOARD_MODE)

        self.testCaseChecked("FUN_8101_0003", _AUTHOR)
    # end def test_reset_device_onboard_mode_after_depp_sleep

    @features("Feature8101")
    @level("Functionality")
    def test_set_onboard_profile_as_power_on_profile_on_onboard_mode(self):
        """
        Validate a valid onboard profile can be set as power-on profile thru getSetPowerOnParams on onboard mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        _, profiles = ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
            test_case=self, save_profile_in_nvs=True, save_directory_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to set power on profile to {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=profile.file_id_lsb)

        self.testCaseChecked("FUN_8101_0004", _AUTHOR)
    # end def test_set_onboard_profile_as_power_on_profile_on_onboard_mode

    @features("Feature8101")
    @level("Functionality")
    def test_set_onboard_profile_as_power_on_profile_on_host_mode(self):
        """
        Validate a valid onboard profile can be set as power-on profile thru getSetPowerOnParams on host mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        _, profiles = ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
            test_case=self, save_profile_in_nvs=True, save_directory_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSetMode request with set_onboard_mode=1, "
                                 f"onboard_mode={ProfileManagement.Mode.HOST_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.get_set_mode(
            test_case=self,
            onboard_mode=ProfileManagement.Mode.HOST_MODE,
            set_onboard_mode=ProfileManagementTestUtils.RequestType.SET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to set the power on profile to {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=profile.file_id_lsb)

        self.testCaseChecked("FUN_8101_0005", _AUTHOR)
    # end def test_set_onboard_profile_as_power_on_profile_on_host_mode

    @features("Feature8101")
    @level("Functionality")
    @services("HardwareReset")
    def test_set_host_profile_as_power_on_profile(self):
        """
        Validate a valid host mode profile can be set as power-on profile thru getSetPowerOnParams on both
        onboard mode and host mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, onboard_profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a host profile")
        # --------------------------------------------------------------------------------------------------------------
        host_profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
            self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write the host profile to NVS\n{host_profile}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(host_profile),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=host_profile.first_sector_id_lsb,
                                         crc_32=host_profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Update the directory and save in the NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to set the power on profile to {host_profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=host_profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {host_profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=host_profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {host_profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=host_profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Check the current profile matches the settings of power on profile")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            expected_curr_profile_file_id=host_profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Set onboard mode to Host Mode and check all fields as expected from the response")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.SET,
            onboard_mode=ProfileManagement.Mode.HOST_MODE,
            expected_curr_profile_file_id=host_profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to set the power on profile to {host_profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=host_profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {host_profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=host_profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {host_profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=host_profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Check the current profile matches the settings of power on profile")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            expected_curr_profile_file_id=host_profile.file_id_lsb)

        self.testCaseChecked("FUN_8101_0006", _AUTHOR)
    # end def test_set_host_profile_as_power_on_profile

    @features("Feature8101")
    @level("Functionality")
    def test_set_profile_saved_in_ram_as_power_on_profile(self):
        """
        Validate a valid profile saved in the RAM can not be set as power-on profile thru getSetPowerOnParams
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load request to load the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(test_case=self,
                                                    first_sector_id=profile.first_sector_id_lsb,
                                                    count=directory.files[profile.file_id_lsb].n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSetPowerOnParams request with set_power_on_profile=1,"
                                 f"power_on_profile={ProfileManagement.Partition.FileId.RAM}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.get_set_power_on_params_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            set_power_on_profile=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=ProfileManagement.Partition.FileId.RAM)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Send getSetPowerOnParams request to check the power on profile is "
                  f"{ProfileManagement.Partition.FileId.OOB | 0x0001}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=ProfileManagement.Partition.FileId.OOB | 0x0001)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Send getSetPowerOnParams request to check the power on profile is "
                  f"{ProfileManagement.Partition.FileId.OOB | 0x0001}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=ProfileManagement.Partition.FileId.OOB | 0x0001)

        self.testCaseChecked("FUN_8101_0007", _AUTHOR)
    # end def test_set_profile_saved_in_ram_as_power_on_profile

    @features("Feature8101")
    @level("Functionality")
    def test_retrieve_whole_profile_tag_list(self):
        """
        Validate the whole profile tag list can be retrieved thru getProfileTagList
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: while partial_tag_list[0] is not EOF")
        # --------------------------------------------------------------------------------------------------------------
        for iteration in range((ProfileManagementTestUtils.get_len_of_tag_list_from_settings(test_case=self) //
                                int(GetProfileTagListResponse.LEN.PARTIAL_TAG_LIST/8)) + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getProfileTagList request with {offset_byte}")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_profile_tag_list(
                test_case=self, offset_bytes=iteration * int(GetProfileTagListResponse.LEN.PARTIAL_TAG_LIST/8))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getProfileTagList response and check the content of partial_tag_list is"
                                      "as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.GetProfileTagListResponseChecker
            check_map = checker.get_check_map(
                test_case=self, offset_bytes=iteration * int(GetProfileTagListResponse.LEN.PARTIAL_TAG_LIST/8))
            checker.check_fields(self, response, self.feature_8101.get_profile_tag_list_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8101_0008", _AUTHOR)
    # end def test_retrieve_whole_profile_tag_list

    @features("Feature8101")
    @level("Functionality")
    @services("HardwareReset")
    def test_data_in_ram_is_rest_after_power_cycle(self):
        """
        Validate the profile wrote in RAM buffer will be reset after power cycle
        """
        data = RandHexList(WriteBuffer.LEN.DATA // 8)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send startWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(test_case=self, count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send writeBuffer request with data={data}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(test_case=self, data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=self, offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the data is as expected")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data)
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.read_buffer_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there is no data can be read from buffer and the device return the "
                                  "INVALID_ARGUMENT(0x02) error")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("FUN_8101_0009", _AUTHOR)
    # end def test_data_in_ram_is_rest_after_power_cycle

    @features("Feature8101")
    @features('Feature1830powerMode', 3)
    @level("Functionality")
    def test_data_in_ram_is_rest_after_deep_sleep(self):
        """
        Validate the profile wrote in RAM buffer will be reset after waking-up from deep sleep
        """
        data = RandHexList(WriteBuffer.LEN.DATA // 8)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send startWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(test_case=self, count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send writeBuffer request with data={data}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(test_case=self, data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=self, offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the data is as expected")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data)
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake-up the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.read_buffer_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the data is reset")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("FUN_8101_0010", _AUTHOR)
    # end def test_data_in_ram_is_rest_after_deep_sleep

    @features("Feature8101")
    @level("Functionality")
    def test_active_profile_saved_in_ram(self):
        """
        Validate the profile wrote in RAM buffer can be configured as the active profile

        NB: The main FKC file could be: Remap 'A' to execute macro, the macro file could be: 'z' + 'y' + 'x'
        keystrokes
        """
        trigger_key = KEY_ID.BUTTON_1 if self.f.PRODUCT.F_IsMice else KEY_ID.KEYBOARD_A
        macro_keys = [KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_X]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro file and save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries = [PresetMacroEntry(commands=[StandardKeyCommand(key_id=macro_keys[0]),
                                                    StandardKeyCommand(key_id=macro_keys[1]),
                                                    StandardKeyCommand(key_id=macro_keys[2]),
                                                    MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Create a FKC base layer table file and remap {trigger_key!s} to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                              main_tables[FkcMainTable.Layer.BASE].file_id_lsb})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteBuffer request to the user profile in the RAM")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=False,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.RAM,
                                            count=len(HexList(profile)),
                                            crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check curr_profile_file_id is {ProfileManagement.Partition.FileId.RAM}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            expected_curr_profile_file_id=ProfileManagement.Partition.FileId.RAM)

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
        LogHelper.log_step(self, "Perform a keystroke on the trigger key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the HID keyboard reports are received")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        self.testCaseChecked("FUN_8101_0011", _AUTHOR)
    # end def test_active_profile_saved_in_ram

    @features("Feature8101")
    @level("Functionality")
    def test_edit_profile_in_ram(self):
        """
        Validate the profile wrote in RAM buffer can be edited thru editBuffer
        """
        data = RandHexList(WriteBuffer.LEN.DATA // 8)
        data_to_overwrite = RandHexList(EditBuffer.LEN.DATA // 8)
        data_to_insert = RandHexList(EditBuffer.LEN.DATA // 8)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send startWriteBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.start_write_buffer(test_case=self, count=len(data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send writeBuffer with the data={data}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.write_buffer(test_case=self, data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send editBuffer request with "
                                 f"opcode={ProfileManagement.EditBufferOperation.Opcode.OVERWRITE}, "
                                 f"data={data_to_overwrite}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=len(data_to_overwrite), opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE,
            address=0, data=data_to_overwrite)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=self, offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait readBuffer response and check data is match {data_to_overwrite}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_to_overwrite + data[len(data_to_overwrite) - len(data):])
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send editBuffer request with "
                                 f"opcode={ProfileManagement.EditBufferOperation.Opcode.INSERT}, "
                                 f"data={data}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=len(data_to_insert),
            opcode=ProfileManagement.EditBufferOperation.Opcode.INSERT,
            address=0, data=data_to_insert)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=self, offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check data is "
                                  f"{data_to_overwrite[:(WriteBuffer.LEN.DATA // 8) - len(data_to_insert)]}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_to_insert + data_to_overwrite[
                                                          :(WriteBuffer.LEN.DATA // 8) - len(data_to_insert)])
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send editBuffer request with "
                                 f"opcode={ProfileManagement.EditBufferOperation.Opcode.DELETE}, "
                                 f"address=0, count={len(data)}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=len(data_to_insert),
            opcode=ProfileManagement.EditBufferOperation.Opcode.DELETE,
            address=0, data=data_to_insert)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=self, offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait readBuffer response and check data is match {data_to_overwrite}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_to_overwrite + data[len(data_to_overwrite) - len(data):])
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        self.testCaseChecked("FUN_8101_0012", _AUTHOR)
    # end def test_edit_profile_in_ram

    @features("Feature8101")
    @level("Functionality")
    def test_edit_oob_profile_in_ram(self):
        """
        Validate the OOB profile can be loaded to RAM buffer and edited
        """
        data_to_overwrite = RandHexList(EditBuffer.LEN.DATA // 8)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send load request with first_sector_id={ProfileManagement.Partition.SectorId.OOB | 0x0001}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(test_case=self,
                                                    first_sector_id=ProfileManagement.Partition.SectorId.OOB | 0x0001,
                                                    count=self.config.F_RamBufferSize)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send editBuffer request with "
                                 f"opcode={ProfileManagement.EditBufferOperation.Opcode.OVERWRITE}, "
                                 f"address={0}, data={data_to_overwrite}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=len(data_to_overwrite), opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE,
            address=0, data=data_to_overwrite)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=self, offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check profile_name in the user profile has been"
                                  f"changed to {data_to_overwrite}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_to_overwrite +
                     HexList(ProfileManagementTestUtils.ProfileHelper.get_oob_profile(self))[
                        len(data_to_overwrite):ReadBufferResponse.LEN.DATA // 8])
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        self.testCaseChecked("FUN_8101_0013", _AUTHOR)
    # end def test_edit_oob_profile_in_ram

    @features("Feature8101")
    @level("Functionality")
    def test_edit_profile_saved_in_nvs(self):
        """
        Validate a profile can be saved in the NVS partition and loaded to RAM buffer then edit
        """
        data_to_overwrite = RandHexList(EditBuffer.LEN.DATA // 8)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send load request with first_sector_id={directory.files[profile.file_id_lsb].first_sector_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self, first_sector_id=
            ProfileManagement.Partition.SectorId.NVS | to_int(directory.files[profile.file_id_lsb].first_sector_id_lsb),
            count=directory.files[profile.file_id_lsb].n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send editBuffer request with "
                                 f"opcode={ProfileManagement.EditBufferOperation.Opcode.OVERWRITE}, "
                                 f"address={0}, data={data_to_overwrite}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=len(data_to_overwrite), opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE,
            address=0, data=data_to_overwrite)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=self, offset_bytes=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check profile_name in the user profile has been"
                                  "changed to {profile_name}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_to_overwrite +
                     HexList(profile)[len(data_to_overwrite):ReadBufferResponse.LEN.DATA // 8])
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        self.testCaseChecked("FUN_8101_0014", _AUTHOR)
    # end def test_edit_profile_saved_in_nvs

    @features("Feature8101")
    @level("Functionality")
    def test_set_profiles_saved_in_nvs_as_active_profile(self):
        """
        Validate an user profile saved in the NVS partition can be configured as the active profile
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.configure(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=profile.file_id_lsb,
            count=directory.files[profile.file_id_lsb].n_bytes,
            hash_key=directory.files[profile.file_id_lsb].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Send getSetMode request to check the curr_profile_file_id is {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            expected_curr_profile_file_id=profile.file_id_lsb)

        self.testCaseChecked("FUN_8101_0015", _AUTHOR)
    # end def test_set_profiles_saved_in_nvs_as_active_profile

    @features("Feature8101")
    @level("Functionality")
    def test_retrieve_hash_from_profiles(self):
        """
        Validate the hash of profiles can be retrieved from the device
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

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write the profile to NVS\n{profiles[index]}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profiles[index]),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profiles[index].first_sector_id_lsb,
                                             crc_32=profiles[index].crc_32)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over index in range(1..max_file_id or 1..max_sector_id)")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(min(self.config.F_MaxFileId - self.config.F_NumOnboardProfiles,
                               self.config.F_MaxSectorId - directory.id_manager.get_next_sector_id_lsb() + 1)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create a new host profile")
            # ----------------------------------------------------------------------------------------------------------
            profiles.append(ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE))
            profiles[index].update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.PROFILE_IDENTIFIER:
                                  self.config.F_NumOnboardProfiles + index})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profiles[index]}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profiles[index]),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profiles[index].first_sector_id_lsb,
                                             crc_32=profiles[index].crc_32)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over index in range(1..max_file_id or 1..max_sector_id)")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(min(self.config.F_MaxFileId - self.config.F_NumOnboardProfiles,
                               self.config.F_MaxSectorId - directory.id_manager.get_next_sector_id_lsb() + 1)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getHashes request with compute=0, file_id[0]=index")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_hashes(
                test_case=self, compute=0, file_id_0=index + 1, file_id_1=0, file_id_2=0, file_id_3=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getHashes response and check the hash is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.GetHashesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "hash_0": directory.files[index + 1].crc_32
            })
            checker.check_fields(self, response, self.feature_8101.get_hashes_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getHashes request with compute=1, file_id[0]=index")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_hashes(
                test_case=self, compute=1, file_id_0=index + 1, file_id_1=0, file_id_2=0, file_id_3=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getHashes response and check the hash is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ProfileManagementTestUtils.GetHashesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "hash_0": directory.files[index + 1].crc_32
            })
            checker.check_fields(self, response, self.feature_8101.get_hashes_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8101_0016", _AUTHOR)
    # end def test_retrieve_hash_from_profiles

    @features("Feature8101")
    @level("Functionality")
    def test_profile_saved_in_nvs_kept_after_dfu(self):
        """
        Validate the user profiles saved in the NVS partition will be kept after DFU
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enter bootloader mode')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.jump_on_bootloader(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform DFU")
        # --------------------------------------------------------------------------------------------------------------
        dfu_file = os.path.join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)
        LogHelper.log_info(self, f'DFU file: {dfu_file}')
        self.post_requisite_program_mcu_initial_state = True
        self._perform_dfu()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(test_case=self, text="Force target on application")
        # --------------------------------------------------------------------------------------------------------------
        self.debugger.reset()
        DfuTestUtils.force_target_on_application(test_case=self, check_required=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load request with first_sector_id="
                                 f"{ProfileManagement.Partition.SectorId.NVS | profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self, first_sector_id=ProfileManagement.Partition.SectorId.NVS | profile.first_sector_id_lsb,
            count=directory.files[profile.file_id_lsb].n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        ram_buffer_data = ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(
            self, directory.files[profile.file_id_lsb].n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the data is as expected")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range((len(ram_buffer_data) // (ReadBufferResponse.LEN.DATA // 8)) + 1):
            self.assertEqual(
                expected=HexList(profile)[offset * (ReadBufferResponse.LEN.DATA // 8):
                                          (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                obtained=ram_buffer_data[offset * (ReadBufferResponse.LEN.DATA // 8):
                                         (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                msg=f"The data parameter differs found at offset {offset * (ReadBufferResponse.LEN.DATA // 8)}, "
                    f"(expected:{HexList(profile)}, obtained:{ram_buffer_data})")
        # end for

        self.testCaseChecked("FUN_8101_0017", _AUTHOR)
    # end def test_profile_saved_in_nvs_kept_after_dfu

    @features("Feature8101")
    @level("Functionality")
    def test_profile_saved_in_nvs_reset_after_set_oob(self):
        """
        Validate the content of user profiles saved in the NVS partition will be reset after setting OOB
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1805.SetOobState request")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load request with first_sector_id="
                                 f"{ProfileManagement.Partition.SectorId.NVS | profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.load_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            first_sector_id=ProfileManagement.Partition.SectorId.NVS | to_int(
                directory.files[profile.file_id_lsb].first_sector_id_lsb),
            count=directory.files[profile.file_id_lsb].n_bytes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code is received")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        self.testCaseChecked("FUN_8101_0018", _AUTHOR)
    # end def test_profile_saved_in_nvs_reset_after_set_oob

    @features("Feature8101")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.FN_KEY, KEY_ID.ONBOARD_PROFILE_1,))
    @services('SimultaneousKeystrokes')
    def test_switch_onboard_profiles_thru_shortcut_keys(self):
        """
        Validate the FW shall assign onboard profile indices according to their order in the directory
        """
        trigger_keys = ProfileManagementTestUtils.get_onboard_profiles_selection_keys(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create {self.config.F_NumOnboardProfiles} onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        profiles = self.create_onboard_profiles_and_save_in_nvs(test_case=self, directory=directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {trigger_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for index, trigger_key in enumerate(trigger_keys):
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a key combination on the FN + {trigger_key!s}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(0.05)
            self.button_stimuli_emulator.keystroke(key_id=trigger_key, delay=1)
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait profileChangeEvent and check the nwe_profile is as expected")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({'new_profile': (checker.check_new_profile, profiles[index].file_id_lsb)})
            checker.check_fields(self, response, self.feature_8101.profile_change_event_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8101_0019", _AUTHOR)
    # end def test_switch_onboard_profiles_thru_shortcut_keys

    @features("Feature8101")
    @features("Feature8101MultipleProfiles")
    @level("Functionality")
    def test_switch_onboard_profiles_thru_profile_selection_button(self):
        """
        Validate the FW shall assign onboard profile indices according to their order in the directory and the user is
        allowed to switch the onboard profiles thru profile selection button
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2, KEY_ID.BUTTON_3] \
            if self.f.PRODUCT.F_IsMice else [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_C]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create {self.config.F_NumOnboardProfiles} onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        profiles = self.create_onboard_profiles_and_save_in_nvs(test_case=self, directory=directory, save_in_nvs=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table file to remap keys be the 'Profile X selection buttons'")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = []
        for index in range(self.config.F_NumOnboardProfiles):
            remapped_key_settings.append(
                RemappedKey(action_type=RemappedKey.ActionType.FUNCTION, trigger_key=trigger_keys[index],
                            action_key=KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE,
                            profile_number=profiles[index].file_id_lsb))
        # end for
        remapped_key_settings.append(
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=KEY_ID.KEYBOARD_D,
                        action_key=KEY_ID.KEYBOARD_A,
                        action_modifier_keys=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_SHIFT]))
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over index in range({self.config.F_NumOnboardProfiles})")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(self.config.F_NumOnboardProfiles):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Link the file ID of FKC with the created FKC base layer table")
            # ----------------------------------------------------------------------------------------------------------
            profiles[index].update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profiles[index]}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profiles[index]),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=profiles[index].first_sector_id_lsb,
                                             crc_32=profiles[index].crc_32)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self,
            "Send configure request with file_id="
            f"{ProfileManagement.Partition.FileId.NVS | profiles[self.config.F_NumOnboardProfiles - 1].file_id_lsb}, "
            "feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.NVS |
                                            profiles[self.config.F_NumOnboardProfiles - 1].file_id_lsb,
                                            count=len(HexList(profiles[self.config.F_NumOnboardProfiles - 1])),
                                            crc_32=profiles[self.config.F_NumOnboardProfiles - 1].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                  fkc_enabled=1, set_toggle_keys_enabled=0)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over {trigger_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for index, trigger_key in enumerate(trigger_keys):
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {trigger_key} to switch to profile{index}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=trigger_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait profileChangeEvent and check the nwe_profile is as expected")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({'new_profile': (checker.check_new_profile, remapped_key_settings[index].profile_number)})
            checker.check_fields(self, response, self.feature_8101.profile_change_event_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8101_0020", _AUTHOR)
    # end def test_switch_onboard_profiles_thru_profile_selection_button

    @features("Feature8101")
    @features("Feature8101FlashEraseCounter")
    @level("Functionality")
    def test_flash_erase_count_increase_after_nvs_bank_switching(self):
        """
        Validate the FW shall increment the flash erase counter at every other NVS bank switch
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response_1 = ProfileManagementTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform NVS bank switch")
        # --------------------------------------------------------------------------------------------------------------
        # TODO - Switch NVS bank

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response_2 = ProfileManagementTestUtils.HIDppHelper.get_capabilities(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getCapabilities response and check the erase counter is reduced one count")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "flash_erase_counter": (checker.check_flash_erase_counter, response_1.flash_erase_counter - 1)
        })
        checker.check_fields(self, response_2, self.feature_8101.get_capabilities_response_cls, check_map)

        self.testCaseChecked("FUN_8101_0021", _AUTHOR)
    # end def test_flash_erase_count_increase_after_nvs_bank_switching

    @features("Feature8101")
    @level("Functionality")
    def test_file_system_error_kept_after_power_cycle(self):
        """
        Validate the error is stored to persistent section of RAM such that it should not be erased after a FW
        reboot.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send configure request with invalid hashes")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8101.configure_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8101_index,
            feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=profile.file_id_lsb,
            count=directory.files[profile.file_id_lsb].n_bytes,
            hash_key=HexList(0, 0, 0, 0))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate HW_ERROR(0x04) error code is sent")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getError request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getError response and check the fsErrorCode is Feature Configuration Error "
                                  f"check error({ProfileManagement.FileSystemErrorCode.FILE_DETAIL_MISMATCH})")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetErrorResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "fs_error_code": (checker.check_fs_error_code, ProfileManagement.FileSystemErrorCode.FILE_DETAIL_MISMATCH),
            "fs_error_param_1": (checker.check_fs_error_param_1, profile.file_id_lsb),
            "fs_error_param_2": (checker.check_fs_error_param_2, ProfileManagement.FileSystemErrorCode.NOT_SUPPORTED),
        })
        checker.check_fields(self, response, self.feature_8101.get_error_response_cls, check_map)

        self.testCaseChecked("FUN_8101_0022", _AUTHOR)
    # end def test_file_system_error_kept_after_power_cycle

    @features("Feature8101")
    @features("Feature8101MultipleProfiles")
    @level("Functionality")
    def test_link_feature_settings_file_to_multiple_profiles(self):
        """
        Validate a feature settings file can be linked to multiple user profiles
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2, KEY_ID.BUTTON_3] \
            if self.f.PRODUCT.F_IsMice else [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_C]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create {self.config.F_NumOnboardProfiles} onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        profiles = self.create_onboard_profiles_and_save_in_nvs(test_case=self, directory=directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC base layer table to remap several keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[0],
                        action_key=KEY_ID.KEYBOARD_Z),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[1],
                        action_key=KEY_ID.KEYBOARD_Y),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[2],
                        action_key=KEY_ID.KEYBOARD_X),
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Edit the file_id of FKC base layer of the onboard profile with "
                  f"{main_tables[FkcMainTable.Layer.BASE].first_sector_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        profiles[0].update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                              main_tables[FkcMainTable.Layer.BASE].file_id_lsb})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send save request with first_sector_id={profiles[0].first_sector_id_lsb} "
                                 "to save the user profile in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profiles[0]), store_in_nvs=True,
                                         first_sector_id_lsb=profiles[0].first_sector_id_lsb,
                                         crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Set the file_id of 0x1b05 with {main_tables[FkcMainTable.Layer.BASE].first_sector_id_lsb} "
                           f"in the {profiles[1]}")
        # --------------------------------------------------------------------------------------------------------------
        profiles[1].update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                              main_tables[FkcMainTable.Layer.BASE].file_id_lsb})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send save request with first_sector_id={profiles[1].first_sector_id_lsb}"
                                 " to save the user profile in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profiles[1]), store_in_nvs=True,
                                         first_sector_id_lsb=profiles[1].first_sector_id_lsb,
                                         crc_32=profiles[1].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profiles[0].file_id_lsb} "
                                 "to activate the first profile")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.NVS | profiles[0].file_id_lsb,
                                            count=len(HexList(profiles[0])),
                                            crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                  fkc_enabled=1, set_toggle_keys_enabled=0)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check the curr_profile_file_id is {profiles[0].file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            expected_curr_profile_file_id=profiles[0].file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over trigger_key in {remapped_key_settings}:")
        # --------------------------------------------------------------------------------------------------------------
        for remapped_key in remapped_key_settings:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {remapped_key.trigger_key}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(remapped_key.trigger_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the expected user action has been performed")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
                test_case=self, remapped_key=remapped_key)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profiles[0].file_id_lsb} "
                                 "to activate the first profile")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.NVS | profiles[1].file_id_lsb,
                                            count=len(HexList(profiles[1])),
                                            crc_32=profiles[1].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                  fkc_enabled=1, set_toggle_keys_enabled=0)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check the curr_profile_file_id is {profiles[1].file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            expected_curr_profile_file_id=profiles[1].file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over trigger_key in {remapped_key_settings}:")
        # --------------------------------------------------------------------------------------------------------------
        for remapped_key in remapped_key_settings:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {remapped_key.trigger_key}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(remapped_key.trigger_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the expected user action has been performed")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
                test_case=self, remapped_key=remapped_key)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8101_0023", _AUTHOR)
    # end def test_link_feature_settings_file_to_multiple_profiles

    @features("Feature8101")
    @level("Functionality")
    def test_configure_1b05_feature_setting_file(self):
        """
        Validate a feature settings file of 0x1b05 can be configured as the active profile directly.
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2, KEY_ID.BUTTON_3] \
            if self.f.PRODUCT.F_IsMice else [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_C]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, _ = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC base layer table to remap several keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[0],
                        action_key=KEY_ID.KEYBOARD_Z),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[1],
                        action_key=KEY_ID.KEYBOARD_Y),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[2],
                        action_key=KEY_ID.KEYBOARD_X),
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Send configure request with file_id={main_tables[FkcMainTable.Layer.BASE].file_id_lsb}, "
                           "feature_id=0x1b05")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
                                            file_id=main_tables[FkcMainTable.Layer.BASE].file_id_lsb,
                                            count=main_tables[FkcMainTable.Layer.BASE].n_bytes,
                                            crc_32=main_tables[FkcMainTable.Layer.BASE].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                  fkc_enabled=1, set_toggle_keys_enabled=0)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over trigger_key in trigger_keys:")
        # --------------------------------------------------------------------------------------------------------------
        for remapped_key in remapped_key_settings:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {remapped_key.trigger_key}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(remapped_key.trigger_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the expected user action has been performed")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
                test_case=self, remapped_key=remapped_key)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_8101_0024", _AUTHOR)
    # end def test_configure_1b05_feature_setting_file

    @features("Feature8101")
    @features('Bluetooth')
    @level("Functionality")
    @services('BleContext')
    @services('Debugger')
    def test_profile_persistence_when_switching_protocols(self):
        """
        Validate the profile is persistent in different protocol
        """
        if KEY_ID.LS2_BLE_CONNECTION_TOGGLE in self.button_stimuli_emulator._keyboard_layout.KEYS.keys():
            connection_buttons = [KEY_ID.LS2_BLE_CONNECTION_TOGGLE] * 2
        elif KEY_ID.LS2_CONNECTION in self.button_stimuli_emulator._keyboard_layout.KEYS.keys() \
                and KEY_ID.BLE_CONNECTION in self.button_stimuli_emulator._keyboard_layout.KEYS.keys():
            connection_buttons = [KEY_ID.LS2_CONNECTION, KEY_ID.BLE_CONNECTION]
        else:
            raise KeyError('No available connection button is defined in the key matrix.')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create {self.config.F_NumOnboardProfiles} onboard profiles and save in NVS")
        # --------------------------------------------------------------------------------------------------------------
        profiles = self.create_onboard_profiles_and_save_in_nvs(test_case=self, directory=directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over index in range(2) [Unifying, BLE]")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(2):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Create a host_profile_{index}")
            # ----------------------------------------------------------------------------------------------------------
            host_profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write the host profile to NVS\n{host_profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(host_profile),
                                             store_in_nvs=True,
                                             first_sector_id_lsb=host_profile.first_sector_id_lsb,
                                             crc_32=host_profile.crc_32)
            profiles.append(host_profile)

            if index == 1:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Switch to BLE Mode")
                # ------------------------------------------------------------------------------------------------------
                self.post_requisite_exit_ble_channel = True
                ProtocolManagerUtils.select_channel_by_protocol(self, LogitechProtocol.BLE)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Update the profile directory of NVS")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send configure request with file_id={host_profile.file_id_lsb}, feature_id=0x8101")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE,
                                                file_id=host_profile.file_id_lsb,
                                                count=directory.files[host_profile.file_id_lsb].n_bytes,
                                                crc_32=directory.files[host_profile.file_id_lsb].crc_32)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check the curr_profile_file_id is {profiles[-1].file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            expected_curr_profile_file_id=profiles[-1].file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Exit BLE channel")
        # --------------------------------------------------------------------------------------------------------------
        ProtocolManagerUtils.exit_ble_channel(self)
        self.post_requisite_exit_ble_channel = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {connection_buttons[0]} to switch to Unifying")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=connection_buttons[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check the curr_profile_file_id is {profiles[-1].file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            expected_curr_profile_file_id=profiles[-1].file_id_lsb)

        self.testCaseChecked("FUN_8101_0025", _AUTHOR)
    # end def test_profile_persistence_when_switching_protocols

    @features("Feature8101")
    @level("Functionality")
    @services("HardwareReset")
    def test_revert_power_on_profile_to_oob_when_configure_invalid_power_on_profile(self):
        """
        Validate the power-on profile will be reset to OOB profile at next power reset if the last set power-on profile
        is invalid.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the profile ID")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.PROFILE_IDENTIFIER: profile.file_id_lsb + 1})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to set the power on profile to {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.SET,
            power_on_profile=profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetPowerOnParams request to check the power on profile is {profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=profile.file_id_lsb)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, "Send getSetPowerOnParams request to check the power on profile is "
                  f"{ProfileManagement.Partition.FileId.OOB | 0x0001}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_power_on_params(
            test_case=self,
            request_type=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=ProfileManagement.Partition.FileId.OOB | 0x0001)

        self.testCaseChecked("FUN_8101_0026", _AUTHOR)
    # end def test_revert_power_on_profile_to_oob_when_configure_invalid_power_on_profile

    @features("Feature8101")
    @level("Functionality")
    def test_sw_in_control_switching_profile_mode(self):
        """
        Validate the device's mode can be switched to SW in control mode and the onboard profiles can't be
        configured in this mode.
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2] \
            if self.f.PRODUCT.F_IsMice else [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC base layer table to remap several keys and save it in the RAM")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION, trigger_key=trigger_keys[0],
                        action_key=KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE),
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION, trigger_key=trigger_keys[1],
                        action_key=KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE,
                        profile_number=profiles[0].file_id_lsb)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings,
                                                              save_in_nvs=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request to activate the {main_tables[FkcMainTable.Layer.BASE]}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
            file_id=ProfileManagement.Partition.FileId.RAM,
            count=main_tables[FkcMainTable.Layer.BASE].n_bytes,
            crc_32=main_tables[FkcMainTable.Layer.BASE].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                  fkc_enabled=1, set_toggle_keys_enabled=0)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to set the profile mode to {ProfileManagement.ProfileMode.SW_CONTROL}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.SET,
            profile_mode=ProfileManagement.ProfileMode.SW_CONTROL,
            # The curr_profile_file_id is not updated when configuring a feature settings file.
            expected_curr_profile_file_id=ProfileManagement.Partition.FileId.OOB | 0x0001)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check the profile mode is {ProfileManagement.ProfileMode.SW_CONTROL}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.GET,
            profile_mode=ProfileManagement.ProfileMode.SW_CONTROL)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over index in range({self.config.F_NumOnboardProfiles} * 3)")
        # --------------------------------------------------------------------------------------------------------------
        profile_selection_keys = ProfileManagementTestUtils.get_onboard_profiles_selection_keys(test_case=self)
        for index in range(self.config.F_NumOnboardProfiles * 3):
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            if index < self.config.F_NumOnboardProfiles:
                if len(profile_selection_keys) > 0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Emulate a key combination on the FN + {profile_selection_keys[index]!s}')
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
                    sleep(0.05)
                    self.button_stimuli_emulator.keystroke(key_id=profile_selection_keys[index], delay=1)
                    self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
                else:
                    continue
                # end if
            elif index < self.config.F_NumOnboardProfiles * 2:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keystroke on the {trigger_keys[0]!s}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=trigger_keys[0])
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keystroke on the {trigger_keys[1]!s}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=trigger_keys[1])
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait profileChangeEvent and check the failure=1")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            profile_change_result_checker = ProfileManagementTestUtils.ProfileChangeResultResponseChecker
            profile_change_result_check_map = profile_change_result_checker.get_default_check_map(self)
            profile_change_result_check_map.update({'failure': (
                profile_change_result_checker.check_failure, ProfileManagement.ProfileChangeResult.Result.FAILURE)})
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({'new_profile': (checker.check_new_profile,
                                              profiles[index % self.config.F_NumOnboardProfiles].file_id_lsb),
                              'profile_change_result': (checker.check_profile_change_result,
                                                        profile_change_result_check_map)})
            checker.check_fields(self, response, self.feature_8101.profile_change_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, "Send getSetMode request to check the profile mode is "
                      f"{ProfileManagement.ProfileMode.SW_CONTROL}")
            # ----------------------------------------------------------------------------------------------------------
            self._send_and_check_the_get_set_mode_response(
                test_case=self,
                request_type_profile_mode=ProfileManagementTestUtils.RequestType.GET,
                profile_mode=ProfileManagement.ProfileMode.SW_CONTROL)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request to activate the {profiles[0]}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=profiles[0].file_id_lsb,
            count=directory.files[profiles[0].file_id_lsb].n_bytes,
            crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check the current profile file ID is {profiles[0].file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.GET,
            profile_mode=ProfileManagement.ProfileMode.SW_CONTROL,
            expected_curr_profile_file_id=profiles[0].file_id_lsb)

        self.testCaseChecked("FUN_8101_0027", _AUTHOR)
    # end def test_sw_in_control_switching_profile_mode

    @features("Feature8101")
    @level("Functionality")
    def test_set_hw_sw_control_profile_mode(self):
        """
        Validate the user can set the profile_mode to 1(Software and device are in control of switching profiles) then
        switch profiles thru shortcut or SW
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2] \
            if self.f.PRODUCT.F_IsMice else [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create onboard profiles and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC base layer table to remap several keys and save it in the RAM")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION, trigger_key=trigger_keys[0],
                        action_key=KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE),
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION, trigger_key=trigger_keys[1],
                        action_key=KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE,
                        profile_number=profiles[0].file_id_lsb)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings,
                                                              save_in_nvs=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request to activate the {main_tables[FkcMainTable.Layer.BASE]}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
            file_id=ProfileManagement.Partition.FileId.RAM,
            count=main_tables[FkcMainTable.Layer.BASE].n_bytes,
            crc_32=main_tables[FkcMainTable.Layer.BASE].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                  fkc_enabled=1, set_toggle_keys_enabled=0)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to set the profile mode to {ProfileManagement.ProfileMode.HW_SW_CONTROL}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.SET,
            profile_mode=ProfileManagement.ProfileMode.HW_SW_CONTROL,
            # The curr_profile_file_id is not updated when configuring a feature settings file.
            expected_curr_profile_file_id=ProfileManagement.Partition.FileId.OOB | 0x0001)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check the profile mode is {ProfileManagement.ProfileMode.HW_SW_CONTROL}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.GET,
            profile_mode=ProfileManagement.ProfileMode.HW_SW_CONTROL)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over index in range({self.config.F_NumOnboardProfiles} * 3)")
        # --------------------------------------------------------------------------------------------------------------
        profile_selection_keys = ProfileManagementTestUtils.get_onboard_profiles_selection_keys(test_case=self)
        for index in range(self.config.F_NumOnboardProfiles * 3):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send configure request to activate the {main_tables[FkcMainTable.Layer.BASE]}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(
                test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
                file_id=ProfileManagement.Partition.FileId.RAM,
                count=main_tables[FkcMainTable.Layer.BASE].n_bytes,
                crc_32=main_tables[FkcMainTable.Layer.BASE].crc_32)
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
            if index < self.config.F_NumOnboardProfiles:
                if len(profile_selection_keys) > 0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Emulate a key combination on the FN + {profile_selection_keys[index]!s}')
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
                    sleep(0.05)
                    self.button_stimuli_emulator.keystroke(key_id=profile_selection_keys[index], delay=1)
                    self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
                else:
                    continue
                # end if
            elif index < self.config.F_NumOnboardProfiles * 2:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keystroke on the {trigger_keys[0]!s}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=trigger_keys[0])
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keystroke on the {trigger_keys[1]!s}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=trigger_keys[1])
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait profileChangeEvent and check the failure=0")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            profile_change_result_checker = ProfileManagementTestUtils.ProfileChangeResultResponseChecker
            profile_change_result_check_map = profile_change_result_checker.get_default_check_map(self)
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({'new_profile': (checker.check_new_profile,
                                              profiles[index % self.config.F_NumOnboardProfiles].file_id_lsb if
                                              index < self.config.F_NumOnboardProfiles * 2 else
                                              profiles[0].file_id_lsb),
                              'profile_change_result': (checker.check_profile_change_result,
                                                        profile_change_result_check_map)})
            checker.check_fields(self, response, self.feature_8101.profile_change_event_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, "Send getSetMode request to check the profile mode is "
                      f"{ProfileManagement.ProfileMode.HW_SW_CONTROL}")
            # ----------------------------------------------------------------------------------------------------------
            self._send_and_check_the_get_set_mode_response(
                test_case=self,
                request_type_profile_mode=ProfileManagementTestUtils.RequestType.GET,
                profile_mode=ProfileManagement.ProfileMode.HW_SW_CONTROL,
                expected_curr_profile_file_id=profiles[index % self.config.F_NumOnboardProfiles].file_id_lsb if
                index < self.config.F_NumOnboardProfiles * 2 else profiles[0].file_id_lsb)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request to activate the {profiles[0]}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=profiles[0].file_id_lsb,
            count=directory.files[profiles[0].file_id_lsb].n_bytes,
            crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to check the current profile file ID is {profiles[0].file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.GET,
            profile_mode=ProfileManagement.ProfileMode.HW_SW_CONTROL,
            expected_curr_profile_file_id=profiles[0].file_id_lsb)

        self.testCaseChecked("FUN_8101_0028", _AUTHOR)
    # end def test_set_hw_sw_control_profile_mode

    @features("Feature8101")
    @level("Functionality")
    @services("HardwareReset")
    def test_reset_device_profile_mode_after_power_cycle(self):
        """
        Validate the device's mode will be reset to onboard mode after power cycle
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to set the profile mode to {ProfileManagement.ProfileMode.SW_CONTROL}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.SET,
            profile_mode=ProfileManagement.ProfileMode.SW_CONTROL)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Power OFF -> ON the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request and check onboard_mode is {ProfileManagement.ProfileMode.HW_SW_CONTROL}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self, profile_mode=ProfileManagement.ProfileMode.HW_SW_CONTROL)

        self.testCaseChecked("FUN_8101_0029", _AUTHOR)
    # end def test_reset_device_profile_mode_after_power_cycle

    @features("Feature8101")
    @features('Feature1830powerMode', 3)
    @level("Functionality")
    def test_reset_device_profile_mode_after_depp_sleep(self):
        """
        Validate the device's mode will be reset to onboard mode after waking up from the deep-sleep
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request to set the profile mode to {ProfileManagement.ProfileMode.SW_CONTROL}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.SET,
            profile_mode=ProfileManagement.ProfileMode.SW_CONTROL)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake-up the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Send getSetMode request and check onboard_mode is {ProfileManagement.ProfileMode.HW_SW_CONTROL}")
        # --------------------------------------------------------------------------------------------------------------
        self._send_and_check_the_get_set_mode_response(
            test_case=self, profile_mode=ProfileManagement.ProfileMode.HW_SW_CONTROL)

        self.testCaseChecked("FUN_8101_0030", _AUTHOR)
    # end def test_reset_device_profile_mode_after_depp_sleep

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Functionality")
    @services("HardwareReset")
    def test_reset_configured_settings_in_ram_after_power_cycle(self):
        """
        Validate the settings configured in RAM will be reset after device power cycle.
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2] if self.f.PRODUCT.F_IsMice else \
            [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a base layer to remap {trigger_keys}")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MOUSE, trigger_key=trigger_keys[0],
                        action_key=KEY_ID.BUTTON_3),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[1],
                        action_key=KEY_ID.KEYBOARD_A,
                        action_modifier_keys=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_SHIFT])
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings,
                                                              save_in_nvs=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
                                            file_id=ProfileManagement.Partition.FileId.RAM,
                                            count=main_tables[FkcMainTable.Layer.BASE].n_bytes,
                                            crc_32=main_tables[FkcMainTable.Layer.BASE].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            test_case=self,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.ENABLE,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
            toggle_keys_enabled=FullKeyCustomization.ToggleKeyStatus.DISABLE)

        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        for index in range(2):
            if index == 1:
                self.reset(hardware_reset=True)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {trigger_keys[0]}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=trigger_keys[0])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the expected HID mouse report is received")
            # ----------------------------------------------------------------------------------------------------------
            if index == 1:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(trigger_keys[0], MAKE))
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(trigger_keys[0], BREAK))
            else:
                FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
                    test_case=self, remapped_key=remapped_key_settings[0])
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {trigger_keys[1]}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=trigger_keys[1])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the expected HID keyboard reports are received")
            # ----------------------------------------------------------------------------------------------------------
            if index == 1:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(trigger_keys[1], MAKE))
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(trigger_keys[1], BREAK))
            else:
                FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
                    test_case=self, remapped_key=remapped_key_settings[1])
            # end if
        # end for

        self.testCaseChecked("FUN_8101_0031", _AUTHOR)
    # end def test_reset_configured_settings_in_ram_after_power_cycle

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

    def _perform_first_command_of_dfu(self):
        """
        Perform the first command of DFU: DfuStart. It will also create the DFU file parser objet

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

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            dfu_file_name = self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            dfu_file_name = self.f.SHARED.DEVICES.F_DeviceApplicationDfuFileName
        else:
            raise ValueError(f"Unknown target type: {self.config_manager.current_target}")
        # end if

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", dfu_file_name),
            device_index=ChannelUtils.get_device_index(test_case=self),
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

    def _perform_dfu(self):
        """
        Perform a DFU, if log_step and log_check are <=0, there is no log message.
        """
        dfu_file_parser = self._perform_first_command_of_dfu()
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
                                  status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

    # end def _perform_dfu

    @staticmethod
    def _send_and_check_the_get_set_mode_response(
            test_case,
            request_type_onboard_mode=ProfileManagementTestUtils.RequestType.GET,
            request_type_profile_mode=ProfileManagementTestUtils.RequestType.GET,
            onboard_mode=ProfileManagement.Mode.ONBOARD_MODE,
            profile_mode=ProfileManagement.ProfileMode.HW_SW_CONTROL,
            expected_curr_profile_file_id=ProfileManagement.Partition.FileId.OOB | 0x0001):
        """
        Send the GetSetMode request to set/get the current onboard/profile mode and check all response fields are as
        expected.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param request_type_onboard_mode: Request type of onboard mode - OPTIONAL
        :type request_type_onboard_mode: ``int | ProfileManagementTestUtils.RequestType``
        :param request_type_profile_mode: Request type of profile mode - OPTIONAL
        :type request_type_profile_mode: ``int | ProfileManagementTestUtils.RequestType``
        :param onboard_mode: The set/expected onboard mode - OPTIONAL
        :type onboard_mode: ``int | ProfileManagement.Mode``
        :param profile_mode: The set/expected profile mode - OPTIONAL
        :type profile_mode: ``int | ProfileManagement.ProfileMode``
        :param expected_curr_profile_file_id: Expected current profile file ID - OPTIONAL
        :type expected_curr_profile_file_id: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            test_case, f"Send getSetMode request with set_onboard_mode={ProfileManagementTestUtils.RequestType.GET},"
                       f"set_profile_mode={ProfileManagementTestUtils.RequestType.GET}, onboard_mode={onboard_mode},"
                       f"profile_mode={profile_mode}")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_set_mode(
            test_case=test_case, onboard_mode=onboard_mode, profile_mode=profile_mode,
            set_onboard_mode=request_type_onboard_mode, set_profile_mode=request_type_profile_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case, "Wait the getSetMode response and all fields")
        # --------------------------------------------------------------------------------------------------------------
        operating_mode_checker = ProfileManagementTestUtils.OperatingModeResponseChecker
        operating_mode_check_map = operating_mode_checker.get_default_check_map(test_case=test_case)
        operating_mode_check_map.update({
            'onboard_mode': (
                operating_mode_checker.check_onboard_mode, onboard_mode),
            'profile_mode': (
                operating_mode_checker.check_profile_mode, profile_mode),
        })
        checker = ProfileManagementTestUtils.GetSetModeResponseChecker
        check_map = checker.get_default_check_map(test_case=test_case)
        check_map.update({'operating_mode_response': (
            checker.check_operating_mode_response, operating_mode_check_map),
                          'curr_profile_file_id': (
            checker.check_curr_profile_file_id, expected_curr_profile_file_id)
        })
        checker.check_fields(test_case, response, test_case.feature_8101.get_set_mode_response_cls, check_map)
    # end def _send_and_check_the_get_set_mode_response

    @staticmethod
    def _send_and_check_the_get_set_power_on_params(test_case,
                                                    request_type=ProfileManagementTestUtils.RequestType.GET,
                                                    power_on_profile=ProfileManagement.Partition.FileId.OOB | 0x0001):
        """
        Send the GetSetPowerOnParams request to set/get the power on parameters and check all response fields are as
        expected.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param request_type: Request type of onboard mode - OPTIONAL
        :type request_type: ``int | ProfileManagementTestUtils.RequestType``
        :param power_on_profile: The set/expected power on profile - OPTIONAL
        :type power_on_profile: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, f"Send getSetPowerOnParams request with set_power_on_profile={request_type}, "
                                      f"power_on_profile={power_on_profile}")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=test_case, set_power_on_profile=request_type, power_on_profile=power_on_profile)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            test_case, f"Wait the getSetPowerOnParams response and check the power_on_profile is {power_on_profile}")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetSetPowerOnParamsResponseChecker
        check_map = checker.get_default_check_map(test_case)
        check_map.update({
            'power_on_profile': (checker.check_power_on_profile, power_on_profile)})
        checker.check_fields(
            test_case, response, test_case.feature_8101.get_set_power_on_params_response_cls, check_map)
    # end def _send_and_check_the_get_set_power_on_params
# end class ProfileManagementFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
