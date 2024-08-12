#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1861.functionality
:brief: HID++ 2.0 Battery Levels Calibration functionality test suite
:author: Christophe Roquebert
:date: 2021/04/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1861.batterylevelscalibration import BatteryLevelsCalibrationTestCase
from time import sleep

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BatteryLevelsCalibrationFunctionalityTestCase(BatteryLevelsCalibrationTestCase):
    """
    Validates Battery Levels Calibration functionality TestCases
    """
    @features('Feature1861')
    @features('NoFeature1861Comparator')
    @level('Functionality')
    @services('PowerSupply')
    def test_measure_battery_calibration_point(self):
        """
        Validate MeasureBattery with all calibration point

        Retrieve the ADC value of every calibration points
        """

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Disable cutoff')
        # ---------------------------------------------------------------------------
        self.post_requisite_cutoff = True

        BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
            self, cutoff_change_state_requested=True, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE,
            state_to_check=BatteryLevelsCalibration.CUTOFF_DISABLE)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over the number of calibration points')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        """
        nRF52832 Power Reset
        A step increase in supply voltage of 300 mV or more, with rise time of 300 ms or less, within the valid supply 
        range, may result in a system reset.
        
        So the testing voltage values cannot be [cut-off, full]. Shall reverse it to [full, cut-off] to avoid trigger 
        MCU power reset mechanism.  
        
        Reference: nRF52832 datasheet "nRF52832_PS_v1.0", page 80 for more details.
        """
        for i in reversed(range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb)):
            v = round(int(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPoints[i], 16)/1000,
                      PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1)
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(
                self, 'Send MeasureBattery with tuning the voltage to the requested  calibration point ' + str(v) + 'V')
            # ---------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(voltage=v)

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
                                       f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_AdcCoefficient)

            if isinstance(measure_battery_response.measure, HexList):
                battery_adc = measure_battery_response.measure.toLong()
            else:
                battery_adc = measure_battery_response.measure
            # end if

            self.assertTrue(
                expr=(battery_adc <= cur_voltage_to_adc * 1.05) and (battery_adc >= cur_voltage_to_adc * .95),
                msg=f'The measure parameter {battery_adc} is out of the expected range {cur_voltage_to_adc}')
        # end for
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FUN_1861_0001")
    # end def test_measure_battery_calibration_point

    @features('Feature1861')
    @level('Functionality')
    @services('PowerSupply')
    def test_store_calibration_functionality(self):
        """
        Validate StoreCalibration with boundary value for each measures bytes

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
        read_calibration = self.feature_1861.read_calibration_cls(device_index=self.deviceIndex,
                                                                  feature_index=self.feature_1861_index)
        self.current_calibration = self.send_report_wait_response(
            report=read_calibration, response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.read_calibration_response_cls)

        calibration_values_to_test = [0x0000, 0xFFFF]
        for calibration_value in calibration_values_to_test:
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send StoreCalibration with the all calibrationPoint = '
                                                         '0x%04X' % calibration_value)
            # ---------------------------------------------------------------------------
            f = self.getFeatures()
            calibration_points_list = [0]*7
            for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb):
                calibration_points_list[i] = calibration_value
            # end for
            store_calibration = self.feature_1861.store_calibration_cls(
                device_index=self.deviceIndex, feature_index=self.feature_1861_index,
                calibration_points_nb=f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb,
                calibration_point_0=calibration_points_list[0], calibration_point_1=calibration_points_list[1],
                calibration_point_2=calibration_points_list[2], calibration_point_3=calibration_points_list[3],
                calibration_point_4=calibration_points_list[4], calibration_point_5=calibration_points_list[5],
                calibration_point_6=calibration_points_list[6])
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
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate the ReadCalibration.measures value if it\'s equal '
                                                          'to StoreCalibration.measures')
            # ---------------------------------------------------------------------------
            BatteryLevelsCalibrationTestUtils.compare_store_read_calibration(self, store_calibration=store_calibration,
                                                                             read_calibration=read_calibration_response)
        # end for

        self.testCaseChecked("FUN_1861_0002")
    # end def test_store_calibration_functionality

    @features('Feature1861')
    @features('EnabledBatteryFeature')
    @level('Functionality')
    @services('PowerSupply')
    def test_cut_off_disabled_functionality(self):
        """
        Validate switching between cutoff disable and enable

        Verify if the state have been change successfully
        """

        self.post_requisite_cutoff = True

        # This function does test step 1 and test check 1
        BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
            self, cutoff_change_state_requested=True, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE,
            state_to_check=BatteryLevelsCalibration.CUTOFF_DISABLE)

        required_voltage = round(self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage * 98 / 100,
                                 PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1)
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, f'Tune the voltage 2% below the cutoff voltage (i.e '
                                                     f'{required_voltage})')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(voltage=required_voltage)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send MeasureBattery')
        # ---------------------------------------------------------------------------
        measure_battery = self.feature_1861.measure_battery_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index)
        measure_battery_response = self.send_report_wait_response(
            report=measure_battery, response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.measure_battery_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate MeasureBattery response received and \'measure\' value '
                                                      'is not equal to 0')
        # ---------------------------------------------------------------------------
        self.assertNotEqual(unexpected=0,
                            obtained=int(Numeral(measure_battery_response.measure)),
                            msg='The measure parameter is equal to 0')

        # Put back nominal voltage
        self.power_supply_emulator.set_voltage(voltage=self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage)

        self.testCaseChecked("FUN_1861_0003")
    # end def test_cut_off_disabled_functionality

    @features('Feature1861')
    @features('EnabledBatteryFeature')
    @level('Functionality')
    @services('PowerSupply')
    @bugtracker('BatteryLevelsCalibration_Cut_Off')
    def test_cut_off_enabled_functionality(self):
        """
        Validate switching between cutoff disable and enable

        Verify if the state have been change successfully
        """
        self.reset_device = True

        BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
            self, cutoff_change_state_requested=False, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE,
            state_to_check=BatteryLevelsCalibration.CUTOFF_ENABLE)

        required_voltage = round(self.f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage * 98 / 100,
                                 PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1)
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, f'Tune the voltage 2% below the cutoff voltage (i.e '
                                                     f'{required_voltage})')
        # ---------------------------------------------------------------------------
        self.power_supply_emulator.set_voltage(voltage=required_voltage)
        sleep(self.f.PRODUCT.DEVICE.BATTERY.F_BatteryMeasureBlindWindow)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send MeasureBattery')
        # ---------------------------------------------------------------------------
        measure_battery = self.feature_1861.measure_battery_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index)
        self.send_report_to_device(report=measure_battery)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate no response returned')
        # ---------------------------------------------------------------------------
        self.check_queue_empty(queue=self.hidDispatcher.common_message_queue, during=.5)

        self.testCaseChecked("FUN_1861_0004")
    # end def test_cut_off_enabled_functionality

    @features('Feature1861')
    @level('Functionality')
    def test_cut_off_control_functionality(self):
        """
        Validate switching between cutoff disable and enable

        Verify if the state have been change successfully
        """

        self.post_requisite_cutoff = True
        cutoff_values_to_send = [(BatteryLevelsCalibration.CUTOFF_DISABLE, True),
                                 (BatteryLevelsCalibration.CUTOFF_ENABLE, True)]
        cutoff_values_to_check = [BatteryLevelsCalibration.CUTOFF_DISABLE, BatteryLevelsCalibration.CUTOFF_ENABLE]

        for i in range(len(cutoff_values_to_send)):
            # This function does test step 1 and 2, and check 1 and 2
            BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
                self, cutoff_change_state_requested=cutoff_values_to_send[i][1],
                cutoff_desired_state=cutoff_values_to_send[i][0], state_to_check=cutoff_values_to_check[i])
        # end for

        # If the test is done with no error, no need to enable cutoff in tear down function
        self.post_requisite_cutoff = False

        self.testCaseChecked("FUN_1861_0005")
    # end def test_cut_off_control_functionality

    @features('Feature1861v1+')
    @features('Feature1004BatteryMultiSourcing')
    @level('Functionality')
    def test_set_battery_source_info_functionality(self):
        """
        Validate we can set the battery source index and read it back using the 0x1004 get capabilities request

        [5] setBatterySourceInfo(battery_source_index) -> batterySourceInfo
        """
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        self.post_requisite_reload_nvs = True

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over values of source index other than 0')
        # ---------------------------------------------------------------------------
        for source_index in range(1, self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_BatterySourceIndex + 1):
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send SetBatterySourceInfo')
            # ---------------------------------------------------------------------------
            set_battery_source_info = self.feature_1861.set_battery_source_info_cls(
                device_index=self.deviceIndex, feature_index=self.feature_1861_index, battery_source_index=source_index)
            set_battery_source_info_response = self.send_report_wait_response(
                report=set_battery_source_info,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1861.set_battery_source_info_response_cls)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate SetBatterySourceInfo.battery_source_index value')
            # ---------------------------------------------------------------------------

            self.assertEqual(expected=Numeral(source_index),
                             obtained=set_battery_source_info_response.battery_source_index,
                             msg='The battery_source_index parameter differs from the one expected')

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send get_capabilities request')
            # ---------------------------------------------------------------------------
            get_capabilities_response = UnifiedBatteryTestUtils.HIDppHelper.get_capabilities(self)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Check battery_source_index parameter')
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(get_capabilities_response.battery_source_index)),
                             expected=int(source_index),
                             msg="The battery_source_index parameter differs from the one expected")
        # end for

        self.testCaseChecked("FUN_1861_0006")
    # end def test_set_battery_source_info_business

# end class BatteryLevelsCalibrationFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
