#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4610.robustness
:brief: HID++ 2.0 ``MultiRoller`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.keyboard.multiroller import MultiRoller
from pyhid.hidpp.features.keyboard.multiroller import RollerMode
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.multirollerutils import MultiRollerTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4610.multiroller import MultiRollerTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRollerRobustnessTestCase(MultiRollerTestCase):
    """
    Validate ``MultiRoller`` robustness test cases
    """

    @features("Feature4610")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [0] getCapabilities() -> numRollers

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MultiRoller.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.GetCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_4610.get_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0001#1", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature4610")
    @level("Robustness")
    def test_get_roller_capabilities_software_id(self):
        """
        Validate ``GetRollerCapabilities`` software id field is ignored by the firmware

        [1] getRollerCapabilities(roller_id) -> incrementsPerRotation, incrementsPerRatchet, capabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RollerId.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MultiRoller.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRollerCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_roller_capabilities(
                test_case=self,
                roller_id=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRollerCapabilitiesResponseV0 fields")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.GetRollerCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_4610.get_roller_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0001#2", _AUTHOR)
    # end def test_get_roller_capabilities_software_id

    @features("Feature4610")
    @level("Robustness")
    def test_get_mode_software_id(self):
        """
        Validate ``GetMode`` software id field is ignored by the firmware

        [2] getMode(roller_id) -> roller_mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RollerId.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MultiRoller.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_mode(
                test_case=self,
                roller_id=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.GetModeResponseChecker.check_fields(
                self, response, self.feature_4610.get_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0001#3", _AUTHOR)
    # end def test_get_mode_software_id

    @features("Feature4610")
    @level("Robustness")
    def test_set_mode_software_id(self):
        """
        Validate ``SetMode`` software id field is ignored by the firmware

        [3] setMode(roller_id, roller_mode) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RollerId.RollerMode.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(MultiRoller.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.set_mode(
                test_case=self,
                roller_id=0,
                divert=0,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.SetModeResponseChecker.check_fields(
                self, response, self.feature_4610.set_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0001#4", _AUTHOR)
    # end def test_set_mode_software_id

    @features("Feature4610")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [0] getCapabilities() -> numRollers

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4610.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.GetCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_4610.get_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0002#1", _AUTHOR)
    # end def test_get_capabilities_padding

    @features("Feature4610")
    @level("Robustness")
    def test_get_roller_capabilities_padding(self):
        """
        Validate ``GetRollerCapabilities`` padding bytes are ignored by the firmware

        [1] getRollerCapabilities(roller_id) -> incrementsPerRotation, incrementsPerRatchet, capabilities

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RollerId.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4610.get_roller_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRollerCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_roller_capabilities(
                test_case=self,
                roller_id=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetRollerCapabilitiesResponseV0 fields")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.GetRollerCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_4610.get_roller_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0002#2", _AUTHOR)
    # end def test_get_roller_capabilities_padding

    @features("Feature4610")
    @level("Robustness")
    def test_get_mode_padding(self):
        """
        Validate ``GetMode`` padding bytes are ignored by the firmware

        [2] getMode(roller_id) -> roller_mode

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RollerId.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4610.get_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.get_mode(
                test_case=self,
                roller_id=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.GetModeResponseChecker.check_fields(
                self, response, self.feature_4610.get_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0002#3", _AUTHOR)
    # end def test_get_mode_padding

    @features("Feature4610")
    @level("Robustness")
    def test_set_mode_padding(self):
        """
        Validate ``SetMode`` padding bytes are ignored by the firmware

        [3] setMode(roller_id, roller_mode) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.RollerId.RollerMode.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4610.set_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = MultiRollerTestUtils.HIDppHelper.set_mode(
                test_case=self,
                roller_id=0,
                divert=0,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.SetModeResponseChecker.check_fields(
                self, response, self.feature_4610.set_mode_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0002#4", _AUTHOR)
    # end def test_set_mode_padding

    @features("Feature4610")
    @level("Robustness")
    def test_reserved_bits_of_roller_id_in_get_roller_capabilities(self):
        """
        Validate reserved bits of the first input byte shall be ignored by the firmware when sending
        GetRollerCapabilities request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: reserved in sample values(0x1, 0xF + 0x1)")
            # ----------------------------------------------------------------------------------------------------------
            for reserved_bits in range(0x1, 0xF + 0x1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    self, f"Send GetRollerCapabilities request with input={reserved_bits | roller_index}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiRollerTestUtils.HIDppHelper.get_roller_capabilities(
                    test_case=self, reserved=reserved_bits, roller_id=roller_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check GetRollerCapabilities response is not affected by reserved")
                # ------------------------------------------------------------------------------------------------------
                checker = MultiRollerTestUtils.GetRollerCapabilitiesResponseChecker
                check_map = checker.get_check_map(test_case=self, roller_id=roller_index)
                checker.check_fields(test_case=self, message=response,
                                     expected_cls=self.feature_4610.get_roller_capabilities_response_cls,
                                     check_map=check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0003", _AUTHOR)
    # end def test_reserved_bits_of_roller_id_in_get_roller_capabilities

    @features("Feature4610")
    @level("Robustness")
    def test_reserved_bits_of_roller_id_in_get_mode(self):
        """
        Validate reserved bits of the first input byte shall be ignored by the firmware when sending GetMode request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: reserved in sample values(0x1, 0xF + 0x1)")
            # ----------------------------------------------------------------------------------------------------------
            for reserved_bits in range(0x1, 0xF + 0x1):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send GetMode request with input={reserved_bits | roller_index}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiRollerTestUtils.HIDppHelper.get_mode(test_case=self,
                                                                     reserved=reserved_bits,
                                                                     roller_id=roller_index)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check GetMode response is not affected by reserved")
                # ------------------------------------------------------------------------------------------------------
                MultiRollerTestUtils.GetModeResponseChecker.check_fields(
                    self, response, self.feature_4610.get_mode_response_cls)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0004", _AUTHOR)
    # end def test_reserved_bits_of_roller_id_in_get_mode

    @features("Feature4610")
    @level("Robustness")
    def test_reserved_bits_of_roller_id_in_set_mode(self):
        """
        Validate reserved bits of the first input byte shall be ignored by the firmware when sending SetMode request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: reserved in sample values(0x10, 0xF0 + 0x10, 0x10)")
            # ----------------------------------------------------------------------------------------------------------
            for reserved_bits in range(0x10, 0xF0 + 0x10, 0x10):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetMode request with input={reserved_bits | roller_index}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self,
                                                                     roller_id=reserved_bits | roller_index,
                                                                     divert=RollerMode.DEFAULT_MODE)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetMode response is not affected by reserved")
                # ------------------------------------------------------------------------------------------------------
                checker = MultiRollerTestUtils.SetModeResponseChecker
                check_map = checker.get_check_map(roller_id=roller_index, divert=RollerMode.DEFAULT_MODE)
                checker.check_fields(self, response, self.feature_4610.set_mode_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0005", _AUTHOR)
    # end def test_reserved_bits_of_roller_id_in_set_mode

    @features("Feature4610")
    @level("Robustness")
    def test_reserved_bits_of_roller_mode_in_set_mode(self):
        """
        Validate reserved bits of 'roller_mode' shall be ignored by the firmware when sending SetMode request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop roller_index in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop: reserved in sample values(0x02, 0xFF, 0x2)")
            # ----------------------------------------------------------------------------------------------------------
            for reserved_bits in range(0x2, 0xFF, 0x2):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetMode request with roller_mode={reserved_bits}")
                # ------------------------------------------------------------------------------------------------------
                response = MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self,
                                                                     roller_id=roller_index,
                                                                     divert=reserved_bits)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Check SetMode response is not affected by reserved")
                # ------------------------------------------------------------------------------------------------------
                checker = MultiRollerTestUtils.SetModeResponseChecker
                check_map = checker.get_check_map(roller_id=roller_index, divert=RollerMode.DEFAULT_MODE)
                checker.check_fields(self, response, self.feature_4610.set_mode_response_cls, check_map)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4610_0006", _AUTHOR)
    # end def test_reserved_bits_of_roller_mode_in_set_mode
# end class MultiRollerRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
