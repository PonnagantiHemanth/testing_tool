#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.reconnection_test_cases
:brief: Validate LS2 connection scheme for RECONNECTION test cases
:author: Zane Lu
:date: 2020/11/5
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.ls2connectionscheme.uhs_connection_scheme import UhsConnectionSchemeBase
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReconnectionTestCases(UhsConnectionSchemeBase):
    """
    LS2 connection scheme - Power On Test Cases
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

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_connection_business_case_in_disconnected_state(self):
        """
        Crush connection business Case in Disconnected state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[False, True, False, False, False],
                                 target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0033")
    # end def test_crush_connection_business_case_in_disconnected_state

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_connection_in_disconnected_state_when_pre_paired_receiver_is_available(self):
        """
        Crush connection in Disconnected state when pre-paired receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[True, True, False, False, False],
                                 target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0034")
    # end def test_crush_connection_in_disconnected_state_when_pre_paired_receiver_is_available

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_cursh_connection_in_disconnected_state_when_pre_paired_and_ls2_pairing_receivers_are_available(self):
        """
        Crush connection in Disconnected state when pre-paired and LS2-Pairing receivers are available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered on')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[True, True, True, False, False],
                                 target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0035")
    # end def test_cursh_connection_in_disconnected_state_when_pre_paired_and_ls2_pairing_receivers_are_available

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_connection_in_disconnected_state_when_pre_paired_receiver_on_and_ls2_paired_receiver_off(self):
        """
        Crush connection in Disconnected state when pre-paired receiver is available and LS2 Pairing Slot3 filled in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered off')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[True, True, False, False, False],
                                 target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0036")
    # end def test_crush_connection_in_disconnected_state_when_pre_paired_receiver_on_and_ls2_paired_receiver_off

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_ls2_pairing_receiver_business_case_in_disconnected_state(self):
        """
        Connection to a LS2-Pairing receiver Business case in Disconnected state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered on')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[False, False, True, False, False],
                                 target_port=PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0037")
    # end def test_connection_to_ls2_pairing_receiver_business_case_in_disconnected_state

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_ls2_pairing_receiver_in_disconnected_state_while_crush_paired_but_off(self):
        """
        Connection to a LS2-Pairing receiver in Disconnected state while Crush is paired but power Off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered on')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[False, False, True, False, False],
                                 target_port=PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0038")
    # end def test_connection_to_ls2_pairing_receiver_in_disconnected_state_while_crush_paired_but_off

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_ls2_pairing_receiver_in_disconnected_state_when_pre_paired_receiver_is_available(self):
        """
        Connection to a LS2-Pairing receiver in Disconnected state when pre-paired receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered on')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[True, False, True, False, False],
                                 target_port=PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0039")
    # end def test_connection_to_ls2_pairing_receiver_in_disconnected_state_when_pre_paired_receiver_is_available

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_pre_paired_receiver_business_case_in_disconnected_state(self):
        """
        Connection to the Pre-paired receiver Business case in Disconnected state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush slot never paired')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[True, False, False, False, False],
                                 target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0040")
    # end def test_connection_to_pre_paired_receiver_business_case_in_disconnected_state

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_pre_paired_receiver_in_disconnected_state_while_crush_paired_and_off(self):
        """
        Connection to the Pre-paired receiver in Disconnected state while Crush is powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[True, False, False, False, False],
                                 target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0041")
    # end def test_connection_to_pre_paired_receiver_in_disconnected_state_while_crush_paired_and_off

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_pre_paired_rcvr_in_disconnected_state_while_paired_crush_off_and_ls2rcvr_not_paired(self):
        """
        Connection to the Pre-paired receiver in Disconnected state while Crush is powered off
        and LS2-Pairing receiver is available but not paired
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered on')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[True, False, True, False, False],
                                 target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0042")
    # end def test_connection_to_pre_paired_rcvr_in_disconnected_state_while_paired_crush_off_and_ls2rcvr_not_paired

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_pre_paired_rcvr_in_disconnected_state_while_paired_crush_and_paired_ls2_rcvr_are_off(self):
        """
        Connection to the Pre-paired receiver in Disconnected state while Crush is powered off
        and LS2-Pairing slot3 filled in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered off')
        LogHelper.log_info(self, 'the device is in Disconnected state')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_reconnection(port_settings=[True, False, False, False, False],
                                 target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0043")
    # end def test_connection_to_pre_paired_rcvr_in_disconnected_state_while_paired_crush_and_paired_ls2_rcvr_are_off

    @features('Ls2ConnectionScheme')
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
        self.testCaseChecked("FNT_LS2_CONNECT_0044")
    # end def test_enter_deep_sleep_mode_in_disconnected_while_pre_paired_off

    @features('Ls2ConnectionScheme')
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
        self.testCaseChecked("FNT_LS2_CONNECT_0045")
    # end def test_enter_deep_sleep_mode_in_disconnected_while_crush_is_already_paired_but_powered_off

    @features('Ls2ConnectionScheme')
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
        self.testCaseChecked("FNT_LS2_CONNECT_0046")
    # end def test_enter_in_deep_sleep_mode_in_disconnected_while_the_ls2_pairing_receiver_is_powered_off

# end class ReconnectionTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
