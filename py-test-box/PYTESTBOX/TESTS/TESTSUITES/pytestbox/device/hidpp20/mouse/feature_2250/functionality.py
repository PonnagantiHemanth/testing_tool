#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2250.functionality
:brief: HID++ 2.0 ``AnalysisMode`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/08/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import randint

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.analysismode import AccumulationPacket
from pyhid.hidpp.features.mouse.analysismode import AnalysisMode
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analysismodeutils import AnalysisModeTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hid.base.hidreportutils import to_signed_int
from pytestbox.device.hidpp20.mouse.feature_2250.analysismode import AnalysisModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalysisModeFunctionalityTestCase(AnalysisModeTestCase):
    """
    Validate ``AnalysisMode`` functionality test cases
    """

    @features('Feature2250')
    @level('Functionality')
    def test_all_analysis_mode(self):
        """
        Validate SetAnalysisMode mode validity range

        Check all possible values [0..1]
        """
        on = AnalysisMode.MODE.ON
        off = AnalysisMode.MODE.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as ON')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, on)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as OFF')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, off)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, off)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Send SetAnalysisMode request with mode parameter as ON 2 times in a row')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(2):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'SetAnalysisMode ON {i + 1}\n')
            # ----------------------------------------------------------------------------------------------------------
            AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, on)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Send SetAnalysisMode request with mode parameter as OFF 2 times in a row')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(2):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'SetAnalysisMode OFF {i + 1}\n')
            # ----------------------------------------------------------------------------------------------------------
            AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, off)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, off)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        self.testCaseChecked("FUN_2250_0001")
    # end def test_all_analysis_mode

    @features('Feature2250')
    @features('Feature1802')
    @level('Functionality')
    def test_get_mode_hidpp_reset(self):
        """
        Validate Analysis mode returned to 'OFF' after a hidpp reset
        """
        off = AnalysisMode.MODE.OFF
        on = AnalysisMode.MODE.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as ON')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, on)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable manufacturing features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do a Hidpp Reset on the device')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, off)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        self.testCaseChecked("FUN_2250_0002")
    # end def test_get_mode_hidpp_reset

    @features('Feature2250')
    @level('Functionality')
    @services('HardwareReset')
    def test_get_mode_hardware_reset(self):
        """
        Validate Analysis mode returned to 'OFF' after a hardware reset
        """

        off = AnalysisMode.MODE.OFF
        on = AnalysisMode.MODE.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request as ON')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, on)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do a hardware reset on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_connection_reset=False,
                   verify_wireless_device_status_broadcast_event=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisMode request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, off)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        self.testCaseChecked("FUN_2250_0003")
    # end def test_get_mode_hardware_reset

    @features('Feature2250')
    @level('Functionality')
    @services('OpticalSensor')
    def test_set_analysis_mode_flow(self):
        """
        Validate multiple calls to SetAnalysisMode to 'ON' does not reset the accumulated data
        """
        on = AnalysisMode.MODE.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as ON')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, on)
            }
        )
        checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAnalysisData request to clear the buffers")
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Clear the pending HID Mouse messages')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(self, HIDDispatcher.QueueName.MOUSE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Emulate motion on X and Y")
        # --------------------------------------------------------------------------------------------------------------
        x, y = randint(1, 16), randint(1, 16)
        self.emulate_continuous_motion(self, x, y)
        self.emulate_continuous_motion(self, -x, -y)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Send SetAnalysisMode to ON many times in a row')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(randint(1, 3)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'SetAnalysisMode ON {i + 1}\n')
            # ----------------------------------------------------------------------------------------------------------
            AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Provide stimuli to generate a displacement on X and Y')
            # ----------------------------------------------------------------------------------------------------------
            x, y = randint(1, 16), randint(1, 16)
            self.emulate_continuous_motion(self, x, y)
            self.emulate_continuous_motion(self, -x, -y)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisDataResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        # Retrieve X and Y displacement from the HID mouse interface
        expected_counters = HexList(self.compute_cumulative_displacement(self))

        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "data": (checker.check_data, expected_counters)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        self.testCaseChecked("FUN_2250_0004")
    # end def test_set_analysis_mode_flow

    @features('Feature2250')
    @level('Functionality')
    @services('HardwareReset')
    @services('OpticalSensor')
    def test_get_analysis_data_flow(self):
        """
        Validate data is zeroed after a reset or a call to getAnalysisData
        """
        on = AnalysisMode.MODE.ON
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetAnalysisMode request with mode parameter as ON')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, on)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SetAnalysisModeResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, on)
            }
        )
        checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate positive and negative motions on X and Y')
        # --------------------------------------------------------------------------------------------------------------
        x, y = randint(1, 16), randint(1, 16)
        self.emulate_continuous_motion(self, x, y)
        self.emulate_continuous_motion(self, -x, -y)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request for the second time')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisDataResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate positive and negative motions on X and Y')
        # --------------------------------------------------------------------------------------------------------------
        x, y = randint(1, 16), randint(1, 16)
        self.emulate_continuous_motion(self, x, y)
        self.emulate_continuous_motion(self, -x, -y)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_connection_reset=False,
                   verify_wireless_device_status_broadcast_event=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisDataResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        self.testCaseChecked("FUN_2250_0005")
    # end def test_get_analysis_data_flow

    @features('Feature2250v1')
    @features('SaturatedData')
    @level('ReleaseCandidate')
    @services('OpticalSensor')
    def test_get_analysis_data_saturation_positive_x(self):
        """
        Validate data will not be reset but will be clamped at max values for accuPositiveX counter if device
        supports an overflow saturation
        """
        self.set_analysis_mode_on()

        self.set_highest_reporting_rate()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli generating an overflow on positive X')
        # --------------------------------------------------------------------------------------------------------------
        self.emulate_continuous_motion(self, x=self.positive_clamped_value + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisData.data.accuPositiveX value is clamped at max possible value')
        # --------------------------------------------------------------------------------------------------------------
        expected_counters = AccumulationPacket()
        expected_counters.accuPositiveX = self.positive_clamped_value

        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "data": (checker.check_data, HexList(expected_counters))
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        self.testCaseChecked("FUN_2250_0006#1")
    # end def test_get_analysis_data_saturation_positive_x

    @features('Feature2250v1')
    @features('SaturatedData')
    @level('ReleaseCandidate')
    @services('OpticalSensor')
    def test_get_analysis_data_saturation_other_axis(self):
        """
        Validate data will not be reset but will be clamped at max values for accuPositiveY, accuNegativeX and
        accuNegativeY counters if device supports an overflow saturation
        """
        self.set_analysis_mode_on()

        self.set_highest_reporting_rate()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli generating an overflow on negative X')
        # --------------------------------------------------------------------------------------------------------------
        self.emulate_continuous_motion(self, x=to_signed_int(Numeral(self.negative_clamped_value)) - 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisData.data.accuNegativeX value is clamped at max possible value')
        # --------------------------------------------------------------------------------------------------------------
        expected_counters = AccumulationPacket()
        expected_counters.accuNegativeX = self.negative_clamped_value

        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "data": (checker.check_data, HexList(expected_counters))
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli generating an overflow on positive Y')
        # --------------------------------------------------------------------------------------------------------------
        self.emulate_continuous_motion(self, y=self.positive_clamped_value + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisData.data.accuPositiveY value is clamped at max possible value')
        # --------------------------------------------------------------------------------------------------------------
        expected_counters = AccumulationPacket()
        expected_counters.accuPositiveY = self.positive_clamped_value

        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "data": (checker.check_data, HexList(expected_counters))
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli generating an overflow on negative Y')
        # --------------------------------------------------------------------------------------------------------------
        self.emulate_continuous_motion(self, y=to_signed_int(Numeral(self.negative_clamped_value)) - 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisData.data.accuNegativeY value is clamped at max possible value')
        # --------------------------------------------------------------------------------------------------------------
        expected_counters = AccumulationPacket()
        expected_counters.accuNegativeY = self.negative_clamped_value

        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "data": (checker.check_data, HexList(expected_counters))
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        self.testCaseChecked("FUN_2250_0006#2")
    # end def test_get_analysis_data_saturation_other_axis

    @features('Feature2250')
    @features('NoSaturatedData')
    @level('Time-consuming')
    @services('OpticalSensor')
    def test_get_analysis_data_overflow(self):
        """
        Validate one specific counter is zeroed after an overflow
        """
        self.set_analysis_mode_on()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli generating an overflow on positive X')
        # --------------------------------------------------------------------------------------------------------------
        self.emulate_continuous_motion(self, x=self.positive_clamped_value + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisData.data.positive X value has been cleared')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli generating an overflow on negative X')
        # --------------------------------------------------------------------------------------------------------------
        self.emulate_continuous_motion(self, x=to_signed_int(Numeral(self.negative_clamped_value)) - 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisData.data.negative X value has been cleared')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli generating an overflow on positive Y')
        # --------------------------------------------------------------------------------------------------------------
        self.emulate_continuous_motion(self, y=self.negative_clamped_value + 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisData.data.positive Y value has been cleared')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Provide stimuli generating an overflow on negative Y')
        # --------------------------------------------------------------------------------------------------------------
        self.emulate_continuous_motion(self, y=to_signed_int(Numeral(self.negative_clamped_value)) - 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetAnalysisData request')
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetAnalysisData.data.negative Y value has been cleared')
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

        self.testCaseChecked("FUN_2250_0007")
    # end def test_get_analysis_data_overflow

    @features('Feature2250')
    @level('Functionality')
    @services('OpticalSensor')
    def test_get_analysis_data_byte_transition(self):
        """
        Validate GetAnalysisData accumulation buffer increment at boundary values and during byte transition

          accuPositiveX and accuPositiveY counter values:
          1. 0x00 to 0x01
          2. 0xFF to 0x100
          3. 0xFFFF to 0x10000
          4. 0xFFFFFF to 0x1000000
          5. 0x7FFFFFFF (max value)

          accuPositiveY and accuNegativeY counter values:
          1. 0x00 to 0xFFFFFFFF
          2. 0xFFFFFF01 to 0xFFFFFF00
          3. 0xFFFF0001 to 0xFFFF0000
          4. 0xFF000001 to 0xFF000000
          5. 0x80000000 (max value)
        """
        self.set_analysis_mode_on()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over X and Y positive and negative displacements")
        # --------------------------------------------------------------------------------------------------------------
        for counter in ['accuPositiveX', 'accuNegativeX', 'accuPositiveY', 'accuNegativeY']:
            x_motion = 1 if counter == 'accuPositiveX' else -1 if counter == 'accuNegativeX' else 0
            y_motion = 1 if counter == 'accuPositiveY' else -1 if counter == 'accuNegativeY' else 0
            cumulative_value = self.twos_complement(x_motion or y_motion)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Provide stimuli to generate a displacement and force the {counter} counter '
                                     f'from 0 to {cumulative_value}')
            # ----------------------------------------------------------------------------------------------------------
            self.emulate_continuous_motion(self, x_motion, y_motion)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetAnalysisData request')
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check GetAnalysisDataResponse.data.{counter} value is {cumulative_value}')
            # ----------------------------------------------------------------------------------------------------------
            expected_packet = AccumulationPacket()
            expected_packet.setValue(expected_packet.getFidFromName(counter), cumulative_value)
            checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "data": (checker.check_data, expected_packet)
                }
            )
            checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Compute x and y motion values for next byte transition')
            # ----------------------------------------------------------------------------------------------------------
            x_motion_values = [0xFF, 1] if counter == 'accuPositiveX' else [-0xFF, -1] if counter == 'accuNegativeX' \
                else [0, 0]
            y_motion_values = [0xFF, 1] if counter == 'accuPositiveY' else [-0xFF, -1] if counter == 'accuNegativeY' \
                else [0, 0]
            motion_values = list(filter(any, [x_motion_values, y_motion_values]))[0]
            cumulative_value = self.twos_complement(sum(motion_values))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Provide stimuli to generate a displacement and force the {counter} counter '
                                     f'from {self.twos_complement(motion_values[0])} to '
                                     f'{cumulative_value}')
            # ----------------------------------------------------------------------------------------------------------
            for x, y in zip(x_motion_values, y_motion_values):
                self.emulate_continuous_motion(self, x, y)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetAnalysisData request')
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check GetAnalysisDataResponse.data.{counter} value is {cumulative_value}')
            # ----------------------------------------------------------------------------------------------------------
            expected_packet = AccumulationPacket()
            expected_packet.setValue(expected_packet.getFidFromName(counter), cumulative_value)
            checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "data": (checker.check_data, expected_packet)
                }
            )
            checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Compute x and y motion values for next byte transition')
            # ----------------------------------------------------------------------------------------------------------
            x_motion_values = [0xFFF, 1] if counter == 'accuPositiveX' else [-0xFFF, -1] if counter == 'accuNegativeX' \
                else [0, 0]
            y_motion_values = [0xFFF, 1] if counter == 'accuPositiveY' else [-0xFFF, -1] if counter == 'accuNegativeY' \
                else [0, 0]
            motion_values = list(filter(any, [x_motion_values, y_motion_values]))[0]
            cumulative_value = self.twos_complement(sum(motion_values))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Provide stimuli to generate a displacement and force the {counter} counter '
                                     f'from {self.twos_complement(motion_values[0])} to {cumulative_value}')
            # ----------------------------------------------------------------------------------------------------------
            for x, y in zip(x_motion_values, y_motion_values):
                self.emulate_continuous_motion(self, x, y)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetAnalysisData request')
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check {counter} counter value is {cumulative_value}')
            # ----------------------------------------------------------------------------------------------------------
            expected_packet = AccumulationPacket()
            expected_packet.setValue(expected_packet.getFidFromName(counter), cumulative_value)
            checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "data": (checker.check_data, expected_packet)
                }
            )
            checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Compute x and y motion values for next byte transition')
            # ----------------------------------------------------------------------------------------------------------
            x_motion_values = [0xFFFFFF, 1] if counter == 'accuPositiveX' else [-0xFFFFFF, -1] if \
                counter == 'accuNegativeX' else [0, 0]
            y_motion_values = [0xFFFFFF, 1] if counter == 'accuPositiveY' else [-0xFFFFFF, -1] if \
                counter == 'accuNegativeY' else [0, 0]
            motion_values = list(filter(any, [x_motion_values, y_motion_values]))[0]
            cumulative_value = self.twos_complement(sum(motion_values))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Provide stimuli to generate a displacement and force the {counter} counter '
                                     f'from {self.twos_complement(motion_values[0])} to {cumulative_value}')
            # ----------------------------------------------------------------------------------------------------------
            for x, y in zip(x_motion_values, y_motion_values):
                self.emulate_continuous_motion(self, x, y)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetAnalysisData request')
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

            expected_packet = AccumulationPacket()
            expected_packet.setValue(expected_packet.getFidFromName(counter), cumulative_value)
            checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "data": (checker.check_data, expected_packet)
                }
            )
            checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Compute x and y motion values for next byte transition')
            # ----------------------------------------------------------------------------------------------------------
            x_motion_value = self.positive_clamped_value if counter == 'accuPositiveX' else \
                self.negative_clamped_value if counter == 'accuNegativeX' else 0
            y_motion_value = self.positive_clamped_value if counter == 'accuPositiveY' else \
                self.negative_clamped_value if counter == 'accuNegativeY' else 0
            cumulative_displacement = self.twos_complement(x_motion_value or y_motion_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Provide stimuli to generate a displacement and '
                                     f'force the {counter} counter to max value {cumulative_displacement}')
            # ----------------------------------------------------------------------------------------------------------
            for x, y in zip(x_motion_values, y_motion_values):
                self.emulate_continuous_motion(self, x, y)
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetAnalysisData request')
            # ----------------------------------------------------------------------------------------------------------
            response = AnalysisModeTestUtils.HIDppHelper.get_analysis_data(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check GetAnalysisData.data.counter value is {cumulative_value}')
            # ----------------------------------------------------------------------------------------------------------
            expected_packet = AccumulationPacket()
            expected_packet.setValue(expected_packet.getFidFromName(counter), cumulative_value)
            checker = AnalysisModeTestUtils.GetAnalysisDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "data": (checker.check_data, expected_packet)
                }
            )
            checker.check_fields(self, response, self.feature_2250.get_analysis_data_response_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_2250_0008")
    # end def test_get_analysis_data_byte_transition
# end class AnalysisModeFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
