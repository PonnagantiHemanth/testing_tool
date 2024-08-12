#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8100.business
:brief: HID++ 2.0 ``OnboardProfiles`` business test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/01/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffects
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import KEYSTROKE
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.mcu.profileformat import ProfileDirectory
from pylibrary.mcu.profileformat import ProfileFieldName
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.reportrateutils import ReportRateTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.hidpp20.gaming.feature_8100.onboardprofiles import OnboardProfilesTestCase
from pytestbox.shared.base.specialkeysmsebuttonsutils import SpecialKeysMseButtonsTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OnboardProfilesBusinessTestCase(OnboardProfilesTestCase):
    """
    Validate ``OnboardProfiles`` business test cases
    """

    @features("Feature8100")
    @level('Business', 'SmokeTests')
    def test_oob_profile_business(self):
        """
        Validate all of the OOB profile contents from device shall be the same as the product default definitions.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read OOB profile directory")
        # --------------------------------------------------------------------------------------------------------------
        oob_profile_directory = OnboardProfilesTestUtils.DirectorySettings.read_profile_directory(
            test_case=self, profile_directory_id=OnboardProfiles.SectorId.OOB_PROFILE_DIRECTORY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the settings in OOB profile directory are all as expected settings.")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(self.config.F_ProfileCountOOB, len(oob_profile_directory.directory_items))
        self.assertEqual(self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILE_DIRECTORY),
                         oob_profile_directory.convert_to_test_config_format())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Loop over OOB profile in [0x0101..0x010{self.config.F_ProfileCountOOB}]")
        # --------------------------------------------------------------------------------------------------------------
        for idx in range(self.config.F_ProfileCountOOB):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Read OOB profile")
            # ----------------------------------------------------------------------------------------------------------
            oob_profile = OnboardProfilesTestUtils.Profile.read_profile(
                test_case=self, profile_id=OnboardProfiles.SectorId.OOB_PROFILE_START + idx)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the settings in OOB profile are all as expected settings.")
            # ----------------------------------------------------------------------------------------------------------
            check_map = OnboardProfilesTestUtils.ProfileChecker.get_check_map(test_case=self, index=idx)
            OnboardProfilesTestUtils.ProfileChecker.check_fields(test_case=self, message=oob_profile,
                                                                 expected_cls=type(oob_profile), check_map=check_map)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End of Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8100_0001", _AUTHOR)
    # end def test_oob_profile_business

    @features("Feature8100")
    @level("Business")
    def test_profile_return_to_default(self):
        """
        Create profiles by OOB profiles. Modify the default DPI index for each profiles. Validate these profiles can
        be restored to default OOB settings.
        """
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        none_default_dpi_index = OnboardProfilesTestUtils.get_none_default_dpi_index(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create default profiles from OOB profiles and change the default DPI index "
                  f"to {none_default_dpi_index}.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(
            test_case=self, modifier={'default_dpi_index': none_default_dpi_index})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read modified profiles and validate settings has been changes.")
        # --------------------------------------------------------------------------------------------------------------
        for idx in range(self.config.F_ProfileCountOOB):
            profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=idx+1)
            checker = OnboardProfilesTestUtils.ProfileChecker
            check_map = checker.get_check_map(test_case=self, index=idx)
            check_map['default_dpi_index'] = (checker.check_default_dpi_index, none_default_dpi_index)
            check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
            checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Restore settings to default for all profiles")
        # --------------------------------------------------------------------------------------------------------------
        for idx in range(self.config.F_ProfileCountOOB):
            profile = OnboardProfilesTestUtils.Profile.read_profile(
                test_case=self, profile_id=OnboardProfiles.SectorId.OOB_PROFILE_START + idx)
            OnboardProfilesTestUtils.Profile.write_profile(test_case=self, profile_id=profile_1 + idx, profile=profile)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate settings are all back to default settings")
        # --------------------------------------------------------------------------------------------------------------
        for idx in range(self.config.F_ProfileCountOOB):
            profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=idx + 1)
            checker = OnboardProfilesTestUtils.ProfileChecker
            check_map = checker.get_check_map(test_case=self, index=idx)
            check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
            checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)
        # end for

        self.testCaseChecked("BUS_8100_0002", _AUTHOR)
    # end def test_profile_return_to_default

    @features("Feature8100")
    @level("Business")
    def test_rename_profile(self):
        """
        Add a profile from the OOB profile and rename it by an unicode string. Validate the profile name by readData()
        function.
        """
        oob_profile_1 = OnboardProfiles.SectorId.OOB_PROFILE_START
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        profile_name = 'CI Profile 1'
        profile_name_0_to_23 = OnboardProfilesTestUtils.str_to_profile_name(name=profile_name)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Create a profile 0x0001 from OOB profile 0x0101 and change the profile name to {profile_name}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(
            test_case=self, oob_profile_id=oob_profile_1,
            dest_profile_id=profile_1, modifier={'profile_name_0_to_23': profile_name_0_to_23})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the profile name has been changed to {profile_name} by readData()")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self,
                                                                profile_id=OnboardProfiles.SectorId.PROFILE_START)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map['profile_name_0_to_23'] = (checker.check_profile_name_0_to_23, profile_name_0_to_23)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)
        self.assertEqual(profile_name, OnboardProfilesTestUtils.profile_name_to_str(profile.profile_name_0_to_23))

        self.testCaseChecked("BUS_8100_0003", _AUTHOR)
    # end def test_rename_profile

    @features("Feature8100")
    @features("Feature8060")
    @level("Business")
    def test_report_rate(self):
        """
        Modify report rate in the profile 0x0001. Validate the report rate has been updated by 0x8060.
        """
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        report_rate = OnboardProfilesTestUtils.get_none_default_report_rate(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Create a profile 0x0001 from OOB profile 0x0101 and change the report rate to {report_rate}.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(test_case=self, modifier={'report_rate': report_rate})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map['report_rate'] = (checker.check_report_rate, report_rate)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Validate the report rate has been changed to {report_rate} by 0x8060.getReportRate()")
        # --------------------------------------------------------------------------------------------------------------
        report_rate_response = ReportRateTestUtils.HIDppHelper.get_report_rate(test_case=self)
        self.assertEqual(report_rate, to_int(report_rate_response.report_rate))

        self.testCaseChecked("BUS_8100_0004", _AUTHOR)
    # end def test_report_rate

    @features("Feature8100")
    @features("Feature2201")
    @features("PluralProfiles")
    @level("Business")
    def test_default_dpi_index(self):
        """
        Modify default DPI index in the profile 0x0001.  Validate by 0x8100.getActiveProfileResolution and
        0x2201.getSensorDpi the default DPI index has been updated while changing profile.
        """
        oob_profile_1 = OnboardProfiles.SectorId.OOB_PROFILE_START
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        profile_2 = profile_1 + 1
        non_default_dpi_index, modified_dpi = OnboardProfilesTestUtils.get_none_default_dpi(test_case=self)
        default_dpi_index, default_dpi = OnboardProfilesTestUtils.get_default_dpi(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Create profiles from OOB profiles and change the default DPI index to {non_default_dpi_index}.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(test_case=self,
                                                                 modifier={'default_dpi_index': non_default_dpi_index})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a profile 0x0002 from OOB profile 0x0101")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(test_case=self, oob_profile_id=oob_profile_1,
                                                                       dest_profile_id=profile_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profile directory")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_profile_directory(
            test_case=self,
            directory_items={
                profile_1: ProfileDirectory.Item(sector_id=profile_1, enabled=OnboardProfiles.Status.ENABLED),
                profile_2: ProfileDirectory.Item(sector_id=profile_2, enabled=OnboardProfiles.Status.ENABLED)})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Validate the modified profile settings of profile 0x0001 are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map['default_dpi_index'] = (checker.check_default_dpi_index, non_default_dpi_index)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the profile settings of profile 0x0002 are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_2)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Validate the default DPI index is {default_dpi_index} instead of {non_default_dpi_index} "
                  "by 0x8100.getActiveProfileResolution()")
        # --------------------------------------------------------------------------------------------------------------
        active_resolution_response = OnboardProfilesTestUtils.HIDppHelper.get_active_profile_resolution(test_case=self)
        self.assertEqual(default_dpi_index, to_int(active_resolution_response.resolution_index))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the current DPI is {default_dpi} instead of {modified_dpi} "
                                  "by 0x2201.getSensorDpi()")
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_spi_response = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(test_case=self, sensor_idx=0)
        self.assertEqual(default_dpi, to_int(get_sensor_spi_response.dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set profile 0x0002 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Validate the default DPI index is {default_dpi_index} instead of {non_default_dpi_index} "
                  "by 0x8100.getActiveProfileResolution()")
        # --------------------------------------------------------------------------------------------------------------
        active_resolution_response = OnboardProfilesTestUtils.HIDppHelper.get_active_profile_resolution(test_case=self)
        self.assertEqual(default_dpi_index, to_int(active_resolution_response.resolution_index))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the current DPI is {default_dpi} instead of {modified_dpi} "
                                  "by 0x2201.getSensorDpi()")
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_spi_response = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(test_case=self, sensor_idx=0)
        self.assertEqual(default_dpi, to_int(get_sensor_spi_response.dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Validate the default DPI index has been changed to {non_default_dpi_index} "
                  "by 0x8100.getActiveProfileResolution()")
        # --------------------------------------------------------------------------------------------------------------
        active_resolution_response = OnboardProfilesTestUtils.HIDppHelper.get_active_profile_resolution(test_case=self)
        self.assertEqual(non_default_dpi_index, to_int(active_resolution_response.resolution_index))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the default DPI has been changed to {modified_dpi} "
                                  "by 0x2201.getSensorDpi()")
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_spi_response = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(test_case=self, sensor_idx=0)
        self.assertEqual(modified_dpi, to_int(get_sensor_spi_response.dpi))

        self.testCaseChecked("BUS_8100_0005", _AUTHOR)
    # end def test_default_dpi_index

    @features("Feature8100")
    @features("Feature2201")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_dpi_shift_dpi_index(self):
        """
        Modify DPI-shift DPI index in the profile 0x0001 and remap the first button as DPI-shift button.
        Validate the resolution index has been updated by 0x8100.getActiveProfileResolution and 0x2201.getSensorDpi
        while press and hold DPI-shift button.
        """
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        btn_index = 0
        dpi_shift_button = ProfileButton.create_function_button(ProfileButton.FunctionExecution.DPI_SHIFT)
        btn_0_to_15 = OnboardProfilesTestUtils.get_default_button_settings(
            test_case=self,  modifier={btn_index: dpi_shift_button})
        shift_dpi_index, shift_dpi = OnboardProfilesTestUtils.get_none_default_dpi(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create a profile 0x0001 from OOB profile 0x0101. Change the shift DPI index to "
                  f"{shift_dpi_index} and remap the first button as DPI-shift button.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(
            test_case=self, modifier={'shift_dpi_index': shift_dpi_index, 'btn_0_to_15': HexList(btn_0_to_15)})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map['shift_dpi_index'] = (checker.check_shift_dpi_index, shift_dpi_index)
        check_map[ProfileFieldName.BUTTON] = (checker.check_button_fields, HexList(btn_0_to_15))
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press and hold DPI-shift button")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.key_press(test_case=self, key_id=KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Validate the DPI index has been changed to {shift_dpi_index} "
                  "by 0x8100.getActiveProfileResolution()")
        # --------------------------------------------------------------------------------------------------------------
        active_profile_resolution = OnboardProfilesTestUtils.HIDppHelper.get_active_profile_resolution(test_case=self)
        self.assertEqual(shift_dpi_index, to_int(active_profile_resolution.resolution_index))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the default DPI has been changed to {shift_dpi} "
                                  "by 0x2201.getSensorDpi()")
        # --------------------------------------------------------------------------------------------------------------
        adjustable_dpi = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(test_case=self, sensor_idx=0)
        self.assertEqual(shift_dpi, to_int(adjustable_dpi.dpi))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release the DPI-shift button")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.key_release(test_case=self, key_id=KEY_ID.BUTTON_1)

        default_dpi_index, default_dpi = OnboardProfilesTestUtils.get_default_dpi(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Validate the DPI index has been changed to {default_dpi_index} "
                  "by 0x8100.getActiveProfileResolution()")
        # --------------------------------------------------------------------------------------------------------------
        active_profile_resolution = OnboardProfilesTestUtils.HIDppHelper.get_active_profile_resolution(test_case=self)
        self.assertEqual(default_dpi_index, to_int(active_profile_resolution.resolution_index))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the default DPI has been changed to {default_dpi} "
                                  "by 0x2201.getSensorDpi()")
        # --------------------------------------------------------------------------------------------------------------
        adjustable_dpi = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(test_case=self, sensor_idx=0)
        self.assertEqual(default_dpi, to_int(adjustable_dpi.dpi))

        self.testCaseChecked("BUS_8100_0006", _AUTHOR)
    # end def test_dpi_shift_dpi_index

    @features("Feature8100")
    @features("Feature2201")
    @level("Business")
    def test_change_default_dpi_resolution(self):
        """
        Modify the default DPI resolution in the profile 0x0001. Validate the DPI has been updated by
        0x2201.getSensorDpi.
        """
        oob_profile_1_index = 0
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        default_dpi_index = self.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[oob_profile_1_index]
        default_dpi_list = self.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DPI_LIST)[oob_profile_1_index]
        default_dpi_list[default_dpi_index] += 100
        modified_default_dpi = default_dpi_list[default_dpi_index]
        dpi_0_to_4 = OnboardProfilesTestUtils.to_raw_dpi_0_to_4(default_dpi_list)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create a profile 0x0001 from OOB profile 0x0101 and change the resolution "
                  f"to {modified_default_dpi}.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(test_case=self, modifier={'dpi_0_to_4': dpi_0_to_4})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=oob_profile_1_index)
        check_map['dpi_0_to_4'] = (checker.check_dpi_0_to_4, dpi_0_to_4)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the default DPI has been changed to {modified_default_dpi} "
                                  "by 0x2201.getSensorDpi()")
        # --------------------------------------------------------------------------------------------------------------
        obtained_dpi = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(test_case=self, sensor_idx=0)
        self.assertEqual(modified_default_dpi, to_int(obtained_dpi.dpi))

        self.testCaseChecked("BUS_8100_0007", _AUTHOR)
    # end def test_change_default_dpi_resolution

    @features("Feature8100")
    @features("Feature8071")
    @features("ProfileFormatV4+")
    @level("Business")
    def test_power_timeout_parameters(self):
        """
        Change the power save timeout to 10 seconds and power off timeout to 30 seconds. Validate the RGB color effect
        shall be changed to passive effect after 10 seconds and the RGB effect be turned off after 30 seconds.

        Require 0x8071, LED analyzer/spy
        """
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        power_save_timeout = 10
        power_off_timeout = 30
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profiles from OOB profiles and change the power save timeout "
                                 "to 10 seconds and power off timeout to 30 seconds. Then create profile directory")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(
            test_case=self, modifier={
                'power_save_timeout': OnboardProfilesTestUtils.to_2_bytes_form(power_save_timeout),
                'power_off_timeout': OnboardProfilesTestUtils.to_2_bytes_form(power_off_timeout)})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map['pwr_save_timeout'] = (checker.check_power_save_timeout, power_save_timeout)
        check_map['pwr_off_timeout'] = (checker.check_power_off_timeout, power_off_timeout)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Validate RGB color effect turns to power save effect by 0x8071.manageRgbPowerModeConfig(0)")
        # --------------------------------------------------------------------------------------------------------------
        manage_rgb_power_mode_config = RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(test_case=self,
                                                                                                    get_or_set=0)
        self.assertEqual(power_save_timeout, to_int(manage_rgb_power_mode_config.rgb_no_act_timeout_to_psave))
        self.assertEqual(power_off_timeout, to_int(manage_rgb_power_mode_config.rgb_no_act_timeout_to_off))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power reset device then wait 10 seconds")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Commented this step because the related check is not ready
        # self.reset(hardware_reset=True)
        # sleep(power_save_timeout + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the RGB color effect by LED analyzer/spy")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require LED analyzer

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power reset device then wait 30 seconds")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Commented this step because the related check is not ready
        # self.reset(hardware_reset=True)
        # sleep(power_off_timeout + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate RGB color effect turned off by LED analyzer/spy")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require LED analyzer

        self.testCaseChecked("BUS_8100_0008", _AUTHOR)
    # end def test_power_timeout_parameters

    @features("Feature8100")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_remap_button(self):
        """
        Remap the first supported button to mouse right button. Validate the button has been remapped to
        the mouse right button.
        """
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        btn_index = ProfileButton.ButtonIndex.BUTTON_1
        mouse_right_button = ProfileButton.create_mouse_button(button_mask=ProfileButton.MouseButton.RIGHT)
        btn_settings = OnboardProfilesTestUtils.ButtonRemapping.from_default_button_settings(
            test_case=self, modifier={btn_index: mouse_right_button})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profiles from OOB profiles and change the first button to mouse right button. "
                                 "Then create profile directory.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(
            test_case=self, modifier={ProfileFieldName.BUTTON: HexList(btn_settings)})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map[ProfileFieldName.BUTTON] = (checker.check_button_fields, HexList(btn_settings))
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Click the button")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        OnboardProfilesTestUtils.keystroke(test_case=self, key_id=KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate device sends the HID packet with expected button state.")
        # --------------------------------------------------------------------------------------------------------------
        SpecialKeysMseButtonsTestUtils.check_hid_packet(
            test_case=self, cid=CidTable.RIGHT_CLICK, action='make', ignore_queue_empty_check=True)
        SpecialKeysMseButtonsTestUtils.check_hid_packet(test_case=self, cid=CidTable.RIGHT_CLICK, action='break')

        self.testCaseChecked("BUS_8100_0009", _AUTHOR)
    # end def test_remap_button

    @features("Feature8100")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_1, KEY_ID.BUTTON_2))
    def test_remap_g_shift_button(self):
        """
        Remap the first g-shift button to mouse right button and remap 2nd button as g-shift button. Validate the
        button has been remapped to the mouse right button by press and hold g-shift button and click the first button.
        """
        profile_1 = OnboardProfiles.SectorId.PROFILE_START

        g_shift_btn_index = ProfileButton.ButtonIndex.BUTTON_1
        mouse_middle_button = ProfileButton.create_mouse_button(button_mask=ProfileButton.MouseButton.MIDDLE)
        g_shift_btn_settings = OnboardProfilesTestUtils.ButtonRemapping.from_default_button_settings(
            test_case=self, button_type=ProfileButton.ButtonType.G_SHIFT,
            modifier={g_shift_btn_index: mouse_middle_button})

        btn_index = ProfileButton.ButtonIndex.BUTTON_2
        g_shift_button = ProfileButton.create_function_button(function_type=ProfileButton.FunctionExecution.G_SHIFT)
        btn_settings = OnboardProfilesTestUtils.ButtonRemapping.from_default_button_settings(
            test_case=self, modifier={btn_index: g_shift_button})
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profiles from OOB profiles and change the first g-shift button to mouse right "
                                 "button and remap the 2nd button as g-shift button. Then create profile directory.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        btn_field_name = OnboardProfilesTestUtils.get_btn_field_name(test_case=self)
        g_shift_btn_field_name = OnboardProfilesTestUtils.get_g_shift_btn_field_name(test_case=self)
        OnboardProfilesTestUtils.Profile.create_default_profiles(
            test_case=self,
            modifier={btn_field_name: HexList(btn_settings), g_shift_btn_field_name: HexList(g_shift_btn_settings)})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map[ProfileFieldName.BUTTON] = (checker.check_button_fields, HexList(btn_settings))
        check_map[ProfileFieldName.G_SHIFT_BUTTON] = (checker.check_g_shift_button_fields,
                                                      HexList(g_shift_btn_settings))
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Click the button")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        OnboardProfilesTestUtils.perform_action_list(
            test_case=self,
            action_list=[[KEY_ID.BUTTON_2, MAKE], [KEY_ID.BUTTON_1, KEYSTROKE], [KEY_ID.BUTTON_2, BREAK]])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate device sends the HID packet with expected button state.")
        # --------------------------------------------------------------------------------------------------------------
        SpecialKeysMseButtonsTestUtils.check_hid_packet(
            test_case=self, cid=CidTable.MIDDLE_BUTTON, action=MAKE, ignore_queue_empty_check=True)
        SpecialKeysMseButtonsTestUtils.check_hid_packet(test_case=self, cid=CidTable.MIDDLE_BUTTON, action=BREAK)

        self.testCaseChecked("BUS_8100_0010", _AUTHOR)
    # end def test_remap_g_shift_button

    @features("Feature8100")
    @features("ProfileFormatV2+")
    @level("Business")
    def test_change_active_rgb_effect(self):
        """
        Change the default active RGB effect and write it into the profile. Validate the current active RGB effect
        has been changed to the new RGB effect.

        Require LED analyzer/spy
        """
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        fixed_color_effect = [RGBEffects.RGBEffectID.FIXED, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        active_rgb_effect_field_name = 'logo_effect'
        modified_lightning_flag = None
        if self.config.F_ProfileFormatID == 4:
            active_rgb_effect_field_name = 'logo_active_effect'
        elif self.config.F_ProfileFormatID == 5:
            modified_lightning_flag = OnboardProfilesTestUtils.adjust_lightning_flag_by_rgb_effect_id(
                test_case=self, power_mode='active', rgb_effect_id=RGBEffects.RGBEffectID.FIXED)
            active_rgb_effect_field_name = OnboardProfilesTestUtils.get_rgb_effect_stored_field_name(
                power_mode='active', lightning_flag=modified_lightning_flag)
        # end if
        active_rgb_effect_field_name_checker = \
            OnboardProfilesTestUtils.get_rgb_effect_stored_field_checker(active_rgb_effect_field_name)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a profile 0x0001 from OOB profile 0x0101 and change the active RGB color "
                                 "effect to Fixed red color effect.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        if modified_lightning_flag is None:
            OnboardProfilesTestUtils.Profile.create_default_profiles(
                    test_case=self, modifier={active_rgb_effect_field_name: HexList(fixed_color_effect)})
        else:
            OnboardProfilesTestUtils.Profile.create_default_profiles(
                    test_case=self, modifier={active_rgb_effect_field_name: HexList(fixed_color_effect),
                                              'lightning_flag': modified_lightning_flag})
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map[active_rgb_effect_field_name] = (active_rgb_effect_field_name_checker, fixed_color_effect)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        if modified_lightning_flag is not None:
            check_map['lightning_flag'] = (checker.check_lightning_flag,  modified_lightning_flag)
        # end if
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a user action to make sure the DUT is in run mode")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the active RGB color effect by LED analyzer/spy")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require LED analyzer

        self.testCaseChecked("BUS_8100_0011", _AUTHOR)
    # end def test_change_active_rgb_effect

    @features("Feature8100")
    @features("ProfileFormatV4+")
    @level("Business")
    def test_change_passive_rgb_effect(self):
        """
        Change the default passive RGB effect and write it into the profile. Validate the current passive RGB effect
        has been changed to the new RGB effect after power save timeout.

        Require LED analyzer/spy
        """
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        disabled_color_effect = [RGBEffects.RGBEffectID.DISABLED, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        passive_rgb_effect_field_name = 'logo_passive_effect'
        modified_lightning_flag = None
        if self.config.F_ProfileFormatID == 5:
            modified_lightning_flag = OnboardProfilesTestUtils.adjust_lightning_flag_by_rgb_effect_id(
                test_case=self, power_mode='passive', rgb_effect_id=RGBEffects.RGBEffectID.DISABLED)
            passive_rgb_effect_field_name = OnboardProfilesTestUtils.get_rgb_effect_stored_field_name(
                power_mode='passive', lightning_flag=modified_lightning_flag)
        # end if
        passive_rgb_effect_field_name_checker = \
            OnboardProfilesTestUtils.get_rgb_effect_stored_field_checker(
                rgb_effect_stored_field_name=passive_rgb_effect_field_name)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a profile 0x0001 from OOB profile 0x0101 and change the passive RGB color "
                                 "effect to disabled color effect. Then create profile directory.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        if modified_lightning_flag is None:
            OnboardProfilesTestUtils.Profile.create_default_profiles(
                    test_case=self, modifier={passive_rgb_effect_field_name: HexList(disabled_color_effect)})
        else:
            OnboardProfilesTestUtils.Profile.create_default_profiles(
                    test_case=self, modifier={passive_rgb_effect_field_name: HexList(disabled_color_effect),
                                              'lightning_flag': modified_lightning_flag})
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Validate the active RGB color effect has been changed to Fixed red color effect by 0x8071")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=0)
        check_map[passive_rgb_effect_field_name] = (passive_rgb_effect_field_name_checker, disabled_color_effect)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(
            sector_raw_data=HexList(profile)[:-2]))
        if modified_lightning_flag is not None:
            check_map['lightning_flag'] = (checker.check_lightning_flag, modified_lightning_flag)
        # end if
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a user action then wait until entered power save mode")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Commented this step because the related check is not ready
        # self.button_stimuli_emulator.user_action()
        # sleep(self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_POWER_SAVE_TIMEOUT)[0] + 2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the active RGB color effect by LED analyzer/spy")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require LED analyzer

        self.testCaseChecked("BUS_8100_0012", _AUTHOR)
    # end def test_change_passive_rgb_effect

    @features("Feature8100")
    @features("PluralProfiles")
    @level("Business")
    def test_visit_all_possible_profiles(self):
        """
        Add profiles up to the maximum quantum. Visit to all of profiles by setActiveProfile(). Validate the active
        profile and profile LED indication color has been changed.

        Color: White, Orange, Cyan, Yellow, Magenta (with fast blinking)
        """
        profile_count = self.config.F_ProfileCount
        oob_profile_1 = OnboardProfiles.SectorId.OOB_PROFILE_START
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        directory_items = {}
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a profile 0x0001..0x000{profile_count} from OOB profile 0x0101")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        for idx in range(profile_count):
            OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(
                test_case=self, oob_profile_id=oob_profile_1, dest_profile_id=profile_1 + idx)
            directory_items[profile_1 + idx] = ProfileDirectory.Item(sector_id=profile_1 + idx,
                                                                     enabled=OnboardProfiles.Status.ENABLED)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_profile_directory(test_case=self,
                                                                            directory_items=directory_items)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over ProfileID in Profiles")
        # --------------------------------------------------------------------------------------------------------------
        for idx in reversed(range(profile_count)):
            profile_id = profile_1 + idx
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Activate profile {profile_id} by setActiveProfile()")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the profile indicator by LED analyzer")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Require LED analyzer

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate the current active profile is {profile_id} by getActiveProfile()")
            # ----------------------------------------------------------------------------------------------------------
            active_profile = OnboardProfilesTestUtils.HIDppHelper.get_active_profile(test_case=self)
            checker = OnboardProfilesTestUtils.GetActiveProfileResponseChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map['profile_id'] = (checker.check_profile_id, profile_id)
            checker.check_fields(test_case=self, message=active_profile,
                                 expected_cls=self.feature_8100.get_active_profile_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End of Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8100_0013", _AUTHOR)
    # end def test_visit_all_possible_profiles

    @features("Feature8100")
    @features("PluralProfiles")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_visit_all_possible_profiles_by_button(self):
        """
        Add profiles up to the maximum quantum. Visit to all of profiles by profile button. Validate the active
        profile and profile LED indication color has been changed.

        Color: White, Orange, Cyan, Yellow, Magenta (with fast blinking)
        """
        profile_count = self.config.F_ProfileCount
        oob_profile_1 = OnboardProfiles.SectorId.OOB_PROFILE_START
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        directory_items = {}
        btn_index = 0
        btn_field_name = OnboardProfilesTestUtils.get_btn_field_name(test_case=self)
        profile_cycle_button = ProfileButton.create_function_button(
            function_type=ProfileButton.FunctionExecution.CYCLE_THROUGH_PROFILE)
        btn_0_to_15 = OnboardProfilesTestUtils.get_default_button_settings(
            test_case=self, modifier={btn_index: profile_cycle_button})
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a profile 0x0001..0x000{profile_count} from OOB profile 0x0101")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        for idx in range(profile_count):
            OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(
                test_case=self, oob_profile_id=oob_profile_1, dest_profile_id=profile_1 + idx,
                modifier={btn_field_name: HexList(btn_0_to_15)})
            directory_items[profile_1 + idx] = ProfileDirectory.Item(sector_id=profile_1 + idx,
                                                                     enabled=OnboardProfiles.Status.ENABLED)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_profile_directory(test_case=self,
                                                                            directory_items=directory_items)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over ProfileID in Profiles")
        # --------------------------------------------------------------------------------------------------------------
        for idx in range(self.config.F_ProfileCount):
            profile_id = (profile_1 + 1 + idx)
            if profile_id > self.config.F_ProfileCount:
                profile_id %= self.config.F_ProfileCount
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Press ProfileButton")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.keystroke(test_case=self, key_id=KEY_ID.BUTTON_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the profile indicator by LED analyzer")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Require LED analyzer

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate the current active profile is {profile_id} by getActiveProfile()")
            # ----------------------------------------------------------------------------------------------------------
            active_profile = OnboardProfilesTestUtils.HIDppHelper.get_active_profile(test_case=self)
            checker = OnboardProfilesTestUtils.GetActiveProfileResponseChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map['profile_id'] = (checker.check_profile_id, profile_id)
            checker.check_fields(test_case=self, message=active_profile,
                                 expected_cls=self.feature_8100.get_active_profile_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End of Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8100_0014", _AUTHOR)
    # end def test_visit_all_possible_profiles_by_button

    @features("Feature8100")
    @level("Business")
    def test_profiles_crc(self):
        """
        Initialize onboard profiles by OOB profile. Loop over each onboard profiles. Validate there is no error while
        doing initialization, change profiles and check CRC value by getCrc().
        """
        profile_count = self.config.F_ProfileCount
        oob_profile_1 = OnboardProfiles.SectorId.OOB_PROFILE_START
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        directory_items = {}
        crc_list = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a profile 0x0001..0x000{profile_count} from OOB profile 0x0101")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        for idx in range(profile_count):
            crc_list.append(OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(
                test_case=self, oob_profile_id=oob_profile_1, dest_profile_id=profile_1 + idx))
            directory_items[profile_1 + idx] = ProfileDirectory.Item(sector_id=profile_1 + idx,
                                                                     enabled=OnboardProfiles.Status.ENABLED)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_profile_directory(test_case=self,
                                                                            directory_items=directory_items)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update crc check map")
        # --------------------------------------------------------------------------------------------------------------
        checker = OnboardProfilesTestUtils.GetCrcResponseChecker
        check_map = checker.get_check_map(count=self.config.F_SectorCount - profile_1)
        for idx in range(profile_count):
            profile_id = profile_1 + idx
            field_name = f'crc_{profile_id}'
            expected_crc = crc_list[idx]
            check_method = getattr(checker, f'check_crc_{profile_id}')
            check_map[field_name] = (check_method, expected_crc)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over ProfileID in [Profiles]")
        # --------------------------------------------------------------------------------------------------------------
        for idx in range(profile_count):
            profile_id = profile_1 + idx
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setActiveProfile with {profile_id}")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate no error returned")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getCrc()")
            # ----------------------------------------------------------------------------------------------------------
            crc = OnboardProfilesTestUtils.HIDppHelper.get_crc(test_case=self, sector_id=profile_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the CRC value received from device")
            # ----------------------------------------------------------------------------------------------------------
            checker.check_fields(test_case=self, message=crc,
                                 expected_cls=self.feature_8100.get_crc_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End of Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8100_0015", _AUTHOR)
    # end def test_profiles_crc

    @features("Feature8100")
    @features("PluralProfiles")
    @level("Business")
    def test_active_profiles_wont_change_after_power_reset(self):
        """
        Create onboard profiles from OOB profiles. Loop over the OOB profiles then set the new created onboard profiles
        as active profile. Power reset device then validate the active profile shall not be changed.
        """
        profile_count = self.config.F_ProfileCount
        oob_profile_1 = OnboardProfiles.SectorId.OOB_PROFILE_START
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        directory_items = {}
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a profile 0x0001..0x000{profile_count} from OOB profile 0x0101")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        for idx in range(profile_count):
            OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(
                test_case=self, oob_profile_id=oob_profile_1, dest_profile_id=profile_1 + idx)
            directory_items[profile_1 + idx] = ProfileDirectory.Item(sector_id=profile_1 + idx,
                                                                     enabled=OnboardProfiles.Status.ENABLED)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_profile_directory(test_case=self,
                                                                            directory_items=directory_items)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over ProfileID in [Profiles]")
        # --------------------------------------------------------------------------------------------------------------
        for idx in reversed(range(profile_count)):
            profile_id = profile_1 + idx
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setActiveProfile with {profile_id}")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate the active profile has been changed to {profile_id}")
            # ----------------------------------------------------------------------------------------------------------
            active_profile = OnboardProfilesTestUtils.HIDppHelper.get_active_profile(test_case=self)
            checker = OnboardProfilesTestUtils.GetActiveProfileResponseChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map['profile_id'] = (checker.check_profile_id, profile_id)
            checker.check_fields(test_case=self, message=active_profile,
                                 expected_cls=self.feature_8100.get_active_profile_response_cls, check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power reset DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validate the active profile {profile_id} shall not be changed")
            # ----------------------------------------------------------------------------------------------------------
            active_profile = OnboardProfilesTestUtils.HIDppHelper.get_active_profile(test_case=self)
            checker = OnboardProfilesTestUtils.GetActiveProfileResponseChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map['profile_id'] = (checker.check_profile_id, profile_id)
            checker.check_fields(test_case=self, message=active_profile,
                                 expected_cls=self.feature_8100.get_active_profile_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End of Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8100_0016", _AUTHOR)
    # end def test_active_profiles_wont_change_after_power_reset

    @features("Feature8100")
    @features("PluralProfiles")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_profile_activated_event_by_button(self):
        """
        Validate device sends the profileActivated event after pressed Profile button.
        """
        oob_profile_1 = OnboardProfiles.SectorId.OOB_PROFILE_START
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        profile_2 = OnboardProfiles.SectorId.PROFILE_START + 1
        btn_index = 0
        btn_field_name = OnboardProfilesTestUtils.get_btn_field_name(test_case=self)
        profile_cycle_button = ProfileButton.create_function_button(
            function_type=ProfileButton.FunctionExecution.CYCLE_THROUGH_PROFILE)
        btn_0_to_15 = OnboardProfilesTestUtils.get_default_button_settings(
            test_case=self, modifier={btn_index: profile_cycle_button})
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a profile 0x0001 from OOB profile 0x0101 and remap the button 1"
                                 "as ProfileButton")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(
            test_case=self, oob_profile_id=oob_profile_1,
            dest_profile_id=profile_1, modifier={btn_field_name: HexList(btn_0_to_15)})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a profile 0x0002 from OOB profile 0x0101")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(
            test_case=self, oob_profile_id=oob_profile_1,
            dest_profile_id=profile_2, modifier={btn_field_name: HexList(btn_0_to_15)})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_profile_directory(
            test_case=self, directory_items={
                profile_1: ProfileDirectory.Item(sector_id=profile_1, enabled=OnboardProfiles.Status.ENABLED),
                profile_2: ProfileDirectory.Item(sector_id=profile_2, enabled=OnboardProfiles.Status.ENABLED)})
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results")
        # --------------------------------------------------------------------------------------------------------------
        for profile_id in [profile_1, profile_2]:
            profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_id)
            check_map = OnboardProfilesTestUtils.ProfileChecker.get_check_map(test_case=self, index=0)
            check_map[ProfileFieldName.BUTTON] = (OnboardProfilesTestUtils.ProfileChecker.check_button_fields,
                                                  HexList(btn_0_to_15))
            check_map['crc'] = (OnboardProfilesTestUtils.ProfileChecker.check_crc,
                                OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
            OnboardProfilesTestUtils.ProfileChecker.check_fields(test_case=self, message=profile,
                                                                 expected_cls=type(profile), check_map=check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pressed ProfileButton")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        OnboardProfilesTestUtils.keystroke(test_case=self, key_id=KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate device sends profileActivated event")
        # --------------------------------------------------------------------------------------------------------------
        profile_activated_event = ChannelUtils.get_only(test_case=self,
                                                        queue_name=HIDDispatcher.QueueName.EVENT,
                                                        class_type=self.feature_8100.profile_activated_event_cls)
        checker = OnboardProfilesTestUtils.ProfileActivatedEventChecker
        check_map = checker.get_default_check_map(test_case=self)
        check_map['profile_id'] = (checker.check_profile_id, profile_2)
        checker.check_fields(
            test_case=self, message=profile_activated_event,
            expected_cls=self.feature_8100.profile_activated_event_cls, check_map=check_map)

        self.testCaseChecked("BUS_8100_0017", _AUTHOR)
    # end def test_profile_activated_event_by_button

    @features("Feature8100")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_resolution_changed_event_by_button(self):
        """
        Validate device sends the activeProfileResolutionChanged event after pressed DPI button.
        """
        oob_profile_1 = OnboardProfiles.SectorId.OOB_PROFILE_START
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        btn_index = 0
        btn_field_name = OnboardProfilesTestUtils.get_btn_field_name(test_case=self)
        dpi_cycle_button = ProfileButton.create_function_button(
            function_type=ProfileButton.FunctionExecution.CYCLE_THROUGH_DPI)
        btn_0_to_15 = OnboardProfilesTestUtils.get_default_button_settings(
            test_case=self, modifier={btn_index: dpi_cycle_button})
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a profile 0x0001 from OOB profile 0x0101 and remap the button 1 "
                                 "as DPI Cycling Button.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_profile_by_oob_profile(
            test_case=self, oob_profile_id=oob_profile_1,
            dest_profile_id=profile_1, modifier={btn_field_name: HexList(btn_0_to_15)})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create profile directory and set profile 0x0001 as active profile.")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_profile_directory(
            test_case=self, directory_items={
                profile_1: ProfileDirectory.Item(sector_id=profile_1, enabled=OnboardProfiles.Status.ENABLED)})
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        check_map = OnboardProfilesTestUtils.ProfileChecker.get_check_map(self, 0)
        check_map[ProfileFieldName.BUTTON] = \
            (OnboardProfilesTestUtils.ProfileChecker.check_button_fields, HexList(btn_0_to_15))
        check_map['crc'] = (OnboardProfilesTestUtils.ProfileChecker.check_crc,
                            OnboardProfilesTestUtils.calculate_crc(sector_raw_data=HexList(profile)[:-2]))
        OnboardProfilesTestUtils.ProfileChecker.check_fields(test_case=self, message=profile,
                                                             expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pressed DPICyclingButton.")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        OnboardProfilesTestUtils.keystroke(test_case=self, key_id=KEY_ID.BUTTON_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate device sends activeProfileResolutionChanged event.")
        # --------------------------------------------------------------------------------------------------------------
        event = ChannelUtils.get_only(test_case=self,
                                      queue_name=HIDDispatcher.QueueName.EVENT,
                                      class_type=self.feature_8100.active_profile_resolution_changed_event_cls)
        expected_resolution_index = self.config_manager.get_feature(
            feature_id=ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[0] + 1
        checker = OnboardProfilesTestUtils.ActiveProfileResolutionChangedEventChecker
        check_map = checker.get_default_check_map(test_case=self)
        check_map['resolution_index'] = (checker.check_resolution_index, expected_resolution_index)
        checker.check_fields(
            test_case=self, message=event,
            expected_cls=self.feature_8100.active_profile_resolution_changed_event_cls, check_map=check_map)

        self.testCaseChecked("BUS_8100_0018", _AUTHOR)
    # end def test_resolution_changed_event_by_button

    @features("Feature8100")
    @features("Feature8061")
    @level("Business")
    def test_report_rate_wireless(self):
        """
        [ProfileFormatV6] Check the wireless report rate can be changed by profile. And validate it
        by 0x8061.getReportRate().
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create a profile 0x0001 from OOB profile 0x0101 and change the wireless report rate to "
                  "{none default setting}.")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require none default wired report rate from 0x8061 test configurations

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Depending on previous step

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Depending on previous step

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Validate the wireless report rate has been changed to {none default setting} "
                  "by 0x8061.getReportRate().")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require 0x8061

        self.testCaseChecked("BUS_8100_0019", _AUTHOR)
    # end def test_report_rate_wireless

    @features("Feature8100")
    @features("Feature8061")
    @level("Business")
    def test_report_rate_wired(self):
        """
        [ProfileFormatV6] Check the wired report rate can be changed by profile. And validate it
        by 0x8061.getReportRate().
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create a profile 0x0001 from OOB profile 0x0101 and change the wired report rate to "
                  "{none default setting}.")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require none default wired report rate from 0x8061 test configurations

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Depending on previous step

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Depending on previous step

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Validate the wired report rate has been changed to {none default setting} "
                  "by 0x8061.getReportRate().")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require 0x8061

        self.testCaseChecked("BUS_8100_0020", _AUTHOR)
    # end def test_report_rate_wired

    @features("Feature8100")
    @features("Feature2202")
    @level("Business")
    def test_change_first_dpi_xy_lod(self):
        """
        [ProfileFormatV6] Check the DPI X, Y and LOD can be changed by profile. And validate it
        by 0x2202.getSensorDpiParameters(). 
        """
        oob_profile_1_index = 0
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        default_dpi_index = self.config_manager.get_feature(
            feature_id=ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[oob_profile_1_index]
        default_dpi_list = self.config_manager.get_feature(
            feature_id=ConfigurationManager.ID.OOB_PROFILES_DPI_XY_LIST)[oob_profile_1_index]
        default_dpi_list[default_dpi_index][0] += 100  # DPI X
        default_dpi_list[default_dpi_index][1] += 100  # DPI Y
        default_dpi_list[default_dpi_index][2] = 1 if default_dpi_list[default_dpi_index][2] != 1 else 1  # LOD
        dpi_xy_0_to_4 = OnboardProfilesTestUtils.to_raw_dpi_0_to_4(dpi_list=default_dpi_list)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create a profile 0x0001 from OOB profile 0x0101 and change the DPI X, Y and LOD to "
                  f"{default_dpi_list}.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(test_case=self,
                                                                 modifier={'dpi_xy_0_to_4': dpi_xy_0_to_4})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=oob_profile_1_index)
        check_map['dpi_xy_0_to_4'] = (checker.check_dpi_xy_0_to_4, dpi_xy_0_to_4)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate the DPI X, Y and LOD has been changed to {default_dpi_list} "
                                  "by 0x2202.getSensorDpiParameters()")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require 0x2202 feature class and its utils

        self.testCaseChecked("BUS_8100_0021", _AUTHOR)
    # end def test_change_first_dpi_xy_lod

    @features("Feature8100")
    @features("Feature2202")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.LEFT_BUTTON,))
    def test_change_delta_xy(self):
        """
        [ProfileFormatV6] Validate the DPI DeltaX and DeltaY in the profile be applied in the DPI calibration.
        """
        oob_profile_1_index = 0
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        none_default_dpi_delta_x = \
            self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_DPI_DELTA_X)[oob_profile_1_index] + 100
        none_default_dpi_delta_y = \
            self.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_DPI_DELTA_Y)[oob_profile_1_index] + 100

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create a profile 0x0001 from OOB profile 0x0101 and change the DPI Delta X, Y "
                  f"to delta x: {none_default_dpi_delta_x}, delta y: {none_default_dpi_delta_y}.")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        OnboardProfilesTestUtils.Profile.create_default_profiles(
            test_case=self, modifier={'dpi_delta_x': none_default_dpi_delta_x, 'dpi_delta_y': none_default_dpi_delta_y})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case=self)
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case=self, profile_id=profile_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
        # --------------------------------------------------------------------------------------------------------------
        profile = OnboardProfilesTestUtils.Profile.read_profile(test_case=self, profile_id=profile_1)
        checker = OnboardProfilesTestUtils.ProfileChecker
        check_map = checker.get_check_map(test_case=self, index=oob_profile_1_index)
        check_map['dpi_delta_x'] = (checker.check_dpi_delta_x, none_default_dpi_delta_x)
        check_map['dpi_delta_y'] = (checker.check_dpi_delta_y, none_default_dpi_delta_y)
        check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
        checker.check_fields(test_case=self, message=profile, expected_cls=type(profile), check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start DPI calibration by HW process by 0x2202.startDpiCalibration")
        # -------------------------------------------------------------------------------------------------------------
        # TODO: Require 0x2202 feature class and its utils

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start DPI calibration by left button press and hold 6 seconds then release "
                                 "the button to stop process")
        # -------------------------------------------------------------------------------------------------------------
        # TODO: Require 0x2202 feature class and its utils

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the DPI Delta X, Y from 0x2202.dpiCalibrationCompletedEvent")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Require 0x2202 feature class and its utils

        self.testCaseChecked("BUS_8100_0022", _AUTHOR)
    # end def test_change_delta_xy
# end class OnboardProfilesBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
