#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1861.robustness
:brief: HID++ 2.0 Battery Levels Calibration robustness test suite
:author: Christophe Roquebert
:date: 2021/04/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from unittest import expectedFailure

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.hidpp20.common.feature_1861.batterylevelscalibration import BatteryLevelsCalibrationTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BatteryLevelsCalibrationRobustnessTestCase(BatteryLevelsCalibrationTestCase):
    """
    Validates Battery Levels Calibration robustness TestCases
    """

    @features('Feature1861')
    @level('Robustness')
    @services('PowerSupply')
    def test_store_calibration_reserved_ignored(self):
        """
        Validate StoreCalibration with other reserved

        Test reserved of the StoreCalibration will be flushed
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
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over values of Reserved other than 0')
        # ---------------------------------------------------------------------------
        for wrong_reserved in compute_wrong_range(
                0, max_value=(1 << self.feature_1861.store_calibration_cls.LEN.RESERVED) - 1):
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send StoreCalibration with reserved = ' + str(wrong_reserved))
            # ---------------------------------------------------------------------------
            store_calibration = self.feature_1861.store_calibration_cls(
                device_index=self.deviceIndex, feature_index=self.feature_1861_index,
                calibration_points_nb=self.current_calibration.calibration_points_nb,
                calibration_point_0=self.current_calibration.calibration_point_0,
                calibration_point_1=self.current_calibration.calibration_point_1,
                calibration_point_2=self.current_calibration.calibration_point_2,
                calibration_point_3=self.current_calibration.calibration_point_3,
                calibration_point_4=self.current_calibration.calibration_point_4,
                calibration_point_5=self.current_calibration.calibration_point_5,
                calibration_point_6=self.current_calibration.calibration_point_6)
            store_calibration.reserved = wrong_reserved
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
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate ReadCalibration.measures')
            # ---------------------------------------------------------------------------
            BatteryLevelsCalibrationTestUtils.compare_store_read_calibration(
                self, store_calibration=store_calibration, read_calibration=read_calibration_response)
        # end for
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        # No need to reload the initial calibration in the tear down as the compare function pass successfully and
        # we are only testing the reserved bits of the interface.
        self.current_calibration = None

        self.testCaseChecked("ROB_1861_0001")
    # end def test_store_calibration_reserved_ignored

    # TODO This need to check if the number of calibration points needed is lower than 7
    @features('Feature1861')
    @level('Robustness')
    @services('PowerSupply')
    def test_store_calibration_more_calibration_point(self):
        """
        Validate StoreCalibration with quantity of measures greater than calibPointsNb

        none = [2]StoreCalibration(calibPointsNb, reserved, measures)
        Request: 0x11.DeviceIndex.FeatureIndex.2F.02.00.calibPoint1.calibPoint2.calibPoint3
        Test calibPoint3 will be flushed
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
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send StoreCalibration with the quantity of measures > '
                                                     'calibPointsNb')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        calibration_points_list = [0]*7
        for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb + 1):
            calibration_points_list[i] = 0x1010
        # end for
        store_calibration = self.feature_1861.store_calibration_cls(
                device_index=self.deviceIndex, feature_index=self.feature_1861_index,
                calibration_points_nb=f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb,
                calibration_point_0=calibration_points_list[0],
                calibration_point_1=calibration_points_list[1],
                calibration_point_2=calibration_points_list[2],
                calibration_point_3=calibration_points_list[3],
                calibration_point_4=calibration_points_list[4],
                calibration_point_5=calibration_points_list[5],
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
            report=read_calibration, response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_1861.read_calibration_response_cls)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate ReadCalibration response received (minus the extra '
                                                      'calibration points)')
        # ---------------------------------------------------------------------------
        calibration_points_list[f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb] = 0
        store_calibration.calibration_points_nb = \
            f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb
        store_calibration.calibration_point_0 = calibration_points_list[0]
        store_calibration.calibration_point_1 = calibration_points_list[1]
        store_calibration.calibration_point_2 = calibration_points_list[2]
        store_calibration.calibration_point_3 = calibration_points_list[3]
        store_calibration.calibration_point_4 = calibration_points_list[4]
        store_calibration.calibration_point_5 = calibration_points_list[5]
        store_calibration.calibration_point_6 = calibration_points_list[6]
        BatteryLevelsCalibrationTestUtils.compare_store_read_calibration(
            self, store_calibration=store_calibration, read_calibration=read_calibration_response)

        self.testCaseChecked("ROB_1861_0002")
    # end def test_store_calibration_more_calibration_point

    @features('Feature1861')
    @level('Robustness')
    def test_cutoff_control_reserved_ignored(self):
        """
        Validate CutOffControl with other reserved bits

        Test reserved bits will be flushed
        """

        self.post_requisite_cutoff = True

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over values of Reserved other than 0')
        # ---------------------------------------------------------------------------
        desired_state = BatteryLevelsCalibration.CUTOFF_DISABLE
        for wrong_reserved in compute_wrong_range(
                                    value=0,
                                    max_value=(1 << self.feature_1861.cut_off_control_cls.LEN.RESERVED) - 1):
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send CutOffControl with reserved = 0x%X' % wrong_reserved)
            # ---------------------------------------------------------------------------
            cutoff_control = self.feature_1861.cut_off_control_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_1861_index,
                cutoff_change_state_requested=True,
                cutoff_desired_state=desired_state)
            cutoff_control.reserved = wrong_reserved
            cutoff_control_response = self.send_report_wait_response(
                report=cutoff_control,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1861.cut_off_control_response_cls)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate CutOffControl response received')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=desired_state,
                             obtained=int(Numeral(cutoff_control_response.cutoff_state)),
                             msg='The cutoffState parameter differs from the one expected')

            if desired_state == BatteryLevelsCalibration.CUTOFF_DISABLE:
                desired_state = BatteryLevelsCalibration.CUTOFF_ENABLE
            else:
                desired_state = BatteryLevelsCalibration.CUTOFF_DISABLE
        # end for
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROB_1861_0003")
    # end def test_cutoff_control_reserved_ignored

    @features('Feature1861')
    @level('Robustness')
    def test_get_batt_calibration_wrong_software_id(self):
        """
        Validates Battery Level Calibration softwareId are ignored

        calibPointsNb, reserved, calibPoints = [0]GetBattCalibrationInfo()
        Request: 0x10.DeviceIndex.FeatureIndex.0x00.0x00.0x00.0x00
        """

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over values of SoftwareId other than 0')
        # ---------------------------------------------------------------------------
        for wrong_software_id in compute_wrong_range(
                0xF, max_value=(1 << self.feature_1861.get_battery_calibration_info_response_cls.LEN.SOFTWARE_ID) - 1):
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send GetBattCalibrationInfo with softwareId = 0x%X' %
                                                   wrong_software_id)
            # ---------------------------------------------------------------------------
            get_batt_calibration_info = self.feature_1861.get_battery_calibration_info_cls(
                device_index=self.deviceIndex, feature_index=self.feature_1861_index)
            get_batt_calibration_info.softwareId = wrong_software_id
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
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPoints'
                                                          '[0..calibPointsNb-1] value')
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
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPoints'
                                                          '[calibPointsNb..7] = 0')
            # ---------------------------------------------------------------------------
            for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb,
                           BatteryLevelsCalibration.MAX_NUMBER_OF_CALIBRATION_POINTS):
                self.assertEqual(expected=HexList(Numeral(0, 2)),
                                 obtained=calibration_points_list[i],
                                 msg='The calibPoints[' + str(i) + '] parameter differs from the one expected')
            # end for
        # end for
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROB_1861_0004")
    # end def test_get_batt_calibration_wrong_software_id

    @features('Feature1861')
    @level('Robustness')
    def test_get_batt_calibration_padding_ignored(self):
        """
        Validates Battery Levels Calibration padding bytes are ignored

        calibPointsNb, reserved, calibPoints = [0]GetBattCalibrationInfo()
        Request: 0x10.DeviceIndex.FeatureIndex.0x0F.0xAA.0xBB.0xCC
        """

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'Test Loop over values of Padding other than 0')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(
                self.feature_1861.get_battery_calibration_info_cls.DEFAULT.PADDING,
                self.feature_1861.get_battery_calibration_info_cls.LEN.PADDING // 8))):
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send GetBattCalibrationInfo with padding = 0x' +
                                                   str(padding_byte))
            # ---------------------------------------------------------------------------
            get_batt_calibration_info = self.feature_1861.get_battery_calibration_info_cls(
                device_index=self.deviceIndex, feature_index=self.feature_1861_index)
            get_batt_calibration_info.padding = padding_byte
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
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPoints'
                                                          '[0..calibPointsNb-1] value')
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
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate GetBattCalibrationInfo.calibPoints'
                                                          '[calibPointsNb..7] = 0')
            # ---------------------------------------------------------------------------
            for i in range(f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION.F_RequiredCalibrationPointNb,
                           BatteryLevelsCalibration.MAX_NUMBER_OF_CALIBRATION_POINTS):
                self.assertEqual(expected=HexList(Numeral(0, 2)),
                                 obtained=calibration_points_list[i],
                                 msg='The calibPoints[' + str(i) + '] parameter differs from the one expected')
            # end for
        # end for
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_title_2(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROB_1861_0005")
    # end def test_get_batt_calibration_padding_ignored

    @features('Feature1861v1+')
    @features('Feature1004v3+')
    @features('NoFeature1004BatteryMultiSourcing')
    @level('Robustness')
    @expectedFailure  # https://jira.logitech.io/browse/NRF52-101
    def test_set_battery_source_info_not_supported(self):
        """
        [5] setBatterySourceInfo(battery_source_index) -> batterySourceInfo
        Use to set battery information in case of multi-sourcing support.

        Check function is not supported if multi-sourcing is not supported.
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send SetBatterySourceInfo')
        # ---------------------------------------------------------------------------
        set_battery_source_info = self.feature_1861.set_battery_source_info_cls(
            device_index=self.deviceIndex, feature_index=self.feature_1861_index,
            battery_source_index=self.feature_1861.set_battery_source_info_cls.DEFAULT.BATTERY_SOURCE_INDEX)
        err_resp = self.send_report_wait_response(
            report=set_battery_source_info,
            response_queue=self.hidDispatcher.error_message_queue,
            response_class_type=Hidpp2ErrorCodes)

        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check HIDPP_ERR_INVALID_FUNCTION_ID (7) Error Code returned by '
                                                      'the device')
        # ----------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
            test_case=self,
            error_message=err_resp,
            feature_index=set_battery_source_info.featureIndex,
            function_index=set_battery_source_info.functionIndex,
            error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID])

        self.testCaseChecked("ROB_1861_0006")
    # end def test_set_battery_source_info_not_supported
# end class BatteryLevelsCalibrationRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
