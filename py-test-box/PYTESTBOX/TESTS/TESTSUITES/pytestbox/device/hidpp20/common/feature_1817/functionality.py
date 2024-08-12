#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1817.functionality
:brief: HID++ 2.0 ``LightspeedPrepairing`` functionality test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.lightspeedprepairing import GetPrepairingData
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairing
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagement
from pyhid.hidpp.features.common.lightspeedprepairing import SetLTK
from pyhid.hidpp.features.common.lightspeedprepairing import SetPrepairingData
from pyhid.hidpp.features.common.oobstate import OobState, OobStateFactory
from pyhid.hidpp.features.error import ErrorCodes
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
class LightspeedPrepairingFunctionalityTestCase(LightspeedPrepairingTestCase):
    """
    Validate ``LightspeedPrepairing`` functionality test cases
    """

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_have_been_preserved_after_a_OOB_reset(self):
        """
        Check the pre-pairing data have been preserved after a OOB reset
        """
        self.post_requisite_program_nvs = True
        slot = self._test_get_the_first_available_slot()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Roll out the Device Pre-pairing sequence on {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        rcvr_base_address, rcvr_last_dest_id, rcvt_equad_attributes = \
            LightspeedPrepairingTestUtils.get_the_pairing_information_from_the_receiver(self)

        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot,
            base_address=rcvr_base_address,
            last_dest_id=rcvr_last_dest_id,
            equad_attributes=rcvt_equad_attributes,
            long_term_key=RandHexList(SetLTK.LEN.LTK//8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x1805)")
        # --------------------------------------------------------------------------------------------------------------
        feature_1805_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=OobState.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the initial pre-pairing information")
        # --------------------------------------------------------------------------------------------------------------
        initial_base_address, initial_last_dest_id, initial_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # Get the 0x1805 feature
        feature_1805 = OobStateFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.OOB_STATE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Force device in OOB state")
        # --------------------------------------------------------------------------------------------------------------
        set_oob_state = feature_1805.set_oob_state_cls(device_index=ChannelUtils.get_device_index(test_case=self),
                                                       feature_index=feature_1805_index)
        ChannelUtils.send(test_case=self, report=set_oob_state,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=feature_1805.set_oob_state_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the current pre-pairing information")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current base addresses match")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=initial_base_address,
                         obtained=current_base_address,
                         msg='The current base address differs from the initial one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current last dest id match")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=initial_last_dest_id,
                         obtained=current_last_dest_id,
                         msg='The current last_dest_id differs from the initial one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current equad attributes match")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=initial_equad_attributes,
                         obtained=current_equad_attributes,
                         msg='The current equad attributes differs from the initial one')

        self.testCaseChecked("FUN_1817_0001", _AUTHOR)
    # end def test_check_the_prepairing_data_have_been_preserved_after_a_OOB_reset

    @features("Feature1817")
    @features('Feature1817LsSlotSupported')
    @features('Feature1817Ls2SlotSupported')
    @level("Functionality")
    def test_completing_the_pairing_sequence_shall_not_remove_the_prepairing_data_of_other_slots(self):
        """
        Validate `Completing the pairing sequence on one available slot
         shall not remove the pre-pairing data of other slots
        """
        ls_base_address = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        ls_equad_address = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        ls2_base_address1 = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        ls2_equad_address1 = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        ls2_base_address2 = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        ls2_equad_address2 = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        ltk = RandHexList(SetLTK.LEN.LTK//8)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence for LS and LS2")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.LS,
            base_address=ls_base_address,
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=ls_equad_address,
            long_term_key=ltk)

        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.LS2,
            base_address=ls2_base_address1,
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=ls2_equad_address1,
            long_term_key=ltk)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the base address for the LS slot")
        # --------------------------------------------------------------------------------------------------------------
        current_ls_base_address1, _, _ = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.LS,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the base address for the LS2 slot")
        # --------------------------------------------------------------------------------------------------------------
        current_ls2_base_address1, _, _ = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.LS2,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence a second time for LS2")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.LS2,
            base_address=ls2_base_address2,
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=ls2_equad_address2,
            long_term_key=ltk)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the base address for the LS slot")
        # --------------------------------------------------------------------------------------------------------------
        current_ls_base_address2, _, _ = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.LS,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the base address for the LS2 slot")
        # --------------------------------------------------------------------------------------------------------------
        current_ls2_base_address2, _, _ = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.LS2,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the base addresses of LS unchanged.")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=current_ls_base_address1,
                         obtained=current_ls_base_address2,
                         msg="The base addresses of LS shall be unchanged.")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the base address of LS2 changed.")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=current_ls2_base_address1,
                            obtained=current_ls2_base_address2,
                            msg="The base address of LS2 shall be changed.")

        self.testCaseChecked("FUN_1817_0002", _AUTHOR)
    # end def test_completing_the_pairing_sequence_shall_not_remove_the_prepairing_data_of_other_slots

    @features("Feature1817")
    @features('Feature1817LsSlotSupported')
    @level("Functionality")
    def test_prepairing_ls_slot_replacement(self):
        """
        Validate PrePairing LS slot replacement: Relaunch the pre-pairing sequence on a already paired LS slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence for LS")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.LS,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8),
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the initial base address for the LS slot")
        # --------------------------------------------------------------------------------------------------------------
        initial_base_address, initial_last_dest_id, initial_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.LS,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence a second time for LS")
        # --------------------------------------------------------------------------------------------------------------
        base_address_new = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes_new = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.LS,
            base_address=base_address_new,
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=equad_attributes_new,
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the current base address for the LS slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.LS,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the new base address has been stored")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=base_address_new,
                         obtained=current_base_address,
                         msg="The new base address shall be stored")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current base addresses differ")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=initial_base_address,
                            obtained=current_base_address,
                            msg="The base address shall differ from the old one")

        self.testCaseChecked("FUN_1817_0003", _AUTHOR)
    # end def test_prepairing_ls_slot_replacement

    @features("Feature1817")
    @features('Feature1817CrushSlotSupported')
    @level("Functionality")
    def test_prepairing_crush_slot_replacement(self):
        """
        Validate PrePairing Crush slot replacement: Relaunch the pre-pairing sequence on a already paired Crush slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence for Crush")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.CRUSH,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8),
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the initial base address for the Crush slot")
        # --------------------------------------------------------------------------------------------------------------
        initial_base_address, initial_last_dest_id, initial_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.CRUSH,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence a second time for Crush")
        # --------------------------------------------------------------------------------------------------------------
        base_address_new = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes_new = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.CRUSH,
            base_address=base_address_new,
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=equad_attributes_new,
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the current base address for the Crush slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.CRUSH,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the new base address has been stored")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=base_address_new,
                         obtained=current_base_address,
                         msg="The new base address shall be stored")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current base addresses differ")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=initial_base_address,
                            obtained=current_base_address,
                            msg="The base address shall differ from the old one")

        self.testCaseChecked("FUN_1817_0004", _AUTHOR)
    # end def test_prepairing_crush_slot_replacement

    @features("Feature1817")
    @features('Feature1817Ls2SlotSupported')
    @level("Functionality")
    def test_prepairing_ls2_slot_replacement(self):
        """
        Validate PrePairing LS2 slot replacement: Relaunch the pre-pairing sequence on a already paired LS2 slot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence for LS2")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.LS2,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8),
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the initial base address for the LS2 slot")
        # --------------------------------------------------------------------------------------------------------------
        initial_base_address, initial_last_dest_id, initial_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.LS2,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence a second time for LS2")
        # --------------------------------------------------------------------------------------------------------------
        base_address_new = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes_new = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=PrepairingManagement.PairingSlot.LS2,
            base_address=base_address_new,
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=equad_attributes_new,
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the current base address for the LS2 slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=PrepairingManagement.PairingSlot.LS2,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the new base address has been stored")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=base_address_new,
                         obtained=current_base_address,
                         msg="The new base address shall be stored")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current base addresses differ")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEqual(unexpected=initial_base_address,
                            obtained=current_base_address,
                            msg="The base address shall differ from the old one")

        self.testCaseChecked("FUN_1817_0005", _AUTHOR)
    # end def test_prepairing_ls2_slot_replacement

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_is_not_changed_if_no_ltk_data(self):
        """
        Check the pre-pairing data is not changed if no LTK data
        """
        slot = self._test_get_the_first_available_slot()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Roll out the Device Pre-pairing sequence for {slot!s}")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8),
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the initial base address for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        initial_base_address, initial_last_dest_id, initial_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence a second time "
                                 f"for {slot!s} with new base address but without calling set_LTK")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8))

        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        # expect to get the error NOT_ALLOWED(0x05)
        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the current base address for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current base addresses same")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=initial_base_address,
            obtained=current_base_address,
            msg="The base address shall be same")

        self.testCaseChecked("FUN_1817_0006", _AUTHOR)
    # end def test_check_the_prepairing_data_is_not_changed_if_no_ltk_data

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_is_not_changed_if_no_base_address_data(self):
        """
        Check the pre-pairing data is not changed if no base address data
        """
        slot = self._test_get_the_first_available_slot()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Roll out the Device Pre-pairing sequence for {slot!s}")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8),
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the initial base address for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        initial_base_address, initial_last_dest_id, initial_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence a second time "
                                 f"for {slot!s} with new base address but without set the new base address")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8))

        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=RandHexList(SetLTK.LEN.LTK//8))

        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        # expect to get the error NOT_ALLOWED(0x05)
        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the current base address for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current base addresses same")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=initial_base_address,
            obtained=current_base_address,
            msg="The base address shall be same")

        self.testCaseChecked("FUN_1817_0007", _AUTHOR)
    # end def test_check_the_prepairing_data_is_not_changed_if_no_base_address_data

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_is_not_changed_if_no_equad_attributes_data(self):
        """
        Check the pre-pairing data is not changed if no equad attributes data
        """
        slot = self._test_get_the_first_available_slot()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Roll out the Device Pre-pairing sequence for {slot!s}")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8),
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the initial base address for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        initial_base_address, initial_last_dest_id, initial_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence a second time "
                                 f"for {slot!s} with new base address but without equad attributes")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=RandHexList(SetLTK.LEN.LTK//8))

        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        # expect to get the error NOT_ALLOWED(0x05)
        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the current base address for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current base addresses same")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=initial_base_address,
            obtained=current_base_address,
            msg="The base address shall be same")

        self.testCaseChecked("FUN_1817_0008", _AUTHOR)
    # end def test_check_the_prepairing_data_is_not_changed_if_no_equad_attributes_data

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_is_not_changed_if_an_invalid_action_is_set_after_start(self):
        """
        Check the pre-pairing data is not changed if an invalid action is set
        after the prepairing_management_control 'Start' action
        """
        slot = self._test_get_the_first_available_slot()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Roll out the Device Pre-pairing sequence for {slot!s}")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8),
            long_term_key=RandHexList(SetLTK.LEN.LTK//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the initial base address for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        initial_base_address, initial_last_dest_id, initial_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence a second time "
                                 f"for {slot!s} with new base address but with calling an invalid control code command")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8))

        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=RandHexList(SetLTK.LEN.LTK//8))

        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=0xff # invalid control
        )

        # expect to get the error NOT_ALLOWED(0x05)
        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        # expect to get the error NOT_ALLOWED(0x05)
        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the current base address for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current base addresses same")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=initial_base_address,
            obtained=current_base_address,
            msg="The base address shall be same")

        self.testCaseChecked("FUN_1817_0009", _AUTHOR)
    # end def test_check_the_prepairing_data_is_not_changed_if_an_invalid_action_is_set_after_start

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_for_set_ltk_keya_then_set_keyb(self):
        """
        Check the pre-pairing data for set_LTK(keyA) then set_LTK(keyB)
        """
        self.post_requisite_reload_nvs = True

        base_address = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        key_a = RandHexList(SetLTK.LEN.LTK//8)
        key_b = RandHexList(SetLTK.LEN.LTK//8)
        slot = self._test_get_the_first_available_slot()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send prepairing_management with {slot!s} slot and control='Start'")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the base address")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=base_address,
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the equad attributes")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=equad_attributes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_LTK with keyA")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=key_a)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_LTK with keyB")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=key_b)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send prepairing_management with {slot!s} slot and control='Store'")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the current pre-pairing information for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the current pre-pairing information")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=base_address,
            obtained=current_base_address,
            msg="The base address shall be same")

        self.assertEqual(
            expected=equad_attributes,
            obtained=current_equad_attributes,
            msg="The equad attributes shall be same")

        self.testCaseChecked("FUN_1817_0010", _AUTHOR)
    # end def test_check_the_prepairing_data_for_set_ltk_keya_then_set_keyb

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_for_set_address_a_then_set_address_b(self):
        """
        Check the pre-pairing data for set_prepairing_data(AddressA) then set_prepairing_data(AddressB)
        """
        self.post_requisite_reload_nvs = True

        base_address_a = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        base_address_b = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        key = RandHexList(SetLTK.LEN.LTK//8)
        slot = self._test_get_the_first_available_slot()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send prepairing_management with {slot!s} slot and control='Start'")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the base address A")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=base_address_a,
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the base address B")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=base_address_b,
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the equad attributes")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=equad_attributes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_LTK with key")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send prepairing_management with {slot!s} slot and control='Store'")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the current pre-pairing information for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the current pre-pairing information")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=base_address_b,
            obtained=current_base_address,
            msg="The base address shall be same")

        self.assertEqual(
            expected=equad_attributes,
            obtained=current_equad_attributes,
            msg="The equad attributes shall be same")

        self.testCaseChecked("FUN_1817_0011", _AUTHOR)
    # end def test_check_the_prepairing_data_for_set_address_a_then_set_address_b

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_for_set_attributes_a_then_set_attributes_b(self):
        """
        Check the pre-pairing data for set_prepairing_data(Equad_AttributeA) then set_prepairing_data(Equad_AttributeB)
        """
        self.post_requisite_reload_nvs = True

        base_address = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes_a = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        equad_attributes_b = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        key = RandHexList(SetLTK.LEN.LTK//8)
        slot = self._test_get_the_first_available_slot()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send prepairing_management with {slot!s} slot and control='Start'")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the base address A")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=base_address,
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the equad attributes A")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=equad_attributes_a)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the equad attributes B")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=equad_attributes_b)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_LTK with key")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send prepairing_management with {slot!s} slot and control='Store'")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the current pre-pairing information for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the current pre-pairing information")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=base_address,
            obtained=current_base_address,
            msg="The base address shall be same")

        self.assertEqual(
            expected=equad_attributes_b,
            obtained=current_equad_attributes,
            msg="The equad attributes shall be same")

        self.testCaseChecked("FUN_1817_0012", _AUTHOR)
    # end def test_check_the_prepairing_data_for_set_attributes_a_then_set_attributes_b

    @features("Feature1817")
    @level("Functionality")
    def test_check_the_prepairing_data_for_interleaving_a_get_capabilities_request_between_each_prepairing_step(self):
        """
        Check the pre-pairing data for interleaving a get_capabilities request
        between each step of a valid pre pairing sequence
        """
        self.post_requisite_reload_nvs = True

        base_address = RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8)
        equad_attributes = RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        key = RandHexList(SetLTK.LEN.LTK//8)
        slot = self._test_get_the_first_available_slot()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send prepairing_management with {slot!s} slot and control='Start'")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send get_capabilities")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.get_capabilities(self);

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the base address")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=base_address,
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send get_capabilities")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.get_capabilities(self);

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data for the equad attributes")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=equad_attributes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send get_capabilities")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.get_capabilities(self);

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_LTK with key")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_ltk(
            test_case=self,
            ltk=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send prepairing_management with {slot!s} slot and control='Store'")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get the current pre-pairing information for {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        current_base_address, current_last_dest_id, current_equad_attributes = \
            LightspeedPrepairingTestUtils.get_pairing_information(
                test_case=self,
                slot_index=slot,
                information_type=GetPrepairingData.InfoType.PRE_PAIRING)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the current pre-pairing information")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=base_address,
            obtained=current_base_address,
            msg="The base address shall be same")

        self.assertEqual(
            expected=equad_attributes,
            obtained=current_equad_attributes,
            msg="The equad attributes shall be same")

        self.testCaseChecked("FUN_1817_0013", _AUTHOR)
    # end def test_check_the_prepairing_data_for_interleaving_a_get_capabilities_request_between_each_prepairing_step
# end class LightspeedPrepairingFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
