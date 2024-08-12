#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.test.onboardprofiles_test
:brief: HID++ 2.0 ``OnboardProfiles`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.onboardprofiles import ActiveProfileResolutionChangedEvent
from pyhid.hidpp.features.gaming.onboardprofiles import EndWrite
from pyhid.hidpp.features.gaming.onboardprofiles import EndWriteResponse
from pyhid.hidpp.features.gaming.onboardprofiles import ExecuteMacro
from pyhid.hidpp.features.gaming.onboardprofiles import ExecuteMacroResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetActiveProfile
from pyhid.hidpp.features.gaming.onboardprofiles import GetActiveProfileResolution
from pyhid.hidpp.features.gaming.onboardprofiles import GetActiveProfileResolutionResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetActiveProfileResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetCrc
from pyhid.hidpp.features.gaming.onboardprofiles import GetCrcResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetOnboardMode
from pyhid.hidpp.features.gaming.onboardprofiles import GetOnboardModeResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetOnboardProfilesInfo
from pyhid.hidpp.features.gaming.onboardprofiles import GetOnboardProfilesInfoResponseV0
from pyhid.hidpp.features.gaming.onboardprofiles import GetOnboardProfilesInfoResponseV1
from pyhid.hidpp.features.gaming.onboardprofiles import GetProfileFieldsList
from pyhid.hidpp.features.gaming.onboardprofiles import GetProfileFieldsListResponse
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfilesFactory
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfilesV0
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfilesV1
from pyhid.hidpp.features.gaming.onboardprofiles import ProfileActivatedEvent
from pyhid.hidpp.features.gaming.onboardprofiles import ReadData
from pyhid.hidpp.features.gaming.onboardprofiles import ReadDataResponse
from pyhid.hidpp.features.gaming.onboardprofiles import SetActiveProfile
from pyhid.hidpp.features.gaming.onboardprofiles import SetActiveProfileResolution
from pyhid.hidpp.features.gaming.onboardprofiles import SetActiveProfileResolutionResponse
from pyhid.hidpp.features.gaming.onboardprofiles import SetActiveProfileResponse
from pyhid.hidpp.features.gaming.onboardprofiles import SetOnboardMode
from pyhid.hidpp.features.gaming.onboardprofiles import SetOnboardModeResponse
from pyhid.hidpp.features.gaming.onboardprofiles import StartWrite
from pyhid.hidpp.features.gaming.onboardprofiles import StartWriteResponse
from pyhid.hidpp.features.gaming.onboardprofiles import WriteData
from pyhid.hidpp.features.gaming.onboardprofiles import WriteDataResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OnboardProfilesInstantiationTestCase(TestCase):
    """
    Test ``OnboardProfiles`` testing classes instantiations
    """
    @staticmethod
    def test_onboard_profiles():
        """
        Test ``OnboardProfiles`` class instantiation
        """
        my_class = OnboardProfiles(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = OnboardProfiles(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_onboard_profiles

    @staticmethod
    def test_get_onboard_profiles_info():
        """
        Test ``GetOnboardProfilesInfo`` class instantiation
        """
        my_class = GetOnboardProfilesInfo(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetOnboardProfilesInfo(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_onboard_profiles_info

    @staticmethod
    def test_get_onboard_profiles_info_response_v0():
        """
        Test ``GetOnboardProfilesInfoResponse`` class instantiation
        """
        my_class = GetOnboardProfilesInfoResponseV0(device_index=0, feature_index=0,
                                                    memory_model_id=0,
                                                    profile_format_id=0,
                                                    macro_format_id=0,
                                                    profile_count=0,
                                                    profile_count_oob=0,
                                                    button_count=0,
                                                    sector_count=0,
                                                    sector_size=0,
                                                    mechanical_layout=0,
                                                    various_info=0,
                                                    sector_count_rule=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetOnboardProfilesInfoResponseV0(device_index=0xff, feature_index=0xff,
                                                    memory_model_id=0xff,
                                                    profile_format_id=0xff,
                                                    macro_format_id=0xff,
                                                    profile_count=0xff,
                                                    profile_count_oob=0xff,
                                                    button_count=0xff,
                                                    sector_count=0xff,
                                                    sector_size=0xffff,
                                                    mechanical_layout=0xff,
                                                    various_info=0xff,
                                                    sector_count_rule=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_onboard_profiles_info_response_v0

    @staticmethod
    def test_get_onboard_profiles_info_response_v1():
        """
        Tests ``GetOnboardProfilesInfoResponse`` class instantiation
        """
        my_class = GetOnboardProfilesInfoResponseV1(device_index=0, feature_index=0,
                                                    memory_model_id=0,
                                                    profile_format_id=0,
                                                    macro_format_id=0,
                                                    profile_count=0,
                                                    profile_count_oob=0,
                                                    button_count=0,
                                                    sector_count=0,
                                                    sector_size=0,
                                                    mechanical_layout=0,
                                                    various_info=0,
                                                    sector_count_rule=0,
                                                    supported_host_layer=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetOnboardProfilesInfoResponseV1(device_index=0xff, feature_index=0xff,
                                                    memory_model_id=0xff,
                                                    profile_format_id=0xff,
                                                    macro_format_id=0xff,
                                                    profile_count=0xff,
                                                    profile_count_oob=0xff,
                                                    button_count=0xff,
                                                    sector_count=0xff,
                                                    sector_size=0xff,
                                                    mechanical_layout=0xff,
                                                    various_info=0xff,
                                                    sector_count_rule=0xff,
                                                    supported_host_layer=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_onboard_profiles_info_response_v1

    @staticmethod
    def test_set_onboard_mode():
        """
        Test ``SetOnboardMode`` class instantiation
        """
        my_class = SetOnboardMode(device_index=0, feature_index=0,
                                  onboard_mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetOnboardMode(device_index=0xff, feature_index=0xff,
                                  onboard_mode=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_onboard_mode

    @staticmethod
    def test_set_onboard_mode_response():
        """
        Test ``SetOnboardModeResponse`` class instantiation
        """
        my_class = SetOnboardModeResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetOnboardModeResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_onboard_mode_response

    @staticmethod
    def test_get_onboard_mode():
        """
        Test ``GetOnboardMode`` class instantiation
        """
        my_class = GetOnboardMode(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetOnboardMode(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_onboard_mode

    @staticmethod
    def test_get_onboard_mode_response():
        """
        Test ``GetOnboardModeResponse`` class instantiation
        """
        my_class = GetOnboardModeResponse(device_index=0, feature_index=0,
                                          onboard_mode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetOnboardModeResponse(device_index=0xff, feature_index=0xff,
                                          onboard_mode=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_onboard_mode_response

    @staticmethod
    def test_set_active_profile():
        """
        Test ``SetActiveProfile`` class instantiation
        """
        my_class = SetActiveProfile(device_index=0, feature_index=0,
                                    profile_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetActiveProfile(device_index=0xff, feature_index=0xff,
                                    profile_id=0xffff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_active_profile

    @staticmethod
    def test_set_active_profile_response():
        """
        Test ``SetActiveProfileResponse`` class instantiation
        """
        my_class = SetActiveProfileResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetActiveProfileResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_active_profile_response

    @staticmethod
    def test_get_active_profile():
        """
        Test ``GetActiveProfile`` class instantiation
        """
        my_class = GetActiveProfile(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetActiveProfile(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_active_profile

    @staticmethod
    def test_get_active_profile_response():
        """
        Test ``GetActiveProfileResponse`` class instantiation
        """
        my_class = GetActiveProfileResponse(device_index=0, feature_index=0,
                                            profile_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetActiveProfileResponse(device_index=0xff, feature_index=0xff,
                                            profile_id=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_active_profile_response

    @staticmethod
    def test_read_data():
        """
        Test ``ReadData`` class instantiation
        """
        my_class = ReadData(device_index=0, feature_index=0,
                            sector_id=0,
                            sub_address=0,
                            read_count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadData(device_index=0xff, feature_index=0xff,
                            sector_id=0xffff,
                            sub_address=0xffff,
                            read_count=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_data

    @staticmethod
    def test_read_data_response():
        """
        Test ``ReadDataResponse`` class instantiation
        """
        my_class = ReadDataResponse(
            device_index=0, feature_index=0,
            data=HexList('00' * (ReadDataResponse.LEN.DATA // 8)))


        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadDataResponse(
            device_index=0xff, feature_index=0xff,
            data=HexList('FF' * (ReadDataResponse.LEN.DATA // 8)))


        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_data_response

    @staticmethod
    def test_start_write():
        """
        Test ``StartWrite`` class instantiation
        """
        my_class = StartWrite(device_index=0, feature_index=0,
                              sector_id=0,
                              sub_address=0,
                              write_count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartWrite(device_index=0xff, feature_index=0xff,
                              sector_id=0xffff,
                              sub_address=0xffff,
                              write_count=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_write

    @staticmethod
    def test_start_write_response():
        """
        Test ``StartWriteResponse`` class instantiation
        """
        my_class = StartWriteResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartWriteResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_write_response

    @staticmethod
    def test_write_data():
        """
        Test ``WriteData`` class instantiation
        """
        my_class = WriteData(
            device_index=0, feature_index=0,
            data=HexList('00' * (WriteData.LEN.DATA // 8)))


        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteData(
            device_index=0xff, feature_index=0xff,
            data=HexList('FF' * (WriteData.LEN.DATA // 8)))


        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_data

    @staticmethod
    def test_write_data_response():
        """
        Test ``WriteDataResponse`` class instantiation
        """
        my_class = WriteDataResponse(device_index=0, feature_index=0,
                                     frame_nb=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteDataResponse(device_index=0xff, feature_index=0xff,
                                     frame_nb=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_data_response

    @staticmethod
    def test_end_write():
        """
        Test ``EndWrite`` class instantiation
        """
        my_class = EndWrite(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = EndWrite(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_end_write

    @staticmethod
    def test_end_write_response():
        """
        Test ``EndWriteResponse`` class instantiation
        """
        my_class = EndWriteResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EndWriteResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_end_write_response

    @staticmethod
    def test_execute_macro():
        """
        Test ``ExecuteMacro`` class instantiation
        """
        my_class = ExecuteMacro(device_index=0, feature_index=0,
                                sector_id=0,
                                sub_address=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ExecuteMacro(device_index=0xff, feature_index=0xff,
                                sector_id=0xffff,
                                sub_address=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_execute_macro

    @staticmethod
    def test_execute_macro_response():
        """
        Test ``ExecuteMacroResponse`` class instantiation
        """
        my_class = ExecuteMacroResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ExecuteMacroResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_execute_macro_response

    @staticmethod
    def test_get_crc():
        """
        Test ``GetCrc`` class instantiation
        """
        my_class = GetCrc(device_index=0, feature_index=0,
                          sector_id=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCrc(device_index=0xff, feature_index=0xff,
                          sector_id=0xffff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_crc

    @staticmethod
    def test_get_crc_response():
        """
        Test ``GetCrcResponse`` class instantiation
        """
        my_class = GetCrcResponse(device_index=0, feature_index=0,
                                  crc_1=0,
                                  crc_2=0,
                                  crc_3=0,
                                  crc_4=0,
                                  crc_5=0,
                                  crc_6=0,
                                  crc_7=0,
                                  crc_8=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCrcResponse(device_index=0xff, feature_index=0xff,
                                  crc_1=0xffff,
                                  crc_2=0xffff,
                                  crc_3=0xffff,
                                  crc_4=0xffff,
                                  crc_5=0xffff,
                                  crc_6=0xffff,
                                  crc_7=0xffff,
                                  crc_8=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_crc_response

    @staticmethod
    def test_get_active_profile_resolution():
        """
        Test ``GetActiveProfileResolution`` class instantiation
        """
        my_class = GetActiveProfileResolution(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetActiveProfileResolution(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_active_profile_resolution

    @staticmethod
    def test_get_active_profile_resolution_response():
        """
        Test ``GetActiveProfileResolutionResponse`` class instantiation
        """
        my_class = GetActiveProfileResolutionResponse(device_index=0, feature_index=0,
                                                      resolution_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetActiveProfileResolutionResponse(device_index=0xff, feature_index=0xff,
                                                      resolution_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_active_profile_resolution_response

    @staticmethod
    def test_set_active_profile_resolution():
        """
        Test ``SetActiveProfileResolution`` class instantiation
        """
        my_class = SetActiveProfileResolution(device_index=0, feature_index=0,
                                              resolution_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetActiveProfileResolution(device_index=0xff, feature_index=0xff,
                                              resolution_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_active_profile_resolution

    @staticmethod
    def test_set_active_profile_resolution_response():
        """
        Test ``SetActiveProfileResolutionResponse`` class instantiation
        """
        my_class = SetActiveProfileResolutionResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetActiveProfileResolutionResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_active_profile_resolution_response

    @staticmethod
    def test_get_profile_fields_list():
        """
        Test ``GetProfileFieldsList`` class instantiation
        """
        my_class = GetProfileFieldsList(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetProfileFieldsList(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_profile_fields_list

    @staticmethod
    def test_get_profile_fields_list_response():
        """
        Test ``GetProfileFieldsListResponse`` class instantiation
        """
        my_class = GetProfileFieldsListResponse(
            device_index=0, feature_index=0,
            fields_list=HexList('00' * (GetProfileFieldsListResponse.LEN.FIELDS_LIST // 8)))


        RootTestCase._long_function_class_checker(my_class)

        my_class = GetProfileFieldsListResponse(
            device_index=0xff, feature_index=0xff,
            fields_list=HexList('FF' * (GetProfileFieldsListResponse.LEN.FIELDS_LIST // 8)))


        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_profile_fields_list_response

    @staticmethod
    def test_profile_activated_event():
        """
        Test ``ProfileActivatedEvent`` class instantiation
        """
        my_class = ProfileActivatedEvent(device_index=0, feature_index=0,
                                         profile_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ProfileActivatedEvent(device_index=0xff, feature_index=0xff,
                                         profile_id=0xffff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_profile_activated_event

    @staticmethod
    def test_active_profile_resolution_changed_event():
        """
        Test ``ActiveProfileResolutionChangedEvent`` class instantiation
        """
        my_class = ActiveProfileResolutionChangedEvent(device_index=0, feature_index=0,
                                                       resolution_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ActiveProfileResolutionChangedEvent(device_index=0xff, feature_index=0xff,
                                                       resolution_index=0x0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_active_profile_resolution_changed_event
# end class OnboardProfilesInstantiationTestCase


class OnboardProfilesTestCase(TestCase):
    """
    Test ``OnboardProfiles`` factory feature
    """
    @classmethod
    def setUpClass(cls):
        cls.expected = {
            OnboardProfilesV0.VERSION: {
                "cls": OnboardProfilesV0,
                "interfaces": {
                    "get_onboard_profiles_info_cls": GetOnboardProfilesInfo,
                    "get_onboard_profiles_info_response_cls": GetOnboardProfilesInfoResponseV0,
                    "set_onboard_mode_cls": SetOnboardMode,
                    "set_onboard_mode_response_cls": SetOnboardModeResponse,
                    "get_onboard_mode_cls": GetOnboardMode,
                    "get_onboard_mode_response_cls": GetOnboardModeResponse,
                    "set_active_profile_cls": SetActiveProfile,
                    "set_active_profile_response_cls": SetActiveProfileResponse,
                    "get_active_profile_cls": GetActiveProfile,
                    "get_active_profile_response_cls": GetActiveProfileResponse,
                    "read_data_cls": ReadData,
                    "read_data_response_cls": ReadDataResponse,
                    "start_write_cls": StartWrite,
                    "start_write_response_cls": StartWriteResponse,
                    "write_data_cls": WriteData,
                    "write_data_response_cls": WriteDataResponse,
                    "end_write_cls": EndWrite,
                    "end_write_response_cls": EndWriteResponse,
                    "execute_macro_cls": ExecuteMacro,
                    "execute_macro_response_cls": ExecuteMacroResponse,
                    "get_crc_cls": GetCrc,
                    "get_crc_response_cls": GetCrcResponse,
                    "get_active_profile_resolution_cls": GetActiveProfileResolution,
                    "get_active_profile_resolution_response_cls": GetActiveProfileResolutionResponse,
                    "set_active_profile_resolution_cls": SetActiveProfileResolution,
                    "set_active_profile_resolution_response_cls": SetActiveProfileResolutionResponse,
                    "profile_activated_event_cls": ProfileActivatedEvent,
                    "active_profile_resolution_changed_event_cls": ActiveProfileResolutionChangedEvent,
                },
                "max_function_index": 12
            },
            OnboardProfilesV1.VERSION: {
                "cls": OnboardProfilesV1,
                "interfaces": {
                    "get_onboard_profiles_info_cls": GetOnboardProfilesInfo,
                    "get_onboard_profiles_info_response_cls": GetOnboardProfilesInfoResponseV1,
                    "set_onboard_mode_cls": SetOnboardMode,
                    "set_onboard_mode_response_cls": SetOnboardModeResponse,
                    "get_onboard_mode_cls": GetOnboardMode,
                    "get_onboard_mode_response_cls": GetOnboardModeResponse,
                    "set_active_profile_cls": SetActiveProfile,
                    "set_active_profile_response_cls": SetActiveProfileResponse,
                    "get_active_profile_cls": GetActiveProfile,
                    "get_active_profile_response_cls": GetActiveProfileResponse,
                    "read_data_cls": ReadData,
                    "read_data_response_cls": ReadDataResponse,
                    "start_write_cls": StartWrite,
                    "start_write_response_cls": StartWriteResponse,
                    "write_data_cls": WriteData,
                    "write_data_response_cls": WriteDataResponse,
                    "end_write_cls": EndWrite,
                    "end_write_response_cls": EndWriteResponse,
                    "execute_macro_cls": ExecuteMacro,
                    "execute_macro_response_cls": ExecuteMacroResponse,
                    "get_crc_cls": GetCrc,
                    "get_crc_response_cls": GetCrcResponse,
                    "get_active_profile_resolution_cls": GetActiveProfileResolution,
                    "get_active_profile_resolution_response_cls": GetActiveProfileResolutionResponse,
                    "set_active_profile_resolution_cls": SetActiveProfileResolution,
                    "set_active_profile_resolution_response_cls": SetActiveProfileResolutionResponse,
                    "get_profile_fields_list_cls": GetProfileFieldsList,
                    "get_profile_fields_list_response_cls": GetProfileFieldsListResponse,
                    "profile_activated_event_cls": ProfileActivatedEvent,
                    "active_profile_resolution_changed_event_cls": ActiveProfileResolutionChangedEvent,
                },
                "max_function_index": 13
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``OnboardProfilesFactory``
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(OnboardProfilesFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``OnboardProfilesFactory`` with out of range versions
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                OnboardProfilesFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``OnboardProfilesFactory`` returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            obj = OnboardProfilesFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(obj, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(obj, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check ``get_max_function_index`` returns correct value at each version
        """
        for version, expected in self.expected.items():
            obj = OnboardProfilesFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class OnboardProfilesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
