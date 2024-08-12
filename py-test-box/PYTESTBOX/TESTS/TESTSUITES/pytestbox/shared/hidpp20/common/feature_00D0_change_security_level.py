#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hidpp20.common.feature_00D0_change_security_level
:brief: Shared HID++ 2.0 Common feature 0x00D0
:author: Stanislas Cottard
:date: 2019/09/05
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from os.path import exists
from os.path import join

from intelhex import IntelHex

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.bootloadertest import CommonBootloaderTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.dfuprocessing import CommonDfuTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedDfuTestCaseChangeSecurityLevel(CommonDfuTestCase, ABC):
    """
    Validate DFU TestCases that needs to change the DFU security level
    """

    def setUp(self):
        """
        Handle test setup, prerequisites will be done separately.
        """
        self.current_nvs_parser = None

        # We do only the setup of the great grand parent class and skip the one of the parent
        super(CommonBootloaderTestCase, self).setUp()
    # end def setUp

    def pre_requisite(self, secur_lvl_chunk_id_str, secur_lvl):
        """
        Handle test prerequisites.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        if hasattr(self.memory_manager, "backup_secure_nvs"):
            self.memory_manager.backup_secure_nvs()
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Program the MCU with the given security Level = 0x{secur_lvl:X}')
        # --------------------------------------------------------------------------------------------------------------
        if self.current_channel.protocol == LogitechProtocol.USB:
            ChannelUtils.close_channel(test_case=self)
        # end if
        if secur_lvl_chunk_id_str in self.memory_manager.chunk_id_map:
            self.memory_manager.nvs_parser.add_new_chunk(chunk_id=secur_lvl_chunk_id_str, data=[secur_lvl])
            self.memory_manager.load_nvs()
            self.reset()
        else:
            self.memory_manager.set_security_level_application(secur_lvl)
            self.reset(hardware_reset=True)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send DFU Control.startDfu to switch in bootloader')
        # --------------------------------------------------------------------------------------------------------------
        try:
            self.dut_jump_on_bootloader()
        except AssertionError as err:
            if err.args[0] == "Could not find feature ID 0x00C3 in device":
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, "Already in bootloader")
                # ------------------------------------------------------------------------------------------------------
                self.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(self, feature_id=Dfu.FEATURE_ID)
            # end if
        # end try
    # end def pre_requisite

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if hasattr(self.memory_manager, "restore_secure_nvs"):
                self.memory_manager.restore_secure_nvs()
            # end if
        # end with

        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Restore initial NVS")
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.NvsHelper.restore_nvs(
                    self,
                    backup=True,
                    no_reset=True,
                    ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled)
        # end with

        super().tearDown()
    # end def tearDown

    @features('Feature00D0V2+')
    @level('Functionality')
    @services('Debugger')
    def test_application_security_level_default(self):
        """
        Check the security level saved by the firmware in a dedicated NVS chunk at first boot.
        """
        self.post_requisite_reset_receiver = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        self.device_firmware_hex_file = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)
        firmware_intel_hex = IntelHex(self.device_firmware_hex_file)

        if self.memory_manager.nvs_encryption_key:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Get DUT initial AES Encryption key')
            # ----------------------------------------------------------------------------------------------------------
            aes_key_addresses = range(
                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY,
                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY + self.memory_manager.SIZE.NVS_ENCRYPTION_KEY)
            aes_key_intel_hex = IntelHex(dict(zip(aes_key_addresses, self.memory_manager.nvs_encryption_key)))
            firmware_intel_hex.merge(aes_key_intel_hex, overlap='replace')
        # end if

        if self.f.PRODUCT.FEATURES.COMMON.DFU.F_BootHexFileName:
            btldr_hex = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_BootHexFileName)
            btldr_hex = IntelHex(btldr_hex)
            firmware_intel_hex.merge(btldr_hex, 'replace')
        # end if
        if self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesHexFileName:
            img_hex = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_ImagesHexFileName)
            img_hex = IntelHex(img_hex)
            firmware_intel_hex.merge(img_hex, 'replace')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reload the default firmware (with the initial AES encryption key if applicable)")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.erase_and_flash_firmware(firmware_intel_hex)
        self.memory_manager.debugger.reset(soft_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump data in NVS and validate chunk structure')
        # --------------------------------------------------------------------------------------------------------------
        if (secur_lvl_chunk_id_str := "NVS_APP_SECUR_LVL_ID") in self.memory_manager.chunk_id_map:
            nvs_parser_to_check = self.get_dut_nvs_parser()
            security_level_chunks = nvs_parser_to_check.get_chunk_history(secur_lvl_chunk_id_str)

            self.assertEqual(expected=1, obtained=len(security_level_chunks),
                             msg="Wrong number of security level chunks in NVS.")
            self.assertEqual(expected=int(self.f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl),
                             obtained=to_int(security_level_chunks[-1].chunk_data[0]),
                             msg='The default security level differs from the expected one')
        else:
            self.memory_manager.read_secure_nvs()
            secur_lvl_chunk, secur_lvl_chunk_index = self.memory_manager.get_security_level_chunk()
            self.assertEqual(expected=0, obtained=secur_lvl_chunk_index,
                             msg="Wrong number of security level chunks in NVS.")
            self.assertEqual(expected=int(self.f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl),
                             obtained=int(secur_lvl_chunk[self.memory_manager.SECURE_LVL_APP_INDEX]),
                             msg='The default security level differs from the expected one')
        # end if

        self.testCaseChecked("FNT_00D0_0052")
    # end def test_application_security_level_default

    @features('Feature00D0V2+')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationSecurLvl0x01To0x01(self):
        """
        Check the DFU processing with a security level byte equal to the value of the last valid firmware.
        Create a DFU with the securLvl parameter set to 0x01 to update a firmware with securLvl = 0x01.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x01)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0x01)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0036")
    # end def test_ApplicationSecurLvl0x01To0x01

    @features('Feature00D0V2+')
    @level('Business')
    @services('Debugger')
    def test_ApplicationSecurLvl0x00To0x01(self):
        """
        Check the DFU processing business Case with security level byte incremented by 1 compared to the value of the
        last valid firmware.
        Create a DFU with the securLvl parameter set to 0x01 to update a firmware with securLvl = 0x00.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x00)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0x01)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0037")
    # end def test_ApplicationSecurLvl0x00To0x01

    @features('Feature00D0V2+')
    @level('Time-consuming')
    @services('Debugger')
    def test_ApplicationSecurLvl0x00To0x02(self):
        """
        Check the DFU processing with a security level byte greater than the value of the last valid firmware.
        Create a DFU with the securLvl parameter set to 0x02 to update a firmware with securLvl = 0x00.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x00)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0x02)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0038")
    # end def test_ApplicationSecurLvl0x00To0x02

    @features('Feature00D0V2+')
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_ApplicationSecurLvl0x0FTo0x10(self):
        """
        Check the DFU processing with a security level byte incremented by 1 compared to the value of the last valid
        firmware.
        Create a DFU with the securLvl parameter set to 0x10 to update a firmware with securLvl = 0x0F.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x0F)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0x10)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0039")
    # end def test_ApplicationSecurLvl0x0FTo0x10

    @features('Feature00D0V2+')
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_ApplicationSecurLvl0xFETo0xFF(self):
        """
        Check the DFU processing with a security level byte incremented by 1 compared to the value of the last valid
        firmware.
        Create a DFU with the securLvl parameter set to 0xFF to update a firmware with securLvl = 0xFE.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0xFE)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0xFF)

        DfuTestUtils.send_dfu_restart_function(
            test_case=self,
            bootloader_dfu_feature_id=self.bootloader_dfu_feature_id,
            ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0040")
    # end def test_ApplicationSecurLvl0xFETo0xFF

    @features('Feature00D0V2+')
    @level('ErrorHandling')
    @services('Debugger')
    def test_ApplicationSecurLvl0x01To0x00(self):
        """
        Test the security level parameter verification with securLvl byte equal to the value of the second to last
        valid firmware.
        Create a DFU with the securLvl parameter set to 0x00 to update a firmware with securLvl = 0x01.

        [event0] dfuStatus() -> pktNb, status, param


        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x01)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0x00, True)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("ROT_00D0_0045")
    # end def test_ApplicationSecurLvl0x01To0x00

    @features('Feature00D0V2+')
    @level('ErrorHandling')
    @services('Debugger')
    def test_ApplicationSecurLvl0x10To0x0F(self):
        """
        Test the security level parameter verification with securLvl byte equal to the value of the second to last
        valid firmware.
        Create a DFU with the securLvl parameter set to 0x0F to update a firmware with securLvl = 0x10.

        [event0] dfuStatus() -> pktNb, status, param


        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x10)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0x0F, True)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("ROT_00D0_0046")
    # end def test_ApplicationSecurLvl0x10To0x0F

    @features('Feature00D0V2+')
    @level('ErrorHandling')
    @services('Debugger')
    def test_ApplicationSecurLvl0x10To0x00(self):
        """
        Test the security level parameter verification with securLvl byte strictly lower than the value of the
        second to last valid firmware.
        Create a DFU with the securLvl parameter set to 0x00 to update a firmware with securLvl = 0x10.

        [event0] dfuStatus() -> pktNb, status, param


        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x10)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0x00, True)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("ROT_00D0_0047")
    # end def test_ApplicationSecurLvl0x10To0x00

    @features('Feature00D0V2+')
    @level('ErrorHandling')
    @services('Debugger')
    def test_ApplicationSecurLvl0x8FTo0x10(self):
        """
        Test the security level parameter verification with securLvl byte strictly lower than the value of the
        second to last valid firmware.
        Create a DFU with the securLvl parameter set to 0x10 to update a firmware with securLvl = 0x8F.

        [event0] dfuStatus() -> pktNb, status, param


        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x8F)
        # This function does all steps and checks
        self._load_app_dfu_with_requested_level(0x10, True)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("ROT_00D0_0048")
    # end def test_ApplicationSecurLvl0x8FTo0x10

    @features('Feature00D0V2+')
    @features('Feature00D0SoftDevice')
    @level('Time-consuming')
    @services('Debugger')
    def test_SoftDeviceSecurLvl0x01To0x01(self):
        """
        Check the SD DFU processing with a security level byte equal to the value of the last valid firmware.
        Create a SoftDevice DFU with the securLvl parameter set to 0x01 to update a firmware with securLvl = 0x01.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x01)

        # SoftDevice DFU sequence
        self._load_sd_dfu_with_requested_level(0x01)

        # Force a reset if needed
        self.reset(hardware_reset=True)

        # Application DFU sequence
        self._load_app_dfu_with_requested_level(0x01)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0046")
    # end def test_SoftDeviceSecurLvl0x01To0x01

    @features('Feature00D0V2+')
    @features('Feature00D0SoftDevice')
    @level('Business')
    @services('Debugger')
    def test_SoftDeviceSecurLvl0x00To0x01(self):
        """
        Check the SD DFU processing business Case with security level byte incremented by 1 compared to the value of
        the last valid firmware.
        Create a SoftDevice DFU with the securLvl parameter set to 0x01 to update a firmware with securLvl = 0x00.

        [0] dfuCmdData0(cmd, param) -> pktNb, status, param
        [1] dfuCmdData1(cmd, param) -> pktNb, status, param
        [2] dfuCmdData2(cmd, param) -> pktNb, status, param
        [3] dfuCmdData3(cmd, param) -> pktNb, status, param
        [event0] dfuStatus() -> pktNb, status, param

        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x00)

        # SoftDevice DFU sequence
        self._load_sd_dfu_with_requested_level(0x01)

        # Force a reset if needed
        self.reset(hardware_reset=True)

        # Application DFU sequence
        self._load_app_dfu_with_requested_level(0x01)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("FNT_00D0_0047")
    # end def test_SoftDeviceSecurLvl0x00To0x01

    @features('Feature00D0V2+')
    @features('Feature00D0SoftDevice')
    @level('ErrorHandling')
    @services('Debugger')
    def test_SoftDeviceSecurLvl0x01To0x00(self):
        """
        Test the security level parameter verification with securLvl byte equal to the value of the second to last
        valid firmware.
        Create a SoftDevice DFU with the securLvl parameter set to 0x00 to update a firmware with securLvl = 0x01.

        [event0] dfuStatus() -> pktNb, status, param


        v0: [4] dfuStart(fwEntity, encrypt, magicStrg) -> pktNb, status, param
        v1: [4] dfuStart(fwEntity, encrypt, magicStrg, flag) -> pktNb, status, param
        v2: [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) -> pktNb, status, param
        """
        # This function handles the pre-requisites
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=0x01)
        # SoftDevice DFU sequence
        self._load_sd_dfu_with_requested_level(0x00, True)

        # If the test is successful, there is still the need to program MCU to initial state

        self.testCaseChecked("ROT_00D0_0051")
    # end def test_SoftDeviceSecurLvl0x01To0x00

    @features('Feature00D0V2+')
    @level('ErrorHandling')
    @services('Debugger')
    def test_lower_application_security_level(self):
        """
        Check the dfu start request triggers an error when the security level in the command is lower than the
        one saved in the firmware.
        Expected error code = 167 (0xA7) Bad/incompatible security level
        """
        #
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        nvs_secur_lvl = int(self.f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl) + 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Program the NVS with securLvl = 0x{nvs_secur_lvl:X}')
        # --------------------------------------------------------------------------------------------------------------
        self.pre_requisite(secur_lvl_chunk_id_str="NVS_APP_SECUR_LVL_ID", secur_lvl=nvs_secur_lvl)

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES",
                               self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=ChannelUtils.get_device_index(self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuStart with fwEntity = application and a lower secure level')
        # --------------------------------------------------------------------------------------------------------------
        dfu_start_class = self.get_dfu_start_class()
        dfu_start = dfu_start_class(device_index=ChannelUtils.get_device_index(self),
                                    feature_index=self.bootloader_dfu_feature_id,
                                    fw_entity=dfu_file_parser.dfu_start_command.fw_entity,
                                    encrypt=dfu_file_parser.dfu_start_command.encrypt,
                                    magic_str=self.format_magic_string_hex_list(
                                        self.f.PRODUCT.FEATURES.COMMON.DFU.F_MagicString),
                                    flag=int(self.f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartFlags),
                                    secur_lvl=int(self.f.PRODUCT.FEATURES.COMMON.DFU.F_DfuStartSecurLvl))

        dfu_status_response = ChannelUtils.send(
            test_case=self,
            report=dfu_start,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x27 (Bad/incompatible security level)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.BAD_INCOMPATIBLE_SECURITY_LEVEL,
                                 packet_number=0)

        self.testCaseChecked("ROT_00D0_0059")
    # end def test_lower_application_security_level

    @features('Feature00D0V2+')
    @features('CompanionMCU')
    @level('ErrorHandling')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_next_security_level(self):
        """
        Check the companion application can be updated with a DFU with a higher security level.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Jump on bootloader")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restart_in_main_application = True
        self.dut_jump_on_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get DFU file parser with higher security level')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES",
                             self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileNameNextSecurityLevel)
        if (self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileNameNextSecurityLevel and
                exists(dfu_file_path)):
            dfu_file_parser = DfuFileParser.parse_dfu_file(
                dfu_file_path=dfu_file_path,
                device_index=int(Numeral(ChannelUtils.get_device_index(self))),
                dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
                dfu_feature_version=self.get_dfu_version())
        else:
            dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
            dfu_file_parser = DfuFileParser.parse_dfu_file(
                dfu_file_path=dfu_file_path,
                device_index=int(Numeral(ChannelUtils.get_device_index(self))),
                dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
                dfu_feature_version=self.get_dfu_version())

            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=HexList("FF" * self.companion_debugger.FMM_CRC_SIZE))

            dfu_file_parser.dfu_start_command.secur_lvl = to_int(dfu_file_parser.dfu_start_command.secur_lvl) + 1
            key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
            status = dfu_file_parser.compute_signature(
                key_file,
                max_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress,
                min_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                additional_auth=True)
            assert status, "Signature failed"

            crc = dfu_file_parser.compute_stm32_crc(
                start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                end_address=self.companion_debugger.FMM_CRC_STORE_ADDR)

            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=crc)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Update companion application')
        # --------------------------------------------------------------------------------------------------------------
        self._perform_dfu(dfu_file_parser=dfu_file_parser, error_expected=None)

        self.testCaseChecked("ERR_00D0_0068")
    # end def test_companion_next_security_level

    @features('Feature00D0V2+')
    @features('CompanionMCU')
    @level('ErrorHandling')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_previous_security_level(self):
        """
        Check the companion application can not be updated with a DFU with a lower security level.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Jump on bootloader")
        # --------------------------------------------------------------------------------------------------------------
        self.dut_jump_on_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get DFU file parser with higher security level')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES",
                             self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileNameNextSecurityLevel)
        if (self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileNameNextSecurityLevel and
                exists(dfu_file_path)):
            dfu_file_parser = DfuFileParser.parse_dfu_file(
                dfu_file_path=dfu_file_path,
                device_index=int(Numeral(ChannelUtils.get_device_index(self))),
                dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
                dfu_feature_version=self.get_dfu_version())
        else:
            dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
            dfu_file_parser = DfuFileParser.parse_dfu_file(
                dfu_file_path=dfu_file_path,
                device_index=int(Numeral(ChannelUtils.get_device_index(self))),
                dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
                dfu_feature_version=self.get_dfu_version())

            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=HexList("FF" * self.companion_debugger.FMM_CRC_SIZE))

            dfu_file_parser.dfu_start_command.secur_lvl = to_int(dfu_file_parser.dfu_start_command.secur_lvl) + 1
            key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
            status = dfu_file_parser.compute_signature(
                key_file,
                max_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress,
                min_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                additional_auth=True)
            assert status, "Signature failed"

            crc = dfu_file_parser.compute_stm32_crc(
                start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                end_address=self.companion_debugger.FMM_CRC_STORE_ADDR)

            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=crc)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Update companion application')
        # --------------------------------------------------------------------------------------------------------------
        self._perform_dfu(dfu_file_parser=dfu_file_parser, error_expected=None)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Parse DFU file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(ChannelUtils.get_device_index(self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())

        dfu_status_response = ChannelUtils.send(
            test_case=self,
            report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x27 (Bad/incompatible security level)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.BAD_INCOMPATIBLE_SECURITY_LEVEL,
                                 packet_number=0)

        self.testCaseChecked("ERR_00D0_0069")
    # end def test_companion_previous_security_level

    @features('Feature00D0V2+')
    @features('CompanionMCU')
    @level('Functionality')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_higher_security_levels(self):
        """
        Check the companion application can be updated with a DFU with a higher security level (check multiple higher
        security levels)
        """
        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Jump on bootloader")
        # --------------------------------------------------------------------------------------------------------------
        self.dut_jump_on_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Parse DFU file")
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(ChannelUtils.get_device_index(self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())
        initial_secur_lvl = dfu_file_parser.dfu_start_command.secur_lvl

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Loop over security levels higher than the original one')
        # --------------------------------------------------------------------------------------------------------------
        for secur_lvl in compute_sup_values(to_int(dfu_file_parser.dfu_start_command.secur_lvl)):
            dfu_file_parser.dfu_start_command.secur_lvl = secur_lvl
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set security level = {secur_lvl} in DFU file')
            # ----------------------------------------------------------------------------------------------------------
            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=HexList("FF" * self.companion_debugger.FMM_CRC_SIZE))
            status = dfu_file_parser.compute_signature(
                key_file,
                max_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress,
                min_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                additional_auth=True)
            assert status, "Signature failed"

            crc = dfu_file_parser.compute_stm32_crc(
                start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                end_address=self.companion_debugger.FMM_CRC_STORE_ADDR)
            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=crc)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Start DFU with security level = {secur_lvl}')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=self,
                report=dfu_file_parser.dfu_start_command,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=0)
        # end for

        if to_int(initial_secur_lvl) > 0:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set security level to 0 in DFU file to test more higher values')
            # ----------------------------------------------------------------------------------------------------------
            dfu_file_parser.dfu_start_command.secur_lvl = 0

            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=HexList("FF" * self.companion_debugger.FMM_CRC_SIZE))
            status = dfu_file_parser.compute_signature(
                key_file,
                max_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress,
                min_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                additional_auth=True)
            assert status, "Signature failed"

            crc = dfu_file_parser.compute_stm32_crc(
                start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                end_address=self.companion_debugger.FMM_CRC_STORE_ADDR)
            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=crc)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Update companion application')
            # ----------------------------------------------------------------------------------------------------------
            self._perform_dfu(dfu_file_parser=dfu_file_parser, error_expected=None)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Loop over security levels higher than the original one')
            # ----------------------------------------------------------------------------------------------------------
            for secur_lvl in compute_inf_values(to_int(dfu_file_parser.dfu_start_command.secur_lvl)):
                dfu_file_parser.dfu_start_command.secur_lvl = secur_lvl
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Set security level = {secur_lvl} in DFU file')
                # ------------------------------------------------------------------------------------------------------
                dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                        crc_data=HexList("FF" * self.companion_debugger.FMM_CRC_SIZE))
                status = dfu_file_parser.compute_signature(
                    key_file,
                    max_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress,
                    min_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                    additional_auth=True)
                assert status, "Signature failed"

                crc = dfu_file_parser.compute_stm32_crc(
                    start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                    end_address=self.companion_debugger.FMM_CRC_STORE_ADDR)
                dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                        crc_data=crc)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Start DFU with security level = {secur_lvl}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self,
                    report=dfu_file_parser.dfu_start_command,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=0)
            # end for
        # end if

        self.testCaseChecked("FUN_00D0_0070")
    # end def test_companion_higher_security_levels

    @features('Feature00D0V2+')
    @features('CompanionMCU')
    @level('ErrorHandling')
    @services('Debugger')
    @services('CompanionDebugger')
    def test_companion_lower_security_levels(self):
        """
        Check the companion application can not be updated with a DFU with a lower security level (check multiple
        lower security levels)
        """
        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        dfu_file_path = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionDfuFileName)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Jump on bootloader")
        # --------------------------------------------------------------------------------------------------------------
        self.dut_jump_on_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Parse DFU file")
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=dfu_file_path,
            device_index=int(Numeral(ChannelUtils.get_device_index(self))),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=self.get_dfu_version())
        initial_secur_lvl = dfu_file_parser.dfu_start_command.secur_lvl

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Enable post-requisite to restore companion application after DFU')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restore_companion = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Loop over security levels lower than the original one')
        # --------------------------------------------------------------------------------------------------------------
        for secur_lvl in compute_inf_values(to_int(dfu_file_parser.dfu_start_command.secur_lvl)):
            dfu_file_parser.dfu_start_command.secur_lvl = secur_lvl
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set security level = {secur_lvl} in DFU file')
            # ----------------------------------------------------------------------------------------------------------
            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=HexList("FF" * self.companion_debugger.FMM_CRC_SIZE))
            status = dfu_file_parser.compute_signature(
                key_file,
                max_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress,
                min_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                additional_auth=True)
            assert status, "Signature failed"

            crc = dfu_file_parser.compute_stm32_crc(
                start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                end_address=self.companion_debugger.FMM_CRC_STORE_ADDR)
            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=crc)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Start DFU with security level = {secur_lvl}')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=self,
                report=dfu_file_parser.dfu_start_command,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x27 (Bad/incompatible security level)')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.BAD_INCOMPATIBLE_SECURITY_LEVEL,
                                     packet_number=0)
        # end for

        if to_int(initial_secur_lvl) < 0xFF:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set security level to 0xFF in DFU file to test more lower values')
            # ----------------------------------------------------------------------------------------------------------
            dfu_file_parser.dfu_start_command.secur_lvl = 0xFF

            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=HexList("FF" * self.companion_debugger.FMM_CRC_SIZE))
            status = dfu_file_parser.compute_signature(
                key_file,
                max_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress,
                min_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                additional_auth=True)
            assert status, "Signature failed"

            crc = dfu_file_parser.compute_stm32_crc(
                start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                end_address=self.companion_debugger.FMM_CRC_STORE_ADDR)
            dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                    crc_data=crc)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Update companion application')
            # ----------------------------------------------------------------------------------------------------------
            self._perform_dfu(dfu_file_parser=dfu_file_parser, error_expected=None)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Loop over security levels lower than the original one')
            # ----------------------------------------------------------------------------------------------------------
            for secur_lvl in compute_inf_values(to_int(dfu_file_parser.dfu_start_command.secur_lvl)):
                dfu_file_parser.dfu_start_command.secur_lvl = secur_lvl
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Set security level = {secur_lvl} in DFU file')
                # ------------------------------------------------------------------------------------------------------
                dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                        crc_data=HexList("FF" * self.companion_debugger.FMM_CRC_SIZE))
                status = dfu_file_parser.compute_signature(
                    key_file,
                    max_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionHighestApplicationAddress,
                    min_app_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                    additional_auth=True)
                assert status, "Signature failed"

                crc = dfu_file_parser.compute_stm32_crc(
                    start_address=self.f.PRODUCT.FEATURES.COMMON.DFU.F_CompanionLowestApplicationAddress,
                    end_address=self.companion_debugger.FMM_CRC_STORE_ADDR)
                dfu_file_parser.set_crc(crc_address=self.companion_debugger.FMM_CRC_STORE_ADDR,
                                        crc_data=crc)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Start DFU with security level = {secur_lvl}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self,
                    report=dfu_file_parser.dfu_start_command,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x27 (Bad/incompatible security level)')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.BAD_INCOMPATIBLE_SECURITY_LEVEL,
                                         packet_number=0)
            # end for
        # end if

        self.testCaseChecked("ERR_00D0_0071")
    # end def test_companion_lower_security_levels

    def _load_app_dfu_with_requested_level(self, secur_lvl_for_dfu, error_expected=False):

        # Get the supported version
        f = self.getFeatures()
        dfu_feature_version = self.get_dfu_version()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change dfuStart.securLvl of Regular_application.dfu file to '
                                 f'0x{secur_lvl_for_dfu:X} and sign it')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName),
            device_index=ChannelUtils.get_device_index(self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        dfu_file_parser.dfu_start_command.secur_lvl = secur_lvl_for_dfu

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self._perform_dfu(dfu_file_parser, error_expected)
    # end def _load_app_dfu_with_requested_level

    def _load_sd_dfu_with_requested_level(self, secur_lvl_for_dfu, error_expected=False):

        # Get the supported version
        f = self.getFeatures()
        dfu_feature_version = self.get_dfu_version()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Change dfuStart.securLvl of Regular_softdevice.dfu file to '
                                 f'0x{secur_lvl_for_dfu:X} and sign it')
        # --------------------------------------------------------------------------------------------------------------
        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", f.PRODUCT.FEATURES.COMMON.DFU.F_SoftDeviceDfuFileName),
            device_index=ChannelUtils.get_device_index(self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=False)

        dfu_file_parser.dfu_start_command.secur_lvl = secur_lvl_for_dfu

        key_file = join(TESTS_PATH, 'DFU_FILES', 'priv_tstkey_jenkins.pem')
        status = dfu_file_parser.compute_signature(
                                            key_file,
                                            max_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_HighestApplicationAddress,
                                            min_app_address=f.PRODUCT.FEATURES.COMMON.DFU.F_LowestApplicationAddress,
                                            additional_auth=f.PRODUCT.FEATURES.COMMON.DFU.F_AdditionalAuthentication)

        assert status, "Signature failed"

        dfu_file_parser.encrypt_decrypt_command_1(encrypt=True)

        self._perform_dfu(dfu_file_parser, error_expected)
    # end def _load_sd_dfu_with_requested_level

    def _perform_dfu(self, dfu_file_parser, error_expected):
        self.post_requisite_program_mcu_initial_state = True
        self.post_requisite_restart_in_main_application = False
        sequence_number = 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuStart : 16 first bytes of dfu data file')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self,
            report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        if error_expected:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x27 (Bad/incompatible security level)')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.BAD_INCOMPATIBLE_SECURITY_LEVEL)
            return

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 0')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                 packet_number=sequence_number)

        sequence_number += 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send dfuCmdData1 : next 16 bytes of dfu data file is command 1')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=self,
                report=cmd_1,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and pktNb = 1')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over the number of program data packets to be sent = '
                                     f'{len(program_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(program_data_list)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send dfuCmdDatax : next 16 bytes of dfu data '
                                         f'is program data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self,
                    report=program_data_list[i],
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and '
                                          f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send dfuCmdDatax : next 16 bytes of dfu data is command 2')
            # ----------------------------------------------------------------------------------------------------------
            dfu_status_response = ChannelUtils.send(
                test_case=self,
                report=cmd_2,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and '
                                      f'pktNb = {sequence_number}')
            # ----------------------------------------------------------------------------------------------------------
            self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                     status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                     packet_number=sequence_number)

            sequence_number += 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over the number of check data packets to be sent = '
                                     f'{len(check_data_list)}, packet number should start at 1')
            # ----------------------------------------------------------------------------------------------------------
            for i in range(len(check_data_list)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send dfuCmdDatax : next 16 bytes of dfu data is check data packet {i+1}')
                # ------------------------------------------------------------------------------------------------------
                dfu_status_response = ChannelUtils.send(
                    test_case=self,
                    report=check_data_list[i],
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x01 (Packet success) and '
                                          f'pktNb = {sequence_number}')
                # ------------------------------------------------------------------------------------------------------
                self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                         status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                         packet_number=sequence_number)

                sequence_number += 1
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ----------------------------------------------------------------------------------------------------------
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send dfuCmdDatax : next 16 bytes of dfu data is command 3')
        # --------------------------------------------------------------------------------------------------------------
        dfu_status_response = ChannelUtils.send(
            test_case=self,
            report=dfu_file_parser.command_3,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for dfuStatus with status = 0x02 or 0x06 (DFU success)')
        # --------------------------------------------------------------------------------------------------------------
        self.wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                 status=DfuStatusResponse.StatusValue.ALL_DFU_SUCCESS)
    # end def _perform_dfu
# end class SharedDfuTestCaseChangeSecurityLevel

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
