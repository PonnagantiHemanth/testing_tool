#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1817.errorhandling
:brief: HID++ 2.0 ``LightspeedPrepairing`` error handling test suite
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
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.lightspeedprepairingutils import LightspeedPrepairingTestUtils
from pytestbox.device.hidpp20.common.feature_1817.lightspeedprepairing import LightspeedPrepairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LightspeedPrepairingErrorHandlingTestCase(LightspeedPrepairingTestCase):
    """
    Validate ``LightspeedPrepairing`` errorhandling test cases
    """

    @features("Feature1817")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1817.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1817.get_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index)
            report.functionIndex = function_index

            LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1817_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1817")
    @features("NoFeature1817CrushSlotSupported")
    @level("ErrorHandling")
    def test_verify_not_allowed_if_the_target_slot_is_not_available(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised
        if the prepairing_management action is called on a not available pairing slot.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify NOT_ALLOWED (5) is raised if the targetedSlot is not available")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=False,
            crush=True,
            ls=False,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1817_0002", _AUTHOR)
    # end test_verify_not_allowed_if_the_target_slot_is_not_available

    @features("Feature1817")
    @level("ErrorHandling")
    def test_verify_not_allowed_if_more_than_a_target_slot_is_set(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised
        if the prepairing_management action is called on more than a targetedSlot is set.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify NOT_ALLOWED (5) is raised if more than a targetedSlot is set")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=True,
            crush=False,
            ls=True,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1817_0003", _AUTHOR)
    # end test_verify_not_allowed_if_more_than_a_target_slot_is_set

    @features("Feature1817")
    @features("MultiplePairingSlots")
    @level("ErrorHandling")
    def test_verify_not_allowed_if_the_targeted_slot_is_not_the_same_for_start_store_action(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised
        if the prepairing_management action is called on the targetedSlot at Store action
        is not the same as the Start action.
        """
        self.post_requisite_reload_nvs = True
        slot = self._test_get_the_first_available_slot()
        second_slot = PrepairingManagement.PairingSlot.CRUSH if self.config.F_CrushSlot else \
            PrepairingManagement.PairingSlot.LS

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"start the pre-pairing sequence with START control on {slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "set the base address")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "set the equad attributes")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.HIDppHelper.set_prepairing_data(
            test_case=self,
            data_type=SetPrepairingData.DataType.EQUAD_ATTRIBUTES,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Verify NOT_ALLOWED (5) is raised if STORE action on {second_slot!s} slot")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=False,
            crush=second_slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=second_slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.STORE
        )

        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1817_0004", _AUTHOR)
    # end test_verify_not_allowed_if_the_targeted_slot_is_not_the_same_for_start_store_action

    @features("Feature1817")
    @level("ErrorHandling")
    def test_verify_not_allowed_if_prepairing_management_action_is_not_start_store_or_delete(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised
        if the prepairing_management action is called on not 'Start', 'Store', 'Delete'.
        """
        slot = self._test_get_the_first_available_slot()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify NOT_ALLOWED (5) is raised if the action is not START/STORE/DELETE")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=HexList(0xff))

        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1817_0005", _AUTHOR)
    # end def test_verify_not_allowed_if_prepairing_management_action_is_not_start_store_or_delete

    @features("Feature1817")
    @level("ErrorHandling")
    def test_verify_not_allowed_if_set_ltk_is_not_sent_in_the_active_prepairing_session(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised
        if the command set_LTK is not sent in active prepairing session.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify NOT_ALLOWED (5) is raised if set_ltk is not sent "
                                  "in active prepairing session")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.set_ltk_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ltk=RandHexList(SetLTK.LEN.LTK//8))

        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1817_0006", _AUTHOR)
    # end test_verify_not_allowed_if_set_ltk_is_not_sent_in_the_active_prepairing_session

    @features("Feature1817")
    @level("ErrorHandling")
    def test_verify_not_allowed_if_set_pairing_data_is_not_sent_in_the_active_prepairing_session(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised
        if the command set_prepairing_data is not sent in active prepairing session.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify NOT_ALLOWED (5) is raised "
                                  "if set_prepairing_data is not sent in active prepairing session")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.set_prepairing_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            data_type=SetPrepairingData.DataType.PAIRING_ADDRESS,
            pairing_address_base=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)

        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1817_0007", _AUTHOR)
    # end test_verify_not_allowed_if_set_pairing_data_is_not_sent_in_the_active_prepairing_session

    @features("Feature1817")
    @level("ErrorHandling")
    def test_verify_not_allowed_if_get_pairing_data_is_not_sent_in_the_active_prepairing_session(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised
        if the command get_prepairing_data is not sent in active prepairing session.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify NOT_ALLOWED (5) is raised "
                                  "if get_prepairing_data is not sent in active prepairing session")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.get_prepairing_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            information_type=GetPrepairingData.InfoType.PRE_PAIRING,
            data_type=GetPrepairingData.DataType.PAIRING_ADDRESS,
            reserved=HexList("00" * (GetPrepairingData.LEN.RESERVED // 8)))

        LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1817_0008", _AUTHOR)
    # end test_verify_not_allowed_if_get_pairing_data_is_not_sent_in_the_active_prepairing_session
# end class LightspeedPrepairingErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
