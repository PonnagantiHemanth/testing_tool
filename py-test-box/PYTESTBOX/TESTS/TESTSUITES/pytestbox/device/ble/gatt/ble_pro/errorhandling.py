#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.ble_pro.errorhandling
:brief: Validate Gatt Ble Pro services error handling test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/08/31
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from copy import deepcopy

from pychannel import blechannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.logiconstants import LogitechVendorUuid
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleUuid


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattBleProErrorHandlingTestCaseMixin(DeviceBaseTestCase):
    """
    GATT BLE PRO Service Error Handling Test Cases Common class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_backup_nvs = False
        self.post_requisite_restart_in_main_application = False
        self.current_ble_device = None
        self.ble_context = None
        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        self.memory_manager.backup_nvs_parser = deepcopy(self.memory_manager.nvs_parser)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_restart_in_main_application:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Restart in Main Application mode")
                # ------------------------------------------------------------------------------------------------------
                DfuTestUtils.force_target_on_application(self, check_required=False)

                self.post_requisite_restart_in_main_application = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_backup_nvs:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(test_case=self)
                ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self, channel=self.backup_dut_channel)
                self.post_requisite_backup_nvs = False
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_ble_device is not None:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Delete bond from direct BLE device")
                # ------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.current_ble_device)
            # end if
        # end with

        with self.manage_post_requisite():
            LogHelper.log_post_requisite(self, "Clean WirelessDeviceStatusBroadcastEvent messages")
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with

        super().tearDown()
    # end def tearDown

    def _generic_test_ble_pro_security(self):
        """
        Validate the security level of the ble pro service
        """
        service_uuid = BleUuid(BleUuidStandardService.LOGITECH_BLE_PRO)

        characteristic_uuid = BleProtocolTestUtils.build_128_bits_uuid(
            LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CONTROL_CHARACTERISTIC)
        service = self.ble_context.get_service(ble_context_device=self.ble_context_device_used, uuid=service_uuid)
        characteristics = service.get_characteristics(characteristic_uuid=characteristic_uuid)
        if len(characteristics) == 1:
            BleProtocolTestUtils.check_write_permission(self, service_uuid, characteristic_uuid,
                                                        HexList("00000000"))
        # end if
    # end def _generic_test_ble_pro_security
# end class GattBleProErrorHandlingTestCaseMixin


class GattBleProApplicationErrorHandlingTestCase(GattBleProErrorHandlingTestCaseMixin):
    """
    GATT BLE PRO Service Error Handling Test Cases in application class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disconnect by entering pairing mode")
        # ------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        self.post_requisite_backup_nvs = True

        DeviceBaseTestUtils.enter_pairing_mode_ble(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Connect to the device without the authentication")
        # --------------------------------------------------------------------------------------------------------------
        self.current_ble_device = BleProtocolTestUtils.scan_for_current_device(self,
                                                                               scan_timeout=2,
                                                                               send_scan_request=True)
        self.ble_context = BleProtocolTestUtils.get_ble_context(self)
        self.ble_context_device_used = self.current_ble_device
        BleProtocolTestUtils.connect_no_encryption(test_case=self, ble_context_device=self.ble_context_device_used)
    # end def setup

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_ble_pro_security(self):
        """
        Validate the security level of the ble pro service
        """
        self._generic_test_ble_pro_security()

        self.testCaseChecked("ERR_GATT_BLE_PRO_0001", _AUTHOR)
    # end def test_ble_pro_security
# end class GattBleProApplicationErrorHandlingTestCase


class GattBleProBootloaderErrorHandlingTestCase(GattBleProErrorHandlingTestCaseMixin):
    """
    GATT BLE PRO Service Error Handling Test Cases in application class
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enter bootloader mode, without automatic reconnection")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_restart_in_main_application = True
        self.post_requisite_backup_nvs = True

        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=False)
        self.debugger.stop()
        ChannelUtils.wait_usb_ble_channel_connection_state(
            test_case=self, channel=self.current_channel, connection_state=False)
        self.debugger.run()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Connect to the device without the authentication")
        # --------------------------------------------------------------------------------------------------------------
        self.current_ble_device = self.current_channel.get_ble_context_device()
        self.ble_context = BleProtocolTestUtils.get_ble_context(self)
        self.ble_context_device_used = self.current_ble_device
        BleProtocolTestUtils.connect_no_encryption(test_case=self, ble_context_device=self.ble_context_device_used)
    # end def setUp

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_ble_pro_security(self):
        """
        Validate the security level of the ble pro service
        """
        self._generic_test_ble_pro_security()

        self.testCaseChecked("ERR_GATT_BLE_PRO_0002", _AUTHOR)
    # end def test_ble_pro_security
# end class GattBleProBootloaderErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
