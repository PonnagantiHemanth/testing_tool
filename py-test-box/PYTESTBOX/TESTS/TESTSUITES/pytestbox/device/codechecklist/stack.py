#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.codechecklist.stack
:brief: Device Stack tests
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration, \
    BatteryLevelsCalibrationFactory
from pyhid.hidpp.features.common.changehost import ChangeHost, ChangeHostFactory
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName, DeviceFriendlyNameFactory
from pyhid.hidpp.features.root import RootFactory, Root
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.hostsinfoutils import HostsInfoTestUtils
from pytestbox.device.base.propertyaccessutils import PropertyAccessTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils
from pytestbox.shared.codechecklist.stack import SharedStackTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceStackTestCase(SharedStackTestCase, DeviceBaseTestCase):
    """
    Validate Stack management
    """

    def execute_scenario(self):
        # See ``SharedStackTestCase.execute_scenario``

        # Get the 0x0000 root feature object
        self.feature_0000 = RootFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceInfo request')
        # --------------------------------------------------------------------------------------------------------------
        DeviceInformationTestUtils.HIDppHelper.get_device_info(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Check if the Device Type And Name feature is supported by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        feature_0005_index, _, _, _ = DeviceTypeAndNameTestUtils.HIDppHelper.get_parameters(self, skip_not_found=True)

        if feature_0005_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetDeviceNameCount')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name_count(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetDeviceName with index = 0')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name(test_case=self, char_index=0)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Check if the Device Friendly Name feature is supported by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        feature_0007_index, _, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
            self, DeviceFriendlyName.FEATURE_ID, DeviceFriendlyNameFactory, skip_not_found=True)

        if feature_0007_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetFriendlyNameLen')
            # ----------------------------------------------------------------------------------------------------------
            DeviceFriendlyNameTestUtils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetFriendlyName')
            # ----------------------------------------------------------------------------------------------------------
            DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(self, byte_index=0)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Check if the Property Access feature is supported by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        feature_0011_index, _, _, _ = PropertyAccessTestUtils.HIDppHelper.get_parameters(self, skip_not_found=True)

        if feature_0011_index != Root.FEATURE_NOT_FOUND:
            self.post_requisite_reload_nvs = True

            property_id, _ = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(
                self, write_data_if_none=0xAA)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Get first property info")
            # ----------------------------------------------------------------------------------------------------------
            PropertyAccessTestUtils.HIDppHelper.get_property_info(self, property_id)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Check if Change Host is supported by the DUT (featureId = {ChangeHost.FEATURE_ID})')
        # --------------------------------------------------------------------------------------------------------------
        feature_1814_index, _, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
            self, ChangeHost.FEATURE_ID, ChangeHostFactory, skip_not_found=True)

        if feature_1814_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ChangeHost.GetHostInfov1")
            # ----------------------------------------------------------------------------------------------------------
            ChangeHostTestUtils.HIDppHelper.get_host_info(
                self, device_index=ChannelUtils.get_device_index(test_case=self))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCookie with  hostIndex=0 and cookie=0x11")
            # ----------------------------------------------------------------------------------------------------------
            ChangeHostTestUtils.HIDppHelper.set_cookie(
                self, host_index=0, cookie=0x11, device_index=ChannelUtils.get_device_index(test_case=self))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ChangeHost.GetCookies")
            # ----------------------------------------------------------------------------------------------------------
            ChangeHostTestUtils.HIDppHelper.get_cookies(
                self, device_index=ChannelUtils.get_device_index(test_case=self))
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Check if the Hosts Info feature is supported by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        feature_1815_index, _, _, _ = HostsInfoTestUtils.HIDppHelper.get_parameters(self, skip_not_found=True)

        if feature_1815_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostInfo request with host index = 0xFF')
            # ----------------------------------------------------------------------------------------------------------
            HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0xFF)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable Manufacturing Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Check if the Battery Levels Calibration feature is supported by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        feature_1861_index, _, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
            self, BatteryLevelsCalibration.FEATURE_ID, BatteryLevelsCalibrationFactory, skip_not_found=True)

        if feature_1861_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enable cutoff')
            # ----------------------------------------------------------------------------------------------------------
            BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
                self, cutoff_change_state_requested=True, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_ENABLE,
                state_to_check=BatteryLevelsCalibration.CUTOFF_ENABLE)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Check if the 0x1982 Backlight feature is supported by the DUT')
        # --------------------------------------------------------------------------------------------------------------
        feature_1982_index, feature_1982, device_index, _ = BacklightTestUtils.HIDppHelper.get_parameters(
            self, skip_not_found=True)

        if feature_1982_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetBacklightConfig request')
            # ----------------------------------------------------------------------------------------------------------
            BacklightTestUtils.HIDppHelper.get_backlight_config(self)
        # end if

        if self.f.SHARED.PAIRING.F_BLEDevicePairing:
            self.post_requisite_reload_nvs = True

            # Cleanup all receiver pairing slots except the first one
            DevicePairingTestUtils.unpair_all(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Run a user pairing sequence')
            # ----------------------------------------------------------------------------------------------------------
            ble_addr = DiscoveryTestUtils.discover_device(self)
            pairing_slot = DevicePairingTestUtils.pair_device(self, ble_addr)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Unpair the last slot')
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, pairing_slot=pairing_slot)
        # end if
    # end def execute_scenario
# end class DeviceStackTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
