#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.imageformat.business
:brief: Device Dual Bank Boot Image Format Business tests
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os.path import join

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.dualbank.boot.imageformat.imageformat import ImageFormatTestCase
from pytestbox.device.dualbank.boot.imageformat.imageformattestutils import ImageFormatTestUtils
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ImageFormatBusinessTestCase(ImageFormatTestCase):
    """
    Validate Image Format Business Case
    """

    @features('DualBank')
    @level('Business')
    def test_force_switch_app(self):
        """
        Check slot selection : set higher version on slot 0 and check it is selected on reset
        """
        pc_reg_idx = self.debugger.get_pc_register_index()
        pc_reg_val = self.debugger.get_pc_register_value(pc_reg_idx)
        initial_slot_index = ImageFormatTestUtils.get_slot_index(self,pc_reg_val)
        ImageFormatTestUtils.check_pc(self, pc_reg_val, initial_slot_index)
        final_slot_index = 1 if initial_slot_index == 0 else 0

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get device name")
        # --------------------------------------------------------------------------------------------------------------
        device_name_count = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name_count(self)
        initial_device_name = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
            self, to_int(device_name_count.device_name_count))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Device name : {initial_device_name}")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Fetch slot {final_slot_index} data")
        # --------------------------------------------------------------------------------------------------------------
        final_slot = ImageFormatTestUtils.SlotFactory.create(self)
        final_slot.base_address = to_int(self.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[final_slot_index])
        final_slot.init_header()
        final_slot.init_public_signature_key()
        final_slot.init_image()
        final_slot.init_trailer()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get slot {initial_slot_index} header")
        # --------------------------------------------------------------------------------------------------------------
        initial_slot = ImageFormatTestUtils.SlotFactory.create(self)
        initial_slot.base_address = to_int(self.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[initial_slot_index])
        initial_slot.init_mcu_boot_header()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Check Slot {initial_slot_index} version is greater than Slot {final_slot_index} version")
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(
            initial_slot.mcu_boot_header.image_version, final_slot.mcu_boot_header.image_version,
            f"Slot {initial_slot_index} version should be higher than slot {final_slot_index} version")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Increment Slot {final_slot_index} version")
        # --------------------------------------------------------------------------------------------------------------
        final_slot.mcu_boot_header.image_version.major = to_int(initial_slot.mcu_boot_header.image_version.major) + 1

        if self.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_Enabled and self.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_KeyCount > 0:
            # If key hierarchy is enabled, then we don't have access to the private key to sign the slot. So,
            # we have to generate a new private key and to update the key hierarchy.
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Generate new private key")
            # ----------------------------------------------------------------------------------------------------------
            key_path = str(join(TESTS_PATH, 'DFU_FILES', self.f.PRODUCT.DUAL_BANK.KEY_HIERARCHY.F_Keys[0]))
            first_key_hierarchy_private_key = final_slot.get_private_key_from_path(key_path)
            new_private_key = final_slot.generate_private_key()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get corresponding new public key")
            # ----------------------------------------------------------------------------------------------------------
            new_public_key = new_private_key.public_key()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Change entry in key hierarchy")
            # ----------------------------------------------------------------------------------------------------------
            final_slot.update_key_hierarchy_entry(
                index=-1, new_public_key=new_public_key, signing_key=first_key_hierarchy_private_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check second signature")
            # ----------------------------------------------------------------------------------------------------------
            signature = final_slot.get_signature_from_key_hierarchy(final_slot.key_hierarchy_table[-1].signature)
            final_slot.check_signature(first_key_hierarchy_private_key.public_key(),
                                       signature,
                                       final_slot.get_key_hierarchy_entry_signed_data(index=-1))

            public_key = final_slot.get_public_key_from_key_hierarchy(final_slot.key_hierarchy_table[0].public_key)
            final_slot.check_signature(public_key, signature, final_slot.get_key_hierarchy_entry_signed_data(index=-1))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Get key hash")
            # ----------------------------------------------------------------------------------------------------------
            final_slot.tlv_list.key_hash.key_hash = ImageFormatTestUtils.hash_data(
                final_slot.get_public_signature_key_bytes(new_public_key))

            private_signature_key = new_private_key
            public_signature_key = new_public_key
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Key hash doesn't change, no need to read it")
            # ----------------------------------------------------------------------------------------------------------
            if self.f.PRODUCT.DUAL_BANK.ROOT_OF_TRUST_TABLE.F_Enabled:
                key = self.f.PRODUCT.DUAL_BANK.ROOT_OF_TRUST_TABLE.F_Keys[0]
            else:
                key = self.f.PRODUCT.DUAL_BANK.F_Key
            # end if
            key_path = str(join(TESTS_PATH, 'DFU_FILES', key))
            private_signature_key = final_slot.get_private_key_from_path(key_path)
            public_signature_key = private_signature_key.public_key()
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get hash of slot header + slot image (+ protected TLV list if any)")
        # --------------------------------------------------------------------------------------------------------------
        slot_data = final_slot.get_slot_data()
        final_slot.tlv_list.slot_hash.slot_hash = ImageFormatTestUtils.hash_data(slot_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Sign image slot")
        # --------------------------------------------------------------------------------------------------------------
        new_signature = final_slot.sign(private_signature_key, slot_data)

        final_slot.tlv_info.tlv_tot = (to_int(final_slot.tlv_info.tlv_tot)
                                       - to_int(final_slot.tlv_list.signature.length)
                                       + len(new_signature))
        final_slot.tlv_list.signature.length = len(new_signature)
        final_slot.tlv_list.signature.signature = HexList(new_signature)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify signature")
        # --------------------------------------------------------------------------------------------------------------
        final_slot.check_signature(public_signature_key, final_slot.tlv_list.signature.signature, slot_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write new values")
        # --------------------------------------------------------------------------------------------------------------
        setattr(self, f"post_requisite_reload_header_slot_{final_slot_index}", True)
        setattr(self, f"post_requisite_reload_trailer_slot_{final_slot_index}", True)
        self.memory_manager.debugger.reset()
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.writeMemory(final_slot.base_address, final_slot.get_full_header())
        self.memory_manager.debugger.writeMemory(
            final_slot.base_address + to_int(final_slot.mcu_boot_header.ih_hdr_size), final_slot.image)
        self.memory_manager.debugger.writeMemory(final_slot.trailer_start_address, final_slot.tlv_info)
        self.memory_manager.debugger.writeMemory(final_slot.tlv_list_start_address, final_slot.tlv_list)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read device name")
        # --------------------------------------------------------------------------------------------------------------
        device_name_count = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name_count(self)
        device_name = DeviceTypeAndNameTestUtils.HIDppHelper.get_full_device_name(
            self, to_int(device_name_count.device_name_count))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Device name : {device_name}")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check PC value to check running slot")
        # --------------------------------------------------------------------------------------------------------------
        pc_reg_val = self.debugger.get_pc_register_value(pc_reg_idx)
        ImageFormatTestUtils.check_pc(self, pc_reg_val, final_slot_index)

        self.testCaseChecked("BUS_DUAL_BANK_IMG_0001")
    # end def test_force_switch_app
# end class ImageFormatBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
