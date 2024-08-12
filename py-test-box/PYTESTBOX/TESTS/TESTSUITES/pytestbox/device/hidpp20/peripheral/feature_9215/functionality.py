#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9215.functionality
:brief: HID++ 2.0 ``Ads1231`` functionality test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.devicereset import DeviceReset
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ads1231utils import Ads1231TestUtils as Utils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.peripheral.feature_9215.ads1231 import Ads1231TestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Ads1231FunctionalityTestCase(Ads1231TestCase):
    """
    Validate ``Ads1231`` functionality test cases
    """

    @features("Feature9215")
    @level("Functionality")
    def test_write_calibration_verify(self):
        """
        Validate WriteCalibration is able to set reference point out value and calibration value
        """
        self.post_requisite_reload_nvs = True
        ref_point_index_value = [HexList("00"), HexList("01"), HexList("02")]
        ref_point_out_value = [HexList("00"), HexList("30"), HexList("40")]
        ref_point_cal_value = [HexList("002000"), HexList("F01000"), HexList("FE0000")]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Issuing WriteCalibration for Reference point index 1")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.write_calibration(self, ref_point_index=ref_point_index_value[1],
                                            ref_point_out_value=ref_point_out_value[1],
                                            ref_point_cal_value=ref_point_cal_value[1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadCalibration request")
        # --------------------------------------------------------------------------------------------------------------
        response = Utils.HIDppHelper.read_calibration(self, ref_point_index=ref_point_index_value[1])

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validating reference point out value and reference point calibration value ")
        # ----------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=ref_point_out_value[1],
            obtained=response.ref_point_out_value,
            msg=f"The value of calibrate is not as expected")
        self.assertEqual(
            expected=ref_point_cal_value[1],
            obtained=response.ref_point_cal_value,
            msg=f"The value of calibrate is not as expected")
        self.testCaseChecked("FUN_9215_0001", _AUTHOR)
    # end def test_write_calibration_verify

    @features("Feature9215")
    @features("Feature1802")
    @level("Functionality")
    def test_write_calibration_retained_verify(self):
        """
        Validate WriteCalibration values set is retained across reset for all valid reference point indices
        """
        self.post_requisite_reload_nvs = True
        ref_point_index_value = [HexList("00"), HexList("01"), HexList("02")]
        ref_point_out_value = [HexList("00"), HexList("30"), HexList("40")]
        ref_point_cal_value = [HexList("002000"), HexList("F01000"), HexList("FE0000")]

        # writing any value to reference index 0 will not be saved as index 0 always points to value zero

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send WriteCalibrate request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.write_calibration(self, ref_point_index=ref_point_index_value[0],
                                            ref_point_out_value=ref_point_out_value[1],
                                            ref_point_cal_value=ref_point_cal_value[0])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send WriteCalibrate request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.write_calibration(self, ref_point_index=ref_point_index_value[1],
                                            ref_point_out_value=ref_point_out_value[1],
                                            ref_point_cal_value=ref_point_cal_value[1])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send WriteCalibrate request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.write_calibration(self, ref_point_index=ref_point_index_value[2],
                                            ref_point_out_value=ref_point_out_value[2],
                                            ref_point_cal_value=ref_point_cal_value[2])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset Sensor")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.reset_sensor(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        device_reset_feature_id = self.updateFeatureMapping(feature_id=DeviceReset.FEATURE_ID)
        force_device_reset = ForceDeviceReset(deviceIndex=self.deviceIndex, featureId=device_reset_feature_id)
        self.send_report_to_device(report=force_device_reset)
        # Wait DUT to complete reset procedure
        sleep(5)
        # Reset device connection
        self.reset(hardware_reset=False, recover_time_needed=True)
        sleep(2)
        # Enable Hidden Features

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Hidden Features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        for index in range(len(ref_point_index_value)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Issuing ReadCalibration to HIDppHelper.read calibration values after reset")
            # ----------------------------------------------------------------------------------------------------------
            response = Utils.HIDppHelper.read_calibration(self,
                                                          ref_point_index=ref_point_index_value[index])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validating reference point output value for index :{index}")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(
                expected=ref_point_out_value[index],
                obtained=response.ref_point_out_value,
                msg=f"The value of ref point output value is not as expected")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validating reference point calibration value for index :{index}")
            # ----------------------------------------------------------------------------------------------------------
            if index == 0:
                # writing any value to reference index 0 will not be saved
                self.assertNotEqual(
                    unexpected=ref_point_cal_value[index],
                    obtained=response.ref_point_cal_value,
                    msg=f"The value of calibrate is not as expected")
            else:
                self.assertEqual(
                    expected=ref_point_cal_value[index],
                    obtained=response.ref_point_cal_value,
                    msg=f"The value of calibrate is not as expected")
            # end if
        # end for
        self.testCaseChecked("FUN_9215_0002", _AUTHOR)
    # end def test_write_calibration_retained_verify

    @features("Feature9215")
    @level("Functionality")
    def test_write_other_nvs_data_verify(self):
        """
        Validate WriteOtherNvsData is able to write max load value
        """
        self.post_requisite_reload_nvs = True
        data = HexList("400000000000000000000000000000")
        data_field_id_zero = HexList("00")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Writing data using WriteOtherNvsData")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.write_other_nvs_data(self, data_field_id=data_field_id_zero,
                                               data=data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reading data using ReadOtherNvsData")
        # --------------------------------------------------------------------------------------------------------------
        response_read_other_nvs_data = Utils.HIDppHelper.read_other_nvs_data(self,
                                                                             data_field_id=data_field_id_zero)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verifying data HIDppHelper.read from ReadOtherNvsData matches values "
                                  "set by WriteOtherNvsData")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=data,
            obtained=response_read_other_nvs_data.data,
            msg=f"The value of max load is not as expected")
        self.testCaseChecked("FUN_9215_0003", _AUTHOR)
    # end def test_write_other_nvs_data_verify

    @features("Feature9215")
    @level("Functionality")
    def test_set_monitor_mode_verify(self):
        """
        Validate SetMonitorModeVerify is able to generate MonitorModeEvents
        """
        threshold = HexList("00")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clearing any existing Event messages of monitor report type")
        # --------------------------------------------------------------------------------------------------------------
        self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                         class_type=self.feature_9215.monitor_report_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set monitor mode with count as 1")
        # --------------------------------------------------------------------------------------------------------------
        count = HexList("0001")
        Utils.HIDppHelper.set_monitor_mode(self, count=count,
                                           threshold=threshold)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read notifications from the event queue")
        # --------------------------------------------------------------------------------------------------------------
        set_monitor_mode_verify_response = Utils.HIDppHelper.monitor_report_event(self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validating Set monitor mode response count")
        # ----------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=count,
            obtained=set_monitor_mode_verify_response.counter,
            msg=f"The value of count is not as expected")
        self.testCaseChecked("FUN_9215_0004", _AUTHOR)
    # end def test_set_monitor_mode_verify

    @features("Feature9215")
    @level("Functionality")
    def test_set_monitor_mode_rollover_verify(self):
        """
        Validate MonitorReportEvent counter rollover
        """
        threshold = HexList("00")
        count = HexList("FFFF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set monitor mode with count as FFFF")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_monitor_mode(self, count=count,
                                           threshold=threshold)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Read notifications from the event queue until counter value is 0xFFFF")
        # --------------------------------------------------------------------------------------------------------------
        set_monitor_mode_verify_response = Utils.HIDppHelper.monitor_report_event(self)
        while set_monitor_mode_verify_response.counter != count:
            set_monitor_mode_verify_response = Utils.HIDppHelper.monitor_report_event(self)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Read notifications from the event queue until counter value is 0xFFFF + 1")
        # --------------------------------------------------------------------------------------------------------------
        set_monitor_mode_verify_response = Utils.HIDppHelper.monitor_report_event(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verifying 0xFFFF + 1 notifications sets counter to 0000")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=HexList("0000"),
            obtained=set_monitor_mode_verify_response.counter,
            msg=f"The value of count is not as expected")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read notifications from the event queue until counter value is 0xFFFF + 2")
        # --------------------------------------------------------------------------------------------------------------
        set_monitor_mode_verify_response = Utils.HIDppHelper.monitor_report_event(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verifying 0xFFFF + 2 notifications sets counter to 0001")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=HexList("0001"),
            obtained=set_monitor_mode_verify_response.counter,
            msg=f"The value of count is not as expected")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop Event messages of monitor report type")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_monitor_mode(self, count=HexList("0000"),
                                           threshold=threshold)
        self.testCaseChecked("FUN_9215_0005", _AUTHOR)
    # end def test_set_monitor_mode_rollover_verify

    @features("Feature9215")
    @level("Functionality")
    def test_set_monitor_mode_stop_verify(self):
        """
        Validate SetMonitorMode can stop notification events
        """
        threshold = HexList("00")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Start issuing Event messages of monitor report type indefinitely")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_monitor_mode(self, count=HexList("FFFF"),
                                           threshold=threshold)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Stop Event messages of monitor report type")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_monitor_mode(self, count=HexList("0000"),
                                           threshold=threshold)

        # Adding delay until SetMonitorMode is completed
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clearing any existing Event messages of monitor report type")
        # --------------------------------------------------------------------------------------------------------------
        self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                         class_type=self.feature_9215.monitor_report_event_cls)
        set_monitor_mode_stop_response = self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.event_message_queue, class_type=self.feature_9215.monitor_report_event_cls,
            allow_no_message=True, skip_error_message=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check event_message_queue has no new event messages of monitor report type")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=None,
                         obtained=set_monitor_mode_stop_response,
                         msg="event_message_queue is not empty!")
        self.testCaseChecked("FUN_9215_0006", _AUTHOR)
        # end def test_set_monitor_mode_stop_verify

    @features("Feature9215WithManDynCal")
    @level("Functionality")
    def test_manage_dynamic_calibration_parameters_verify(self):
        """
        Validate ManageDynamicCalibrationParameter is able to Set and Get Parameters
        """
        command_get_value = HexList("00")
        command_set_value = HexList("80")
        offset_extension_value = HexList("07")
        offset_adjustment_count_value = HexList("0014")
        dynamic_threshold_value = HexList("05")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Issuing ManageDynamicCalibrationParameters to Set Parameters")
        # --------------------------------------------------------------------------------------------------------------
        manage_dyn_cal_param = Utils.HIDppHelper.manage_dynamic_calibration_parameters
        manage_dyn_cal_param(self, command=command_set_value, offset_extension=offset_extension_value,
                             offset_adjustment_count=offset_adjustment_count_value,
                             dynamic_threshold=dynamic_threshold_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Issuing ManageDynamicCalibrationParameters to Get Parameters")
        # --------------------------------------------------------------------------------------------------------------
        manage_dyn_cal_param_response = manage_dyn_cal_param(self, command=command_get_value,
                                                             offset_extension=HexList("00"),
                                                             offset_adjustment_count=HexList("0000"),
                                                             dynamic_threshold=HexList("00"))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verifying parameters set by ManageDynamicCalibrationParameters are same as "
                                  "Parameters value to Get by ManageDynamicCalibrationParameters ")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=offset_extension_value,
            obtained=manage_dyn_cal_param_response.offset_extension,
            msg=f"The value of offset extension is not as expected")
        self.assertEqual(
            expected=offset_adjustment_count_value,
            obtained=manage_dyn_cal_param_response.offset_adjustment_count,
            msg=f"The value of offset adjustment count is not as expected")
        self.assertEqual(
            expected=dynamic_threshold_value,
            obtained=manage_dyn_cal_param_response.dynamic_threshold,
            msg=f"The value of dynamic threshold is not as expected")
        self.testCaseChecked("FUN_9215_0007", _AUTHOR)
    # end def test_manage_dynamic_calibration_parameters_verify

    @features("Feature9215")
    @level("Functionality")
    def test_calibrate_verify(self):
        """
        Validate Calibrate Response is as expected
        """
        ref_point_index_value = [HexList("00"), HexList("01"), HexList("02")]
        ref_point_out_value = [HexList("00"), HexList("30"), HexList("40")]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Calibrating all 3 points using calibrate api")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Calibrate request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.calibrate(self, ref_point_index=ref_point_index_value[0],
                                    ref_point_out_value=ref_point_out_value[1])
        # Adding delay until Calibration is completed
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Calibrate request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.calibrate(self, ref_point_index=ref_point_index_value[1],
                                    ref_point_out_value=ref_point_out_value[1])
        # Adding delay until Calibration is completed
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send Calibrate request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.calibrate(self, ref_point_index=ref_point_index_value[2],
                                    ref_point_out_value=ref_point_out_value[2])
        # Adding delay until Calibration is completed
        sleep(1)
        for index in range(len(ref_point_index_value)):

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadCalibration request")
            # ----------------------------------------------------------------------------------------------------------
            read_calibration_response = Utils.HIDppHelper.read_calibration(
                self, ref_point_index=ref_point_index_value[index])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verifying Reference Point out value is same as value set")
            # ----------------------------------------------------------------------------------------------------------
            if index == 0:
                self.assertEqual(
                    expected=HexList("00"),
                    obtained=read_calibration_response.ref_point_out_value,
                    msg=f"The value of max load is not as expected")
            # end if
        # end for
        self.testCaseChecked("FUN_9215_0008", _AUTHOR)
    # end def test_calibrate_verify

    @features("Feature9215")
    @features("Feature1802")
    @level("Functionality")
    def test_calibrate_retained_verify(self):
        """
        Validate Calibration values set is retained across reset for all valid reference point indices
        """
        ref_point_output_zero_value = HexList("00")
        ref_point_output = [HexList("35"), HexList("56"), HexList("60")]
        ref_point_index_value = [HexList("00"), HexList("01"), HexList("02")]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Issuing Calibrate for Reference point index 0,1 and 2")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(len(ref_point_index_value)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Calibrate request")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.calibrate(self, ref_point_index=ref_point_index_value[index],
                                        ref_point_out_value=ref_point_output[index])
            # Adding delay until Calibration is completed
            sleep(1)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset Sensor")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.reset_sensor(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        device_reset_feature_id = self.updateFeatureMapping(feature_id=DeviceReset.FEATURE_ID)
        force_device_reset = ForceDeviceReset(deviceIndex=self.deviceIndex, featureId=device_reset_feature_id)
        self.send_report_to_device(report=force_device_reset)
        # Wait DUT to complete reset procedure
        sleep(5)
        # Reset device connection
        self.reset(hardware_reset=False, recover_time_needed=True)
        sleep(2)
        # Enable Hidden Features
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Enable Hidden Features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        for index in range(len(ref_point_index_value)):

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Issuing ReadCalibration to HIDppHelper.read calibration values after reset")
            # ----------------------------------------------------------------------------------------------------------
            read_calibration_response = Utils.HIDppHelper.read_calibration(
                self, ref_point_index=ref_point_index_value[index])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verifying Reference Point out value is same as value set")
            # ----------------------------------------------------------------------------------------------------------
            if index == 0:
                self.assertEqual(
                    expected=ref_point_output_zero_value,
                    obtained=read_calibration_response.ref_point_out_value,
                    msg=f"The value of max load is not as expected")
            # end if
            else:
                self.assertEqual(
                    expected=ref_point_output[index],
                    obtained=read_calibration_response.ref_point_out_value,
                    msg=f"The value of max load is not as expected")
            # end else
        # end for
        self.testCaseChecked("FUN_9215_0009", _AUTHOR)
    # end def test_calibrate_retained_verify

    @features("Feature9215")
    @level("Functionality")
    def test_calibrate_boundary_verify(self):
        """
        Check Valid boundary conditions for Calibration and WriteCalibration don't cause failure
        """
        ref_point_output = [HexList("00"), HexList("63"), HexList("64")]
        ref_point_index_value = [HexList("00"), HexList("01"), HexList("02")]
        ref_point_cal_value = [HexList("002000"), HexList("F01000"), HexList("FE0000")]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Issuing Calibrate for Reference point index 0,1 and 2")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(len(ref_point_index_value)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Calibrate request")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.calibrate(self, ref_point_index=ref_point_index_value[index],
                                        ref_point_out_value=ref_point_output[index])
            # Adding delay until Calibration is completed
            sleep(2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadCalibration request")
            # ----------------------------------------------------------------------------------------------------------
            read_calibration_response = Utils.HIDppHelper.read_calibration(
                self, ref_point_index=ref_point_index_value[index])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verifying Reference Point out value is same as value set")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(
                expected=ref_point_output[index],
                obtained=read_calibration_response.ref_point_out_value,
                msg=f"The value of max load is not as expected")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send WriteCalibration request")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.write_calibration(self, ref_point_index=ref_point_index_value[index],
                                                ref_point_out_value=ref_point_output[index],
                                                ref_point_cal_value=ref_point_cal_value[index])
            # Adding delay until Calibration is completed
            sleep(1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Issuing ReadCalibration to HIDppHelper.read calibration values after reset")
            # ----------------------------------------------------------------------------------------------------------
            response = Utils.HIDppHelper.read_calibration(self,
                                                          ref_point_index=ref_point_index_value[index])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Validating reference point output value for index :{index}")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(
                expected=ref_point_output[index],
                obtained=response.ref_point_out_value,
                msg=f"The value of ref point output value is not as expected")
        # end for
        self.testCaseChecked("FUN_9215_0010", _AUTHOR)
    # end def test_calibrate_boundary_verify
# end class Ads1231FunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
