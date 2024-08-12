#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.connection_parameters.connectionparameters
:brief: Validate BLE connection parameters test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/09/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import WarningLevel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleconnectionparametersutils import BleConnectionParametersTestUtils
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.ble.bleconstants import BleContextEventType
from pytransport.ble.blecontext import BleContextDevice


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConnectionParametersTestCases(DeviceBaseTestCase):
    """
    BLE connection parameters Test Cases class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_reload_nvs = False
        self.post_requisite_reset_os_emulation = False
        self.post_requisite_restart_in_main_application = False
        self.previous_devices_to_delete_bond = []
        self.ble_context = None
        self.current_device = None
        self.ble_channel = None

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Get the BLE context here to do the sanity checks sooner")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        DeviceBaseTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enter pairing mode")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ChannelUtils.close_channel(test_case=self)
        DeviceBaseTestUtils.enter_pairing_mode_ble(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Scan for current device")
        # --------------------------------------------------------------------------------------------------------------
        self.current_device = BleProtocolTestUtils.scan_for_current_device(
            test_case=self, scan_timeout=2, send_scan_request=True)
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
            if self.ble_channel is not None:
                if self.ble_channel.is_open:
                    # ------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Close BLE channel")
                    # ------------------------------------------------------
                    self.ble_channel.close()
                # end if
                self.ble_channel = None
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_device is not None and self.current_device.connected:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Disconnect device")
                # ------------------------------------------------------
                BleProtocolTestUtils.disconnect_device(test_case=self, ble_context_device=self.current_device)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.current_device is not None:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Delete device bond")
                # ------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=self.current_device)
                self.current_device = None
            # end if
        # end with

        with self.manage_post_requisite():
            for previous_device in self.previous_devices_to_delete_bond:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, f"Delete device bond of {previous_device}")
                # ------------------------------------------------------
                BleProtocolTestUtils.delete_device_bond(test_case=self, ble_context_device=previous_device)
            # end for
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload device initial NVS")
                # ------------------------------------------------------
                self.memory_manager.load_nvs(backup=True)
                ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)
                # There is an extra event that happen before the end of the method
                # wait_for_channel_device_to_be_connected, so we need to wait for both events
                for _ in range(2):
                    ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                          class_type=WirelessDeviceStatusBroadcastEvent, timeout=1,
                                          check_first_message=False, allow_no_message=True)
                # end for
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        with self.manage_post_requisite():
            if self.ble_context is not None and self.ble_context.connection_parameters_range is not None:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "reset host connection parameter range")
                # ------------------------------------------------------
                self.ble_context.connection_parameters_range = None
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reset_os_emulation:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reset host GATT table")
                # ------------------------------------------------------
                BleProtocolTestUtils.get_ble_context(test_case=self).reset_central_gatt_table()
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def _clear_events_and_log_them(self):
        """
        Clear all previous L2CAP Connection Parameters Update Request events and log them as robustness warning
        """
        # Adding type hint does not add overhead and greatly helps the indexer
        self.current_device: BleContextDevice

        queue = self.current_device.ble_context_event_queue
        previous_events = queue.clear_all_events_of_a_type(
                event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST) + \
            queue.clear_all_events_of_a_type(
                event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT) + \
            queue.clear_all_events_of_a_type(
                event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_COMPLETED)
        if len(previous_events) > 0:
            for event in previous_events:
                self.log_warning(message=f"Received even prior to the test: {event}",
                                 warning_level=WarningLevel.ROBUSTNESS)
            # end for
        # end if
    # end def _clear_events_and_log_them

    # end class ConnectionParametersTestCases

    def _generic_test_correct_connection_parameters(
            self, correct_parameters, connection_parameters, one_request_present=False):
        """
        Generic method for tests.

        :param correct_parameters: Flag indicating that the parameters are incorrect or not
        :type correct_parameters: ``bool``
        :param connection_parameters: The connection parameters to use
        :type connection_parameters: ``BleGapConnectionParameters``
        :param one_request_present: Flag indicating that one change request should be received. It is only relevant
                                    if ``correct_parameters`` is ``True`` - OPTIONAL
        :type one_request_present: ``bool``
        """
        # Adding type hint does not add overhead and greatly helps the indexer
        self.current_device: BleContextDevice

        log_str = "expected" if correct_parameters else "unexpected"
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Connect and bond to device with the {log_str} connection parameters")
        # --------------------------------------------------------------------------------------------------------------
        # Clear the events before the connection
        self._clear_events_and_log_them()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Connection parameters = {connection_parameters}")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_channel = BleProtocolTestUtils.create_new_ble_channel(
            test_case=self, ble_context_device=self.current_device, connection_parameters=connection_parameters)

        if correct_parameters:
            if one_request_present:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, "Check that one Connection Parameters Update Request is received (timeout 2s)")
                # ------------------------------------------------------------------------------------------------------
                update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
                    event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=2,
                    skip_error=True)
                self.assertNotNone(obtained=update_request_event,
                                   msg="Connection Parameters Update Request not received after bonding while it "
                                       f"should have.\nParameters used: {connection_parameters}")

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check that no Connection Parameters Update Request is received after the "
                                          "first one (timeout 30s)")
                # ------------------------------------------------------------------------------------------------------
                update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
                    event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=30,
                    skip_error=True)
                self.assertNone(obtained=update_request_event,
                                msg="Connection Parameters Update Request received after bonding while it should "
                                    f"not have.\nParameters used: {connection_parameters}\n")
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check that no Connection Parameters Update Request is received (timeout 2s)")
                # ------------------------------------------------------------------------------------------------------
                update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
                    event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=2,
                    skip_error=True)
                self.assertNone(obtained=update_request_event,
                                msg="Connection Parameters Update Request received after bonding while it should not "
                                    f"have.\nParameters used: {connection_parameters}")
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send a HID++ request (root feature 0x0000)")
            LogHelper.log_check(self, "Check that a response is received")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.update_feature_mapping(
                test_case=self, feature_id=DeviceInformation.FEATURE_ID, channel=self.ble_channel)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that a Connection Parameters Update Request is received (timeout 2s)")
            # ----------------------------------------------------------------------------------------------------------
            update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
                event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=2,
                skip_error=True)
            self.assertNotNone(obtained=update_request_event,
                               msg="Connection Parameters Update Request not received after bonding while it "
                                   f"should have.\nParameters used: {connection_parameters}")
        # end if

    # end def _generic_test_correct_connection_parameters

    def _generic_looped_test_correct_connection_parameters(self, connection_parameters_list, first_connection=False,
                                                           one_request_present=False, bootloader=False,
                                                           first_iteration=True):
        """
        Generic method for looping multiple correct connection parameter test.

        :param connection_parameters_list: list of connection parameter in the acceptable or extended range
        :type connection_parameters_list: ``list[BleGapConnectionParameters]``
        :param first_connection: Flag indicating if the device need to re-pair each loop - OPTIONAL
        :type first_connection: ``bool``
        :param one_request_present: Flag indicating that one change request should be received. It is only relevant
                            if ``correct_parameters`` is ``True`` - OPTIONAL
        :type one_request_present: ``bool``
        :param first_iteration: Flag indicating that this is the first iteration of the loop, and that the
                            initial conditions are as expected already - OPTIONAL
        :type first_iteration: ``bool``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop on connection parameters")
        # --------------------------------------------------------------------------------------------------------------
        for connection_parameters in connection_parameters_list:
            if first_iteration:
                first_iteration = False
            else:  # between iterations
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Disconnect from device")
                # ------------------------------------------------------------------------------------------------------
                if first_connection:  # if we need pair the device again
                    self.previous_devices_to_delete_bond.append(self.current_device)
                    ChannelUtils.close_channel(self, self.ble_channel)
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Enter pairing mode")
                    # --------------------------------------------------------------------------------------------------
                    DeviceBaseTestUtils.enter_pairing_mode_ble(test_case=self)
                else:
                    ChannelUtils.disconnect_ble_channel(self, self.ble_channel)
                    ChannelUtils.wait_usb_ble_channel_connection_state(
                        test_case=self, channel=self.ble_channel, connection_state=False, skip_error=False)
                    # Add a small delay to let the device realize the disconnection and enter deep sleep
                    sleep(.1)
                    # Perform a user action to wake up the device
                    self.button_stimuli_emulator.user_action()

                    if bootloader:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(self, "Scan for current device")
                        # ----------------------------------------------------------------------------------------------
                        self.current_device = BleProtocolTestUtils.scan_for_current_device(
                            test_case=self, scan_timeout=2, send_scan_request=False)
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(self, "Connect to device")
                        # ----------------------------------------------------------------------------------------------
                        self.current_channel = BleProtocolTestUtils.create_new_ble_channel(
                            test_case=self, ble_context_device=self.current_device)
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(self, "Put Device in BLE bootloader mode, without reconnecting")
                        # ----------------------------------------------------------------------------------------------
                        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=False)
                        self.post_requisite_restart_in_main_application = True
                        ChannelUtils.wait_usb_ble_channel_connection_state(
                            test_case=self,
                            channel=self.current_channel,
                            connection_state=False,
                            skip_error=True)
                    # end if
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Scan for current device")
                # ------------------------------------------------------------------------------------------------------
                self.current_device = BleProtocolTestUtils.scan_for_current_device(
                    test_case=self, scan_timeout=2, send_scan_request=False)
            # end if

            self._generic_test_correct_connection_parameters(connection_parameters=connection_parameters,
                                                             correct_parameters=True,
                                                             one_request_present=one_request_present)

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test loop on connection parameters")
        # --------------------------------------------------------------------------------------------------------------
    # end def _generic_looped_test_correct_connection_parameters
