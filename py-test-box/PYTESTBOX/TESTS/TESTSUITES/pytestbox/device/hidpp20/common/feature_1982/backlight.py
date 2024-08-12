#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1982.backlight
:brief: Validate HID++ 2.0 ``Backlight`` feature
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pylibrary.emulator.ledid import LED_ID
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightTestCase(DeviceBaseTestCase):
    """
    Validate ``Backlight`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        self.post_requisite_disable_recharge = False
        self.post_requisite_restore_default_luminance_value = False
        self.post_requisite_clean_pairing_data = False
        self.post_requisite_unplug_usb_charging_cable = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Delete backlight chunk")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.delete_backlight_chunk(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)
        CommonBaseTestUtils.verify_wireless_device_status_broadcast_event_reconnection(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1982 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1982_index, self.feature_1982, _, _ = BacklightTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Wait power led turned off")
        # --------------------------------------------------------------------------------------------------------------
        # Some product turn on ALS sensor after Power LED timeout
        sleep(BacklightTestUtils.POWER_LED_TIMEOUT)

        self.config = self.f.PRODUCT.FEATURES.COMMON.BACKLIGHT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Clean-up any Battery Status event")
        # --------------------------------------------------------------------------------------------------------------
        self.cleanup_battery_event_from_queue()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            if self.post_requisite_unplug_usb_charging_cable:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Unplug USB charging cable")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.ChargingHelper.exit_charging_mode(self)

                self.post_requisite_unplug_usb_charging_cable = False
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_clean_pairing_data:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean pairing data")
                # ------------------------------------------------------------------------------------------------------
                # Cleanup all pairing slots except the first one
                DevicePairingTestUtils.NvsManager.clean_pairing_data(self)

                self.post_requisite_clean_pairing_data = False
            # end if
        # end with
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                # To make sure no backlight up/down be pressed before restored NVS
                self.button_stimuli_emulator.release_all()

                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_disable_recharge:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Disable recharge feature")
                # ------------------------------------------------------------------------------------------------------
                self.device.turn_off_usb_charging_cable()
                self.power_supply_emulator.recharge(False)
                self.post_requisite_disable_recharge = False
            # end if
        # end with
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_restore_default_luminance_value:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Set ALS to default value by ALS emulator")
                # ------------------------------------------------------------------------------------------------------
                self.ambient_light_sensor_emulator.set_ambient_light_intensity()
                self.post_requisite_restore_default_luminance_value = False
            # end if
        # end with
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Stop proximity sensor enable signal monitoring')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(
                self, led_identifiers=[LED_ID.PROXIMITY_SENSOR_ENABLED], build_timeline=False)
        # end with
        super().tearDown()
    # end def tearDown

    @staticmethod
    def _sort_sequence_by_delay(sequence):
        """
        Sort a sequence composed of ``MAKE`` and ``BREAK`` with timestamp to a sequence composed of ``MAKE`` and ``BREAK``
        with a delay between two consecutive actions in order to be used by button_stimuli_emulator class.

        :param sequence: List of ``KEY_ID`` and its list of action name (make or break) with timestamp
        :type sequence: ``list[KEY_ID, list[tuple(str, float)]]``

         :return: tuple(sequence_sorted_by_delay, maximum_timestamp)  with the list of action with ``KEY_ID``,
                  action name (make or break) and delay between two consecutive actions and the maximum timestamp of
                  the sequence.
        :rtype: ``tuple(list[tuple[KEY_ID, str, float]], float)``
        """
        sequence_sorted = []
        for key_id_sequence in sequence:
            for action in key_id_sequence[1]:
                sequence_sorted.append((key_id_sequence[0], action[0], action[1]))
            # end for
        # end for
        sequence_sorted.sort(key=lambda x: x[2])
        maximum_timestamp = sequence_sorted[-1][2]

        sequence_sorted_by_delay = sequence_sorted.copy()
        for i in range(1, len(sequence_sorted)):
            delay = sequence_sorted[i][2] - sequence_sorted[i - 1][2]
            # for rounding error
            delay = 0 if delay < 10 ** -8 else delay
            sequence_sorted_by_delay[i] = (sequence_sorted[i][0],
                                           sequence_sorted[i][1],
                                           delay)
        # end for
        return sequence_sorted_by_delay, maximum_timestamp
    # end def _sort_sequence_by_delay
# end class BacklightTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
