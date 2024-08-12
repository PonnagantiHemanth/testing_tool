#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_40a3.functionality
:brief: HID++ 2.0 ``FnInversionForMultiHostDevices`` functionality test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/9/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevices
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.keyboard.feature_40a3.fninversionformultihostdevices \
    import FnInversionForMultiHostDevicesTestCase
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.equaddeviceconnectionutils import EQuadDeviceConnectionUtils
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------

_AUTHOR = "Masan Xu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FnInversionForMultiHostDevicesFunctionalityTestCase(FnInversionForMultiHostDevicesTestCase):
    """
    Validate ``FnInversionForMultiHostDevices`` functionality test cases
    """

    @features("Feature40A3")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_fn_inversion_state_toggle_by_key_combination(self):
        """
        Verify fnInversionState from getGlobalFnInversion after turning ON/OFF FnInversion by key combination
        """
        self.post_requisite_reload_nvs = True

        if self.f.PRODUCT.F_IsGaming is False:
            DevicePairingTestUtils.pair_all_hosts_to_receivers(self)
            self.set_fn_inversion_state_for_all_host(FnInversionForMultiHostDevices.FnInversionState.OFF)
        else:
            self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                        fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for host_idx in range(self.nb_host):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform FnLockKeyCombination")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=self.f.PRODUCT.F_IsGaming)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform FnLockKeyCombination")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=self.f.PRODUCT.F_IsGaming)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                self.check_fn_inversion_state(host_idx2, FnInversionForMultiHostDevices.FnInversionState.OFF)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            if self.nb_host > 1:
                # Switch to the next host for loop
                self.switch_to_another_host((host_idx + 1) % self.nb_host)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_40A3_0001", _AUTHOR)
    # end def test_fn_inversion_state_toggle_by_key_combination

    @features("Feature40A3")
    @level("Functionality")
    @bugtracker("Default_Fn_Inversion_State")
    def test_fn_inversion_state_toggle_by_40a3(self):
        """
        Verify fnInversionState from getGlobalFnInversion after turning ON/OFF FnInversion by SW
        """
        if self.f.PRODUCT.F_IsGaming is False:
            DevicePairingTestUtils.pair_all_hosts_to_receivers(self)
            self.set_fn_inversion_state_for_all_host(FnInversionForMultiHostDevices.FnInversionState.OFF)
        else:
            self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                        fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for host_idx in range(self.nb_host):
            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.OFF)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                self.check_fn_inversion_state(host_idx2, FnInversionForMultiHostDevices.FnInversionState.OFF)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            if self.nb_host > 1:
                # Switch to the next host for loop
                self.switch_to_another_host((host_idx + 1) % self.nb_host)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_40A3_0002", _AUTHOR)
    # end def test_fn_inversion_state_toggle_by_40a3

    @features("Feature40A3")
    @level("Functionality")
    @bugtracker("Default_Fn_Inversion_State")
    def test_fn_inversion_state_after_power_cycle(self):
        """
        Verify that fnInversionState is stored for each host separately to withstand a power off event
        """
        if self.f.PRODUCT.F_IsGaming is False:
            DevicePairingTestUtils.pair_all_hosts_to_receivers(self)
            self.set_fn_inversion_state_for_all_host(FnInversionForMultiHostDevices.FnInversionState.OFF)
        else:
            self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                        fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for host_idx in range(self.nb_host):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power off/on the device")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            self.check_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.OFF)
            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power off/on the device")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.OFF)
            if self.nb_host > 1:
                # Switch to the next host for loop
                self.switch_to_another_host((host_idx + 1) % self.nb_host)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_40A3_0003", _AUTHOR)
    # end def test_fn_inversion_state_after_power_cycle

    @features("Feature40A3")
    @features('Feature1814')
    @level("Functionality")
    @bugtracker("Default_Fn_Inversion_State")
    def test_fn_inversion_state_change_host_by_1814(self):
        """
        Verify that fnInversionState is stored for each host separately to withstand a change of host from SW
        """
        if self.f.PRODUCT.F_IsGaming is False:
            DevicePairingTestUtils.pair_all_hosts_to_receivers(self)
            self.set_fn_inversion_state_for_all_host(FnInversionForMultiHostDevices.FnInversionState.OFF)
        else:
            self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                        fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for host_idx in range(self.nb_host):
            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Change to the next host index {(host_idx + 1) % self.nb_host} "
                                     "by 0x1814.setCurrentHost")
            # ----------------------------------------------------------------------------------------------------------
            self.switch_to_another_host((host_idx + 1) % self.nb_host)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Back to the host index {host_idx} by 0x1814.setCurrentHost")
            # ----------------------------------------------------------------------------------------------------------
            self.switch_to_another_host(host_idx)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.OFF)
            if self.nb_host > 1:
                # Switch to the next host for loop
                self.switch_to_another_host((host_idx + 1) % self.nb_host)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_40A3_0004", _AUTHOR)
    # end def test_fn_inversion_state_change_host_by_1814

    @features("Feature40A3")
    @features('MultipleEasySwitchButtons')
    @level("Functionality")
    def test_fn_inversion_state_change_host_by_easy_switch(self):
        """
        Verify that fnInversionState is stored for each host separately to withstand a change of host by easy switch
        button
        """
        if self.f.PRODUCT.F_IsGaming is False:
            DevicePairingTestUtils.pair_all_hosts_to_receivers(self)
            self.set_fn_inversion_state_for_all_host(FnInversionForMultiHostDevices.FnInversionState.OFF)
        else:
            self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                        fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for host_idx in range(self.nb_host):
            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Change to the next host index {(host_idx + 1) % self.nb_host} "
                                     "by keystroke easy switch")
            # ----------------------------------------------------------------------------------------------------------
            self.switch_to_another_host((host_idx + 1) % self.nb_host, self.ChangeHostType.EASY_SWITCH)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            self.set_fn_inversion_state((host_idx + 1) % self.nb_host,
                                        FnInversionForMultiHostDevices.FnInversionState.ON)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Back to the host index {host_idx} by keystroke easy switch")
            # ----------------------------------------------------------------------------------------------------------
            self.switch_to_another_host(host_idx, self.ChangeHostType.EASY_SWITCH)

            self.check_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.ON)

            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.OFF)
            self.set_fn_inversion_state((host_idx + 1) % self.nb_host,
                                        FnInversionForMultiHostDevices.FnInversionState.OFF)
            if self.nb_host > 1:
                # Switch to the next host for loop
                self.switch_to_another_host((host_idx + 1) % self.nb_host)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_40A3_0005", _AUTHOR)
    # end def test_fn_inversion_state_change_host_by_easy_switch

    @features("Feature40A3")
    @features('Feature1830powerMode', 3)
    @level("Functionality")
    @bugtracker("Default_Fn_Inversion_State")
    def test_fn_inversion_state_after_deep_sleep(self):
        """
        Verify that the current host fnInversionState can be restored at wake-up from deep sleep
        """
        if self.f.PRODUCT.F_IsGaming is False:
            DevicePairingTestUtils.pair_all_hosts_to_receivers(self)
            self.set_fn_inversion_state_for_all_host(FnInversionForMultiHostDevices.FnInversionState.OFF)
        else:
            self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                        fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for host_idx in range(self.nb_host):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set DUT into deep-sleep mode by 0x1830.SetPowerMode")
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wake up DUT via keystroke enter key")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                self.check_fn_inversion_state(host_idx2, FnInversionForMultiHostDevices.FnInversionState.OFF)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set DUT into deep-sleep mode by 0x1830.SetPowerMode")
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wake up DUT via keystroke enter key")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            self.check_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.ON)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
            # ----------------------------------------------------------------------------------------------------------
            for host_idx2 in range(self.nb_host):
                expected_state = FnInversionForMultiHostDevices.FnInversionState.ON if host_idx2 == host_idx \
                    else FnInversionForMultiHostDevices.FnInversionState.OFF
                self.check_fn_inversion_state(host_idx2, expected_state)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------

            self.set_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.OFF)
            if self.nb_host > 1:
                # Switch to the next host for loop
                self.switch_to_another_host((host_idx + 1) % self.nb_host)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_40A3_0006", _AUTHOR)
    # end def test_fn_inversion_state_after_deep_sleep

    @features("Feature40A3")
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    @bugtracker("Pollux_Fn_Lock_Reversed")
    def test_f_lock_change_event_after_key_combination(self):
        """
        Verify that the device notifies the SW with a FN-Lock status at each FnLockKeyCombination pressed
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform FnLockKeyCombination")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=self.f.PRODUCT.F_IsGaming)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Check the fnInversionState == {FnInversionForMultiHostDevices.FnInversionState.OFF}(PWS) "
                            f"or == {FnInversionForMultiHostDevices.FnInversionState.ON}(Gaming) from fLockChange event"
                            )
        # --------------------------------------------------------------------------------------------------------------
        self.check_f_lock_change_event(FnInversionForMultiHostDevices.FnInversionState.ON if self.f.PRODUCT.F_IsGaming
                                       else FnInversionForMultiHostDevices.FnInversionState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform FnLockKeyCombination")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=self.f.PRODUCT.F_IsGaming)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            f"Check the fnInversionState == {FnInversionForMultiHostDevices.FnInversionState.ON}(PWS) "
                            f"or == {FnInversionForMultiHostDevices.FnInversionState.OFF}(Gaming) from fLockChange "
                            "event")
        # --------------------------------------------------------------------------------------------------------------
        self.check_f_lock_change_event(FnInversionForMultiHostDevices.FnInversionState.OFF if self.f.PRODUCT.F_IsGaming
                                       else FnInversionForMultiHostDevices.FnInversionState.ON)

        self.testCaseChecked("FUN_40A3_0007", _AUTHOR)
    # end def test_f_lock_change_event_after_key_combination

    @features("Feature40A3")
    @features('NoGamingDevice')
    @level("Functionality")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_non_gaming_fn_inversion_state_reset_by_pairing(self):
        """
        The device shall reset the current host fnInversionState when paired to a new host.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set fnInversionState == {FnInversionForMultiHostDevices.FnInversionState.OFF} "
                                 "for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Re-pair the device for HOST1 again")
        # --------------------------------------------------------------------------------------------------------------
        self._ble_pro_pairing_with_fn_lock()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the fnInversionState == {FnInversionForMultiHostDevices.FnInversionState.ON} "
                                  "for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        get_global_fn_inversion_resp = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.get_global_fn_inversion(
            self, host_index=FnInversionForMultiHostDevices.HostIndex.HOST1)

        # FnInversionState should be restored to FnInversionDefaultState
        checker = FnInversionForMultiHostDevicesTestUtils.GetGlobalFnInversionResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['host_index'] = (checker.check_host_index, FnInversionForMultiHostDevices.HostIndex.HOST1)
        checker.check_fields(self, get_global_fn_inversion_resp, self.feature_40a3.get_global_fn_inversion_response_cls,
                             check_map)

        self.keystroke_f_row_and_check_report(press_fn=False, expected_report_type=self.ReportType.SHORTCUT_KEY)
        self.testCaseChecked("FUN_40A3_0008#1", _AUTHOR)
    # end def test_non_gaming_fn_inversion_state_reset_by_pairing

    @features("Feature40A3")
    @features('GamingDevice')
    @level("Functionality")
    def test_gaming_fn_inversion_state_reset_by_pairing(self):
        """
        The device shall reset the current host fnInversionState when paired to a new host.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get device unit id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        self.unit_id = DeviceInformationTestUtils.HIDppHelper.get_device_info(test_case=self).unit_id

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set fnInversionState == {FnInversionForMultiHostDevices.FnInversionState.ON} "
                                 "for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        self.post_requisite_new_equad_connection = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Re-pair the device")
        # --------------------------------------------------------------------------------------------------------------
        EQuadDeviceConnectionUtils.new_device_connection_and_pre_pairing(
            test_case=self, unit_ids=[self.unit_id], disconnect=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the fnInversionState == {FnInversionForMultiHostDevices.FnInversionState.OFF}"
                                  " for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        get_global_fn_inversion_resp = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.get_global_fn_inversion(
            self, host_index=FnInversionForMultiHostDevices.HostIndex.HOST1)

        # FnInversionState should be restored to FnInversionDefaultState
        checker = FnInversionForMultiHostDevicesTestUtils.GetGlobalFnInversionResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map['host_index'] = (checker.check_host_index, FnInversionForMultiHostDevices.HostIndex.HOST1)
        checker.check_fields(self, get_global_fn_inversion_resp, self.feature_40a3.get_global_fn_inversion_response_cls,
                             check_map)

        self.keystroke_f_row_and_check_report(press_fn=False, expected_report_type=self.ReportType.F_KEY)
        self.testCaseChecked("FUN_40A3_0008#2", _AUTHOR)
    # end def test_gaming_fn_inversion_state_reset_by_pairing

    def _ble_pro_pairing_with_fn_lock(self):
        """
        Redo the pairing on the default channel (BLE_PRO, HOST1) when the FnInversionState is OFF (i.e Fn Lock is ON)
        meaning the user shall press Fn + F-keys to access the shortcuts keys
        cf https://spaces.logitech.com/display/sysarch/19.+FN-Lock
        """
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
        self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
            test_case=self, memory_manager=self.device_memory_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Force device in discoverable mode with Fn + Host1')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.FN_KEY)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)
        self.button_stimuli_emulator.enter_pairing_mode(HOST.CH1)
        self.button_stimuli_emulator.key_release(KEY_ID.FN_KEY)
        sleep(ButtonStimuliInterface.DEFAULT_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Start the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Stop the discovery sequence')
        # --------------------------------------------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Restart the pairing sequence')
        # --------------------------------------------------------------------------------------------------------------
        self.pairing_slot = DevicePairingTestUtils.pair_device(self, bluetooth_address)
        self.post_requisite_clean_pairing_info_on_receivers = True
        self.current_channel = DeviceManagerUtils.get_channel(test_case=self, channel_id=ChannelIdentifier(
            port_index=ChannelUtils.get_port_index(test_case=self), device_index=self.pairing_slot))
        ChannelUtils.open_channel(test_case=self)
        ChannelUtils.empty_queues(self)
    # end def _ble_pro_pairing_with_fn_lock

# end class FnInversionForMultiHostDevicesFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
