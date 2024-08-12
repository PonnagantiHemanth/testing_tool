#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1817.business
:brief: HID++ 2.0 ``LightspeedPrepairing`` business test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.lightspeedprepairing import GetPrepairingData
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairing
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagement
from pyhid.hidpp.features.common.lightspeedprepairing import SetLTK
from pyhid.hidpp.features.common.lightspeedprepairing import SetPrepairingData
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.lightspeedprepairingutils import LightspeedPrepairingTestUtils
from pytestbox.device.hidpp20.common.feature_1817.lightspeedprepairing import LightspeedPrepairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LightspeedPrepairingBusinessTestCase(LightspeedPrepairingTestCase):
    """
    Validate ``LightspeedPrepairing`` business test cases
    """

    @features("Feature1817")
    @features('Feature1817LsSlotSupported')
    @level('Business', 'SmokeTests')
    def test_device_prepairing_sequence_for_ls_slot(self):
        """
        Verify the device prepairing sequence for LS slot
        """
        self.verify_device_prepairing_sequence(slot_index=PrepairingManagement.PairingSlot.LS)
        self.testCaseChecked("BUS_1817_0001", _AUTHOR)
    # end def test_device_prepairing_sequence_for_ls_slot

    @features("Feature1817")
    @features('Feature1817CrushSlotSupported')
    @level("Business")
    def test_device_prepairing_sequence_for_crush_slot(self):
        """
        Verify the device prepairing sequence for CRUSH slot
        """
        self.verify_device_prepairing_sequence(slot_index=PrepairingManagement.PairingSlot.CRUSH)
        self.testCaseChecked("BUS_1817_0002", _AUTHOR)
    # end def test_device_prepairing_sequence_for_crush_slot

    @features("Feature1817")
    @features('Feature1817Ls2SlotSupported')
    @level("Business")
    def test_device_prepairing_sequence_for_ls2_slot(self):
        """
        Verify the device prepairing sequence for LS2 slot
        """
        self.verify_device_prepairing_sequence(slot_index=PrepairingManagement.PairingSlot.LS2)
        self.testCaseChecked("BUS_1817_0003", _AUTHOR)
    # end def test_device_prepairing_sequence_for_ls2_slot

    @features("Feature1817")
    @features('Feature1817LsSlotSupported')
    @level("Business")
    def test_delete_the_prepairing_data_on_ls_slot(self):
        """
        Verify the deletion of the prepairing data for LS slot
        """
        self.verify_delete_the_prepairing_data(slot_index=PrepairingManagement.PairingSlot.LS)
        self.testCaseChecked("BUS_1817_0004", _AUTHOR)
    # end def test_delete_the_prepairing_data_on_ls_slot

    @features("Feature1817")
    @features('Feature1817CrushSlotSupported')
    @level("Business")
    def test_delete_the_prepairing_data_on_crush_slot(self):
        """
        Verify the deletion of the prepairing data for CRUSH slot
        """
        self.verify_delete_the_prepairing_data(slot_index=PrepairingManagement.PairingSlot.CRUSH)
        self.testCaseChecked("BUS_1817_0005", _AUTHOR)
    # end def test_delete_the_prepairing_data_on_crush_slot

    @features("Feature1817")
    @features('Feature1817Ls2SlotSupported')
    @level("Business")
    def test_delete_the_prepairing_data_on_ls2_slot(self):
        """
        Verify the deletion of the prepairing data for LS2 slot
        """
        self.verify_delete_the_prepairing_data(slot_index=PrepairingManagement.PairingSlot.LS2)
        self.testCaseChecked("BUS_1817_0006", _AUTHOR)
    # end def test_delete_the_prepairing_data_on_ls2_slot

    @features("Feature1817")
    @features('Feature1817LsSlotSupported')
    @level("Business")
    def test_read_prepairing_data_for_ls_slot(self):
        """
        Verify reading the prepairing data for LS slot
        """
        self.verify_read_prepairing_data_sequence(slot_index=PrepairingManagement.PairingSlot.LS)
        self.testCaseChecked("BUS_1817_0007", _AUTHOR)
    # end def test_read_prepairing_data_for_ls_slot

    @features("Feature1817")
    @features('Feature1817CrushSlotSupported')
    @level("Business")
    def test_read_prepairing_data_for_crush_slot(self):
        """
        Verify reading the prepairing data for CRUSH slot
        """
        self.verify_read_prepairing_data_sequence(slot_index=PrepairingManagement.PairingSlot.CRUSH)
        self.testCaseChecked("BUS_1817_0008", _AUTHOR)
    # end def test_read_prepairing_data_for_crush_slot

    @features("Feature1817")
    @features('Feature1817Ls2SlotSupported')
    @level("Business")
    def test_read_prepairing_data_for_ls2_slot(self):
        """
        Verify reading the prepairing data for LS2 slot
        """
        self.verify_read_prepairing_data_sequence(slot_index=PrepairingManagement.PairingSlot.LS2)
        self.testCaseChecked("BUS_1817_0009", _AUTHOR)
    # end def test_read_prepairing_data_for_ls2_slot

    def verify_device_prepairing_sequence(self, slot_index):
        """
        Verify the device prepairing sequence

        :param slot_index: index for LS(0x01), Crush(0x02), LS2(0x04)
        :type slot_index: ``int``
        """
        self.post_requisite_reload_nvs = True

        base_address = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "prepairing_management (Start, the specific slot)")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=(slot_index == PrepairingManagement.PairingSlot.LS2),
            crush=(slot_index == PrepairingManagement.PairingSlot.CRUSH),
            ls=(slot_index == PrepairingManagement.PairingSlot.LS),
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "set_prepairing_data(pairing address, equad attributes)")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=base_address,
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=equad_attributes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "set_LTK(ltk)")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=RandHexList(SetLTK.LEN.LTK//8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "prepairing_management (Store, the specific slot)")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=(slot_index == PrepairingManagement.PairingSlot.LS2),
            crush=(slot_index == PrepairingManagement.PairingSlot.CRUSH),
            ls=(slot_index == PrepairingManagement.PairingSlot.LS),
            prepairing_management_control=PrepairingManagement.Control.STORE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the current base address / equad attributes for the specific slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot_index,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the pre-pairing data of LS is correct")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=base_address,
                         obtained=current_base_address,
                         msg="The base address shall be same")

        self.assertEqual(expected=equad_attributes,
                         obtained=current_equad_attributes,
                         msg="The equad attributes shall be same")
    # end def verify_device_prepairing_sequence

    def verify_delete_the_prepairing_data(self, slot_index):
        """
        Verify the deletion of the prepairing data

        :param slot_index: index for LS(0x01), Crush(0x02), LS2(0x04)
        :type slot_index: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence for the specific slot")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot_index,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8),
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "prepairing_management(Delete, the specific slot)")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=(slot_index == PrepairingManagement.PairingSlot.LS2),
            crush=(slot_index == PrepairingManagement.PairingSlot.CRUSH),
            ls=(slot_index == PrepairingManagement.PairingSlot.LS),
            prepairing_management_control=PrepairingManagement.Control.DELETE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the prepairing data of the specific slot is empty")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=(slot_index == PrepairingManagement.PairingSlot.LS2),
            crush=(slot_index == PrepairingManagement.PairingSlot.CRUSH),
            ls=(slot_index == PrepairingManagement.PairingSlot.LS),
            prepairing_management_control=PrepairingManagement.Control.START
        )

        report = self.feature_1817.get_prepairing_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            information_type=GetPrepairingData.InfoType.PRE_PAIRING,
            data_type=GetPrepairingData.DataType.PAIRING_ADDRESS,
            reserved=HexList("00" * (GetPrepairingData.LEN.RESERVED // 8)))

        # expect to get the error 0x04 (HW_ERROR)
        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.HW_ERROR])
    # end def verify_delete_the_prepairing_data

    def verify_read_prepairing_data_sequence(self, slot_index):
        """
        Verify reading prepairing data sequence

        :param slot_index: index for LS(0x01), Crush(0x02), LS2(0x04)
        :type slot_index: ``int``
        """
        base_address = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence for the specific slot")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot_index,
            base_address=base_address,
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=equad_attributes,
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the prepairing information")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, _, current_equad_attributes =\
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot_index,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING
            )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the prepairing data for the specific slot")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=base_address,
                         obtained=current_base_address,
                         msg="The base address shall be same")

        self.assertEqual(expected=equad_attributes,
                         obtained=current_equad_attributes,
                         msg="The equad attributes shall be same")
    # end def verify_read_prepairing_data_sequence

# end class LightspeedPrepairingBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
