#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.imageformat.interface
:brief: Device Dual Bank Boot Image Format Interface tests
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.mcu.mcuboot.imageformat import MagicNumbers
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.dualbank.boot.imageformat.imageformat import ImageFormatTestCase
from pytestbox.device.dualbank.boot.imageformat.imageformattestutils import ImageFormatTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ImageFormatInterfaceTestCase(ImageFormatTestCase):
    """
    Validate Image Format Interface Case
    """

    def _test_image_header(self, slot_index):
        """
        Check image header of a given slot

        :param slot_index: Slot index
        :type slot_index: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read image header")
        # --------------------------------------------------------------------------------------------------------------
        slot = ImageFormatTestUtils.SlotFactory.create(self)
        slot.base_address = to_int(self.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[slot_index])
        slot.init_mcu_boot_header()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check header matches configuration")
        # --------------------------------------------------------------------------------------------------------------
        exp_image_header = self.config_manager.get_feature(ConfigurationManager.ID.DUAL_BANK_IMAGE_HEADERS)[slot_index]
        self.assertEqual(exp_image_header, slot.mcu_boot_header, "Image header should be as expected")
    # end def _test_image_header

    @features('DualBank')
    @level('Interface')
    def test_image_header_slot0(self):
        """
        Check image header on slot 0
        """
        self._test_image_header(slot_index=0)
        self.testCaseChecked("INT_DUAL_BANK_IMG_0001")
    # end def test_image_header_slot0

    @features('DualBank')
    @level('Interface')
    def test_image_header_slot1(self):
        """
        Check image header on slot 1
        """
        self._test_image_header(slot_index=1)
        self.testCaseChecked("INT_DUAL_BANK_IMG_0002")
    # end def test_image_header_slot1

    def _test_image_trailer(self, slot_index):
        """
        Check image trailer of a given slot

        :param slot_index: Slot index
        :type slot_index: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Fetch slot data")
        # --------------------------------------------------------------------------------------------------------------
        slot = ImageFormatTestUtils.SlotFactory.create(self)
        slot.base_address = to_int(self.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[slot_index])
        slot.init_header()
        slot.init_public_signature_key()
        slot.init_image()
        slot.init_trailer()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check TLV info magic")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(HexList(Numeral(MagicNumbers.IMAGE_TLV_INFO_MAGIC)), slot.tlv_info.magic)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Compute expected public signature key hash")
        # --------------------------------------------------------------------------------------------------------------
        public_key_hash = slot.get_public_signature_key_hash()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Key Hash")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(public_key_hash, slot.tlv_list.key_hash.key_hash, "Key Hash should match")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Compute expected hash of slot header + slot image (+ protected TLV list if any)")
        # --------------------------------------------------------------------------------------------------------------
        slot_data = slot.get_slot_data()
        slot_hash = ImageFormatTestUtils.hash_data(slot_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Slot Hash")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(slot_hash, slot.tlv_list.slot_hash.slot_hash, "Slot Hash should match")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Verify signature")
        # --------------------------------------------------------------------------------------------------------------
        pad_len = 0
        while HexList(slot.tlv_list.signature.signature[-(pad_len + 1)]) == HexList("FF"):
            pad_len += 1
        # end while
        signature_len = len(slot.tlv_list.signature.signature) - pad_len
        slot.check_signature(slot.public_signature_key,
                             slot.tlv_list.signature.signature[:signature_len],
                             slot_data)
    # end def _test_image_trailer

    @features('DualBank')
    @level('Interface')
    def test_image_trailer_slot0(self):
        """
        Check image trailer for slot 0
        """
        self._test_image_trailer(slot_index=0)
        self.testCaseChecked("INT_DUAL_BANK_IMG_0003")
    # end def test_image_trailer_slot0

    @features('DualBank')
    @level('Interface')
    def test_image_trailer_slot1(self):
        """
        Check image trailer for slot 1
        """
        self._test_image_trailer(slot_index=1)
        self.testCaseChecked("INT_DUAL_BANK_IMG_0004")
    # end def test_image_trailer_slot1
# end class ImageFormatInterfaceTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
