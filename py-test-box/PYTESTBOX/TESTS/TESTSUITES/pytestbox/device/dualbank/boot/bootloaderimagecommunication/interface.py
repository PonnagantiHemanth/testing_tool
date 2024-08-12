#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.bootloaderimagecommunication.interface
:brief: Device Dual Bank Boot Bootloader Image Communication Interface tests
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.mcu.mcuboot.imageformat import BootImageCommunication
from pylibrary.mcu.mcuboot.imageformat import BootImageCommunicationWithRootOfTrust
from pylibrary.mcu.mcuboot.imageformat import KeyHierarchyHeader
from pylibrary.mcu.mcuboot.imageformat import MagicNumbers
from pylibrary.mcu.mcuboot.imageformat import RootOfTrust
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.bootloaderimagecommunication import \
    BootloaderImageCommunicationTestCase
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.bootloaderimagecommunicationtestutils import \
    BootloaderImageCommunicationTestUtils
from pytestbox.device.dualbank.boot.imageformat.imageformattestutils import ImageFormatTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BootloaderImageCommunicationInterfaceTestCase(BootloaderImageCommunicationTestCase):
    """
    Validate Bootloader to Image Communication Interface Case
    """

    @features('DualBank')
    @level('Interface')
    def test_bootloader_image_communication_info(self):
        """
        Check bootloader info in Bootloader Image Communication structure
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get bootloader image communication structure")
        # --------------------------------------------------------------------------------------------------------------
        bic_comm = BootloaderImageCommunicationTestUtils.get_structure(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check bootloader image communication structure")
        # --------------------------------------------------------------------------------------------------------------
        git_hash = self.config_manager.get_feature(ConfigurationManager.ID.LOGI_MCU_BOOT_GIT_HASH)
        build_flags = HexList(BootImageCommunication.BuildFlags(
            dirty_build=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_DirtyBuildFlag,
            debug_build=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_DebugBuildFlag,
            development_credentials=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_DevelopmentCredentialsFlag
        ))

        # ASCII to HexList conversion + padding
        fw_prefix = HexList(
            [ord(i) for i in self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_FwPrefix[::-1] if i != ' '])
        fw_prefix.addPadding(size=BootImageCommunication.LEN.PREFIX // 8)

        if self.f.PRODUCT.DUAL_BANK.ROOT_OF_TRUST_TABLE.F_Enabled:
            expected_bic_comm = BootImageCommunicationWithRootOfTrust(
                magic_number=MagicNumbers.BIC_COMM_MAGIC,
                version=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_Version,
                prefix=fw_prefix,
                fw_number=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_FwNumber,
                fw_version=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_FwVersion,
                fw_build_number=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_FwBuildNumber,
                git_hash=git_hash,
                build_flags=build_flags,
                root_of_trust_count=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_RootOfTrustCount,
                root_of_trust_addr=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_RootOfTrustAddr,
                bl_to_img_flags=bic_comm.bl_to_img_flags,  # Dynamic fields can be ignored in this test
                img_to_bl_flags=bic_comm.img_to_bl_flags   # Dynamic fields can be ignored in this test
            )
        else:
            expected_bic_comm = BootImageCommunication(
                magic_number=MagicNumbers.BIC_COMM_MAGIC,
                version=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_Version,
                prefix=fw_prefix,
                fw_number=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_FwNumber,
                fw_version=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_FwVersion,
                fw_build_number=self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_FwBuildNumber,
                git_hash=git_hash,
                build_flags=build_flags,
                bl_to_img_flags=bic_comm.bl_to_img_flags,  # Dynamic fields can be ignored in this test
                img_to_bl_flags=bic_comm.img_to_bl_flags  # Dynamic fields can be ignored in this test
            )
        # end if

        self.assertEqual(expected_bic_comm, bic_comm, "Bootloader to Image Communication should be as expected")

        self.testCaseChecked("INT_DUAL_BANK_COM_0001")
    # end def test_bootloader_image_communication_info

    @features('DualBank')
    @level('Interface')
    def test_currently_booted_slot(self):
        """
        Check currently booted slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get bootloader image communication bootloader to image flags")
        # --------------------------------------------------------------------------------------------------------------
        bl_to_img_flags = BootloaderImageCommunicationTestUtils.get_bl_to_img_flags(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check currently booted slot flag")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=BootImageCommunication.BlToImgFlags.BootedSlot.DEFAULT_SLOT,
                         obtained=bl_to_img_flags.booted_slot,
                         msg="Currently booted slot should be default slot")

        self.testCaseChecked("INT_DUAL_BANK_COM_0002")
    # end def test_currently_booted_slot

    def _test_key_hierarchy(self, slot_index):
        """
        Check key hierarchy for a given slot

        :param slot_index: Slot index
        :type slot_index: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get slot key hierarchy")
        # --------------------------------------------------------------------------------------------------------------
        slot = ImageFormatTestUtils.SlotFactory.create(self)
        slot.base_address = to_int(self.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[slot_index])
        slot.init_header()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check key hierarchy header")
        # --------------------------------------------------------------------------------------------------------------
        expected_key_hierarchy_header = KeyHierarchyHeader(magic_number=MagicNumbers.KEY_HIERARCHY_MAGIC,
                                                           root_of_trust_index=0,
                                                           key_count=self.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_KeyCount,
                                                           reserved=0x0000)
        self.assertEqual(expected_key_hierarchy_header, slot.key_hierarchy_header, "Key Hierarchy header should match")

        if self.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_KeyCount > 0:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check first key")
            # ----------------------------------------------------------------------------------------------------------
            key_path = str(join(TESTS_PATH, 'DFU_FILES', self.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_Keys[0]))
            expected_pub_key = HexList(slot.get_key_hierarchy_public_key_bytes(
                slot.get_private_key_from_path(key_path).public_key()))
            pub_key = slot.get_public_key_from_key_hierarchy(slot.key_hierarchy_table[0].public_key)
            pub_key = HexList(slot.get_key_hierarchy_public_key_bytes(pub_key))
            self.assertEqual(expected_pub_key, pub_key, "First public key in key hierarchy should match expected one")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check first signature")
            # ----------------------------------------------------------------------------------------------------------
            root_of_trust_key_addr = BootloaderImageCommunicationTestUtils.get_root_of_trust_table(self)[
                to_int(slot.key_hierarchy_header.root_of_trust_index)].public_key_address
            root_of_trust_key = self.memory_manager.debugger.readMemory(to_int(root_of_trust_key_addr),
                                                                        slot.public_signature_key_size)
            root_of_trust_key = slot.get_public_key_from_root_of_trust(root_of_trust_key)
            signature = slot.get_signature_from_key_hierarchy(HexList(slot.key_hierarchy_table[0].signature))
            slot.check_signature(root_of_trust_key, signature, slot.get_key_hierarchy_entry_signed_data(index=0))
        # end if

        if self.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_KeyCount > 1:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Second key can not be directly checked as the private key is not known")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check second signature")
            # ----------------------------------------------------------------------------------------------------------
            public_key = slot.key_hierarchy_table[0].public_key
            public_key = slot.get_public_key_from_key_hierarchy(public_key)
            signature = slot.get_signature_from_key_hierarchy(HexList(slot.key_hierarchy_table[1].signature))
            slot.check_signature(public_key, signature, slot.get_key_hierarchy_entry_signed_data(index=1))
        # end if
    # end def _test_key_hierarchy

    @features('DualBank')
    @level('Interface')
    def test_key_hierarchy_slot0(self):
        """
        Check key hierarchy for slot 0
        """
        self._test_key_hierarchy(slot_index=0)
        self.testCaseChecked("INT_DUAL_BANK_COM_0003")
    # end def test_key_hierarchy_slot0

    @features('DualBank')
    @level('Interface')
    def test_key_hierarchy_slot1(self):
        """
        Check key hierarchy for slot 1
        """
        self._test_key_hierarchy(slot_index=1)
        self.testCaseChecked("INT_DUAL_BANK_COM_0004")
    # end def test_key_hierarchy_slot1

    @features('DualBank')
    @features('RootOfTrustTable')
    @level('Interface')
    def test_root_of_trust_table(self):
        """
        Check root of trust table
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get root of trust table")
        # --------------------------------------------------------------------------------------------------------------
        rot_table = BootloaderImageCommunicationTestUtils.get_root_of_trust_table(self)
        rot_util = ImageFormatTestUtils.RootOfTrustFactory.create(self)
        dev_cred = self.f.PRODUCT.DUAL_BANK.BOOTLOADER_IMAGE_COMMUNICATION.F_DevelopmentCredentialsFlag

        for rot_index, rot in enumerate(rot_table):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get public key")
            # ----------------------------------------------------------------------------------------------------------
            pub_key_addr = to_int(rot.public_key_address)
            key_path = str(join(TESTS_PATH, 'DFU_FILES',
                                self.f.PRODUCT.DUAL_BANK.ROOT_OF_TRUST_TABLE.F_Keys[rot_index]))
            key_type = RootOfTrust.EncodedFlags.Type[self.f.PRODUCT.DUAL_BANK.ROOT_OF_TRUST_TABLE.F_Types[rot_index]]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check root of trust public key")
            # ----------------------------------------------------------------------------------------------------------
            rot_util.check_root_of_trust_public_key(key_path, pub_key_addr, dev_cred, key_type)
        # end for
        self.testCaseChecked("INT_DUAL_BANK_COM_0005")
    # end def test_root_of_trust_table
# end class BootloaderImageCommunicationInterfaceTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
