#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.connection_parameters.functionality
:brief: Validate BLE connection parameters Functionality test cases
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/09/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import perf_counter

from pychannel.blechannel import BASE_UUID_TO_ADD
from pychannel.logiconstants import LogitechBleConnectionParameters
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleconnectionparametersutils import BleConnectionParametersTestUtils
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.connection_parameters.connectionparameters import \
    ConnectionParametersApplicationReconnectionTestCases
from pytestbox.device.ble.connection_parameters.connectionparameters import \
    ConnectionParametersBootloaderReconnectionTestCases
from pytestbox.device.ble.connection_parameters.connectionparameters import ConnectionParametersTestCases
from pytransport.ble.bleconstants import BleContextConnectionParameterUpdateRequestResult
from pytransport.ble.bleconstants import BleContextEventDataType
from pytransport.ble.bleconstants import BleContextEventType
from pytransport.ble.blecontext import BleContext
from pytransport.ble.blecontext import BleContextDevice
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParameters
from pytransport.transportcontext import TransportContextException

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"

TIMEOUT_BETWEEN_UPDATES = 35  # in seconds

NUMBER_OF_REQUESTS = 5


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConnectionParametersFunctionalityTestCasesMixin(ConnectionParametersTestCases):
    """
    BLE connection parameters Functionality Test Cases
    """

    def _generic_test_connection_parameter_after_bonding_and_stop_after_change(self):
        """
        Generic test verifying that a Connection Parameters Update Request is received after bonding and not before
        """
        # Adding type hint does not add overhead and greatly helps the indexer
        self.current_device: BleContextDevice

        connection_parameters = BleConnectionParametersTestUtils.get_any_os_incorrect_connection_parameters(
            test_case=self)
        counter = 0
        while counter < BleProtocolTestUtils.MAX_TRIES:
            try:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Connect to device with wrong connection parameters")
                # ------------------------------------------------------------------------------------------------------
                # Clear the events before the connection
                self._clear_events_and_log_them()
                self.current_device.wait_for_disconnection_event.clear()
                # Connect to device
                self.ble_context.connect(
                    ble_context_device=self.current_device, service_discovery=False, confirm_connect=True,
                    connection_parameters=connection_parameters)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check that no Connection Parameters Update Request is received (for 2s)")
                # ------------------------------------------------------------------------------------------------------
                update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
                    event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=2,
                    skip_error=True)
                self.assertNone(
                    obtained=update_request_event,
                    msg="Connection Parameters Update Request received after bonding while it should not have."
                        f"\nParameters used: {connection_parameters}")

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Perform service discovery")
                # ------------------------------------------------------------------------------------------------------
                self.ble_context.perform_service_discovery(
                    ble_context_device=self.current_device, vendor_uuid_bases_to_add=BASE_UUID_TO_ADD)

                break
            except TransportContextException as e:
                self.log_traceback_as_warning(
                    supplementary_message="TransportContextException while trying to connect to device "
                                          "with wrong connection parameters")
                counter += 1
                if e.get_cause() in [TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                     TransportContextException.Cause.DEVICE_DISCONNECTION_DURING_OPERATION] and \
                        counter < BleProtocolTestUtils.MAX_TRIES:
                    # Add a large wait time to let the internal state of the BLE context to be the right one
                    if not self.current_device.wait_for_disconnection_event.wait(
                            timeout=BleContext.DISCONNECTION_STATE_SYNC_UP):
                        try:
                            BleProtocolTestUtils.disconnect_device(test_case=self,
                                                                   ble_context_device=self.current_device)
                        except TransportContextException:
                            self.logTrace("TransportContextException while trying to disconnect a device")
                        # end try
                    # end if
                    continue
                # end if
                e.add_message(f"after {counter} tries")
                raise
            # end try
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that no Connection Parameters Update Request is received (for 2s)")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=2,
            skip_error=True)
        self.assertNone(obtained=update_request_event,
                        msg="Connection Parameters Update Request received after bonding while it should not have."
                            f"\nParameters used: {connection_parameters}")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Bond to device")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.authenticate_just_works(ble_context_device=self.current_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a Connection Parameters Update Request is received (timeout 2s)")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=2,
            skip_error=True)
        self.assertNotNone(obtained=update_request_event,
                           msg="Connection Parameters Update Request not received after bonding while it "
                               f"should have.\nParameters used: {connection_parameters}")
        self.assertTrue(expr=BleContextEventDataType.CONNECTION_PARAMETERS_REQUESTED in update_request_event.event_data,
                        msg="The event data does not have the requested connection parameters")
        connection_parameters_requested = update_request_event.event_data[
            BleContextEventDataType.CONNECTION_PARAMETERS_REQUESTED]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Update requested connection parameters {connection_parameters_requested}")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.update_connection_parameters(
            ble_context_device=self.current_device,
            connection_parameters=connection_parameters_requested)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a Connection Parameters Update Request is not received (timeout 30s)")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=30,
            skip_error=True)
        self.assertNone(obtained=update_request_event,
                        msg="Received Connection Parameters Update Request after changing parameters to the right one "
                            f"while it should not have.\nParameters used: {connection_parameters_requested}\n")
    # end def _generic_test_connection_parameter_after_bonding_and_stop_after_change

    def _generic_test_accepted_change_request(self):
        """
        Generic test verifying that the DUT stops sending connection parameters change requests if the host accepts one
        """
        # Adding type hint does not add overhead and greatly helps the indexer
        self.ble_context: BleContext
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the host to accept parameters of parameters change requests")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.connection_parameters_range = \
            BleConnectionParametersTestUtils.get_always_acceptable_host_range()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to device with wrong connection parameters")
        # --------------------------------------------------------------------------------------------------------------
        # Clear the events before the connection
        self._clear_events_and_log_them()
        connection_parameters = BleConnectionParametersTestUtils.get_any_os_incorrect_connection_parameters(
            test_case=self)
        # Connect to device
        BleProtocolTestUtils.connect_and_bond_device(test_case=self,
                                                     ble_context_device=self.current_device,
                                                     connection_parameters=connection_parameters)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            "Check that a Connection Parameters Update Request is received and accepted(timeout 2s)")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=2,
            skip_error=True)
        self.assertNotNone(obtained=update_request_event,
                           msg="Connection Parameters Update Request not received after bonding while it "
                               f"should have.\nParameters used: {connection_parameters}")
        self.assertTrue(expr=BleContextEventDataType.CONNECTION_PARAMETERS_REQUESTED in update_request_event.event_data,
                        msg="The event data does not have the requested connection parameters")
        update_result_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT, timeout=0.5,
            skip_error=True
        )
        self.assertNotNone(obtained=update_result_event,
                           msg="No Connection Parameter Update Request Result event received")
        self.assertIn(member=BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT,
                      container=update_result_event.event_data,
                      msg="The event data does not contain the result of the request")
        self.assertEqual(expected=BleContextConnectionParameterUpdateRequestResult.ACCEPTED,
                         obtained=update_result_event.event_data[
                             BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT],
                         msg="The connection parameter update request was not accepted")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that no connection parameter change request is sent for more than 30s")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=30,
            skip_error=True)
        self.assertNone(obtained=update_request_event,
                        msg="Received Connection Parameters Update Request after changing parameters accepting the "
                            f"update request while it should not have.\n")
    # end def _generic_test_accepted_change_request

    def _generic_test_number_of_request(self, number_of_requests_expected, connect):
        """
        Generic test verifying the correct number of connection parameter update is sent

        :param number_of_requests_expected: the total number of connection parameter request expected
        :type number_of_requests_expected: ``int``
        :param connect: Flag indicating if a new connection will happen, otherwise update the parameters
        :type connect: ``True``
        """
        connection_parameters = BleConnectionParametersTestUtils.get_any_os_incorrect_connection_parameters(
            test_case=self)
        if connect:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Connect to the device with the wrong connection parameters")
            # ----------------------------------------------------------------------------------------------------------
            # Clear the event before the connection to then wait on it to check that it was or was not received
            self._clear_events_and_log_them()
            # Connect to device

            self.ble_channel = BleProtocolTestUtils.create_new_ble_channel(
                test_case=self, ble_context_device=self.current_device, connection_parameters=connection_parameters)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send a connection parameter update with unacceptable settings")
            # ----------------------------------------------------------------------------------------------------------
            self.ble_context.update_connection_parameters(ble_context_device=self.current_device,
                                                          connection_parameters=connection_parameters)
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test loop: {number_of_requests_expected}x for each requests to be sent ")
        # --------------------------------------------------------------------------------------------------------------

        for i in range(number_of_requests_expected):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check that a connection parameters change request is received")
            # ----------------------------------------------------------------------------------------------------------
            update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
                event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST,
                timeout=TIMEOUT_BETWEEN_UPDATES+10,
                skip_error=True)

            self.assertNotNone(update_request_event, msg=f"Connection Parameters Update Request n°{i+1} not received"
                                                         f" while it should have.\n"
                                                         f"Parameters used: {connection_parameters}")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"End Test loop: {number_of_requests_expected}x for each requests to be sent ")
        LogHelper.log_check(self, "Check that no connection parameters change request is received")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)

        self.assertNone(update_request_event, msg=f"No connection Parameters Update Request should received"
                                                  f" after receiving them {number_of_requests_expected} times already.")
    # end def _generic_test_number_of_request

    def _generic_test_number_request_with_disconnection(self):
        """
        Generic test verifying the correct number of connection parameter update is sent after a disconnection during
        the update change requests
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to the device with wrong connection parameters")
        # --------------------------------------------------------------------------------------------------------------
        # Clear the event before the connection to then wait on it to check that it was or was not received
        self._clear_events_and_log_them()
        # Connect to device
        connection_parameters = BleConnectionParametersTestUtils.get_any_os_incorrect_connection_parameters(
            test_case=self)
        self.ble_channel = BleProtocolTestUtils.create_new_ble_channel(
            test_case=self, ble_context_device=self.current_device, connection_parameters=connection_parameters)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a connection parameters change request is received")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST,
            timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNotNone(update_request_event, msg=f"Connection Parameters Update Request n°1 not received"
                                                     f" after bonding while it should have.")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a connection parameters change request is received after 30s")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST,
            timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNotNone(update_request_event, msg=f"Connection Parameters Update Request n°2 not received"
                                                     f" after bonding while it should have.")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disconnect from the device")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.disconnect_ble_channel(self, self.ble_channel)
        ChannelUtils.wait_usb_ble_channel_connection_state(
            test_case=self,
            channel=self.ble_channel,
            connection_state=False,
            skip_error=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Scan for current device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        self.current_device = BleProtocolTestUtils.scan_for_current_device(
            test_case=self, scan_timeout=2, send_scan_request=False)
        self._generic_test_number_of_request(NUMBER_OF_REQUESTS + 1, True)
    # end def _generic_test_number_request_with_disconnection

    def _generic_test_number_request_with_update(self):
        """
        Generic test verifying the correct number of connection parameter update is sent after a disconnection during
        the update change requests
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to the device with wrong connection parameters")
        # --------------------------------------------------------------------------------------------------------------
        # Clear the event before the connection to then wait on it to check that it was or was not received
        self._clear_events_and_log_them()
        # Connect to device
        connection_parameters = BleConnectionParametersTestUtils.get_any_os_incorrect_connection_parameters(
            test_case=self)
        self.ble_channel = BleProtocolTestUtils.create_new_ble_channel(
            test_case=self, ble_context_device=self.current_device, connection_parameters=connection_parameters)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a connection parameters change request is received")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST,
            timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNotNone(update_request_event, msg=f"Connection Parameters Update Request n°1 not received"
                                                     f" after bonding while it should have.")
        update_result_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT, timeout=0.5,
            skip_error=True
        )
        self.assertNotNone(obtained=update_result_event,
                           msg="No Connection Parameter Update Request Result event received")
        self.assertIn(member=BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT,
                      container=update_result_event.event_data,
                      msg="The event data does not contain the result of the request")
        self.assertEqual(expected=BleContextConnectionParameterUpdateRequestResult.REJECTED,
                         obtained=update_result_event.event_data[
                             BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT],
                         msg="The connection parameter update request was not accepted")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set host to accept parameters of parameters change request")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.connection_parameters_range = \
            BleConnectionParametersTestUtils.get_always_acceptable_host_range()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a connection parameters change request is received after "
                                  "30 seconds and accepted.")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST,
            timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNotNone(update_request_event, msg=f"Connection Parameters Update Request n°2 not received"
                                                     f" after bonding while it should have.")
        update_result_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT, timeout=0.5,
            skip_error=True
        )
        self.assertNotNone(obtained=update_result_event,
                           msg="No Connection Parameter Update Request Result event received")
        self.assertIn(member=BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT,
                      container=update_result_event.event_data,
                      msg="The event data does not contain the result of the request")
        self.assertEqual(expected=BleContextConnectionParameterUpdateRequestResult.ACCEPTED,
                         obtained=update_result_event.event_data[
                             BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT],
                         msg="The connection parameter update request was not accepted")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set host to refuse parameters of parameters change request")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.connection_parameters_range = None
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that no connection parameters change request is received for more than 30s")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNone(obtained=update_request_event,
                        msg="Connection Parameters Update Request received after bonding while it should "
                            f"not have.\nParameters used: {connection_parameters}\n")

        self._generic_test_number_of_request(NUMBER_OF_REQUESTS - 1, connect=False)
    # end def _generic_test_number_request_with_update

