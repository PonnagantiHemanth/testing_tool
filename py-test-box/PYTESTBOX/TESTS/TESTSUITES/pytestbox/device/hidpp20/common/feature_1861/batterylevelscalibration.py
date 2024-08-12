#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1861.batterylevelscalibration
:brief: HID++ 2.0 Battery Levels Calibration test case
:author: Christophe Roquebert
:date: 2021/04/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationFactory
from pyhid.hidpp.features.common.batterylevelscalibration import StoreCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import StoreCalibrationResponse
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BatteryLevelsCalibrationTestCase(BaseTestCase):
    """
    Validates Battery Levels Calibration in Application mode
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.reset_device = False
        self.current_calibration = None
        self.post_requisite_cutoff = False
        self.post_requisite_reload_nvs = False
        self.post_requisite_set_nominal_voltage = False

        super().setUp()

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1861)')
        # ---------------------------------------------------------------------------
        self.feature_1861_index = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, BatteryLevelsCalibration.FEATURE_ID)
        self.feature_1861 = BatteryLevelsCalibrationFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.BATTERY_LEVELS_CALIBRATION))

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Enable Manufacturing Features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_set_nominal_voltage:
                # Put back nominal voltage
                self.power_supply_emulator.set_voltage(voltage=self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage)
            # end if

            if self.reset_device:
                # ---------------------------------------------------------------------------
                CommonBaseTestUtils.LogHelper.log_post_requisite(self, 'Power off and restart the device')
                # ---------------------------------------------------------------------------
                self.reset(hardware_reset=True)

                self.reset_device = False
            # end if

            if self.current_calibration is not None:
                # ---------------------------------------------------------------------------
                CommonBaseTestUtils.LogHelper.log_post_requisite(self,
                                                                 'Send StoreCalibration with initial calibration value')
                # ---------------------------------------------------------------------------
                store_calibration = StoreCalibration(device_index=self.deviceIndex,
                                                     feature_index=self.feature_1861_index,
                                                     calibration_points_nb=self.current_calibration.calibration_points_nb,
                                                     calibration_point_0=self.current_calibration.calibration_point_0,
                                                     calibration_point_1=self.current_calibration.calibration_point_1,
                                                     calibration_point_2=self.current_calibration.calibration_point_2,
                                                     calibration_point_3=self.current_calibration.calibration_point_3,
                                                     calibration_point_4=self.current_calibration.calibration_point_4,
                                                     calibration_point_5=self.current_calibration.calibration_point_5,
                                                     calibration_point_6=self.current_calibration.calibration_point_6)
                self.send_report_wait_response(report=store_calibration,
                                               response_queue=self.hidDispatcher.common_message_queue,
                                               response_class_type=StoreCalibrationResponse)

                self.current_calibration = None
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        # noinspection PyBroadException
        try:
            if self.post_requisite_cutoff:
                # ---------------------------------------------------------------------------
                CommonBaseTestUtils.LogHelper.log_post_requisite(self, 'Enable cutoff')
                # ---------------------------------------------------------------------------
                BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
                    self, cutoff_change_state_requested=True,
                    cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_ENABLE,
                    state_to_check=BatteryLevelsCalibration.CUTOFF_ENABLE)

                self.post_requisite_cutoff = False
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        if self.post_requisite_reload_nvs:
            # --------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_post_requisite(self, "Reload initial NVS")
            # --------------------------------------------------------------------------
            CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            self.post_requisite_reload_nvs = False
        # end if

        super().tearDown()
    # end def tearDown

# end class BatteryLevelsCalibrationTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
