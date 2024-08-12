#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.connection_parameters.robustness
:brief: Validate BLE connection parameters robustness test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/05/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleconnectionparametersutils import BleConnectionParametersTestUtils
from pytestbox.device.ble.connection_parameters.connectionparameters import \
    ConnectionParametersApplicationReconnectionTestCases
from pytestbox.device.ble.connection_parameters.connectionparameters import \
    ConnectionParametersBootloaderReconnectionTestCases
from pytestbox.device.ble.connection_parameters.connectionparameters import ConnectionParametersTestCases
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParameters

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConnectionParametersRobustnessTestCasesMixin(ConnectionParametersTestCases):
    """
    BLE connection parameters Robustness Test Cases
    """

    def _generic_slave_latency_robustness_test(self, first_connection, bootloader=False):
        """
        Generic test verifying the robustness of the slave latency

        :param first_connection: Flag indicating if each connection need to be done as the first connection of a
                new pairing
        :type first_connection: ``bool``
        :param bootloader: Flag indicating if the device must be in bootloader - OPTIONAL
        :type bootloader: ``bool``
        """
        if bootloader:
            acceptable = BleConnectionParametersTestUtils.get_bootloader_connection_parameters(self)
        else:
            acceptable = BleConnectionParametersTestUtils.get_default_os_connection_parameters(self)
        # end if
        connection_parameters_acceptable_list = []
        connection_parameters_extended_list = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate set of connection parameters for valid slave latency range for "
                                 "the accepted range ")
        # --------------------------------------------------------------------------------------------------------------
        if acceptable.min_connection_interval != acceptable.max_connection_interval:
            # for the minimal acceptable Connection interval
            connection_parameters_acceptable_list.extend(self._get_slave_latency_range(
                acceptable, acceptable.min_connection_interval))
            # for the maximal acceptable Connection interval
            connection_parameters_acceptable_list.extend(self._get_slave_latency_range(
                acceptable, acceptable.max_connection_interval))
        else:
            connection_parameters_acceptable_list.extend(self._get_slave_latency_range(
                acceptable, acceptable.min_connection_interval))
        # end if
        self._generic_looped_test_correct_connection_parameters(connection_parameters_acceptable_list,
                                                                first_connection=first_connection,
                                                                one_request_present=False,
                                                                bootloader=bootloader)
        if acceptable.min_connection_interval > BleConnectionParametersTestUtils.MIN_CONNECTION_INTERVAL_EXTENDED_RANGE:
            if first_connection:
                self.previous_devices_to_delete_bond.append(self.current_device)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Generate set of connection parameters for valid slave latency range for "
                                     "the extended range ")
            # ----------------------------------------------------------------------------------------------------------
            extended_min = BleConnectionParametersTestUtils.get_extended_range_recommended(acceptable)
            max_connection_interval = acceptable.min_connection_interval \
                - BleConnectionParametersTestUtils.CONNECTION_INTERVAL_GRANULARITY
            extended_max = BleConnectionParametersTestUtils.get_extended_range_recommended(
                acceptable, connection_interval=max_connection_interval)

            connection_parameters_extended_list.extend(self._get_slave_latency_range(
                extended_min, extended_min.min_connection_interval, is_extended_range=True))
            connection_parameters_extended_list.extend(self._get_slave_latency_range(
                extended_max, extended_max.min_connection_interval, is_extended_range=True))

            self._generic_looped_test_correct_connection_parameters(connection_parameters_extended_list,
                                                                    first_connection=first_connection,
                                                                    one_request_present=True,
                                                                    bootloader=bootloader,
                                                                    first_iteration=False)
        # end if
    # end def _generic_slave_latency_robustness_test

    def _generic_supervision_timeout_robustness_test(self, first_connection, bootloader=False):
        """
        Generic test verifying the robustness of the supervision timeout

        :param first_connection: Flag indicating if each connection need to be done as the first connection of a
                new pairing
        :type first_connection: ``bool``
        :param bootloader: Flag indicating if the device must be in bootloader - OPTIONAL
        :type bootloader: ``bool``
        """
        if bootloader:
            acceptable = BleConnectionParametersTestUtils.get_bootloader_connection_parameters(self)
        else:
            acceptable = BleConnectionParametersTestUtils.get_default_os_connection_parameters(self)
        # end if
        connection_parameters_acceptable_list = []
        connection_parameters_extended_list = []
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Generate set of connection parameters for valid supervision timeout range for "
                                 "the accepted range ")
        # --------------------------------------------------------------------------------------------------------------
        connection_parameters_acceptable_list.extend(self._get_supervision_timeout_range(acceptable))
        self._generic_looped_test_correct_connection_parameters(connection_parameters_acceptable_list,
                                                                first_connection=first_connection,
                                                                one_request_present=False,
                                                                bootloader=bootloader)
        if acceptable.min_connection_interval > BleConnectionParametersTestUtils.MIN_CONNECTION_INTERVAL_EXTENDED_RANGE:
            if first_connection:
                self.previous_devices_to_delete_bond.append(self.current_device)
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Generate set of connection parameters for valid slave latency range for "
                                     "the extended range ")
            # ----------------------------------------------------------------------------------------------------------
            extended = BleConnectionParametersTestUtils.get_extended_range_recommended(acceptable)
            connection_parameters_extended_list.extend(self._get_supervision_timeout_range(extended,
                                                                                           is_extended_range=True))

            self._generic_looped_test_correct_connection_parameters(connection_parameters_extended_list,
                                                                    first_connection=first_connection,
                                                                    one_request_present=True,
                                                                    bootloader=bootloader,
                                                                    first_iteration=False)
        # end if
    # end def _generic_supervision_timeout_robustness_test

    @staticmethod
    def _get_slave_latency_range(acceptable, connection_interval, is_extended_range=False):
        """
        Create a list of valid slave latency connection parameters testing the minimum and maximum acceptable,
        for a specific connection interval

        :param acceptable: the acceptable parameters to use as a central point
        :type acceptable: ``BleGapConnectionParameters``
        :param connection_interval: the connection interval to use
        :type connection_interval: ``float``
        :param is_extended_range: Flag indicating the expected parameters are for extended range - OPTIONAL
        :type is_extended_range: ``bool``

        :return: A list comprising the connection parameters for the minimum and maximum slave latency supported
        :rtype: ``list[BleGapConnectionParameters]``
        """
        min_slave_latency, max_slave_latency = BleConnectionParametersTestUtils.get_slave_latency_valid_range(
            connection_parameters=acceptable, connection_interval=connection_interval,
            is_extended_range=is_extended_range)
        if is_extended_range:
            parameters = [BleGapConnectionParameters(min_connection_interval=connection_interval,
                                                     max_connection_interval=connection_interval,
                                                     supervision_timeout=acceptable.supervision_timeout,
                                                     slave_latency=min_slave_latency)]
        else:
            parameters = [BleGapConnectionParameters(min_connection_interval=connection_interval,
                                                     max_connection_interval=connection_interval,
                                                     supervision_timeout=acceptable.supervision_timeout,
                                                     slave_latency=min_slave_latency),
                          BleGapConnectionParameters(min_connection_interval=connection_interval,
                                                     max_connection_interval=connection_interval,
                                                     supervision_timeout=acceptable.supervision_timeout,
                                                     slave_latency=max_slave_latency)]
        return parameters

    # end def _get_slave_latency_range

    @staticmethod
    def _get_supervision_timeout_range(acceptable, is_extended_range=False):
        """
        Create a list of valid supervision timeout connection parameters testing the minimum and maximum acceptable.
        Note: Can modify the slave latency if needed to correspond to valid ble range.

        :param acceptable: the acceptable parameters to use as a central point
        :type acceptable: ``BleGapConnectionParameters``
        :param is_extended_range: Flag indicating the expected parameters are for extended range - OPTIONAL
        :type is_extended_range: ``bool``

        :return: A list comprising the connection parameters for the minimum and maximum supervision timeout supported
        :rtype: ``list[BleGapConnectionParameters]``
        """
        min_supervision_timeout, max_supervision_timeout =\
            BleConnectionParametersTestUtils.get_supervision_timeout_valid_range(connection_parameters=acceptable,
                                                                                 is_extended_range=is_extended_range)
        # for the current slave latency, the minimum supervision timeout can be lower than the minimum defined by ble,
        # slave latency need to be adjusted accordingly
        min_supervision_timeout_for_sl = (1 + acceptable.slave_latency) * acceptable.max_connection_interval * 2

        if min_supervision_timeout < min_supervision_timeout_for_sl:
            sl = int((min_supervision_timeout / (acceptable.max_connection_interval * 2)) - 1)
        else:
            sl = acceptable.slave_latency
        # end if

        if is_extended_range:
            parameters = [BleGapConnectionParameters(min_connection_interval=acceptable.min_connection_interval,
                                                     max_connection_interval=acceptable.max_connection_interval,
                                                     supervision_timeout=min_supervision_timeout,
                                                     slave_latency=sl)]
        else:
            parameters = [BleGapConnectionParameters(min_connection_interval=acceptable.min_connection_interval,
                                                     max_connection_interval=acceptable.max_connection_interval,
                                                     supervision_timeout=min_supervision_timeout,
                                                     slave_latency=sl),
                          BleGapConnectionParameters(min_connection_interval=acceptable.min_connection_interval,
                                                     max_connection_interval=acceptable.max_connection_interval,
                                                     supervision_timeout=max_supervision_timeout,
                                                     slave_latency=acceptable.slave_latency)]
        # end if

        return parameters
    # end def _get_supervision_timeout_range
