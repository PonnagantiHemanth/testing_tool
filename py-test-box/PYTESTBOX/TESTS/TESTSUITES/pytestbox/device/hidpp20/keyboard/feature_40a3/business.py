#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_40a3.business
:brief: HID++ 2.0 ``FnInversionForMultiHostDevices`` business test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/9/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import time
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagement
from pyhid.hidpp.features.common.lightspeedprepairing import SetLTK
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtons
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsFactory
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevices
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import CONNECTIVITY_STATUS_LEDS
from pylibrary.emulator.ledid import LED_ID
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.mcu.profileformat import ProfileFieldName
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.cidutils import CidEmulation
from pytestbox.base.cidutils import CidInfoFlags
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.lightspeedprepairingutils import LightspeedPrepairingTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.keyboard.feature_40a3.fninversionformultihostdevices \
    import FnInversionForMultiHostDevicesTestCase
from pytestbox.shared.base.bleprosafeprepairedreceiverutils import BleProSafePrePairedReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.specialkeysmsebuttonsutils import SpecialKeysMseButtonsTestUtils
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FnInversionForMultiHostDevicesBusinessTestCase(FnInversionForMultiHostDevicesTestCase):
    """
    Validate ``FnInversionForMultiHostDevices`` business test cases
    """

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL, 1)
    @level('Business', 'SmokeTests')
    @bugtracker("Pollux_Fn_Lock_Reversed")
    def test_shortcut_keys(self):
        """
        [PWS]

        Verify that the device reports the Shortcut key for each Fx key pressed in state {FnInversion ON, Keys
        non-diverted}
        """
        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        self.keystroke_f_row_and_check_report(press_fn=False, expected_report_type=self.ReportType.SHORTCUT_KEY)

        self.testCaseChecked("BUS_40A3_0001", _AUTHOR)
    # end def test_shortcut_keys

    def _set_cid_reporting_diverted_and_verify_diverted_button_event(self, press_fn=False):
        """
        Set diverted flag to True for all F-Row keys, keystroke the F-Row keys and verify if divertedButtonsEvent is
        received

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param press_fn: Press Fn key or not
        :type press_fn: ``bool``
        """
        self.special_keys_and_mouse_buttons_feature = SpecialKeysMSEButtonsFactory.create(
            self.config_manager.get_feature_version(
                self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS))
        feature_1b04_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=SpecialKeysMSEButtons.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        feature_1b04_index)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                self, f'Send getCidInfo with index = {index} to get CID value')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=feature_1b04_index,
                ctrl_id_index=index)

            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.special_keys_and_mouse_buttons_feature.get_cid_info_response_cls)

            # Ignore Host Switch buttons
            if Numeral(get_cid_info_response.ctrl_id) in [CidTable.HOST_SWITCH_1, CidTable.HOST_SWITCH_2,
                                                          CidTable.HOST_SWITCH_3]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self,
                                   f"Skip CID index = {index} because it's host-switch button")
                # ------------------------------------------------------------------------------------------------------
                continue
            # Skip the CIDs which are not in the F-ROW
            elif Numeral(get_cid_info_response.fkey_pos) == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'Skip CID index = {index} because its position is not in F-Row')
                # ------------------------------------------------------------------------------------------------------
                continue
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Verify it has divert capability')
                # ------------------------------------------------------------------------------------------------------
                self.assertTrue(expr=get_cid_info_response.divert == 1,
                                msg="CID located in the F-Row shall expose the 'divert' capability")
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and '
                                     'set divert = 1, dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=feature_1b04_index,
                ctrl_id=get_cid_info_response.ctrl_id,
                divert_valid=True,
                divert=True)

            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_RRD,
                press_fn=press_fn)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_diverted_and_verify_diverted_button_event

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL, 1)
    @level("Business")
    @bugtracker("Pollux_Fn_Lock_Reversed")
    def test_cid_keys(self):
        """
        [PWS]
        Verify that the device reports the CID key code for each Fx key pressed in state {FnInversion ON, Keys
        diverted}
        """
        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        self._set_cid_reporting_diverted_and_verify_diverted_button_event(press_fn=False)

        self.testCaseChecked("BUS_40A3_0002", _AUTHOR)
    # end def test_cid_keys

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL, 1)
    @level("Business")
    @bugtracker("Pollux_Fn_Lock_Reversed")
    def test_f_keys(self):
        """
        [PWS]

        Verify that the device reports the F key for each Fx key pressed in state {FnInversion OFF}
        """
        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        self.keystroke_f_row_and_check_report(press_fn=False, expected_report_type=self.ReportType.F_KEY)

        self.testCaseChecked("BUS_40A3_0003", _AUTHOR)
    # end def test_f_keys

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL, 1)
    @level("Business")
    @bugtracker("Pollux_Fn_Lock_Reversed")
    def test_f_keys_with_fn_key(self):
        """
        [PWS]
        Verify that the device reports the F key for each Fn + Fx key pressed in state {FnInversion ON}
        """
        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        self.keystroke_f_row_and_check_report(press_fn=True, expected_report_type=self.ReportType.F_KEY)

        self.testCaseChecked("BUS_40A3_0004", _AUTHOR)
    # end def test_f_keys_with_fn_key

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL, 1)
    @level("Business")
    @bugtracker("Pollux_Fn_Lock_Reversed")
    def test_shortcut_keys_with_fn_key(self):
        """
        [PWS]
        Verify that the device reports the Shortcut key for each Fn + Fx key pressed in state {FnInversion OFF, Keys
        non-diverted}
        """
        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        self.keystroke_f_row_and_check_report(press_fn=True, expected_report_type=self.ReportType.SHORTCUT_KEY)

        self.testCaseChecked("BUS_40A3_0005", _AUTHOR)
    # end def test_shortcut_keys_with_fn_key

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL, 1)
    @level("Business")
    @bugtracker("Pollux_Fn_Lock_Reversed")
    def test_cid_keys_with_fn_key(self):
        """
        [PWS]
        Verify that the device reports the CID key code for each Fn + Fx key pressed in state {FnInversion OFF, Keys
        diverted}
        """
        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        self._set_cid_reporting_diverted_and_verify_diverted_button_event(press_fn=True)

        self.testCaseChecked("BUS_40A3_0006", _AUTHOR)
    # end def test_cid_keys_with_fn_key

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL, 1)
    @level("Business")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.CHROME_OS,))
    @bugtracker("ChromeOS_Backlight_KeyCode")
    def test_chrome_os_shortcut_keys(self):
        """
        [PWS]
        Verify that the device reports the Shortcut key for each Fx key pressed on Chrome OS(FN-Lock feature remains
        without effects) but for PWS Fn Lock UX v1.2, the FN-Lock feature on Chrome OS has the same behavior as other
        OSs
        """
        KeyMatrixTestUtils.emulate_os_shortcut(test_case=self,
                                               os_type=OS.CHROME,
                                               duration=ButtonStimuliInterface.LONG_PRESS_DURATION,
                                               delay=0.1)

        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        self.keystroke_f_row_and_check_report(press_fn=False, expected_report_type=self.ReportType.SHORTCUT_KEY,
                                              os_variant=OS.CHROME)

        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        self.keystroke_f_row_and_check_report(
            press_fn=False,
            expected_report_type=self.ReportType.F_KEY if self.f.PRODUCT.DEVICE.FN_LOCK.F_PWS_UX_V1_2 else
            self.ReportType.SHORTCUT_KEY,
            os_variant=OS.CHROME)
        self.testCaseChecked("BUS_40A3_0007", _AUTHOR)
    # end def test_chrome_os_shortcut_keys

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL, 1)
    @level("Business")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.CHROME_OS,))
    @bugtracker("ChromeOS_Backlight_KeyCode")
    def test_chrome_os_shortcut_keys_with_fn_key(self):
        """
        [PWS]
        Verify that the device reports the F key for each Fn + Fx key pressed on Chrome OS(FN-Lock feature remains
        without effects) but for PWS Fn Lock UX v1.2, the FN-Lock feature on Chrome OS has the same behavior as other
        OSs
        """
        KeyMatrixTestUtils.emulate_os_shortcut(test_case=self,
                                               os_type=OS.CHROME,
                                               duration=ButtonStimuliInterface.LONG_PRESS_DURATION,
                                               delay=0.1)

        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        self.keystroke_f_row_and_check_report(
            press_fn=True,
            expected_report_type=self.ReportType.SHORTCUT_KEY if self.f.PRODUCT.DEVICE.FN_LOCK.F_PWS_UX_V1_2 else
            self.ReportType.F_KEY,
            os_variant=OS.CHROME)

        self.set_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                    fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        self.keystroke_f_row_and_check_report(press_fn=True, expected_report_type=self.ReportType.F_KEY,
                                              os_variant=OS.CHROME)
        self.testCaseChecked("BUS_40A3_0008", _AUTHOR)
    # end def test_chrome_os_shortcut_keys_with_fn_key

    @features("Feature40A3")
    @features('NoGamingDevice')
    @features('Feature1805')
    @features('Feature1816')
    @level("Business")
    @services("HardwareReset")
    @services('RequiredKeys', (KEY_ID.HOST_1,))
    @bugtracker("Default_Fn_Inversion_State")
    def test_default_fn_inversion_after_oob(self):
        """
        [PWS]
        Verify that FnInversion is ON by default in OOB state

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-477
        """
        self.post_requisite_clean_pairing_info_on_receivers = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pre-pair device to the first receiver")
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pair_device_to_receiver(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1805.SetOobState request")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        if self.is_hardware_reset_possible():
            self.reset(hardware_reset=True, verify_connection_reset=False,
                       verify_wireless_device_status_broadcast_event=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for host_idx in range(self.nb_host):
            self.check_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.ON)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_40A3_0009", _AUTHOR)
    # end def test_default_fn_inversion_after_oob

    @features("Feature40A3")
    @features('GamingDevice')
    @level('Business', 'SmokeTests')
    def test_gaming_f_keys_host(self):
        """
        [Gaming]

        Verify that the device reports the F key for each Fx key pressed in state {FnInversion OFF} when the device is
        in Host mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set FnInversion to OFF for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the device into host mode by 0x8100.setOnboardMode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        OnboardProfilesTestUtils.clean_up_messages(self, delay=1)
        self.keystroke_f_row_and_check_report_gaming()

        self.testCaseChecked("BUS_40A3_0011", _AUTHOR)
    # end def test_gaming_f_keys_host

    @features("Feature40A3")
    @features('GamingDevice')
    @level("Business")
    def test_gaming_f_keys_onboard(self):
        """
        [Gaming]
        Verify that the device reports the F key for each Fx key pressed in state {FnInversion OFF} when the device is
        in OnBoard mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set FnInversion to OFF for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the device into host mode by 0x8100.setOnboardMode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.ONBOARD_MODE)

        OnboardProfilesTestUtils.clean_up_messages(self, delay=1)
        self.keystroke_f_row_and_check_report_gaming()

        self.testCaseChecked("BUS_40A3_0012", _AUTHOR)
    # end def test_gaming_f_keys_onboard

    @features("Feature40A3")
    @features("Feature8010")
    @features("Feature8100")
    @features('GamingDevice')
    @level("Business")
    @skip("In development")
    def test_gaming_f_keys_host_swctrl_dis(self):
        """
        [Gaming]

        Verify that the device reports the F key for each Fx key pressed in state {FnInversion ON} when the device is
        in Host mode and software control is disabled
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set FnInversion to ON for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the device into host mode by 0x8100.setOnboardMode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable software control by 0x8010")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Wait 0x8010 implement

        OnboardProfilesTestUtils.clean_up_messages(self, delay=1)
        self.keystroke_f_row_and_check_report_gaming()

        self.testCaseChecked("BUS_40A3_0013", _AUTHOR)
    # end def test_gaming_f_keys_host_swctrl_dis

    @features("Feature40A3")
    @features('GamingDevice')
    @features("Feature8010")
    @features("Feature8100")
    @level("Business")
    @skip("In development")
    def test_gaming_g_keys_host_swctrl_en(self):
        """
        [Gaming]

        Verify that the device reports the G key for each Fx key pressed in state {FnInversion ON} when the device is
        in Host mode and software control is enabled
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set FnInversion to ON for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the device into host mode by 0x8100.setOnboardMode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # TODO: Wait 0x8010 implement for the following steps
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable software control by 0x8010")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {dual_key} value in range {all_dual_keys}")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Keystroke {dual_key}")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that the HIDPP event (0x8010) is the corresponding Fx key")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_40A3_0014", _AUTHOR)
    # end def test_gaming_g_keys_host_swctrl_en

    @features("Feature40A3")
    @features("Feature8100")
    @features('GamingDevice')
    @level("Business")
    def test_gaming_remapped_keys_onboard_remapped(self):
        """
        [Gaming]

        Verify that the device reports the remapped key for each Fx key pressed in state {FnInversion ON} when the
        device is in OnBoard mode and key is remapped in profile
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set FnInversion to ON for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the device into onboard mode by 0x8100.setOnboardMode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.ONBOARD_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over key_id in range {(KEY_ID.KEYBOARD_F1, KEY_ID.KEYBOARD_F24)}")
        # --------------------------------------------------------------------------------------------------------------
        profile_1 = OnboardProfiles.SectorId.PROFILE_START
        btn_index = 0
        for key_id in range(KEY_ID.KEYBOARD_F1, KEY_ID.KEYBOARD_F24):
            if key_id not in self.button_stimuli_emulator._keyboard_layout.KEYS:
                continue
            # end if
            mouse_left_button = ProfileButton.create_mouse_button(ProfileButton.MouseButton.LEFT)
            btn_settings = OnboardProfilesTestUtils.get_default_button_settings(
                self, modifier={btn_index: mouse_left_button})
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create profiles from OOB profiles and change "
                                     f"{str(KEY_ID(key_id))} to mouse right button.")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.Profile.create_default_profiles(self,
                                                                     {ProfileFieldName.BUTTON: HexList(btn_settings)})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Create default profile directory and set profile 0x0001 as active profile")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(self)
            OnboardProfilesTestUtils.HIDppHelper.set_active_profile(self, profile_id=profile_1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the modified profile settings are all as expected results.")
            # ----------------------------------------------------------------------------------------------------------
            profile = OnboardProfilesTestUtils.Profile.read_profile(self, profile_1)
            checker = OnboardProfilesTestUtils.ProfileChecker
            check_map = checker.get_check_map(self, 0)
            check_map[ProfileFieldName.BUTTON] = (checker.check_button_fields, HexList(btn_settings))
            check_map['crc'] = (checker.check_crc, OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2]))
            checker.check_fields(self, profile, type(profile), check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Click {str(KEY_ID(key_id))}")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)
            self.button_stimuli_emulator.keystroke(key_id=key_id)
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(KEY_ID.LEFT_BUTTON,
                                                                                                     MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(KEY_ID.LEFT_BUTTON,
                                                                                                     BREAK))
            btn_index += 1
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_40A3_0015", _AUTHOR)
    # end def test_gaming_remapped_keys_onboard_remapped

    @features("Feature40A3")
    @features('GamingDevice')
    @level("Business")
    def test_gaming_f_keys_onboard_not_remapped(self):
        """
        [Gaming]
        Verify that the device reports the F key for each Fx key pressed in state {FnInversion ON} when the device is
        in OnBoard mode and key is not remapped in profile
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set FnInversion to ON for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the device into onboard mode by 0x8100.setOnboardMode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.ONBOARD_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set active profile to OOB profile 0x{OnboardProfiles.SectorId.OOB_PROFILE_START:4x}")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_active_profile(self, OnboardProfiles.SectorId.OOB_PROFILE_START)

        OnboardProfilesTestUtils.clean_up_messages(self, delay=1)
        self.keystroke_f_row_and_check_report_gaming()

        self.testCaseChecked("BUS_40A3_0016", _AUTHOR)
    # end def test_gaming_f_keys_onboard_not_remapped

    @features("Feature40A3")
    @features('GamingDevice')
    @features('Feature1805')
    @features('Feature1817')
    @level("Business")
    @services("HardwareReset")
    @skip("In development")
    def test_gaming_default_fn_inversion_after_oob(self):
        """
        [Gaming]
        The fnInversionState shall be deactivated by default in the OOB state
        """
        self.set_fn_inversion_state_for_all_host(
            FnInversionForMultiHostDevices.FnInversionState.ON)

        # Determine slot by ini config. Using Lightspeed protocol by default according x1817 feature spec
        slot = PrepairingManagement.PairingSlot.LS
        if self.f.PRODUCT.FEATURES.COMMON.LIGHTSPEED_PREPAIRING.F_Ls2Slot:
            slot = PrepairingManagement.PairingSlot.LS2
        elif self.f.PRODUCT.FEATURES.COMMON.LIGHTSPEED_PREPAIRING.F_CrushSlot:
            slot = PrepairingManagement.PairingSlot.CRUSH
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pre-pair device to the first receiver")
        # --------------------------------------------------------------------------------------------------------------
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot,
            long_term_key=RandHexList(SetLTK.LEN.LTK // 8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1805.SetOobState request")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=self)

        # TODO: Follow the procedure as PWS products. Pre-pair(0x1816) the DUT and receiver first, then OOB and
        #  power cycle. For PWS products, it works well. But in the gaming product(verify it on topaz_tkl), even if
        #  the DUT is pre-paired by 0x1817, the DUT still doesn't connect to the receiver automatically after
        #  OOB + power cycle. Need to investigate it further.
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform a device hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        if self.is_hardware_reset_possible():
            self.reset(hardware_reset=True, verify_connection_reset=False,
                       verify_wireless_device_status_broadcast_event=False)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for host_idx in range(self.nb_host):
            self.check_fn_inversion_state(host_idx, FnInversionForMultiHostDevices.FnInversionState.OFF)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_40A3_0017", _AUTHOR)
    # end def test_gaming_default_fn_inversion_after_oob

    def _keystroke_other_dual_keys_and_check_report(self, hidden_fn_keys):
        """
        Fn + Keystroke all other dual keys which are not in standard F-row function keys and check the report

        :param self: Current test case
        :type self: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param hidden_fn_keys: All the hidden fn keys
        :type hidden_fn_keys: ``dict``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {other_dual_key} value in range {all_other_dual_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for hidden_fn_key_name, hidden_fn_key_val in hidden_fn_keys.items():
            LogHelper.log_step(self, f'Emulate a Fn + keystroke on the supported key {str(KEY_ID(hidden_fn_key_val))}')
            self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)
            self.button_stimuli_emulator.keystroke(key_id=hidden_fn_key_val)
            self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                               delay=ButtonStimuliInterface.DEFAULT_DURATION)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {other_dual_key} value in range {all_other_dual_keys}")
        # --------------------------------------------------------------------------------------------------------------
        for hidden_fn_key_name, hidden_fn_key_val in hidden_fn_keys.items():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check that the HID report corresponds to the Shortcut key'
                                      f'({str(KEY_ID(hidden_fn_key_name))}) on {str(KEY_ID(hidden_fn_key_val))}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(hidden_fn_key_name, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(hidden_fn_key_name, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
    # def _keystroke_other_dual_keys_and_check_report

    @features("Feature40A3")
    @features('NoGamingDevice')
    @level("Business")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_other_dual_keys_f_keys(self):
        """
        Verify that all other dual printed keys are not affected by any change of fnInversionState
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set FnInversion to OFF for HOST1")
        # --------------------------------------------------------------------------------------------------------------
        FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self,
            host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.OFF)

        # To get all hidden fn keys which excludes the function keys in standard F-row and escape from FN_KEYS dict
        hidden_fn_keys = {}
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        for fn_key_name, fn_key_val in fn_keys.items():
            if fn_key_name in range(KEY_ID.KEYBOARD_F1, KEY_ID.KEYBOARD_F24) or fn_key_val == KEY_ID.KEYBOARD_ESCAPE:
                continue
            else:
                hidden_fn_keys[fn_key_name] = fn_key_val
            # end if
        # end for

        # Keystroke Fn + hidden_fn_keys and check the report
        self._keystroke_other_dual_keys_and_check_report(hidden_fn_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform FnLockKeyCombination")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=self.f.PRODUCT.F_IsGaming)
        self.check_f_lock_change_event(fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)
        self.check_fn_inversion_state(host_index=FnInversionForMultiHostDevices.HostIndex.HOST1,
                                      fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)

        # Keystroke Fn + hidden_fn_keys and check the report
        self._keystroke_other_dual_keys_and_check_report(hidden_fn_keys)

        self.testCaseChecked("BUS_40A3_0018", _AUTHOR)
    # end def test_other_dual_keys_f_keys

    @features("Feature40A3")
    @features('NoGamingDevice')
    @level("Business")
    @skip("In development")
    def test_fn_lock_led(self):
        """
        [PWS]
        As a user, I expect my device to display the Connectivity Status if my device is a keyboard when I press
        “fn + ESC” keys to change the fn inversion.
        """
        DevicePairingTestUtils.pair_all_hosts_to_receivers(self)
        self.post_requisite_clean_pairing_info_on_receivers = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for idx in range(self.nb_host):
            # Either FnInversionState is ON or OFF, the LED behavior should be same
            for _ in range(len([FnInversionForMultiHostDevices.FnInversionState.ON,
                               FnInversionForMultiHostDevices.FnInversionState.OFF])):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Start LEDs monitoring')
                # ------------------------------------------------------------------------------------------------------
                BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(
                    self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Perform FnLockKeyCombination(Keystroke Fn key + ESC)")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=False)

                # Sleep until the LED of HOSTx timeout
                time.sleep(6)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check the LED of HOST{idx+1} is steady for 5s then off")
                # ------------------------------------------------------------------------------------------------------
                BleProConnectionSchemeTestUtils.LedSpyHelper.check_steady_time(
                    self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1 + idx,
                    position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
                BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                    self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1 + idx)

                # Check the other LEDs are always off
                for idx2 in range(self.nb_host):
                    if idx2 != idx:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(self, f"Check the LED of HOST{idx2 + 1} is always off")
                        # ----------------------------------------------------------------------------------------------
                        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1 + idx2,
                            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.FIVE_SECONDS,
                            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
                    # end if
                # end for

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Stop LEDs monitoring')
                # ------------------------------------------------------------------------------------------------------
                BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self,
                                                                             led_identifiers=CONNECTIVITY_STATUS_LEDS)

            if self.nb_host > 1:
                # Switch to the next host for loop
                self.switch_to_another_host((idx + 1) % self.nb_host)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over {host} value in range {all_available_hosts}")
        # --------------------------------------------------------------------------------------------------------------
        for idx in range(self.nb_host):
            current_channel_receiver_usb_port_index = ChannelUtils.get_port_index(test_case=self)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Disable the USB port {current_channel_receiver_usb_port_index} of the receiver "
                                     f"for HOST{idx+1} to disconnect the DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.device.disable_usb_port(port_index=current_channel_receiver_usb_port_index)
            self.post_requisite_enable_all_usb_ports = True

            # Either FnInversionState is ON or OFF, the LED behavior should be same
            for _ in range(len([FnInversionForMultiHostDevices.FnInversionState.ON,
                               FnInversionForMultiHostDevices.FnInversionState.OFF])):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Start LEDs monitoring')
                # ------------------------------------------------------------------------------------------------------
                BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(
                    self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Perform FnLockKeyCombination(Keystroke Fn key + ESC)")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=False)

                # Sleep until the LED of HOSTx timeout
                time.sleep(6)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check the LED of HOST{idx+1} is SLOW_BLINKING for 5s then off")
                # ------------------------------------------------------------------------------------------------------
                BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
                    self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1 + idx,
                    position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
                BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                    self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1 + idx)

                # Check the other LEDs are always off
                for idx2 in range(self.nb_host):
                    if idx2 != idx:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(self, f"Check the LED of HOST{idx2 + 1} is always off")
                        # ----------------------------------------------------------------------------------------------
                        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1 + idx2,
                            minimum_duration=BleProConnectionSchemeTestUtils.LedSpyHelper.FIVE_SECONDS,
                            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
                    # end if
                # end for

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Stop LEDs monitoring')
                # ------------------------------------------------------------------------------------------------------
                BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(
                    self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

            if self.nb_host > 1 and (idx + 1) < self.nb_host:
                # Change to the next host by keystroke HOSTx button
                self.button_stimuli_emulator.change_host(HOST.ALL[idx + 1])
                DeviceManagerUtils.set_channel(
                    test_case=self,
                    new_channel_id=ChannelIdentifier(
                        port_index=self.host_number_to_port_index((idx + 1))))
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_40A3_0019#1", _AUTHOR)
    # end def test_fn_lock_led

    @features("Feature40A3")
    @features('GamingDevice')
    @level("Business")
    @skip("In development")
    def test_gaming_fn_key_led(self):
        """
        [Gaming]
        When fnInversionState is changed, the device shall inform the user through a LED effect.
        As a user, I expect my device will switch-off the LED after a defined timeout even if FN lock is activated and
        shows its FN Lock status after OFF/ON if FN lock is activated.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=LED_ID.FN_KEY_LED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform FnLockKeyCombination(Keystroke Fn key)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=True)


        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check the LED of Fn key is STEADY for 5s then off")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_slow_blinking_time(
            self, led_id=LED_ID.FN_KEY_LED,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.ANY)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.FN_KEY_LED)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform FnLockKeyCombination(Keystroke Fn key)")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.perform_fn_lock_key_combination(is_gaming=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the LED of Fn key is OFF")
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.FN_KEY_LED)

        self.testCaseChecked("BUS_40A3_0019#2", _AUTHOR)
    # end def test_gaming_fn_key_led
# end class FnInversionForMultiHostDevicesBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
