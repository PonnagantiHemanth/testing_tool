#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b08.errorhandling
:brief: HID++ 2.0 ``AnalogKeys`` error handling test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/03/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.analogkeys import AnalogKeys
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analogkeysutils import AnalogKeysTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hidpp20.common.feature_1b08.analogkeys import AnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysErrorHandlingTestCase(AnalogKeysTestCase):
    """
    Validate ``AnalogKeys`` errorhandling test cases
    """

    @features("Feature1B08")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1b08.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.HIDppHelper.get_capabilities_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B08_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1B08")
    @features("Feature8101")
    @level("ErrorHandling")
    def test_wrong_crc_shall_return_error(self):
        """
        Add 0x1B08 configuration file into 0x8101 profile directory with wrong CRC value shall return HW_ERROR(0x04)
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create Profile Table")
        # --------------------------------------------------------------------------------------------------------------
        profiles = []
        # Create all supported onboard profiles
        for profile_index in range(self.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_NumOnboardProfiles):
            profile = ProfileManagementTestUtils.ProfileHelper.create_profile_from_oob(
                test_case=self, directory=directory,
                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE)
            profiles.append(profile)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create Actuation Configuration table")
        # --------------------------------------------------------------------------------------------------------------
        actuation_table = AnalogKeysTestUtils.AnalogKeysHelper.create_actuation_point_table(
            test_case=self, directory=directory, number_of_key_to_be_random_generated=3)
        for profile in profiles:
            profile.update_tag_content(
                directory=directory,
                tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_ACTUATION: actuation_table.table_id})
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write tables to NVS")
        # --------------------------------------------------------------------------------------------------------------
        for profile in profiles:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile), store_in_nvs=True,
                                             first_sector_id_lsb=profile.first_sector_id_lsb, crc_32=profile.crc_32)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x1B08 actuation table to NVS\n{actuation_table}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(actuation_table), store_in_nvs=True,
                                         first_sector_id_lsb=actuation_table.first_sector_id_lsb,
                                         crc_32=actuation_table.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb, crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure 0x8101 in NVS to take the changes")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=AnalogKeys.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B08.ACTUATION_CONFIGURATION_FILE,
            file_id=ProfileManagement.Partition.FileId.NVS | actuation_table.table_id,
            count=len(HexList(actuation_table)),
            crc_32=actuation_table.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Load 0x1B08 Actuation table")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(test_case=self, first_sector_id=actuation_table.first_sector_id_lsb,
                                                    count=len(HexList(actuation_table)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Corrupt the CRC-32 value of 0x1B08 tables in 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        start_address = 2
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE, count=1,
            address=start_address,
            data=HexList(Numeral(1, byteCount=1)) + HexList(Numeral(0, byteCount=12)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Save changes")
        # --------------------------------------------------------------------------------------------------------------
        actuation_table.rows[0].trigger_cidx = 1
        actuation_table.crc_32 = ProfileManagementTestUtils.ProfileHelper.calculate_crc32(HexList(actuation_table))
        try:
            ProfileManagementTestUtils.HIDppHelper.save(
                test_case=self, first_sector_id=actuation_table.first_sector_id_lsb,
                count=len(HexList(actuation_table)), hash32=actuation_table.crc_32)
        except AssertionError:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check received HW_ERROR from device")
            # ----------------------------------------------------------------------------------------------------------
            err_resp = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR)
            self.assertEqual(expected=Hidpp2ErrorCodes.HW_ERROR, obtained=to_int(err_resp.error_code))
        # end try

        self.testCaseChecked("ERR_1B08_0002", _AUTHOR)
    # end def test_wrong_crc_shall_return_error
# end class AnalogKeysErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
