#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.uhs_power_on_test_cases
:brief: Validate UHS connection scheme for power on test cases
:author: Zane Lu
:date: 2022/10/4
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
class UhsPowerOnTestCases(UhsConnectionSchemeBase):
    """
    UHS connection scheme - Power On Test Cases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.restart_device()
    # end def setUp

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_the_pre_paired_uhs_receiver_business_case_in_reset_state(self):
        """
        Connection to a UHS receiver Business case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------

        self.verify_power_on([True, False, False, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_POWER_ON_0001")
    # end def test_connection_to_the_pre_paired_uhs_receiver_business_case_in_reset_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_a_uhs_receiver_when_a_paired_crush_is_available(self):
        """
        Connection to a UHS receiver when a paired Crush is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired UHS receiver powered on')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver not paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        self.verify_power_on([True, True, False, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_POWER_ON_0002")
    # end def test_connection_to_the_pre_paired_uhs_receiver_business_case_in_reset_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_a_uhs_receiver_when_a_crush_pairing_is_available(self):
        """
        Connection to a UHS receiver when a Crush pairing is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired UHS receiver powered on')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver not paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        self.verify_power_on([True, True, False, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_POWER_ON_0003")
    # end def test_connection_to_a_uhs_receiver_when_a_crush_pairing_is_available

    @features('UhsConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_a_uhs_receiver_when_a_ls2_pairing_receiver_is_powered_on(self):
        """
        Connection to a UHS receiver when a LS2-Pairing receiver is powered on
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired UHS receiver powered on')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        self.verify_power_on([True, False, True, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_POWER_ON_0004")
    # end def test_connection_to_a_uhs_receiver_when_a_ls2_pairing_receiver_is_powered_on

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_connection_business_case_in_reset_state(self):
        """
        Crush connection business Case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        self.verify_power_on([False, True, False, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_POWER_ON_0005")
    # end def test_crush_connection_business_case_in_reset_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_connection_in_reset_state_when_a_ls2_pairing_receiver_is_powered_on(self):
        """
        Crush connection in Reset state when a LS2-Pairing receiver is powered on
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        self.verify_power_on([False, True, True, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_POWER_ON_0006")
    # end def test_crush_connection_in_reset_state_when_a_ls2_pairing_receiver_is_powered_on

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_connection_in_reset_state_when_a_ls2_pairing_slot3_filled_in(self):
        """
        Crush connection in Reset state when LS2 Pairing Slot3 filled in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired but powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        self.verify_power_on([False, True, False, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_POWER_ON_0007")
    # end def test_crush_connection_in_reset_state_when_a_ls2_pairing_slot3_filled_in

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_pairing_business_case_in_reset_state(self):
        """
        Crush pairing business Case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        self.verify_power_on([False, True, False, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_POWER_ON_0008")
    # end def test_crush_pairing_business_case_in_reset_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_pairing_in_reset_state_when_a_ls2_pairing_receiver_is_powered_on(self):
        """
        Crush pairing in Reset state when a LS2-Pairing receiver is powered on
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)
        self.pair_ls2_receiver()

        self.verify_power_on([False, True, True, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_POWER_ON_0009")
    # end def test_crush_pairing_in_reset_state_when_a_ls2_pairing_receiver_is_powered_on

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_pairing_in_reset_state_when_ls2_pairing_slot3_filled_in(self):
        """
        Crush pairing in Reset state when LS2 Pairing Slot3 filled in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired but powered off')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)
        self.pair_ls2_receiver()

        self.verify_power_on([False, True, False, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_POWER_ON_0010")
    # end def test_crush_pairing_in_reset_state_when_ls2_pairing_slot3_filled_in

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_a_ls2_pairing_receiver_business_case_in_reset_state(self):
        """
        Connection to a LS2-Pairing receiver Business case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        self.verify_power_on([False, False, True, False, False], PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_POWER_ON_0011")
    # end def test_connection_to_a_ls2_pairing_receiver_business_case_in_reset_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_a_ls2_pairing_receiver_in_reset_state_when_crush_is_paired_but_powered_off(self):
        """
        Connection to a LS2-Pairing receiver in Reset state when Crush is paired but powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired but powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        self.verify_power_on([False, False, True, False, False], PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_POWER_ON_0012")
    # end def test_connection_to_a_ls2_pairing_receiver_in_reset_state_when_crush_is_paired_but_powered_off

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pairing_to_a_new_ls2_pairing_receiver_business_case_in_reset_state(self):
        """
        Pairing to a new LS2-Pairing receiver Business case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired but receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        self.verify_power_on([False, False, True, False, False], PortConfiguration.LS2_RECEIVER_PORT, openlock_mode=7)

        self.testCaseChecked("BUS_UHS_POWER_ON_0013")
    # end def test_pairing_to_a_new_ls2_pairing_receiver_business_case_in_reset_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_pairing_to_a_new_ls2_pairing_receiver_in_reset_state_while_crush_is_already_paired_but_powered_off(self):
        """
        Pairing to a new LS2-Pairing receiver in Reset state while Crush is already paired but powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired but receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        self.verify_power_on([False, False, True, False, False], PortConfiguration.LS2_RECEIVER_PORT, openlock_mode=7)

        self.testCaseChecked("FUN_UHS_POWER_ON_0014")
    # end def test_pairing_to_a_new_ls2_pairing_receiver_in_reset_state_while_crush_is_already_paired_but_powered_off

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_ls2_pairing_receiver_replacement_use_case_in_reset(self):
        """
        LS2-Pairing receiver replacement use case in Reset while
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired but powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot paired but receiver powered off')
        LogHelper.log_prerequisite(self, 'another LS2-2Devices receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        self.verify_power_on([False, False, False, True, False], PortConfiguration.LS2_RECEIVER2_PORT, openlock_mode=7)

        self.testCaseChecked("BUS_UHS_POWER_ON_0015")
    # end def test_ls2_pairing_receiver_replacement_use_case_in_reset

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pre_paired_uhs_receiver_replacement_business_case_in_reset(self):
        """
        Pre-paired UHS receiver replacement Business case in Reset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and receiver powered off')
        LogHelper.log_prerequisite(self, 'another UHS receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        self.verify_power_on([False, False, False, True, False], PortConfiguration.LS2_RECEIVER2_PORT, openlock_mode=1)

        self.testCaseChecked("BUS_UHS_POWER_ON_0016")
    # end def test_pre_paired_uhs_receiver_replacement_business_case_in_reset

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_pairing_to_a_new_uhs_receiver_in_reset_while_crush_is_already_paired_but_powered_off(self):
        """
        Pairing to a new UHS receiver in Reset while Crush is already paired but powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired but powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and receiver powered off')
        LogHelper.log_prerequisite(self, 'another UHS receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        self.verify_power_on([False, False, False, True, False], PortConfiguration.LS2_RECEIVER2_PORT, openlock_mode=1)

        self.testCaseChecked("FUN_UHS_POWER_ON_0017")
    # end def test_pairing_to_a_new_uhs_receiver_in_reset_while_crush_is_already_paired_but_powered_off

    @features('UhsConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_pairing_to_a_new_uhs_receiver_in_reset_while_the_ls2_pairing_receiver_is_powered_off(self):
        """
        Pairing to a new UHS receiver in Reset while the LS2-Pairing receiver is powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired but powered off')
        LogHelper.log_prerequisite(self, 'another UHS receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        self.verify_power_on([False, False, False, True, False], PortConfiguration.LS2_RECEIVER2_PORT, openlock_mode=1)

        self.testCaseChecked("FUN_UHS_POWER_ON_0018")
    # end def test_pairing_to_a_new_uhs_receiver_in_reset_while_the_ls2_pairing_receiver_is_powered_off

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_replacement_use_case_in_reset_state(self):
        """
        Crush replacement Use Case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired but another Crush On')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER2_PORT)

        self.verify_power_on([False, False, False, False, True], PortConfiguration.CRUSH_RECEIVER2_PORT)

        self.testCaseChecked("BUS_UHS_POWER_ON_0019")
        # end def test_crush_replacement_use_case_in_reset_state

    @features('UhsConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_in_deep_sleep_mode_in_reset_while_pre_paired_off(self):
        """
        Enter in Deep Sleep mode in Reset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_power_on_no_receiver_available()

        self.testCaseChecked("FUN_UHS_POWER_ON_0020")
    # end def test_enter_in_deep_sleep_mode_in_reset_while_pre_paired_off

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_in_deep_sleep_mode_in_reset_while_crush_is_already_paired_but_power_off(self):
        """
        Enter in Deep Sleep mode in Reset while Crush is already paired but power Off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired but powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        self.verify_power_on_no_receiver_available()

        self.testCaseChecked("FUN_UHS_POWER_ON_0021")
    # end def test_enter_in_deep_sleep_mode_in_reset_while_crush_is_already_paired_but_power_off

    @features('UhsConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_in_deep_sleep_mode_in_reset_while_the_ls2_pairing_receiver_is_powered_off(self):
        """
        Enter in Deep Sleep mode in Reset while the LS2-Pairing receiver is powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        self.verify_power_on_no_receiver_available()

        self.testCaseChecked("FUN_UHS_POWER_ON_0022")
    # end def test_enter_in_deep_sleep_mode_in_reset_while_the_ls2_pairing_receiver_is_powered_off

# end class UhsPowerOnTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
