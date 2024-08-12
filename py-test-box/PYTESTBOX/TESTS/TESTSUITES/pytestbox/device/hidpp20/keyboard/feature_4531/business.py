#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4531.business
:brief: HID++ 2.0 ``MultiPlatform`` business test suite
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
from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.common.powermodes import PowerModes
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import LED_ID
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.multiplatformutils import MultiPlatformTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4531.multiplatform import MultiPlatformTestCase
from pytestbox.shared.base.bleprosafeprepairedreceiverutils import BleProSafePrePairedReceiverTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiPlatformBusinessTestCase(MultiPlatformTestCase):
    """
    Validate ``MultiPlatform`` business test cases
    """

    @features("Feature4531")
    @level('Business', 'SmokeTests')
    def test_keyboard_os_layout_selection_mechanism(self):
        """
        Verify the keyboard OS layout selections are available on all paired channels of the device.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, "Wait the getHostPlatform response and check the platformIndex is defined and as expected")
            # ----------------------------------------------------------------------------------------------------------
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
                    (checker.check_platform_source, int(self.config.F_PlatformSource[host_index])),
                "auto_platform":
                    (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
                "auto_descriptor":
                    (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_4531_0001", _AUTHOR)
    # end def test_keyboard_os_layout_selection_mechanism

    @features("Feature4531")
    @level("Business")
    @services('BleContext')
    @bugtracker("Platform_Source")
    def test_keyboard_os_layout_selection_mechanism_ble(self):
        """
        Verify the device shall select automatically the keyboard layout after BLE pairing
        """
        if self.device_memory_manager is not None:
            # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
            self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                test_case=self, memory_manager=self.device_memory_manager)
        # end if
        host_index = 0x00
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start the discovery sequence")
        # --------------------------------------------------------------------------------------------------------------
        device_bluetooth_address = DiscoveryTestUtils.discover_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start the pairing sequence")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.set_authentication_method(test_case=self, config_manager=self.config_manager)
        DevicePairingTestUtils.start_pairing_sequence(self, device_bluetooth_address, log_check=True)

        # Wait for a start pairing status notification
        DevicePairingTestUtils.PairingChecker.check_start_pairing_status(self)

        # Wait for a display passkey notification
        passkey_digits = DevicePairingTestUtils.PairingChecker.get_passkey_digits(self)

        # Wait for a 'Digit Start' passkey notification
        DevicePairingTestUtils.PairingChecker.get_display_passkey_start(self)

        # Loop over passkey inputs list provided by the receiver
        DevicePairingTestUtils.generate_keystrokes(self, passkey_digits)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=False)
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent, timeout=.5, check_first_message=False, allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Wait the getHostPlatform response and check the platformSource is "
                                  f"{MultiPlatform.PlatformSource.AUTO}")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "status": (checker.check_status, MultiPlatform.Status.PAIRED),
            "platform_index": (checker.check_platform_index, int(self.config.F_PlatformIndex[host_index])),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.DEFAULT),
            "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
            "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        self.testCaseChecked("BUS_4531_0002", _AUTHOR)
    # end def test_keyboard_os_layout_selection_mechanism_ble

    @features("Feature4531")
    @level("Business")
    @services('BLEProReceiver')
    @bugtracker("Platform_Source")
    def test_keyboard_os_layout_selection_mechanism_receiver(self):
        """
        Verify the device shall select the default keyboard layout when the device is connected through a Bolt
        receiver.
        """
        if self.device_memory_manager is not None:
            # Retrieve the last BLE address in the DUT NVS to correctly filter Device Discovery notifications
            self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
                test_case=self, memory_manager=self.device_memory_manager)
        # end if
        host_index = 0x01
        marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        if marketing_name.endswith('for Mac'):
            default_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
                self, MultiPlatform.OsMask.MAC_OS)
        else:
            windows_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
                self, MultiPlatform.OsMask.WINDOWS)
            default_platform_index = windows_platform_index
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Initialize the authentication method parameter")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean the receiver pairing slot of HOST.CH2")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        DevicePairingTestUtils.unpair_all(self, host_index + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Force the device in pairing mode with a long press on the Host{host_index + 1} Easy switch button")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_unpairing = True
        self.button_stimuli_emulator.enter_pairing_mode(host_index=host_index + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start the discovery sequence")
        # --------------------------------------------------------------------------------------------------------------
        bluetooth_address = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start the pairing sequence")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_device(self, bluetooth_address)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index + 1}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=host_index + 1)
        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index + 1), allow_no_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the getHostPlatform response and check the platformSource is "
                                  f"{MultiPlatform.PlatformSource.DEFAULT}")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "status": (checker.check_status, MultiPlatform.Status.PAIRED),
            "platform_index": (checker.check_platform_index, default_platform_index),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.DEFAULT),
            "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
            "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press host easy switch key to switch to {HOST.CH1}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=1, device_index=HOST.CH1), allow_no_message=True)

        self.testCaseChecked("BUS_4531_0003", _AUTHOR)
    # end def test_keyboard_os_layout_selection_mechanism_receiver

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Business")
    @bugtracker("Platform_Source")
    def test_keyboard_os_layout_restore_after_host_changed(self):
        """
        Verify the device shall restore the current host keyboard layout at each host change
        """
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        default_platform_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reload initial NVS")
            # ----------------------------------------------------------------------------------------------------------
            if self.post_requisite_reload_nvs:
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Pair the device to BLE Pro receiver with all available hosts")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            self.post_requisite_unpairing = True
            DevicePairingTestUtils.pair_all_available_hosts(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index + 1}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index + 1)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index + 1), allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self,
                                                                            host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the getHostPlatform.platformIndex is defined and as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, MultiPlatform.Status.PAIRED),
                "platform_index": (checker.check_platform_index, default_platform_index),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.DEFAULT),
                "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
                "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send setHostPlatform request with platformIndex = {platform_index_to_be_changed}")
            # ----------------------------------------------------------------------------------------------------------
            MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                                 host_index=host_index,
                                                                 platform_index=platform_index_to_be_changed)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self,
                                                                                check_first_message=False)
            checker = MultiPlatformTestUtils.PlatformChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE)
            })
            checker.check_fields(test_case=self,
                                 message=response,
                                 expected_cls=self.feature_4531.platform_change_event_cls,
                                 check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index + 2}")
            # ----------------------------------------------------------------------------------------------------------
            another_host_index = host_index + 1 if host_index + 1 < self.f.PRODUCT.DEVICE.F_NbHosts else 1
            self.button_stimuli_emulator.change_host(host_index=another_host_index + 1)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=another_host_index + 1),
                allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {another_host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self,
                                                                            host_index=another_host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the getHostPlatform.platformIndex is defined and as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, another_host_index),
                "status": (checker.check_status, MultiPlatform.Status.PAIRED),
                "platform_index": (checker.check_platform_index, default_platform_index),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.DEFAULT),
                "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[another_host_index])),
                "auto_descriptor": (checker.check_auto_descriptor,
                                    int(self.config.F_AutoDescriptor[another_host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index + 1}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index + 1)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index + 1), allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self,
                                                                            host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the getHostPlatform.platformIndex is defined and as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, MultiPlatform.Status.PAIRED),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE),
                "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
                "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {HOST.CH1}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=HOST.CH1), allow_no_message=True)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_4531_0004", _AUTHOR)
    # end def test_keyboard_os_layout_restore_after_host_changed

    @features("Feature4531")
    @features("Feature1830")
    @features("SetHostPlatform")
    @level("Business")
    @services("SimultaneousKeystrokes")
    def test_keyboard_os_layout_restore_after_deep_sleep(self):
        """
        Verify the device shall restore the current host keyboard layout at wake up from deep sleep
        """
        self.post_requisite_reload_nvs = True
        host_index = 0
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        default_platform_index = 0
        marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        default_layout_os_type = OS.MAC if marketing_name.endswith('for Mac') else OS.WINDOWS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Root.GetFeature(0x1830)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=PowerModes.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setHostPlatform request with platformIndex = {platform_index_to_be_changed} to "
                                 "change the current host keyboard layout")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self, host_index=host_index,
                                                                        platform_index=platform_index_to_be_changed)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the setHostPlatform response and check its inputs fields are valid")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
        })
        checker.check_fields(self, response, self.feature_4531.set_host_platform_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)
        checker = MultiPlatformTestUtils.PlatformChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_4531.platform_change_event_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.setPowerMode request with powerMode = 3 (deep-sleep mode)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake up the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getHostPlatform request")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Wait getHostPlatform response and check the platformIndex equals {platform_index_to_be_changed}")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "status": (checker.check_status, MultiPlatform.Status.PAIRED),
            "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE),
            "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
            "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Long press keyboard OS layout selection shortcut to switch to default keyboard layout")
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.emulate_os_shortcut(test_case=self,
                                               os_type=default_layout_os_type,
                                               duration=float(ButtonStimuliInterface.LONG_PRESS_DURATION))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)
        checker = MultiPlatformTestUtils.PlatformChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "platform_index": (checker.check_platform_index, default_platform_index),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.MANUAL)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_4531.platform_change_event_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.setPowerMode request with powerMode = 3 (deep-sleep mode)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake up the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getHostPlatform request")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex is as expected")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "status": (checker.check_status, MultiPlatform.Status.PAIRED),
            "platform_index": (checker.check_platform_index, default_platform_index),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.MANUAL),
            "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
            "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        self.testCaseChecked("BUS_4531_0005", _AUTHOR)
    # end def test_keyboard_os_layout_restore_after_deep_sleep

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Business")
    def test_configure_all_hosts_keyboard_os_layout_by_software(self):
        """
        Verify the user can configure the device through the SW
        """
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        interesting_keys = [KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,
                            KEY_ID.KEYBOARD_RIGHT_ALT, KEY_ID.KEYBOARD_A]
        variant = MultiPlatformTestUtils.get_os_type_thru_os_mask(
            os_mask=MultiPlatformTestUtils.get_os_mask_thru_platform_index(self, platform_index_to_be_changed))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device to BLE Pro receiver with all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_unpairing = True
        DevicePairingTestUtils.pair_all_available_hosts(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index + 1}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index + 1)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index + 1), allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setHostPlatform request with hostIndex = {host_index}, "
                                     f"platformIndex = {platform_index_to_be_changed}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                                            host_index=host_index,
                                                                            platform_index=platform_index_to_be_changed)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the setHostPlatform response and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            })
            checker.check_fields(self, response, self.feature_4531.set_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self,
                                                                                check_first_message=False)
            checker = MultiPlatformTestUtils.PlatformChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE)
            })
            checker.check_fields(test_case=self,
                                 message=response,
                                 expected_cls=self.feature_4531.platform_change_event_cls,
                                 check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self,
                                                                            host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Wait the getHostPlatform response and check the platformIndex = {platform_index_to_be_changed}")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, MultiPlatform.Status.PAIRED),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE),
                "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
                "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform keystrokes with some interesting keys")
            # ----------------------------------------------------------------------------------------------------------
            for key_id in interesting_keys:
                self.button_stimuli_emulator.keystroke(key_id=key_id)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over key in some interesting keys")
            # ----------------------------------------------------------------------------------------------------------
            for key_id in interesting_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in current OS mode')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                              variant=variant)

                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                              variant=variant)
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

        self.testCaseChecked("BUS_4531_0006", _AUTHOR)
    # end def test_configure_all_hosts_keyboard_os_layout_by_software

    @features("Feature4531")
    @level("Business")
    @services("SimultaneousKeystrokes")
    @services("Debugger")
    @services("LedIndicator")
    def test_configure_all_hosts_keyboard_os_layout_by_manual(self):
        """
        Verify the device shall inform the user through the current host easy switch key led when the user changes the
        layout manually
        """
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        os_type = MultiPlatformTestUtils.get_os_type_thru_os_mask(
            os_mask=MultiPlatformTestUtils.get_os_mask_thru_platform_index(self, platform_index_to_be_changed))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device to BLE Pro receiver with all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        self.post_requisite_unpairing = True
        DevicePairingTestUtils.pair_all_available_hosts(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        connectivity_leds = [LED_ID.CONNECTIVITY_STATUS_LED_1]
        host_indexs = [HOST.CH1]
        if self.f.PRODUCT.DEVICE.F_NbHosts > 1:
            connectivity_leds.append(LED_ID.CONNECTIVITY_STATUS_LED_2)
            host_indexs.append(HOST.CH2)
        # end if
        if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
            connectivity_leds.append(LED_ID.CONNECTIVITY_STATUS_LED_3)
            host_indexs.append(HOST.CH3)
        # end if
        for host_index, connectivity_led in zip(host_indexs, connectivity_leds):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Start LEDs monitoring')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=connectivity_leds)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index), allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, "Long press keyboard OS layout selection shortcut to switch keyboard layout")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.emulate_os_shortcut(test_case=self,
                                                   os_type=os_type,
                                                   duration=float(ButtonStimuliInterface.LONG_PRESS_DURATION))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self,
                                                                                check_first_message=False)
            checker = MultiPlatformTestUtils.PlatformChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index - 1),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.MANUAL)
            })
            checker.check_fields(test_case=self,
                                 message=response,
                                 expected_cls=self.feature_4531.platform_change_event_cls,
                                 check_map=check_map)

            for led_id in connectivity_leds:
                if led_id == connectivity_led:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, f"Check {str(led_id)} matching the current host index "
                                              f"{host_index} is steady")
                    # --------------------------------------------------------------------------------------------------
                    BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                        self, led_id=led_id, state=SchemeType.STEADY)
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, f"Check {str(led_id)} not matching the current host index "
                                              f"{host_index} is off")
                    # --------------------------------------------------------------------------------------------------
                    BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                        self, led_id=led_id, state=SchemeType.OFF)
                # end if
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Stop LEDs monitoring')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=connectivity_leds)
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

        self.testCaseChecked("BUS_4531_0007", _AUTHOR)
    # end def test_configure_all_hosts_keyboard_os_layout_by_manual

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Business")
    @services("PowerSupply")
    @bugtracker("PlatformChange_EventNotSent")
    def test_keyboard_os_layout_restore_separately_after_power_reset(self):
        """
        Verify the device shall store the keyboard layout for each host separately to be persistent after power cycle
        """
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        hosts_platform_index = list(map(int, self.config.F_PlatformIndex))
        hosts_platform_source = list(map(int, self.config.F_PlatformSource))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setHostPlatform request with hostIndex = {host_index}, "
                                     f"platformIndex = {platform_index_to_be_changed}")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            response = MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                                            host_index=host_index,
                                                                            platform_index=platform_index_to_be_changed)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the setHostPlatform response and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            })
            checker.check_fields(self, response, self.feature_4531.set_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            if int(self.config.F_Status[host_index]) == 1:
                response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self,
                                                                                    check_first_message=False)
                checker = MultiPlatformTestUtils.PlatformChangeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "host_index": (checker.check_host_index, host_index),
                    "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                    "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE)
                })
                checker.check_fields(test_case=self,
                                     message=response,
                                     expected_cls=self.feature_4531.platform_change_event_cls,
                                     check_map=check_map)
            else:
                self.assertNone(obtained=ChannelUtils.get_only(
                                            test_case=self,
                                            queue_name=HIDDispatcher.QueueName.EVENT,
                                            class_type=self.feature_4531.platform_change_event_cls,
                                            check_first_message=False,
                                            allow_no_message=True),
                                msg="The PlatformChange event shall not be sent, if the selected host is not paired.")
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power OFF -> ON the DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self,
                                                                            host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, int(self.config.F_Status[host_index])),
                "platform_index": (checker.check_platform_index,
                                   platform_index_to_be_changed if int(self.config.F_Status[host_index]) == 1
                                   else int(self.config.F_PlatformIndex[host_index])),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE),
                "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
                "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)
            hosts_platform_index[host_index] = platform_index_to_be_changed
            hosts_platform_source[host_index] = MultiPlatform.PlatformSource.SOFTWARE

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over other_host in all other available hosts")
            # ----------------------------------------------------------------------------------------------------------
            for other_host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
                if other_host == host_index:
                    continue
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {other_host}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self,
                                                                                host_index=other_host)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex is as expected")
                # ------------------------------------------------------------------------------------------------------
                checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "host_index": (checker.check_host_index, other_host),
                    "status": (checker.check_status, int(self.config.F_Status[other_host])),
                    "platform_index": (checker.check_platform_index,
                                       hosts_platform_index[other_host] if int(self.config.F_Status[other_host]) == 1
                                       else int(self.config.F_PlatformIndex[other_host])),
                    "platform_source": (checker.check_platform_source, hosts_platform_source[other_host]),
                    "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[other_host])),
                    "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[other_host])),
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

        self.testCaseChecked("BUS_4531_0008", _AUTHOR)
    # end def test_keyboard_os_layout_restore_separately_after_power_reset

    @features("Feature4531")
    @features("Feature1830")
    @features("SetHostPlatform")
    @level("Business")
    @bugtracker("PlatformChange_EventNotSent")
    def test_keyboard_os_layout_restore_separately_after_deep_sleep(self):
        """
        Verify the device shall store the keyboard layout for each host separately to be persistent after deep sleep
        """
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        hosts_platform_index = list(map(int, self.config.F_PlatformIndex))
        hosts_platform_source = list(map(int, self.config.F_PlatformSource))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Root.GetFeature(0x1830)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=PowerModes.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setHostPlatform request with hostIndex = {host_index}, "
                                     f"platformIndex = {platform_index_to_be_changed}")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            response = MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                                            host_index=host_index,
                                                                            platform_index=platform_index_to_be_changed)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the setHostPlatform response and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            })
            checker.check_fields(self, response, self.feature_4531.set_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            if int(self.config.F_Status[host_index]) == 1:
                response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self,
                                                                                    check_first_message=False)
                checker = MultiPlatformTestUtils.PlatformChangeEventChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "host_index": (checker.check_host_index, host_index),
                    "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                    "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE)
                })
                checker.check_fields(test_case=self,
                                     message=response,
                                     expected_cls=self.feature_4531.platform_change_event_cls,
                                     check_map=check_map)
            else:
                self.assertNone(obtained=ChannelUtils.get_only(
                                            test_case=self,
                                            queue_name=HIDDispatcher.QueueName.EVENT,
                                            class_type=self.feature_4531.platform_change_event_cls,
                                            check_first_message=False,
                                            allow_no_message=True),
                                msg="The PlatformChange event shall not be sent, if the selected host is not paired.")
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 0x1830.setPowerMode request with powerMode = 3 (deep-sleep mode)")
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform an user action to wake up the DUT")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, int(self.config.F_Status[host_index])),
                "platform_index": (checker.check_platform_index,
                                   platform_index_to_be_changed if int(self.config.F_Status[host_index]) == 1
                                   else int(self.config.F_PlatformIndex[host_index])),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE),
                "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
                "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)
            hosts_platform_index[host_index] = platform_index_to_be_changed
            hosts_platform_source[host_index] = MultiPlatform.PlatformSource.SOFTWARE

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over other_host in all other available hosts")
            # ----------------------------------------------------------------------------------------------------------
            for other_host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
                if other_host == host_index:
                    continue
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {other_host}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=other_host)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex is as expected")
                # ------------------------------------------------------------------------------------------------------
                checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "host_index": (checker.check_host_index, other_host),
                    "status": (checker.check_status, int(self.config.F_Status[other_host])),
                    "platform_index": (checker.check_platform_index,
                                       hosts_platform_index[other_host] if int(self.config.F_Status[other_host]) == 1
                                       else int(self.config.F_PlatformIndex[other_host])),
                    "platform_source": (checker.check_platform_source, hosts_platform_source[other_host]),
                    "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[other_host])),
                    "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[other_host])),
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

        self.testCaseChecked("BUS_4531_0009", _AUTHOR)
    # end def test_keyboard_os_layout_restore_separately_after_deep_sleep

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Business")
    @bugtracker("Platform_Source")
    def test_keyboard_os_layout_restore_separately_after_host_change(self):
        """
        Verify the device shall store the keyboard layout for each host separately to be persistent after host change
        """
        self.post_requisite_reload_nvs = True
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        default_platform_index = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over host in all available hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reload initial NVS")
            # ----------------------------------------------------------------------------------------------------------
            if self.post_requisite_reload_nvs:
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Pair the device to BLE Pro receiver with all available hosts")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            self.post_requisite_unpairing = True
            DevicePairingTestUtils.pair_all_available_hosts(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index + 1}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index + 1)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index + 1), allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setHostPlatform request with hostIndex = {host_index}, "
                                     f"platformIndex = {platform_index_to_be_changed}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                                            host_index=host_index,
                                                                            platform_index=platform_index_to_be_changed)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the setHostPlatform response and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            })
            checker.check_fields(self, response, self.feature_4531.set_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self,
                                                                                check_first_message=False)
            checker = MultiPlatformTestUtils.PlatformChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE)
            })
            checker.check_fields(test_case=self,
                                 message=response,
                                 expected_cls=self.feature_4531.platform_change_event_cls,
                                 check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, MultiPlatform.Status.PAIRED),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE),
                "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
                "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over other_host in all other available hosts")
            # ----------------------------------------------------------------------------------------------------------
            for other_host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
                if other_host == host_index:
                    continue
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Press host easy switch key to switch to {other_host + 1}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.change_host(host_index=other_host + 1)
                DeviceManagerUtils.switch_channel(
                    test_case=self,
                    new_channel_id=ChannelIdentifier(port_index=1, device_index=other_host + 1), allow_no_message=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {other_host}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=other_host)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex is as expected")
                # ------------------------------------------------------------------------------------------------------
                checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
                check_map = checker.get_default_check_map(self)
                check_map.update({
                    "host_index": (checker.check_host_index, other_host),
                    "status": (checker.check_status, MultiPlatform.Status.PAIRED),
                    "platform_index": (checker.check_platform_index, default_platform_index),
                    "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.DEFAULT),
                    "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[other_host])),
                    "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[other_host])),
                })
                checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {host_index + 1}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index + 1)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=host_index + 1), allow_no_message=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex is as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "status": (checker.check_status, MultiPlatform.Status.PAIRED),
                "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
                "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE),
                "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
                "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
            })
            checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press host easy switch key to switch to {HOST.CH1}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=HOST.CH1)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=1, device_index=HOST.CH1), allow_no_message=True)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_4531_0010", _AUTHOR)
    # end def test_keyboard_os_layout_restore_separately_after_host_change

    @features("Feature4531")
    @features("Feature1805")
    @features("Feature1816")
    @features("Feature1E00")
    @features("SetHostPlatform")
    @level("Business")
    @services('BLEProReceiver')
    @services("SimultaneousKeystrokes")
    @services("HardwareReset")
    @bugtracker("Platform_Source")
    def test_keyboard_layout_reset_after_set_oob(self):
        """
        Verify the device shall select the default keyboard layout after the device was set OOB
        """
        host_index = 0x00
        platform_index_to_be_changed = len(self.config.F_OsMask) - 1
        os_type = MultiPlatformTestUtils.get_os_type_thru_os_mask(
            os_mask=MultiPlatformTestUtils.get_os_mask_thru_platform_index(self, platform_index_to_be_changed))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Root.GetFeature(0x1805)")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=OobState.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Long press keyboard OS layout selection shortcut to switch keyboard layout")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
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
        LogHelper.log_step(self, "Pre-pair device to the first receiver")
        # --------------------------------------------------------------------------------------------------------------
        BleProSafePrePairedReceiverTestUtils.pre_pair_device_to_receiver(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Hidden Features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

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
        LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex and platformSource match"
                                  "the default keyboard layout")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "status": (checker.check_status, int(self.config.F_Status[host_index])),
            "platform_index": (checker.check_platform_index, int(self.config.F_PlatformIndex[host_index])),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.DEFAULT),
            "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
            "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setHostPlatform request to change the current keyboard OS layout")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        MultiPlatformTestUtils.HIDppHelper.set_host_platform(test_case=self,
                                                             host_index=host_index,
                                                             platform_index=platform_index_to_be_changed)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait the PlatformChange event and check its inputs fields are valid")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.platform_change_event(test_case=self, check_first_message=False)
        checker = MultiPlatformTestUtils.PlatformChangeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "platform_index": (checker.check_platform_index, platform_index_to_be_changed),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.SOFTWARE)
        })
        checker.check_fields(test_case=self,
                             message=response,
                             expected_cls=self.feature_4531.platform_change_event_cls,
                             check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

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
        LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {host_index}")
        # --------------------------------------------------------------------------------------------------------------
        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(test_case=self, host_index=host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getHostPlatform response and check the platformIndex and platformSource match"
                                  "the default keyboard layout")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "status": (checker.check_status, int(self.config.F_Status[host_index])),
            "platform_index": (checker.check_platform_index, int(self.config.F_PlatformIndex[host_index])),
            "platform_source": (checker.check_platform_source, int(self.config.F_PlatformSource[host_index])),
            "auto_platform": (checker.check_auto_platform, int(self.config.F_AutoPlatform[host_index])),
            "auto_descriptor": (checker.check_auto_descriptor, int(self.config.F_AutoDescriptor[host_index])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        self.testCaseChecked("BUS_4531_0011", _AUTHOR)
    # end def test_keyboard_layout_reset_after_set_oob
# end class MultiPlatformBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