# end class ConnectionParametersRobustnessTestCasesMixin


class ConnectionParametersRobustnessApplicationFirstConnectionTestCases(ConnectionParametersRobustnessTestCasesMixin):
    """
    BLE connection parameters Robustness Test Cases for first connection use cases
    """

    @features('BLESpacesSpecification')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_slave_latency_robustness(self):
        """
        Verify the robustness of the slave latency
        """
        self._generic_slave_latency_robustness_test(first_connection=True)

        self.testCaseChecked("ROB_BLE_CONN_PARAM_0001", _AUTHOR)
    # end def test_slave_latency_robustness

    @features('BLESpacesSpecification')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_supervision_timeout_robustness(self):
        """
        Verify the robustness of the supervision timeout
        """
        self._generic_supervision_timeout_robustness_test(first_connection=True)
    # end def test_supervision_timeout_robustness
# end class ConnectionParametersRobustnessApplicationFirstConnectionTestCases


class ConnectionParametersRobustnessApplicationReconnectionTestCases(
        ConnectionParametersApplicationReconnectionTestCases, ConnectionParametersRobustnessTestCasesMixin):
    """
    BLE connection parameters Robustness Test Cases for reconnection use cases
    """

    @features('BLESpacesSpecification')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_slave_latency_robustness(self):
        """
        Verify the robustness of the slave latency
        """
        self._generic_slave_latency_robustness_test(first_connection=False)

        self.testCaseChecked("ROB_BLE_CONN_PARAM_0002", _AUTHOR)
    # end def test_slave_latency_robustness

    @features('BLESpacesSpecification')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_supervision_timeout_robustness(self):
        """
        Verify the robustness of the supervision timeout
        """
        self._generic_supervision_timeout_robustness_test(first_connection=False)
    # end def test_supervision_timeout_robustness
# end class ConnectionParametersRobustnessApplicationReconnectionTestCases


@features.class_decorator("BootloaderBLESupport")
class ConnectionParametersRobustnessBootloaderReconnectionTestCases(
        ConnectionParametersBootloaderReconnectionTestCases, ConnectionParametersRobustnessTestCasesMixin):
    """
    BLE connection parameters Robustness Test Cases for bootloader use cases
    """

    @features('BLESpacesSpecification')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_slave_latency_robustness(self):
        """
        Verify the robustness of the slave latency
        """
        self._generic_slave_latency_robustness_test(first_connection=False, bootloader=True)
    # end def test_slave_latency_robustness

    @features('BLESpacesSpecification')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_supervision_timeout_robustness(self):
        """
        Verify the robustness of the supervision timeout
        """
        self._generic_supervision_timeout_robustness_test(first_connection=False, bootloader=True)
    # end def test_supervision_timeout_robustness
# end class ConnectionParametersRobustnessBootloaderReconnectionTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
