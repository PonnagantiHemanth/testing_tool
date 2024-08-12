#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9001.functionality
:brief: HID++ 2.0 ``PMW3816andPMW3826`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/01/10
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.pmw3816andpmw3826utils import PMW3816andPMW3826TestUtils
from pytestbox.device.base.spidirectaccessutils import SPI_PERIPHERAL_REGISTER_DICT
from pytestbox.device.hidpp20.peripheral.feature_9001.pmw3816andpmw3826 import PMW3816andPMW3826TestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826FunctionalityTestCase(PMW3816andPMW3826TestCase):
    """
    Validate ``PMW3816andPMW3826`` functionality test cases
    """

    @features("Feature9001")
    @level("Functionality")
    def test_read_register_sensor(self):
        """
        Validate the Read sensor register across all valid input ranges
        """
        sensor_map = SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over valid Register Addresses which supports read")
        # --------------------------------------------------------------------------------------------------------------
        for register in self.config.F_ReadOnlyRegisters + self.config.F_ReadAndWriteRegisters:
            register_address = sensor_map[register]["address"]

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Read Sensor request with Register Address={register_address}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                test_case=self,
                register_address=HexList(register_address))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the Response Register value is in valid range.")
            # ----------------------------------------------------------------------------------------------------------
            checker = PMW3816andPMW3826TestUtils.RegisterValueInRangeChecker
            check_map = checker.get_check_map(self, register_name=register)
            checker.check_fields(self,
                                 message=response,
                                 expected_cls=self.feature_9001.read_sensor_register_response_cls,
                                 check_map=check_map
                                 )
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0001", _AUTHOR)
    # end def test_read_register_sensor

    @features("Feature9001")
    @level("Functionality")
    def test_write_register_sensor(self):
        """
        Validate write sensor register across all valid input ranges
        """
        sensor_map = SPI_PERIPHERAL_REGISTER_DICT[self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup Registers which support Write Access")
        # --------------------------------------------------------------------------------------------------------------
        register_backup = {"powerup_reset": 0x00, "shutdown": 0x00}
        for register in self.config.F_ReadAndWriteRegisters:
            register_address = sensor_map[register]["address"]
            register_value = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                self, register_address=register_address).register_value
            register_backup[register] = register_value
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over valid Register Addresses which supports Write Access")
        # --------------------------------------------------------------------------------------------------------------
        for register in self.config.F_ReadAndWriteRegisters + self.config.F_WriteOnlyRegisters:
            register_address = sensor_map[register]["address"]

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Write Sensor request with Register Address={register_address} "
                                     f"and RegisterValue=01")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                self, register_address=register_address, register_value=HexList(0x01))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the Write Sensor Response value is valid.")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {}
            checker.check_fields(self, response, self.feature_9001.write_sensor_register_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send Read Sensor Request for the Register Address={register}")
            # ----------------------------------------------------------------------------------------------------------
            response = PMW3816andPMW3826TestUtils.HIDppHelper.read_sensor_register(
                self, register_address=register_address)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the Response Register value is the same used for write operation or in"
                                      "valid range")
            # ----------------------------------------------------------------------------------------------------------
            if register in ["motion", "chip_observation", "pixel_grab", "axis_control", "shutdown", "powerup_reset"]:
                checker = PMW3816andPMW3826TestUtils.RegisterValueInRangeChecker
                check_map = checker.get_check_map(self, register_name=register)
                checker.check_fields(self,
                                     message=response,
                                     expected_cls=self.feature_9001.read_sensor_register_response_cls,
                                     check_map=check_map
                                     )
            else:
                self.assertEqual(expected=HexList(0x01), obtained=response.register_value,
                                 msg=f"The register value parameter differs expected:"
                                     f"{HexList(0x01)}, obtained:{response})"
                                 )
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Restore Register data from backup")
        # --------------------------------------------------------------------------------------------------------------
        for register, register_value in register_backup.items():
            PMW3816andPMW3826TestUtils.HIDppHelper.write_sensor_register(
                 self, register_address=sensor_map[register]["address"], register_value=HexList(register_value))
        # end for

        self.testCaseChecked("FUN_9001_0002", _AUTHOR)
    # end def test_write_register_sensor

    @features("Feature9001")
    @level("Functionality")
    @skip("Kosmos dependency")
    def test_validate_tracking_test_returns_correct_number_of_events(self):
        """
        Validate the Tracking Test returns correct number of events requested.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over few interesting values between 0x0000 and 0xFFFF for cursor movement")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "send Tracking Test with selected count 'n'")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify Tracking Test response fields.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "emulate 'n' mouse cursor movement in any direction")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "verify the first event is received with counter=1")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify counter in Each event is reported with previous counter+1 until nth"
                                      "event.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the number of trackingReport events received is same as the requested"
                                      "count.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check no HID Reports are received while the events are reported.")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0003", _AUTHOR)
    # end def test_validate_tracking_test_returns_correct_number_of_events

    @features("Feature9001")
    @level("Functionality")
    @skip("Kosmos dependency")
    def test_validate_positive_delta_x_value_when_mouse_moved_right(self):
        """
        Validate the Positive Delta X reported by the sensor when the mouse is moved Right
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over few interesting values between 0x0000 and 0xFFFF  for cursor movement")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over few interesting values between 0x0001 and 0x7FFF")
            # ----------------------------------------------------------------------------------------------------------
            for _ in []:  # TODO: fill this condition
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "send Tracking Test with selected count 'n'")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify Tracking Test response fields.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "emulate 'n' mouse cursor movement in positive Delta X with selected delta"
                                         "value")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify the DeltaX in trackingReportEvent received is same as selected")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify the DeltaY in trackingReportEvent received is 0x0000")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check no HID Reports are received while the events are reported.")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0004", _AUTHOR)
    # end def test_validate_positive_delta_x_value_when_mouse_moved_right

    @features("Feature9001")
    @level("Functionality")
    @skip("Kosmos dependency")
    def test_validate_negative_delta_x_value_when_mouse_moved_left(self):
        """
        Validate the Negative Delta X reported by the sensor when the mouse is moved Left
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over few interesting values between 0x0000 and 0xFFFF for cursor movement")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over few interesting values between 0x8001 and 0xFFFF")
            # ----------------------------------------------------------------------------------------------------------
            for _ in []:  # TODO: fill this condition
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "send Tracking Test with selected count 'n'")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify Tracking Test response fields.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "emulate 'n' mouse cursor movement in negative Delta X with selected value")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify the DeltaX in trackingReportEvent received is same as input")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify the DeltaY in trackingReportEvent received is 0x0000")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check no HID Reports are received while the events are reported.")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0005", _AUTHOR)
    # end def test_validate_negative_delta_x_value_when_mouse_moved_left

    @features("Feature9001")
    @level("Functionality")
    @skip("Kosmos dependency")
    def test_validate_positive_delta_y_value_when_mouse_moved_up(self):
        """
        Validate the Positive Delta Y reported by the sensor when the mouse is moved Up
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over few interesting values between 0x0000 and 0xFFFF for cursor movement")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over few interesting values between 0x0001 and 0x7FFF")
            # ----------------------------------------------------------------------------------------------------------
            for _ in []:  # TODO: fill this condition
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "send Tracking Test with selected count 'n'")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify Tracking test response fields.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "emulate 'n' mouse cursor movement in positive Delta Y with selected value")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify the DeltaX in trackingReportEvent received is 0x0000")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify the DeltaY in trackingReportEvent received is same as input")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop.")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0006", _AUTHOR)
    # end def test_validate_positive_delta_y_value_when_mouse_moved_up

    @features("Feature9001")
    @level("Functionality")
    @skip("Kosmos dependency")
    def test_validate_negative_delta_y_value_when_mouse_moved_down(self):
        """
        Validate the Negative Delta Y reported by the sensor when the mouse is moved Down
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over few interesting values between 0x0000 and 0xFFFF for cursor movement")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over few interesting values between 0x8001 and 0xFFFF")
            # ----------------------------------------------------------------------------------------------------------
            for _ in []:  # TODO: fill this condition
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "send Tracking Test with selected count 'n'")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify Tracking test response fields.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "emulate 'n' mouse cursor movement in negative Delta Y with selected value")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify the DeltaX in trackingReportEvent received is 0x0000")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify the DeltaY in trackingReportEvent received is same as input")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check no HID Reports are received while the events are reported.")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0007", _AUTHOR)
    # end def test_validate_negative_delta_y_value_when_mouse_moved_down

    @features("Feature9001")
    @level("Functionality")
    @skip("Kosmos dependency")
    def test_validate_surface_quality_and_average(self):
        """
        Validate the surface Quality Value and Average when cursor is moved .
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over few interesting value between 0x0000 and 0xFFFF for cursor movement")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test loop over few interesting values between 0x00 and 0xFF for SQUAL value")
            # ----------------------------------------------------------------------------------------------------------
            for _ in []:  # TODO: fill this condition
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Use Kosmos TOG emulator to expose the selected SQUAL value")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send Read register for register= 0x07")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "validate the register value returned is same as input.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "send Tracking Test with selected count 'n'")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "validate tracking test response fields.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify SQUAL value received is in valid range.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the SQUAL Value and SQUAL Average is same as input")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check no HID Reports are received while the events are reported.")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0008", _AUTHOR)
    # end def test_validate_surface_quality_and_average

    @features("Feature9001")
    @level("Functionality")
    @skip("Kosmos dependency")
    def test_validate_shutter_value_and_average(self):
        """
        Validate the Shutter Value and Average when cursor is moved
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over interesting value between 0x0000 and 0xFFFF")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over SHUTTER possible values between 0x0000 and 0x1FFF.")
            # ----------------------------------------------------------------------------------------------------------
            for _ in []:  # TODO: fill this condition
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Use Kosmos TOG emulator to expose the selected SHUTTER value")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send Read register for register= 0x0B")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "validate the register value returned is same as (selected value & mask"
                                          "0xFF).")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send Read register for register= 0x0C")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "validate the register value returned is same as (selected value right"
                                          "shifted by 8)")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "send Tracking Test with selected count 'n'")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Validate tracking test response fields.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify Shutter value received is in valid range.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check the Shutter Value and Shutter Average is same as the input")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check no HID Reports are received while the events are reported.")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0009", _AUTHOR)
    # end def test_validate_shutter_value_and_average

    @features("Feature9001")
    @level("Functionality")
    @skip("Kosmos dependency")
    def validate_pixel_sum_max_pixel_min_pixel(self):
        """
        Validate the Pixel Sum, Max and Min Pixel  when cursor is moved.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over interesting value between 0x0000 and 0xFFFF")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop over PIXEL possible values between 0x00 and 0x98.")
            # ----------------------------------------------------------------------------------------------------------
            for _ in []:  # TODO: fill this condition
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Use Kosmos TOG emulator to expose the selected PIXEL value")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "send Tracking Test with selected count 'n'")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "verify tracking test response fields.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "emulate 'n' mouse cursor movement in any direction.")
                # ------------------------------------------------------------------------------------------------------

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify Pixel sum, max pixel and nim pixel value received are same as"
                                          "emulated value.")
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_9001_0010", _AUTHOR)
    # end def validate_pixel_sum_max_pixel_min_pixel
# end class PMW3816andPMW3826FunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
