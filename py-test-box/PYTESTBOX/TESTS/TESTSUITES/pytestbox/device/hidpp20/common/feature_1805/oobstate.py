#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1805.oobstate
:brief: Validate HID++ 2.0 ``OobState`` feature
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2022/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pylibrary.emulator.ledid import CONNECTIVITY_STATUS_LEDS
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.oobstateutils import OobStateTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobStateTestCase(DeviceBaseTestCase):
    """
    Validate ``OobState`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        self.post_requisite_clean_pairing_data = False
        self.post_requisite_cutoff = False
        self.post_requisite_reload_nvs = False
        self.post_requisite_unplug_usb_cable = False
        self.post_requisite_pair_device = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1805 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1805_index, self.feature_1805, _, _ = OobStateTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.OOB_STATE
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_kosmos_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Stop LEDs monitoring')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(
                self, led_identifiers=CONNECTIVITY_STATUS_LEDS, build_timeline=False)
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_clean_pairing_data:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean pairing data")
                # ------------------------------------------------------------------------------------------------------
                # Cleanup all pairing slots except the first one
                DevicePairingTestUtils.unpair_all(self)
                self.post_requisite_clean_pairing_data = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_unplug_usb_cable:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Power OFF the USB cable and switch to the receiver channel')
                # ------------------------------------------------------------------------------------------------------
                ProtocolManagerUtils.exit_usb_channel(test_case=self)
                self.post_requisite_unplug_usb_cable = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.f.PRODUCT.F_IsGaming and self.post_requisite_pair_device:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Pair DUT with EQuad Receiver')
                # ------------------------------------------------------------------------------------------------------
                if (not isinstance(self.current_channel, ThroughEQuadReceiverChannel)
                        and isinstance(self.backup_dut_channel, ThroughEQuadReceiverChannel)):
                    self.current_channel = self.backup_dut_channel
                # end if
                OobStateTestUtils.pair_equad_device(self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_cutoff:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Enable cutoff')
                # ------------------------------------------------------------------------------------------------------
                BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
                    self, cutoff_change_state_requested=True,
                    cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_ENABLE,
                    state_to_check=BatteryLevelsCalibration.CUTOFF_ENABLE)
                self.post_requisite_cutoff = False
            # end if
        # end with

        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Clean Battery Notification Status Event")
            # ----------------------------------------------------------------------------------------------------------
            self.cleanup_battery_event_from_queue()
        # end with

        super().tearDown()
    # end def tearDown
# end class OobStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
