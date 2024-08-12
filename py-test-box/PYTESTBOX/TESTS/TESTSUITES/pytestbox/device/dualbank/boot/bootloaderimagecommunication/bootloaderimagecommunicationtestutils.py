#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.bootloaderimagecommunication.bootloaderimagecommunicationtestutils
:brief: Helpers for Bootloader Image Communication feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/12/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.mcu.mcuboot.imageformat import BootImageCommunication
from pylibrary.mcu.mcuboot.imageformat import BootImageCommunicationWithRootOfTrust
from pylibrary.mcu.mcuboot.imageformat import RootOfTrust
from pylibrary.mcu.mcuboot.imageformat import RootOfTrustTable
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.memoryutils import SharedMemoryTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BootloaderImageCommunicationTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on Bootloader Image Communication feature
    """

    @staticmethod
    def get_structure(test_case):
        """
        Get Bootloader Image communication structure

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Bootloader Image communication structure
        :rtype: ``BootImageCommunication``
        """
        ram_noinit_start_addr, _ = SharedMemoryTestUtils.RamHelper.get_ram_noinit_address_size(
            test_case.f.PRODUCT.CODE_CHECKLIST.F_BootLoaderElfFileName)
        if test_case.f.PRODUCT.DUAL_BANK.ROOT_OF_TRUST_TABLE.F_Enabled:
            bic_comm_raw = test_case.memory_manager.debugger.readMemory(
                ram_noinit_start_addr,
                sum([field.length for field in BootImageCommunicationWithRootOfTrust.FIELDS]) // 8)
            bic_comm = BootImageCommunicationWithRootOfTrust.fromHexList(bic_comm_raw)
        else:
            bic_comm_raw = test_case.memory_manager.debugger.readMemory(
                ram_noinit_start_addr, sum([field.length for field in BootImageCommunication.FIELDS]) // 8)
            bic_comm = BootImageCommunication.fromHexList(bic_comm_raw)
        # end if
        return bic_comm
    # end def get_structure

    @classmethod
    def get_bl_to_img_flags(cls, test_case):
        """
        Get Bootloader to Image flags in Bootloader-Image communication structure

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Bootloader to Image flags
        :rtype: ``BootImageCommunication.BlToImgFlags``
        """
        bic_comm = cls.get_structure(test_case)
        bl_to_img_flags = BootImageCommunication.BlToImgFlags.fromHexList(bic_comm.bl_to_img_flags)
        return bl_to_img_flags
    # end def get_bl_to_img_flags

    @classmethod
    def get_img_to_bl_flags(cls, test_case):
        """
        Get Image to Bootloader flags in Bootloader-Image communication structure

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Image to Bootloader flags
        :rtype: ``BootImageCommunication.ImgToBlFlags``
        """
        bic_comm = cls.get_structure(test_case)
        img_to_bl_flags = BootImageCommunication.ImgToBlFlags.fromHexList(bic_comm.img_to_bl_flags)
        return img_to_bl_flags
    # end def get_img_to_bl_flags

    @classmethod
    def set_cold_boot_request(cls, test_case, cold_boot_request=False):
        """
        Set cold boot request flag in image to bootloader flags

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param cold_boot_request: Cold boot request flag value
        :type cold_boot_request: ``bool``
        """
        bic_comm = cls.get_structure(test_case)
        img_to_bl_flags = HexList(BootImageCommunication.ImgToBlFlags(cold_boot_request=cold_boot_request))
        bic_comm.img_to_bl_flags |= img_to_bl_flags
        ram_noinit_start_addr, _ = SharedMemoryTestUtils.RamHelper.get_ram_noinit_address_size(
            test_case.f.PRODUCT.CODE_CHECKLIST.F_BootLoaderElfFileName)
        test_case.memory_manager.debugger.writeMemory(ram_noinit_start_addr, bic_comm)
    # end def set_cold_boot_request

    @classmethod
    def set_alternate_slot_request(cls, test_case, alternate_slot_request=False):
        """
        Set alternate slot request flag in image to bootloader flags

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param alternate_slot_request: Alternate slot request flag value
        :type alternate_slot_request: ``bool``
        """
        bic_comm = cls.get_structure(test_case)
        img_to_bl_flags = HexList(BootImageCommunication.ImgToBlFlags(alternate_slot_request=alternate_slot_request))
        bic_comm.img_to_bl_flags |= img_to_bl_flags
        ram_noinit_start_addr, _ = SharedMemoryTestUtils.RamHelper.get_ram_noinit_address_size(
            test_case.f.PRODUCT.CODE_CHECKLIST.F_BootLoaderElfFileName)
        test_case.memory_manager.debugger.writeMemory(ram_noinit_start_addr, bic_comm)
    # end def set_alternate_slot_request

    @classmethod
    def get_root_of_trust_table(cls, test_case):
        """
        Get root of trust table

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Root of trust table
        :rtype: ``RootOfTrustTable``
        """
        bic_comm = cls.get_structure(test_case)
        rot_table_cnt = to_int(bic_comm.root_of_trust_count)
        rot_table_addr = to_int(bic_comm.root_of_trust_addr)
        rot_table_raw = test_case.memory_manager.debugger.readMemory(
            rot_table_addr, rot_table_cnt * sum([field.length for field in RootOfTrust.FIELDS]) // 8)
        rot_table = RootOfTrustTable.fromHexList(rot_table_raw)
        return rot_table
    # end def get_root_of_trust_table
# end class BootloaderImageCommunicationTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
