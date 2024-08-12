#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8100.interface
:brief: HID++ 2.0 ``OnboardProfiles`` interface test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/01/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.gaming.feature_8100.onboardprofiles import OnboardProfilesTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OnboardProfilesInterfaceTestCase(OnboardProfilesTestCase):
    """
    Validate ``OnboardProfiles`` interface test cases
    """

    @features("Feature8100")
    @level("Interface")
    def test_get_onboard_profiles_info_interface(self):
        """
        Validate ``GetOnboardProfilesInfo`` interface.
        The profile info shall be the same as the constant project settings.

        [0] getOnboardProfilesInfo() → MemoryModelID,ProfileFormatID,MacroFormatID,ProfileCount,ProfileCountOOB,
                                       ButtonCount,SectorCount,SectorSize,MechanicalLayout,VariousInfo,SectorCountRule
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetOnboardProfilesInfo request")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.get_onboard_profiles_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.get_onboard_profiles_info_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the returned information in the onboardProfilesInfo are all as expected.")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.GetOnboardProfilesInfoResponseChecker.check_fields(
            self, response, self.feature_8100.get_onboard_profiles_info_response_cls)

        self.testCaseChecked("INT_8100_0001", _AUTHOR)
    # end def test_get_onboard_profiles_info_interface

    @features("Feature8100")
    @level("Interface")
    def test_set_onboard_mode_interface(self):
        """
        Validate ``SetOnboardMode`` interface

        [1] setOnboardMode(onboardMode)
        """
        onboard_mode = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode={onboard_mode}")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.set_onboard_mode_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index,
            onboard_mode=onboard_mode)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.set_onboard_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetOnboardModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, request.deviceIndex),
            "featureIndex": (checker.check_feature_index, request.featureIndex),
        }
        checker.check_fields(self, response, self.feature_8100.set_onboard_mode_response_cls, check_map)

        self.testCaseChecked("INT_8100_0002", _AUTHOR)
    # end def test_set_onboard_mode_interface

    @features("Feature8100")
    @level("Interface")
    def test_get_onboard_mode_interface(self):
        """
        Validate ``GetOnboardMode`` interface

        [2] getOnboardMode()→ onboardMode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetOnboardMode request")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.get_onboard_mode_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.get_onboard_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the returned onboardMode = {OnboardProfiles.Mode.ONBOARD_MODE}")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.GetOnboardModeResponseChecker.check_fields(
            self, response, self.feature_8100.get_onboard_mode_response_cls)

        self.testCaseChecked("INT_8100_0003", _AUTHOR)
    # end def test_get_onboard_mode_interface

    @features("Feature8100")
    @level("Interface")
    def test_set_active_profile_interface(self):
        """
        Validate ``SetActiveProfile`` interface

        [3] setActiveProfile(profileID)
        """
        self.post_requisite_reload_nvs = True
        profile_id = 0x0101
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setActiveProfile(profileID=0x0101) request")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.set_active_profile_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index,
            profile_id=profile_id)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.set_active_profile_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetActiveProfileResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, request.deviceIndex),
            "featureIndex": (checker.check_feature_index, request.featureIndex),
        }
        checker.check_fields(self, response, self.feature_8100.set_active_profile_response_cls, check_map)

        self.testCaseChecked("INT_8100_0004", _AUTHOR)
    # end def test_set_active_profile_interface

    @features("Feature8100")
    @level("Interface")
    def test_get_active_profile_interface(self):
        """
        Validate ``GetActiveProfile`` interface

        [4] getActiveProfile()→ profileID
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetActiveProfile request")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.get_active_profile_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.get_active_profile_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the returned profileID = 0x0101")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.GetActiveProfileResponseChecker.check_fields(
            self, response, self.feature_8100.get_active_profile_response_cls)

        self.testCaseChecked("INT_8100_0005", _AUTHOR)
    # end def test_get_active_profile_interface

    @features("Feature8100")
    @level("Interface")
    def test_read_data_interface(self):
        """
        Validate ``ReadData`` interface

        [5] readData(sectorID, subAddress, readCount) → data
        """
        sector_id = 0
        sub_address = 0
        read_count = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readData request with sectorID=0, subAddress=0, readCount=0")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.read_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index,
            sector_id=sector_id,
            sub_address=sub_address,
            read_count=read_count)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.read_data_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the returned 16 bytes data are all 0xFF")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.ReadDataResponseChecker.check_fields(
            self, response, self.feature_8100.read_data_response_cls)

        self.testCaseChecked("INT_8100_0006", _AUTHOR)
    # end def test_read_data_interface

    @features("Feature8100")
    @level("Interface")
    def test_start_write_interface(self):
        """
        Validate ``StartWrite`` interface

        [6] startWrite(sectorID, subAddress, writeCount)
        """
        self.post_requisite_reload_nvs = True
        sector_id = 0
        sub_address = 0
        write_count = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send StartWrite request")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.start_write_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index,
            sector_id=sector_id,
            sub_address=sub_address,
            write_count=write_count)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.start_write_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check StartWriteResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, request.deviceIndex),
            "featureIndex": (checker.check_feature_index, request.featureIndex),
        }
        checker.check_fields(self, response, self.feature_8100.start_write_response_cls, check_map)

        self.testCaseChecked("INT_8100_0007", _AUTHOR)
    # end def test_start_write_interface

    @features("Feature8100")
    @level("Interface")
    def test_execute_macro_interface(self):
        """
        Validate ``ExecuteMacro`` interface

        [9] executeMacro(sectorID, subAddress)
        """
        self.post_requisite_reload_nvs = True
        sector_id = int(Numeral(self.config.F_ProfileCount)) + 1
        sub_address = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send executeMacro with sectorID={sector_id}, subAddress=0")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.execute_macro_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index,
            sector_id=sector_id,
            sub_address=sub_address)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.execute_macro_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check ExecuteMacroResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, request.deviceIndex),
            "featureIndex": (checker.check_feature_index, request.featureIndex),
        }
        checker.check_fields(self, response, self.feature_8100.execute_macro_response_cls, check_map)

        self.testCaseChecked("INT_8100_0008", _AUTHOR)
    # end def test_execute_macro_interface

    @features("Feature8100")
    @level("Interface")
    def test_get_crc_interface(self):
        """
        Validate ``GetCrc`` interface

        [10] getCrc(sectorID) → CRCs
        """
        sector_id = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getCrc request with sectorID=0x0000")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.get_crc_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index,
            sector_id=sector_id)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.get_crc_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCrcResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.GetCrcResponseChecker.check_fields(
            self, response, self.feature_8100.get_crc_response_cls)

        self.testCaseChecked("INT_8100_0009", _AUTHOR)
    # end def test_get_crc_interface

    @features("Feature8100")
    @level("Interface")
    def test_get_active_profile_resolution_interface(self):
        """
        Validate ``GetActiveProfileResolution`` interface

        [11] getActiveProfileResolution() → resolutionIndex
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetActiveProfileResolution request")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.get_active_profile_resolution_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.get_active_profile_resolution_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the returned resolutionIndex is as same as the product default setting")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.GetActiveProfileResolutionResponseChecker.check_fields(
            self, response, self.feature_8100.get_active_profile_resolution_response_cls)

        self.testCaseChecked("INT_8100_0010", _AUTHOR)
    # end def test_get_active_profile_resolution_interface

    @features("Feature8100")
    @level("Interface")
    def test_set_active_profile_resolution_interface(self):
        """
        Validate ``SetActiveProfileResolution`` interface

        [12] setActiveProfileResolution(resolutionIndex)
        """
        self.post_requisite_reload_nvs = True
        resolution_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setActiveProfileResolution request with resolutionIndex={resolution_index}")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.set_active_profile_resolution_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index,
            resolution_index=resolution_index)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.set_active_profile_resolution_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetActiveProfileResolutionResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, request.deviceIndex),
            "featureIndex": (checker.check_feature_index, request.featureIndex),
        }
        checker.check_fields(self, response, self.feature_8100.set_active_profile_resolution_response_cls, check_map)

        self.testCaseChecked("INT_8100_0011", _AUTHOR)
    # end def test_set_active_profile_resolution_interface

    @features("Feature8100v1")
    @level("Interface")
    def test_get_profile_fields_list_interface(self):
        """
        Validate ``GetProfileFieldsList`` interface

        [13] getProfileFieldsList() → fieldsList
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetProfileFieldsList request")
        # --------------------------------------------------------------------------------------------------------------
        request = self.feature_8100.get_profile_fields_list_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8100_index)
        response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8100.get_profile_fields_list_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the returned fieldsList is as same as the product setting")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.GetProfileFieldsListResponseChecker.check_fields(
            self, response, self.feature_8100.get_profile_fields_list_response_cls)

        self.testCaseChecked("INT_8100_0012", _AUTHOR)
    # end def test_get_profile_fields_list_interface
# end class OnboardProfilesInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