# end class ConnectionParametersFunctionalityTestCasesMixin


class ConnectionParametersFunctionalityFirstConnectionTestCases(
        ConnectionParametersFunctionalityTestCasesMixin, ConnectionParametersTestCases):
    """
    BLE connection parameters Functionality Test Cases for first connection use cases
    """

    def setUp(self):
        """
        handle test prerequisite
        """
        ConnectionParametersTestCases.setUp(self)
    # end def setUp

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_connection_parameters_update_request_after_bonding_and_stop_on_change(self):
        """
        Verify that a Connection Parameters Update Request is received after bonding and not before that the parameters
        change requests stop after changing to expected values
        """
        self._generic_test_connection_parameter_after_bonding_and_stop_after_change()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0001", _AUTHOR)
    # end def test_connection_parameters_update_request_after_bonding_and_stop_on_change

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_accept_change_request(self):
        """
        Verify that the DUT stops sending connection parameters change requests if the host accepts one
        """
        self._generic_test_accepted_change_request()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0004", _AUTHOR)
    # end def test_accept_change_request

    @features('BLESpacesSpecification')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_number_of_request(self):
        """
        Verify the correct number of connection parameter update is sent
        """
        self._generic_test_number_of_request(NUMBER_OF_REQUESTS + 1, True)

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0007", _AUTHOR)
    # end def test_number_of_request

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_connection_update_in_range(self):
        """
        Verify that the DUT accepts an update of connection parameter
        """
        # Adding type hint does not add overhead and greatly helps the indexer
        self.ble_context: BleContext

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to the device with correct connection parameters ")
        # --------------------------------------------------------------------------------------------------------------
        connection_parameters = BleConnectionParametersTestUtils.get_default_os_connection_parameters(self)

        self.ble_channel = BleProtocolTestUtils.create_new_ble_channel(
            test_case=self, ble_context_device=self.current_device, connection_parameters=connection_parameters)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that no connection parameters change request is received for more than 30s")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNone(obtained=update_request_event,
                        msg="Connection Parameters Update Request received after bonding while it should "
                            f"not have.\nParameters used: {connection_parameters}\n")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the connection parameters to different acceptable parameters")
        # --------------------------------------------------------------------------------------------------------------
        different_connection_parameters = BleGapConnectionParameters(
            min_connection_interval=connection_parameters.min_connection_interval,
            max_connection_interval=connection_parameters.max_connection_interval,
            supervision_timeout=(connection_parameters.supervision_timeout +
                                 BleConnectionParametersTestUtils.VALIDITY_RANGE_MS / 2),
            slave_latency=int(connection_parameters.slave_latency)
        )
        self.ble_context.update_connection_parameters(ble_context_device=self.current_device,
                                                      connection_parameters=different_connection_parameters)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that no connection parameters change request is received for more than 30s")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNone(obtained=update_request_event,
                        msg="Connection Parameters Update Request received after update while it should "
                            f"not have.\nParameters used: {connection_parameters}\n")

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send a HID++ request (root feature 0x0000)")
        LogHelper.log_check(self, "Check that a response is received")
        # ----------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=DeviceInformation.FEATURE_ID, channel=self.ble_channel)

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0010", _AUTHOR)
    # end def test_connection_update_in_range

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_connection_update_out_of_range(self):
        """
        Verify that the DUT sends connection parameters update requests if it received new connection parameters that
        aren't acceptable
        """
        # Adding type hint does not add overhead and greatly helps the indexer
        self.ble_context: BleContext

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set the host to accept parameters of parameters change requests")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.connection_parameters_range =\
            BleConnectionParametersTestUtils.get_always_acceptable_host_range()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to the device with correct connection parameters ")
        # --------------------------------------------------------------------------------------------------------------
        connection_parameters = BleConnectionParametersTestUtils.get_default_os_connection_parameters(self)

        self.ble_channel = BleProtocolTestUtils.create_new_ble_channel(
            test_case=self, ble_context_device=self.current_device, connection_parameters=connection_parameters)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that no connection parameters change request is received for more than 30s")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNone(obtained=update_request_event,
                        msg="Connection Parameters Update Request received after bonding while it should "
                            f"not have.\nParameters used: {connection_parameters}\n")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the connection parameters to unaccepted parameters")
        # --------------------------------------------------------------------------------------------------------------
        different_connection_parameters = \
            BleConnectionParametersTestUtils.get_any_os_incorrect_connection_parameters(self)

        start_time = perf_counter()
        self.ble_context.update_connection_parameters(ble_context_device=self.current_device,
                                                      connection_parameters=different_connection_parameters)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a connection parameters change request "
                                  "is received after 30s and accepted")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNotNone(obtained=update_request_event,
                           msg="Connection Parameters Update Request not received after update while it should "
                               f"have.\nParameters used: {connection_parameters}\n")

        self.assertGreater(a=update_request_event.timestamp-start_time, b=30, msg="Connection Parameter Update Request "
                           "received too early after update")

        update_result_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT, timeout=0.5,
            skip_error=True
        )
        self.assertNotNone(obtained=update_result_event,
                           msg="No Connection Parameter Update Request Result event received")
        self.assertIn(member=BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT,
                      container=update_result_event.event_data,
                      msg="The event data does not contain the result of the request")
        self.assertEqual(expected=BleContextConnectionParameterUpdateRequestResult.ACCEPTED,
                         obtained=update_result_event.event_data[
                             BleContextEventDataType.CONNECTION_PARAMETERS_UPDATE_REQUEST_RESULT],
                         msg="The connection parameter update request was not accepted")

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send a HID++ request (root feature 0x0000)")
        LogHelper.log_check(self, "Check that a response is received")
        # ----------------------------------------------------------------------------------------------------------
        ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=DeviceInformation.FEATURE_ID, channel=self.ble_channel)

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0011", _AUTHOR)
    # end def test_connection_update_out_of_range

    @features('BLESpacesSpecification')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_number_request_with_disconnection(self):
        """
        Verify the correct number of connection parameter update is sent after a disconnection during
        the update change requests
        """
        self._generic_test_number_request_with_disconnection()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0012", _AUTHOR)
    # end def test_number_request_with_disconnection

    @features('BLESpacesSpecification')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_number_request_with_update(self):
        """
        Verify the correct number of connection parameter update when the host sends an update
        """
        self._generic_test_number_request_with_update()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0014", _AUTHOR)
    # end def test_number_request_with_update

    @features('BLEProtocol')
    @features('Keyboard')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_extended_range(self):
        """
        Verify that the device switch to extended range correctly

        NOTE: be modified depending on issue: https://jira.logitech.io/browse/BT-484
        """
        connection_interval_ms = LogitechBleConnectionParameters.BLE_PRO_RECEIVER_CONNECTION_INTERVAL_MS

        preferred_connection_parameters = BleConnectionParametersTestUtils.get_default_os_connection_parameters(self)
        extended_range_recommended = BleConnectionParametersTestUtils.get_extended_range_recommended(
                                              preferred_connection_parameters,
                                              connection_interval_ms)
        extended_range_invalid = BleGapConnectionParameters(
            min_connection_interval=extended_range_recommended.min_connection_interval,
            max_connection_interval=extended_range_recommended.max_connection_interval,
            slave_latency=extended_range_recommended.slave_latency,
            supervision_timeout=extended_range_recommended.supervision_timeout +
            BleConnectionParametersTestUtils.VALIDITY_RANGE_MS +
            BleConnectionParametersTestUtils.SUPERVISION_TIMEOUT_GRANULARITY,
        )
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Connect to the device with parameters invalid for extended range but with connection "
                                 "interval in extended range")
        LogHelper.log_info(self, f"Connection parameters = {extended_range_invalid}")
        # --------------------------------------------------------------------------------------------------------------
        # Clear the events before the connection
        self._clear_events_and_log_them()
        self.ble_channel = BleProtocolTestUtils.create_new_ble_channel(
            test_case=self, ble_context_device=self.current_device, connection_parameters=extended_range_invalid)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a connection parameters change request is received and correspond "
                                  "to the preferred parameters.")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=2,
            skip_error=True)
        self.assertNotNone(obtained=update_request_event,
                           msg="Connection Parameters Update Request not received after bonding while it should "
                               f"not have.\nParameters used: {extended_range_invalid}\n")
        self.assertIn(member=BleContextEventDataType.CONNECTION_PARAMETERS_REQUESTED,
                      container=update_request_event.event_data,
                      msg="The event data does not contain the requested parameters")
        self.assertEqual(expected=preferred_connection_parameters,
                         obtained=update_request_event.event_data[
                             BleContextEventDataType.CONNECTION_PARAMETERS_REQUESTED],
                         msg="The requested connection parameters do not match the preferred")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check that a connection parameters change request is received after 30s and "
                                  "correspond to the extended range parameters for this connection interval")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNotNone(obtained=update_request_event,
                           msg="Connection Parameters Update Request not received after bonding while it should "
                               f"not have.\nParameters used: {extended_range_invalid}\n")
        self.assertIn(member=BleContextEventDataType.CONNECTION_PARAMETERS_REQUESTED,
                      container=update_request_event.event_data,
                      msg="The event data does not contain the requested parameters")
        parameters_requested = update_request_event.event_data[BleContextEventDataType.CONNECTION_PARAMETERS_REQUESTED]

        self.assertEqual(expected=extended_range_recommended,
                         obtained=parameters_requested,
                         msg="The requested connection parameters do not match the preferred")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Change the connection parameters to the requested parameters")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context.update_connection_parameters(connection_parameters=parameters_requested,
                                                      ble_context_device=self.current_device)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check that no connection parameters change request is received "
                                 "for more than 30 seconds")
        # --------------------------------------------------------------------------------------------------------------
        update_request_event = self.current_device.ble_context_event_queue.get_first_event_of_a_type(
            event_type=BleContextEventType.L2CAP_CONNECTION_PARAMETERS_UPDATE_REQUEST, timeout=TIMEOUT_BETWEEN_UPDATES,
            skip_error=True)
        self.assertNone(obtained=update_request_event,
                        msg="Connection Parameters Update Request received after update while it should "
                            f"not have.")
    # end def test_extended_range
