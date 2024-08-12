#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.profilemanagementutils
:brief: Helpers for ``ProfileManagement`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from copy import deepcopy
from enum import IntEnum
from enum import unique

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.gaming.profilemanagement import GetProfileTagListResponse
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagementFactory
from pyhid.hidpp.features.gaming.profilemanagement import WriteBuffer
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import DirectoryFile
from pylibrary.mcu.fkcprofileformat import OobProfile
from pylibrary.mcu.fkcprofileformat import PROFILE_TAG_INFO_MAP
from pylibrary.mcu.fkcprofileformat import Profile
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProfileManagementTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ProfileManagement`` feature
    """

    @unique
    class RequestType(IntEnum):
        """
        Request type for functions (GetSetMode, GetSetPowerOnParams)
        """
        GET = 0
        SET = 1
    # end class RequestType

    class EditBufferCapabilitiesChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``EditBufferCapabilities``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "opcode": (
                    cls.check_opcode,
                    config.F_EditBufferCapabilities)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: EditBufferCapabilities to check
            :type bitmap: ``ProfileManagement.EditBufferCapabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_opcode(test_case, bitmap, expected):
            """
            Check opcode field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: EditBufferCapabilities to check
            :type bitmap: ``ProfileManagement.EditBufferCapabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert opcode that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.opcode),
                msg="The opcode parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.opcode})")
        # end def check_opcode
    # end class EditBufferCapabilitiesChecker

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT
            return {
                "file_system_ver": (
                    cls.check_file_system_ver,
                    config.F_FileSystemVersion),
                "profile_tag_ver": (
                    cls.check_profile_tag_ver,
                    config.F_ProfileTagVersion),
                "max_sector_size": (
                    cls.check_max_sector_size,
                    int(config.F_MaxSectorSize)),
                "ram_buffer_size": (
                    cls.check_ram_buffer_size,
                    int(config.F_RamBufferSize)),
                "max_sector_id": (
                    cls.check_max_sector_id,
                    int(config.F_MaxSectorId)),
                "max_file_id": (
                    cls.check_max_file_id,
                    int(config.F_MaxFileId)),
                "max_directory_sector_id": (
                    cls.check_max_directory_sector_id,
                    config.F_MaxDirectorySectorId),
                "total_flash_size_kb": (
                    cls.check_total_flash_size_kb,
                    int(config.F_TotalFlashSizeKb)),
                "flash_erase_counter": (
                    cls.check_flash_erase_counter,
                    config.F_FlashEraseCounter),
                "flash_life_expect": (
                    cls.check_flash_life_expect,
                    config.F_FlashLifeExpect),
                "num_onboard_profiles": (
                    cls.check_num_onboard_profiles,
                    config.F_NumOnboardProfiles),
                "edit_buffer_capabilities": (
                    cls.check_edit_buffer_capabilities,
                    ProfileManagementTestUtils.EditBufferCapabilitiesChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_file_system_ver(test_case, response, expected):
            """
            Check file_system_ver field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert file_system_ver that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.file_system_ver),
                msg="The file_system_ver parameter differs "
                    f"(expected:{expected}, obtained:{response.file_system_ver})")
        # end def check_file_system_ver

        @staticmethod
        def check_profile_tag_ver(test_case, response, expected):
            """
            Check profile_tag_ver field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert profile_tag_ver that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.profile_tag_ver),
                msg="The profile_tag_ver parameter differs "
                    f"(expected:{expected}, obtained:{response.profile_tag_ver})")
        # end def check_profile_tag_ver

        @staticmethod
        def check_max_sector_size(test_case, response, expected):
            """
            Check max_sector_size field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert max_sector_size that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.max_sector_size),
                msg="The max_sector_size parameter differs "
                    f"(expected:{expected}, obtained:{response.max_sector_size})")
        # end def check_max_sector_size

        @staticmethod
        def check_ram_buffer_size(test_case, response, expected):
            """
            Check ram_buffer_size field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert ram_buffer_size that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.ram_buffer_size),
                msg="The ram_buffer_size parameter differs "
                    f"(expected:{expected}, obtained:{response.ram_buffer_size})")
        # end def check_ram_buffer_size

        @staticmethod
        def check_max_sector_id(test_case, response, expected):
            """
            Check max_sector_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert max_sector_id that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.max_sector_id),
                msg="The max_sector_id parameter differs "
                    f"(expected:{expected}, obtained:{response.max_sector_id})")
        # end def check_max_sector_id

        @staticmethod
        def check_max_file_id(test_case, response, expected):
            """
            Check max_file_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert max_file_id that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.max_file_id),
                msg="The max_file_id parameter differs "
                    f"(expected:{expected}, obtained:{response.max_file_id})")
        # end def check_max_file_id

        @staticmethod
        def check_max_directory_sector_id(test_case, response, expected):
            """
            Check max_directory_sector_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert max_directory_sector_id that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.max_directory_sector_id),
                msg="The max_directory_sector_id parameter differs "
                    f"(expected:{expected}, obtained:{response.max_directory_sector_id})")
        # end def check_max_directory_sector_id

        @staticmethod
        def check_total_flash_size_kb(test_case, response, expected):
            """
            Check total_flash_size_kb field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert total_flash_size_kb that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.total_flash_size_kb),
                msg="The total_flash_size_kb parameter differs "
                    f"(expected:{expected}, obtained:{response.total_flash_size_kb})")
        # end def check_total_flash_size_kb

        @staticmethod
        def check_flash_erase_counter(test_case, response, expected):
            """
            Check flash_erase_counter field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert flash_erase_counter that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.flash_erase_counter),
                msg="The flash_erase_counter parameter differs "
                    f"(expected:{expected}, obtained:{response.flash_erase_counter})")
        # end def check_flash_erase_counter

        @staticmethod
        def check_flash_life_expect(test_case, response, expected):
            """
            Check flash_life_expect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert flash_life_expect that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.flash_life_expect),
                msg="The flash_life_expect parameter differs "
                    f"(expected:{expected}, obtained:{response.flash_life_expect})")
        # end def check_flash_life_expect

        @staticmethod
        def check_num_onboard_profiles(test_case, response, expected):
            """
            Check num_onboard_profiles field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert num_onboard_profiles that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.num_onboard_profiles),
                msg="The num_onboard_profiles parameter differs "
                    f"(expected:{expected}, obtained:{response.num_onboard_profiles})")
        # end def check_num_onboard_profiles

        @staticmethod
        def check_edit_buffer_capabilities(test_case, message, expected):
            """
            Check ``edit_buffer_capabilities``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetCapabilitiesResponse to check
            :type message: ``pyhid.hidpp.features.gaming.profilemanagement.GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ProfileManagementTestUtils.EditBufferCapabilitiesChecker.check_fields(
                test_case, message.edit_buffer_capabilities, ProfileManagement.EditBufferCapabilities, expected)
        # end def check_edit_buffer_capabilities
    # end class GetCapabilitiesResponseChecker

    class GetProfileTagListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetProfileTagListResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case=test_case, offset_bytes=0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, offset_bytes):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param offset_bytes: This is the offset, in bytes, into the profile tag list at which to read the data.
            :type offset_bytes: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            len_of_partial_tag_list = int(GetProfileTagListResponse.LEN.PARTIAL_TAG_LIST/8)
            config = test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT
            end_pos_shift = len_of_partial_tag_list \
                if ((sum([len(tag) for tag in config.F_TagList]) / 2) - offset_bytes) >= len_of_partial_tag_list \
                else int(sum([len(tag) for tag in config.F_TagList]) / 2) - offset_bytes + 1
            expected_tag_list_data = ''.join(config.F_TagList)[offset_bytes * 2: (offset_bytes + end_pos_shift)*2]
            expected_tag_list_data = expected_tag_list_data if end_pos_shift == len_of_partial_tag_list \
                else expected_tag_list_data + '00' * (len_of_partial_tag_list - (end_pos_shift - 1))
            return {
                "partial_tag_list": (
                    cls.check_partial_tag_list, expected_tag_list_data)
            }
        # end def get_check_map

        @staticmethod
        def check_partial_tag_list(test_case, response, expected):
            """
            Check partial_tag_list field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetProfileTagListResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetProfileTagListResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert partial_tag_list that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.partial_tag_list),
                msg="The partial_tag_list parameter differs "
                    f"(expected:{expected}, obtained:{response.partial_tag_list})")
        # end def check_partial_tag_list
    # end class GetProfileTagListResponseChecker

    class WriteBufferResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``WriteBufferResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(frame_num=1)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, frame_num):
            """
            Get the check methods and expected values

            :param frame_num: Frame number
            :type frame_num: ``init``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "frame_num": (
                    cls.check_frame_num,
                    frame_num)
            }
        # end def get_check_map

        @staticmethod
        def check_frame_num(test_case, response, expected):
            """
            Check frame_num field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: WriteBufferResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.WriteBufferResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert frame_num that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.frame_num),
                msg="The frame_num parameter differs "
                    f"(expected:{expected}, obtained:{response.frame_num})")
        # end def check_frame_num
    # end class WriteBufferResponseChecker

    class GetErrorResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetErrorResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "fs_error_code": (
                    cls.check_fs_error_code, 0),
                "fs_error_param_1": (
                    cls.check_fs_error_param_1, 0),
                "fs_error_param_2": (
                    cls.check_fs_error_param_2, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_fs_error_code(test_case, response, expected):
            """
            Check fs_error_code field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetErrorResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetErrorResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fs_error_code that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.fs_error_code),
                msg="The fs_error_code parameter differs "
                    f"(expected:{expected}, obtained:{response.fs_error_code})")
        # end def check_fs_error_code

        @staticmethod
        def check_fs_error_param_1(test_case, response, expected):
            """
            Check fs_error_param_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetErrorResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetErrorResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fs_error_param_1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.fs_error_param_1),
                msg="The fs_error_param_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.fs_error_param_1})")
        # end def check_fs_error_param_1

        @staticmethod
        def check_fs_error_param_2(test_case, response, expected):
            """
            Check fs_error_param_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetErrorResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetErrorResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert fs_error_param_2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.fs_error_param_2),
                msg="The fs_error_param_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.fs_error_param_2})")
        # end def check_fs_error_param_2
    # end class GetErrorResponseChecker

    class OperatingModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``OperatingModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "onboard_mode": (
                    cls.check_onboard_mode,
                    ProfileManagement.Mode.ONBOARD_MODE),
                'profile_mode': (
                    cls.check_profile_mode,
                    ProfileManagement.ProfileMode.HW_SW_CONTROL)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OperatingModeResponse to check
            :type bitmap: ``ProfileManagement.OperatingModeResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_onboard_mode(test_case, bitmap, expected):
            """
            Check onboard_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OperatingModeResponse to check
            :type bitmap: ``ProfileManagement.OperatingModeResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert onboard_mode that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.onboard_mode),
                msg="The onboard_mode parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.onboard_mode})")
        # end def check_onboard_mode

        @staticmethod
        def check_profile_mode(test_case,
                               bitmap,
                               expected):
            """
            Check profile_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: OperatingModeResponse to check
            :type bitmap: ``ProfileManagement.OperatingModeResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert profile_mode that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.profile_mode),
                msg="The profile_mode parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.profile_mode})")
        # end def check_profile_mode
    # end class OperatingModeResponseChecker

    class GetSetModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSetModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "operating_mode_response": (
                    cls.check_operating_mode_response,
                    ProfileManagementTestUtils.OperatingModeResponseChecker.get_default_check_map(test_case)),
                "curr_profile_file_id": (
                    cls.check_curr_profile_file_id,
                    ProfileManagement.Partition.FileId.OOB | 0x0001)
            }
        # end def get_default_check_map

        @staticmethod
        def check_operating_mode_response(test_case, message, expected):
            """
            Check ``operating_mode_response``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetSetModeResponse to check
            :type message: ``pyhid.hidpp.features.gaming.profilemanagement.GetSetModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ProfileManagementTestUtils.OperatingModeResponseChecker.check_fields(
                test_case, message.operating_mode_response, ProfileManagement.OperatingModeResponse, expected)
        # end def check_operating_mode_response

        @staticmethod
        def check_curr_profile_file_id(test_case, response, expected):
            """
            Check curr_profile_file_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSetModeResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetSetModeResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert curr_profile_file_id that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.curr_profile_file_id),
                msg="The curr_profile_file_id parameter differs "
                    f"(expected:{expected}, obtained:{response.curr_profile_file_id})")
        # end def check_curr_profile_file_id
    # end class GetSetModeResponseChecker

    class GetSetPowerOnParamsResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSetPowerOnParamsResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "power_on_profile": (
                    cls.check_power_on_profile,
                    ProfileManagement.Partition.FileId.OOB | 0x0001)
            }
        # end def get_default_check_map

        @staticmethod
        def check_power_on_profile(test_case, response, expected):
            """
            Check power_on_profile field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSetPowerOnParamsResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetSetPowerOnParamsResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert power_on_profile that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.power_on_profile),
                msg="The power_on_profile parameter differs "
                    f"(expected:{expected}, obtained:{response.power_on_profile})")
        # end def check_power_on_profile
    # end class GetSetPowerOnParamsResponseChecker

    class GetHashesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetHashesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "hash_0": (
                    cls.check_hash_0,
                    0xFFFFFFFF),
                "hash_1": (
                    cls.check_hash_1,
                    0xFFFFFFFF),
                "hash_2": (
                    cls.check_hash_2,
                    0xFFFFFFFF),
                "hash_3": (
                    cls.check_hash_3,
                    0xFFFFFFFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_hash_0(test_case, response, expected):
            """
            Check hash_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHashesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetHashesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert hash_0 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.hash_0),
                msg="The hash_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.hash_0})")
        # end def check_hash_0

        @staticmethod
        def check_hash_1(test_case, response, expected):
            """
            Check hash_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHashesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetHashesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert hash_1 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.hash_1),
                msg="The hash_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.hash_1})")
        # end def check_hash_1

        @staticmethod
        def check_hash_2(test_case, response, expected):
            """
            Check hash_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHashesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetHashesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert hash_2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.hash_2),
                msg="The hash_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.hash_2})")
        # end def check_hash_2

        @staticmethod
        def check_hash_3(test_case, response, expected):
            """
            Check hash_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHashesResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.GetHashesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert hash_3 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.hash_3),
                msg="The hash_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.hash_3})")
        # end def check_hash_3
    # end class GetHashesResponseChecker

    class ReadBufferResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadBufferResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "data": (
                    cls.check_data,
                    None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_data(test_case, response, expected):
            """
            Check data field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ReadBufferResponse to check
            :type response: ``pyhid.hidpp.features.gaming.profilemanagement.ReadBufferResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert data that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.data),
                msg="The data parameter differs "
                    f"(expected:{expected}, obtained:{response.data})")
        # end def check_data
    # end class ReadBufferResponseChecker

    class ProfileChangeResultResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ProfileChangeResultResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "failure": (
                    cls.check_failure,
                    ProfileManagement.ProfileChangeResult.Result.SUCCESS)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ProfileChangeResultResponse to check
            :type bitmap: ``ProfileManagement.ProfileChangeResult``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_failure(test_case, bitmap, expected):
            """
            Check onboard_mode field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: ProfileChangeResultResponse to check
            :type bitmap: ``ProfileManagement.ProfileChangeResult``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert failure that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.failure),
                msg="The failure parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.failure})")
        # end def check_failure
    # end class ProfileChangeResultResponseChecker

    class ProfileChangeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ProfileChangeEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "new_profile": (
                    cls.check_new_profile,
                    ProfileManagement.Partition.FileId.OOB | 0x0001),
                "profile_change_result": (
                    cls.check_profile_change_result,
                    ProfileManagementTestUtils.ProfileChangeResultResponseChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_new_profile(test_case, message, expected):
            """
            Check new profile field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: ProfileChangeEvent to check
            :type message: ``ProfileChangeEvent``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert new_profile that raise an exception
            """
            # The new_profile should be ignored if the profile change result failed.
            # cf https://jira.logitech.io/projects/NERV/issues/NERV-186
            if not message.profile_change_result.failure:
                test_case.assertEqual(
                    expected=to_int(expected),
                    obtained=to_int(message.new_profile),
                    msg="The new_profile parameter differs "
                        f"(expected:{expected}, obtained:{message.new_profile})")
            # end if
        # end def check_new_profile

        @staticmethod
        def check_profile_change_result(test_case, message, expected):
            """
            Check ProfileChangeResult field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: ProfileChangeEvent to check
            :type message: ``ProfileChangeEvent``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ProfileManagementTestUtils.ProfileChangeResultResponseChecker.check_fields(
                test_case, message.profile_change_result, ProfileManagement.ProfileChangeResult, expected)
        # end def check_profile_change_result
    # end class ProfileChangeEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=ProfileManagement.FEATURE_ID,
                           factory=ProfileManagementFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetCapabilitiesResponse
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_8101_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_profile_tag_list(cls, test_case, offset_bytes, device_index=None, port_index=None, software_id=None,
                                 padding=None):
            """
            Process ``GetProfileTagList``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param offset_bytes: Offset Bytes
            :type offset_bytes: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetProfileTagListResponse
            :rtype: ``GetProfileTagListResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.get_profile_tag_list_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                offset_bytes=offset_bytes)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.get_profile_tag_list_response_cls)
        # end def get_profile_tag_list

        @classmethod
        def start_write_buffer(cls, test_case, count, device_index=None, port_index=None, software_id=None,
                               padding=None):
            """
            Process ``StartWriteBuffer``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param count: Count
            :type count: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: StartWriteBufferResponse
            :rtype: ``StartWriteBufferResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.start_write_buffer_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                count=count)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.start_write_buffer_response_cls)
        # end def start_write_buffer

        @classmethod
        def write_buffer(cls, test_case, data, device_index=None, port_index=None, software_id=None):
            """
            Process ``WriteBuffer``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param data: Data
            :type data: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: WriteBufferResponse
            :rtype: ``WriteBufferResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.write_buffer_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                data=data)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.write_buffer_response_cls)
        # end def write_buffer

        @classmethod
        def get_error(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetError``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetErrorResponse
            :rtype: ``GetErrorResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.get_error_cls(
                device_index=device_index,
                feature_index=feature_8101_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.get_error_response_cls)
        # end def get_error

        @classmethod
        def edit_buffer(cls, test_case, count, opcode, address, data, device_index=None, port_index=None,
                        software_id=None):
            """
            Process ``EditBuffer``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param count: Count
            :type count: ``int | HexList``
            :param opcode: Opcode
            :type opcode: ``int | HexList``
            :param address: Address
            :type address: ``int | HexList``
            :param data: Data
            :type data: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: EditBufferResponse
            :rtype: ``EditBufferResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.edit_buffer_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                count=count,
                opcode=opcode,
                address=address,
                data=data)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.edit_buffer_response_cls)
        # end def edit_buffer

        @classmethod
        def get_set_mode(cls, test_case,
                         onboard_mode=ProfileManagement.Mode.ONBOARD_MODE,
                         set_onboard_mode=0,
                         profile_mode=ProfileManagement.ProfileMode.HW_SW_CONTROL,
                         set_profile_mode=0,
                         device_index=None, port_index=None,
                         software_id=None, padding=None):
            """
            Process ``GetSetMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param onboard_mode: Onboard Mode  - OPTIONAL
            :type onboard_mode: ``int | HexList``
            :param set_onboard_mode: Set Onboard Mode - OPTIONAL
            :type set_onboard_mode: ``int | HexList``
            :param profile_mode: Profile Mode  - OPTIONAL
            :type profile_mode: ``int | HexList``
            :param set_profile_mode: Set Profile Mode  - OPTIONAL
            :type set_profile_mode: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetSetModeResponse
            :rtype: ``GetSetModeResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.get_set_mode_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                onboard_mode=onboard_mode,
                set_onboard_mode=set_onboard_mode,
                profile_mode=profile_mode,
                set_profile_mode=set_profile_mode)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.get_set_mode_response_cls)
        # end def get_set_mode

        @classmethod
        def save(cls, test_case, first_sector_id, count, hash32, device_index=None, port_index=None, software_id=None,
                 padding=None):
            """
            Process ``Save``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param first_sector_id: First Sector Id
            :type first_sector_id: ``int | HexList``
            :param count: Count
            :type count: ``int | HexList``
            :param hash32: Hash32
            :type hash32: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SaveResponse
            :rtype: ``SaveResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.save_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                first_sector_id=first_sector_id,
                count=count,
                hash32=hash32)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.save_response_cls)
        # end def save

        @classmethod
        def load(cls, test_case, first_sector_id, count, device_index=None, port_index=None, software_id=None,
                 padding=None):
            """
            Process ``Load``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param first_sector_id: First Sector Id
            :type first_sector_id: ``int | HexList``
            :param count: Count
            :type count: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: LoadResponse
            :rtype: ``LoadResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.load_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                first_sector_id=first_sector_id,
                count=count)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.load_response_cls)
        # end def load

        @classmethod
        def configure(cls, test_case, feature_id, file_type_id, file_id, count, hash_key,
                      device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``Configure``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param feature_id: Feature Id
            :type feature_id: ``int | HexList``
            :param file_type_id: File Type Id
            :type file_type_id: ``int | HexList``
            :param file_id: File Id
            :type file_id: ``int | HexList``
            :param count: Count
            :type count: ``int | HexList``
            :param hash_key: Hash
            :type hash_key: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ConfigureResponse
            :rtype: ``ConfigureResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.configure_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                feature_id=feature_id,
                file_type_id=file_type_id,
                file_id=file_id,
                count=count,
                hash_key=hash_key)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.configure_response_cls)
        # end def configure

        @classmethod
        def get_set_power_on_params(cls, test_case, set_power_on_profile, power_on_profile, device_index=None,
                                    port_index=None, software_id=None):
            """
            Process ``GetSetPowerOnParams``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param set_power_on_profile: Set Power On Profile
            :type set_power_on_profile: ``int | HexList``
            :param power_on_profile: Power On Profile
            :type power_on_profile: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: GetSetPowerOnParamsResponse
            :rtype: ``GetSetPowerOnParamsResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.get_set_power_on_params_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                set_power_on_profile=set_power_on_profile,
                power_on_profile=power_on_profile)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.get_set_power_on_params_response_cls)
        # end def get_set_power_on_params

        @classmethod
        def get_hashes(cls, test_case, compute, file_id_0, file_id_1, file_id_2, file_id_3, device_index=None,
                       port_index=None, software_id=None, padding=None):
            """
            Process ``GetHashes``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param compute: Compute
            :type compute: ``int | HexList``
            :param file_id_0: File Id 0
            :type file_id_0: ``int | HexList``
            :param file_id_1: File Id 1
            :type file_id_1: ``int | HexList``
            :param file_id_2: File Id 2
            :type file_id_2: ``int | HexList``
            :param file_id_3: File Id 3
            :type file_id_3: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetHashesResponse
            :rtype: ``GetHashesResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.get_hashes_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                compute=compute,
                file_id_0=HexList(file_id_0),
                file_id_1=HexList(file_id_1),
                file_id_2=HexList(file_id_2),
                file_id_3=HexList(file_id_3))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.get_hashes_response_cls)
        # end def get_hashes

        @classmethod
        def read_buffer(cls, test_case, offset_bytes, device_index=None, port_index=None, software_id=None,
                        padding=None):
            """
            Process ``ReadBuffer``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param offset_bytes: Offset Bytes
            :type offset_bytes: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReadBufferResponse
            :rtype: ``ReadBufferResponse``
            """
            feature_8101_index, feature_8101, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8101.read_buffer_cls(
                device_index=device_index,
                feature_index=feature_8101_index,
                offset_bytes=offset_bytes)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8101.read_buffer_response_cls)
        # end def read_buffer

        @classmethod
        def profile_change_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``ProfileChangeEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: ProfileChangeEvent
            :rtype: ``ProfileChangeEvent``
            """
            _, feature_8101, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8101.profile_change_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def profile_change_event
    # end class HIDppHelper

    class ProfileHelper:
        """
        0x8101 Profile definition class
        """

        _tag_list_from_device = None

        @classmethod
        def create_directory(cls, test_case, hex_directory=None):
            """
            Create a directory

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param hex_directory: Directory in hex representation - OPTIONAL
            :type hex_directory: ``HexList``

            :return: The ``DirectoryFile`` instance
            :rtype: ``DirectoryFile``
            """
            directory = DirectoryFile() if not hex_directory else DirectoryFile.fromHexList(data=hex_directory)
            config = test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT
            directory.init_id_manager(max_directory_sector_id=int(config.F_MaxDirectorySectorId),
                                      max_sector_id=int(config.F_MaxSectorId),
                                      sector_size=int(config.F_MaxSectorSize),
                                      max_file_id=int(config.F_MaxFileId))
            return directory
        # end def create_directory

        @classmethod
        def get_oob_directory(cls, test_case):
            """
            Get OOB Directory from device

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: The ``DirectoryFile`` instance
            :rtype: ``DirectoryFile``
            """
            ProfileManagementTestUtils.HIDppHelper.load(test_case=test_case,
                                                        first_sector_id=ProfileManagement.Partition.SectorId.OOB,
                                                        count=0xFFFF)
            max_dir_sector_id = int(test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_MaxDirectorySectorId)
            max_sector_size = int(test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_MaxSectorSize)
            hex_oob_directory = HexList()
            directory_size = max_dir_sector_id * max_sector_size
            for offset in range(0, max_dir_sector_id * max_sector_size, 16):
                resp = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=test_case, offset_bytes=offset)
                is_eof = True if HexList(DirectoryFile.NO_FILE) in resp.data else False
                eof_index = resp.data.index(HexList(DirectoryFile.NO_FILE)) if is_eof else None

                if offset == 0:
                    # "DirectoryFile.HEADER_LENGTH - 1" is the index of nFiles
                    directory_size = DirectoryFile.HEADER_LENGTH + \
                                     resp.data[DirectoryFile.HEADER_LENGTH - 1] * DirectoryFile.FILE_LENGTH + \
                                     DirectoryFile.EOF_LENGTH
                # end if

                if not is_eof:
                    hex_oob_directory += resp.data
                else:
                    if (len(hex_oob_directory) + eof_index + 1) >= directory_size:
                        hex_oob_directory += resp.data[:eof_index]
                        break
                    else:
                        hex_oob_directory += resp.data
                    # end if
                # end if
            # end for
            return cls.create_directory(test_case=test_case, hex_directory=hex_oob_directory)
        # end def get_oob_directory

        @classmethod
        def get_oob_directory_from_settings(cls, test_case):
            """
            Get OOB Directory from settings

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: The ``DirectoryFile`` instance
            :rtype: ``DirectoryFile``
            """
            oob_directory_config = test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.OOB_PROFILE_DIRECTORY
            # The default value of OOB directory hash bytes are: [0xFF, 0xFF, 0xFF, 0xFF]
            hex_oob_directory = HexList(len(oob_directory_config.F_FileId))
            for index in range(len(oob_directory_config.F_FileId)):
                hex_oob_directory += HexList(
                    to_int(oob_directory_config.F_FileId[index]),
                    to_int(oob_directory_config.F_FeatureId[index]) >> 8 & 0xFF,
                    to_int(oob_directory_config.F_FeatureId[index]) & 0xFF,
                    to_int(oob_directory_config.F_FileTypeId[index]) << 6 +
                    ((to_int(oob_directory_config.F_Length[index]) >> 8 & 0xFF) & (2 ** 6 - 1)),
                    to_int(oob_directory_config.F_Length[index]) & 0xFF,
                    to_int(oob_directory_config.F_Crc32[index]) >> 24 & 0xFF,
                    to_int(oob_directory_config.F_Crc32[index]) >> 16 & 0xFF,
                    to_int(oob_directory_config.F_Crc32[index]) >> 8 & 0xFF,
                    to_int(oob_directory_config.F_Crc32[index]) & 0xFF,
                    to_int(oob_directory_config.F_SectorId_Lsb[index]))
            # end for
            hex_oob_directory += HexList(ProfileManagement.Tag.EOF)
            hex_oob_directory = \
                ProfileManagementTestUtils.ProfileHelper.calculate_crc32(hex_oob_directory) + hex_oob_directory

            return cls.create_directory(test_case=test_case, hex_directory=HexList(hex_oob_directory))
        # end def get_oob_directory_from_settings

        @classmethod
        def get_hex_tag_list(cls, test_case):
            """
            Get the supported tag list from device in hex representation

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: The profile tag list
            :rtype: ``HexList``
            """
            max_sector_size = int(test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_MaxSectorSize)
            hex_tag_list = HexList()
            for offset in range(0, max_sector_size, 16):
                resp = ProfileManagementTestUtils.HIDppHelper.get_profile_tag_list(test_case=test_case,
                                                                                   offset_bytes=offset)
                is_eof = True if HexList(Numeral(ProfileManagement.Tag.EOF)) in resp.partial_tag_list else False
                eof_index = resp.partial_tag_list.index(HexList(Numeral(ProfileManagement.Tag.EOF))) if is_eof else None

                if not is_eof:
                    hex_tag_list += resp.partial_tag_list
                else:
                    hex_tag_list += resp.partial_tag_list[:eof_index + 1]
                    break
                # end if
            # end for
            return hex_tag_list
        # end def get_hex_tag_list

        @classmethod
        def get_tag_list(cls, test_case):
            """
            Get the supported tag list

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: The profile tag list
            :rtype: ``list[ProfileManagement.Tag]``
            """
            if not cls._tag_list_from_device:
                hex_tag_list = cls.get_hex_tag_list(test_case=test_case)
                tag_list = []
                offset = 0
                while offset < len(hex_tag_list):
                    if hex_tag_list[offset] in [ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO >> 16,
                                                ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE >> 16,
                                                ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_FN >> 16,
                                                ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_GSHIFT >> 16]:
                        tag_list.append(ProfileManagement.Tag(to_int(hex_tag_list[offset: offset + 3])))
                        offset += 3
                    elif hex_tag_list[offset] == ProfileManagement.Tag.EOF:
                        break
                    else:
                        tag_list.append(ProfileManagement.Tag(hex_tag_list[offset]))
                        offset += 1
                    # end if
                # end while
                cls._tag_list_from_device = tag_list
            # end if
            return cls._tag_list_from_device
        # end def get_tag_list

        @classmethod
        def get_field_address_in_profile(cls, profile, field):
            """
            Get the address of specified field in the profile

            :param profile: The profile
            :type profile: ``Profile``
            :param field: The specified field in profile
            :type field: ``ProfileManagement.Tag | int``

            :return: The address of the specified field in the profile
            :rtype: ``int``

            :raise ``ValueError``: if the specified field is not found in the profile
            """
            address = 0
            for tag in profile.tag_fields:
                if tag == field:
                    return address
                else:
                    address += PROFILE_TAG_INFO_MAP[tag].byte_count
                # end if
            # end for

            raise ValueError(f'The specified field {field} cannot be found in the {profile}')
        # end def get_field_address_in_profile

        @classmethod
        def get_oob_profile(cls, test_case, oob_profile_index=0):
            """
            Get OOB Profile from device

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param oob_profile_index: The oob profile index - OPTIONAL
            :type oob_profile_index: ``int``

            :return: The ``OobProfile`` instance
            :rtype: ``OobProfile | None``
            """
            oob_directory = cls.get_oob_directory(test_case=test_case)
            tag_list = cls.get_tag_list(test_case=test_case)
            oob_profile = None
            current_profile_index = 0
            for file_id, file in oob_directory.files.items():
                if to_int(file.feature_id) == ProfileManagement.FEATURE_ID:
                    if current_profile_index == oob_profile_index:
                        first_sector_id = ProfileManagement.Partition.SectorId.OOB + to_int(file.first_sector_id_lsb)
                        count = to_int(file.n_bytes)
                        ProfileManagementTestUtils.HIDppHelper.load(test_case=test_case,
                                                                    first_sector_id=first_sector_id, count=count)
                        hex_oob_profile = HexList()
                        for offset in range(0, count, 16):
                            read_buffer = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=test_case,
                                                                                             offset_bytes=offset)
                            hex_oob_profile += read_buffer.data
                        # end for
                        oob_profile = OobProfile.from_hex_list(tag_list=tag_list, data=hex_oob_profile)
                    # end if
                    current_profile_index += 1
                # end if
            # end for
            return oob_profile
        # end def get_oob_profile

        @classmethod
        def get_oob_profile_from_settings(cls, test_case, oob_profile_index=0):
            """
            Get OOB Profile from settings

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param oob_profile_index: The oob profile index - OPTIONAL
            :type oob_profile_index: ``int``

            :return: The ``OobProfile`` instance
            :rtype: ``OobProfile | None``
            """
            tag_list = cls.get_tag_list(test_case=test_case)
            str_oob_profile = str()
            hex_oob_profile = HexList()

            for tag in tag_list:
                if PROFILE_TAG_INFO_MAP[tag].name_in_settings != '':
                    setting = getattr(test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.OOB_PROFILES,
                                      f'F_{PROFILE_TAG_INFO_MAP[tag].name_in_settings}')
                    str_oob_profile += setting[oob_profile_index].replace(' ', '')
                # end if
            # end for
            for index in range(len(str_oob_profile) // 2):
                hex_oob_profile += HexList(str_oob_profile[2 * index: 2 * (index + 1)])
            # end for
            hex_oob_profile.append(0xFF)
            oob_profile = OobProfile.from_hex_list(tag_list=tag_list, data=hex_oob_profile)

            return oob_profile
        # end def get_oob_profile_from_settings

        @classmethod
        def get_ram_buffer_data(cls, test_case, count=0):
            """
            Get data from RAM buffer

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param count: Count - OPTIONAL
            :type count: ``int``

            :return: RAM buffer data in ``HexList``
            :rtype: ``HexList``
            """
            hex_oob_profile = HexList()
            for offset in range(0, count, 16):
                read_buffer = ProfileManagementTestUtils.HIDppHelper.read_buffer(test_case=test_case,
                                                                                 offset_bytes=offset)
                hex_oob_profile += read_buffer.data if (count - offset) >= 16 else read_buffer.data[:count - offset]
            # end for
            return hex_oob_profile
        # end def get_ram_buffer_data

        @classmethod
        def create_profile_from_oob(cls, test_case, directory, oob_profile_index=0,
                                    file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE):
            """
            Create a default profile from oob profile

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param oob_profile_index: The oob profile index - OPTIONAL
            :type oob_profile_index: ``int``
            :param file_type_id: The file type id - OPTIONAL
            :type file_type_id: ``ProfileManagement.FileTypeId.X8101 | int``

            :return: The ``Profile`` instance
            :rtype: ``Profile``

            :raise ``AssertionError``: If the oob profile is None
            """
            oob_profile = cls.get_oob_profile(test_case=test_case, oob_profile_index=oob_profile_index)
            assert oob_profile is not None

            tag_list = cls.get_tag_list(test_case=test_case)
            tag_fields = deepcopy(oob_profile.tag_fields)
            for tag in tag_list:
                if tag == ProfileManagement.Tag.EOF:
                    break
                elif tag in [ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO,
                             ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE,
                             ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_FN,
                             ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_GSHIFT,
                             ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_ACTUATION,
                             ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER,
                             ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_MULTI_ACTION]:
                    tag_info = PROFILE_TAG_INFO_MAP[tag]
                    tag_settings = 'FF FF FF FF'
                    tag_fields[tag] = tag_info.class_type.fromHexList(data=HexList(tag_settings))
                # end if
            # end for

            profile = Profile(tag_fields=tag_fields)
            profile.register(directory=directory, file_type_id=file_type_id)
            return profile
        # end def create_profile_from_oob

        @classmethod
        def create_profile_from_settings(cls, test_case, directory, oob_profile_index=0,
                                         file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE):
            """
            Create a default profile from test settings

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param oob_profile_index: The profile index in the test settings - OPTIONAL
            :type oob_profile_index: ``int``
            :param file_type_id: The file type id - OPTIONAL
            :type file_type_id: ``ProfileManagement.FileTypeId.X8101 | int``

            :return: The ``Profile`` instance
            :rtype: ``Profile``
            """
            tag_list = [ProfileManagement.Tag(to_int(x))
                        for x in test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_TagList]
            tag_fields = {}
            oob_profile_config = test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.OOB_PROFILES
            for tag in tag_list:
                if tag == ProfileManagement.Tag.EOF:
                    break
                # end if
                tag_info = PROFILE_TAG_INFO_MAP[tag]
                # Set feature settings file id = 0xFFFF by default for 0x1B05, 0x1B05 Macro and 0x4523.
                # Shall update these fields later.
                tag_settings = 'FF FF FF FF' if not tag_info.name_in_settings \
                    else getattr(oob_profile_config, f'F_{tag_info.name_in_settings}')[oob_profile_index]
                tag_fields[tag] = tag_info.class_type.fromHexList(data=HexList(tag_settings))
            # end for

            profile = Profile(tag_fields=tag_fields)
            profile.register(directory=directory, file_type_id=file_type_id)
            return profile
        # end def create_profile_from_settings

        @classmethod
        def calculate_crc32(cls, data):
            """
            Calculate CRC32 for input data

            :param data: Data
            :type data: ``HexList``

            :return: The CRC32 result of input data
            :rtype: ``HexList``
            """
            return DirectoryFile.calculate_crc32(data=data)
        # end def calculate_crc32

        @classmethod
        def convert_to_tag(cls, file_type_id):
            """
            Convert 0x1B05 file type id to 0x8101 tag

            :param file_type_id: The 0x1B05 file type id
            :type file_type_id: ``ProfileManagement.FileTypeId.X1B05 | int``

            :return: The corresponding 0x8101 tag
            :rtype: ``ProfileManagement.Tag``

            :raise ``ValueError``: If the input file_type_id is unknown
            """
            if file_type_id == ProfileManagement.FileTypeId.X1B05.MACRO_DEFINITION_FILE:
                return ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO
            elif file_type_id == ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE:
                return ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE
            elif file_type_id == ProfileManagement.FileTypeId.X1B05.FN_LAYER_SETTINGS_FILE:
                return ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_FN
            elif file_type_id == ProfileManagement.FileTypeId.X1B05.GSHIFT_LAYER_SETTINGS_FILE:
                return ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_GSHIFT
            else:
                raise ValueError(f'Unknown file_type_id: {file_type_id}')
            # end if
        # end def convert_to_tag

        @classmethod
        def create_onboard_profiles_and_save_in_nvs(cls, test_case, directory, save_in_nvs=True):
            """
            Create the device supported number of onboard profiles

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param save_in_nvs: Indicate to save onboard profiles in NVS - OPTIONAL
            :type save_in_nvs: ``bool``

            :return: The onboard profiles
            :rtype: ``list[Profile]``
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case,
                               "Test Loop: Loop over index in range("
                               f"{test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_NumOnboardProfiles})")
            # ----------------------------------------------------------------------------------------------------------
            profiles = []
            for index in range(test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_NumOnboardProfiles):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Create a onboard profile with file_id={index} from a settings")
                # ------------------------------------------------------------------------------------------------------
                profiles.append(ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                    test_case, directory, file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE))
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            if save_in_nvs:
                for profile in profiles:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Write 0x8101 profile to NVS\n{profile}")
                    # --------------------------------------------------------------------------------------------------
                    ProfileManagementTestUtils.write(test_case=test_case, data=HexList(profile),
                                                     store_in_nvs=True,
                                                     first_sector_id_lsb=profile.first_sector_id_lsb,
                                                     crc_32=profile.crc_32)
                # end for
            # end if

            return profiles
        # end def create_onboard_profiles_and_save_in_nvs

        @classmethod
        def create_onboard_profiles_from_settings_and_update_profile_directory(
                cls, test_case, save_profile_in_nvs=False, save_directory_in_nvs=False, directory=None):
            """
            Create a default profile from test settings and create the profile directory if the directory parameter is
            None

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param save_profile_in_nvs: Flag indicating if the created profile should be saved in the NVS - OPTIONAL
            :type save_profile_in_nvs: ``bool``
            :param save_directory_in_nvs:
                Flag indicating if the created  directory should be saved in the NVS - OPTIONAL
            :type save_directory_in_nvs: ``bool``
            :param directory: ``DirectoryFile`` instance - OPTIONAL
            :type directory: ``DirectoryFile | None``

            :return: The ``DirectoryFile`` and ``Profile`` instances
            :rtype: ``tuple[DirectoryFile, list[Profile]]``
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "Create an empty 0x8101 directory")
            # ----------------------------------------------------------------------------------------------------------
            if directory is None:
                directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=test_case)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "Create valid 0x8101 onboard profiles from settings")
            # ----------------------------------------------------------------------------------------------------------
            profiles = ProfileManagementTestUtils.ProfileHelper.create_onboard_profiles_and_save_in_nvs(
                test_case=test_case, directory=directory)

            for profile in profiles:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Write 0x8101 profile to NVS\n{profile}")
                # ------------------------------------------------------------------------------------------------------
                ProfileManagementTestUtils.write(test_case=test_case, data=HexList(profile),
                                                 store_in_nvs=save_profile_in_nvs,
                                                 first_sector_id_lsb=profile.first_sector_id_lsb,
                                                 crc_32=profile.crc_32)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Write 0x8101 directory to NVS\n{directory}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=test_case, data=HexList(directory),
                                             store_in_nvs=save_directory_in_nvs,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)

            return directory, profiles
        # end def create_onboard_profiles_from_settings_and_update_profile_directory
    # end class ProfileHelper

    @classmethod
    def write(cls, test_case, data, store_in_nvs=False, first_sector_id_lsb=None, crc_32=None,
              raise_buffer_exception=True):
        """
        Write file to device

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param data: Data to be written to device
        :type data: ``HexList``
        :param store_in_nvs: Indicate to save data in NVS or keep in RAM - OPTIONAL
        :type store_in_nvs: ``bool``
        :param first_sector_id_lsb: The sector_id of the NVS partition sector at which to start the write. - OPTIONAL
        :type first_sector_id_lsb: ``int``
        :param crc_32: The 32-bit hash key to check against - OPTIONAL
        :type crc_32: ``int | HexList``
        :param raise_buffer_exception: Raise exception if count exceeds RAM buffer size - OPTIONAL
        :type raise_buffer_exception: ``bool``

        :raise ``AssertionError``: If the first_sector_id_lsb or crc_32 is None when store_in_nvs is True
        :raise ``Exception``: If writing the data fails
        """
        try:
            ChannelUtils.check_queue_empty(test_case=test_case, queue_name=HIDDispatcher.QueueName.ERROR)

            # For the robustness test case to validate a macro which exceeds the maximum macro size, if the data length
            # is larger than the RAM buffer size, only write the first part
            if (raise_buffer_exception is False and len(data) >
                    test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_RamBufferSize):
                byte_count = test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_RamBufferSize
                crc_32 = ProfileManagementTestUtils.ProfileHelper.calculate_crc32(data=HexList(data[:byte_count]))
            else:
                byte_count = len(data)
            # end if
            data_len = int(WriteBuffer.LEN.DATA/8)
            cls.HIDppHelper.start_write_buffer(test_case=test_case, count=byte_count)
            for index in range(0, byte_count, data_len):
                offset = data_len if index + data_len <= byte_count else byte_count - index
                cls.HIDppHelper.write_buffer(
                    test_case=test_case,
                    data=data[index: index + offset]
                    if offset == data_len else data[index: index + offset] + ([0] * (data_len - offset)))
            # end for

            if store_in_nvs:
                assert first_sector_id_lsb is not None
                assert crc_32 is not None
                test_case.post_requisite_reload_nvs = True
                first_sector_id = ProfileManagement.Partition.SectorId.NVS | first_sector_id_lsb
                cls.HIDppHelper.save(test_case=test_case,
                                     first_sector_id=HexList(Numeral(first_sector_id, byteCount=2)),
                                     count=HexList(Numeral(byte_count, byteCount=2)),
                                     hash32=crc_32)
            # end if
        except Exception as e:
            response = ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.ERROR,
                                                   class_type=ErrorCodes)
            get_error_resp = cls.HIDppHelper.get_error(test_case=test_case)
            raise Exception(f'Exception: {e}, HID++ 2.0 Error: {response}, 0x8101 Error: {get_error_resp}')
        # end try
    # end def write

    @classmethod
    def activate(cls, test_case, feature_id, file_type_id, file_id, count, crc_32):
        """
        Activate 0x8101 or 0x1B05 feature settings

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param feature_id: Feature Id
        :type feature_id: ``int | HexList``
        :param file_type_id: File Type Id
        :type file_type_id: ``int | HexList``
        :param file_id: File Id
        :type file_id: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param crc_32: CRC 32 hash code
        :type crc_32: ``int | HexList``

        :raise ``Exception``: If configuring the feature settings fails
        """
        try:
            cls.HIDppHelper.configure(test_case=test_case, feature_id=feature_id, file_type_id=file_type_id,
                                      file_id=file_id, count=count, hash_key=crc_32)
        except Exception as e:
            response = ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.ERROR,
                                                   class_type=ErrorCodes)
            get_error_resp = cls.HIDppHelper.get_error(test_case=test_case)
            raise Exception(f'Exception: {e}, HID++ 2.0 Error: {response}, 0x8101 Error: {get_error_resp}')
        # end try
    # end def activate

    @classmethod
    def get_len_of_tag_list_from_settings(cls, test_case):
        """
        Get the number of total bytes of tag list from settings

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The number of bytes of tag list
        :rtype: ``int``
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT
        return int(len(''.join(config.F_TagList))/2)
    # end def get_len_of_tag_list_from_settings

    @classmethod
    def get_onboard_profiles_selection_keys(cls, test_case):
        """
        Get the onboard profile selection keys.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The KEY_ID list of onboard profiles selection keys
        :rtype: ``list[KEY_ID]``
        """
        selection_keys = []
        for index in range(1, test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_NumOnboardProfiles + 1):
            try:
                selection_keys.append(test_case.button_stimuli_emulator.get_fn_keys()[
                                          getattr(KEY_ID, f'ONBOARD_PROFILE_{str(index)}')])
            except KeyError:
                warnings.warn(f'The KEY_ID.ONBOARD_PROFILE_{str(index)} is not defined in FN_KEYS')
            # end try
        # end for

        return selection_keys
    # end def get_onboard_profiles_selection_keys
# end class ProfileManagementTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
