#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1861.business
:brief: HID++ 2.0 Battery Levels Calibration business test suite
:author: Christophe Roquebert
:date: 2021/04/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.unifiedbattery import GetCapabilitiesResponseV0ToV1
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.threadutils import QueueEmpty
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1861.batterylevelscalibration import BatteryLevelsCalibrationTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BatteryLevelsCalibrationBusinessTestCase(BatteryLevelsCalibrationTestCase):
    """
    Validates Battery Levels Calibration business TestCases
    """
    @features('Feature1861')
    @features('EnabledBatteryFeature')
    @features('NoFeature1861Comparator')
    @level('Business', 'SmokeTests')
    @services('PowerSupply')
    def test_measure_battery_business(self):
        """
        Validate MeasureBattery Business case sequence

        Retrieve the ADC value of all range of voltage for device
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Disable cutoff')
        # ---------------------------------------------------------------------------
        self.post_requisite_cutoff = True

        BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
            self, cutoff_change_state_requested=True, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE,
            state_to_check=BatteryLevelsCalibration.CUTOFF_DISABLE)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over battery voltage values from full to cutoff by '
                                                        'step of 0.1')
        # ---------------------------------------------------------------------------
        number_of_values_to_test = int((self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage -
                                        self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage) / 0.1) + 1
        for i in [round(
                self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage - x*0.1, 1) for x in range(number_of_values_to_test)]:
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Send MeasureBattery with tuning the voltage = {i}V')
            # ---------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(i)
            sleep(UnifiedBatteryTestUtils.BATTERY_MEASURE_BLIND_WINDOW)
            measure_battery = self.feature_1861.measure_battery_cls(
                device_index=self.deviceIndex, feature_index=self.feature_1861_index)
            measure_battery_response = self.send_report_wait_response(
                report=measure_battery,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1861.measure_battery_response_cls)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Compare MeasureBattery.measure value and expected value with'
                                                          ' tolerance 5%')
            # ---------------------------------------------------------------------------
            # We multiply by 8 because it should be in mV
            cur_voltage_to_adc = round(1000 * self.power_supply_emulator.get_voltage() *
                                       self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_AdcCoefficient)

            if isinstance(measure_battery_response.measure, HexList):
                battery_adc = measure_battery_response.measure.toLong()
            else:
                battery_adc = measure_battery_response.measure
            # end if

            self.assertTrue(expr=(battery_adc <= cur_voltage_to_adc * 1.05) and
                                 (battery_adc >= cur_voltage_to_adc * .95),
                            msg=f'The measure parameter {battery_adc} is out of the expected range \
                                {cur_voltage_to_adc}')
        # end for
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        # Put back nominal voltage
        self.power_supply_emulator.set_voltage(voltage=self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage)

        self.testCaseChecked("BUS_1861_0001")
    # end def test_measure_battery_business

    @features('Feature1861')
    @features('EnabledBatteryFeature')
    @features('Feature1861Comparator')
    @level('Business')
    @services('PowerSupply')
    def test_measure_battery_business_with_comparator(self):
        """
        Validate MeasureBattery Business case sequence

        Check measureBattery thresholds for all valid ranges for device using a comparator.
        """
        self.post_requisite_set_nominal_voltage = True
        self.post_requisite_cutoff = True

        if self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage > \
                self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_CompVRef:
            comp_v_ref = self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage
        else:
            comp_v_ref = self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_CompVRef
        # end if
        min_mcu_voltage = self.f.PRODUCT.DEVICE.F_MCUMinOperatingVoltage if \
            self.f.PRODUCT.DEVICE.F_MCUMinOperatingVoltage else 0

        min_threshold = self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_CompMinThreshold
        max_threshold = self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_CompMaxThreshold

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Disable cutoff')
        # ---------------------------------------------------------------------------
        BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
            self, cutoff_change_state_requested=True, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE,
            state_to_check=BatteryLevelsCalibration.CUTOFF_DISABLE)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over comparator ranges')
        # ---------------------------------------------------------------------------
        power_supply_bias_correction = 0
        for threshold in reversed(range(min_threshold, max_threshold)):
            exp_low_threshold = threshold
            exp_high_threshold = threshold + 1
            exp_low_voltage = exp_low_threshold * (comp_v_ref / (max_threshold - min_threshold))
            exp_high_voltage = exp_high_threshold * (comp_v_ref / (max_threshold - min_threshold))
            raw_voltage = round(exp_low_voltage + (exp_high_voltage - exp_low_voltage) / 2 +
                                power_supply_bias_correction, PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1)

            if raw_voltage > self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage:
                # Skip if voltage is higher than maximum voltage
                continue
            # end if

            if raw_voltage < min_mcu_voltage:
                # break loop if the raw_voltage is less than minimum MCU operating voltage
                break
            # end if

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, f'Set voltage to {raw_voltage}V')
            # ---------------------------------------------------------------------------
            try:
                self.power_supply_emulator.set_voltage(raw_voltage)
            except AssertionError:
                self.log_traceback_as_warning(supplementary_message="Power Supply Emulator could not set voltage")
                break
            # end try
            sleep(2.0)

            power_supply_bias_correction = BatteryLevelsCalibrationTestUtils.check_comp_measure_battery(
                self, exp_low_threshold, exp_high_threshold, power_supply_bias_correction)
        # end for
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("BUS_1861_0001")
    # end def test_measure_battery_business

    @features('Feature1861')
    @level('Business')
    @services('PowerSupply')
    def test_store_calibration_business(self):
        """
        Validate StoreCalibration Business case sequence

        Verify if the return value from ReadCalibration is equal to StoreCalibration
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Disable cutoff')
        # ---------------------------------------------------------------------------
        self.post_requisite_cutoff = True

        BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
            self, cutoff_change_state_requested=True, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE,
            state_to_check=BatteryLevelsCalibration.CUTOFF_DISABLE)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Send ReadCalibration to store the current calibration')
        # ---------------------------------------------------------------------------
        try:
            read_calibration = self.feature_1861.read_calibration_cls(device_index=self.deviceIndex,
                                                                      feature_index=self.feature_1861_index)
            self.current_calibration = self.send_report_wait_response(
                report=read_calibration, response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1861.read_calibration_response_cls)
        except (AssertionError, QueueEmpty):
            pass
        # end try

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send GetBattCalibrationInfo')
        # ---------------------------------------------------------------------------
        get_batt_calibration_info = self.feature_1861.get_battery_calibration_info_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index)
        get_batt_calibration_info_response = self.send_report_wait_response(
            report=get_batt_calibration_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.get_battery_calibration_info_response_cls)

        precision_to_10_mv = PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1
        calibration_points_list = [
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_0)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_1)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_2)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_3)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_4)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_5)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_6)) / 1000, precision_to_10_mv)]

        calibration_points_list_to_store = [0] * 7

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over battery voltage values from full to cutoff by '
                                                        'step of 0.1')
        # ---------------------------------------------------------------------------
        """
         nRF52832 Power Reset
         A step increase in supply voltage of 300 mV or more, with rise time of 300 ms or less, within the valid supply 
         range, may result in a system reset.

         So the testing voltage values cannot be [cut-off, full]. Shall reverse it to [full, cut-off] to avoid trigger 
         MCU power reset mechanism.  

         Reference: nRF52832 datasheet "nRF52832_PS_v1.0", page 80 for more details.
         """
        for i in reversed(range(int(Numeral(get_batt_calibration_info_response.calibration_points_nb)))):
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send MeasureBattery with tuning the voltage to the requested '
                                                         'calibration point ' + str(calibration_points_list[i]) + 'V')
            # ---------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(calibration_points_list[i])
            measure_battery = self.feature_1861.measure_battery_cls(
                device_index=self.deviceIndex, feature_index=self.feature_1861_index)
            measure_battery_response = self.send_report_wait_response(
                report=measure_battery,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1861.measure_battery_response_cls)

            calibration_points_list_to_store[i] = int(Numeral(measure_battery_response.measure))
        # end for
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send StoreCalibration with the value gotten from MeasureBattery')
        # ---------------------------------------------------------------------------
        store_calibration = self.feature_1861.store_calibration_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index,
            calibration_points_nb=get_batt_calibration_info_response.calibration_points_nb,
            calibration_point_0=calibration_points_list_to_store[0],
            calibration_point_1=calibration_points_list_to_store[1],
            calibration_point_2=calibration_points_list_to_store[2],
            calibration_point_3=calibration_points_list_to_store[3],
            calibration_point_4=calibration_points_list_to_store[4],
            calibration_point_5=calibration_points_list_to_store[5],
            calibration_point_6=calibration_points_list_to_store[6])
        self.send_report_wait_response(report=store_calibration,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=self.feature_1861.store_calibration_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send ReadCalibration')
        # ---------------------------------------------------------------------------
        read_calibration = self.feature_1861.read_calibration_cls(device_index=self.deviceIndex,
                                                                  feature_index=self.feature_1861_index)
        read_calibration_response = self.send_report_wait_response(
            report=read_calibration,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.read_calibration_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate ReadCalibration.measuresNB')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=get_batt_calibration_info_response.calibration_points_nb,
                         obtained=read_calibration_response.calibration_points_nb,
                         msg='The measuresNB parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate ReadCalibration.reserved')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=int(Numeral(read_calibration_response.reserved)),
                         msg='The reserved parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate ReadCalibration.measures')
        # ---------------------------------------------------------------------------
        BatteryLevelsCalibrationTestUtils.compare_store_read_calibration(self, store_calibration=store_calibration,
                                                                         read_calibration=read_calibration_response)

        self.testCaseChecked("BUS_1861_0002")
    # end def test_store_calibration_business

    @features('Feature1861')
    @level('Business')
    def test_cut_off_control_business(self):
        """
        Validate CutOffControl Business case sequence

        Validate CutOffControl.cutOffEnabled value of each of the desiredState and changeStateRequested
        """
        self.post_requisite_cutoff = True
        cutoff_values_to_send = [(BatteryLevelsCalibration.CUTOFF_DISABLE, False),
                                 (BatteryLevelsCalibration.CUTOFF_DISABLE, True),
                                 (BatteryLevelsCalibration.CUTOFF_DISABLE, True),
                                 (BatteryLevelsCalibration.CUTOFF_ENABLE, False),
                                 (BatteryLevelsCalibration.CUTOFF_ENABLE, True),
                                 (BatteryLevelsCalibration.CUTOFF_ENABLE, True)]
        cutoff_values_to_check = [BatteryLevelsCalibration.CUTOFF_ENABLE, BatteryLevelsCalibration.CUTOFF_DISABLE,
                                  BatteryLevelsCalibration.CUTOFF_DISABLE, BatteryLevelsCalibration.CUTOFF_DISABLE,
                                  BatteryLevelsCalibration.CUTOFF_ENABLE, BatteryLevelsCalibration.CUTOFF_ENABLE]

        for i in range(len(cutoff_values_to_send)):
            # This function does test step 1 to 6, and check 1 to 6
            BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
                self, cutoff_change_state_requested=cutoff_values_to_send[i][1],
                cutoff_desired_state=cutoff_values_to_send[i][0], state_to_check=cutoff_values_to_check[i])
        # end for

        # If the test is done with no error, no need to enable cutoff in tear down function
        self.post_requisite_cutoff = False

        self.testCaseChecked("BUS_1861_0003")
    # end def test_cut_off_control_business

    @features('Feature1861v1+')
    @features('Feature1004v3+')
    @features('Feature1004BatteryMultiSourcing')
    @level('Business')
    def test_set_battery_source_info_business(self):
        """
        Validate setBatterySourceInfo business case

        [5] setBatterySourceInfo(battery_source_index) -> batterySourceInfo
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send SetBatterySourceInfo')
        # ---------------------------------------------------------------------------
        set_battery_source_info = self.feature_1861.set_battery_source_info_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index,
            battery_source_index=self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_BatterySourceIndex)
        set_battery_source_info_response = self.send_report_wait_response(
            report=set_battery_source_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.set_battery_source_info_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate SetBatterySourceInfo.battery_source_index value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=Numeral(self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_BatterySourceIndex),
                         obtained=set_battery_source_info_response.battery_source_index,
                         msg='The battery_source_index parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send get_capabilities request')
        # ---------------------------------------------------------------------------
        get_capabilities_response = UnifiedBatteryTestUtils.HIDppHelper.get_capabilities(self)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check battery_source_index parameter')
        # ---------------------------------------------------------------------------
        UnifiedBatteryTestUtils.GetCapabilitiesResponseChecker.check_fields(test_case=self,
                                                                            message=get_capabilities_response,
                                                                            expected_cls=GetCapabilitiesResponseV0ToV1)

        self.testCaseChecked("BUS_1861_0004")
    # end def test_set_battery_source_info_business
# end class BatteryLevelsCalibrationBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
