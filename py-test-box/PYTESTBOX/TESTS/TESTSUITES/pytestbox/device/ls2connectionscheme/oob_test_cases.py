#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.oob_test_cases
:brief: Validate LS2 connection scheme for OOB test cases
:author: Zane Lu
:date: 2020/11/2
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.ls2connectionscheme.uhs_connection_scheme import UhsConnectionSchemeBase
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class OobTestCases(UhsConnectionSchemeBase):
    """
    LS2 connection scheme - OOB Test Cases
    """

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_pairing_business_case_in_oob_state(self):
        """
        Crush pairing business Case in OOB state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered on")
        LogHelper.log_prerequisite(self, "pre-paired receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered off")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_oob(port_settings=[False, True, False, False, False],
                        target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0001")
    # end def test_crush_pairing_business_case_in_oob_state

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_pairing_in_oob_state_when_prepaired_receiver_is_available(self):
        """
        Crush pairing in OOB state when pre-paired receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered on")
        LogHelper.log_prerequisite(self, "pre-paired receiver powered on")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered off")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_oob(port_settings=[True, True, False, False, False],
                        target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0002")
    # end def test_crush_pairing_in_oob_state_when_prepaired_receiver_is_available

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_pairing_in_oob_state_when_pre_paired_and_ls2pairing_receivers_are_available(self):
        """
        Crush pairing in OOB state when pre-paired and LS2-Pairing receivers are available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered on")
        LogHelper.log_prerequisite(self, "pre-paired receiver powered on")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_oob(port_settings=[True, True, True, False, False],
                        target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0003")
    # end def test_crush_pairing_in_oob_state_when_prepaired_and_ls2pairing_receivers_are_available

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_the_pre_paired_receiver_business_case_in_oob_state(self):
        """
        Connection to the Pre-paired receiver Business case in OOB state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered off")
        LogHelper.log_prerequisite(self, "pre-paired receiver powered on")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered off")
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_oob(port_settings=[True, False, False, False, False],
                        target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0004")
    # end def test_connection_to_the_pre_paired_receiver_business_case_in_oob_state

    @features('Ls2ConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_the_pre_paired_receiver_while_an_ls2_pairing_receiver_is_available(self):
        """
        Connection to the Pre-paired receiver while an LS2-Pairing receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered off")
        LogHelper.log_prerequisite(self, "pre-paired receiver powered on")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_oob(port_settings=[True, False, True, False, False],
                        target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0005")
    # end def test_connection_to_the_pre_paired_receiver_while_an_ls2_pairing_receiver_is_available

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pairing_to_a_new_ls2_pairing_receiver_business_in_oob_state(self):
        """
        Pairing to a new LS2-Pairing receiver Business case in OOB state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Crush never paired and powered off")
        LogHelper.log_prerequisite(self, "pre-paired receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_oob(port_settings=[False, False, True, False, False],
                        target_port=PortConfiguration.LS2_RECEIVER_PORT,
                        openlock_mode=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0006")
    # end def test_pairing_to_a_new_ls2_pairing_receiver_business_in_oob_state

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pre_paired_receiver_replacement_business_case_in_oob(self):
        """
        Pre-paired receiver replacement Business case in OOB
        """
        # --------------------------------------------------------------------------------------------------------------
        # noinspection DuplicatedCode
        LogHelper.log_prerequisite(self, "Crush never paired and powered off")
        LogHelper.log_prerequisite(self, "pre-paired receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered off")
        LogHelper.log_prerequisite(self, "another receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_oob(port_settings=[False, False, False, True, False],
                        target_port=PortConfiguration.LS2_RECEIVER2_PORT,
                        openlock_mode=QuadDeviceConnection.ConnectDevices.OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0007")
    # end def test_pre_paired_receiver_replacement_business_case_in_oob

    @features('Ls2ConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_pre_paired_receiver_replacement_in_oob_while_an_ls2_pairing_receiver_is_available(self):
        """
        Pre-paired receiver replacement in OOB while an LS2-Pairing receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        # noinspection DuplicatedCode
        LogHelper.log_prerequisite(self, "Crush never paired and powered off")
        LogHelper.log_prerequisite(self, "pre-paired receiver powered off")
        LogHelper.log_prerequisite(self, "LS2-Pairing slot never paired and receiver powered on")
        LogHelper.log_prerequisite(self, "another receiver powered on")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_oob(port_settings=[False, False, True, True, False],
                        target_port=PortConfiguration.LS2_RECEIVER2_PORT,
                        openlock_mode=QuadDeviceConnection.ConnectDevices.OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0008")
    # end def test_pre_paired_receiver_replacement_in_oob_while_an_ls2_pairing_receiver_is_available

    @features('Ls2ConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_in_deep_sleep_mode_in_oob(self):
        """
        Enter in Deep Sleep mode in OOB
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and receiver powered off')
        # ---------------------------------------------------------------------------
        self.verify_oob_no_receiver_available()

        self.testCaseChecked("FNT_LS2_CONNECT_0009")
    # end def test_enter_in_deep_sleep_mode_in_oob
# end class OObTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
