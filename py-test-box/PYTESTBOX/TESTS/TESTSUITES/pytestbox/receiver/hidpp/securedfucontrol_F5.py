#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.hidpp.securedfucontrol_F5
    :brief: Validates HID++ 1.0 DFU control 0xF5 register
    :author: Stanislas Cottard
    :date: 2020/10/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.shared.hidpp.securedfucontrol import CommonSecureDfuControlTestCase
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverSecureDfuControlTestCase(CommonSecureDfuControlTestCase, ReceiverBaseTestCase):
    """
    Validates Secure DFU Control TestCases for the receiver (feature 0xF5)
    """
    
    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_get_dfu_control_no_dfu_chunk_api(self):
        """
        getDfuControl API validation when no DFU chunk in NVS
        """
        self.generic_get_dfu_control_no_dfu_chunk_api()
        
        self.testCaseChecked("FNT_RCV-F5_0001")
    # end def test_get_dfu_control_no_dfu_chunk_api

    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_get_dfu_control_dfu_enabled_in_nvs_api(self):
        """
        getDfuControl API validation when DFU enabled in NVS

        [0] getDfuControl() -> enableDfu, dfuControlParam, dfuControlTimeout, dfuControlActionType, dfuControlActionData
        """
        self.generic_get_dfu_control_dfu_enabled_in_nvs_api()

        self.testCaseChecked("FNT_RCV-F5_0002")
    # end def test_get_dfu_control_dfu_enabled_in_nvs_api

    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_get_dfu_control_dfu_disabled_in_nvs_api(self):
        """
        getDfuControl API validation when DFU disabled in NVS

        [0] getDfuControl() -> enableDfu, dfuControlParam, dfuControlTimeout, dfuControlActionType, dfuControlActionData
        """
        self.generic_get_dfu_control_dfu_disabled_in_nvs_api()

        self.testCaseChecked("FNT_RCV-F5_0003")
    # end def test_get_dfu_control_dfu_disabled_in_nvs_api

    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_set_dfu_control_enable_dfu_api(self):
        """
        setDfuControl API validation with DFU enable when no DFU chunk in NVS

        [1] setDfuControl(enableDfu, dfuControlParam, dfuMagicKey)
        """
        self.generic_set_dfu_control_enable_dfu_api()

        self.testCaseChecked("FNT_RCV-F5_0004")
    # end def test_set_dfu_control_enable_dfu_api

    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_set_dfu_control_disable_dfu_api(self):
        """
        setDfuControl API validation with DFU disable when no DFU chunk in NVS

        [1] setDfuControl(enableDfu, dfuControlParam, dfuMagicKey)
        """
        self.generic_set_dfu_control_disable_dfu_api()

        self.testCaseChecked("FNT_RCV-F5_0005")
    # end def test_set_dfu_control_disable_dfu_api

    @features('SecureDfuControlAllActionTypes')
    @level('Business')
    @services('Debugger')
    def test_dfu_control_business(self):
        """
        DFU Control business case when enable DFU mode is requested. Check receiver is in bootloader mode after a reset
        is performed with the requested user actions. Check 0xD0 feature is advertised in bootloader mode. Check DFU
        status LED starts blinking when entering bootloader mode and stops immediately when it leaves this mode.
        """
        self.generic_dfu_control_business()

        self.testCaseChecked("FNT_RCV-F5_0006")
    # end def test_dfu_control_business

    @features('SecureDfuControlActionTypeNot0')
    @level('Functionality')
    @services('Debugger')
    def test_perform_action_when_dfu_disabled(self):
        """
        DFU Control use case when enable DFU mode is NOT requested. Check receiver stays in application mode after a
        reset is performed with the requested user actions.
        """
        self.generic_perform_action_when_dfu_disabled()

        self.testCaseChecked("FNT_RCV-F5_0007")
    # end def test_perform_action_when_dfu_disabled

    @features('SecureDfuControlActionTypeNot0')
    @level('Functionality')
    @services('Debugger')
    def test_perform_action_when_dfu_enabled_then_disabled(self):
        """
        Cancel a previous enable DFU request. Check receiver stays in application mode after a reset is performed with
        the requested user actions.
        """
        self.generic_perform_action_when_dfu_enabled_then_disabled()

        self.testCaseChecked("FNT_RCV-F5_0008")
    # end def test_perform_action_when_dfu_enabled_then_disabled

    @features('SecureDfuControlActionTypeNot0')
    @level('Time-consuming')
    @services('Debugger')
    def test_perform_action_when_just_before_timeout(self):
        """
        DFU Control Timeout: Enable DFU mode is requested and reset is performed just before the end of the DFU control
        timeout. Check receiver is in bootloader mode after a reset is performed with the requested user actions.
        """
        self.generic_perform_action_when_just_before_timeout()

        self.testCaseChecked("FNT_RCV-F5_0009")
    # end def test_perform_action_when_just_before_timeout

    @features('SecureDfuControlActionTypeNot0')
    @level('Time-consuming')
    @services('Debugger')
    def test_perform_action_when_just_after_timeout(self):
        """
        DFU Control Timeout: Enable DFU mode is requested and reset is performed just after the DFU control timeout.
        Check device stays in application mode after the reset is performed with the requested user actions.
        """
        self.generic_perform_action_when_just_after_timeout()

        self.testCaseChecked("FNT_RCV-F5_0010")
    # end def test_perform_action_when_just_after_timeout

    @features('SecureDfuControlActionTypeNot0')
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_perform_action_when_just_before_timeout_after_restarting_it(self):
        """
        DFU Control Timeout restart: Send multiple enable DFU mode requests and validate the DFU control timeout
        restarts each time from zero. Check receiver is in bootloader mode after the reset performed with the requested
        user actions.
        """
        self.generic_perform_action_when_just_before_timeout_after_restarting_it()

        self.testCaseChecked("FNT_RCV-F5_0011")
    # end def test_perform_action_when_just_before_timeout_after_restarting_it

    @features('SecureDfuControlActionTypeNot0')
    @level('ReleaseCandidate')
    @services('Debugger')
    def test_perform_action_when_just_after_timeout_after_restarting_it(self):
        """
        DFU Control Timeout restart: Send multiple enable Dfu mode requests and validate the timeout notification is
        returned after the correct delay following the last request
        """
        self.generic_perform_action_when_just_after_timeout_after_restarting_it()

        self.testCaseChecked("FNT_RCV-F5_0012")
    # end def test_perform_action_when_just_after_timeout_after_restarting_it

    @features('SecureDfuControlActionTypeNot0')
    @level('Time-consuming')
    @services('Debugger')
    def test_get_dfu_control_do_not_influence_timeout(self):
        """
        DFU Control Timeout: Send multiple getDfuControl requests and validate the DFU control timeout does NOT restart
        each time from zero. Check device stays in application mode after the reset performed with the requested user
        actions.
        """
        self.generic_get_dfu_control_do_not_influence_timeout()

        self.testCaseChecked("FNT_RCV-F5_0013")
    # end def test_get_dfu_control_do_not_influence_timeout

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_soft_reset_do_not_jump_on_bootloader(self):
        """
        DFU Control reset type. Check receiver stays in application mode after a Soft reset is performed with the
        requested user actions. Check the DFU enable NVS state is not modified by a soft reset.
        """
        self.generic_soft_reset_do_not_jump_on_bootloader()

        self.testCaseChecked("FNT_RCV-F5_0014")
    # end def test_soft_reset_do_not_jump_on_bootloader

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_dfu_disabled_to_enabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not matches the
        request:
        - setDfuControl with DFU enabled when DFU disabled in NVS
        """
        self.generic_nvs_chunk_dfu_disabled_to_enabled()

        self.testCaseChecked("FNT_RCV-F5_0015")
    # end def test_nvs_chunk_dfu_disabled_to_enabled

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_dfu_enabled_to_disabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not matches the
        request:
        - setDfuControl with DFU disabled when DFU enabled in NVS
        """
        self.generic_nvs_chunk_dfu_enabled_to_disabled()

        self.testCaseChecked("FNT_RCV-F5_0016")
    # end def test_nvs_chunk_dfu_enabled_to_disabled

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_dfu_enabled_to_enable(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not matches the
        request:
        - setDfuControl with DFU enabled when DFU already enabled in NVS
        """
        self.generic_nvs_chunk_dfu_enabled_to_enable()

        self.testCaseChecked("FNT_RCV-F5_0017")
    # end def test_nvs_chunk_dfu_enabled_to_enable

    @features('SecureDfuControlUseNVS')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_dfu_disabled_to_disabled(self):
        """
        DFU Control NVS Chunk handling: Check a chunk is added when the saved enable DFU mode does not matches the
        request:
        - setDfuControl with DFU disabled when DFU already disabled in NVS
        """
        self.generic_nvs_chunk_dfu_disabled_to_disabled()

        self.testCaseChecked("FNT_RCV-F5_0018")
    # end def test_nvs_chunk_dfu_disabled_to_disabled

    @features('SecureDfuControlUseNVS')
    @level('Security')
    @services('Debugger')
    def test_get_dfu_control_enable_in_nvs_superior_to_1(self):
        """
        getDfuControl when enable byte value greater than 1 in NVS but with enable bit to 1 should return enable = 1
        and all reserved bit to 0
        """
        self.generic_get_dfu_control_enable_in_nvs_superior_to_1()

        self.testCaseChecked("ROT_RCV-F5_0001")
    # end def test_get_dfu_control_enable_in_nvs_superior_to_1

    @features('SecureDfuControlUseNVS')
    @level('Security')
    @services('Debugger')
    def test_entering_dfu_enable_in_nvs_superior_to_1(self):
        """
        getDfuControl when enable byte value greater than 1 in NVS but with enable bit to 1. Check receiver is in
        bootloader mode after the reset performed with the requested user actions
        """
        self.generic_entering_dfu_enable_in_nvs_superior_to_1()

        self.testCaseChecked("ROT_RCV-F5_0002")
    # end def test_entering_dfu_enable_in_nvs_superior_to_1

    @features('SecureDfuControlUseNVS')
    @level('Robustness')
    @services('Debugger')
    def test_entering_dfu_param_in_nvs_superior_to_0(self):
        """
        getDfuControl when param value different than 0 in NVS. Check receiver is in bootloader mode after the reset
        performed with the requested user actions
        """
        self.generic_entering_dfu_param_in_nvs_superior_to_0()

        self.testCaseChecked("ROT_RCV-F5_0003")
    # end def test_entering_dfu_param_in_nvs_superior_to_0

    @features('SecureDfuControlUseNVS')
    @level('Robustness')
    @services('Debugger')
    def test_set_dfu_control_reserved_enable_ignored(self):
        """
        setDfuControl processing shall ignore bits which are reserved for future use in the first enableDfu byte
        """
        self.generic_set_dfu_control_reserved_enable_ignored()

        self.testCaseChecked("ROT_RCV-F5_0004")
    # end def test_set_dfu_control_reserved_enable_ignored

    @features('SecureDfuControlActionTypeNot0')
    @level('Robustness')
    @services('Debugger')
    def test_set_dfu_control_reserved_ignored(self):
        """
        setDfuControl processing shall ignore bytes which are reserved for future use
        """
        self.generic_set_dfu_control_reserved_ignored()

        self.testCaseChecked("ROT_RCV-F5_0005")
    # end def test_set_dfu_control_reserved_ignored

    @features('SecureDfuControlActionTypeNot0')
    @level('ErrorHandling')
    @services('Debugger')
    def test_set_dfu_control_wrong_magic_key(self):
        """
        setDfuControl processing shall enforce the magic key value - Every bit flipped combination shall be verify
        """
        self.generic_set_dfu_control_wrong_magic_key()

        self.testCaseChecked("ROT_RCV-F5_0006")
    # end def test_set_dfu_control_wrong_magic_key

    @features('SecureDfuControlActionTypeNot0')
    @level('Robustness')
    @services('Debugger')
    def test_get_dfu_control_padding_ignored(self):
        """
        Validates getDfuControl padding bytes are ignored
        """
        self.generic_get_dfu_control_padding_ignored()

        self.testCaseChecked("ROT_RCV-F5_007")
    # end def test_get_dfu_control_padding_ignored

    @features('SecureDfuControlActionTypeNot0')
    @level('Robustness')
    @services('Debugger')
    def test_set_dfu_control_padding_ignored(self):
        """
        Validates setDfuControl padding bytes are ignored
        """
        self.generic_set_dfu_control_padding_ignored()

        self.testCaseChecked("ROT_RCV-F5_008")
    # end def test_set_dfu_control_padding_ignored
# end class ReceiverSecureDfuControlTestCase


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
