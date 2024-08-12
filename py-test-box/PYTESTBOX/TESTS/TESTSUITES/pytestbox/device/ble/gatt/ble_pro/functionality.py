#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.ble_pro.interface
:brief: Validate Gatt Ble Pro services Functionality test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/06/29
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import queue
from copy import deepcopy
from time import perf_counter_ns

from pychannel.logiconstants import BleProAuthenticationValues
from pychannel.logiconstants import LogitechVendorUuid
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.threadutils import QueueWithEvents
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import ReportReferences
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.ble.gatt.ble_pro.ble_pro import GattBleProApplicationTestCase
from pytestbox.device.ble.gatt.ble_pro.ble_pro import attribute_value_format
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceTestCase
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.blecontext import BleContext
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.transportcontext import TransportContextException

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


MIN_DELAY = 100e6

BLE_PRO_SERVICE_UUID = BleUuid(BleUuidStandardService.LOGITECH_BLE_PRO)
ATTRIBUTE_CAPABILITY_UUID = BleProtocolTestUtils.build_128_bits_uuid(
    LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CAPABILITY_CHARACTERISTIC)
ATTRIBUTE_CONTROL_UUID = BleProtocolTestUtils.build_128_bits_uuid(
    LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CONTROL_CHARACTERISTIC)
AUTHENTICATION_CAPABILITIES_CHARACTERISTIC_UUID = BleProtocolTestUtils.build_128_bits_uuid(
    LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CAPABILITIES_CHARACTERISTIC)
AUTHENTICATION_CONTROL_CHARACTERISTIC_UUID = BleProtocolTestUtils.build_128_bits_uuid(
    LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CONTROL_CHARACTERISTIC)

