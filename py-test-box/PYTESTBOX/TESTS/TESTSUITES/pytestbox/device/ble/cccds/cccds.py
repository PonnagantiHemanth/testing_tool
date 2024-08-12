#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.osdetection.osdetection
:brief: Validate BLE CCCDs toggling test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/09/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.enablehidden import EnableHidden
from pylibrary.mcu.nrf52.blesysattrchunks import DeviceBleUserServices
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.ble.base.bleppserviceutils import BleppServiceUtils
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.bleinterfaceclasses import BleUuid


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleppCccdToggledTestCases(DeviceBaseTestCase):
    """
    BLE CCCDs toggling Test Cases class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_reload_nvs = False
        self.blepp_time_stamped_msg_queue = None
        self.ble_context = None

        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        self.memory_manager.read_nvs()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1D4B)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=WirelessDeviceStatus.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1E00)')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(test_case=self, feature_id=EnableHidden.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1004)')
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_1004, _, _ = UnifiedBatteryTestUtils.HIDppHelper.get_parameters(self)

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Check the BLE++ CCCD is disabled by default")
        # ------------------------------------------------------------------------
        self.ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
        characteristic = BleppServiceUtils.get_blepp_characteristic(test_case=self)
        blepp_cccd_descriptor = self.ble_context.attribute_read(
            ble_context_device=self.ble_context_device_used, attribute=characteristic.get_descriptors(
                descriptor_uuid=BleUuid(value=BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION))[0])
        if to_int(blepp_cccd_descriptor.data) != DeviceBleUserServices.CCCD.NOTIFICATION.DISABLED:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Disable BLE++ service CCCD")
            # ----------------------------------------------------------------------------------------------------------
            BleppServiceUtils.configure_blepp_cccds(test_case=self, enabled=False)
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload device initial NVS i.e. disable BLE++ CCCD")
                # ------------------------------------------------------
                self.memory_manager.load_nvs(backup=True)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown
# end class BleppCccdToggledTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
