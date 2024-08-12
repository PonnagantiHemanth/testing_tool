#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8101.business
:brief: HID++ 2.0 ``ProfileManagement`` business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/04/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from time import time_ns

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HidConsumer
from pyhid.hid import HidKeyboardBitmap
from pyhid.hid import HidKeyboard
from pyhid.hid import HidMouse
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hiddata import HidData
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.gaming.profilemanagement import EditBuffer
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.gaming.profilemanagement import ReadBufferResponse
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDX
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.mcu.fkcprofileformat import NOT_REMAPPABLE_KEY_LIST
from pylibrary.mcu.fkcprofileformat import PROFILE_TAG_INFO_MAP
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.mcu.fkcprofileformat import TagField_11_Bytes
from pylibrary.mcu.fkcprofileformat import TagField_16_Bytes
from pylibrary.mcu.profileformat import AcPanCommand
from pylibrary.mcu.profileformat import ConsumerKeyCommand
from pylibrary.mcu.profileformat import JumpCommand
from pylibrary.mcu.profileformat import KeyAction
from pylibrary.mcu.profileformat import MacroEndCommand
from pylibrary.mcu.profileformat import MouseButtonCommand
from pylibrary.mcu.profileformat import PresetMacroEntry
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.mcu.profileformat import RepeatUntilCancelCommand
from pylibrary.mcu.profileformat import RepeatWhilePressedCommand
from pylibrary.mcu.profileformat import RollerCommand
from pylibrary.mcu.profileformat import StandardKeyCommand
from pylibrary.mcu.profileformat import WaitForReleaseCommand
from pylibrary.mcu.profileformat import WaitForXmsCommand
from pylibrary.mcu.profileformat import XYCommand
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.hidpp20.gaming.feature_8101.profilemanagement import ProfileManagementTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ProfileManagementBusinessTestCase(ProfileManagementTestCase):
    """
    Validate ``ProfileManagement`` business test cases
    """

    @features("Feature8101")
    @level('Business', 'SmokeTests')
    def test_correctness_of_oob_profile_and_directory(self):
        """
        Validate the correctness of OOB profile directory and profile settings
        """
        expected_oob_profile_directory = \
            HexList(ProfileManagementTestUtils.ProfileHelper.get_oob_directory_from_settings(self))
        expected_oob_profile = \
            HexList(ProfileManagementTestUtils.ProfileHelper.get_oob_profile_from_settings(self))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load and readBuffer request to load OOB profile")
        # --------------------------------------------------------------------------------------------------------------
        oob_profile = HexList(ProfileManagementTestUtils.ProfileHelper.get_oob_profile(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the data matches the profile settings")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range((len(oob_profile) // (ReadBufferResponse.LEN.DATA // 8)) + 1):
            self.assertEqual(
                expected=expected_oob_profile[offset * (ReadBufferResponse.LEN.DATA // 8):
                                              (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                obtained=oob_profile[offset * (ReadBufferResponse.LEN.DATA // 8):
                                     (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                msg=f"The data parameter differs found at offset {offset * (ReadBufferResponse.LEN.DATA // 8)}, "
                    f"(expected:{expected_oob_profile}, obtained:{oob_profile})")
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load and readBuffer request to load OOB profile directory")
        # --------------------------------------------------------------------------------------------------------------
        oob_profile_directory = HexList(ProfileManagementTestUtils.ProfileHelper.get_oob_directory(test_case=self))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait readBuffer response and check the content of directory is as expected")
        # --------------------------------------------------------------------------------------------------------------
        for offset in range((len(oob_profile_directory) // (ReadBufferResponse.LEN.DATA // 8)) + 1):
            self.assertEqual(
                expected=expected_oob_profile_directory[offset * (ReadBufferResponse.LEN.DATA // 8):
                                                        (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                obtained=oob_profile_directory[offset * (ReadBufferResponse.LEN.DATA // 8):
                                               (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                msg=f"The data parameter differs found at offset {offset * (ReadBufferResponse.LEN.DATA // 8)}, "
                    f"(expected:{expected_oob_profile_directory}, obtained:{oob_profile_directory})")
        # end for

        self.testCaseChecked("BUS_8101_0001", _AUTHOR)
    # end def test_correctness_of_oob_profile_and_directory

    @features("Feature8101")
    @level("Business")
    def test_power_on_profile_not_updated_when_switching_to_host_profile(self):
        """
        Validate the FW shall not update the power-on profile when the user switches to host profiles
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
            LogHelper.log_step(self, f"Create a onboard profile with file_id={index} from a settings and link the"
                                     "file ID of FKC with the created FKC base layer file")
            # ----------------------------------------------------------------------------------------------------------
            profiles.append(ProfileManagementTestUtils.ProfileHelper.create_profile_from_settings(
                self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE))

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
        LogHelper.log_step(self, f"Send configure request with file_id={host_profile.file_id_lsb}, file_type_id=0")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE,
                                            file_id=host_profile.file_id_lsb,
                                            count=len(HexList(host_profile)),
                                            crc_32=host_profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSetPowerOnParams request with set_power_on_profile=0")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self, set_power_on_profile=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getSetPowerOnParams response and check the power_on_profile is not the"
                                  f"{host_profile.file_id_lsb}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.GetSetPowerOnParamsResponseChecker.check_fields(
            self, response, self.feature_8101.get_set_power_on_params_response_cls)

        self.testCaseChecked("BUS_8101_0002", _AUTHOR)
    # end def test_power_on_profile_not_updated_when_switching_to_host_profile

    @features("Feature8101")
    @level("Business")
    def test_power_on_profile_is_updated_when_switching_to_onboard_profile(self):
        """
        Validate the FW shall update the power-on profile when the user switches to onboard profiles
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        _, onboard_profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        onboard_profile = onboard_profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={onboard_profile.file_id_lsb}, file_type_id=0")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=onboard_profile.file_id_lsb,
            count=len(HexList(onboard_profile)),
            crc_32=onboard_profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSetPowerOnParams request with set_power_on_profile=0")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.get_set_power_on_params(
            test_case=self, set_power_on_profile=ProfileManagementTestUtils.RequestType.GET,
            power_on_profile=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getSetPowerOnParams response and check the power_on_profile is the onboard"
                                  "profile")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.GetSetPowerOnParamsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            'power_on_profile': (checker.check_power_on_profile, onboard_profile.file_id_lsb)})
        checker.check_fields(self, response, self.feature_8101.get_set_power_on_params_response_cls, check_map)

        self.testCaseChecked("BUS_8101_0003", _AUTHOR)
    # end def test_power_on_profile_is_updated_when_switching_to_onboard_profile

    @features("Feature8101")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.FN_KEY, KEY_ID.ONBOARD_PROFILE_1,))
    @services('SimultaneousKeystrokes')
    def test_profile_change_event_sent_after_switching_profile_thru_shortcut(self):
        """
        Validate the profileChangeEvent is sent when the user changed the profile thru shortcut keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create {self.config.F_NumOnboardProfiles} onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        profiles = self.create_onboard_profiles_and_save_in_nvs(test_case=self, directory=directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Press FN + {self.button_stimuli_emulator.get_fn_keys()[KEY_ID.ONBOARD_PROFILE_1]!s} "
                  "to switch to the user profile")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
        sleep(0.05)
        self.button_stimuli_emulator.keystroke(
            key_id=self.button_stimuli_emulator.get_fn_keys()[KEY_ID.ONBOARD_PROFILE_1], delay=1)
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait profileChangeEvent and check the nwe_profile is as expected")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
        checker = ProfileManagementTestUtils.ProfileChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({'new_profile': (checker.check_new_profile, profiles[0].file_id_lsb)})
        checker.check_fields(self, response, self.feature_8101.profile_change_event_cls, check_map)

        self.testCaseChecked("BUS_8101_0004", _AUTHOR)
    # end def test_profile_change_event_sent_after_switching_profile_thru_shortcut

    @features("Feature8101")
    @level("Business")
    def test_profile_change_event_not_sent_when_switching_profile_thru_software(self):
        """
        Validate the profileChangeEvent is not sent when the user changed the profile thru software
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        _, onboard_profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        onboard_profile = onboard_profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={onboard_profile.file_id_lsb}, file_type_id=0")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
            file_id=onboard_profile.file_id_lsb,
            count=len(HexList(onboard_profile)),
            crc_32=onboard_profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no profileChangeEvent is sent from the device")
        # --------------------------------------------------------------------------------------------------------------
        response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                         class_type=self.feature_8101.profile_change_event_cls,
                                         check_first_message=False,
                                         allow_no_message=True)
        self.assertNone(obtained=response,
                        msg="The ProfileChangeEvent should not be received when the user changes the profile thru "
                            "software.")

        self.testCaseChecked("BUS_8101_0005", _AUTHOR)
    # end def test_profile_change_event_not_sent_when_switching_profile_thru_software

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_cycle_thru_onboard_profiles(self):
        """
        Validate the user can cycle thru the onboard profiles, if the device supports multiple onboard profiles. (It
        means that the user can cycle thru the profiles rather than select them individually)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create {self.config.F_NumOnboardProfiles} onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        profiles = self.create_onboard_profiles_and_save_in_nvs(test_case=self, directory=directory, save_in_nvs=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC base layer table file to remap a key to cycle thru onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION, trigger_key=self.trigger_key,
                        action_key=KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over index in range({self.config.F_NumOnboardProfiles})")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(self.config.F_NumOnboardProfiles):
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
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profiles[0].file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profiles[0].file_id_lsb,
                                            count=directory.files[profiles[0].file_id_lsb].n_bytes,
                                            crc_32=profiles[0].crc_32)

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
        LogHelper.log_info(self, f"Test Loop: Loop over index in range({self.config.F_NumOnboardProfiles})")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(self.config.F_NumOnboardProfiles):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press the {self.trigger_key} to cycle thru the onboard profiles")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=self.trigger_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait profileChangeEvent and check the nwe_profile is as expected")
            # ----------------------------------------------------------------------------------------------------------
            response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
            checker = ProfileManagementTestUtils.ProfileChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({'new_profile':
                             (checker.check_new_profile,
                              profiles[0 if index == self.config.F_NumOnboardProfiles - 1 else index + 1].file_id_lsb)})
            checker.check_fields(self, response, self.feature_8101.profile_change_event_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8101_0006", _AUTHOR)
    # end def test_cycle_thru_onboard_profiles

    @features("Feature8101")
    @features("Feature8071")
    @level("Business")
    def test_configure_active_effect_on_primary_cluster(self):
        """
        Validate users can configure the all the device supported effects on the primary cluster as the active
        effects
        """
        self._test_configure_effects_on_the_clusters(cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                                     is_active=True)

        self.testCaseChecked("BUS_8101_0007", _AUTHOR)
    # end def test_configure_active_effect_on_primary_cluster

    @features("Feature8101")
    @features("Feature8071")
    @level("Business")
    def test_configure_passive_effect_on_primary_cluster(self):
        """
        Validate users can configure the all the device supported effects on the primary cluster as the passive
        effects
        """
        self._test_configure_effects_on_the_clusters(cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                                     is_active=False)

        self.testCaseChecked("BUS_8101_0008", _AUTHOR)
    # end def test_configure_passive_effect_on_primary_cluster

    @features("Feature8101")
    @features("Feature8071")
    @level("Business")
    def test_configure_active_effect_on_edge_cluster(self):
        """
        Validate users can configure the all the device supported effects on the edge cluster as the active effects
        """
        self._test_configure_effects_on_the_clusters(cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                                     is_active=True)

        self.testCaseChecked("BUS_8101_0009", _AUTHOR)
    # end def test_configure_active_effect_on_edge_cluster

    @features("Feature8101")
    @features("Feature8071")
    @level("Business")
    def test_configure_passive_effect_on_edge_cluster(self):
        """
        Validate users can configure the all the device supported effects on the edge cluster as the passive effects
        """
        self._test_configure_effects_on_the_clusters(cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE,
                                                     is_active=False)

        self.testCaseChecked("BUS_8101_0010", _AUTHOR)
    # end def test_configure_passive_effect_on_edge_cluster

    @features("Feature8101")
    @features("Feature8071")
    @level("Business")
    def test_configure_active_effect_on_multi_cluster(self):
        """
        Validate users can configure the all the device supported effects on the multi-cluster as the active effects
        """
        self._test_configure_effects_on_the_clusters(cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
                                                     is_active=True)

        self.testCaseChecked("BUS_8101_0011", _AUTHOR)
    # end def test_configure_active_effect_on_multi_cluster

    @features("Feature8101")
    @features("Feature8071")
    @level("Business")
    def test_configure_passive_effect_on_multi_cluster(self):
        """
        Validate users can configure the all the device supported effects on the multi-cluster as the passive effects
        """
        self._test_configure_effects_on_the_clusters(cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
                                                     is_active=False)

        self.testCaseChecked("BUS_8101_0012", _AUTHOR)
    # end def test_configure_passive_effect_on_multi_cluster

    @features("Feature8101")
    @level("Business")
    @services("RGBMonitoring")
    def test_configure_power_save_timeout(self):
        """
        Validate users can configure the power save timeout (Time to switch from active to passive lighting)
        """
        oob_profile = ProfileManagementTestUtils.ProfileHelper.get_oob_profile_from_settings(self)
        new_ps_timeout = HexList().fromLong(to_int(self.config.OOB_PROFILES.F_PSTimeout[0]) - 5,
                                            PROFILE_TAG_INFO_MAP[ProfileManagement.Tag.PO_TIMEOUT].byte_count)
        address_of_ps_timeout = ProfileManagementTestUtils.ProfileHelper.get_field_address_in_profile(
                oob_profile, ProfileManagement.Tag.PS_TIMEOUT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load request with first_sector_id=0x0101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self, first_sector_id=ProfileManagement.Partition.SectorId.OOB | 0x0001,
            count=to_int(self.config.OOB_PROFILE_DIRECTORY.F_Length[0]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send editBuffer request to change the power_save_timeout to non_default_value")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=PROFILE_TAG_INFO_MAP[ProfileManagement.Tag.PS_TIMEOUT].byte_count,
            opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE,
            address=address_of_ps_timeout,
            data=new_ps_timeout + HexList(oob_profile)[
                                    address_of_ps_timeout:
                                    address_of_ps_timeout + (EditBuffer.LEN.DATA // 8) -
                                    PROFILE_TAG_INFO_MAP[ProfileManagement.Tag.PS_TIMEOUT].byte_count])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(
            test_case=self,
            offset_bytes=ProfileManagementTestUtils.ProfileHelper.get_field_address_in_profile(
                oob_profile, ProfileManagement.Tag.PS_TIMEOUT))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified power_save_timeout is as expected")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, new_ps_timeout + HexList(oob_profile)[
                                            address_of_ps_timeout +
                                            PROFILE_TAG_INFO_MAP[ProfileManagement.Tag.PS_TIMEOUT].byte_count:
                                            address_of_ps_timeout + (ReadBufferResponse.LEN.DATA // 8)])
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.RAM,
                                            count=to_int(self.config.OOB_PROFILE_DIRECTORY.F_Length[0]),
                                            crc_32=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(
                                                ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(
                                                    test_case=self,
                                                    count=to_int(self.config.OOB_PROFILE_DIRECTORY.F_Length[0]))))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait for {new_ps_timeout}")
        # --------------------------------------------------------------------------------------------------------------
        sleep(to_int(new_ps_timeout))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validate the RGB color effect turns to passive from active by LED analyzer/spy")
        # --------------------------------------------------------------------------------------------------------------
        self._check_rgb_effect(test_case=self)

        self.testCaseChecked("BUS_8101_0013", _AUTHOR)
    # end def test_configure_power_save_timeout

    @features("Feature8101")
    @level("Business")
    @services("RGBMonitoring")
    def test_configure_power_off_timeout(self):
        """
        Validate users can configure the power off timeout (Time to switch from passive to deep-sleep)
        """
        oob_profile = ProfileManagementTestUtils.ProfileHelper.get_oob_profile_from_settings(self)
        new_po_timeout = HexList().fromLong(to_int(self.config.OOB_PROFILES.F_PSTimeout[0]) + 5,
                                            PROFILE_TAG_INFO_MAP[ProfileManagement.Tag.PO_TIMEOUT].byte_count)
        address_of_po_timeout = ProfileManagementTestUtils.ProfileHelper.get_field_address_in_profile(
            oob_profile, ProfileManagement.Tag.PO_TIMEOUT)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send load request with first_sector_id=0x0101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.load(
            test_case=self, first_sector_id=ProfileManagement.Partition.SectorId.OOB | 0x0001,
            count=to_int(self.config.OOB_PROFILE_DIRECTORY.F_Length[0]))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send editBuffer request to change the power_off_timeout to {non_default_value}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.edit_buffer(
            test_case=self, count=PROFILE_TAG_INFO_MAP[ProfileManagement.Tag.PO_TIMEOUT].byte_count,
            opcode=ProfileManagement.EditBufferOperation.Opcode.OVERWRITE,
            address=address_of_po_timeout,
            data=new_po_timeout + HexList(oob_profile)[
                                  address_of_po_timeout:
                                  address_of_po_timeout + (EditBuffer.LEN.DATA // 8) -
                                  PROFILE_TAG_INFO_MAP[ProfileManagement.Tag.PO_TIMEOUT].byte_count])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send readBuffer request")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.read_buffer(
            test_case=self,
            offset_bytes=ProfileManagementTestUtils.ProfileHelper.get_field_address_in_profile(
                oob_profile, ProfileManagement.Tag.PO_TIMEOUT))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the modified power_off_timeout is as expected")
        # --------------------------------------------------------------------------------------------------------------
        checker = ProfileManagementTestUtils.ReadBufferResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, new_po_timeout + HexList(oob_profile)[
                                                          address_of_po_timeout +
                                                          PROFILE_TAG_INFO_MAP[
                                                              ProfileManagement.Tag.PO_TIMEOUT].byte_count:
                                                          address_of_po_timeout + (ReadBufferResponse.LEN.DATA // 8)])
        })
        checker.check_fields(self, response, self.feature_8101.read_buffer_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.RAM,
                                            count=to_int(self.config.OOB_PROFILE_DIRECTORY.F_Length[0]),
                                            crc_32=ProfileManagementTestUtils.ProfileHelper.calculate_crc32(
                                                ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(
                                                    test_case=self,
                                                    count=to_int(self.config.OOB_PROFILE_DIRECTORY.F_Length[0]))))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Wait for {new_po_timeout}")
        # --------------------------------------------------------------------------------------------------------------
        sleep(to_int(new_po_timeout))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Validate the RGB color effect is off by LED analyzer/spy")
        # --------------------------------------------------------------------------------------------------------------
        self._check_rgb_effect(test_case=self)

        self.testCaseChecked("BUS_8101_0014", _AUTHOR)
    # end def test_configure_power_off_timeout

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_remap_keys_on_fkc_base_layer(self):
        """
        Validate users can remap button_1/KEYBOARD_A to "Mouse Middle" and button_2/KEYBOARD_B to
        "Left Ctrl + Left Shift + A", then configure the 0x1B05 feature settings file. (FKC Base Layer)
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2] \
            if self.f.PRODUCT.F_IsMice else [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create an onboard profile and directory then save the profile in the NVS partition only")
        # --------------------------------------------------------------------------------------------------------------
        directory, _ = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=False, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a FKC base layer table file to remap {trigger_keys[0]} to 'Mouse Left' and "
                                 f"{trigger_keys[1]} to 'Left Ctrl + Left Shift + A'")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MOUSE, trigger_key=trigger_keys[0],
                        action_key=KEY_ID.BUTTON_3),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[1],
                        action_key=KEY_ID.KEYBOARD_A,
                        action_modifier_keys=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_SHIFT]),
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
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
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(test_case=self, set_fkc_enabled=1,
                                                                  fkc_enabled=1, set_toggle_keys_enabled=0)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform a keystroke on the {trigger_keys[0]}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=trigger_keys[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the expected HID mouse report is received")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=remapped_key_settings[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a keystroke on the button_2")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=trigger_keys[1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the expected HID keyboard reports are received")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
            test_case=self, remapped_key=remapped_key_settings[1])

        self.testCaseChecked("BUS_8101_0015", _AUTHOR)
    # end def test_remap_keys_on_fkc_base_layer

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    @services('SimultaneousKeystrokes')
    def test_remap_keys_on_fn_layer(self):
        """
        Validate users can remap 'FN + trigger_key' to 'Play/Pause', then configure the 0x1B05 feature settings file.
        (FN layer table)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Create an onboard profile and directory then save the profile in the NVS partition only")
        # --------------------------------------------------------------------------------------------------------------
        directory, _ = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=False, save_profile_in_nvs=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Create a FN layer table file to remap a 'FN + {self.trigger_key!s}' to 'Play/Pause'")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.CONSUMER, trigger_key=self.trigger_key,
                        action_key=KEY_ID.PLAY_PAUSE, layer=FkcMainTable.Layer.FN)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send configure request with file_id={main_tables[FkcMainTable.Layer.FN].file_id_lsb}, "
                  "feature_id=0x1b05")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X1B05.FN_LAYER_SETTINGS_FILE,
                                            file_id=main_tables[FkcMainTable.Layer.FN].file_id_lsb,
                                            count=main_tables[FkcMainTable.Layer.FN].n_bytes,
                                            crc_32=main_tables[FkcMainTable.Layer.FN].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC and disable toggle keys by sending 0x1b05.get_set_enabled request")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            test_case=self,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.ENABLE,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
            toggle_keys_enabled=FullKeyCustomization.ToggleKeyStatus.DISABLE)
        # Wait all key release events
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform a key combination stroke on 'FN + {self.trigger_key!s}'")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
        sleep(0.05)
        self.button_stimuli_emulator.keystroke(key_id=self.trigger_key, delay=1)
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the expected HID consumer report is received")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_key_settings[0])

        self.testCaseChecked("BUS_8101_0016", _AUTHOR)
    # end def test_remap_keys_on_fn_layer

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    @services('SimultaneousKeystrokes')
    def test_remap_keys_on_g_shift_layer(self):
        """
        Validate users can remap "G-Shift + trigger_key" to "Cycle thru Onboard Profiles".
        (G-Shift layer table)
        """
        virtual_g_shift = KEY_ID.BUTTON_2 if self.f.PRODUCT.F_IsMice else KEY_ID.KEYBOARD_1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create {self.config.F_NumOnboardProfiles} onboard profiles")
        # --------------------------------------------------------------------------------------------------------------
        profiles = self.create_onboard_profiles_and_save_in_nvs(test_case=self, directory=directory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Create a G-Shift layer table file to remap {virtual_g_shift!s} to 'G-Shift' and"
                           f" {self.trigger_key!s} to {KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE!s}")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.FUNCTION, trigger_key=self.trigger_key,
                        action_key=KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE, layer=FkcMainTable.Layer.GSHIFT),
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER, trigger_key=virtual_g_shift,
                        action_key=KEY_ID.G_SHIFT)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings)
        profiles[0].update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_GSHIFT:
                              main_tables[FkcMainTable.Layer.GSHIFT].file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                              main_tables[FkcMainTable.Layer.BASE].file_id_lsb})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 profile to NVS\n{profiles[0]}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profiles[0]),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=profiles[0].first_sector_id_lsb,
                                         crc_32=profiles[0].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x8101 directory to NVS\n{directory}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory),
                                         store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profiles[0].file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profiles[0].file_id_lsb,
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
        LogHelper.log_step(
            self, f"Perform a key combination stroke on '{virtual_g_shift!s} + {self.trigger_key!s}'")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=virtual_g_shift)
        sleep(0.05)
        self.button_stimuli_emulator.keystroke(key_id=self.trigger_key, delay=1)
        self.button_stimuli_emulator.key_release(key_id=virtual_g_shift)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait profileChangeEvent and check the nwe_profile is as expected")
        # --------------------------------------------------------------------------------------------------------------
        response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self)
        checker = ProfileManagementTestUtils.ProfileChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({'new_profile': (checker.check_new_profile, profiles[1].file_id_lsb)})
        checker.check_fields(self, response, self.feature_8101.profile_change_event_cls, check_map)

        self.testCaseChecked("BUS_8101_0017", _AUTHOR)
    # end def test_remap_keys_on_g_shift_layer

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    @services('SimultaneousKeystrokes')
    def test_configure_multiple_fkc_layers_in_ram(self):
        """
        Validate the user can configure multiple FKC layers repeatedly in the RAM, and FW shall keep all configurations.
        """
        self._test_configure_multiple_fkc_layers(configure_in_nvs=False)

        self.testCaseChecked("BUS_8101_0018", _AUTHOR)
    # end def test_configure_multiple_fkc_layers_in_ram

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    @services('SimultaneousKeystrokes')
    def test_configure_multiple_fkc_layers_in_nvs(self):
        """
        Validate the user can configure multiple FKC layers repeatedly in the NVS, and FW shall keep all
        configurations.
        """
        self._test_configure_multiple_fkc_layers(configure_in_nvs=True)

        self.testCaseChecked("BUS_8101_0019", _AUTHOR)
    # end def test_configure_multiple_fkc_layers_in_nvs

    def _test_configure_multiple_fkc_layers(self, configure_in_nvs):
        """
        Validate the user can configure multiple FKC layers repeatedly in the RAM or NVS, and FW shall keep all
        configurations.

        :param configure_in_nvs: Flag indicating the FKC layers to be configured are saved in NVS or RAM (True / False)
        :type configure_in_nvs: ``bool``
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2, KEY_ID.BUTTON_5] if self.f.PRODUCT.F_IsMice else \
            [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_E]
        virtual_fn_key = KEY_ID.BUTTON_3 if self.f.PRODUCT.F_IsMice else KEY_ID.KEYBOARD_C
        virtual_g_shift = KEY_ID.BUTTON_4 if self.f.PRODUCT.F_IsMice else KEY_ID.KEYBOARD_D
        fn_remapped_key = RemappedKey(action_type=RemappedKey.ActionType.CONSUMER,
                                      trigger_key=trigger_keys[0],
                                      action_key=KEY_ID.PLAY_PAUSE, layer=FkcMainTable.Layer.FN)
        if configure_in_nvs:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, "Create onboard profiles and directory then save the profile in the NVS partition only")
            # ----------------------------------------------------------------------------------------------------------
            directory, _ = \
                ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                    test_case=self, save_directory_in_nvs=False, save_profile_in_nvs=True)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create an empty 0x8101 directory")
            # ----------------------------------------------------------------------------------------------------------
            directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Create a base layer to remap {virtual_g_shift!s} to 'G-Shift' and"
                           f" {self.trigger_key!s} to {KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE!s}")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MOUSE, trigger_key=trigger_keys[0],
                        action_key=KEY_ID.BUTTON_3),
            RemappedKey(action_type=RemappedKey.ActionType.KEYBOARD, trigger_key=trigger_keys[1],
                        action_key=KEY_ID.KEYBOARD_A,
                        action_modifier_keys=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_SHIFT]),
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER, trigger_key=virtual_fn_key,
                        action_key=KEY_ID.FN_KEY),
            RemappedKey(action_type=RemappedKey.ActionType.VIRTUAL_MODIFIER, trigger_key=virtual_g_shift,
                        action_key=KEY_ID.G_SHIFT),
        ]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a main table and save in {'NVS' if configure_in_nvs else 'RAM'}")
        # --------------------------------------------------------------------------------------------------------------
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings,
                                                              save_in_nvs=configure_in_nvs)

        if configure_in_nvs:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Update the profile directory of NVS")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)
        # end if

        file_id_to_be_configured = main_tables[FkcMainTable.Layer.BASE].file_id_lsb if configure_in_nvs \
            else ProfileManagement.Partition.FileId.RAM
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={file_id_to_be_configured}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE,
                                            file_id=file_id_to_be_configured,
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
        remapped_keys = FullKeyCustomizationTestUtils.FkcTableHelper.convert_to_remapped_keys(
            test_case=self, fkc_main_tables=main_tables, os_variant=OS.WINDOWS)
        # Wait 50ms to ensure all key release reports have been sent from the device
        sleep(self.WAIT_ALL_KEY_RELEASE_EVENT_S)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        def _perform_remapping_keystrokes_and_check_results(perform_keystrokes_on_fn_layer=False,
                                                            perform_keystrokes_on_g_shift_layer=False):
            """
            Perform keystrokes with remapping keys and check the results on the specified layers.

            :param perform_keystrokes_on_fn_layer: Flag indicating the keystroke is performing on FN layer
            :type perform_keystrokes_on_fn_layer: ``bool``
            :param perform_keystrokes_on_g_shift_layer: Flag indicating the keystroke is performing on G-Shift layer
            :type perform_keystrokes_on_g_shift_layer: ``bool``
            """
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {trigger_keys[0]!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=trigger_keys[0])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the expected HID mouse report is received")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
                test_case=self, remapped_key=remapped_keys[0])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {trigger_keys[1]!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=trigger_keys[1])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the expected HID keyboard reports are received")
            # ----------------------------------------------------------------------------------------------------------
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(
                test_case=self, remapped_key=remapped_keys[1])

            if perform_keystrokes_on_fn_layer:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Perform a key combination stroke on 'FN + {trigger_keys[0]!r}'")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=virtual_fn_key)
                sleep(0.05)
                self.button_stimuli_emulator.keystroke(key_id=trigger_keys[0], delay=1)
                self.button_stimuli_emulator.key_release(key_id=virtual_fn_key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the expected HID consumer report is received")
                # ------------------------------------------------------------------------------------------------------
                FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                                  remapped_key=fn_remapped_key)
            # end if

            if perform_keystrokes_on_g_shift_layer:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self,
                    f"Perform a key combination stroke on 'G-Shift({virtual_g_shift!r}) + {trigger_keys[0]!r}'")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key_id=virtual_g_shift)
                sleep(0.05)
                self.button_stimuli_emulator.keystroke(key_id=trigger_keys[0], delay=1)
                self.button_stimuli_emulator.key_release(key_id=virtual_g_shift)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the profileChangeEvent is received from the device")
                # ------------------------------------------------------------------------------------------------------
                response = ProfileManagementTestUtils.HIDppHelper.profile_change_event(test_case=self,
                                                                                       check_first_message=False,
                                                                                       allow_no_message=True)
                self.assertNotNone(obtained=response,
                                   msg="The profileChangeEvent is not received from the device, the G-Shift layer "
                                       "remapping may not work as expected.")
            # end if
        # end def _perform_remapping_keystrokes_and_check_results

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform keystrokes on the remapping keys")
        # --------------------------------------------------------------------------------------------------------------
        _perform_remapping_keystrokes_and_check_results()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Create a FN layer table file to remap 'FN + {trigger_keys[0]!s}' to 'Play/Pause'")
        # --------------------------------------------------------------------------------------------------------------
        fn_remapped_key_settings = [fn_remapped_key]
        main_tables[FkcMainTable.Layer.FN] = self.create_main_tables_and_save_in_nvs(
            test_case=self, directory=directory, preset_remapped_keys=fn_remapped_key_settings,
            save_in_nvs=configure_in_nvs)[FkcMainTable.Layer.FN]

        if configure_in_nvs:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Update the profile directory of NVS")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)
        # end if

        file_id_to_be_configured = main_tables[FkcMainTable.Layer.FN].file_id_lsb if configure_in_nvs \
            else ProfileManagement.Partition.FileId.RAM
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={file_id_to_be_configured}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X1B05.FN_LAYER_SETTINGS_FILE,
                                            file_id=file_id_to_be_configured,
                                            count=main_tables[FkcMainTable.Layer.FN].n_bytes,
                                            crc_32=main_tables[FkcMainTable.Layer.FN].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform keystrokes on the remapping keys")
        # --------------------------------------------------------------------------------------------------------------
        _perform_remapping_keystrokes_and_check_results(perform_keystrokes_on_fn_layer=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Create a G-Shift layer table file to remap 'G-Shift + {trigger_keys[0]!s} to "
                           f"{KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE!s}")
        # --------------------------------------------------------------------------------------------------------------
        g_shift_remapped_key_settings = [RemappedKey(action_type=RemappedKey.ActionType.FUNCTION,
                                                     trigger_key=trigger_keys[0],
                                                     action_key=KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE,
                                                     layer=FkcMainTable.Layer.GSHIFT)]
        main_tables[FkcMainTable.Layer.GSHIFT] = self.create_main_tables_and_save_in_nvs(
            test_case=self, directory=directory, preset_remapped_keys=g_shift_remapped_key_settings,
            save_in_nvs=configure_in_nvs)[
            FkcMainTable.Layer.GSHIFT]

        if configure_in_nvs:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Update the profile directory of NVS")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                             first_sector_id_lsb=directory.first_sector_id_lsb,
                                             crc_32=directory.crc_32)
        # end if

        file_id_to_be_configured = main_tables[FkcMainTable.Layer.GSHIFT].file_id_lsb if configure_in_nvs \
            else ProfileManagement.Partition.FileId.RAM
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={file_id_to_be_configured}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X1B05.GSHIFT_LAYER_SETTINGS_FILE,
                                            file_id=file_id_to_be_configured,
                                            count=main_tables[FkcMainTable.Layer.GSHIFT].n_bytes,
                                            crc_32=main_tables[FkcMainTable.Layer.GSHIFT].crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform keystrokes on the remapping keys")
        # --------------------------------------------------------------------------------------------------------------
        _perform_remapping_keystrokes_and_check_results(perform_keystrokes_on_fn_layer=True,
                                                        perform_keystrokes_on_g_shift_layer=True)
    # end def _test_configure_multiple_fkc_layers

    @features("Feature8101")
    @features("Feature1B05")
    @features("Feature4523")
    @level("Business")
    def test_disable_physical_controls(self):
        """
        Validate users can create a macro to send all of mouse keys
        """
        valid_physical_controls = FullKeyCustomizationTestUtils.FkcTableHelper.KeyProvider.get_all_remappable_keys(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=False, save_profile_in_nvs=False)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the all physical controls disabled.")
        # --------------------------------------------------------------------------------------------------------------
        profile.tag_fields[ProfileManagement.Tag.X4523_CIDX_BITMAP].setValue(
            fid=TagField_16_Bytes.FID.DATA,
            value=HexList([0xFF] * (TagField_16_Bytes.LEN.DATA // 8)))
        profile.crc_32 = directory.update_file(file_id_lsb=profile.file_id_lsb,
                                               table_in_hexlist=HexList(profile))
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=False,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}, "
                                 "feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.RAM,
                                            count=len(HexList(profile)),
                                            crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x4523 parameters")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_4523, _, _ = DisableControlsByCIDXTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Game Mode")
        # --------------------------------------------------------------------------------------------------------------
        # Make sure the game mode is disabled before enabling.
        self.game_mode_emulator.set_mode(activate_game_mode=False)
        sleep(0.5)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        self.game_mode_emulator.set_mode(activate_game_mode=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the gameModeEvent and check the game mode is enabled")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.game_mode_event(test_case=self)
        game_mode_state_checker = DisableControlsByCIDXTestUtils.GameModeStateChecker
        game_mode_state_check_map = game_mode_state_checker.get_default_check_map(self)
        game_mode_state_check_map.update({'enabled': (
            game_mode_state_checker.check_enabled, DisableControlsByCIDX.GameMode.ENABLE)})
        checker = DisableControlsByCIDXTestUtils.GameModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({'game_mode_state': (
            checker.check_game_mode_state, game_mode_state_check_map)})
        checker.check_fields(self, response, self.feature_4523.game_mode_event_cls, check_map)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over controls in all_physical_controls:")
        # --------------------------------------------------------------------------------------------------------------
        for control in valid_physical_controls:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {control!s}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=control)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check there is no HID report received")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the all physical controls enabled")
        # --------------------------------------------------------------------------------------------------------------
        profile.tag_fields[ProfileManagement.Tag.X4523_CIDX_BITMAP].setValue(
            fid=TagField_16_Bytes.FID.DATA,
            value=HexList([0] * (TagField_16_Bytes.LEN.DATA // 8)))
        profile.crc_32 = directory.update_file(file_id_lsb=profile.file_id_lsb,
                                               table_in_hexlist=HexList(profile))
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=False,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}, "
                                 "feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.RAM,
                                            count=len(HexList(profile)),
                                            crc_32=profile.crc_32)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over controls in all_physical_controls:")
        # --------------------------------------------------------------------------------------------------------------
        for control in set(valid_physical_controls).difference(set(NOT_REMAPPABLE_KEY_LIST)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on the {control!s}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=control)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the corresponding HID report is received")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(control, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(control, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set some physical controls disabled randomly")
        # --------------------------------------------------------------------------------------------------------------
        profile.tag_fields[ProfileManagement.Tag.X4523_CIDX_BITMAP].setValue(
            fid=TagField_16_Bytes.FID.DATA,
            value=HexList([time_ns() % (2 ** 8) for _ in range(TagField_16_Bytes.LEN.DATA // 8)]))
        profile.crc_32 = directory.update_file(file_id_lsb=profile.file_id_lsb,
                                               table_in_hexlist=HexList(profile))
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=False,
                                         first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}, "
                                 "feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.HOST_MODE_PROFILE,
                                            file_id=ProfileManagement.Partition.FileId.RAM,
                                            count=len(HexList(profile)),
                                            crc_32=profile.crc_32)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over controls in all_physical_controls:")
        # --------------------------------------------------------------------------------------------------------------
        for index, control in enumerate(ControlListTestUtils.get_cid_list_from_device(test_case=self)):
            if control in CID_TO_KEY_ID_MAP.keys():
                if CID_TO_KEY_ID_MAP[control] in set(valid_physical_controls).difference(set(NOT_REMAPPABLE_KEY_LIST)):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f"Perform a keystroke on the {CID_TO_KEY_ID_MAP[control]!s}")
                    # --------------------------------------------------------------------------------------------------
                    self.button_stimuli_emulator.keystroke(key_id=CID_TO_KEY_ID_MAP[control])

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, "Check the corresponding HID report is received/not received")
                    # --------------------------------------------------------------------------------------------------
                    if (int(profile.tag_fields[ProfileManagement.Tag.X4523_CIDX_BITMAP].data[index // 8]) &
                            (2 ** (index % 8))):
                        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                    else:
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self, key=KeyMatrixTestUtils.Key(CID_TO_KEY_ID_MAP[control], MAKE))
                        KeyMatrixTestUtils.check_hid_report_by_key_id(
                            test_case=self, key=KeyMatrixTestUtils.Key(CID_TO_KEY_ID_MAP[control], BREAK))
                    # end if
                # end if
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8101_0020", _AUTHOR)
    # end def test_disable_physical_controls

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_mouse_key(self):
        """
        Validate users can create a macro to send all of mouse keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform keystrokes on all of mouse keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries_in_key_id = []
        for key_id in list(ProfileButton.KEY_ID_TO_MOUSE_BUTTON_MASK.keys()):
            macro_entries_in_key_id.append(MouseButtonCommand(key_id=key_id, action=KeyAction.PRESS))
            macro_entries_in_key_id.append(WaitForXmsCommand())
            macro_entries_in_key_id.append(MouseButtonCommand(key_id=key_id, action=KeyAction.RELEASE))
            macro_entries_in_key_id.append(WaitForXmsCommand())
        # end for
        macro_entries_in_key_id = [PresetMacroEntry(commands=macro_entries_in_key_id + [MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries_in_key_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap a key to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_check(self, "Validate the received HID mouse input and check the button flags.")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        self.testCaseChecked("BUS_8101_0021", _AUTHOR)
    # end def test_macro_mouse_key

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_standard_key(self):
        """
        Validate users can create a macro to send all of standard keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform keystrokes on all of standard keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries_in_key_id = [PresetMacroEntry(
            commands=[StandardKeyCommand(key_id=key_id) for key_id in list(STANDARD_KEYS.keys())] +
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
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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

        self.testCaseChecked("BUS_8101_0022", _AUTHOR)
    # end def test_macro_standard_key

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_consumer_key(self):
        """
        Validate users can create a macro to send all of consumer keys
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform keystrokes on all of consumer keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        consumer_keys = []
        for key_id, consumer_usage_in_os in HidData.CONSUMER_KEYS.items():
            if len({OS.ALL, OS.WINDOWS}.intersection(consumer_usage_in_os.keys())) > 0:
                consumer_keys.append(key_id)
            # end if
        # end for
        macro_entries_in_key_id = [PresetMacroEntry(
            commands=[ConsumerKeyCommand(key_id=key_id) for key_id in consumer_keys] +
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
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                              main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_check(self, "Validate the received HID consumer input and check the button codes")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        self.testCaseChecked("BUS_8101_0023", _AUTHOR)
    # end def test_macro_consumer_key

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_xy_movement(self):
        """
        Validate users can create a macro to send some XY movements
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform keystrokes on all of consumer keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries = []
        for _ in range(10):
            macro_entries.append(XYCommand(x=time_ns() % (2 ** 16), y=time_ns() % (2 ** 16)))
            macro_entries.append(WaitForXmsCommand())
        # end for
        macro_entries = [PresetMacroEntry(commands=macro_entries + [MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap a key to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_check(self, "Validate the received HID consumer input and check the button codes")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        self.testCaseChecked("BUS_8101_0024", _AUTHOR)
    # end def test_macro_xy_movement

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_vertical_roller_movement(self):
        """
        Validate users can create a macro to send some roller movements (vertical roller)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform 10 random vertical roller movement and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries = []
        for _ in range(10):
            macro_entries.append(RollerCommand(wheel=time_ns() % (2 ** 8)))
            macro_entries.append(WaitForXmsCommand())
        # end for
        macro_entries = [PresetMacroEntry(commands=macro_entries + [MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap a key to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_check(self, "Validate the received HID mouse input and check the vertical roller movements")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        self.testCaseChecked("BUS_8101_0025", _AUTHOR)
    # end def test_macro_vertical_roller_movement

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_horizontal_roller_movement(self):
        """
        Validate users can create a macro to send some AcPan movements (horizontal roller)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform 10 random horizontal roller movement and save it in the"
                                 "NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries = []
        for _ in range(10):
            macro_entries.append(AcPanCommand(ac_pan=time_ns() % (2 ** 8)))
            macro_entries.append(WaitForXmsCommand())
        # end for
        macro_entries = [PresetMacroEntry(commands=macro_entries + [MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap a key to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_check(self, "Validate the received HID mouse input and check the horizontal roller movements")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        self.testCaseChecked("BUS_8101_0026", _AUTHOR)
    # end def test_macro_horizontal_roller_movement

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_wait_for_release(self):
        """
        Validate users can create a macro to send ['Z', 'Y', 'X'] with WaitForRelease(0x01)
        """
        macro_keys = [KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_X]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a macro to perform {macro_keys} keystrokes with WaitForRelease(0x01) in"
                                 "the end and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries = [PresetMacroEntry(commands=[WaitForReleaseCommand(),
                                                    StandardKeyCommand(key_id=macro_keys[0]),
                                                    StandardKeyCommand(key_id=macro_keys[1]),
                                                    StandardKeyCommand(key_id=macro_keys[2]),
                                                    MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap a key to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_step(self, "Press and hold on the remapping key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=self.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate is no HID keyboard report")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release the remapping key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=self.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the expected HID keyboard reports are received")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        self.testCaseChecked("BUS_8101_0027", _AUTHOR)
    # end def test_macro_wait_for_release

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_repeat_while_pressed(self):
        """
        Validate users can create a macro to send ['Z', 'Y', 'X'] with RepeatWhilePressed(0x02)
        """
        macro_keys = [KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_X]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a macro to perform {macro_keys} keystrokes with RepeatWhilePressed(0x02)"
                                 "in the end and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries = [PresetMacroEntry(commands=[StandardKeyCommand(key_id=macro_keys[0]),
                                                    StandardKeyCommand(key_id=macro_keys[1]),
                                                    StandardKeyCommand(key_id=macro_keys[2]),
                                                    RepeatWhilePressedCommand(),
                                                    MacroEndCommand()])]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap a key to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_step(self, "Press and hold on the remapping key for 0.5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=self.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for 0.5 seconds")
        # --------------------------------------------------------------------------------------------------------------
        sleep(0.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release the remapping key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=self.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate expected HID keyboard reports are repeatedly received.")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(5):
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                              remapped_key=remapped_keys[0])
        # end for
        # Empty all remaining HID reports
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

        self.testCaseChecked("BUS_8101_0028", _AUTHOR)
    # end def test_macro_repeat_while_pressed

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_repeat_until_cancel(self):
        """
        Validate users can create a macro to send ['Z', 'Y', 'X'] with RepeatUntilCancel(0x03)
        """
        trigger_keys = [KEY_ID.BUTTON_1, KEY_ID.BUTTON_2] \
            if self.f.PRODUCT.F_IsMice else [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B]
        macro_keys = [KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_X]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a macro to perform {macro_keys} keystrokes with RepeatUntilCancel(0x03)"
                                 "in the end and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries = [PresetMacroEntry(commands=[StandardKeyCommand(key_id=macro_keys[0]),
                                                    WaitForXmsCommand(ms=10),
                                                    StandardKeyCommand(key_id=macro_keys[1]),
                                                    WaitForXmsCommand(ms=10),
                                                    StandardKeyCommand(key_id=macro_keys[2]),
                                                    WaitForXmsCommand(ms=10),
                                                    RepeatUntilCancelCommand()])]

        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create a FKC main table to remap {trigger_keys[0]!s} to execute the macro and "
                                 f"{trigger_keys[1]!s} to 'MacroEnd'")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=trigger_keys[0], macro_entry_index=0),
            RemappedKey(action_type=RemappedKey.ActionType.STOP_MACRO, trigger_key=trigger_keys[1], macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_step(self, f"Perform a keystroke on the {trigger_keys[0]!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=trigger_keys[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait for 0.2 seconds")
        # --------------------------------------------------------------------------------------------------------------
        sleep(0.2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform a keystroke on the {trigger_keys[1]!s}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=trigger_keys[1])
        timestamp_of_macro_end = time_ns()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate expected HID keyboard reports are repeatedly received.")
        # --------------------------------------------------------------------------------------------------------------
        for _ in range(5):
            FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                              remapped_key=remapped_keys[0])
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate there is no HID keyboard sent after sending macro end")
        # --------------------------------------------------------------------------------------------------------------
        keyboard_reports = ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.HID, class_type=HidKeyboard)
        for report in keyboard_reports:
            self.assertLessEqual(report.timestamp, timestamp_of_macro_end,
                                 msg="Should not received any message sent after sending macro end.")
        # end for

        self.testCaseChecked("BUS_8101_0029", _AUTHOR)
    # end def test_macro_repeat_until_cancel

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_delay(self):
        """
        Validate users can create a macro to send ['A', 'B', 'C', 'D', 'E'] with delays[''300', '600', '1200',
        '3600'] between each keystroke. (The unit of delay: ms)
        """
        macro_keys = [KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_X, KEY_ID.KEYBOARD_W, KEY_ID.KEYBOARD_V]
        delays = [300, 600, 1200, 1800]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform ['Z', 'Y', 'X', 'W', 'V'] keystrokes with delays['300',"
                                 "'600', '1200', '1800'] between each keystroke and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries = []
        for index in range(len(delays)):
            macro_entries.append(StandardKeyCommand(key_id=macro_keys[index]))
            macro_entries.append(WaitForXmsCommand(ms=delays[index]))
        # end for
        macro_entries.append(StandardKeyCommand(key_id=macro_keys[-1]))
        macro_entries.append(MacroEndCommand())
        macro_entries = [PresetMacroEntry(commands=macro_entries)]
        macro = self.create_macro_and_save_in_nvs(test_case=self, directory=directory,
                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap a key to execute the macro")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_step(self, "Perform a keystroke on the remapping key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=self.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate expected HID keyboard reports are received")
        # --------------------------------------------------------------------------------------------------------------
        reports = []
        for key in macro_keys:
            hid_reports = []
            for key_action in [MAKE, BREAK]:
                responses_class, fields_name, fields_value = KeyMatrixTestUtils.KeyExpectedActions.get(
                    KeyMatrixTestUtils.Key(key, key_action), OS.WINDOWS)
                hid_report = self._check_key_actions(self, responses_class, fields_name, fields_value, True)[0]
                hid_reports.append(hid_report)
            # end for
            reports.append(hid_reports)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the time intervals of reports match the delay time")
        # --------------------------------------------------------------------------------------------------------------
        for index, delay in enumerate(delays):
            # Check the time intervals of reports match the delay time with 8 ms tolerance
            self.assertAlmostEqual(
                delay, (reports[index + 1][0].timestamp - reports[index][0].timestamp) // 10 ** 6, delta=8,
                msg=f'The time interval of reports does not match the delay: {delay}.\n'
                    f'first_report: {reports[index][0]}\nsecond_report: {reports[index + 1][0]}')
        # end for

        self.testCaseChecked("BUS_8101_0030", _AUTHOR)
    # end def test_macro_delay

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_jump_in_same_profile(self):
        """
        Validate users can create a macro to jump to another macro. (Two macros in the same profile)
        """
        macro_keys_1 = [KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_X]
        macro_keys_2 = [KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_2, KEY_ID.KEYBOARD_3]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create macro_1 to perform ['Z', 'Y', 'X'] keystrokes with Jump to the macro_2 in"
                                 "the end and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro = FullKeyCustomizationTestUtils.FkcTableHelper.create_macro(
            test_case=self, directory=directory, preset_macro_entries=[])
        keystroke_macro_preset = [StandardKeyCommand(key_id=macro_keys_1[0]),
                                  StandardKeyCommand(key_id=macro_keys_1[1]),
                                  StandardKeyCommand(key_id=macro_keys_1[2])]
        macro_1 = PresetMacroEntry(
            commands=keystroke_macro_preset + [
                JumpCommand(sector_id=macro.first_sector_id_lsb,
                            address=sum([len(command) for command in keystroke_macro_preset]) +
                            JumpCommand.COMMAND_LEN)])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create macro_2 in the same file of macro_1 to perform ['1', '2', '3'] keystrokes"
                                 "and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_2 = PresetMacroEntry(commands=[StandardKeyCommand(key_id=macro_keys_2[0]),
                                             StandardKeyCommand(key_id=macro_keys_2[1]),
                                             StandardKeyCommand(key_id=macro_keys_2[2]),
                                             MacroEndCommand()])
        macro_entries = [macro_1, macro_2]
        FullKeyCustomizationTestUtils.FkcTableHelper.update_macro(test_case=self,
                                                                  directory=directory,
                                                                  macro=macro,
                                                                  preset_macro_entries=macro_entries)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x1B05 macro table to NVS\n{macro_1}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(macro),
                                         store_in_nvs=True, first_sector_id_lsb=macro.first_sector_id_lsb,
                                         crc_32=macro.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap button_1 to execute the macro_1")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_step(self, "Perform a keystroke on the button_1")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=self.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over key in {macro_keys_1 + macro_keys_2}")
        # --------------------------------------------------------------------------------------------------------------
        for key in macro_keys_1 + macro_keys_2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate expected HID keyboard reports are received ('ABC123').")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8101_0031", _AUTHOR)
    # end def test_macro_jump_in_same_profile

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_macro_jump_in_different_profile(self):
        """
        Validate users can create a macro to jump to another macro. (Two macros in the different profile)
        """
        macro_keys_1 = [KEY_ID.KEYBOARD_Z, KEY_ID.KEYBOARD_Y, KEY_ID.KEYBOARD_X]
        macro_keys_2 = [KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_2, KEY_ID.KEYBOARD_3]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create macro_1 to perform {macro_keys_1} keystrokes with Jump to the macro_2 in"
                                 "the end and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_1 = FullKeyCustomizationTestUtils.FkcTableHelper.create_macro(
                    test_case=self, directory=directory, preset_macro_entries=[])
        macro_2 = FullKeyCustomizationTestUtils.FkcTableHelper.create_macro(
                    test_case=self, directory=directory, preset_macro_entries=[])
        macro_entry_1 = [PresetMacroEntry(commands=[StandardKeyCommand(key_id=macro_keys_1[0]),
                                                    StandardKeyCommand(key_id=macro_keys_1[1]),
                                                    StandardKeyCommand(key_id=macro_keys_1[2]),
                                                    JumpCommand(sector_id=macro_2.first_sector_id_lsb,
                                                                address=0)])]
        FullKeyCustomizationTestUtils.FkcTableHelper.update_macro(test_case=self,
                                                                  directory=directory,
                                                                  macro=macro_1,
                                                                  preset_macro_entries=macro_entry_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Create macro_2 in the different file of macro_1 to perform {macro_keys_2}"
                                 "keystrokes and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entry_2 = [PresetMacroEntry(commands=[StandardKeyCommand(key_id=macro_keys_2[0]),
                                                    StandardKeyCommand(key_id=macro_keys_2[1]),
                                                    StandardKeyCommand(key_id=macro_keys_2[2]),
                                                    MacroEndCommand()])]
        FullKeyCustomizationTestUtils.FkcTableHelper.update_macro(test_case=self,
                                                                  directory=directory,
                                                                  macro=macro_2,
                                                                  preset_macro_entries=macro_entry_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x1B05 macro table to NVS\n{macro_1}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(macro_1),
                                         store_in_nvs=True, first_sector_id_lsb=macro_1.first_sector_id_lsb,
                                         crc_32=macro_1.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write 0x1B05 macro table to NVS\n{macro_2}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(macro_2),
                                         store_in_nvs=True, first_sector_id_lsb=macro_2.first_sector_id_lsb,
                                         crc_32=macro_2.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a FKC main table to remap button_1 to execute the macro_1")
        # --------------------------------------------------------------------------------------------------------------
        remapped_key_settings = [
            RemappedKey(action_type=RemappedKey.ActionType.MACRO, trigger_key=self.trigger_key, macro_entry_index=0)
        ]
        main_tables = self.create_main_tables_and_save_in_nvs(test_case=self, directory=directory,
                                                              preset_remapped_keys=remapped_key_settings, macro=macro_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro_1.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

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
        LogHelper.log_step(self, "Perform a keystroke on the button_1")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=self.trigger_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: Loop over key in {macro_keys_1 + macro_keys_2}:")
        # --------------------------------------------------------------------------------------------------------------
        for key in macro_keys_1 + macro_keys_2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate expected HID keyboard reports are received "
                                      f"{macro_keys_1} + {macro_keys_2}.")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_8101_0032", _AUTHOR)
    # end def test_macro_jump_in_different_profile

    # noinspection PyTypeChecker
    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    @bugtracker('MacroNotSentDeepSleep')
    def test_macro_sent_after_dut_woken_up_from_deep_sleep(self):
        """
        Validate the device can be woken up from deep sleep after pressing a key which is remapping to execute a macro.
        And check the macro commands are performed as expected.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create a macro to perform keystrokes on all of standard keys and save it in the NVS")
        # --------------------------------------------------------------------------------------------------------------
        macro_entries_in_key_id = [PresetMacroEntry(
            commands=[StandardKeyCommand(key_id=key_id) for key_id in list(STANDARD_KEYS.keys())] +
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
                                                              preset_remapped_keys=remapped_key_settings, macro=macro)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Link the FKC settings tables to the onboard profile")
        # --------------------------------------------------------------------------------------------------------------
        profile.update_tag_content(
            directory=directory,
            tag_content_dict={ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: macro.file_id_lsb,
                              ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE:
                                  main_tables[FkcMainTable.Layer.BASE].file_id_lsb})
        ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                         store_in_nvs=True, first_sector_id_lsb=profile.first_sector_id_lsb,
                                         crc_32=profile.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update the profile directory of NVS")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(directory), store_in_nvs=True,
                                         first_sector_id_lsb=directory.first_sector_id_lsb,
                                         crc_32=directory.crc_32)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send configure request with file_id={profile.file_id_lsb}, feature_id=0x8101")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                            file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                            file_id=profile.file_id_lsb,
                                            count=directory.files[profile.file_id_lsb].n_bytes,
                                            crc_32=directory.files[profile.file_id_lsb].crc_32)

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
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Perform a keystroke on the remapping key: {self.trigger_key}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=self.trigger_key)
        number_of_all_key_released_hid_reports = 3
        for _ in range(number_of_all_key_released_hid_reports):
            # Empty all key release reports from HID queue
            ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                  class_type=(HidKeyboardBitmap, HidConsumer, HidKeyboard, HidMouse))
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the received HID keyboard input and check the button flags.")
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.FkcKeyMatrixHelper.check_hid_report(test_case=self,
                                                                          remapped_key=remapped_keys[0])

        self.testCaseChecked("BUS_8101_0033", _AUTHOR)
    # end def test_macro_sent_after_dut_woken_up_from_deep_sleep

    @features("Feature8101")
    @features("Feature1B05")
    @level("Business")
    def test_oob_behaviors(self):
        """
        Validate the default OOB behavior are as expected
        - No default FKC behavior, FKC disabled/enabled (before FKC 1.2 / since FKC 1.3)
        - FN layer assignment correspond to key cap FN layer labels ->
            tested in the pytestbox.device.hid.keyboard.keycode.business.KeyCodeBusinessTestCase.test_fn_key
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSetEnabled request")
        # --------------------------------------------------------------------------------------------------------------
        response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            test_case=self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetSetEnabledResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        fkc_checker = FullKeyCustomizationTestUtils.FkcStateChecker
        fkc_check_map = fkc_checker.get_default_check_map(self)
        fkc_check_map.update({"fkc_enabled": (fkc_checker.check_fkc_enabled,
                                              self.f.PRODUCT.FEATURES.COMMON.FULL_KEY_CUSTOMIZATION.F_FkcEnabled)})
        checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"fkc_state": (checker.check_fkc_state, fkc_check_map)})
        checker.check_fields(self, response, type(response), check_map)

        self.testCaseChecked("BUS_8101_0033", _AUTHOR)
    # end def test_oob_behaviors

    def _test_configure_effects_on_the_clusters(self, cluster_index, is_active):
        """
        Configure effect on the specified cluster and check the effect over LED spy

        :param cluster_index: Index of the cluster
        :type cluster_index: ``int``
        :param is_active: Flag indicating the effect is active or passive effect
        :type is_active: ``bool``
        """
        cluster_effects = RGBEffectsTestUtils.get_supported_effect_ids_by_cluster(
            test_case=self, cluster_index=cluster_index)
        _, feature_8071, _, _ = RGBEffectsTestUtils.HIDppHelper.get_parameters(self)
        effect_dict = feature_8071.get_effect_dictionary()
        cluster_tags = [
            ProfileManagement.Tag.ACTIVE_CLUSTER_0_EFFECT, ProfileManagement.Tag.ACTIVE_CLUSTER_1_EFFECT] if is_active \
            else [ProfileManagement.Tag.PASSIVE_CLUSTER_0_EFFECT, ProfileManagement.Tag.PASSIVE_CLUSTER_1_EFFECT]
        cluster_tag = cluster_tags[0] if cluster_index in [
            RGBEffectsTestUtils.RGBClusterId.PRIMARY, RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER] \
            else cluster_tags[1]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an onboard profile and directory then save in the NVS partition")
        # --------------------------------------------------------------------------------------------------------------
        directory, profiles = \
            ProfileManagementTestCase.create_onboard_profiles_from_settings_and_update_profile_directory(
                test_case=self, save_directory_in_nvs=True, save_profile_in_nvs=True)
        profile = profiles[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: Loop over effect in device_supported_effects")
        # --------------------------------------------------------------------------------------------------------------
        for effect in cluster_effects:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Change the active RGB color effect of the cluster{cluster_index} to {effect}.")
            # ----------------------------------------------------------------------------------------------------------
            profile.tag_fields[cluster_tag].setValue(
                fid=TagField_11_Bytes.FID.DATA,
                value=effect_dict[effect](random_value=True).params)
            profile.crc_32 = directory.update_file(file_id_lsb=profile.file_id_lsb,
                                                   table_in_hexlist=HexList(profile))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write 0x8101 profile to RAM\n{profile}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(profile),
                                             store_in_nvs=False,
                                             first_sector_id_lsb=profile.first_sector_id_lsb,
                                             crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send readBuffer request")
            # ----------------------------------------------------------------------------------------------------------
            ram_buffer_data = ProfileManagementTestUtils.ProfileHelper.get_ram_buffer_data(
                test_case=self, count=directory.files[profile.file_id_lsb].n_bytes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the modified RGB effect settings are all as expected results.")
            # ----------------------------------------------------------------------------------------------------------
            for offset in range((len(ram_buffer_data) // (ReadBufferResponse.LEN.DATA // 8)) + 1):
                self.assertEqual(
                    expected=HexList(profile)[offset * (ReadBufferResponse.LEN.DATA // 8):
                                              (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                    obtained=ram_buffer_data[offset * (ReadBufferResponse.LEN.DATA // 8):
                                             (offset + 1) * (ReadBufferResponse.LEN.DATA // 8)],
                    msg=f"The data parameter differs found at offset {offset * (ReadBufferResponse.LEN.DATA // 8)}, "
                        f"(expected:{HexList(profile)}, obtained:{ram_buffer_data})")
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send configure request with file_id={ProfileManagement.Partition.FileId.RAM}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(test_case=self, feature_id=ProfileManagement.FEATURE_ID,
                                                file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE,
                                                file_id=ProfileManagement.Partition.FileId.RAM,
                                                count=directory.files[profile.file_id_lsb].n_bytes,
                                                crc_32=profile.crc_32)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform an user action to keep the DUT in the run mode")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Validate the active RGB color effect of cluster{cluster_index} by LED analyzer/spy")
            # ----------------------------------------------------------------------------------------------------------
            # TODO: Check RGB Effect by LED analyzer/spy

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_configure_effects_on_the_clusters

    @classmethod
    def _check_key_actions(cls, test_case, responses_class, fields_name, fields_value, raise_exception):
        """
        Check the HID report associated to a keystroke.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param responses_class: list of HID report messages
        :type responses_class: ``list[BitFieldContainerMixin]``
        :param fields_name: list of names related to the fields that are expected to change
        :type fields_name: ``list[str | tuple[str, str]]``
        :param fields_value: list of values related to the fields that are expected to change
        :type fields_value: ``list[int | tuple[int, int]]``
        :param raise_exception: Flag enabling to raise an exception when a failure occurs
        :type raise_exception: ``bool``

        :return: The HID reports
        :rtype: ``list[BitFieldContainerMixin]``
        """
        hid_packets = []
        if len(responses_class) == 0:
            # Add timing here to prevent the next operations to trigger a timeout
            sleep(ButtonStimuliInterface.DEFAULT_DURATION)
        # end if
        for i in range(len(responses_class)):
            # Retrieve the previous HID report
            last_report = KeyMatrixTestUtils.get_last_report(test_case, responses_class[i])
            # Compute the next expected report
            for j in range(len(fields_name[i])):
                if responses_class[i] is HidConsumer:
                    KeyMatrixTestUtils._handle_consumer_report(last_report, value=fields_value[i][j])
                elif responses_class[i] is HidKeyboard and fields_name[i][j].lower().startswith('key_code'):
                    KeyMatrixTestUtils._handle_keyboard_report(last_report, value=fields_value[i][j])
                elif fields_value[i][j] >= 0:
                    last_report.setValue(last_report.getFidFromName(fields_name[i][j].lower()), fields_value[i][j])
                else:
                    last_report.setValue(last_report.getFidFromName(fields_name[i][j].lower()), 0)
                # end if
            # end for

            # Handle the case of a desynchronization with the DUT
            is_saved_report_matching = False
            saved_reports = KeyMatrixTestUtils.dut_mismached_reports(test_case)
            if len(saved_reports) > 0:
                for saved_report in saved_reports:
                    if HexList(last_report) == HexList(saved_report):
                        LogHelper.log_info(test_case, f'The expected report {HexList(last_report)} matches the '
                                                      f'missing {HexList(saved_report)}')
                        saved_reports.remove(saved_report)
                        is_saved_report_matching = True
                        break
                    # end if
                # end for
                if not is_saved_report_matching:
                    KeyMatrixTestUtils.get_missing_report_counter(test_case, increment=True)
                # end if
            else:
                # Retrieve the next HID report
                hid_packet = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                                   class_type=responses_class[i], check_first_message=False)

                test_case.logTrace(f'{responses_class[i].__name__}: {hid_packet!s}\n')
                if not last_report == hid_packet:
                    KeyMatrixTestUtils.get_missing_report_counter(test_case, increment=True)
                    LogHelper.log_info(test_case, f'The expected report {HexList(last_report)} differs from the one '
                                                  f'received {HexList(hid_packet)}')
                    KeyMatrixTestUtils.dut_mismached_reports(test_case, report=HexList(hid_packet))
                    if raise_exception:
                        test_case.fail(f'Error on report verification {hid_packet} != {last_report}')
                    # end if
                else:
                    hid_packets.append(hid_packet)
                # end if
            # end if
        # end for

        return hid_packets
    # end def _check_key_actions

    @classmethod
    def _check_rgb_effect(cls, test_case, red_value=0, green_value=0, blue_value=0,
                          period_msb=0x3E, period_lsb=0xE8, brightness=100, calibration_data=0):
        """
        Check RGB effect is as expected, Using Kosmos to spy the RGB effect (via I2C led driver or LED pwm) and compare
        to the expected value

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param red_value: Red value of RGB color model - OPTIONAL
        :type red_value: ``int``
        :param green_value: Green value of RGB color model - OPTIONAL
        :type green_value: ``int``
        :param blue_value: Blue value of RGB color model - OPTIONAL
        :type blue_value: ``int``
        :param period_msb: MSB of the effect period - OPTIONAL
        :type period_msb: ``int``
        :param period_lsb: LSB of the effect period - OPTIONAL
        :type period_lsb: ``int``
        :param brightness: Intensity of the effect : 0 = default(100), Valid values are 1-100,
         >100 = default - OPTIONAL
        :type brightness: ``int``
        :param calibration_data: RGB calibration data for zone 0, zone 1 and zone 2 - OPTIONAL
        :type calibration_data: ``list[list[int, int, int]]``
        """
        two_periods_duration = 2 * (period_lsb | period_msb << 8) / 1000
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Stop I2C monitoring after 2 periods of effects')
        # --------------------------------------------------------------------------------------------------------------
        sleep(two_periods_duration)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case, 'Check RGB data match pulsing/breathing (waveform) effect reference for the '
                                       'primary cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper. \
            check_pulsing_breathing_effect(test_case, red_value=red_value, green_value=green_value,
                                           blue_value=blue_value, period_msb=period_msb, period_lsb=period_lsb,
                                           brightness=brightness, calibration_data=calibration_data,
                                           cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)

        if test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_HasEdgeLedDriver:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Check no effect is played on Edge cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper. \
                check_disabled_effect(test_case, calibration_data=calibration_data,
                                      cluster_index=RGBEffectsTestUtils.RGBClusterId.EDGE)
        # end if
    # end def _check_rgb_effect
# end class ProfileManagementBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