SUPPRESSION_ENABLED_VALUE = attribute_value_format(suppressed_latency=True)
SUPPRESSION_DISABLED_VALUE = attribute_value_format(suppressed_latency=False)


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattBleProApplicationFunctionalityTestCase(GattBleProApplicationTestCase):
    """
    Gatt Small Services Application mode Functionality Test Cases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.notification_queue = QueueWithEvents()
        super().setUp()
    # end def setUp

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @features('BLELatencyRemoval')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_hid_report_delay(self):
        """
        Verify that writes on BLE Pro Attribute Control characteristic the suppression of the delay on first hid report
        """
        self.ble_context: BleContext

        report = self._key_and_report_prerequisite()

        self.ble_context.update_notification_queue(ble_context_device=self.current_ble_device, characteristic=report,
                                                   time_stamped_queue=self.notification_queue)

        self._check_capabilities()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set device to ignore delay on sending HID reports "
                                 "by writing on BLE Pro Attribute characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=BLE_PRO_SERVICE_UUID,
                                                  characteristic_uuid=ATTRIBUTE_CONTROL_UUID,
                                                  value=SUPPRESSION_ENABLED_VALUE)
        # TODO: When https://jira.logitech.io/browse/NRF52-494 is fixed, invert the test methods
        #       so to verify before disconnecting-reconnecting
        self._hid_delay_test_on_connection(suppressed=True)

        self._hid_delay_test_on_cccd_write(report, suppressed=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set device to have delay on sending HID reports "
                                 "by writing on BLE Pro Attribute characteristic")
        # --------------------------------------------------------------------------------------------------------------

        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=BLE_PRO_SERVICE_UUID,
                                                  characteristic_uuid=ATTRIBUTE_CONTROL_UUID,
                                                  value=SUPPRESSION_DISABLED_VALUE)
        # TODO: When https://jira.logitech.io/browse/NRF52-494 is fixed, invert the test methods
        #       so to verify before disconnecting-reconnecting
        self._hid_delay_test_on_connection(suppressed=False)

        self._hid_delay_test_on_cccd_write(report, suppressed=False)

        self.testCaseChecked("FUN_GATT_BLE_PRO_0001", _AUTHOR)
    # end def test_hid_report_delay

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @features('BLELatencyRemoval')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_hid_report_delay_persistent_with_reset(self):
        """
        Verify that writes on BLE Pro Attributes Control characteristic are persistent with reset
        """
        report = self._key_and_report_prerequisite()

        self._check_capabilities()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set device to ignore delay on sending HID reports "
                                 "by writing on BLE Pro Attribute characteristic")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=BLE_PRO_SERVICE_UUID,
                                                  characteristic_uuid=ATTRIBUTE_CONTROL_UUID,
                                                  value=SUPPRESSION_ENABLED_VALUE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self, delay=2.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reconnect to the device")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_and_bond_device(self, self.current_ble_device)

        self._hid_delay_test_on_cccd_write(report, suppressed=True)

        self.testCaseChecked("FUN_GATT_BLE_PRO_0002", _AUTHOR)
    # end def test_hid_report_delay_persistent_with_reset

    def _key_and_report_prerequisite(self):
        """
        Return the report characteristic user actions will be received on
        :return: the corresponding ble characteristic
        :rtype: ``BleCharacteristic``
        """
        if self.f.PRODUCT.F_IsPlatform:
            report_id = ReportReferences.MOUSE_INPUT  # platforms send a mouse report on user action
        elif self.f.PRODUCT.F_IsGaming:
            report_id = ReportReferences.GAMING_KEYBOARD_INPUT
        else:
            report_id = ReportReferences.KEYBOARD_INPUT
        # end if
        return BleProtocolTestUtils.get_hid_report(self,
                                                   gatt_table=self.ble_context.get_gatt_table(self.current_ble_device),
                                                   current_ble_device=self.current_ble_device,
                                                   report_reference=report_id)
    # end def _key_and_report_prerequisite

    def _check_capabilities(self):
        """
        Verify that the device advertise the HID first report delay suppression in its capability
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read capability")
        # --------------------------------------------------------------------------------------------------------------
        capabilities = BleProtocolTestUtils.read_characteristics(
            self, self.current_ble_device, service_uuid=BLE_PRO_SERVICE_UUID,
            characteristic_uuid=ATTRIBUTE_CAPABILITY_UUID)[0].data
        suppression_capability = capabilities & SUPPRESSION_ENABLED_VALUE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device has the necessary capability")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=SUPPRESSION_ENABLED_VALUE, obtained=suppression_capability,
                         msg="Suppressing first report latency not supported")
    # end def _check_capabilities

    def _hid_delay_test_on_cccd_write(self, report, suppressed):
        """
        Perform a test on the presence of hid report after writing on the CCCDs

        :param report: The report characteristic the notification will be received on
        :type report: ``BleCharacteristic``
        :param suppressed: Flag indicating if the delay is expected to be suppressed
        :type suppressed: ``bool``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable notification")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.disable_notification(ble_context_device=self.current_ble_device, characteristic=report)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable notification, press a key, timing the delay between press and reception")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.enable_notification(ble_context_device=self.current_ble_device, characteristic=report,
                                             time_stamped_queue=self.notification_queue)
        self._timing_test(delay_present=not suppressed)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press a key, timing the delay between press and reception")
        # --------------------------------------------------------------------------------------------------------------
        self._timing_test(delay_present=False)
    # end def _hid_delay_test_on_cccd_write
    
    def _hid_delay_test_on_connection(self, suppressed):
        """
        Perform a test on the presence of hid report after reconnection

        :param suppressed: Flag indicating if the delay is expected to be suppressed
        :type suppressed: ``bool``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disconnect and reconnect, press a key, timing the delay between press and reception")
        # --------------------------------------------------------------------------------------------------------------
        self._disconnect_reconnect()

        self._timing_test(delay_present=not suppressed)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press a key, timing the delay between press and reception")
        # --------------------------------------------------------------------------------------------------------------
        self._timing_test(delay_present=False)
    # end def _hid_delay_test_on_connection
    
    def _timing_test(self, delay_present=True, delay=MIN_DELAY):
        """
        Perform the timing test

        :param delay_present: Flag indicating if the delay should be present
        :type delay_present: ``bool``
        :param delay: length of the delay in ns
        :type delay: ``int``
        """
        timestamp_notification = perf_counter_ns()
        self.button_stimuli_emulator.user_action()
        notification = self.notification_queue.get(timeout=5)
        delta_time = notification.timestamp - timestamp_notification
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Delta time {delta_time / 1e6}ms")
        # --------------------------------------------------------------------------------------------------------------
        if delay_present:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the delay is present")
            # ----------------------------------------------------------------------------------------------------------

            self.assertGreater(delta_time, delay, msg=f"Delay not present when it should be, {delta_time / 1e6:.1f}ms "
                                                      f"should be less than {delay / 1e6:.1f}ms")
        else:

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the delay is not present")
            # ----------------------------------------------------------------------------------------------------------
            self.assertLess(delta_time, MIN_DELAY, msg=f"Delay present when it should be, {delta_time / 1e6:.1f}ms "
                                                       f"should be less than {delay / 1e6:.1f}ms")
        # end if
        self._clear_queue()
    # end def _timing_test

    def _disconnect_reconnect(self):
        """
        Disconnect and reconnect to the device
        """
        BleProtocolTestUtils.disconnect_device(self, self.current_ble_device)
        self.button_stimuli_emulator.user_action()
        BleProtocolTestUtils.connect_and_bond_device(self, self.current_ble_device)
    # end def _disconnect_reconnect

    def _clear_queue(self):
        """
        Clear notification queue of any potential messages already received
        """
        emptied = False
        while not emptied:
            try:
                self.notification_queue.get_nowait()
            except queue.Empty:
                emptied = True
            # end try
        # end while
    # end def _clear_queue
