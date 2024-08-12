#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
""" @package pytestbox.hid.mouse.feature_2121

@brief  Validates HID mouse feature 0x2121

@author Andy Su

@date   2019/3/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import BaseTestCase
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pyhid.hidpp.features.hireswheel import HiResWheel
from pyhid.hidpp.features.hireswheel import GetWheelCapability
from pyhid.hidpp.features.hireswheel import GetWheelCapabilityResponse
from pyhid.hidpp.features.hireswheel import GetWheelMode
from pyhid.hidpp.features.hireswheel import GetWheelModeResponse
from pyhid.hidpp.features.hireswheel import SetWheelModev0
from pyhid.hidpp.features.hireswheel import SetWheelModev0Response
from pyhid.hidpp.features.hireswheel import GetWheelCapabilityv1Response
from pyhid.hidpp.features.hireswheel import GetWheelModev1Response
from pyhid.hidpp.features.hireswheel import SetWheelModev1
from pyhid.hidpp.features.hireswheel import SetWheelModev1Response
from pyhid.hidpp.features.hireswheel import GetRatchetSwitchState
from pyhid.hidpp.features.hireswheel import GetRatchetSwitchStateResponse
from pyhid.hidpp.features.hireswheel import GetAnalyticsData
from pyhid.hidpp.features.hireswheel import GetAnalyticsDataResponse
from pyhid.hidpp.features.hireswheel import GetAnalyticsDataHERZOGResponse

from pylibrary.tools.util import compute_inf_values
import unittest


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HiResWheelTestCase(BaseTestCase):
    """
    Validates HiRes Wheel TestCases
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(HiResWheelTestCase, self).setUp()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x2121)')
        # ---------------------------------------------------------------------------
        self.feature_id = self.updateFeatureMapping(feature_id=HiResWheel.FEATURE_ID)

    # end def setUp

    @features('Feature2121')
    @level('Interface')
    def test_GetWheelCapability(self):
        """
        Validates GetWheelCapability normal processing (Feature 0x2121)

        HiRes Wheel
         multiplier, hasSwitch, hasInvert [0]GetWheelCapability
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send HiResWheel.GetWheelCapability')
        # ---------------------------------------------------------------------------
        get_wheel_capability = GetWheelCapability(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        get_wheel_capability_response = self.send_report_wait_response(
            report=get_wheel_capability,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetWheelCapabilityResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetWheelCapability.multiplier value')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Multiplier,
                         obtained=int(get_wheel_capability_response.multiplier),
                         msg='The multiplier parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetWheelCapability.hasSwitch value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_HasSwitch,
                         obtained=int(get_wheel_capability_response.hasSwitch),
                         msg='The hasSwitch parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate GetWheelCapability.hasInvert value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_HasInvert,
                         obtained=int(get_wheel_capability_response.hasInvert),
                         msg='The hasInvert parameter differs from the one expected')

        self.testCaseChecked("FNT_2121_0001")
    # end def test_GetWheelCapability

    @features('Feature2121v1+')
    @level('Interface')
    def test_GetWheelCapabilityV1(self):
        """
        Validates GetWheelCapability v1 normal processing (Feature 0x2121)

        HiRes Wheel
         multiplier, hasSwitch, hasInvert, hasAnalyticsData, ratchetsPerRotation, wheelDiameter [0]GetWheelCapability v1
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send HiResWheel.GetWheelCapability v1')
        # ---------------------------------------------------------------------------
        get_wheel_capability = GetWheelCapability(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        get_wheel_capability_response = self.send_report_wait_response(
            report=get_wheel_capability,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetWheelCapabilityv1Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetWheelCapability v1.hasAnalyticsData value')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_HasAnalyticsData,
                         obtained=int(get_wheel_capability_response.hasAnalyticsData),
                         msg='The hasAnalytics parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetWheelCapability v1.ratchetsPerRotation value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_RatchetsPerRotation,
                         obtained=int(get_wheel_capability_response.ratchetsPerRotation),
                         msg='The ratchetsPerRotation parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate GetWheelCapability v1.wheelDiameter value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_WheelDiameter,
                         obtained=int(get_wheel_capability_response.wheelDiameter),
                         msg='The wheelDiameter parameter differs from the one expected')

        self.testCaseChecked("FNT_2121_0002")
    # end def test_GetWheelCapabilityV1

    @features('Feature2121')
    @level('Interface')
    def test_GetWheelMode(self):
        """
        Validates GetWheelMode normal processing (Feature 0x2121)

        HiRes Wheel
         target, resolution, invert [1]GetWheelMode
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send HiResWheel.GetWheelMode')
        # ---------------------------------------------------------------------------
        get_wheel_mode = GetWheelMode(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        get_wheel_mode_response = self.send_report_wait_response(
            report=get_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetWheelModeResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetWheelMode.target value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=True,
                         obtained=int(get_wheel_mode_response.target) in HiResWheel.TARGETS,
                         msg='The target parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetWheelMode.resolution value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=True,
                         obtained=int(get_wheel_mode_response.resolution) in HiResWheel.RESOLUTIONS,
                         msg='The resolution parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate GetWheelMode.invert value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=True,
                         obtained=int(get_wheel_mode_response.invert) in HiResWheel.INVERTS,
                         msg='The invert parameter differs from the one expected')

        self.testCaseChecked("FNT_2121_0003")
    # end def test_GetWheelMode

    @features('Feature2121v1+')
    @level('Interface')
    def test_GetWheelModeV1(self):
        """
        Validates GetWheelMode v1 normal processing (Feature 0x2121)

        HiRes Wheel
         target, resolution, invert, analytics [1]GetWheelMode v1
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send HiResWheel.GetWheelMode v1')
        # ---------------------------------------------------------------------------
        get_wheel_mode = GetWheelMode(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        get_wheel_mode_response = self.send_report_wait_response(
            report=get_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetWheelModev1Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetWheelMode v1.analytics value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=True,
                         obtained=int(get_wheel_mode_response.analytics) in HiResWheel.ANALYTICS,
                         msg='The analytics parameter differs from the one expected')

        self.testCaseChecked("FNT_2121_0004")
    # end def test_GetWheelModeV1

    @features('Feature2121')
    @level('Interface')
    def test_SetWheelModeV0(self):
        """
        Validates SetWheelMode v0 normal processing (Feature 0x2121)

        HiRes Wheel
         target, resolution, invert [2]SetWheelMode v0(target, resolution, invert)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetWheelMode v0 with parameter value (1,1,1)')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev0(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        invert=HiResWheel.INVERT,
                                        resolution=HiResWheel.HIGH_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        set_wheel_mode_response = self.send_report_wait_response(
            report=set_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=SetWheelModev0Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate SetWheelMode v0.target value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.HIDPP,
                         obtained=int(set_wheel_mode_response.target),
                         msg='The target parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate SetWheelMode v0.resolution value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.HIGH_RESOLUTION,
                         obtained=int(set_wheel_mode_response.resolution),
                         msg='The resolution parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate SetWheelMode v0.invert value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.INVERT,
                         obtained=int(set_wheel_mode_response.invert),
                         msg='The invert parameter differs from the one expected')

        self.testCaseChecked("FNT_2121_0005")
    # end def test_SetWheelModeV0

    @features('Feature2121v1+')
    @level('Interface')
    def test_SetWheelModeV1(self):
        """
        Validates SetWheelMode v1 normal processing (Feature 0x2121)

        HiRes Wheel
         target, resolution, invert, analytics [2]SetWheelMode v1(target, resolution, invert, analytics)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetWheelMode v1 with parameter value (1,1,1,1)')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        analytics=HiResWheel.ANALYTIC,
                                        invert=HiResWheel.INVERT,
                                        resolution=HiResWheel.HIGH_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        set_wheel_mode_response = self.send_report_wait_response(
            report=set_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=SetWheelModev1Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate SetWheelMode v1.target value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.HIDPP,
                         obtained=int(set_wheel_mode_response.target),
                         msg='The target parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate SetWheelMode v1.resolution value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.HIGH_RESOLUTION,
                         obtained=int(set_wheel_mode_response.resolution),
                         msg='The resolution parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate SetWheelMode v1.invert value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.INVERT,
                         obtained=int(set_wheel_mode_response.invert),
                         msg='The invert parameter differs from the one expected')
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Validate SetWheelMode v1.analytics value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.ANALYTIC,
                         obtained=int(set_wheel_mode_response.analytics),
                         msg='The analytics parameter differs from the one expected')

        self.testCaseChecked("FNT_2121_0006")
    # end def test_SetWheelModeV1

    @features('Feature2121')
    @level('Business', 'SmokeTests')
    def test_SetWheelModeWithAllSets(self):
        """
        Validates SetWheelMode v0 Business case sequence (Feature 0x2121)

        HiRes Wheel
         target, resolution, invert [1]GetWheelMode
         target, resolution, invert [2]SetWheelMode v0(target, resolution, invert)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over all combination of (target, resolution, invert) values '
                       'Test Step 1: Send SetWheelMode v0 with different parameter (target, resolution, invert) values')
        # ---------------------------------------------------------------------------
        wheel_mode_sets = gen_wheel_mode_sets(version=0)
        for item in wheel_mode_sets:
            set_wheel_mode = SetWheelModev0(deviceIndex=self.deviceIndex,
                                            featureId=self.feature_id,
                                            reserved=HiResWheel.DEFAULT_RESERVED,
                                            invert=item[2],
                                            resolution=item[1],
                                            target=item[0])
            set_wheel_mode_response = self.send_report_wait_response(
                report=set_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=SetWheelModev0Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send HiResWheel.GetWheelMode')
            # ---------------------------------------------------------------------------
            get_wheel_mode = GetWheelMode(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_mode_response = self.send_report_wait_response(
                report=get_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetWheelModeResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Compare return value of SetWheelMode v0.target with GetWheelMode.target')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=int(set_wheel_mode_response.target),
                             obtained=int(get_wheel_mode_response.target),
                             msg='The target parameter differs from the one expected')
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Compare return value of SetWheelMode v0.resolution '
                           'with GetWheelMode.resolution')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=int(set_wheel_mode_response.resolution),
                             obtained=int(get_wheel_mode_response.resolution),
                             msg='The resolution parameter differs from the one expected')
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Compare return value of SetWheelMode v0.invert with GetWheelMode.invert')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=int(set_wheel_mode_response.invert),
                             obtained=int(get_wheel_mode_response.invert),
                             msg='The invert parameter differs from the one expected')
        # end for

        self.testCaseChecked("FNT_2121_0007")
    # end def test_SetWheelModeWithAllSets

    @features('Feature2121v1+')
    @level('Business')
    def test_SetWheelModeWithAllSetsV1(self):
        """
        Validates SetWheelMode v1 Business case sequence (Feature 0x2121)

        HiRes Wheel
         target, resolution, invert, analytics [1]GetWheelMode v1
         target, resolution, invert, analytics [2]SetWheelMode v1(target, resolution, invert, analytics)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over all combination of (target, resolution, invert, analytics) values '
                       'Test Step 1: Send SetWheelMode v1 with different parameter'
                       '(target, resolution, invert, analytics) values')
        # ---------------------------------------------------------------------------
        wheel_mode_sets = gen_wheel_mode_sets(version=1)
        for item in wheel_mode_sets:
            set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                            featureId=self.feature_id,
                                            reserved=HiResWheel.DEFAULT_RESERVED,
                                            analytics=item[3],
                                            invert=item[2],
                                            resolution=item[1],
                                            target=item[0])
            set_wheel_mode_response = self.send_report_wait_response(
                report=set_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=SetWheelModev1Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send HiResWheel.GetWheelMode v1')
            # ---------------------------------------------------------------------------
            get_wheel_mode = GetWheelMode(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_mode_response = self.send_report_wait_response(
                report=get_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetWheelModev1Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Compare return value of SetWheelMode v1.target with GetWheelMode v1.target')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=int(set_wheel_mode_response.target),
                             obtained=int(get_wheel_mode_response.target),
                             msg='The target parameter differs from the one expected')
            # ---------------------------------------------------------------------------
            self.logTitle2(
                'Test Check 2: Compare return value of SetWheelMode v1.resolution with GetWheelMode v1.resolution')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=int(set_wheel_mode_response.resolution),
                             obtained=int(get_wheel_mode_response.resolution),
                             msg='The resolution parameter differs from the one expected')
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Compare return value of SetWheelMode v1.invert with GetWheelMode v1.invert')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=int(set_wheel_mode_response.invert),
                             obtained=int(get_wheel_mode_response.invert),
                             msg='The invert parameter differs from the one expected')
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 4: Compare return value of SetWheelMode v1.analytics '
                           'with GetWheelMode v1.analytics')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=int(set_wheel_mode_response.analytics),
                             obtained=int(get_wheel_mode_response.analytics),
                             msg='The analytics parameter differs from the one expected')
        # end for

        self.testCaseChecked("FNT_2121_0008")
    # end def test_SetWheelModeWithAllSetsV1

    @features('Feature2121')
    @level('Interface')
    def test_GetRatchetSwitchState(self):
        """
        Validate GetRatchetSwitchState normal processing (Feature 0x2121)

        HiRes Wheel
         state [3]GetRatchetSwitchState
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send HiResWheel.GetRatchetSwitchState')
        # ---------------------------------------------------------------------------
        get_ratchet_switch_state = GetRatchetSwitchState(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        get_ratchet_switch_state_response = self.send_report_wait_response(
            report=get_ratchet_switch_state,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetRatchetSwitchStateResponse)
        
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetRatchetSwitchState.state value')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=True,
                         obtained=int(get_ratchet_switch_state_response.state) in HiResWheel.STATES,
                         msg='The state parameter differs from the one expected')

        self.testCaseChecked("FNT_2121_0009")
    # end def test_GetRatchetSwitchState

    @features('Feature2121v1+')
    @level('Interface')
    @unittest.skip("Need HERZOG device to know its real behavior")
    def test_GetAnalyticsData_HERZOG(self):
        """
        Validate GetAnalyticsData normal processing (Feature 0x2121)

        HiRes Wheel
         initEpmChargeAdcBattLevel, epmChargingTime, endEpmChargeAdcBattLevel, temperature [4]GetAnalyticsData
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send HiResWheel.GetAnalyticsData')
        # ---------------------------------------------------------------------------
        get_analytics_data = GetAnalyticsData(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        get_analytics_data_response = self.send_report_wait_response(
            report=get_analytics_data,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetAnalyticsDataHERZOGResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetAnalyticsData.initEpmChargeAdcBattLevel value in valid range')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetAnalyticsData.epmChargingTime value in valid range')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate GetAnalyticsData.endEpmChargeAdcBattLevel value in valid range')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Validate GetAnalyticsData.temperature value in valid range')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0010")
    # end def test_GetAnalyticsData

    @features('Feature2121')
    @level('Interface')
    @services('ButtonPressed')
    def test_RatchetSwitch(self):
        """
        Validate RatchetSwitch normal processing (Feature 0x2121)

        HiRes Wheel
         state [event1]RatchetSwitch
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Use EVT test tool to send ratchet mode signal(0->1) to emulate')
        # ---------------------------------------------------------------------------
        # TODO: call the graviton emulator service to trigger a stimuli on the smartshift button

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate the return value of RatchetSwitch.state')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0011")
    # end def test_RatchetSwitch

    @features('Feature2121')
    @level('Business')
    @services('ButtonPressed')
    def test_RatchetSwitchWithTwoPress(self):
        """
        Validate RatchetSwitch Business case sequence (Feature 0x2121)

        HiRes Wheel
         state [event1]RatchetSwitch
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Use EVT test tool to send ratchet mode signal(0->1) to emulate')
        # ---------------------------------------------------------------------------
        # TODO: call the graviton emulator service to trigger a stimuli on the smartshift button

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Compare the return value of RatchetSwitch.state with GetRatchetSwitchState.state')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Use EVT test tool to send ratchet mode signal(1->0) to emulate')
        # ---------------------------------------------------------------------------
        # TODO: call the graviton emulator service to trigger a stimuli on the smartshift button

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Compare the return value of RatchetSwitch.state with GetRatchetSwitchState.state')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0012")
    # end def test_RatchetSwitchWithTwoPress

    @features('Feature2121')
    @level('Interface')
    @services('MainWheel')
    def test_WheelMovement(self):
        """
        Validate WheelMovement normal processing (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Use EVT test tool to emulate a scrolling')
        # ---------------------------------------------------------------------------
        # TODO: call the graviton emulator service to trigger a wheel rotation

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate WheelMovement.resolution value')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate WheelMovement.periods value')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate WheelMovement.deltaV value')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0013")
    # end def test_WheelMovement

    @features('Feature2121')
    @level('Functionality')
    @services('MainWheel')
    def test_WheelMoventmentWithHighResolution(self):
        """
        Validate the change of WheelMovement.deltaV according to high-resolution
        with HID++ notification (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetWheelMode v0 with (1, 1, 0) for (target, resolution, invert)')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev0(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        invert=HiResWheel.NOT_INVERT,
                                        resolution=HiResWheel.HIGH_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        set_wheel_mode_response = self.send_report_wait_response(
            report=set_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=SetWheelModev0Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Use EVT test tool to send scroll signal to emulate')
        # ---------------------------------------------------------------------------
        # TODO: call the graviton emulator service to trigger a wheel rotation

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate WheelMovement.resolution value')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate WheelMovement.deltaV value')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0014")
    # end def test_WheelMovementWithHighResolution

    @features('Feature2121v1+')
    @level('Functionality')
    @services('MainWheel')
    def test_WheelMoventmentWithHighResolutionv1(self):
        """
        Validate the change of WheelMovement.deltaV according to high-resolution
        with HID++ notification (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(
            'Test Step 1: Send SetWheelMode v1 with (1, 1, 0, 0) for (target, resolution, invert, analytics)')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        analytics=HiResWheel.NON_ANALYTIC,
                                        invert=HiResWheel.NOT_INVERT,
                                        resolution=HiResWheel.HIGH_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        set_wheel_mode_response = self.send_report_wait_response(
            report=set_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=SetWheelModev1Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Use EVT test tool to send scroll signal to emulate')
        # ---------------------------------------------------------------------------
        # TODO: call the graviton emulator service to trigger a wheel rotation

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate WheelMovement.resolution value')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate WheelMovement.deltaV value')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0015")
    # end def test_WheelMovementWithHighResolutionv1

    @features('Feature2121')
    @level('Functionality')
    @services('MainWheel')
    def test_WheelMoventmentWithInversion(self):
        """
        Validate the change of WheelMovement.deltaV according to inversion
        with HID++ notification (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetWheelMode v0 with (1, 0, 1) for (target, resolution, invert)')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev0(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        invert=HiResWheel.INVERT,
                                        resolution=HiResWheel.LOW_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        set_wheel_mode_response = self.send_report_wait_response(
            report=set_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=SetWheelModev0Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Use EVT test tool to send scroll signal to emulate')
        # ---------------------------------------------------------------------------
        # TODO: call the graviton emulator service to trigger a wheel rotation

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate WheelMovement.resolution value')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate WheelMovement.deltaV value')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0016")
    # end def test_WheelMovementWithInversion

    @features('Feature2121v1+')
    @level('Functionality')
    @services('MainWheel')
    def test_WheelMovementWithInversionV1(self):
        """
        Validate the change of WheelMovement.deltaV according to inversion
        with HID++ notification (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(
            'Test Step 1: Send SetWheelMode v1 with (1, 0, 1, 0) for (target, resolution, invert, analytics)')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        analytics=HiResWheel.NON_ANALYTIC,
                                        invert=HiResWheel.INVERT,
                                        resolution=HiResWheel.LOW_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        set_wheel_mode_response = self.send_report_wait_response(
            report=set_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=SetWheelModev1Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Use EVT test tool to send scroll signal to emulate')
        # ---------------------------------------------------------------------------
        # TODO: call the graviton emulator service to trigger a wheel rotation

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate WheelMovement.resolution value')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate WheelMovement.deltaV value')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0017")
    # end def test_WheelMovementWithInversionV1

    @features('Feature2121')
    @level('Functionality')
    @services('MainWheel')
    def test_WheelMovementSwitchTarget(self):
        """
        Validate the WheelMovement response by switching the target bit back and force from 0 to 1
        in SetWheelMode v0 (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over target values in [0, 1, 0] '
                       'Test Step 1: Send SetWheelMode v0 with the parameter(target, resolution=0, invert=0)')
        # ---------------------------------------------------------------------------
        for target in [HiResWheel.HID, HiResWheel.HIDPP, HiResWheel.HID]:
            set_wheel_mode = SetWheelModev0(deviceIndex=self.deviceIndex,
                                            featureId=self.feature_id,
                                            reserved=HiResWheel.DEFAULT_RESERVED,
                                            invert=HiResWheel.NOT_INVERT,
                                            resolution=HiResWheel.LOW_RESOLUTION,
                                            target=target)
            set_wheel_mode_response = self.send_report_wait_response(
                report=set_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=SetWheelModev0Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Use EVT test tool to emulate a scrolling')
            # ---------------------------------------------------------------------------
            # TODO: call the graviton emulator service to trigger a wheel rotation

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate the response on the expected end-point')
            # ---------------------------------------------------------------------------

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Validate the other end-points do not receive anything')
            # ---------------------------------------------------------------------------

        # end for

        self.testCaseChecked("FNT_2121_0018")
    # end def test_WheelMovementSwitchTarget

    @features('Feature2121v1+')
    @level('Functionality')
    @services('MainWheel')
    def test_WheelMovementSwitchTargetV1(self):
        """
        Validate the WheelMovement response by switching the target bit back and force from 0 to 1
        in SetWheelMode v1 (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over target values in [0, 1, 0] '
                       'Test Step 1: Send SetWheelMode v1 with the parameter'
                       '(target, resolution=0, invert=0, analytics=0)')
        # ---------------------------------------------------------------------------
        for target in [HiResWheel.HID, HiResWheel.HIDPP, HiResWheel.HID]:
            set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                            featureId=self.feature_id,
                                            reserved=HiResWheel.DEFAULT_RESERVED,
                                            analytics=HiResWheel.NON_ANALYTIC,
                                            invert=HiResWheel.NOT_INVERT,
                                            resolution=HiResWheel.LOW_RESOLUTION,
                                            target=target)
            set_wheel_mode_response = self.send_report_wait_response(
                report=set_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=SetWheelModev1Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Use EVT test tool to emulate a scrolling')
            # ---------------------------------------------------------------------------
            # TODO: call the graviton emulator service to trigger a wheel rotation

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate the response on the expected end-point')
            # ---------------------------------------------------------------------------

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Validate the other end-points do not receive anything')
            # ---------------------------------------------------------------------------

        # end for

        self.testCaseChecked("FNT_2121_0019")
    # end def test_WheelMovementSwitchTargetV1

    @features('Feature2121')
    @level('Functionality')
    @services('ButtonPressed')
    @services('MainWheel')
    def test_WheelMovementPeriodValue(self):
        """
        Validate if WheelMovement.period is not equal to 1 when interrupt by changing
        rachet mode or send SetWheelMode v0 (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Use EVT test tool to emulate a scrolling')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Use EVT test tool to switch ratchet mode (0->1 on the button I/O)')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send SetWheelMode v0 request')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev0(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        invert=HiResWheel.NOT_INVERT,
                                        resolution=HiResWheel.LOW_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        set_wheel_mode_response = self.send_report_wait_response(
            report=set_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=SetWheelModev0Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate WheelMovement.periods is not equal to 1 after the interrupt events')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0020")
    # end def test_WheelMovementPeriodValue

    @features('Feature2121v1+')
    @level('Functionality')
    @services('ButtonPressed')
    @services('MainWheel')
    def test_WheelMovementPeriodValueV1(self):
        """
        Validate if WheelMovement.period is not equal to 1 when interrupt by changing
        rachet mode or send SetWheelMode v1 (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Use EVT test tool to emulate a scrolling')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Use EVT test tool to switch ratchet mode (0->1 on the button I/O)')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send SetWheelMode v1 request')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        analytics=HiResWheel.NON_ANALYTIC,
                                        invert=HiResWheel.NOT_INVERT,
                                        resolution=HiResWheel.LOW_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        set_wheel_mode_response = self.send_report_wait_response(
            report=set_wheel_mode,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=SetWheelModev1Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate WheelMovement.periods is not equal to 1 after the interrupt events')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0021")
    # end def test_WheelMovementPeriodValueV1

    @features('Feature2121v1+')
    @level('Functionality')
    def test_GetAnalyticsDataWithZero(self):
        """
        Validate SetWheelMode v1 with target=1, analytics=0 and get analytics data (Feature 0x2121)

        HiRes Wheel
          initEpmChargeAdcBattLevel, epmChargingTime, endEpmChargeAdcBattLevel, temperature [4]GetAnalyticsData
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(
            'Test Step 1: Send SetWheelMode v1 with (1, 0, 0, 0) for (target, resolution, invert, analytics)')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        analytics=HiResWheel.NON_ANALYTIC,
                                        invert=HiResWheel.NOT_INVERT,
                                        resolution=HiResWheel.LOW_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        self.send_report_wait_response(report=set_wheel_mode,
                                       response_queue=self.hidDispatcher.mouse_message_queue,
                                       response_class_type=SetWheelModev1Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send GetAnalyticsData')
        # ---------------------------------------------------------------------------
        get_analytics_data = GetAnalyticsData(
            deviceIndex=self.deviceIndex,
            featureId=self.feature_id)
        get_analytics_data_response = self.send_report_wait_response(
            report=get_analytics_data,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetAnalyticsDataResponse)

        herzog_response = GetAnalyticsDataHERZOGResponse.fromHexList(HexList(get_analytics_data_response))
        self.logTrace('GetAnalyticsData HERZOG Response: %s\n' % str(herzog_response))

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate that the analytics data are all equal to 0s')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=int(herzog_response.initEpmChargeAdcBattLevel),
                         msg='The initEpmChargeAdcBattLevel parameter differs from the one expected')

        self.assertEqual(expected=0,
                         obtained=int(herzog_response.epmChargingTime),
                         msg='The epmChargingTime parameter differs from the one expected')

        self.assertEqual(expected=0,
                         obtained=int(herzog_response.endEpmChargeAdcBattLevel),
                         msg='The endEpmChargeAdcBattLevel parameter differs from the one expected')

        self.assertEqual(expected=0,
                         obtained=int(herzog_response.temperature),
                         msg='The temperature parameter differs from the one expected')

        self.testCaseChecked("FNT_2121_0022")
    # end def test_GetAnalyticsDataWithZero

    @features('Feature2121v1+')
    @level('Functionality')
    @unittest.skip("Need HERZOG device to know its real behavior")
    def test_GetAnalyticsDataWithOne(self):
        """
        Validate SetWheelMode v1 with target=1, analytics=1 and get analytics data (Feature 0x2121)

        HiRes Wheel
          initEpmChargeAdcBattLevel, epmChargingTime, endEpmChargeAdcBattLevel, temperature [4]GetAnalyticsData
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(
            'Test Step 1: Send SetWheelMode v1 with (1, 0, 0, 1) for (target, resolution, invert, analytics)')
        # ---------------------------------------------------------------------------
        set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                        featureId=self.feature_id,
                                        reserved=HiResWheel.DEFAULT_RESERVED,
                                        analytics=HiResWheel.ANALYTIC,
                                        invert=HiResWheel.NOT_INVERT,
                                        resolution=HiResWheel.LOW_RESOLUTION,
                                        target=HiResWheel.HIDPP)
        self.send_report_wait_response(report=set_wheel_mode,
                                       response_queue=self.hidDispatcher.mouse_message_queue,
                                       response_class_type=SetWheelModev1Response)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send GetAnalyticsData')
        # ---------------------------------------------------------------------------
        get_analytics_data = GetAnalyticsData(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        get_analytics_data_response = self.send_report_wait_response(
            report=get_analytics_data,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetAnalyticsDataHERZOGResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate the analytics data')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_2121_0023")
    # end def test_GetAnalyticsDataWithOne

    @features('Feature2121')
    @level('Business')
    @services('MainWheel')
    def test_WheelMovementScrollUpAndDown(self):
        """
        Validate WheelMovement Business case sequence (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetWheelMode v0 with the last 2 bits consist'
                       'of (0,1) for (target=1, resolution, invert)')
        # ---------------------------------------------------------------------------
        wheel_mode_sets = [item for item in gen_wheel_mode_sets(version=0) if item[0] != 0]
        for item in wheel_mode_sets:
            set_wheel_mode = SetWheelModev0(deviceIndex=self.deviceIndex,
                                            featureId=self.feature_id,
                                            reserved=HiResWheel.DEFAULT_RESERVED,
                                            invert=item[2],
                                            resolution=item[1],
                                            target=item[0])
            self.send_report_wait_response(report=set_wheel_mode,
                                           response_queue=self.hidDispatcher.mouse_message_queue,
                                           response_class_type=SetWheelModev0Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send GetWheelMode')
            # ---------------------------------------------------------------------------
            get_wheel_mode = GetWheelMode(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_mode_response = self.send_report_wait_response(
                report=get_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetWheelModeResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Use EVT test tool to emulate a scrolling')
            # ---------------------------------------------------------------------------

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Compare the return value of GetWheelMode.resolution '
                           'with WheelMovement.resolution')
            # ---------------------------------------------------------------------------

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Validate WheelMovement.periods value')
            # ---------------------------------------------------------------------------

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Validate change of WheelMovement.deltaV according to the '
                           'GetWheelMode.resolution and GetWheelMode.invert')
            # ---------------------------------------------------------------------------

        # end for

        self.testCaseChecked("FNT_2121_0024")
    # end def test_WheelMovementScrollUpAndDown

    @features('Feature2121v1+')
    @level('Business')
    @services('MainWheel')
    def test_WheelMovementScrollUpAndDownv1(self):
        """
        Validate WheelMovement Business case sequence (Feature 0x2121)

        HiRes Wheel
         resolution, periods, deltaV [event0]WheelMovement
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetWheelMode v1 with the last 2 bits consist'
                       'of (0,1) for (target=1, resolution, invert, analytics=0)')
        # ---------------------------------------------------------------------------
        wheel_mode_sets = [item for item in gen_wheel_mode_sets(version=1) if item[0] == 1 and item[3] == 0]
        for item in wheel_mode_sets:
            set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                            featureId=self.feature_id,
                                            reserved=HiResWheel.DEFAULT_RESERVED,
                                            analytics=item[3],
                                            invert=item[2],
                                            resolution=item[1],
                                            target=item[0])
            self.send_report_wait_response(report=set_wheel_mode,
                                           response_queue=self.hidDispatcher.mouse_message_queue,
                                           response_class_type=SetWheelModev1Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send GetWheelMode v1')
            # ---------------------------------------------------------------------------
            get_wheel_mode = GetWheelMode(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_mode_response = self.send_report_wait_response(
                report=get_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetWheelModev1Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Use EVT test tool to emulate a scrolling')
            # ---------------------------------------------------------------------------

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Compare the return value of GetWheelMode v1.resolution '
                           'with WheelMovement.resolution')
            # ---------------------------------------------------------------------------

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Validate WheelMovement.periods value')
            # ---------------------------------------------------------------------------

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Validate change of WheelMovement.deltaV according to the '
                           'GetWheelMode v1.resolution and GetWheelMode v1.invert')
            # ---------------------------------------------------------------------------

        # end for

        self.testCaseChecked("FNT_2121_0025")
    # end def test_WheelMovementScrollUpAndDownv1

    @features('Feature2121v0')
    @level('ErrorHandling')
    def test_WrongFunctionIndex(self):
        """
        Validates HiResWheel robustness processing for v0

        Function indexes valid range [0..3],
            Tests wrong indexes
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetWheelCapability with wrong index value')
        # ---------------------------------------------------------------------------
        for function_index in compute_wrong_range(list(range(HiResWheel.MAX_FUNCTION_INDEX + 1)), max_value=0xF):
            get_wheel_capability = GetWheelCapability(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_capability.functionIndex = int(function_index)
            get_wheel_capability_response = self.send_report_wait_response(
                report=get_wheel_capability,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check Error Codes InvalidFunctionId (7) returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=get_wheel_capability.featureIndex,
                             obtained=get_wheel_capability_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_wheel_capability_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for

        self.testCaseChecked("ROT_1000_0001")
    # end def test_WrongFunctionIndex

    @features('Feature2121v1+')
    @level('ErrorHandling')
    def test_WrongFunctionIndexV1(self):
        """
        Validates HiResWheel robustness processing for v1

        Function indexes valid range [0..4],
            Tests wrong indexes
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetWheelCapability v1 with wrong index value')
        # ---------------------------------------------------------------------------
        for function_index in compute_wrong_range(list(range(HiResWheel.MAX_FUNCTION_INDEX_V1 + 1)), max_value=0xF):
            get_wheel_capability = GetWheelCapability(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_capability.functionIndex = int(function_index)
            get_wheel_capability_response = self.send_report_wait_response(
                report=get_wheel_capability,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check Error Codes InvalidFunctionId (7) returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=get_wheel_capability.featureIndex,
                             obtained=get_wheel_capability_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_wheel_capability_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for

        self.testCaseChecked("ROT_1000_0002")
    # end def test_WrongFunctionIndexV1

    @features('Feature2121v0')
    @level('Robustness')
    def test_OtherRsvBits(self):
        """
        Validate the reservation bit of input for doesn't affect the bit we desired of output

        wheelMode = [2]SetWheelMode v0(target, resolution, invert)
        Request: 0x10.DeviceIndex.FeatureIndex.0x0F.0xFF.0x00.0x00
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetWheelMode v0 with several value for wheelMode')
        # ---------------------------------------------------------------------------
        reserved_value = HiResWheel.DEFAULT_RESERVED
        for power_value in range(5):
            reserved_value = reserved_value + pow(2, power_value)
            set_wheel_mode = SetWheelModev0(deviceIndex=self.deviceIndex,
                                            featureId=self.feature_id,
                                            reserved=reserved_value,
                                            invert=HiResWheel.NOT_INVERT,
                                            resolution=HiResWheel.LOW_RESOLUTION,
                                            target=HiResWheel.HIDPP)
            set_wheel_mode_response = self.send_report_wait_response(
                report=set_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=SetWheelModev0Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate SetWheelMode v0 response received')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=HiResWheel.HIDPP,
                             obtained=int(set_wheel_mode_response.target),
                             msg='The target parameter differs from the one expected')
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Validate if reservation bits of output is echoed')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=reserved_value,
                             obtained=int(set_wheel_mode_response.reserved),
                             msg='The target parameter differs from the one expected')
        # end for

        self.testCaseChecked("ROT_1000_0003")
    # end def test_OtherRsvBits

    @features('Feature2121v1+')
    @level('Robustness')
    def test_OtherRsvBitsV1(self):
        """
        Validate the reservation bit of input for v1 doesn't affect the bit we desired of output

        wheelMode = [2]SetWheelMode v1(target, resolution, invert, analytics)
        Request: 0x10.DeviceIndex.FeatureIndex.0x0F.0xFF.0x00.0x00
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send SetWheelMode v1 with several value for wheelMode')
        # ---------------------------------------------------------------------------
        reserved_value = HiResWheel.DEFAULT_RESERVED
        for power_value in range(4):
            reserved_value = reserved_value + pow(2, power_value)
            set_wheel_mode = SetWheelModev1(deviceIndex=self.deviceIndex,
                                            featureId=self.feature_id,
                                            reserved=reserved_value,
                                            analytics=HiResWheel.NON_ANALYTIC,
                                            invert=HiResWheel.NOT_INVERT,
                                            resolution=HiResWheel.LOW_RESOLUTION,
                                            target=HiResWheel.HIDPP)
            set_wheel_mode_response = self.send_report_wait_response(
                report=set_wheel_mode,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=SetWheelModev1Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate SetWheelMode v1 response received')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=HiResWheel.HIDPP,
                             obtained=int(set_wheel_mode_response.target),
                             msg='The target parameter differs from the one expected')
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Validate if reservation bits of output is echoed')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=reserved_value,
                             obtained=int(set_wheel_mode_response.reserved),
                             msg='The target parameter differs from the one expected')
        # end for

        self.testCaseChecked("ROT_1000_0004")
    # end def test_OtherRsvBitsV1

    @features('Feature2121')
    @level('Robustness')
    def test_OtherSoftwareId(self):
        """
        Validates HiResWheel softwareId are ignored

        getWheelCapability = [0]GetWheelCapability
        Request: 0x10.DeviceIndex.FeatureIndex.0x01.0x00.0x00.0x00
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetWheelCapability with several value for softwareId')
        # ---------------------------------------------------------------------------
        for software_id in compute_inf_values(GetWheelCapability.DEFAULT.SOFTWARE_ID)[1:]:
            get_wheel_capability = GetWheelCapability(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_capability.softwareId = software_id
            get_wheel_capability_response = self.send_report_wait_response(
                report=get_wheel_capability,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetWheelCapabilityResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate GetWheelCapability response received')
            # ---------------------------------------------------------------------------
            f = self.getFeatures()
            self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Multiplier,
                             obtained=int(get_wheel_capability_response.multiplier),
                             msg='The multiplier parameter differs from the one expected')
        # end for

        self.testCaseChecked("ROT_2201_0005")
    # end def test_OtherSoftwareId

    @features('Feature2121v1+')
    @level('Robustness')
    def test_OtherSoftwareIdV1(self):
        """
        Validates HiResWheel softwareId are ignored

        getWheelCapability = [0]GetWheelCapability v1
        Request: 0x10.DeviceIndex.FeatureIndex.0x01.0x00.0x00.0x00
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetWheelCapability v1 with several value for softwareId')
        # ---------------------------------------------------------------------------
        for software_id in compute_inf_values(GetWheelCapability.DEFAULT.SOFTWARE_ID)[1:]:
            get_wheel_capability = GetWheelCapability(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_capability.softwareId = software_id
            get_wheel_capability_response = self.send_report_wait_response(
                report=get_wheel_capability,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetWheelCapabilityv1Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate GetWheelCapability v1 response received')
            # ---------------------------------------------------------------------------
            f = self.getFeatures()
            self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Multiplier,
                             obtained=int(get_wheel_capability_response.multiplier),
                             msg='The multiplier parameter differs from the one expected')
        # end for

        self.testCaseChecked("ROT_2201_0006")
    # end def test_OtherSoftwareIdv1

    @features('Feature2121')
    @level('Robustness')
    def test_OtherPaddingBytes(self):
        """
        Validates HiResWheel padding bytes are ignored

        getWheelCapability = [0]GetWheelCapability
        Request: 0x10.DeviceIndex.FeatureIndex.0x0F.0xAA.0xBB.0xCC
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetWheelCapability with several value for padding')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(GetWheelCapability.DEFAULT.PADDING,
                                                             GetWheelCapability.LEN.PADDING // 8))):
            get_wheel_capability = GetWheelCapability(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_capability.padding = padding_byte
            get_wheel_capability_response = self.send_report_wait_response(
                report=get_wheel_capability,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetWheelCapabilityResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate GetWheelCapability response received')
            # ---------------------------------------------------------------------------
            f = self.getFeatures()
            self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Multiplier,
                             obtained=int(get_wheel_capability_response.multiplier),
                             msg='The multiplier parameter differs from the one expected')
        # end for

        self.testCaseChecked("ROT_2201_0007")
    # end def test_OtherPaddingBytes

    @features('Feature2121v1+')
    @level('Robustness')
    def test_OtherPaddingBytesV1(self):
        """
        Validates HiResWheel padding bytes are ignored

        getWheelCapability = [0]GetWheelCapability v1
        Request: 0x10.DeviceIndex.FeatureIndex.0x0F.0xAA.0xBB.0xCC
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetWheelCapability v1 with several value for padding')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(GetWheelCapability.DEFAULT.PADDING,
                                                             GetWheelCapability.LEN.PADDING // 8))):
            get_wheel_capability = GetWheelCapability(deviceIndex=self.deviceIndex, featureId=self.feature_id)
            get_wheel_capability.padding = padding_byte
            get_wheel_capability_response = self.send_report_wait_response(
                report=get_wheel_capability,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetWheelCapabilityv1Response)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate GetWheelCapability v1 response received')
            # ---------------------------------------------------------------------------
            f = self.getFeatures()
            self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Multiplier,
                             obtained=int(get_wheel_capability_response.multiplier),
                             msg='The multiplier parameter differs from the one expected')
        # end for

        self.testCaseChecked("ROT_2201_0008")
    # end def test_OtherPaddingBytesV1

    @features('Feature2121v1+')
    @level('ErrorHandling')
    @unittest.skip("Need HERZOG device to know its real behavior")
    def test_GetUnsupportedAnalyticsData(self):
        """
        Validate get analytics data when analytics not supported

        If hasAnalyticsData is false, get analytics data will raise an error
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetAnalyticsData')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Error Codes "Unsupported" returned by the device')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_2201_0009")
    # end def test_GetUnsupportedAnalyticsData
# end class HiResWheelTestCase


# Function that generate sets for set wheel mode
def gen_wheel_mode_sets(version):
    wheel_mode_sets = []
    if version == 0:
        for i in range(8):
            tmp = tuple(map(int, list('{0:b}'.format(i).zfill(3))))
            wheel_mode_sets.append(tmp)
        wheel_mode_sets.append((0, 0, 0))
    elif version == 1:
        for i in range(16):
            tmp = tuple(map(int, list('{0:b}'.format(i).zfill(4))))
            wheel_mode_sets.append(tmp)
        wheel_mode_sets.append((0, 0, 0, 0))
    return wheel_mode_sets

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
