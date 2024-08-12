#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.batterylevelscalibrationutils
:brief:  Helpers for Battery Levels Calibration feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.core import TestException
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationFactory
from pylibrary.tools.numeral import Numeral
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BatteryLevelsCalibrationTestUtils(DeviceBaseTestUtils):
    """
    Test utils for Battery Levels Calibration feature
    """

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def set_cutoff_state(cls, test_case, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_ENABLE,
                             cutoff_change_state_requested=False, state_to_check=0, **kwargs):
            """
            Get the number of hosts in the registry and the currently active host index (logically the caller).
            Also returns a capability_mask for the device.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param cutoff_desired_state: Desired state of cutoff
                                        - BatteryLevelsCalibration.CUTOFF_ENABLE (0)
                                        - BatteryLevelsCalibration.CUTOFF_DISABLE (1)
            :type cutoff_desired_state: ``int``
            :param cutoff_change_state_requested: Define if a state change is requested or not
            :type cutoff_change_state_requested: ``bool``
            :param state_to_check: State to check in the response
            :type state_to_check: ``int``
            :param kwargs: Potential future parameters
            :type kwargs: ``dict``

            |

            :kwargs:
                * **device_index** (``int``): Device index - OPTIONAL
                * **port_index** (``int``): Port index - OPTIONAL
            """
            feature_1861_index, feature_1861, device_index, port_index = cls.get_parameters(
                test_case=test_case, feature_id=BatteryLevelsCalibration.FEATURE_ID,
                factory=BatteryLevelsCalibrationFactory, device_index=kwargs.get('device_index', test_case.deviceIndex),
                port_index=kwargs.get('port_index', None))

            DeviceBaseTestUtils.LogHelper.log_step(
                test_case, f'Send CutOffControl with desiredState = '
                f'{cutoff_desired_state} and changeStateRequested = {cutoff_change_state_requested}')

            cut_off_control_req = feature_1861.cut_off_control_cls(
                kwargs.get('device_index', test_case.deviceIndex), feature_1861_index,
                cutoff_change_state_requested=cutoff_change_state_requested, cutoff_desired_state=cutoff_desired_state)
            cut_off_control_resp = test_case.send_report_wait_response(
                report=cut_off_control_req,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1861.cut_off_control_response_cls)

            DeviceBaseTestUtils.LogHelper.log_check(
                test_case, f'Validate CutOffControl.cutoffState = {state_to_check}')

            test_case.assertEqual(expected=state_to_check,
                                  obtained=cut_off_control_resp.cutoff_state,
                                  msg='The cutoffState parameter differs from the one expected')
        # end def set_cutoff_state

        @classmethod
        def comp_measure_battery(cls, test_case, device_index=None, port_index=None):
            """
            Get thresholds when comparator is used to measure battery level

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port Index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: Thresholds returned in MeasureBattery response
            :rtype: ``int``
            """
            feature_1861_index, feature_1861, device_index, port_index = cls.get_parameters(
                test_case, BatteryLevelsCalibration.FEATURE_ID, BatteryLevelsCalibrationFactory, device_index,
                port_index)

            measure_battery = feature_1861.measure_battery_cls(
                device_index=test_case.deviceIndex, feature_index=feature_1861_index)
            measure_battery_response = test_case.send_report_wait_response(
                report=measure_battery, response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1861.measure_battery_response_cls)

            return int(Numeral(measure_battery_response.measure[1])), int(Numeral(measure_battery_response.measure[0]))
        # end def comp_measure_battery
    # end class HIDppHelper

    @classmethod
    def compare_store_read_calibration(cls, test_case, store_calibration, read_calibration):
        """
        Compare two callibration structures

        :param test_case: The current test case
        :type test_case: ``Class inheriting CommonBaseTestCase``
        :param store_calibration: structure coming from the store callibration request
        :type store_calibration: ``StoreCalibration``
        :param read_calibration: structure coming from the read callibration response
        :type read_calibration: ``StoreCalibration``
        """
        test_case.assertEqual(expected=int(Numeral(store_calibration.calibration_points_nb)),
                              obtained=int(Numeral(read_calibration.calibration_points_nb)),
                              msg='The calibPointsNb parameter differs from the one expected')

        store_calibration_points_list = [int(Numeral(store_calibration.calibration_point_0)),
                                         int(Numeral(store_calibration.calibration_point_1)),
                                         int(Numeral(store_calibration.calibration_point_2)),
                                         int(Numeral(store_calibration.calibration_point_3)),
                                         int(Numeral(store_calibration.calibration_point_4)),
                                         int(Numeral(store_calibration.calibration_point_5)),
                                         int(Numeral(store_calibration.calibration_point_6))]
        read_calibration_points_list = [int(Numeral(read_calibration.calibration_point_0)),
                                        int(Numeral(read_calibration.calibration_point_1)),
                                        int(Numeral(read_calibration.calibration_point_2)),
                                        int(Numeral(read_calibration.calibration_point_3)),
                                        int(Numeral(read_calibration.calibration_point_4)),
                                        int(Numeral(read_calibration.calibration_point_5)),
                                        int(Numeral(read_calibration.calibration_point_6))]

        for i in range(len(store_calibration_points_list)):
            test_case.assertEqual(expected=store_calibration_points_list[i],
                                  obtained=read_calibration_points_list[i],
                                  msg='The calibPoint' + str(i) + ' parameter differs from the one expected')
    # end def compare_store_read_calibration

    @classmethod
    def check_comp_measure_battery(cls, test_case, expected_low_threshold, expected_high_threshold,
                                   power_supply_bias_correction=0):
        """
        Check MeasureBattery with comparator

        :param test_case: The current test case
        :type test_case: Class inheriting ``CommonBaseTestCase``
        :param expected_low_threshold: Expected low threshold
        :type expected_low_threshold: ``int``
        :param expected_high_threshold: Expected high threshold
        :type expected_high_threshold: ``int``
        :param power_supply_bias_correction: Known Power Supply bias correction - OPTIONAL
        :type power_supply_bias_correction: ``float``

        :return: Adapted Power Supply bias correction
        :rtype: ``float``

        :raise ``TestException``: If test fails
        """
        # ---------------------------------------------------------------------------
        DeviceBaseTestUtils.LogHelper.log_step(test_case, 'Send MeasureBattery')
        # ---------------------------------------------------------------------------
        low_threshold, high_threshold = BatteryLevelsCalibrationTestUtils.HIDppHelper.comp_measure_battery(test_case)

        # The Power Supply can have a little inaccuracy (about 10mv) which can lead to false positive, because the
        # range can then be the one before or the one after.
        # If this happens, retry the measurement with an input voltage slightly modified (+/-10mV), which should now
        # be in between the expected thresholds
        try:
            # ---------------------------------------------------------------------------
            DeviceBaseTestUtils.LogHelper.log_check(test_case, 'Check measured voltage is between expected thresholds')
            # ---------------------------------------------------------------------------
            test_case.assertListEqual([low_threshold, high_threshold],
                                      [expected_low_threshold, expected_high_threshold],
                                      f'Obtained thresholds {[low_threshold, high_threshold]} are not as expected '
                                      f'{[expected_low_threshold, expected_high_threshold]}')
        except TestException as err:
            def _retry(new_power_supply_bias_correction):
                """
                Set a new voltage and retry measurement

                :param new_power_supply_bias_correction: Power Supply bias correction to apply when setting voltage
                :type new_power_supply_bias_correction: ``float``
                """
                test_case.log_warning(str(err))

                new_voltage = round(test_case.power_supply_emulator.get_voltage() + new_power_supply_bias_correction,
                                    PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1)
                test_case.power_supply_emulator.set_voltage(new_voltage)
                # ---------------------------------------------------------------------------
                DeviceBaseTestUtils.LogHelper.log_step(test_case, 'Retry: Get raw input voltage')
                # ---------------------------------------------------------------------------
                new_raw_voltage = test_case.power_supply_emulator.get_voltage()
                DeviceBaseTestUtils.LogHelper.log_info(test_case, f'Retry: Input voltage is {new_raw_voltage}')

                # ---------------------------------------------------------------------------
                DeviceBaseTestUtils.LogHelper.log_step(test_case, 'Retry: send MeasureBattery')
                # ---------------------------------------------------------------------------
                low, high = BatteryLevelsCalibrationTestUtils.HIDppHelper.comp_measure_battery(test_case)
                # ---------------------------------------------------------------------------
                DeviceBaseTestUtils.LogHelper.log_check(test_case, 'Retry: Check measured voltage is between expected '
                                                                   'thresholds')
                # ---------------------------------------------------------------------------
                test_case.assertListEqual([low, high], [expected_low_threshold, expected_high_threshold],
                                          f'Retry: Obtained thresholds {[low, high]} are not as expected '
                                          f'{[expected_low_threshold, expected_high_threshold]}')
            # end def _retry
            if low_threshold == expected_low_threshold - 1 and high_threshold == expected_high_threshold - 1:
                power_supply_bias_correction = 0.01
            elif low_threshold == expected_low_threshold + 1 and high_threshold == expected_high_threshold + 1:
                power_supply_bias_correction = -0.01
            else:
                raise err
            # end if
            _retry(power_supply_bias_correction)
        # end try
        return power_supply_bias_correction
    # end def check_comp_measure_battery
# end class BatteryLevelsCalibrationTestUtils
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