# end class ConnectionParametersFunctionalityFirstConnectionTestCases


class ConnectionParametersFunctionalityApplicationReconnectionTestCases(
        ConnectionParametersApplicationReconnectionTestCases, ConnectionParametersFunctionalityTestCasesMixin):
    """
    BLE connection parameters Functionality Test Cases for reconnection use cases
    """

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_connection_parameters_update_request_after_bonding_and_stop_on_change(self):
        """
        Verify that a Connection Parameters Update Request is received after bonding and not before that the parameters
        change requests stop after changing to expected values
        """
        self._generic_test_connection_parameter_after_bonding_and_stop_after_change()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0002", _AUTHOR)
    # end def test_connection_parameters_update_request_after_bonding_and_stop_on_change

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_accept_change_request(self):
        """
        Verify that the DUT stops sending connection parameters change requests if the host accepts one
        """
        self._generic_test_accepted_change_request()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0005", _AUTHOR)
    # end def test_accept_change_request

    @features('BLESpacesSpecification')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_number_of_request(self):
        """
        Verify the correct number of connection parameter update is sent
        """
        self._generic_test_number_of_request(NUMBER_OF_REQUESTS + 1, True)

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0008", _AUTHOR)
    # end def test_number_of_request

    @features('BLESpacesSpecification')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_number_request_with_disconnection(self):
        """
        verify the correct number of connection parameter update is sent after a disconnection during
        the update change requests
        """
        self._generic_test_number_request_with_disconnection()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0013", _AUTHOR)
    # end def test_number_request_with_disconnection
