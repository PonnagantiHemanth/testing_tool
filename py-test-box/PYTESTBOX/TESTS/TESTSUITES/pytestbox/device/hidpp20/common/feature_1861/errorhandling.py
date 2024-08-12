#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1861.errorhandling
:brief: HID++ 2.0 Battery Levels Calibration errorhandling test suite
:author: Christophe Roquebert
:date: 2021/04/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.hidpp20.common.feature_1861.batterylevelscalibration import BatteryLevelsCalibrationTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BatteryLevelsCalibrationErrorHandlingTestCase(BatteryLevelsCalibrationTestCase):
    """
    Validates Battery Levels Calibration Error Handling TestCases
    """
    @features('Feature1861')
    @level('ErrorHandling')
    def test_get_batt_calibration_info_wrong_function_index(self):
        """
        Validates Battery Levels Calibration robustness processing

        Function indexes valid range [0..4] in v0 & [0..5] in v1
          Tests wrong indexes
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send GetBattCalibrationInfo')
        # ---------------------------------------------------------------------------
        get_batt_calibration_info = self.feature_1861.get_battery_calibration_info_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index)
        get_batt_calibration_info.functionIndex = self.feature_1861.get_max_function_index() + 1
        get_batt_calibration_info_response = self.send_report_wait_response(
            report=get_batt_calibration_info,
            response_queue=self.hidDispatcher.error_message_queue,
            response_class_type=ErrorCodes)

        self.check_queue_empty(queue=self.hidDispatcher.common_message_queue, during=.1)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check Error Codes InvalidFunctionId (7) returned by the device')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList(ErrorCodes.INVALID_FUNCTION_ID),
                         obtained=get_batt_calibration_info_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ERR_1861_0001")
    # end def test_get_batt_calibration_info_wrong_function_index

    @features('Feature1861')
    @level('ErrorHandling')
    @services('PowerSupply')
    def test_store_calibration_wrong_measures_nb(self):
        """
        Validate StoreCalibration with wrong measuresNb

        measuresNb valid range [Constant / product]
        Tests wrong measuresNb
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
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send StoreCalibration')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        store_calibration = self.feature_1861.store_calibration_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index,
            calibration_points_nb=f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb + 1)
        store_calibration_response = self.send_report_wait_response(
            report=store_calibration,
            response_queue=self.hidDispatcher.error_message_queue,
            response_class_type=ErrorCodes)

        self.check_queue_empty(queue=self.hidDispatcher.common_message_queue, during=.1)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check Error Codes InvalidArgument (2) returned by the device')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                         obtained=store_calibration_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ERR_1861_0002")
    # end def test_store_calibration_wrong_measures_nb
# end class BatteryLevelsCalibrationErrorHandlingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
