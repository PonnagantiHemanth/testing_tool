#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1861.interface
:brief: HID++ 2.0 Battery Levels Calibration interface test suite
:author: Christophe Roquebert
:date: 2021/04/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from math import floor
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.hidpp20.common.feature_1861.batterylevelscalibration import BatteryLevelsCalibrationTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BatteryLevelsCalibrationInterfaceTestCase(BatteryLevelsCalibrationTestCase):
    """
    Validates Battery Levels Calibration interface TestCases
    """

    @features('Feature1861')
    @level('Interface')
    def test_get_battery_calibration_info_api(self):
        """
        @tc_synopsis    Validate GetBattCalibrationInfo normal processing

        [0] getBattCalibrationInfo() -> calibPointsNb, reserved, calibPoints
        """

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send GetBattCalibrationInfo')
        # ---------------------------------------------------------------------------
        get_batt_calibration_info = self.feature_1861.get_battery_calibration_info_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index)
        get_batt_calibration_info_response = self.send_report_wait_response(
            report=get_batt_calibration_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.get_battery_calibration_info_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPointsNb value')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        self.assertEqual(
            expected=HexList(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb),
            obtained=get_batt_calibration_info_response.calibration_points_nb,
            msg='The calibPointsNb parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.reserved value = 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList(0),
                         obtained=get_batt_calibration_info_response.reserved,
                         msg='The reserved parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPoints[0..calibPointsNb-1] '
                                                      'value')
        # ---------------------------------------------------------------------------
        calibration_points_list = [get_batt_calibration_info_response.calibration_point_0,
                                   get_batt_calibration_info_response.calibration_point_1,
                                   get_batt_calibration_info_response.calibration_point_2,
                                   get_batt_calibration_info_response.calibration_point_3,
                                   get_batt_calibration_info_response.calibration_point_4,
                                   get_batt_calibration_info_response.calibration_point_5,
                                   get_batt_calibration_info_response.calibration_point_6]
        for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb):
            self.assertEqual(expected=HexList(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.
                                              F_RequiredCalibrationPoints[i]),
                             obtained=calibration_points_list[i],
                             msg='The calibPoints[' + str(i) + '] parameter differs from the one expected')
        # end for

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPoints[calibPointsNb..7] = '
                                                      '0')
        # ---------------------------------------------------------------------------
        for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb,
                       BatteryLevelsCalibration.MAX_NUMBER_OF_CALIBRATION_POINTS):
            self.assertEqual(expected=HexList(Numeral(0, 2)),
                             obtained=calibration_points_list[i],
                             msg='The calibPoints[' + str(i) + '] parameter differs from the one expected')
        # end for

        self.testCaseChecked("INT_1861_0001")
    # end def test_get_battery_calibration_info_api

    @features('Feature1861')
    @features('NoFeature1861Comparator')
    @level('Interface')
    @services('PowerSupply')
    def test_measure_battery_api(self):
        """
        @tc_synopsis    Validate MeasureBattery() normal processing

        [1] measureBattery() -> measure
        """

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send MeasureBattery')
        # ---------------------------------------------------------------------------
        measure_battery = self.feature_1861.measure_battery_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index)
        measure_battery_response = self.send_report_wait_response(
            report=measure_battery, response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.measure_battery_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Compare MeasureBattery.measure value and expected value with '
                                                      'tolerance 5%')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        # We multiply by 8 because it should be in mV
        cur_voltage_to_adc = round(1000 * self.power_supply_emulator.get_voltage() *
                                   f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_AdcCoefficient)

        battery_adc = int(Numeral(measure_battery_response.measure))

        self.assertTrue(expr=(battery_adc <= cur_voltage_to_adc * 1.05) and (battery_adc >= cur_voltage_to_adc * .95),
                        msg='The measure parameter is out of the expected range')

        self.testCaseChecked("INT_1861_0002")
    # end def test_measure_battery_api

    @features('Feature1861')
    @features('Feature1861Comparator')
    @level('Interface')
    @services('PowerSupply')
    def test_measure_battery_api_with_comparator(self):
        """
        @tc_synopsis    Validate MeasureBattery() normal processing

        [1] measureBattery() -> measure
        """
        if self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage > \
                self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_CompVRef:
            comp_v_ref = self.f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage
        else:
            comp_v_ref = self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_CompVRef
        # end if
        min_threshold = self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_CompMinThreshold
        max_threshold = self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_CompMaxThreshold

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Get raw input voltage')
        # ---------------------------------------------------------------------------
        raw_voltage = self.power_supply_emulator.get_voltage()
        CommonBaseTestUtils.LogHelper.log_info(self, f'Input voltage is {raw_voltage}')

        exp_low_threshold = floor(raw_voltage / (comp_v_ref / (max_threshold - min_threshold)))
        exp_high_threshold = exp_low_threshold + 1

        BatteryLevelsCalibrationTestUtils.check_comp_measure_battery(self, exp_low_threshold, exp_high_threshold)

        self.testCaseChecked("INT_1861_0002")
    # end def test_measure_battery_api_with_comparator

    @features('Feature1861')
    @level('Interface')
    @services('PowerSupply')
    def test_store_calibration_api(self):
        """
        @tc_synopsis    Validate StoreCalibration normal processing

        [2] StoreCalibration(calibPointsNb, reserved, measures) -> none
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
        read_calibration = self.feature_1861.read_calibration_cls(device_index=self.deviceIndex,
                                                                  feature_index=self.feature_1861_index)
        self.current_calibration = self.send_report_wait_response(
            report=read_calibration, response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.read_calibration_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send StoreCalibration with the all calibrationPoint = 0x1010')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        calibration_points_list = [0]*7
        for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb):
            calibration_points_list[i] = 0x1010
        # end for
        store_calibration = self.feature_1861.store_calibration_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index,
            calibration_points_nb=f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb,
            calibration_point_0=calibration_points_list[0], calibration_point_1=calibration_points_list[1],
            calibration_point_2=calibration_points_list[2], calibration_point_3=calibration_points_list[3],
            calibration_point_4=calibration_points_list[4], calibration_point_5=calibration_points_list[5],
            calibration_point_6=calibration_points_list[6])
        store_calibration_response = self.send_report_wait_response(
            report=store_calibration,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.store_calibration_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate StoreCalibration.featureIndex value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=self.feature_1861_index,
                         obtained=int(Numeral(store_calibration_response.featureIndex)),
                         msg='The featureIndex parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate StoreCalibration.padding value')
        # ---------------------------------------------------------------------------
        self.assertEqual(
            expected=HexList(Numeral(source=0, byteCount=(
                    self.feature_1861.store_calibration_response_cls.LEN.PADDING // 8))),
            obtained=store_calibration_response.padding, msg='The padding parameter differs from the one expected')

        self.testCaseChecked("INT_1861_0003")
    # end def test_store_calibration_api

    @features('Feature1861')
    @level('Interface')
    @services('PowerSupply')
    def test_read_calibration_api(self):
        """
        @tc_synopsis    Validate ReadCalibration normal processing

        [3] ReadCalibration() -> calibPointsNb, reserved, measures
        """

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send ReadCalibration')
        # ---------------------------------------------------------------------------
        read_calibration = self.feature_1861.read_calibration_cls(device_index=self.deviceIndex,
                                                                  feature_index=self.feature_1861_index)

        # If got "the device didn't send expected message after 2 seconds" error here, shall make sure to store battery
        # level calibration values in NVS. And for CI pipeline test, nvs_raspberry_PI_x.hex shall contain the values of
        # batter level calibration.
        read_calibration_response = self.send_report_wait_response(
            report=read_calibration, response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.read_calibration_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPointsNb value')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        self.assertEqual(
            expected=HexList(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb),
            obtained=read_calibration_response.calibration_points_nb,
            msg='The calibPointsNb parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.reserved value = 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList(0),
                         obtained=read_calibration_response.reserved,
                         msg='The reserved parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPoints[0..calibPointsNb-1] '
                                                      'value')
        # ---------------------------------------------------------------------------
        calibration_points_list = [read_calibration_response.calibration_point_0,
                                   read_calibration_response.calibration_point_1,
                                   read_calibration_response.calibration_point_2,
                                   read_calibration_response.calibration_point_3,
                                   read_calibration_response.calibration_point_4,
                                   read_calibration_response.calibration_point_5,
                                   read_calibration_response.calibration_point_6]

        # The calibration values because it is device dependent (not product dependent) so just a check of non-zero
        # values is coherent
        for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb):
            self.assertNotEqual(unexpected=HexList(Numeral(0, 2)),
                                obtained=calibration_points_list[i],
                                msg='The calibPoints[' + str(i) + '] parameter differs from the one expected')
        # end for

        for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb,
                       BatteryLevelsCalibration.MAX_NUMBER_OF_CALIBRATION_POINTS):
            self.assertEqual(expected=HexList(Numeral(0, 2)),
                             obtained=calibration_points_list[i],
                             msg='The calibPoints[' + str(i) + '] parameter differs from the one expected')
        # end for

        self.testCaseChecked("INT_1861_0004")
    # end def test_read_calibration_api

    @features('Feature1861')
    @level('Interface')
    def test_cut_off_control_api(self):
        """
        @tc_synopsis    Validate CutOffControl normal processing

        [4] CutOffControl(desiredState, changeStateRequested) -> cutoffState
        """
        # This function does test step 1, and check 1
        BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(self)

        self.testCaseChecked("INT_1861_0005")
    # end def test_cut_off_control_api

    @features('Feature1861v1+')
    @features('Feature1004BatteryMultiSourcing')
    @level('Interface')
    def test_set_battery_source_info(self):
        """
        Validate setBatterySourceInfo API

        [5] setBatterySourceInfo(battery_source_index) -> batterySourceInfo
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Backup NVS')
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send SetBatterySourceInfo')
        # ---------------------------------------------------------------------------
        set_battery_source_info = self.feature_1861.set_battery_source_info_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index, battery_source_index=1)
        set_battery_source_info_response = self.send_report_wait_response(
            report=set_battery_source_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.set_battery_source_info_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate SetBatterySourceInfo.battery_source_index value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=Numeral(1),
                         obtained=set_battery_source_info_response.battery_source_index,
                         msg='The battery_source_index parameter differs from the one expected')

        self.testCaseChecked("INT_1861_0006")
    # end def test_set_battery_source_info
# end class BatteryLevelsCalibrationInterfaceTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
