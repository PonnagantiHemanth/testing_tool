#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
""" @package pytestbox.hid.mouse.feature_2100

@brief  Validates HID mouse feature 0x2100

@author christophe roquebert

@date   2019/03/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import BaseTestCase
from pyharness.selector import features
from pyharness.extensions import level
from pyhid.hidpp.features.verticalscrolling import VerticalScrolling
from pyhid.hidpp.features.verticalscrolling import GetRollerInfo
from pyhid.hidpp.features.verticalscrolling import GetRollerInfoResponse
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pylibrary.tools.util import compute_inf_values
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VerticalScrollingTestCase(BaseTestCase):
    """
    Validates VerticalScrolling TestCases
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(VerticalScrollingTestCase, self).setUp()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x2100)')
        # ---------------------------------------------------------------------------
        self.feature_id = self.updateFeatureMapping(feature_id=VerticalScrolling.FEATURE_ID)
    # end def setUp

    @features('Feature2100')
    @level('Interface')
    def test_GetRollerInfo(self):
        """
        Validates GetRollerInfo normal processing (Feature 0x2100)

         rollerInfo[0]GetRollerInfo ()
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send VerticalScrolling.GetRollerInfo')
        # ---------------------------------------------------------------------------
        get_roller_info = GetRollerInfo(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        get_roller_info_response = self.send_report_wait_response(
            report=get_roller_info,
            response_queue=self.hidDispatcher.mouse_message_queue,
            response_class_type=GetRollerInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetRollerInfo.RollerType value equal to the defined constant')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.VERTICAL_SCROLLING.F_RollerType,
                         obtained=int(Numeral(get_roller_info_response.rollerType)),
                         msg='The rollerType parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetRollerInfo.NumOfRatchetByTurn value equal to the defined constant')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.VERTICAL_SCROLLING.F_NumOfRatchetByTurn,
                         obtained=int(Numeral(get_roller_info_response.numOfRatchetByTurn)),
                         msg='The numOfRatchetByTurn parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate GetRollerInfo.ScrollLines value equal to the defined constant')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.VERTICAL_SCROLLING.F_ScrollLines,
                         obtained=int(Numeral(get_roller_info_response.scrollLines)),
                         msg='The scrollLines parameter differs from the one expected')

        self.testCaseChecked("FNT_2100_0001")
    # end def test_GetRollerInfo

    @features('Feature2100')
    @features('Feature0003v2')
    @level('Business', 'SmokeTests')
    def test_VerticalScrolling(self):
        """
        Validates VerticalScrolling GetRollerInfo Business case sequence
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send VerticalScrolling.GetRollerInfo')
        # ---------------------------------------------------------------------------
        get_roller_info = GetRollerInfo(deviceIndex=self.deviceIndex, featureId=self.feature_id)
        first_response = self.send_report_wait_response(report=get_roller_info,
                                                        response_queue=self.hidDispatcher.mouse_message_queue,
                                                        response_class_type=GetRollerInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate GetRollerInfo.RollerInfo data')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.VERTICAL_SCROLLING.F_RollerType,
                         obtained=int(Numeral(first_response.rollerType)),
                         msg='The rollerType parameter differs from the one expected')

        # ----------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send FirmwareInfo.GetFwInfo')
        # ----------------------------------------------------------------------------
        DeviceInformationTestUtils.HIDppHelper.get_fw_info(test_case=self, entity_index=0)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send VerticalScrolling.GetRollerInfo again')
        # ---------------------------------------------------------------------------
        second_response = self.send_report_wait_response(report=get_roller_info,
                                                         response_queue=self.hidDispatcher.mouse_message_queue,
                                                         response_class_type=GetRollerInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate GetRollerInfo.RollerInfo data are identical to the first call')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=first_response.rollerType,
                         obtained=second_response.rollerType,
                         msg='The rollerType parameter differs from the first response')
        self.assertEqual(expected=first_response.numOfRatchetByTurn,
                         obtained=second_response.numOfRatchetByTurn,
                         msg='The numOfRatchetByTurn parameter differs from the first response')
        self.assertEqual(expected=first_response.scrollLines,
                         obtained=second_response.scrollLines,
                         msg='The scrollLines parameter differs from the first response')

        self.testCaseChecked("FNT_2100_0002")
    # end def test_VerticalScrolling

    @features('Feature2100')
    @level('Functionality')
    def test_SoftwareId(self):
        """
        Validates GetRollerInfo softwareId validity range

        RollerInfo= [0]GetRollerInfo ()
        Request: 0x10.DeviceIndex.0x00.0x1n.0x00.0x00.0x00
          SwID n boundary values 0 to F
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetRollerInfo with softwareId in its validity range')
        # ---------------------------------------------------------------------------
        for software_id in compute_inf_values(VerticalScrolling.DEFAULT.SOFTWARE_ID):
            get_roller_info = GetRollerInfo(
                deviceIndex=self.deviceIndex,
                featureId=self.feature_id)
            get_roller_info.softwareId = software_id
            get_roller_info_response = self.send_report_wait_response(
                report=get_roller_info,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetRollerInfoResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2("""Test Check 1: Validate GetRollerInfo.softwareId matches 
                                                the one from the request""")
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=software_id,
                             obtained=get_roller_info_response.softwareId,
                             msg='The softwareId parameter differs from the one expected')
        # end for
        self.testCaseChecked("FNT_2100_0002")
    # end def test_SoftwareId

    @features('Feature2100')
    @level('ErrorHandling')
    def test_WrongFunctionIndex(self):
        """
        Validates GetRollerInfo robustness processing (Feature 0x2100)

        Function indexes valid range [0]
          Tests wrong indexes
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetRollerInfo with wrong function index value')
        # ---------------------------------------------------------------------------
        for function_index in compute_wrong_range([x for x in range(
                VerticalScrolling.MAX_FUNCTION_INDEX + 1)], max_value=0xF):
            wrong_vertical_scrolling_function = GetRollerInfo(
                deviceIndex=self.deviceIndex,
                featureId=self.feature_id)
            wrong_vertical_scrolling_function.functionIndex = int(function_index)
            wrong_vertical_scrolling_function_response = self.send_report_wait_response(
                report=wrong_vertical_scrolling_function,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check InvalidFunctionId (7) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=wrong_vertical_scrolling_function.featureIndex,
                             obtained=wrong_vertical_scrolling_function_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=wrong_vertical_scrolling_function_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
        self.testCaseChecked("ROT_2100_0001")

    # end def test_WrongIndex

    @features('Feature2100')
    @level('Robustness')
    def test_Padding(self):
        """
        Validates GetRollerInfo padding bytes are ignored

        Roller Info= [0]GetRollerInfo ()
        Request: 0x10.DeviceIndex.0x00.0x1F.0xPP.0xPP.0xPP
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send GetRollerInfo with several value for padding')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(GetRollerInfo.DEFAULT.PADDING,
                                                             GetRollerInfo.LEN.PADDING // 8))):
            get_roller_info = GetRollerInfo(
                deviceIndex=self.deviceIndex,
                featureId=self.feature_id)
            get_roller_info.padding = padding_byte
            get_roller_info_response = self.send_report_wait_response(
                report=get_roller_info,
                response_queue=self.hidDispatcher.mouse_message_queue,
                response_class_type=GetRollerInfoResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate GetRollerInfo response received')
            # ---------------------------------------------------------------------------
            f = self.getFeatures()
            self.assertEqual(expected=f.PRODUCT.FEATURES.MOUSE.VERTICAL_SCROLLING.F_RollerType,
                             obtained=int(Numeral(get_roller_info_response.rollerType)),
                             msg='The rollerType parameter differs from the one expected')
        # end for
        self.testCaseChecked("ROT_2250_0002")
    # end def test_Padding
# end class VerticalScrollingTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
