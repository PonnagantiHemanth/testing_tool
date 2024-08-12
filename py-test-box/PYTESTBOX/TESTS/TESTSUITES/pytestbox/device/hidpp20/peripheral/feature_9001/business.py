#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9001.business
:brief: HID++ 2.0 ``PMW3816andPMW3826`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/01/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpi
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inf_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.pmw3816andpmw3826utils import PMW3816andPMW3826TestUtils
from pytestbox.device.base.spidirectaccessutils import OpticalSensorName
from pytestbox.device.base.spidirectaccessutils import SPI_PERIPHERAL_REGISTER_DICT
from pytestbox.device.hidpp20.peripheral.feature_9001.pmw3816andpmw3826 import PMW3816andPMW3826TestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826BusinessTestCase(PMW3816andPMW3826TestCase):
    """
    Validate ``PMW3816andPMW3826`` business test cases
    """

    @features("Feature9001")
    @level("Business")
    @skip("Kosmos dependency")
    def test_no_tracking_report_in_rest_mode(self):
        """
        Validate Tracking Report is not received when mouse is moved and the sensor is set to Rest Mode.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup Register 0x40")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over different Rest Modes in [0x20, 0x40, 0x60]")
        # --------------------------------------------------------------------------------------------------------------
        for rest_mode in PMW3816andPMW3826TestUtils.PerformanceMode.REST_MODES:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Write Sensor Register for Register Address 0x40(Sensor Performance) and"
                                     f"Register Value={rest_mode}")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate the tracking test response fields.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over interesting value between 0x0000 and 0xFFFF")
            # ----------------------------------------------------------------------------------------------------------
            for count in []:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"send Tracking Test with selected count '{count}'")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Validate the tracking test response fields.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"emulate {count} mouse cursor movement in any direction.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify no Event is received")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check no HID Reports are received.")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Restore Register data from backup")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0001", _AUTHOR)
    # end def test_no_tracking_report_in_rest_mode

    @features("Feature9001")
    @level("Business")
    @skip("Kosmos dependency")
    def test_no_tracking_report_when_mouse_not_moved(self):
        """
        Validate Tracking Report is not received when the mouse is not moved.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over multiple interesting values between 0x00 and 0xFF.")
        # --------------------------------------------------------------------------------------------------------------
        for value in compute_inf_values(['FF']):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Tracking Test count with selected value {value}")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate tracking test response fields.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set the mouse emulator to STILL. (no movement)")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify HID report is not received.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify TrackingReport Event is not received.")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0002", _AUTHOR)
    # end def test_no_tracking_report_when_mouse_not_moved

    @features("Feature9001")
    @features("Feature2201")
    @level("Business")
    def test_set_dpi_through_adjustable_dpi(self):
        """
        Validate the DPI Set via 2201 is reflected in the Sensor register
        """
        sensor_idx = None
        if self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName == OpticalSensorName.TOG6:
            sensor_idx = 0
        elif self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName == OpticalSensorName.TOGX:
            sensor_idx = 1
        # end if
        self.assertIsNotNone(sensor_idx, "Sensor name is not defined in product settings")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2201")
        # --------------------------------------------------------------------------------------------------------------
        feature_2201_index, feature_2201, _, _ = DeviceTestUtils.HIDppHelper.get_parameters(
            self, feature_id=AdjustableDpi.FEATURE_ID, factory=AdjustableDpiFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup Registers 0x4E")
        # --------------------------------------------------------------------------------------------------------------
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["dpi"]["address"]
        register_backup_value = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
            self, register_address).register_value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Sensor DPI List from settings")
        # --------------------------------------------------------------------------------------------------------------
        self.adj_dpi = self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
        dpi_list = list(x for x in range(self.adj_dpi.F_DpiMin, self.adj_dpi.F_DpiMax, self.adj_dpi.F_DpiStep * 16))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several Interesting values within Min and max supported DPI returned")
        # --------------------------------------------------------------------------------------------------------------
        for dpi in dpi_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Set Sensor DPI with the selected Value {dpi}")
            # ----------------------------------------------------------------------------------------------------------
            set_dpi_response = AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(self, sensor_idx=0,
                                                                                 dpi=dpi, dpi_level=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate the set sensor DPI response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = AdjustableDpiTestUtils.SetSensorDpiResponseChecker
            check_map = {"sensor_idx": (checker.check_sensor_idx, sensor_idx),
                         "dpi": (checker.check_dpi, dpi),
                         "dpi_level": (checker.check_dpi_level, 0), 
                         }
            checker.check_fields(self, set_dpi_response,
                                 expected_cls=feature_2201.set_sensor_dpi_response_cls,
                                 check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "send Read Register with Register Address = 0x4E (Resolution)")
            # ----------------------------------------------------------------------------------------------------------
            register_address = \
                SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["dpi"]["address"]
            resolution = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register\
                (test_case=self, register_address=register_address).register_value

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check if the calculated DPI value is the same")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=dpi, obtained=(to_int(resolution) + 1) * 50,
                             msg="Sensor dpi level does not match dpi set by feature 0x2201")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Restore Register data from backup")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(self, register_address, register_backup_value)

        self.testCaseChecked("BUS_9001_0003", _AUTHOR)
    # end def test_set_dpi_through_adjustable_dpi

    @features("Feature9001")
    @features("Feature2201")
    @level("Business")
    def test_set_dpi_through_sensor_register(self):
        """
        Validate the DPI Set via Sensor register is reflected in the 0x2201 Feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2201 index")
        # --------------------------------------------------------------------------------------------------------------)
        feature_2201_index, feature_2201, _, _ = DeviceTestUtils.HIDppHelper.get_parameters(
            self, feature_id=AdjustableDpi.FEATURE_ID, factory=AdjustableDpiFactory)
        
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup resolution register 0x4E")
        # --------------------------------------------------------------------------------------------------------------
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["dpi"]["address"]
        register_backup_value = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
            self, register_address).register_value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over Interesting values between 0x00 and 0x3200 (Max possible value is"
                                 "12800 DPI)")
        # --------------------------------------------------------------------------------------------------------------
        self.adj_dpi = self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
        dpi_list = list(x for x in range(self.adj_dpi.F_DpiMin, self.adj_dpi.F_DpiMax, self.adj_dpi.F_DpiStep * 16))
        for dpi in dpi_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Calculate the value to be set in register using DPI value chosen using"
                                     "value=(DPI/50)-1")
            # ----------------------------------------------------------------------------------------------------------
            dpi = to_int(dpi) // 50 - 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Write Sensor Register with register Address = 0x4E with selected value.")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                self, register_address=register_address, register_value=HexList(dpi))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the write sensor register response fields.")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, response, self.feature_9001.write_sensor_register_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Get Sensor DPI via 0x2201 Feature.")
            # ----------------------------------------------------------------------------------------------------------
            response = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self, sensor_idx=0).dpi
            response = to_int(response)//50 - 1

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the DPI value returned is the same as chosen value.")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=dpi, obtained=to_int(response),
                             msg=f"Dpi value returned by feature 0x2201 differs from dpi value set directly "
                                 f"through sensor")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Restore Register data from backup")
        # --------------------------------------------------------------------------------------------------------------)
        PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(self, register_address, register_backup_value)

        self.testCaseChecked("BUS_9001_0004", _AUTHOR)
    # end def test_set_dpi_through_sensor_register

    @features("Feature9001")
    @level("Business")
    @skip("Kosmos dependency")
    def test_tracking_test(self):
        """
        Validate sending tracking test with 0 count while another tracking test is in progress.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send trackingTest with count=0xFFFF")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate tracking test response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "emulate continuous mouse movement in any direction.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the trackingReportEvent is received")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify no HID report is received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send trackingTest with count=0")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate tracking test response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the Tracking Report Event is stopped with last event counter<0xFFFF")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify new Cursor Movements are received in HID queue.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "stop mouse movement emulation.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0005", _AUTHOR)
    # end def test_tracking_test

    @features("Feature9001")
    @level("Business")
    @services("PowerSupply")
    def test_dpi_reverts_after_power_cycle(self):
        """
        Validate DPI setting reverts to default after Power Cycle.
        
        Requires Power Supply
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup Registers 0x4E")
        # --------------------------------------------------------------------------------------------------------------
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["dpi"]["address"]
        register_backup_value = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
            self, register_address).register_value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over few interesting values between 0x00 and 0xFF")
        # --------------------------------------------------------------------------------------------------------------
        for value in compute_inf_values(['FF']):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"send Write Register with Register Address = 0x4E (Resolution) with selected"
                                     f"value {value}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                test_case=self,
                register_address=register_address,
                register_value=HexList(value))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate write sensor register response fields.")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, response, self.feature_9001.write_sensor_register_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Reset the device.")
            # ----------------------------------------------------------------------------------------------------------
            PMW3816andPMW3826TestUtils.ResetHelper.power_supply_reset(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable TDE Manufacturing Feature.")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send read Register with Register Address =0x4E(Resolution).")
            # ----------------------------------------------------------------------------------------------------------
            dpi_value = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                test_case=self,
                register_address=register_address).register_value

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check if the Value returned matches (value+1)*50 = default DPI.")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_DpiDefault,
                             obtained=(to_int(dpi_value) + 1) * 50,
                             msg="Obtained value does not match the default dpi value")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Restore Register data from backup")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(self, register_address, register_backup_value)

        self.testCaseChecked("BUS_9001_0006", _AUTHOR)
    # end def test_dpi_reverts_after_power_cycle

    @features("Feature9001")
    @features("Feature1802")
    @level("Business")
    def test_dpi_reverts_after_force_device_reset(self):
        """
        Validate DPI setting reverts to default after Force Device Reset
        
        Requires Device Reset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup Registers 0x4E")
        # --------------------------------------------------------------------------------------------------------------
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["dpi"]["address"]
        register_backup_value = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
            self, register_address).register_value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over interesting values between 0x00 and 0xFF")
        # --------------------------------------------------------------------------------------------------------------
        for value in compute_inf_values(['FF']):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "send Write Register with Register Address = 0x4E (Resolution) with selected"
                                     "value.")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                test_case=self,
                register_address=register_address,
                register_value=HexList(value))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate write register response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, response, self.feature_9001.write_sensor_register_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Force device reset via 0x1802")
            # ----------------------------------------------------------------------------------------------------------
            PMW3816andPMW3826TestUtils.ResetHelper.hidpp_reset(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Enable TDE Manufacturing Feature.")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send read Register with Register Address =0x4E(Resolution)")
            # ----------------------------------------------------------------------------------------------------------
            dpi_value = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                test_case=self,
                register_address=register_address).register_value

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check if the Value returned matches (value+1)*50 = default DPI.")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_DpiDefault,
                             obtained=(to_int(dpi_value) + 1) * 50,
                             msg="Obtained value does not match the default dpi value")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Restore Register data from backup")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(self, register_address, register_backup_value)

        self.testCaseChecked("BUS_9001_0007", _AUTHOR)
    # end def test_dpi_reverts_after_force_device_reset

    @features("Feature9001")
    @level("Business")
    @skip("Kosmos dependency")
    def test_reset_sensor(self):
        """
        Verify Reset Sensor reverts to normal HID reporting
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send trackingTest with count=0xFFFF")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate tracking test response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "emulate continuous mouse cursor movement in any direction.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the trackingReportEvent is received")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify no HID report is received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ResetSensor")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "verify reset sensor response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify no trackingReportEvent is received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify HID report is received for mouse movement emulations.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "stop Mouse Emulation.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0008", _AUTHOR)
    # end def test_reset_sensor

    @features("Feature9001")
    @level("Business")
    @skip("NotSupported")
    def test_shutdown_sensor_stops_mouse_reports(self):
        """
        Verify Shutdown Sensor Stops mouse report event
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send trackingTest with count=0xFFFF")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate tracking test response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "emulate continuous mouse cursor movement in any direction.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the trackingReportEvent is received")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify no HID report is received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Shutdown Sensor")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate shutdown sensor response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify no trackingReportEvent is received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify no HID report is received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Reset Sensor")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate reset sensor response fields.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0009", _AUTHOR)
    # end def test_shutdown_sensor_stops_mouse_reports

    @features("Feature9001")
    @level("Business")
    @skip("NotSupported")
    def test_shutdown_sensor_stops_hid_reporting(self):
        """
        Verify Shutdown Sensor Stops standard mouse HID reporting
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "emulate continuous mouse cursor movement in any direction.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the trackingReportEvent is not received")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify HID report is received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Shutdown Sensor")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate shutdown sensor response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify trackingReportEvent is not received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify HID report is not received.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Reset Sensor")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate reset sensor response fields.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0010", _AUTHOR)
    # end def test_shutdown_sensor_stops_hid_reporting

    @features("Feature9001v0")
    @level("Business")
    @bugtracker("Unexpected_FrameCapture_Response")
    def test_frame_capture_returns_full_image_dump(self):
        """
        Verify frameCapture returns full 1225 bytes of image dump.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Frame capture.")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.frame_capture(self)
        event = PMW3816andPMW3826TestUtils.HIDppHelper.frame_capture_report_event(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify 1..76 Events received has data between 0x00.0xFF in each of it's response"
                                  "payload.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the 77th Event has the first 9 bytes has data between 0x00..0xFF and the"
                                  "last 7 bytes are 0x00")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify no new Events are received")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0011", _AUTHOR)
    # end def test_frame_capture_returns_full_image_dump

    @features("Feature9001")
    @features("Feature2201")
    @level("Business")
    def test_check_reset_sensor_reverts_dpi_setting_using_adjustable_dpi(self):
        """
        Verify Reset Sensor reverts the DPI setting to default via 2201 feature.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2201 index.")
        # --------------------------------------------------------------------------------------------------------------
        feature_2201_index, feature_2201, _, _ = DeviceTestUtils.HIDppHelper.get_parameters(
            self, feature_id=AdjustableDpi.FEATURE_ID, factory=AdjustableDpiFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Get Sensor DPI List with sensor index of PWM Sensor. (default =0)")
        # --------------------------------------------------------------------------------------------------------------
        self.adj_dpi = self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
        dpi_list = list(x for x in range(self.adj_dpi.F_DpiMin, self.adj_dpi.F_DpiMax, self.adj_dpi.F_DpiStep * 16))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several Interesting values within Min and max supported DPI")
        # --------------------------------------------------------------------------------------------------------------
        for dpi in dpi_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Set Sensor DPI with the selected Value {dpi}")
            # ----------------------------------------------------------------------------------------------------------
            set_dpi_response = AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(self, sensor_idx=0,
                                                                                 dpi=dpi, dpi_level=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate set sensor DPI response fields.")
            # ----------------------------------------------------------------------------------------------------------
            checker = AdjustableDpiTestUtils.SetSensorDpiResponseChecker
            check_map = {"sensor_idx": (checker.check_sensor_idx, 0),
                         "dpi": (checker.check_dpi, dpi),
                         "dpi_level": (checker.check_dpi_level, 0), }
            checker.check_fields(self, set_dpi_response,
                                 expected_cls=feature_2201.set_sensor_dpi_response_cls,
                                 check_map=check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Reset Sensor")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.reset_sensor(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate reset sensor response fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, response, self.feature_9001.reset_sensor_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Get Sensor DPI")
            # ----------------------------------------------------------------------------------------------------------
            dpi_response = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self, sensor_idx=0).dpi

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the DPI value is equal to the Default DPI")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=self.adj_dpi.F_DpiDefault, obtained=dpi_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0012", _AUTHOR)
    # end def test_check_reset_sensor_reverts_dpi_setting_using_adjustable_dpi

    @features("Feature9001")
    @level("Business")
    def test_check_reset_sensor_reverts_dpi_setting(self):
        """
        Verify Reset Sensor reverts the DPI setting to default.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup Registers 0x4E")
        # --------------------------------------------------------------------------------------------------------------
        register_address = \
            SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]["dpi"]["address"]
        register_backup_value = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
            self, register_address).register_value

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over few interesting values between 0x00 and 0xFF")
        # --------------------------------------------------------------------------------------------------------------
        for value in compute_inf_values(["FF"]):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"send Write Register with Register Address = 0x4E (Resolution) with selected"
                                     f"value {value}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                self, register_address=register_address, register_value=HexList(value))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate write sensor register response fields.")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, response, self.feature_9001.write_sensor_register_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send Reset Sensor.")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.reset_sensor(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "validate reset sensor response fields.")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, response, self.feature_9001.reset_sensor_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "send Read Register with Register Address = 0x4E (Resolution)")
            # ----------------------------------------------------------------------------------------------------------
            resolution = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register\
                (test_case=self, register_address=register_address).register_value

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check if the calculated DPI value is the same")
            # ----------------------------------------------------------------------------------------------------------
            adj_dpi = self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
            self.assertEqual(expected=adj_dpi.F_DpiDefault, obtained=(to_int(resolution) + 1) * 50,
                             msg="Sensor dpi level does not match dpi set by feature 0x2201")
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Restore Register data from backup")
        # --------------------------------------------------------------------------------------------------------------
        PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(self, register_address, register_backup_value)

        self.testCaseChecked("BUS_9001_0013", _AUTHOR)
    # end def test_check_reset_sensor_reverts_dpi_setting

    @features("Feature9001")
    @level("Business")
    @skip("Kosmos dependency")
    def test_tracking_report_send_on_device_wakeup(self):
        """
        Verify tracking report is sent when the device wakes up from deep sleep.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Tracking Test with count=0xFF")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate tracking test response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetPowerMode via 1830 to put the device into deep sleep mode(0x03)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "validate set power mode response fields.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate '0xFF' mouse movements.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "verify the device wakes up and receives the correct number of events.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify no HID report is received.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_9001_0014", _AUTHOR)
    # end def test_tracking_report_send_on_device_wakeup
# end class PMW3816andPMW3826BusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
