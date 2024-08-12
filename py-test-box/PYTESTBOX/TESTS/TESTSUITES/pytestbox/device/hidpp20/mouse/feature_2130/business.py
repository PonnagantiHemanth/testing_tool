#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2130.business
:brief: HID++ 2.0 ``RatchetWheel`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheel
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.ratchetwheelutils import RatchetWheelTestUtils
from pytestbox.device.hidpp20.mouse.feature_2130.ratchetwheel import RatchetWheelTestCase
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_VERIFY_SET_WHEEL_MODE_RESPONSE = "Verify the setWheelMode Response fields"
_SEND_GET_WHEEL_MODE_REQ = "Send getWheelMode request"
_CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_1 = "Check getWheelMode response, divert is HID++ Divert mode (1)"
_CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_0 = "Check getWheelMode response, divert is HID mode (0)"
_SEND_SET_WHEEL_MODE_REQUEST_DIVERT_1 = "Send setWheelMode request with divert = 1"
_SEND_SET_WHEEL_MODE_REQUEST_DIVERT_0 = "Send setWheelMode request with divert = 0"
_TEST_LOOP_OVER_N_VALUES = "Test Loop over 'n' values"
_END_TEST_LOOP = "End Test Loop"
_CHECK_NO_NOTIFICATION_RECEIVED = "Check no notification received in HID queue"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RatchetWheelBusinessTestCase(RatchetWheelTestCase):
    """
    Validate ``RatchetWheel`` business test cases
    """

    @features("Feature2130")
    @level('Business', 'SmokeTests')
    @services("MainWheel")
    def test_positive_delta_v_with_wheel_movement(self):
        """
        Validate ratchet wheel UP motion delta returned by wheelMovement event

        [0] GetWheelMode() -> divert
        [1] SetWheelMode(divert) -> divert
        """
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_OVER_N_VALUES)
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send positive DeltaV Wheel movement")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_NO_NOTIFICATION_RECEIVED)
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check wheelMovement event received scroll up movement.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check deltaV value is between 0x01 to 0x7F (Positive Delta)")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check deltaH value is 0x00.")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_0)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2130_0001", _AUTHOR)
    # end def test_positive_delta_v_with_wheel_movement

    @features("Feature2130")
    @level("Business")
    @services("MainWheel")
    def test_negative_delta_v_with_wheel_movement(self):
        """
        Validate ratchet wheel DOWN motion delta returned by wheelMovement event

        [0] GetWheelMode() -> divert
        [1] SetWheelMode(divert) -> divert
        """
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _TEST_LOOP_OVER_N_VALUES)
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send negative DeltaV Wheel movement")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, _CHECK_NO_NOTIFICATION_RECEIVED)
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check wheelMovement event received scroll down movement.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check deltaV value is between 0x81 to 0xFF (Negative Delta)")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check deltaH value is 0x00.")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_0)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2130_0002", _AUTHOR)
    # end def test_negative_delta_v_with_wheel_movement

    @features("Feature2130")
    @level("Business")
    @services("MainWheel")
    def test_no_event_received_with_no_rotation(self):
        """
        Validate ratchet wheel STILL does not generate wheelMovement event with deltaV=0

        [0] GetWheelMode() -> divert
        [1] SetWheelMode(divert) -> divert
        """
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Main Wheel emulator to Scroll UP once Then to STILL.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check only one wheelMovement Event us received with DeltaV=1")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check No further wheelMovement Event is received with DeltaV=0")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no notification received in HID queue")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Main Wheel emulator to Scroll Down once Then to STILL.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check only one wheelMovement Event us received with DeltaV=FF")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check No further wheelMovement Event is received with DeltaV=0")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no notification received in HID queue")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_0)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2130_0003", _AUTHOR)
    # end def test_no_event_received_with_no_rotation

    @features("Feature2130")
    @level("Business")
    @services("MainWheel")
    def test_no_event_received_in_hid_event(self):
        """
        Validate Roller action does not generate wheelMovement event when in HID Mode

        [0] GetWheelMode() -> divert
        [1] SetWheelMode(divert) -> divert
        """
        raise NotImplementedError('To be implemented when @services("MainWheel") is available')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over various wheel movement UP/DOWN")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:  # TODO: fill this condition
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "No wheelMovement Event should be received.")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check notification received in HID queue.")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_2130_0004", _AUTHOR)
    # end def test_no_event_received_in_hid_event

    @features("Feature2130")
    @features("Feature1802")
    @features("Feature1E00")
    @features("ManageDeactivatableFeaturesAuth")
    @level("Business")
    def test_divert_reverts_after_force_device_reset(self):
        """
        Validate divert mode reverts to Initial state after Device Reset(0x1802)

        [0] GetWheelMode() -> divert
        [1] SetWheelMode(divert) -> divert

        Require 0x1802, 0x1E00, 0x1E02, 0x1602
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.set_mode_status(self, divert=RatchetWheel.DIVERT.HIDPP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HIDPP)
        checker.check_fields(self, response, self.feature_2130.set_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HIDPP)
        checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Hidden features with Manufacturing=True")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send forceDeviceReset request via 1802 Feature.")
        # --------------------------------------------------------------------------------------------------------------
        RatchetWheelTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check getWheelMode response fields, divert is HID mode (0)")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HID)
        checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)

        self.testCaseChecked("BUS_2130_0005", _AUTHOR)
    # end def test_divert_reverts_after_force_device_reset

    @features("Feature2130")
    @level("Business")
    @services("PowerSupply")
    def test_divert_reverts_after_hardware_reset(self):
        """
        Validate divert mode reverts to initial state after device reboot

        [0] GetWheelMode() -> divert

        [1] SetWheelMode(divert) -> divert

        Require Power Supply
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.set_mode_status(self, divert=RatchetWheel.DIVERT.HIDPP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HIDPP)
        checker.check_fields(self, response, self.feature_2130.set_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_GET_WHEEL_MODE_RESPONSE_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HIDPP)
        checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send Hardware.reset through Power Supply emulator")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_connection_reset=False,
                   verify_wireless_device_status_broadcast_event=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check getWheelMode response fields, divert is HID mode (0)")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HID)
        checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)

        self.testCaseChecked("BUS_2130_0006", _AUTHOR)
    # end def test_divert_reverts_after_hardware_reset

    @features("Feature2130")
    @features("Feature1814")
    @features('BLEDevicePairing')
    @features("BLEProConnectionScheme")
    @features("MultipleChannels")
    @level("Business")
    @services("Debugger")
    def test_divert_reverts_after_change_host(self):
        """
        Validate divert mode reverts to initial changing host(0x1814)

        Require 0x1814
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_unpair_all = True
        host_index_0 = 0
        host_index_1 = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Pair device with at least 1 additional host")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.pair_device_to_host(self, host_index_1)
        self.new_channel = self.current_channel

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Switch back to the first host via 0x1814 Feature")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(self, host_index=host_index_0)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_SET_WHEEL_MODE_REQUEST_DIVERT_1)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.set_mode_status(self, divert=RatchetWheel.DIVERT.HIDPP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _VERIFY_SET_WHEEL_MODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HIDPP)
        checker.check_fields(self, response, self.feature_2130.set_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check divert is HID++ Divert mode (1)")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HIDPP)
        checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ChangeHost via 0x1814 Feature")
        # --------------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(self, host_index=host_index_1)
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.new_channel)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_GET_WHEEL_MODE_REQ)
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check divert is HID mode (0)")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HID)
        checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)

        self.testCaseChecked("BUS_2130_0007", _AUTHOR)
    # end def test_divert_reverts_after_change_host
# end class RatchetWheelBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
