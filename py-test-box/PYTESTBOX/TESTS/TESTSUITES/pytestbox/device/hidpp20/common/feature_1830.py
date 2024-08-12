#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
""" @package pytestbox.hid.common.feature_1830

@brief  Validates HID common feature 0x1830

@author Stanislas Cottard

@date   2019/05/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from queue import Empty

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.backlight import Backlight
from pyhid.hidpp.features.common.powermodes import GetPowerModesTotalNumber
from pyhid.hidpp.features.common.powermodes import PowerModes
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ApplicationPowerModesTestCase(BaseTestCase):
    """
    Validates Power Modes TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        # power off device in teardown
        self.post_requisite_poweroff_device = False

        super(ApplicationPowerModesTestCase, self).setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1830)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1830_index, self.feature_1830, _, _ = PowerModesTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Enable the hidden features to get access to the PowerModes feature')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        self.config = self.f.PRODUCT.FEATURES.COMMON.POWER_MODES
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            # Shall make sure to do power-off DUT completely after entered dead and cut-off mode
            if self.post_requisite_poweroff_device:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Power off and restart the device')
                # ------------------------------------------------------------------------------------------------------
                self.power_supply_emulator.restart_device()

                # Since turning off devices that use a unifying dongle will trigger a HidMouse, a HidKeyboard and
                # a DeviceConnection events we just empty the related queues
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
                ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    @features('Feature1830')
    @level('Interface')
    def test_GetPowerModesTotalNumberAPI(self):
        """
        Validate the GetPowerModesTotalNumber request processing

        powerModesTotalNumber = [0]getPowerModesTotalNumber()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetPowerModesTotalNumber')
        # --------------------------------------------------------------------------------------------------------------
        get_power_mode_total_number_response = PowerModesTestUtils.HIDppHelper.get_power_mode_total_number(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetPowerModesTotalNumberResponse.powerModesTotalNumber value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=ChannelUtils.get_device_index(self),
                         obtained=int(Numeral(get_power_mode_total_number_response.deviceIndex)),
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=self.feature_1830_index,
                         obtained=int(Numeral(get_power_mode_total_number_response.featureIndex)),
                         msg='The featureIndex parameter differs from the one expected')
        self.assertEqual(expected=HexList(self.config.F_TotalNumber),
                         obtained=get_power_mode_total_number_response.total_number_of_power_modes,
                         msg='The total_number_of_power_modes parameter differs from the one expected')

        self.testCaseChecked("INT_1830_0001")
    # end def test_GetPowerModesTotalNumberAPI

    @features('Feature1830')
    @level('Interface')
    def test_SetPowerModeAPI(self):
        """
        Validate the SetPowerMode request processing

        powerModeNumber = [1]setPowerMode(powerModeNumber)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_power_mode = self.feature_1830.set_power_mode_cls(device_index=ChannelUtils.get_device_index(self),
                                                              feature_index=self.feature_1830_index,
                                                              power_mode_number=PowerModes.DO_NOTHING)
        set_power_mode_response = ChannelUtils.send(
            test_case=self,
            report=set_power_mode,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1830.set_power_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate SetPowerModeResponse.powerModeNumber value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=set_power_mode.deviceIndex,
                         obtained=set_power_mode_response.deviceIndex,
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=set_power_mode.featureIndex,
                         obtained=set_power_mode_response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')
        self.assertEqual(expected=set_power_mode.power_mode_number,
                         obtained=set_power_mode_response.power_mode_number,
                         msg='The set_power_mode_response parameter differs from the one expected')

        self.testCaseChecked("INT_1830_0002")
    # end def test_SetPowerModeAPI

    @features('Feature1830')
    @level('Functionality')
    @services('PowerSupply')
    @services('JLinkIOSwitch')
    def test_SetPowerMode0Consumption(self):
        """
        Validate the SetPowerMode request with powerModeNumber = 0

        To verify if the current is in the range we desired
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetPowerMode with powerModeNumber = {PowerModes.DO_NOTHING}')
        # --------------------------------------------------------------------------------------------------------------
        set_power_mode = self.feature_1830.set_power_mode_cls(device_index=ChannelUtils.get_device_index(self),
                                                              feature_index=self.feature_1830_index,
                                                              power_mode_number=PowerModes.DO_NOTHING)
        set_power_mode_response = ChannelUtils.send(
            test_case=self,
            report=set_power_mode,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1830.set_power_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetPowerModeResponse.powerModeNumber value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=set_power_mode.power_mode_number,
                         obtained=set_power_mode_response.power_mode_number,
                         msg='The set_power_mode_response parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send command to get current value from power supply')
        # --------------------------------------------------------------------------------------------------------------
        current = CommonBaseTestUtils.EmulatorHelper.get_current(
            self, delay=PowerModesTestUtils.CURRENT_MEASUREMENT_DELAY_TIME) * 1000
        LogHelper.log_info(self, f'Current = {current}uA')

        expected_value = self.config.F_CurrentThresholdDeadMode
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate if the current is bigger than {expected_value}uA')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(current, expected_value,
                           msg=f'The current value {current}uA shall be bigger than {expected_value}uA')

        self.testCaseChecked("FUN_1830_0001")
    # end def test_SetPowerMode0Consumption

    @features('Feature1830')
    @features('Feature1830powerMode', 1)
    @level('Functionality')
    @services('PowerSupply')
    @services('JLinkIOSwitch')
    @bugtracker('SetPowerMode_HighCurrent')
    def test_SetPowerMode1Consumption(self):
        """
        @tc_synopsis    Validate SetPowerMode with powerModeNumber = 1

        To verify if the current is in the range we desired
        """
        # Shall make sure to do power-off DUT completely after entered dead and cut-off mode
        self.post_requisite_poweroff_device = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetPowerMode with powerModeNumber = {PowerModes.DEAD_MODE}')
        # --------------------------------------------------------------------------------------------------------------
        set_power_mode = self.feature_1830.set_power_mode_cls(device_index=ChannelUtils.get_device_index(self),
                                                              feature_index=self.feature_1830_index,
                                                              power_mode_number=PowerModes.DEAD_MODE)
        ChannelUtils.send_only(test_case=self, report=set_power_mode, timeout=.6)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetPowerModeResponse.powerModeNumber value or no error message received')
        # --------------------------------------------------------------------------------------------------------------
        try:
            set_power_mode_response = ChannelUtils.get_only(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.COMMON,
                class_type=self.feature_1830.set_power_mode_response_cls)

            self.assertEqual(expected=set_power_mode.power_mode_number,
                             obtained=set_power_mode_response.power_mode_number,
                             msg='The set_power_mode_response parameter differs from the one expected')
        except (AssertionError, Empty):
            # Check Common message queue is empty
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON, timeout=.1)
            # Check Error code message queue is empty
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR, timeout=.1)
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send command to get current value from power supply')
        # --------------------------------------------------------------------------------------------------------------
        current = CommonBaseTestUtils.EmulatorHelper.get_current(
            self, delay=PowerModesTestUtils.CURRENT_MEASUREMENT_DELAY_TIME) * 1000
        LogHelper.log_info(self, f'Current = {current}uA')

        expected_value = self.config.F_CurrentThresholdDeadMode
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate if the current is below {expected_value}uA')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(current, expected_value,
                        msg=f'The current value {current}uA shall be below {expected_value}uA')

        self.testCaseChecked("FUN_1830_0002")
    # end def test_SetPowerMode1Consumption

    @features('Feature1830')
    @features('Feature1830powerMode', 2)
    @level('Functionality')
    @services('PowerSupply')
    @services('JLinkIOSwitch')
    @bugtracker('SetPowerMode_HighCurrent')
    def test_SetPowerMode2Consumption(self):
        """
        @tc_synopsis    Validate SetPowerMode with powerModeNumber = 2

        To verify if the current is in the range we desired
        """
        # Shall make sure to do power-off DUT completely after entered dead and cut-off mode
        self.post_requisite_poweroff_device = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetPowerMode with powerModeNumber = {PowerModes.FW_CUT_OFF_MODE}')
        # --------------------------------------------------------------------------------------------------------------
        set_power_mode = self.feature_1830.set_power_mode_cls(device_index=ChannelUtils.get_device_index(self),
                                                              feature_index=self.feature_1830_index,
                                                              power_mode_number=PowerModes.FW_CUT_OFF_MODE)
        ChannelUtils.send_only(test_case=self, report=set_power_mode, timeout=.6)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetPowerModeResponse.powerModeNumber value or no error message received')
        # --------------------------------------------------------------------------------------------------------------
        try:
            set_power_mode_response = ChannelUtils.get_only(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.COMMON,
                class_type=self.feature_1830.set_power_mode_response_cls)

            self.assertEqual(expected=set_power_mode.power_mode_number,
                             obtained=set_power_mode_response.power_mode_number,
                             msg='The set_power_mode_response parameter differs from the one expected')
        except (AssertionError, Empty):
            # Check Common message queue is empty
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON, timeout=.1)
            # Check Error code message queue is empty
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR, timeout=.1)
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send command to get current value from power supply')
        # --------------------------------------------------------------------------------------------------------------
        current = CommonBaseTestUtils.EmulatorHelper.get_current(
            self, delay=PowerModesTestUtils.CURRENT_MEASUREMENT_DELAY_TIME) * 1000
        LogHelper.log_info(self, f'Current = {current}uA')

        expected_value = self.config.F_CurrentThresholdDeadMode
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate if the current is below {expected_value}uA')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(current, expected_value,
                        msg=f'The current value {current}uA shall be below {expected_value}uA')

        self.testCaseChecked("FUN_1830_0003")
    # end def test_SetPowerMode2Consumption

    @features('Feature1830')
    @features('Feature1830powerMode', 3)
    @level('Time-consuming')
    @services('PowerSupply')
    @services('JLinkIOSwitch')
    @bugtracker('SetPowerMode_HighCurrent')
    def test_SetPowerMode3Consumption(self):
        """
        @tc_synopsis    Validate SetPowerMode with powerModeNumber = 3

        To verify if the current is in the range we desired
        """
        if self.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_Enabled:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Backup initial NVS")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.NvsHelper.backup_nvs(self)
            self.post_requisite_reload_nvs = True

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Disable Backlight')
            # ----------------------------------------------------------------------------------------------------------
            BacklightTestUtils.HIDppHelper.set_backlight_config(self,
                                                                configuration=Backlight.Configuration.DISABLE,
                                                                options=BacklightTestUtils.get_default_options(self))
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetPowerMode with powerModeNumber = {PowerModes.DEEP_SLEEP}')
        # --------------------------------------------------------------------------------------------------------------
        set_power_mode = self.feature_1830.set_power_mode_cls(device_index=ChannelUtils.get_device_index(self),
                                                              feature_index=self.feature_1830_index,
                                                              power_mode_number=PowerModes.DEEP_SLEEP)
        ChannelUtils.send_only(test_case=self, report=set_power_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Validate SetPowerModeResponse.powerModeNumber value or no error message received')
        # --------------------------------------------------------------------------------------------------------------
        try:
            set_power_mode_response = ChannelUtils.get_only(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.COMMON,
                class_type=self.feature_1830.set_power_mode_response_cls)

            self.assertEqual(expected=set_power_mode.power_mode_number,
                             obtained=set_power_mode_response.power_mode_number,
                             msg='The set_power_mode_response parameter differs from the one expected')
        except (AssertionError, Empty):
            # Check Common message queue is empty
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON, timeout=0.1)
            # Check Error code message queue is empty
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR, timeout=0.1)
        # end try

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send command to get current value from power supply')
        # --------------------------------------------------------------------------------------------------------------
        current = CommonBaseTestUtils.EmulatorHelper.get_current(
            self, delay=PowerModesTestUtils.OPTICAL_SENSOR_SLEEP_TIME, samples=150) * 1000
        LogHelper.log_info(self, f'Current = {current}uA')

        expected_value = self.config.F_CurrentThresholdDeepSleep
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate if the current is below {expected_value}uA')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(current, expected_value,
                        msg=f'The current value {current}uA shall be below {expected_value}uA')

        self.testCaseChecked("FUN_1830_0004")
    # end def test_SetPowerMode3Consumption

    @features('Feature1830')
    @level('ErrorHandling')
    def test_VerifyInvalidFunctionIndexError(self):
        """
        @tc_synopsis    Validates PowerModes robustness processing

        Function indexes valid range [0..1]
        Tests wrong indexes
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over GetPowerModesTotalNumber function index invalid range')
        # --------------------------------------------------------------------------------------------------------------
        for invalid_function_index in compute_wrong_range(
                [x for x in range(self.feature_1830.get_max_function_index() + 1)], max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetPowerModesTotalNumber with a wrong function index value')
            # ----------------------------------------------------------------------------------------------------------
            get_power_mode_total_number = self.feature_1830.get_power_modes_total_number_cls(
                device_index=ChannelUtils.get_device_index(self), feature_index=self.feature_1830_index)
            get_power_mode_total_number.functionIndex = invalid_function_index
            get_power_mode_total_number_response = ChannelUtils.send(
                test_case=self,
                report=get_power_mode_total_number,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidFunctionId (0x07) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_FUNCTION_ID),
                             obtained=get_power_mode_total_number_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for

        self.testCaseChecked("ERR_1830_0001")
    # end def test_VerifyInvalidFunctionIndexError

    @features('Feature1830')
    @level('ErrorHandling')
    @bugtracker('SetPowerMode_ErrorCode')  # Reason explained in the function
    def test_VerifyInvalidPowerModeNumberError(self):
        """
        Validate SetPowerMode processing with an invalid powerModeNumber

        Power Mode Number valid range [0..powerModesTotalNumber]
        Tests wrong indexes
        """
        valid_values = [int(x) for x in self.config.F_NumberList.split(" ")]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over powerModeNumber invalid range')
        # --------------------------------------------------------------------------------------------------------------
        for invalid_power_mode_number in compute_wrong_range(valid_values, min_value=1, max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetPowerMode with wrong powerModeNumber')
            # ----------------------------------------------------------------------------------------------------------
            set_power_mode = self.feature_1830.set_power_mode_cls(device_index=ChannelUtils.get_device_index(self),
                                                                  feature_index=self.feature_1830_index,
                                                                  power_mode_number=invalid_power_mode_number)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            get_power_mode_total_number_response = ChannelUtils.send(
                test_case=self,
                report=set_power_mode,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            """
            This code is following the current specification, however the firmware is not following this part
            of the specification. A change in the specification has been requested.

            "InvalidArgument  [8bits] if parameter powerModeNumber is higher than TOTAL_NUMBER_OF_POWER_MODES
            defined for current project" in Errors for SetPowerMode
            https://sites.google.com/a/logitech.com/samarkand/home/01-common/1830-power-modes

            That is why @unittest.expectedFailure is added to the decorators.
            """
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=get_power_mode_total_number_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
            """
            If the specification change is accepted this commented code is the one to use.
            """
            # self.assertEqual(expected=HexList(ErrorCodes.NOT_ALLOWED),
            #                  obtained=get_power_mode_total_number_response.errorCode,
            #                  msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ERR_1830_0002")
    # end def test_VerifyInvalidPowerModeNumberError

    @features('Feature1830')
    @features('Feature1E00')
    @level('Robustness')
    def test_VerifySoftwareIdIgnored(self):
        """
        Validate the PowerModes softwareId field is ignored

        powerModesTotalNumber = [0]GetPowerModesTotalNumber()
        Request: 0x10.DeviceIndex.FeatureIndex.0x00.0x00.0x00.0x00
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over softwareId validity range')
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GetPowerModesTotalNumber.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetPowerModesTotalNumber with several value for softwareId')
            # ----------------------------------------------------------------------------------------------------------
            get_power_mode_total_number = self.feature_1830.get_power_modes_total_number_cls(
                device_index=ChannelUtils.get_device_index(self), feature_index=self.feature_1830_index)
            get_power_mode_total_number.softwareId = software_id
            get_power_mode_total_number_response = ChannelUtils.send(
                test_case=self,
                report=get_power_mode_total_number,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1830.get_power_modes_total_number_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetPowerModesTotalNumber response received')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_power_mode_total_number.softwareId,
                             obtained=get_power_mode_total_number_response.softwareId,
                             msg='The softwareId parameter differs from the one expected')
            f = self.getFeatures()
            self.assertEqual(expected=HexList(self.config.F_TotalNumber),
                             obtained=get_power_mode_total_number_response.total_number_of_power_modes,
                             msg='The total_number_of_power_modes parameter differs from the one expected')

        self.testCaseChecked("ROB_1830_0001")
    # end def test_VerifySoftwareIdIgnored

    @features('Feature1830')
    @features('Feature1E00')
    @level('Robustness')
    def test_Padding(self):
        """
        Validate the Power Modes padding bytes are ignored

        powerModesTotalNumber = [0]GetPowerModesTotalNumber()
        Request: 0x10.DeviceIndex.FeatureIndex.0x0F.0xAA.0xBB.0xCC
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over GetPowerModesTotalNumber padding range')
        # --------------------------------------------------------------------------------------------------------------
        for padding_byte in compute_sup_values(
                HexList(Numeral(GetPowerModesTotalNumber.DEFAULT.PADDING, GetPowerModesTotalNumber.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetPowerModesTotalNumber with several value for padding')
            # ----------------------------------------------------------------------------------------------------------
            get_power_mode_total_number = self.feature_1830.get_power_modes_total_number_cls(
                device_index=ChannelUtils.get_device_index(self), feature_index=self.feature_1830_index)
            get_power_mode_total_number.padding = padding_byte
            get_power_mode_total_number_response = ChannelUtils.send(
                test_case=self,
                report=get_power_mode_total_number,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1830.get_power_modes_total_number_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetPowerModesTotalNumber response received')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(self.config.F_TotalNumber),
                             obtained=get_power_mode_total_number_response.total_number_of_power_modes,
                             msg='The total_number_of_power_modes parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1830_0002")
    # end def test_Padding
# end class ApplicationPowerModesTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
