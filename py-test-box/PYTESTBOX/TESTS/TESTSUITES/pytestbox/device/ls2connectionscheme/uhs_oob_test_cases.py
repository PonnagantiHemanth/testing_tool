#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.uhs_oob_test_cases
:brief: Validate UHS connection scheme for OOB test cases
:author: Zane Lu
:date: 2022/10/3
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.ls2connectionscheme.uhs_connection_scheme import UhsConnectionSchemeBase
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UhsOobTestCases(UhsConnectionSchemeBase):
    """
    UHS connection scheme - OOB Test Cases
    """

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_the_prepaired_uhs_receiver_business_case_in_oob_state(self):
        """
        Connection to the pre-paired UHS receiver business case in OOB state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Crush never paired and powered off")
        LogHelper.log_info(self, "pre-paired UHS receiver powered on")
        LogHelper.log_info(self, "LS2-Pairing slot never paired and receiver powered off")
        # --------------------------------------------------------------------------------------------------------------

        self.verify_oob([True, False, False, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_OOB_0001")
    # end def test_connection_to_the_prepaired_uhs_receiver_business_case_in_oob_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_the_prepaired_uhs_receiver_while_crush_is_available(self):
        """
        Connection to the pre-paired UHS receiver while Crush is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered on")
        LogHelper.log_prerequisite(self, "pre-paired UHS receiver powered on")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered off")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        self.verify_oob([True, True, False, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_OOB_0002")
    # end def test_connection_to_the_prepaired_uhs_receiver_while_crush_is_available

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_the_prepaired_uhs_receiver_while_crush_and_ls2_pairing_receiver_are_available(self):
        """
        Connection to the pre-paired UHS receiver while Crush and LS2 Pairing receiver are available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered on")
        LogHelper.log_prerequisite(self, "pre-paired UHS receiver powered on")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        self.verify_oob([True, True, True, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_OOB_0003")
    # end def test_connection_to_the_prepaired_uhs_receiver_while_crush_and_ls2_pairing_receiver_are_available

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_pairing_business_case_in_oob_state(self):
        """
        Crush pairing business case in OOB state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered on")
        LogHelper.log_prerequisite(self, "pre-paired UHS receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered off")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        self.verify_oob([False, True, False, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_OOB_0004")
    # end def test_crush_pairing_business_case_in_oob_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_pairing_in_oob_state_when_ls2_pairing_receiver_is_available(self):
        """
        Crush pairing in OOB state when LS2-Pairing receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered on")
        LogHelper.log_prerequisite(self, "pre-paired UHS receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        self.verify_oob([False, True, True, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_OOB_0005")
    # end def test_crush_pairing_business_case_in_oob_state

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pairing_to_a_new_ls2_pairing_receiver_business_in_oob_state(self):
        """
        Pairing to a new LS2-Pairing receiver Business case in OOB state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered off")
        LogHelper.log_prerequisite(self, "pre-paired UHS receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired but receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        self.verify_oob([False, False, True, False, False], PortConfiguration.LS2_RECEIVER_PORT, openlock_mode=7)

        self.testCaseChecked("BUS_UHS_OOB_0006")
    # end def test_pairing_to_a_new_ls2_pairing_receiver_business_in_oob_state

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pre_paired_receiver_replacement_business_case_in_oob(self):
        """
        Pre-paired receiver replacement Business case in OOB
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered off")
        LogHelper.log_prerequisite(self, "pre-paired UHS receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered off")
        LogHelper.log_prerequisite(self, "another receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        self.verify_oob([False, False, False, True, False], PortConfiguration.LS2_RECEIVER2_PORT, openlock_mode=1)

        self.testCaseChecked("BUS_UHS_OOB_0007")
    # end def test_pre_paired_receiver_replacement_business_case_in_oob

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pre_paired_receiver_replacement_in_oob_while_an_ls2_pairing_receiver_is_available(self):
        """
        Pre-paired receiver replacement in OOB while an LS2-Pairing receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered off")
        LogHelper.log_prerequisite(self, "pre-paired UHS receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered on")
        LogHelper.log_prerequisite(self, "another receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        self.verify_oob([False, False, True, True, False], PortConfiguration.LS2_RECEIVER2_PORT, openlock_mode=1)

        self.testCaseChecked("BUS_UHS_OOB_0008")
    # end def test_pre_paired_receiver_replacement_in_oob_while_an_ls2_pairing_receiver_is_available

    @features('UhsConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_in_deep_sleep_mode_in_oob(self):
        """
        Enter in Deep Sleep mode in OOB
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Crush never paired and powered off")
        LogHelper.log_info(self, "pre-paired receiver powered off")
        LogHelper.log_info(self, "LS2-Pairing slot never paired and receiver powered off")
        # --------------------------------------------------------------------------------------------------------------
        self.verify_oob_no_receiver_available()

        self.testCaseChecked("FUN_UHS_OOB_0009")
    # end def test_enter_in_deep_sleep_mode_in_oob

# end class UhsOObTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
