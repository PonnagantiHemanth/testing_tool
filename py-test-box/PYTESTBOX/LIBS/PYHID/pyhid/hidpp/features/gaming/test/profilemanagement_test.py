#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.gaming.test.profilemanagement_test
:brief: HID++ 2.0 ``ProfileManagement`` test module
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.gaming.profilemanagement import Configure
from pyhid.hidpp.features.gaming.profilemanagement import ConfigureResponse
from pyhid.hidpp.features.gaming.profilemanagement import EditBuffer
from pyhid.hidpp.features.gaming.profilemanagement import EditBufferResponse
from pyhid.hidpp.features.gaming.profilemanagement import GetCapabilities
from pyhid.hidpp.features.gaming.profilemanagement import GetCapabilitiesResponse
from pyhid.hidpp.features.gaming.profilemanagement import GetError
from pyhid.hidpp.features.gaming.profilemanagement import GetErrorResponse
from pyhid.hidpp.features.gaming.profilemanagement import GetHashes
from pyhid.hidpp.features.gaming.profilemanagement import GetHashesResponse
from pyhid.hidpp.features.gaming.profilemanagement import GetProfileTagList
from pyhid.hidpp.features.gaming.profilemanagement import GetProfileTagListResponse
from pyhid.hidpp.features.gaming.profilemanagement import GetSetMode
from pyhid.hidpp.features.gaming.profilemanagement import GetSetModeResponse
from pyhid.hidpp.features.gaming.profilemanagement import GetSetPowerOnParams
from pyhid.hidpp.features.gaming.profilemanagement import GetSetPowerOnParamsResponse
from pyhid.hidpp.features.gaming.profilemanagement import Load
from pyhid.hidpp.features.gaming.profilemanagement import LoadResponse
from pyhid.hidpp.features.gaming.profilemanagement import ProfileChangeEvent
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagementFactory
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagementV0
from pyhid.hidpp.features.gaming.profilemanagement import ReadBuffer
from pyhid.hidpp.features.gaming.profilemanagement import ReadBufferResponse
from pyhid.hidpp.features.gaming.profilemanagement import Save
from pyhid.hidpp.features.gaming.profilemanagement import SaveResponse
from pyhid.hidpp.features.gaming.profilemanagement import StartWriteBuffer
from pyhid.hidpp.features.gaming.profilemanagement import StartWriteBufferResponse
from pyhid.hidpp.features.gaming.profilemanagement import WriteBuffer
from pyhid.hidpp.features.gaming.profilemanagement import WriteBufferResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProfileManagementInstantiationTestCase(TestCase):
    """
    Test ``ProfileManagement`` testing classes instantiations
    """

    @staticmethod
    def test_profile_management():
        """
        Test ``ProfileManagement`` class instantiation
        """
        my_class = ProfileManagement(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ProfileManagement(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_profile_management

    @staticmethod
    def test_get_capabilities():
        """
        Test ``GetCapabilities`` class instantiation
        """
        my_class = GetCapabilities(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetCapabilities(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_capabilities

    @staticmethod
    def test_get_capabilities_response():
        """
        Test ``GetCapabilitiesResponse`` class instantiation
        """
        my_class = GetCapabilitiesResponse(device_index=0, feature_index=0,
                                           file_system_ver=0,
                                           profile_tag_ver=0,
                                           max_sector_size=0,
                                           ram_buffer_size=0,
                                           max_sector_id=0,
                                           max_file_id=0,
                                           max_directory_sector_id=0,
                                           total_flash_size_kb=0,
                                           flash_erase_counter=0,
                                           flash_life_expect=0,
                                           num_onboard_profiles=0,
                                           opcode=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetCapabilitiesResponse(
            device_index=0xff,
            feature_index=0xff,
            file_system_ver=0xff,
            profile_tag_ver=0xff,
            max_sector_size=HexList('FF' * (GetCapabilitiesResponse.LEN.MAX_SECTOR_SIZE // 8)),
            ram_buffer_size=HexList('FF' * (GetCapabilitiesResponse.LEN.RAM_BUFFER_SIZE // 8)),
            max_sector_id=0xff,
            max_file_id=0xff,
            max_directory_sector_id=0xff,
            total_flash_size_kb=0xff,
            flash_erase_counter=HexList('FF' * (GetCapabilitiesResponse.LEN.FLASH_ERASE_COUNTER // 8)),
            flash_life_expect=0xff,
            num_onboard_profiles=0xff,
            opcode=0x7)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_capabilities_response

    @staticmethod
    def test_get_profile_tag_list():
        """
        Test ``GetProfileTagList`` class instantiation
        """
        my_class = GetProfileTagList(device_index=0, feature_index=0,
                                     offset_bytes=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetProfileTagList(device_index=0xff, feature_index=0xff,
                                     offset_bytes=HexList('FF' * (GetProfileTagList.LEN.OFFSET_BYTES // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_profile_tag_list

    @staticmethod
    def test_get_profile_tag_list_response():
        """
        Test ``GetProfileTagListResponse`` class instantiation
        """
        my_class = GetProfileTagListResponse(device_index=0, feature_index=0,
                                             partial_tag_list=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetProfileTagListResponse(
            device_index=0xff, feature_index=0xff,
            partial_tag_list=HexList('FF' * (GetProfileTagListResponse.LEN.PARTIAL_TAG_LIST // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_profile_tag_list_response

    @staticmethod
    def test_start_write_buffer():
        """
        Test ``StartWriteBuffer`` class instantiation
        """
        my_class = StartWriteBuffer(device_index=0, feature_index=0,
                                    count=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = StartWriteBuffer(device_index=0xff, feature_index=0xff,
                                    count=HexList('FF' * (StartWriteBuffer.LEN.COUNT // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_start_write_buffer

    @staticmethod
    def test_start_write_buffer_response():
        """
        Test ``StartWriteBufferResponse`` class instantiation
        """
        my_class = StartWriteBufferResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = StartWriteBufferResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_write_buffer_response

    @staticmethod
    def test_write_buffer():
        """
        Test ``WriteBuffer`` class instantiation
        """
        my_class = WriteBuffer(device_index=0, feature_index=0, data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteBuffer(device_index=0xff, feature_index=0xff,
                               data=HexList('FF' * (WriteBuffer.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_buffer

    @staticmethod
    def test_write_buffer_response():
        """
        Test ``WriteBufferResponse`` class instantiation
        """
        my_class = WriteBufferResponse(device_index=0, feature_index=0, frame_num=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = WriteBufferResponse(device_index=0xff, feature_index=0xff,
                                       frame_num=HexList('FF' * (WriteBufferResponse.LEN.FRAME_NUM // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_write_buffer_response

    @staticmethod
    def test_get_error():
        """
        Test ``GetError`` class instantiation
        """
        my_class = GetError(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetError(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_error

    @staticmethod
    def test_get_error_response():
        """
        Test ``GetErrorResponse`` class instantiation
        """
        my_class = GetErrorResponse(device_index=0, feature_index=0,
                                    fs_error_code=0,
                                    fs_error_param_1=0,
                                    fs_error_param_2=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetErrorResponse(device_index=0xff, feature_index=0xff,
                                    fs_error_code=0xff,
                                    fs_error_param_1=HexList('FF' * (GetErrorResponse.LEN.FS_ERROR_PARAM_1 // 8)),
                                    fs_error_param_2=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_error_response

    @staticmethod
    def test_edit_buffer():
        """
        Test ``EditBuffer`` class instantiation
        """
        my_class = EditBuffer(device_index=0, feature_index=0,
                              count=0,
                              opcode=0,
                              address=0,
                              data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EditBuffer(device_index=0xff, feature_index=0xff,
                              count=0xf,
                              opcode=0x7,
                              address=HexList('FF' * (EditBuffer.LEN.ADDRESS // 8)),
                              data=HexList('FF' * (EditBuffer.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_edit_buffer

    @staticmethod
    def test_edit_buffer_response():
        """
        Test ``EditBufferResponse`` class instantiation
        """
        my_class = EditBufferResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = EditBufferResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_edit_buffer_response

    @staticmethod
    def test_get_set_mode():
        """
        Test ``GetSetMode`` class instantiation
        """
        my_class = GetSetMode(device_index=0, feature_index=0,
                              onboard_mode=0,
                              set_onboard_mode=0,
                              profile_mode=0,
                              set_profile_mode=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSetMode(device_index=0xff, feature_index=0xff,
                              onboard_mode=0x1,
                              set_onboard_mode=0x1,
                              profile_mode=0x1,
                              set_profile_mode=0x1)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_set_mode

    @staticmethod
    def test_get_set_mode_response():
        """
        Test ``GetSetModeResponse`` class instantiation
        """
        my_class = GetSetModeResponse(device_index=0, feature_index=0,
                                      onboard_mode=0,
                                      profile_mode=0,
                                      curr_profile_file_id=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSetModeResponse(
            device_index=0xff, feature_index=0xff, onboard_mode=0x1, profile_mode=0x1,
            curr_profile_file_id=HexList('FF' * (GetSetModeResponse.LEN.CURR_PROFILE_FILE_ID // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_set_mode_response

    @staticmethod
    def test_save():
        """
        Test ``Save`` class instantiation
        """
        my_class = Save(device_index=0, feature_index=0,
                        first_sector_id=0,
                        count=0,
                        hash32=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = Save(device_index=0xff, feature_index=0xff,
                        first_sector_id=HexList('FF' * (Save.LEN.FIRST_SECTOR_ID // 8)),
                        count=HexList('FF' * (Save.LEN.COUNT // 8)),
                        hash32=HexList('FF' * (Save.LEN.HASH32 // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_save

    @staticmethod
    def test_save_response():
        """
        Test ``SaveResponse`` class instantiation
        """
        my_class = SaveResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SaveResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_save_response

    @staticmethod
    def test_load():
        """
        Test ``Load`` class instantiation
        """
        my_class = Load(device_index=0, feature_index=0,
                        first_sector_id=0,
                        count=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = Load(device_index=0xff, feature_index=0xff,
                        first_sector_id=HexList('FF' * (Load.LEN.FIRST_SECTOR_ID // 8)),
                        count=HexList('FF' * (Load.LEN.COUNT // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_load

    @staticmethod
    def test_load_response():
        """
        Test ``LoadResponse`` class instantiation
        """
        my_class = LoadResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = LoadResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_load_response

    @staticmethod
    def test_configure():
        """
        Test ``Configure`` class instantiation
        """
        my_class = Configure(device_index=0, feature_index=0,
                             feature_id=0,
                             file_type_id=0,
                             file_id=0,
                             count=0,
                             hash_key=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = Configure(device_index=0xff, feature_index=0xff,
                             feature_id=HexList('FF' * (Configure.LEN.FEATURE_ID // 8)),
                             file_type_id=0x3,
                             file_id=0xffff,
                             count=HexList('FF' * (Configure.LEN.COUNT // 8)),
                             hash_key=HexList('FF' * (Configure.LEN.HASH_KEY // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_configure

    @staticmethod
    def test_configure_response():
        """
        Test ``ConfigureResponse`` class instantiation
        """
        my_class = ConfigureResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ConfigureResponse(device_index=0xff, feature_index=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_configure_response

    @staticmethod
    def test_get_set_power_on_params():
        """
        Test ``GetSetPowerOnParams`` class instantiation
        """
        my_class = GetSetPowerOnParams(device_index=0, feature_index=0,
                                       set_power_on_profile=0,
                                       power_on_profile=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSetPowerOnParams(device_index=0xff, feature_index=0xff,
                                       set_power_on_profile=0x1,
                                       power_on_profile=HexList('FF' * (GetSetPowerOnParams.LEN.POWER_ON_PROFILE // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_set_power_on_params

    @staticmethod
    def test_get_set_power_on_params_response():
        """
        Test ``GetSetPowerOnParamsResponse`` class instantiation
        """
        my_class = GetSetPowerOnParamsResponse(device_index=0, feature_index=0,
                                               power_on_profile=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSetPowerOnParamsResponse(
            device_index=0xff, feature_index=0xff,
            power_on_profile=HexList('FF' * (GetSetPowerOnParamsResponse.LEN.POWER_ON_PROFILE // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_set_power_on_params_response

    @staticmethod
    def test_get_hashes():
        """
        Test ``GetHashes`` class instantiation
        """
        my_class = GetHashes(device_index=0, feature_index=0,
                             compute=0,
                             file_id_0=0,
                             file_id_1=0,
                             file_id_2=0,
                             file_id_3=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHashes(device_index=0xff, feature_index=0xff,
                             compute=0x1,
                             file_id_0=0xff,
                             file_id_1=0xff,
                             file_id_2=0xff,
                             file_id_3=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_hashes

    @staticmethod
    def test_get_hashes_response():
        """
        Test ``GetHashesResponse`` class instantiation
        """
        my_class = GetHashesResponse(device_index=0, feature_index=0,
                                     hash_0=0,
                                     hash_1=0,
                                     hash_2=0,
                                     hash_3=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetHashesResponse(device_index=0xff, feature_index=0xff,
                                     hash_0=HexList('FF' * (GetHashesResponse.LEN.HASH_0 // 8)),
                                     hash_1=HexList('FF' * (GetHashesResponse.LEN.HASH_1 // 8)),
                                     hash_2=HexList('FF' * (GetHashesResponse.LEN.HASH_2 // 8)),
                                     hash_3=HexList('FF' * (GetHashesResponse.LEN.HASH_3 // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_hashes_response

    @staticmethod
    def test_read_buffer():
        """
        Test ``ReadBuffer`` class instantiation
        """
        my_class = ReadBuffer(device_index=0, feature_index=0,
                              offset_bytes=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = ReadBuffer(device_index=0xff, feature_index=0xff,
                              offset_bytes=HexList('FF' * (ReadBuffer.LEN.OFFSET_BYTES // 8)))

        RootTestCase._short_function_class_checker(my_class)
    # end def test_read_buffer

    @staticmethod
    def test_read_buffer_response():
        """
        Test ``ReadBufferResponse`` class instantiation
        """
        my_class = ReadBufferResponse(device_index=0, feature_index=0,
                                      data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ReadBufferResponse(device_index=0xff, feature_index=0xff,
                                      data=HexList('FF' * (ReadBufferResponse.LEN.DATA // 8)))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_read_buffer_response

    @staticmethod
    def test_profile_change_event():
        """
        Test ``ProfileChangeEvent`` class instantiation
        """
        my_class = ProfileChangeEvent(device_index=0, feature_index=0,
                                      new_profile=0,
                                      failure=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = ProfileChangeEvent(device_index=0xff, feature_index=0xff,
                                      new_profile=HexList('FF' * (ProfileChangeEvent.LEN.NEW_PROFILE // 8)),
                                      failure=0x1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_profile_change_event
# end class ProfileManagementInstantiationTestCase


class ProfileManagementTestCase(TestCase):
    """
    Test ``ProfileManagement`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            ProfileManagementV0.VERSION: {
                "cls": ProfileManagementV0,
                "interfaces": {
                    "get_capabilities_cls": GetCapabilities,
                    "get_capabilities_response_cls": GetCapabilitiesResponse,
                    "get_profile_tag_list_cls": GetProfileTagList,
                    "get_profile_tag_list_response_cls": GetProfileTagListResponse,
                    "start_write_buffer_cls": StartWriteBuffer,
                    "start_write_buffer_response_cls": StartWriteBufferResponse,
                    "write_buffer_cls": WriteBuffer,
                    "write_buffer_response_cls": WriteBufferResponse,
                    "get_error_cls": GetError,
                    "get_error_response_cls": GetErrorResponse,
                    "edit_buffer_cls": EditBuffer,
                    "edit_buffer_response_cls": EditBufferResponse,
                    "get_set_mode_cls": GetSetMode,
                    "get_set_mode_response_cls": GetSetModeResponse,
                    "save_cls": Save,
                    "save_response_cls": SaveResponse,
                    "load_cls": Load,
                    "load_response_cls": LoadResponse,
                    "configure_cls": Configure,
                    "configure_response_cls": ConfigureResponse,
                    "get_set_power_on_params_cls": GetSetPowerOnParams,
                    "get_set_power_on_params_response_cls": GetSetPowerOnParamsResponse,
                    "get_hashes_cls": GetHashes,
                    "get_hashes_response_cls": GetHashesResponse,
                    "read_buffer_cls": ReadBuffer,
                    "read_buffer_response_cls": ReadBufferResponse,
                    "profile_change_event_cls": ProfileChangeEvent,
                },
                "max_function_index": 12
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``ProfileManagementFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ProfileManagementFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``ProfileManagementFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                ProfileManagementFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``ProfileManagementFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = ProfileManagementFactory.create(version)
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

        :raise ``AssertionError``: Assert max_function_index that raise an exception
        """
        for version, expected in self.expected.items():
            obj = ProfileManagementFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ProfileManagementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
