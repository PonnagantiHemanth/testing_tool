#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4531.functionality
:brief: HID++ 2.0 ``MultiPlatform`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/10/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import MAKE
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.multiplatformutils import MultiPlatformTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4531.multiplatform import MultiPlatformTestCase
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiPlatformFunctionalityTestCase(MultiPlatformTestCase):
    """
    Validate ``MultiPlatform`` functionality test cases
    """

    @features("Feature4531")
    @level("Functionality")
    @services('SimultaneousKeystrokes')
    def test_platform_change_by_manual(self):
        """
        Verify the PlatformChange event is sent when the platform index of current host is changed by the user.
        """
        self.post_requisite_reload_nvs = True
        host_index = 0x00
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        os_type = MultiPlatformTestUtils.get_os_type_thru_os_mask(
            os_mask=MultiPlatformTestUtils.get_os_mask_thru_platform_index(self, platform_index_to_be_changed))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Long press keyboard OS layout selection shortcut to switch keyboard layout")
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.emulate_os_shortcut(test_case=self,
                                               os_type=os_type,
                                               duration=float(ButtonStimuliInterface.LONG_PRESS_DURATION))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)
        checker = MultiPlatformTestUtils.PlatformChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.MANUAL)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_4531.platform_change_event_cls,
                             check_map=check_map)

        self.testCaseChecked("FUN_4531_0001", _AUTHOR)
    # end def test_platform_change_by_manual

    @features("Feature4531")
    @level("Functionality")
    @services("SimultaneousKeystrokes")
    def test_platform_ignore_change(self):
        """
        Verify the PlatformChange event is not sent when the user long pressed a shortcut keys which are equal to
        current platform.
        """
        self.post_requisite_reload_nvs = True
        marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        os_type = OS.MAC if marketing_name.endswith('for Mac') else OS.WINDOWS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Long press keyboard OS layout selection shortcut Fn + P to switch to Windows keyboard layout")
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.emulate_os_shortcut(test_case=self,
                                               os_type=os_type,
                                               duration=float(ButtonStimuliInterface.LONG_PRESS_DURATION))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no PlatformChange is sent")
        # --------------------------------------------------------------------------------------------------------------
        response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                         class_type=self.feature_4531.platform_change_event_cls, 
                                         allow_no_message=True, check_first_message=False)
        self.assertNone(obtained=response,
                        msg="The PlatformChange event should not be received when the user long pressed a "
                            "shortcut keys which are equal to current platform")

        self.testCaseChecked("FUN_4531_0002", _AUTHOR)
    # end def test_platform_ignore_change

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    def test_platform_change_by_software(self):
        """
        Verify the PlatformChange event is sent when the platform index of current host is changed by the SW.
        """
        self.post_requisite_reload_nvs = True
        current_host = 0x00
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request to change the platform")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=current_host,
                                                             platform_index=platform_index_to_be_changed)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
        # --------------------------------------------------------------------------------------------------------------
        event = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)
        checker = MultiPlatformTestUtils.PlatformChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, 0x00),
            "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE)
        })
        checker.check_fields(self, event, self.feature_4531.platform_change_event_cls, check_map)

        self.testCaseChecked("FUN_4531_0003", _AUTHOR)
    # end def test_platform_change_by_software

    @features("Feature4531")
    @level("Functionality")
    def test_get_platform_descriptor_in_each_host(self):
        """
        Verify the platformDescriptor can be got from each host
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device to BLE Pro receiver with all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_unpairing = True
        DevicePairingTestUtils.pair_all_available_hosts(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(1, self.f.PRODUCT.DEVICE.F_NbHosts + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index), allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over platform_descriptor_index in all available hosts")
            # ----------------------------------------------------------------------------------------------------------
            for platform_descriptor_index in range(len(self.config.F_OsMask)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send getPlatformDescriptor request with {platform_descriptor_index}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiPlatformTestUtils.HIDppHelper.get_platform_descriptor(
                    test_case=self, platform_descriptor_index=platform_descriptor_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait the getPlatformDescriptor response inputs fields are valid")
                # ------------------------------------------------------------------------------------------------------
                checker = MultiPlatformTestUtils.GetPlatformDescriptorResponseChecker
                check_map = checker.get_default_check_map(self)
                os_mask_check_map = MultiPlatformTestUtils.OSMaskChecker.get_check_map(self, platform_descriptor_index)
                check_map.update({
                    "platform_index": (checker.check_platform_index, platform_descriptor_index),
                    "platform_descriptor_index": (checker.check_platform_descriptor_index, platform_descriptor_index),
                    "os_mask": (checker.check_os_mask, os_mask_check_map)
                })
                checker.check_fields(self, response, self.feature_4531.get_platform_descriptor_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press host easy switch key to switch to {HOST.CH1}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=1, device_index=HOST.CH1), allow_no_message=True)

        self.testCaseChecked("FUN_4531_0004", _AUTHOR)
    # end def test_get_platform_descriptor_in_each_host

    @features("Feature4531")
    @level("Functionality")
    @bugtracker("Platform_Source")
    def test_get_host_platform_in_each_host(self):
        """
        Verify hosts platform information can be got from each host
        """
        default_platform_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Initialize the authentication method parameter")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device to BLE Pro receiver with all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_unpairing = True
        DevicePairingTestUtils.pair_all_available_hosts(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(1, self.f.PRODUCT.DEVICE.F_NbHosts + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index), allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over host in all available hosts")
            # ----------------------------------------------------------------------------------------------------------
            for inner_host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {inner_host_index}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self,
                                                                                host_index=inner_host_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait the getHostPlatform response inputs fields are valid")
                # ------------------------------------------------------------------------------------------------------
                checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "host_index": (checker.check_host_index, inner_host_index),
                    "status": (checker.check_status, MultiPlatform.Status.PAIRED),
                    "platform_index": (checker.check_platform_index, default_platform_index),
                    "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.DEFAULT),
                    "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[inner_host_index])),
                    "auto_descriptor": (checker.check_auto_descriptor,
                                        int(self.config.F_AutoDescriptor[inner_host_index])),
                })
                checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press host easy switch key to switch to {HOST.CH1}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=1, device_index=HOST.CH1), allow_no_message=True)

        self.testCaseChecked("FUN_4531_0005", _AUTHOR)
    # end def test_get_host_platform_in_each_host

    @features("Feature4531")
    @level("Functionality")
    @services("SimultaneousKeystrokes")
    def test_platform_source_is_manual(self):
        """
        Verify hosts platformSource is manual when users pressed shortcut keys to change the keyboard OS layout
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        os_type = MultiPlatformTestUtils.get_os_type_thru_os_mask(
            os_mask=MultiPlatformTestUtils.get_os_mask_thru_platform_index(self, platform_index_to_be_changed))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Long press keyboard OS layout selection shortcut to switch keyboard layout")
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.emulate_os_shortcut(test_case=self,
                                               os_type=os_type,
                                               duration=float(ButtonStimuliInterface.LONG_PRESS_DURATION))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)
        checker = MultiPlatformTestUtils.PlatformChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.MANUAL)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_4531.platform_change_event_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getHostPlatform request with current host")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the getHostPlatform response and check the platformSource is Manual")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index":
                (checker.check_host_index, host_index),
            "status":
                (checker.check_status, int(self.config.F_Status[host_index])),
            "platform_index":
                (checker.check_platform_index, platform_index_to_be_changed),
            "platform_source":
                (checker.check_platform_source, MultiPlatform.PlatformSource.MANUAL),
            "auto_platform":
                (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
            "auto_descriptor":
                (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        self.testCaseChecked("FUN_4531_0006", _AUTHOR)
    # end def test_platform_source_is_manual

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    def test_platform_source_is_software(self):
        """
        Verify hosts platformSource is software when users changed the keyboard OS layout through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        platform_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setHostPlatform request with platformIndex = {platform_index}")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getHostPlatform request with current host")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait the getHostPlatform response and check the platformSource is "
                                  f"{MultiPlatform.PlatformSource.SOFTWARE}")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index":
                (checker.check_host_index, host_index),
            "status":
                (checker.check_status, int(self.config.F_Status[host_index])),
            "platform_index":
                (checker.check_platform_index, int(self.config.F_PlatformIndex[host_index])),
            "platform_source":
                (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE),
            "auto_platform":
                (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
            "auto_descriptor":
                (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        self.testCaseChecked("FUN_4531_0007", _AUTHOR)
    # end def test_platform_source_is_software

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.WINDOWS,))
    def test_all_keys_windows_layout(self):
        """
        Verify all FW keycodes are correct when a Windows OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        windows_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
            self, MultiPlatform.OsMask.WINDOWS)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of Windows OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=windows_platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.WINDOWS)

        self.testCaseChecked("FUN_4531_0008", _AUTHOR)
    # end def test_all_keys_windows_layout

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_all_keys_mac_os_layout(self):
        """
        Verify all FW keycodes are correct when a Mac OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        mac_os_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
            self, MultiPlatform.OsMask.MAC_OS)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of Mac OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=mac_os_platform_index)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event")
        # ----------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.MAC)

        self.testCaseChecked("FUN_4531_0009", _AUTHOR)
    # end def test_all_keys_mac_os_layout

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    def test_all_keys_ios_layout(self):
        """
        Verify all FW keycodes are correct when a iPad OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        ios_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(self, MultiPlatform.OsMask.IOS)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of iPad OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=ios_platform_index)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event")
        # ----------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.IPAD)

        self.testCaseChecked("FUN_4531_0010", _AUTHOR)
    # end def test_all_keys_ios_layout

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.CHROME_OS,))
    @bugtracker("ChromeOS_Backlight_KeyCode")
    def test_all_keys_chrome_os_layout(self):
        """
        Verify all FW keycodes are correct when a Chrome OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        chrome_os_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
            self, MultiPlatform.OsMask.CHROME_OS)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of Chrome OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=chrome_os_platform_index)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event")
        # ----------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.CHROME)

        self.testCaseChecked("FUN_4531_0011", _AUTHOR)
    # end def test_all_keys_chrome_os_layout

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.WIN_EMB,))
    def test_all_keys_win_emb_os_layout(self):
        """
        Verify all FW keycodes are correct when a WinEmb OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        win_emb_os_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
            self, MultiPlatform.OsMask.WIN_EMB)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of WinEmb OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=win_emb_os_platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.WIN_EMB)

        self.testCaseChecked("FUN_4531_0012", _AUTHOR)
    # end def test_all_keys_win_emb_os_layout

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.LINUX,))
    def test_all_keys_linux_os_layout(self):
        """
        Verify all FW keycodes are correct when a Linux OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        linux_os_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
            self, MultiPlatform.OsMask.LINUX)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of linux OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=linux_os_platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.LINUX)

        self.testCaseChecked("FUN_4531_0013", _AUTHOR)
    # end def test_all_keys_linux_os_layout

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.ANDROID,))
    def test_all_keys_android_os_layout(self):
        """
        Verify all FW keycodes are correct when an Android OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        android_os_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
            self, MultiPlatform.OsMask.ANDROID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of android OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=android_os_platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.ANDROID)

        self.testCaseChecked("FUN_4531_0014", _AUTHOR)
    # end def test_all_keys_android_os_layout

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.WEB_OS,))
    def test_all_keys_web_os_layout(self):
        """
        Verify all FW keycodes are correct when an Web OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        web_os_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
            self, MultiPlatform.OsMask.WEB_OS)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of Web OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=web_os_platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.WEB_OS)

        self.testCaseChecked("FUN_4531_0015", _AUTHOR)
    # end def test_all_keys_web_os_layout

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("SingleKeystroke")
    @services("RequiredOsLayout", (MultiPlatform.OsMask.TIZEN,))
    def test_all_keys_tizen_os_layout(self):
        """
        Verify all FW keycodes are correct when an Tizen OS keyboard layout has been selected through SW
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        tizen_os_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
            self, MultiPlatform.OsMask.TIZEN)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request with platformIndex = index of Tizen OS")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=tizen_os_platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Emulate keystrokes with all available keys")
        # --------------------------------------------------------------------------------------------------------------
        self._test_all_keys_stroke(variant=OS.TIZEN)

        self.testCaseChecked("FUN_4531_0016", _AUTHOR)
    # end def test_all_keys_tizen_os_layout

    def _test_all_keys_stroke(self, variant=None):
        """
        Emulate keystrokes with all available keys

        :param variant: OS detected by the firmware - OPTIONAL
        :type variant: ``str``
        """
        marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        if variant is None:
            variant = OS.MAC if marketing_name.endswith('for Mac') else OS.WINDOWS
        # end if
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)
        self.kosmos.sequencer.offline_mode = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over key in all supported keys")
        # --------------------------------------------------------------------------------------------------------------
        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Emulate a keystroke on the supported key = {str(key_id)}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over key in all supported keys")
        # --------------------------------------------------------------------------------------------------------------
        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in {variant} mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=variant)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=variant)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_all_keys_stroke
# end class MultiPlatformFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