# end class GattBleProApplicationFunctionalityTestCase


class GattBleProApplicationFunctionalityPairingTestCase(GattSmallServiceTestCase):
    """
    Gatt Small Services Application mode Pairing Functionality Test Cases
    """
    PROTOCOL_TO_CHANGE_TO = None

    def setUp(self):
        """
        Handle test prerequisite
        """
        super().setUp()

        self.post_requisite_reload_nvs = True
        self.post_requisite_backup_nvs = True
        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        self.memory_manager.backup_nvs_parser = deepcopy(self.memory_manager.nvs_parser)

        BleProtocolTestUtils.enter_pairing_mode_ble(self),

        self.current_ble_device = BleProtocolTestUtils.scan_for_current_device(test_case=self, scan_timeout=2,
                                                                               send_scan_request=False)
    # end def setUp

    def _generic_test_authentication_required(self, authentication_method_required):
        """
        verify that the DUT properly enforce authentication requirements

        :param authentication_method_required: The authentication method to enforce, value of
            the control point characteristic
        :type authentication_method_required: ``BleProAuthenticationValues``
        """
        self.ble_context: BleContext

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to device without encrypting")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_no_encryption(test_case=self, ble_context_device=self.current_ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read capability")
        # --------------------------------------------------------------------------------------------------------------
        capabilities = BleProtocolTestUtils.read_characteristics(
            self, self.current_ble_device, service_uuid=BLE_PRO_SERVICE_UUID,
            characteristic_uuid=AUTHENTICATION_CAPABILITIES_CHARACTERISTIC_UUID)[0].data

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"ble pro authentication capabilities: {capabilities}")
        LogHelper.log_check(self, "Check authentication capability is supported")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEquals(obtained=capabilities & authentication_method_required, unexpected=0,
                             msg="Authentication method not supported in capabilities")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set authentication method to 0x{authentication_method_required}")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=BLE_PRO_SERVICE_UUID,
                                                  characteristic_uuid=BleProtocolTestUtils.build_128_bits_uuid(
                                                      LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CONTROL_CHARACTERISTIC),
                                                  value=HexList(authentication_method_required))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Attempt authentication using just work")
        # --------------------------------------------------------------------------------------------------------------
        try:
            self.ble_context.authenticate_just_works(self.current_ble_device)
            # fail the test if no exception was raised
            self.fail("authenticate just work was accepted by DUT")
        except TransportContextException as e:
            if e.get_cause() == TransportContextException.Cause.AUTHENTICATION_FAILED:
                pass
            else:
                raise
            # end if
        # end try
    # end def _generic_test_authentication_required

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @features('PasskeyAuthenticationMethod')
    @level('Functionality')
    @services('BleContext')
    def test_authentication_enforcement_passkey(self):
        """
        Verify that requiring authentication by passkey is enforced
        """
        self._generic_test_authentication_required(
            authentication_method_required=BleProAuthenticationValues.KEYBOARD_PASSKEY)
    # end def test_authentication_enforcement_passkey

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @features('Passkey2ButtonsAuthenticationMethod')
    @level('Functionality')
    @services('BleContext')
    def test_authentication_enforcement_2buttons(self):
        """
        Verify that requiring authentication by 2 button passkey is enforced
        """
        self._generic_test_authentication_required(
            authentication_method_required=BleProAuthenticationValues.TWO_BUTTONS_PASSKEY)
    # end def test_authentication_enforcement_2buttons

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @level('Functionality')
    @services('BleContext')
    def test_no_authentication_enforcement(self):
        """
        Verify that requiring no authentication  method is indeed not enforced
        """
        self.ble_context: BleContext

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to device without encrypting")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.connect_no_encryption(test_case=self, ble_context_device=self.current_ble_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set authentication method to not require any")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.write_characteristic(test_case=self,
                                                  ble_context_device=self.current_ble_device,
                                                  service_uuid=BLE_PRO_SERVICE_UUID,
                                                  characteristic_uuid=AUTHENTICATION_CONTROL_CHARACTERISTIC_UUID,
                                                  value=HexList(BleProAuthenticationValues.NO_AUTHENTICATION))
        try:
            self.ble_context.authenticate_just_works(self.current_ble_device)
        except TransportContextException as e:
            if e.get_cause() == TransportContextException.Cause.AUTHENTICATION_FAILED:
                self.fail("authenticate just work was not accepted by DUT")
            else:
                raise
            # end if
        # end try
    # end def test_no_authentication_enforcement

# end class GattBleProApplicationFunctionalityPairingTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
