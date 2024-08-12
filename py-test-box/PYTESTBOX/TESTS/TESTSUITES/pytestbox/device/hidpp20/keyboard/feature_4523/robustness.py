#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4523.robustness
:brief: HID++ 2.0 ``DisableControlsByCIDX`` robustness test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDX
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4523.disablecontrolsbycidx import DisableControlsByCIDXTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDXRobustnessTestCase(DisableControlsByCIDXTestCase):
    """
    Validate ``DisableControlsByCIDX`` robustness test cases
    """

    @features("Feature4523")
    @level("Robustness")
    def test_set_disabled_controls_software_id(self):
        """
        Validate ``SetDisabledControls`` software id field is ignored by the firmware

        [0] setDisabledControls(cidxBitmap) -> None

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.CidxBitmap

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(DisableControlsByCIDX.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisabledControls request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetDisabledControlsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DisableControlsByCIDXTestUtils.MessageChecker.check_fields(
                self, response, self.feature_4523.set_disabled_controls_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4523_0001#1", _AUTHOR)
    # end def test_set_disabled_controls_software_id

    @features("Feature4523")
    @level("Robustness")
    def test_get_game_mode_software_id(self):
        """
        Validate ``GetGameMode`` software id field is ignored by the firmware

        [1] getGameMode() -> gameModeFullState

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(DisableControlsByCIDX.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetGameMode request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetGameModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DisableControlsByCIDXTestUtils.GetGameModeResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_4523.get_game_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4523_0001#2", _AUTHOR)
    # end def test_get_game_mode_software_id

    @features("Feature4523v1")
    @level("Robustness")
    def test_get_set_power_on_params_software_id(self):
        """
        Validate ``GetSetPowerOnParams`` software id field is ignored by the firmware

        [2] getSetPowerOnParams(setMask, setValue) -> getValue

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SetMask.SetValue.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        poweron_game_mode_lock_valid = False
        poweron_game_mode_valid = False
        poweron_game_mode_lock = False
        poweron_game_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(DisableControlsByCIDX.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSetPowerOnParams request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(
                test_case=self,
                poweron_game_mode_lock_valid=poweron_game_mode_lock_valid,
                poweron_game_mode_valid=poweron_game_mode_valid,
                poweron_game_mode_lock=poweron_game_mode_lock,
                poweron_game_mode=poweron_game_mode,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSetPowerOnParamsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DisableControlsByCIDXTestUtils.GetSetPowerOnParamsResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_4523.get_set_power_on_params_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4523_0001#3", _AUTHOR)
    # end def test_get_set_power_on_params_software_id

    @features("Feature4523v1")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        [3] getCapabilities() -> supportedPowerOnParams

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(DisableControlsByCIDX.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = DisableControlsByCIDXTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DisableControlsByCIDXTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_4523.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4523_0001#4", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature4523")
    @level("Robustness")
    def test_get_game_mode_padding(self):
        """
        Validate ``GetGameMode`` padding bytes are ignored by the firmware

        [1] getGameMode() -> gameModeFullState

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4523.get_game_mode_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetGameMode request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetGameModeResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DisableControlsByCIDXTestUtils.GetGameModeResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_4523.get_game_mode_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4523_0002#1", _AUTHOR)
    # end def test_get_game_mode_padding

    @features("Feature4523v1")
    @level("Robustness")
    def test_get_set_power_on_params_padding(self):
        """
        Validate ``GetSetPowerOnParams`` padding bytes are ignored by the firmware

        [2] getSetPowerOnParams(setMask, setValue) -> getValue

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.SetMask.SetValue.0xPP

        Padding (PP) boundary values [00..FF]
        """
        poweron_game_mode_lock_valid = False
        poweron_game_mode_valid = False
        poweron_game_mode_lock = False
        poweron_game_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4523.get_set_power_on_params_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetSetPowerOnParams request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params(
                test_case=self,
                poweron_game_mode_lock_valid=poweron_game_mode_lock_valid,
                poweron_game_mode_valid=poweron_game_mode_valid,
                poweron_game_mode_lock=poweron_game_mode_lock,
                poweron_game_mode=poweron_game_mode,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetSetPowerOnParamsResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DisableControlsByCIDXTestUtils.GetSetPowerOnParamsResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_4523.get_set_power_on_params_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4523_0002#2", _AUTHOR)
    # end def test_get_set_power_on_params_padding

    @features("Feature4523v1")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        [3] getCapabilities() -> supportedPowerOnParams

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_4523.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = DisableControlsByCIDXTestUtils.HIDppHelper.get_capabilities(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DisableControlsByCIDXTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_4523.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_4523_0002#3", _AUTHOR)
    # end def test_get_capabilities_padding

    def disable_all_controls(self):
        """
        Disable all controls and verify the response of the command
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setDisabledControls request with cidx_bitmap = 0xFF * 16")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(
            test_case=self,
            cidx_7=1, cidx_6=1, cidx_5=1, cidx_4=1, cidx_3=1, cidx_2=1, cidx_1=1, cidx_0=1,
            cidx_15=1, cidx_14=1, cidx_13=1, cidx_12=1, cidx_11=1, cidx_10=1, cidx_9=1, cidx_8=1,
            cidx_23=1, cidx_22=1, cidx_21=1, cidx_20=1, cidx_19=1, cidx_18=1, cidx_17=1, cidx_16=1,
            cidx_31=1, cidx_30=1, cidx_29=1, cidx_28=1, cidx_27=1, cidx_26=1, cidx_25=1, cidx_24=1,
            cidx_39=1, cidx_38=1, cidx_37=1, cidx_36=1, cidx_35=1, cidx_34=1, cidx_33=1, cidx_32=1,
            cidx_47=1, cidx_46=1, cidx_45=1, cidx_44=1, cidx_43=1, cidx_42=1, cidx_41=1, cidx_40=1,
            cidx_55=1, cidx_54=1, cidx_53=1, cidx_52=1, cidx_51=1, cidx_50=1, cidx_49=1, cidx_48=1,
            cidx_63=1, cidx_62=1, cidx_61=1, cidx_60=1, cidx_59=1, cidx_58=1, cidx_57=1, cidx_56=1,
            cidx_71=1, cidx_70=1, cidx_69=1, cidx_68=1, cidx_67=1, cidx_66=1, cidx_65=1, cidx_64=1,
            cidx_79=1, cidx_78=1, cidx_77=1, cidx_76=1, cidx_75=1, cidx_74=1, cidx_73=1, cidx_72=1,
            cidx_87=1, cidx_86=1, cidx_85=1, cidx_84=1, cidx_83=1, cidx_82=1, cidx_81=1, cidx_80=1,
            cidx_95=1, cidx_94=1, cidx_93=1, cidx_92=1, cidx_91=1, cidx_90=1, cidx_89=1, cidx_88=1,
            cidx_103=1, cidx_102=1, cidx_101=1, cidx_100=1, cidx_99=1, cidx_98=1, cidx_97=1, cidx_96=1,
            cidx_111=1, cidx_110=1, cidx_109=1, cidx_108=1, cidx_107=1, cidx_106=1, cidx_105=1, cidx_104=1,
            cidx_119=1, cidx_118=1, cidx_117=1, cidx_116=1, cidx_115=1, cidx_114=1, cidx_113=1, cidx_112=1,
            cidx_127=1, cidx_126=1, cidx_125=1, cidx_124=1, cidx_123=1, cidx_122=1, cidx_121=1, cidx_120=1)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDisabledControlsResponse fields")
        # ----------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.MessageChecker.check_fields(
            self, response, self.feature_4523.set_disabled_controls_response_cls, {})
    # end def disable_all_controls

    def enable_all_controls(self):
        """
        Enable all control and verify the response of the command
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setDisabledControls request with cidx_bitmap = 0x0 * 16")
        # --------------------------------------------------------------------------------------------------------------
        response = DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls(test_case=self)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDisabledControlsResponse fields")
        # ----------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.MessageChecker.check_fields(
            self, response, self.feature_4523.set_disabled_controls_response_cls, {})
    # end def enable_all_controls

    @features("Feature4523")
    @level("Robustness")
    def test_check_disable_all_controls(self):
        """
        Check setDisabledControls(cidx_bitmap = 0xFF * 16) i.e. disable all controls
        """
        self.disable_all_controls()
        self.testCaseChecked("ROB_4523_0003", _AUTHOR)
    # end def test_check_disable_all_controls

    @features("Feature4523")
    @level("Robustness")
    def test_check_re_enable_all_controls(self):
        """
        Check setDisabledControls(cidx_bitmap = 0x00 * 16) i.e. re-enable all controls
        """
        self.disable_all_controls()
        self.enable_all_controls()
        self.testCaseChecked("ROB_4523_0004", _AUTHOR)
    # end def test_check_re_enable_all_controls

# end class DisableControlsByCIDXRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
