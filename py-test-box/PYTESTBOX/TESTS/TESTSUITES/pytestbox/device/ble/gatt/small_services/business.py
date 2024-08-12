#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.small_services.business
:brief: Validate Gatt small services Business test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2022/07/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import queue
from time import perf_counter_ns

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.logiconstants import LogitechVendorUuid
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceApplicationTestCase
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceBootloaderTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattSmallServicesApplicationBusinessTestCase(GattSmallServiceApplicationTestCase):
    """
    Gatt Small Services Application mode Business Test Cases
    """

    @features('BLEProtocol')
    @features('Feature0003')
    @level('Business', 'SmokeTests')
    @services('BleContext')
    @services('Debugger')
    def test_gatt_table_application(self):
        """
        Verify the gatt table in application mode
        """
        self._get_feature_0003_index()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the whole GATT table")
        # --------------------------------------------------------------------------------------------------------------
        gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)
        self._subscribe_to_all(gatt_table)

        self._check_hidpp_communication_enabled(
            blepp_service=BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_SERVICE),
            hidpp_characteristic=BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_CHARACTERISTIC)
        )

        self._check_gatt_table_attribute_presence(gatt_table)

        self.testCaseChecked("BUS_BLE_GATT_SSRV_0001", author=_AUTHOR)
    # end def test_gatt_table_application
# end class GattSmallServicesApplicationBusinessTestCase


@features.class_decorator("BootloaderBLESupport")
class GattSmallServicesBootloaderBusinessTestCase(GattSmallServiceBootloaderTestCase):
    """
    Gatt Small Services Bootloader mode Business Test Cases
    """

    @features('BLEProtocol')
    @features('Feature0003')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_gatt_table_bootloader(self):
        """
        Verify the gatt table in bootloader mode
        """
        self._get_feature_0003_index()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the whole GATT table")
        # --------------------------------------------------------------------------------------------------------------
        gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)

        self._subscribe_to_all(gatt_table)

        self._check_hidpp_communication_enabled(
            blepp_service=BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BOOTLOADER_SERVICE),
            hidpp_characteristic=BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BOOTLOADER_CHARACTERISTIC)
        )

        self._check_gatt_table_attribute_presence(gatt_table)

        self.testCaseChecked("BUS_BLE_GATT_SSRV_0002", author=_AUTHOR)
    # end def test_gatt_table_bootloader
# end class GattSmallServicesBootloaderBusinessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
