#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b05.errorhandling
:brief: HID++ 2.0 ``FullKeyCustomization`` error handling test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/05/29
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import OS
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hidpp20.common.feature_1b05.fullkeycustomization import FullKeyCustomizationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class FullKeyCustomizationErrorHandlingTestCase(FullKeyCustomizationTestCase):
    """
    Validate ``FullKeyCustomization`` errorhandling test cases
    """

    @features('Keyboard')
    @features("Feature1B05")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1b05.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.HIDppHelper.get_capabilities_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B05_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features('Keyboard')
    @features("Feature1B05")
    @level("ErrorHandling")
    @skip("In development")
    def test_get_set_enabled_invalid_toggle_hotkeys(self):
        """
        Validate getSetEnabled API raises an error INVALID_ARGUMENT while assining invalid toggle_keys_enabled
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable invalid toggle_keys by getSetEnabled request with set_toggle_keys_enabled=1"
                                 "and toggle_keys_enabled=bitmap value of invalid toggle_keys")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled_and_check_error(
            test_case=self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
            # toggle_keys_enabled=??, # TODO: All the toggle hotkeys are valid on FKC UX v1.2
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check received a error INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B05_0002", _AUTHOR)
    # end def test_get_set_enabled_invalid_toggle_hotkeys

    @features('Keyboard')
    @features("Feature1B05")
    @level("ErrorHandling")
    @skip("In development")
    def test_configure_invalid_file_type(self):
        """
        If invalid filetype_id of 0x1b05 is assigned while 0x8101.configure, the cfgErrCode is set to 'invalid
        filetype'
        """
        # --------------------------------------------------------------------------------------------------------------
        # TODO: All the 0x1b05 filetypes are valid
        LogHelper.log_prerequisite(self, "Create a FKC profile with invalid filetype=??")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8101.configure request")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8101.getError request")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check error code from getSetEnabled response with FileSystemErrorCode=0x08 and"
                                  "feature_id=0x1b05")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B05_0003", _AUTHOR)
    # end def test_configure_invalid_file_type

    @features('Keyboard')
    @features("Feature1B05")
    @level("ErrorHandling")
    def test_configure_hash_check_fail(self):
        """
        If hash check fails while 0x8101.configure, the cfgErrCode is set to "HASH/CRC CHECK ERROR"
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer with invalid hash")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        random_parameters = random_parameters_cls(button=random_parameters_cls.Button(count=1))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Create FKC main tables\n")
        # --------------------------------------------------------------------------------------------------------------
        main_tables = FullKeyCustomizationTestUtils.FkcTableHelper.create_main_tables(
            test_case=self, directory=directory, os_variant=OS.WINDOWS, random_parameters=random_parameters)
        base_table = main_tables[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Write the FKC main table\n{base_table}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(base_table))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8101.configure request")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ProfileManagementTestUtils.HIDppHelper.configure(
                test_case=self,
                feature_id=FullKeyCustomization.FEATURE_ID,
                file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
                file_id=ProfileManagement.Partition.FileId.RAM,
                count=len(HexList(base_table)),
                hash_key=0x12345678)
        except Exception:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 0x8101.getError request")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check error code from 0x8101.getError response with FileSystemErrorCode="
                                      f"{ProfileManagement.FileSystemErrorCode.CRC_CHECK_ERROR:#x} and "
                                      f"file_id={ProfileManagement.Partition.FileId.RAM:#x}")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(response.fs_error_code)),
                             expected=int(ProfileManagement.FileSystemErrorCode.CRC_CHECK_ERROR),
                             msg="The FileSystemErrorCode differs from the expected"
                                 f"(expected:{ProfileManagement.FileSystemErrorCode.CRC_CHECK_ERROR:#x}, "
                                 f"obtained:{int(Numeral(response.fs_error_code)):#x})")
            self.assertEqual(obtained=int(Numeral(response.fs_error_param_1)),
                             expected=ProfileManagement.Partition.FileId.RAM,
                             msg="The fs_error_param_1 differs from the expected"
                                 f"(expected:{ProfileManagement.Partition.FileId.RAM:#x}, "
                                 f"obtained:{int(Numeral(response.fs_error_param_1)):#x})")
        # end try

        self.testCaseChecked("ERR_1B05_0004", _AUTHOR)
    # end def test_configure_hash_check_fail

    @features('Keyboard')
    @features("Feature1B05")
    @features("Feature1B05FileMaxSize")
    @level("ErrorHandling")
    def test_configure_exceeded_size_fkc_file(self):
        """
        FW should raise an error while configuring an exceeded size fkc file
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Create a FKC profile and remapping in RAM buffer")
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        random_parameters = random_parameters_cls(button=random_parameters_cls.Button(count=1))
        self.create_remapping_in_ram(random_parameters=random_parameters)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Create FKC main tables\n")
        # --------------------------------------------------------------------------------------------------------------
        main_tables = FullKeyCustomizationTestUtils.FkcTableHelper.create_main_tables(
            test_case=self, directory=directory, os_variant=OS.WINDOWS, random_parameters=random_parameters,
            raise_buffer_overflow=False)
        base_table = main_tables[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Write the FKC main table\n{base_table}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(base_table))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x8101.configure request")
        # --------------------------------------------------------------------------------------------------------------
        try:
            ProfileManagementTestUtils.HIDppHelper.configure(
                test_case=self,
                feature_id=FullKeyCustomization.FEATURE_ID,
                file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
                file_id=ProfileManagement.Partition.FileId.RAM,
                count=self.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION.F_FkcConfigFileMaxsize + 1,
                hash_key=base_table.crc_32)
        except Exception:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 0x8101.getError request")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.get_error(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check error code from 0x8101.getError response with FileSystemErrorCode=0x05")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(response.fs_error_code)),
                             expected=int(ProfileManagement.FileSystemErrorCode.FILE_TOO_BIG),
                             msg="The FileSystemErrorCode differs from the expected"
                                 f"(expected:{ProfileManagement.FileSystemErrorCode.FILE_TOO_BIG:#x}, "
                                 f"obtained:{int(Numeral(response.fs_error_code)):#x})")
            self.assertEqual(obtained=int(Numeral(response.fs_error_param_1)),
                             expected=int(ProfileManagement.Partition.FileId.RAM),
                             msg="The fs_error_param_1 differs from the expected"
                                 f"(expected:{ProfileManagement.Partition.FileId.RAM:#x}"
                                 f"obtained:{int(Numeral(response.fs_error_param_1)):#x})")
        # end try

        self.testCaseChecked("ERR_1B05_0006", _AUTHOR)
    # end def test_configure_exceeded_size_fkc_file
# end class FullKeyCustomizationErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