# end class ConnectionParametersTestCases


class ConnectionParametersApplicationReconnectionTestCases(ConnectionParametersTestCases):
    """
    BLE connection parameters Test Cases class for application reconnection
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Connect and bond to device")
        # --------------------------------------------------------------------------------------------------------------
        # connect without logging the gatt table, it will be logged on reconnection, cleaner log
        BleProtocolTestUtils.connect_and_bond_device(
            test_case=self, ble_context_device=self.current_device, log_gatt_table=False,
            connection_parameters=BleConnectionParametersTestUtils.get_default_os_connection_parameters(self))
        # Add a small delay because NRF BLE LIB is too fast, so disconnection happen
        # before the device consider the bonding complete
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Disconnect from the device")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.disconnect_device(test_case=self, ble_context_device=self.current_device)
        # Add a small delay to let the device realize the disconnection and enter deep sleep
        sleep(.1)
        # Perform a user action to wake up the device
        self.button_stimuli_emulator.user_action()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Scan for current device")
        # --------------------------------------------------------------------------------------------------------------
        self.assertTrue(self.ble_context.is_direct_advertising_device_present(self.current_device),
                        "device not advertising")
    # end def setUp
# end class ConnectionParametersApplicationReconnectionTestCases


class ConnectionParametersBootloaderReconnectionTestCases(ConnectionParametersTestCases):
    """
    BLE connection parameters Test Cases class for bootloader reconnection
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Connect and bond to device")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel = BleProtocolTestUtils.create_new_ble_channel(
            test_case=self, ble_context_device=self.current_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Put Device in BLE bootloader mode, without reconnecting")
        # --------------------------------------------------------------------------------------------------------------
        DfuControlTestUtils.target_enter_into_dfu_mode(test_case=self, check_device_reconnection=False)
        self.post_requisite_restart_in_main_application = True
        ChannelUtils.wait_usb_ble_channel_connection_state(
            test_case=self,
            channel=self.current_channel,
            connection_state=False,
            skip_error=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Scan for current device")
        # --------------------------------------------------------------------------------------------------------------
        self.current_device = BleProtocolTestUtils.scan_for_current_device(
            test_case=self, scan_timeout=2, send_scan_request=False)
    # end def setUp
# end class ConnectionParametersBootloaderReconnectionTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
