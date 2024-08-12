#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b08.analogkeys
:brief: Validate HID++ 2.0 ``AnalogKeys`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/03/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.analogkeys import AnalogKeys
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.mcu.analogkeysprofileformat import ActionGroup
from pylibrary.mcu.analogkeysprofileformat import ActuationConfigurationTable
from pylibrary.mcu.analogkeysprofileformat import MultiActionConfigurationTable
from pylibrary.mcu.analogkeysprofileformat import RapidTriggerConfigurationTable
from pylibrary.mcu.fkcprofileformat import FkcMainTable
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analogkeysutils import AnalogKeysTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysTestCase(DeviceBaseTestCase):
    """
    Validate ``AnalogKeys`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1B08 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1b08_index, self.feature_1b08, _, _ = AnalogKeysTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.ANALOG_KEYS
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            # Empty Event Queue
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        super().tearDown()
    # end def tearDown

    def create_actuation_table_in_ram(self, key_count):
        """
        Create and activate Actuation Configuration table in RAM buffer

        :param key_count: The number of keys to be randomly generated
        :type key_count: ``int``

        :return: Actuation table configured in RAM
        :rtype: ``ActuationConfigurationTable``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create Actuation Configuration table")
        # --------------------------------------------------------------------------------------------------------------
        actuation_table = AnalogKeysTestUtils.AnalogKeysHelper.create_actuation_point_table(
            test_case=self, directory=directory, number_of_key_to_be_random_generated=key_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write the Actuation table in RAM\n{actuation_table}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(actuation_table))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure 0x1B08 in RAM to take the changes")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=AnalogKeys.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B08.ACTUATION_CONFIGURATION_FILE,
            file_id=ProfileManagement.Partition.FileId.RAM,
            count=len(HexList(actuation_table)),
            crc_32=actuation_table.crc_32)

        return actuation_table
    # end def create_actuation_table_in_ram

    def create_rapid_trigger_table_in_ram(self, key_count):
        """
        Create and activate Rapid Trigger table in RAM buffer

        :param key_count: The number of keys to be generated
        :type key_count: ``int``

        :return: Rapid trigger configuration table
        :rtype: ``RapidTriggerConfigurationTable``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create Rapid Trigger table")
        # --------------------------------------------------------------------------------------------------------------
        rapid_trigger_table = AnalogKeysTestUtils.AnalogKeysHelper.create_rapid_trigger_table(
            test_case=self, directory=directory, number_of_key_to_be_random_generated=key_count)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write the Rapid Trigger table in RAM\n{rapid_trigger_table}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(rapid_trigger_table))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure 0x1B08 in RAM to take the changes")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=AnalogKeys.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B08.RAPID_TRIGGER_CONFIGURATION_FILE,
            file_id=ProfileManagement.Partition.FileId.RAM,
            count=len(HexList(rapid_trigger_table)),
            crc_32=rapid_trigger_table.crc_32)

        return rapid_trigger_table
    # end def create_rapid_trigger_table_in_ram

    def create_multi_action_table_in_ram(self, preset_action_groups=None, number_of_key_to_be_random_generated=None):
        """
        Create and activate Multi-Action table in RAM buffer

        :param preset_action_groups: The preset action groups - OPTIONAL
        :type preset_action_groups: ``list[ActionGroup] | None``
        :param number_of_key_to_be_random_generated: Number of keys to be randomly generated - OPTIONAL
        :type number_of_key_to_be_random_generated: ``int | None``

        :return: ``MultiActionConfigurationTable`` instance
        :rtype: ``MultiActionConfigurationTable``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create Multi-Action table")
        # --------------------------------------------------------------------------------------------------------------
        multi_action_table = AnalogKeysTestUtils.AnalogKeysHelper.create_multi_action_table(
            test_case=self, directory=directory, preset_groups=preset_action_groups,
            number_of_key_to_be_random_generated=number_of_key_to_be_random_generated)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write the Multi-Action table in RAM\n{multi_action_table}")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.write(test_case=self, data=HexList(multi_action_table))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure 0x1B08 in RAM to take the changes")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.activate(
            test_case=self, feature_id=AnalogKeys.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B08.MULTI_ACTION_CONFIGURATION_FILE,
            file_id=ProfileManagement.Partition.FileId.RAM,
            count=len(HexList(multi_action_table)),
            crc_32=multi_action_table.crc_32)

        return multi_action_table
    # end def create_multi_action_table_in_ram

    def create_fkc_remapping_in_ram(self, preset_remapped_keys=None, random_parameters=None, notify_sw=False,
                                    os_variant=OS.WINDOWS):
        """
        Create and activate FKC remapping in RAM buffer

        :param preset_remapped_keys: The preset remapped keys - OPTIONAL
        :type preset_remapped_keys: ``list[RemappedKey] | None``
        :param random_parameters: Random parameters - OPTIONAL
        :type random_parameters: ``FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters | None``
        :param notify_sw: Flag indicating to set NotifySW bit in the action_bitfield - OPTIONAL
        :type notify_sw: ``bool``
        :param os_variant: OS variant (Windows by default) - OPTIONAL
        :type os_variant: ``OS | str``

        :return: A list of ``RemappedKey`` instance
        :rtype: ``list[RemappedKey]``

        :raise ``AssertionError``: if there are multiple FKC main tables
        """
        random_parameters = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters() \
            if random_parameters is None else random_parameters

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create an empty 0x8101 directory")
        # --------------------------------------------------------------------------------------------------------------
        directory = ProfileManagementTestUtils.ProfileHelper.create_directory(test_case=self)

        preset_remapped_key_count = 0 if not preset_remapped_keys else len(preset_remapped_keys)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Create FKC main tables in RAM\n"
                                 f"Preset remapped keys: {preset_remapped_key_count}\n{random_parameters}")
        # --------------------------------------------------------------------------------------------------------------
        main_tables = FullKeyCustomizationTestUtils.FkcTableHelper.create_main_tables(
            test_case=self, directory=directory, random_parameters=random_parameters,
            preset_remapped_keys=preset_remapped_keys, notify_sw=notify_sw, os_variant=os_variant)

        configured_fkc_main_table = False
        for layer, main_table in enumerate(main_tables):
            if main_table.is_empty():
                continue
            # end if
            assert configured_fkc_main_table is False, 'Having multiple FKC main tables is forbidden'

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write the FKC main table\n{main_table}")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.write(test_case=self, data=HexList(main_table))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Configure 0x1B05 in RAM to take the changes")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.activate(
                test_case=self, feature_id=FullKeyCustomization.FEATURE_ID,
                file_type_id=FkcMainTable.Layer.to_file_type_id(layer),
                file_id=ProfileManagement.Partition.FileId.RAM,
                count=len(HexList(main_table)),
                crc_32=main_table.crc_32)
            configured_fkc_main_table = True
        # end for

        remapped_keys = FullKeyCustomizationTestUtils.FkcTableHelper.convert_to_remapped_keys(
            test_case=self, fkc_main_tables=main_tables, os_variant=os_variant)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_data(self, f"{remapped_keys})")
        # --------------------------------------------------------------------------------------------------------------

        return remapped_keys
    # end def create_fkc_remapping_in_ram

    def empty_hid_queue(self):
        """
        Empty HID queue after a 50ms delay
        """
        # Wait 50ms to ensure all HID events are processed
        sleep(0.05)
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
    # end def empty_hid_queue
# end class AnalogKeysTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