# end class ConnectionParametersFunctionalityApplicationReconnectionTestCases


@features.class_decorator("BootloaderBLESupport")
class ConnectionParametersFunctionalityBootloaderReconnectionTestCases(
        ConnectionParametersBootloaderReconnectionTestCases, ConnectionParametersFunctionalityTestCasesMixin):
    """
    BLE connection parameters Functionality Test Cases for bootloader use cases
    """

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_connection_parameters_update_request_after_bonding_and_stop_on_change(self):
        """
        Verify that a Connection Parameters Update Request is received after bonding and not before that the parameters
        change requests stop after changing to expected values
        """
        self._generic_test_connection_parameter_after_bonding_and_stop_after_change()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0003", _AUTHOR)
    # end def test_connection_parameters_update_request_after_bonding_and_stop_on_change

    @features('BLEProtocol')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_accept_change_request(self):
        """
        Verify that  the DUT stops sending connection parameters change requests if the host accepts one
        """
        self._generic_test_accepted_change_request()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0006", _AUTHOR)
    # end def test_accept_change_request

    @features('BLESpacesSpecification')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_number_of_request(self):
        """
        Verify the correct number of connection parameter update is sent
        """
        self._generic_test_number_of_request(NUMBER_OF_REQUESTS + 1, True)

        # todo check
    # end def test_number_of_request

    @features('BLESpacesSpecification')
    @level('Time-consuming')
    @services('BleContext')
    @services('Debugger')
    def test_number_request_with_update(self):
        """
        Verify the correct number of connection parameter update when the host sends an update
        """
        self._generic_test_number_request_with_update()

        self.testCaseChecked("FUN_BLE_CONN_PARAM_0015", _AUTHOR)
    # end def test_number_request_with_update
# end class ConnectionParametersFunctionalityBootloaderReconnectionTestCases


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
