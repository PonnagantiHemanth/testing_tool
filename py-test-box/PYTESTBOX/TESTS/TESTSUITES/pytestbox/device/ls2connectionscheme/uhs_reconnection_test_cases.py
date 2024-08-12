#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.uhs_reconnection_test_cases
:brief: Validate UHS connection scheme for reconnection test cases
:author: Zane Lu
:date: 2022/10/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.ls2connectionscheme.uhs_connection_scheme import UhsConnectionSchemeBase
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UhsReconnectionTestCases(UhsConnectionSchemeBase):
    """
    UHS connection scheme - Reconnection Test Cases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'the device is connected with the pre-paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        self.connect_to_the_pre_paired_receiver()
    # end def setUp

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_pre_paired_receiver_business_case_in_disconnected_state(self):
        """
        Connection to the Pre-paired UHS receiver Business case in Disconnected state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush slot never paired')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired')
        # --------------------------------------------------------------------------------------------------------------

        self.verify_reconnection([True, False, False, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_RECONNECTION_0001")
    # end def test_connection_to_pre_paired_receiver_business_case_in_disconnected_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_pre_paired_uhs_receiver_in_disconnected_state_while_crush_is_powered_on(self):
        """
        Connection to the Pre-paired UHS receiver in Disconnected state while Crush is powered on
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered on')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        self.verify_reconnection([True, True, False, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_RECONNECTION_0002")
    # end def test_connection_to_pre_paired_uhs_receiver_in_disconnected_state_while_crush_is_powered_on

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_pre_paired_uhs_receiver_in_disconnected_state_while_paired_crush_and_paired_ls2_rcvr_are_on(self):
        """
        Connection to the Pre-paired UHS receiver in Disconnected state
        while Crush and LS2-Pairing receiver are available and paired
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered on')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        self.verify_reconnection([True, True, True, False, False], PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_RECONNECTION_0003")
    # end def test_connection_to_pre_paired_uhs_receiver_in_disconnected_state_while_paired_crush_and_paired_ls2_rcvr_are_on

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_connection_business_case_in_disconnected_state(self):
        """
        Crush connection business Case in Disconnected state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        self.verify_reconnection([False, True, False, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_RECONNECTION_0004")
    # end def test_crush_connection_business_case_in_disconnected_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_cursh_connection_in_disconnected_state_when_ls2_pairing_receivers_is_available(self):
        """
        Crush connection in Disconnected state when LS2-Pairing receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        self.verify_reconnection([False, True, True, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_RECONNECTION_0005")
    # end def test_cursh_connection_in_disconnected_state_when_ls2_pairing_receivers_is_available

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_cursh_connection_in_disconnected_state_when_ls2_paired_receiver_off(self):
        """
        Crush connection in Disconnected state when LS2 Pairing Slot3 filled in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        self.verify_reconnection([False, True, False, False, False], PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_RECONNECTION_0006")
    # end def test_cursh_connection_in_disconnected_state_when_ls2_paired_receiver_off

    @features('UhsConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_ls2_pairing_receiver_business_case_in_disconnected_state(self):
        """
        Connection to a LS2-Pairing receiver Business case in Disconnected state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        self.verify_reconnection([False, False, True, False, False], PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("BUS_UHS_RECONNECTION_0007")
    # end def test_connection_to_ls2_pairing_receiver_business_case_in_disconnected_state

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_ls2_pairing_receiver_in_disconnected_state_while_crush_paired_but_off(self):
        """
        Connection to a LS2-Pairing receiver in Disconnected state while Crush is paired but power Off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        self.verify_reconnection([False, False, True, False, False], PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("FUN_UHS_RECONNECTION_0008")
    # end def test_connection_to_ls2_pairing_receiver_in_disconnected_state_while_crush_paired_but_off

    @features('UhsConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_deep_sleep_mode_in_disconnected_while_pre_paired_off(self):
        """
        Enter in Deep Sleep mode in Disconnected
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired')
        # --------------------------------------------------------------------------------------------------------------

        self.verify_reconnection_no_receiver_available()

        self.testCaseChecked("FUN_UHS_RECONNECTION_0009")
    # end def test_enter_deep_sleep_mode_in_disconnected_while_pre_paired_off

    @features('UhsConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_deep_sleep_mode_in_disconnected_while_crush_is_already_paired_but_powered_off(self):
        """
        Enter in Deep Sleep mode in Disconnected while Crush is already paired but powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        self.verify_reconnection_no_receiver_available()

        self.testCaseChecked("FUN_UHS_RECONNECTION_0010")
    # end def test_enter_deep_sleep_mode_in_disconnected_while_crush_is_already_paired_but_powered_off

    @features('UhsConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_in_deep_sleep_mode_in_disconnected_while_the_ls2_pairing_receiver_is_powered_off(self):
        """
        Enter in Deep Sleep mode in Disconnected while the LS2-Pairing receiver is powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing receiver paired and powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        self.verify_reconnection_no_receiver_available()

        self.testCaseChecked("FUN_UHS_RECONNECTION_0011")
    # end def test_enter_in_deep_sleep_mode_in_disconnected_while_the_ls2_pairing_receiver_is_powered_off

# end class UhsReconnectionTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
