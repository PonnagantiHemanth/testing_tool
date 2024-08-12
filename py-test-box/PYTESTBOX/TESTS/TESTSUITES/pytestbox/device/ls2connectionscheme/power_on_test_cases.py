#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.power_on_test_cases
:brief: Validate LS2 connection scheme for POWER ON test cases
:author: Zane Lu
:date: 2020/11/2
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
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
class PowerOnTestCases(UhsConnectionSchemeBase):
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
    def test_crush_connection_business_case_in_reset_state(self):
        """
        Crush connection business Case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, True, False, False, False],
                             target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0010")
    # end def test_crush_connection_business_case_in_reset_state

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_connection_in_reset_state_when_pre_paired_receiver_is_available_and_ls2_receiver_off(self):
        """
        Crush connection in Reset state when pre-paired receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, True, False, False, False],
                             target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0011")
    # end def test_crush_connection_in_reset_state_when_pre_paired_receiver_is_available

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_connection_in_reset_state_when_pre_paired_and_ls2_pairing_receivers_are_power_on(self):
        """
        Crush connection in Reset state when pre-paired and LS2-Pairing receivers are powered on
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, True, True, False, False],
                             target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0012")
    # end def test_crush_connection_in_reset_state_when_pre_paired_and_ls2_pairing_receivers_are_power_on

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_connection_in_reset_state_when_pre_paired_receiver_is_available_and_ls2_pairing_slot3_filled_in(
            self):
        """
        Crush connection in Reset state when pre-paired receiver is available and LS2 Pairing Slot3 filled in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired but powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, True, False, False, False],
                             target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0013")
    # end def test_crush_connection_in_reset_state_when_pre_paired_receiver_is_available_and_ls2_pairing_slot3_filled_in

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_pairing_business_case_in_reset_state(self):
        """
        Crush pairing business Case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, True, False, False, False],
                             target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0028")
    # end def test_crush_pairing_business_case_in_reset_state

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_pairing_in_reset_state_when_pre_paired_receiver_is_available(self):
        """
        Crush pairing in Reset state when pre-paired receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, True, False, False, False],
                             target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0078")
    # end def test_crush_pairing_in_reset_state_when_pre_paired_receiver_is_available

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_pairing_in_reset_state_when_pre_paired_and_ls2_pairing_receivers_are_powered_on(self):
        """
        Crush pairing in Reset state when pre-paired and LS2-Pairing receivers are powered on
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, True, True, False, False],
                             target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0079")
    # end def test_crush_pairing_in_reset_state_when_pre_paired_and_ls2_pairing_receivers_are_powered_on

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_crush_pairing_in_reset_state_when_pre_paired_receiver_is_available_and_ls2_pairing_slot3_filled_in(self):
        """
        Crush pairing in Reset state when pre-paired receiver is available and LS2 Pairing Slot3 filled in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered on')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired but powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, True, False, False, False],
                             target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0080")
    # end def test_crush_pairing_in_reset_state_when_pre_paired_receiver_is_available_and_ls2_pairing_slot3_filled_in

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_a_ls2_pairing_receiver_business_in_reset_state(self):
        """
        Connection to a LS2-Pairing receiver Business case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, True, False, False],
                             target_port=PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0014")
    # end def test_connection_to_a_ls2_pairing_receiver_business_in_reset_state

    '''
    Deprecated!!!

    @features('Ls2ConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_a_ls2_pairing_receiver_in_reset_state_while_crush_is_powered_on_but_never_paired(self):
        """
        Connection to a LS2-Pairing receiver in Reset state while Crush is powered on but never paired
        """
        # 19-------------------------------------------------------------------------
        self.logTitle2('Pre - requisite  # 1: Crush never paired and powered on')
        self.logTitle2('Pre - requisite  # 2: pre-paired receiver powered off')
        self.logTitle2('Pre - requisite  # 3: LS2-Pairing receiver paired and receiver powered on')
        # ---------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, self.CRUSH_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.pair_equad_receiver(self, self.LS2_RECEIVER_PORT, connect_devices=7)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [False, True, True, False, False])

        self.power_supply_emulator.turn_off()
        sleep(0.5)

        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, self.LS2_RECEIVER_PORT)
        self.enable_hidpp_reporting()
        self.clean_message_type_in_queue(self.hidDispatcher.receiver_connection_event_queue,
                                         (DeviceConnection, DeviceDisconnection))

        self.power_supply_emulator.turn_on()
        Ls2ConnectionSchemeTestUtils.check_device_connected(self)

        self.testCaseChecked("FNT_LS2_CONNECT_0015")

    # end def test_connection_a_ls2_pairing_receiver_in_reset_state_while_crush_is_powered_on_but_never_paired
    '''

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_a_ls2_pairing_receiver_in_reset_state_while_crush_is_paired_but_powered_off(self):
        """
        Connection to a LS2-Pairing receiver in Reset state while Crush is paired but powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, True, False, False],
                             target_port=PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0016")
    # end def test_connection_to_a_ls2_pairing_receiver_in_reset_state_while_crush_is_paired_but_powered_off

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_a_ls2_pairing_receiver_in_reset_state_when_pre_paired_receiver_is_available(self):
        """
        Connection to a LS2-Pairing receiver in Reset state when pre-paired receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing receiver paired and receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, False, True, False, False],
                             target_port=PortConfiguration.LS2_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0017")
    # end def test_connection_to_a_ls2_pairing_receiver_in_reset_state_when_pre_paired_receiver_is_available

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_connection_to_the_pre_paired_receiver_business_case_in_reset_state(self):
        """
        Connection to the Pre-paired receiver Business case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, False, False, False, False],
                             target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0018")
    # end def test_connection_to_the_pre_paired_receiver_business_case_in_reset_state

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_to_the_pre_paired_receiver_in_reset_state_while_crush_is_powered_off(self):
        """
        Connection to the Pre-paired receiver in Reset state while Crush is powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, False, False, False, False],
                             target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0019")
    # end def test_connection_to_the_pre_paired_receiver_in_reset_state_while_crush_is_powered_off

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_pre_paired_receiver_in_reset_state_while_crush_off_and_ls2_pairing_receiver_on(
            self):
        """
        Connection to the Pre-paired receiver in Reset state while Crush is powered off and LS2-Pairing receiver is
        powered on
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, False, True, False, False],
                             target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0020")
    # end def test_connection_pre_paired_receiver_in_reset_state_while_crush_off_and_ls2_pairing_receiver_on

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_connection_pre_paired_receiver_in_reset_state_while_crush_off_and_ls2_pairing_slot3_filled_in(
            self):
        """
        Connection to the Pre-paired receiver in Reset state while Crush is powered off and LS2-Pairing slot3 filled
        in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered on')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[True, False, False, False, False],
                             target_port=PortConfiguration.PRE_PAIRED_RECEIVER_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0021")
    # end def test_connection_pre_paired_receiver_in_reset_state_while_crush_off_and_ls2_pairing_slot3_filled_in

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pairing_to_a_new_ls2_pairing_receiver_business_case_in_reset_state(self):
        """
        Pairing to a new LS2-Pairing receiver Business case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, True, False, False],
                             target_port=PortConfiguration.LS2_RECEIVER_PORT,
                             openlock_mode=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0022")
    # end def test_pairing_to_a_new_ls2_pairing_receiver_business_case_in_reset_state

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_pairing_to_a_new_ls2_pairing_receiver_in_reset_state_while_crush_is_already_paired_but_powered_off(self):
        """
        Pairing to a new LS2-Pairing receiver in Reset state while Crush is already paired but powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, True, False, False],
                             target_port=PortConfiguration.LS2_RECEIVER_PORT,
                             openlock_mode=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0023")
    # end def test_pairing_to_a_new_ls2_pairing_receiver_in_reset_state_while_crush_is_already_paired_but_powered_off

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_ls2_pairing_receiver_replacement_use_case_in_reset(self):
        """
        LS2-Pairing receiver replacement use case in Reset while
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot paired and receiver powered off')
        LogHelper.log_info(self, 'another LS2-2Devices receiver power on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        self.pair_ls2_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, False, True, False],
                             target_port=PortConfiguration.LS2_RECEIVER2_PORT,
                             openlock_mode=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0024")
    # end def test_ls2_pairing_receiver_replacement_use_case_in_reset

    @features('Ls2ConnectionScheme')
    @level('Business')
    @services('PowerSupply')
    def test_pre_paired_receiver_replacement_business_case_in_reset(self):
        """
        Pre-paired receiver replacement Business case in Reset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        LogHelper.log_info(self, 'another receiver power on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, False, True, False],
                             target_port=PortConfiguration.LS2_RECEIVER2_PORT,
                             openlock_mode=QuadDeviceConnection.ConnectDevices.OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0025")
    # end def test_pre_paired_receiver_replacement_business_case_in_reset

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_pairing_to_a_new_pre_paired_receiver_in_reset_while_crush_is_already_paired_but_powered_off(self):
        """
        Pairing to a new pre-paired receiver in Reset while Crush is already paired but powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired but powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and receiver powered off')
        LogHelper.log_prerequisite(self, 'another receiver power on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, False, True, False],
                             target_port=PortConfiguration.LS2_RECEIVER2_PORT,
                             openlock_mode=QuadDeviceConnection.ConnectDevices.OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0026")
    # end def test_pairing_to_a_new_pre_paired_receiver_in_reset_while_crush_is_already_paired_but_powered_off

    @features('Ls2ConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_pairing_to_a_new_pre_paired_receiver_in_reset_while_the_ls2_pairing_receiver_is_powered_off(self):
        """
        Pairing to a new pre-paired receiver in Reset while the LS2-Pairing receiver is powered off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush never paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot paired and receiver powered off')
        LogHelper.log_prerequisite(self, 'another receiver power on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_ls2_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, False, True, False],
                             target_port=PortConfiguration.LS2_RECEIVER2_PORT,
                             openlock_mode=QuadDeviceConnection.ConnectDevices.OPEN_LOCK)

        self.testCaseChecked("FNT_LS2_CONNECT_0027")
    # end def test_pairing_to_a_new_pre_paired_receiver_in_reset_while_the_ls2_pairing_receiver_is_powered_off

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    def test_crush_replacement_use_case_in_reset_state(self):
        """
        Crush replacement Use Case in Reset state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and another Crush powered on')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER2_PORT)

        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_power_on(port_settings=[False, False, False, False, True],
                             target_port=PortConfiguration.CRUSH_RECEIVER2_PORT)

        self.testCaseChecked("FNT_LS2_CONNECT_0029")
    # end def test_crush_replacement_use_case_in_reset_state

    @features('Ls2ConnectionScheme')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_in_deep_sleep_mode_in_reset_while_pre_paired_off(self):
        """
        Enter in Deep Sleep mode in Reset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Crush never paired and powered off')
        LogHelper.log_info(self, 'pre-paired receiver powered off')
        LogHelper.log_info(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.verify_power_on_no_receiver_available()

        self.testCaseChecked("FNT_LS2_CONNECT_0030")

    # end def test_enter_in_deep_sleep_mode_in_reset_while_pre_paired_off

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @level('Functionality')
    @services('PowerSupply')
    def test_enter_in_deep_sleep_mode_in_reset_while_crush_is_already_paired_but_power_off(self):
        """
        Enter in Deep Sleep mode in Reset while Crush is already paired but power Off
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered off')
        LogHelper.log_prerequisite(self, 'pre-paired receiver powered off')
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired and receiver powered off')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        self.verify_power_on_no_receiver_available()

        self.testCaseChecked("FNT_LS2_CONNECT_0031")

    # end def test_enter_in_deep_sleep_mode_in_reset_while_crush_is_already_paired_but_power_off

    @features('Ls2ConnectionScheme')
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

        self.testCaseChecked("FNT_LS2_CONNECT_0032")

    # end def test_enter_in_deep_sleep_mode_in_reset_while_the_ls2_pairing_receiver_is_powered_off

# end class PowerOnTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
