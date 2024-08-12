#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.recovery.recovery
:brief: Validate device Recovery feature
:author: YY Liu <yliu5@logitech.com>
:date: 2024/01/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import time

from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.recovery.recovery import SharedCommonRecoveryTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceRecoveryTestCase(SharedCommonRecoveryTestCase, DeviceBaseTestCase):
    """
    Recovery TestCase class
    """
    HID_PP_TIMEOUT = 300  # 130
    TIME_MARGIN = 10

    def _complete_dfu_business(self, pairing, soft_device=False):
        """
        Execute the DFU process business case in recovery mode

        :param pairing: Flag to perform pairing after connection.
        :type pairing: ``bool``
        :param soft_device: Flag indicating whether the SoftDevice should be updated in addition to the
                            application. - OPTIONAL
        :type soft_device: ``bool``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Jump on recovery bootloader and connect {"with" if pairing else "without"} pairing')
        # --------------------------------------------------------------------------------------------------------------
        self._device_jump_on_recovery_bootloader(pairing=pairing)

        if soft_device:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform Soft Device DFU')
            # ----------------------------------------------------------------------------------------------------------
            self._perform_sd_and_app_dfu()
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform DFU')
            # ----------------------------------------------------------------------------------------------------------
            self._perform_dfu()
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Device shall be in Main Application mode')
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(expr=self._check_device_on_application(), msg="Target not on Application")
    # end def complete_dfu_business

    def _get_current_consumption(self):
        """
        Get the current consumption of the DUT
        """
        # The debugger will affect the current measurement result, shall close it before doing test!
        if self.debugger:
            self.debugger.close()
        # end if
        # Shall disconnect to J-Link before doing current measurement
        self.jlink_connection_control.disconnect()
        self.power_supply_emulator.configure_measurement_mode("current")
        current_sum = 0
        loop_counter = 150
        time.sleep(60)
        for _ in range(loop_counter):
            current_sum += self.power_supply_emulator.get_current() * 1000
            time.sleep(.2)
        # end for
        current_value = current_sum // loop_counter
        self.power_supply_emulator.configure_measurement_mode("tension")
        self.jlink_connection_control.connect()

        return current_value
    # end def _get_current_consumption
# end class RecoveryTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
