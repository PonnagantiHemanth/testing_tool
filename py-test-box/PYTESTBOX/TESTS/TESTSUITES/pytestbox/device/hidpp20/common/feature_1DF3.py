#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
""" @package pytestbox.hid.common.feature_1DF3

@brief  Validates HID common feature 0x1DF3

@author Stanislas Cottard

@date   2019/07/31
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.equaddjdebuginfo import EquadDJDebugInfo
from pyhid.hidpp.features.common.equaddjdebuginfo import ReadEquadDJDebugInfo
from pyhid.hidpp.features.common.equaddjdebuginfo import ReadEquadDJDebugInfoResponse
from pyhid.hidpp.features.common.equaddjdebuginfo import WriteEquadDJDebugInfo
from pyhid.hidpp.features.common.equaddjdebuginfo import WriteEquadDJDebugInfoResponse
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.hidpp1.notifications.linkqualityinfo import LinkQualityInfoShort
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ApplicationEquadDJDebugInfoTestCase(BaseTestCase):
    """
    Validates EquadDJDebugInfo TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_disable_equad_debug = False

        super(ApplicationEquadDJDebugInfoTestCase, self).setUp()
        
        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x1DF3)')
        # ---------------------------------------------------------------------------
        self.feature_id = self.updateFeatureMapping(feature_id=EquadDJDebugInfo.FEATURE_ID)

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#2: Send Root.GetFeature(0x1E00)')
        # ---------------------------------------------------------------------------
        self.enable_hidden_feature_id = self.updateFeatureMapping(feature_id=EnableHidden.FEATURE_ID)
    # end def setUp

    # noinspection PyBroadException
    def tearDown(self):
        """
        Handles test post-requisites.
        """
        post_requisite_number = 1

        if self.post_requisite_disable_equad_debug:
            try:
                # ---------------------------------------------------------------------------
                self.logTitle2(f'Post-requisite#{post_requisite_number}: Disable EQuadDJDebugInfo if failed')
                # ---------------------------------------------------------------------------
                write_equad_d_j_debug_info = WriteEquadDJDebugInfo(
                    device_index=self.deviceIndex,
                    feature_id=self.feature_id,
                    equad_dj_debug_info_reg=EquadDJDebugInfo.REG_DEBUG_OFF)
                self.send_report_wait_response(report=write_equad_d_j_debug_info,
                                               response_queue=self.hidDispatcher.common_message_queue,
                                               response_class_type=WriteEquadDJDebugInfoResponse)

                # Empty receiver notification queue
                self.empty_queue(queue=self.hidDispatcher.receiver_event_queue)
            except:
                self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
            # end try

            self.post_requisite_disable_equad_debug = False
            post_requisite_number += 1
        # end if

        super(ApplicationEquadDJDebugInfoTestCase, self).tearDown()
    # end def tearDown

    @features('Feature1DF3')
    @level('Interface')
    def test_ReadEQuadDJDebugInfoAPI(self):
        """
        @tc_synopsis    Validates ReadEQuadDJDebugInfo API (Feature 0x1DF3)

        DebugMode = [0]ReadEQuadDJDebugInfo()
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Manufacturing features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send ReadEQuadDJDebugInfo')
        # ---------------------------------------------------------------------------
        read_equad_d_j_debug_info = ReadEquadDJDebugInfo(device_index=self.deviceIndex,
                                                         feature_id=self.feature_id)
        read_equad_d_j_debug_info_response = self.send_report_wait_response(
            report=read_equad_d_j_debug_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=ReadEquadDJDebugInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate the return value = 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=EquadDJDebugInfo.REG_DEBUG_OFF,
                         obtained=int(Numeral(read_equad_d_j_debug_info_response.equad_dj_debug_info_reg)),
                         msg='The EquadDJDebugInfoReg parameter differs from the one expected')
        
        self.testCaseChecked("FNT_1DF3_0001")
    # end def test_ReadEQuadDJDebugInfoAPI

    @features('Feature1DF3')
    @level('Interface')
    def test_WriteEQuadDJDebugInfoAPI(self):
        """
        @tc_synopsis    Validates WriteEQuadDJDebugInfo API (Feature 0x1DF3)

        DebugMode = [1]WriteEQuadDJDebugInfo(DebugMode)
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Manufacturing features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send WriteEQuadDJDebugInfo with DebugMode = 0')
        # ---------------------------------------------------------------------------
        write_equad_d_j_debug_info = WriteEquadDJDebugInfo(device_index=self.deviceIndex,
                                                           feature_id=self.feature_id,
                                                           equad_dj_debug_info_reg=EquadDJDebugInfo.REG_DEBUG_OFF)
        write_equad_d_j_debug_info_response = self.send_report_wait_response(
            report=write_equad_d_j_debug_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=WriteEquadDJDebugInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate the return value of DebugMode = 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=EquadDJDebugInfo.REG_DEBUG_OFF,
                         obtained=int(Numeral(write_equad_d_j_debug_info_response.equad_dj_debug_info_reg)),
                         msg='The EquadDJDebugInfoReg parameter differs from the one expected')

        self.testCaseChecked("FNT_1DF3_0002")
    # end def test_WriteEQuadDJDebugInfoAPI

    @features('Feature1DF3')
    @level('Business')
    @bugtracker('1df3_on_corded_devices')
    def test_WriteEQuadDJDebugInfoBusiness(self):
        """
        @tc_synopsis    Validates WriteEQuadDJDebugInfo business case, set DebugMode = 1 to receive eQuad debug message

        Link Quality information
        Short report: 10 ix 49 r0 r1 r2 r3
        Long report:  11 ix 49 r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 ra rb rc rd re rf 00
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Manufacturing features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send WriteEQuadDJDebugInfo with DebugMode = 1')
        # ---------------------------------------------------------------------------
        self.post_requisite_disable_equad_debug = True
        write_equad_d_j_debug_info = WriteEquadDJDebugInfo(device_index=self.deviceIndex,
                                                           feature_id=self.feature_id,
                                                           equad_dj_debug_info_reg=EquadDJDebugInfo.REG_DEBUG_ON)
        write_equad_d_j_debug_info_response = self.send_report_wait_response(
            report=write_equad_d_j_debug_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=WriteEquadDJDebugInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate the return value of DebugMode = 1')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=EquadDJDebugInfo.REG_DEBUG_ON,
                         obtained=int(Numeral(write_equad_d_j_debug_info_response.equad_dj_debug_info_reg)),
                         msg='The EquadDJDebugInfoReg parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Should receive link quality notification by short report')
        # ---------------------------------------------------------------------------
        self.getMessage(queue=self.hidDispatcher.receiver_event_queue, class_type=LinkQualityInfoShort)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Send WriteEQuadDJDebugInfo with DebugMode = 0')
        # ---------------------------------------------------------------------------
        write_equad_d_j_debug_info = WriteEquadDJDebugInfo(device_index=self.deviceIndex,
                                                           feature_id=self.feature_id,
                                                           equad_dj_debug_info_reg=EquadDJDebugInfo.REG_DEBUG_OFF)
        write_equad_d_j_debug_info_response = self.send_report_wait_response(
            report=write_equad_d_j_debug_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=WriteEquadDJDebugInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Validate the return value of DebugMode = 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=EquadDJDebugInfo.REG_DEBUG_OFF,
                         obtained=int(Numeral(write_equad_d_j_debug_info_response.equad_dj_debug_info_reg)),
                         msg='The EquadDJDebugInfoReg parameter differs from the one expected')

        self.post_requisite_disable_equad_debug = False

        # Empty receiver notification queue
        self.empty_queue(queue=self.hidDispatcher.receiver_event_queue)

        self.testCaseChecked("FNT_1DF3_0003")
    # end def test_WriteEQuadDJDebugInfoBusiness

    @features('Feature1DF3')
    @level('Functionality')
    @services('PowerSupply')
    def test_DebugModeReturnToDefaultAfterReset(self):
        """
        @tc_synopsis    validate DebugMode value should return to default after restart DUT

        DebugMode = [1]WriteEQuadDJDebugInfo(DebugMode)
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Manufacturing features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send WriteEQuadDJDebugInfo with DebugMode = 1')
        # ---------------------------------------------------------------------------
        self.post_requisite_disable_equad_debug = True
        write_equad_d_j_debug_info = WriteEquadDJDebugInfo(device_index=self.deviceIndex,
                                                           feature_id=self.feature_id,
                                                           equad_dj_debug_info_reg=EquadDJDebugInfo.REG_DEBUG_ON)
        write_equad_d_j_debug_info_response = self.send_report_wait_response(
            report=write_equad_d_j_debug_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=WriteEquadDJDebugInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate the return value of DebugMode = 1')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=EquadDJDebugInfo.REG_DEBUG_ON,
                         obtained=int(Numeral(write_equad_d_j_debug_info_response.equad_dj_debug_info_reg)),
                         msg='The EquadDJDebugInfoReg parameter differs from the one expected')

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Power off DUT')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Power on DUT')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Enable Manufacturing features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 6: Send ReadEQuadDJDebugInfo')
        # ---------------------------------------------------------------------------
        read_equad_d_j_debug_info = ReadEquadDJDebugInfo(device_index=self.deviceIndex,
                                                         feature_id=self.feature_id)
        read_equad_d_j_debug_info_response = self.send_report_wait_response(
            report=read_equad_d_j_debug_info,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=ReadEquadDJDebugInfoResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Validate the return value = 0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=EquadDJDebugInfo.REG_DEBUG_OFF,
                         obtained=int(Numeral(read_equad_d_j_debug_info_response.equad_dj_debug_info_reg)),
                         msg='The EquadDJDebugInfoReg parameter differs from the one expected')

        self.post_requisite_disable_equad_debug = False

        # Empty receiver notification queue
        self.empty_queue(queue=self.hidDispatcher.receiver_event_queue)

        self.testCaseChecked("FNT_1DF3_0004")
    # end def test_DebugModeReturnToDefaultAfterReset

    @features('Feature1DF3')
    @level('ErrorHandling')
    def test_ReadEQuadDJDebugInfoHiddenFeaturesDisabled(self):
        """
        @tc_synopsis    Send ReadEQuadDJDebugInfo w/o enable hidden features

        DebugMode = [0]ReadEQuadDJDebugInfo()
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Disable hidden features')
        # ------------------------------------------------------------------------
        set_enable_features = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(self),
                                                      feature_index=self.enable_hidden_feature_id,
                                                      enable_byte=EnableHidden.DISABLED)
        self.send_report_wait_response(report=set_enable_features,
                                       response_queue=self.hidDispatcher.common_message_queue,
                                       response_class_type=SetEnableHiddenFeaturesResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send ReadEQuadDJDebugInfo')
        # ---------------------------------------------------------------------------
        read_equad_d_j_debug_info = ReadEquadDJDebugInfo(device_index=self.deviceIndex,
                                                         feature_id=self.feature_id)
        read_equad_d_j_debug_info_response = self.send_report_wait_response(
            report=read_equad_d_j_debug_info,
            response_queue=self.hidDispatcher.error_message_queue,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Error Codes NotAllowed (5) returned by the device')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=int(Numeral(read_equad_d_j_debug_info_response.errorCode)),
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("ROT_1DF3_0001")
    # end def test_ReadEQuadDJDebugInfoHiddenFeaturesDisabled

    @features('Feature1DF3')
    @level('ErrorHandling')
    def test_WriteEQuadDJDebugInfoDebugModeInvalidRange(self):
        """
        @tc_synopsis    Send WriteEQuadDJDebugInfo w/ invalid Inputs.DebugMode value

        Generate invalid Inputs.DebugMode value by compute_wrong_range()
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Manufacturing features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over DebugMode invalid range (several interesting values)')
        # ---------------------------------------------------------------------------
        for invalid_debug_mode in compute_wrong_range([0, 1], min_value=2, max_value=0xFF):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send WriteEQuadDJDebugInfo with DebugMode = 0x%X' % invalid_debug_mode)
            # ---------------------------------------------------------------------------
            write_equad_d_j_debug_info = WriteEquadDJDebugInfo(device_index=self.deviceIndex,
                                                               feature_id=self.feature_id,
                                                               equad_dj_debug_info_reg=invalid_debug_mode)
            write_equad_d_j_debug_info_response = self.send_report_wait_response(
                report=write_equad_d_j_debug_info,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check Error Codes InvalidArgument (2) returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_ARGUMENT,
                             obtained=int(Numeral(write_equad_d_j_debug_info_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_1DF3_0002")
    # end def test_WriteEQuadDJDebugInfoDebugModeInvalidRange

    @features('Feature1DF3')
    @level('ErrorHandling')
    def test_ReadEQuadDJDebugInfoFunctionIndexInvalidRange(self):
        """
        @tc_synopsis    Validates eQuadDJDebugInfo robustness processing

        Function indexes valid range [0..1]
        Tests wrong indexes by compute_wrong_range()
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Manufacturing features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over functionIndex invalid range (several interesting values)')
        # ---------------------------------------------------------------------------
        for invalid_function_index in compute_wrong_range(list(range(EquadDJDebugInfo.MAX_FUNCTION_INDEX)),
                                                          min_value=EquadDJDebugInfo.MAX_FUNCTION_INDEX + 1,
                                                          max_value=0xF):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send ReadEQuadDJDebugInfo')
            # ---------------------------------------------------------------------------
            read_equad_d_j_debug_info = ReadEquadDJDebugInfo(device_index=self.deviceIndex,
                                                             feature_id=self.feature_id)
            read_equad_d_j_debug_info.functionIndex = invalid_function_index
            read_equad_d_j_debug_info_response = self.send_report_wait_response(
                report=read_equad_d_j_debug_info,
                response_queue=self.hidDispatcher.error_message_queue,
                response_class_type=ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check Error Codes InvalidFunctionId (7)  returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=int(Numeral(read_equad_d_j_debug_info_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_1DF3_0003")
    # end def test_ReadEQuadDJDebugInfoFunctionIndexInvalidRange

    @features('Feature1DF3')
    @level('Robustness')
    def test_ReadEQuadDJDebugInfoPadding(self):
        """
        @tc_synopsis    Validates eQuadDJDebugInfo padding bytes are ignored

        DebugMode = [0]ReadEQuadDJDebugInfo()
        Request: 0x10.DeviceIndex.FeatureIndex.0x0F.0xPP.0xPP.0xPP
        Generate several kinds of padding bytes by compute_sup_values()
        """

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Manufacturing features')
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over padding (several interesting values)')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(ReadEquadDJDebugInfo.DEFAULT.PADDING,
                                                             ReadEquadDJDebugInfo.LEN.PADDING // 8))):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send ReadEQuadDJDebugInfo with padding = ' + str(padding_byte))
            # ---------------------------------------------------------------------------
            read_equad_d_j_debug_info = ReadEquadDJDebugInfo(device_index=self.deviceIndex,
                                                             feature_id=self.feature_id)
            read_equad_d_j_debug_info.padding = padding_byte
            read_equad_d_j_debug_info_response = self.send_report_wait_response(
                report=read_equad_d_j_debug_info,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=ReadEquadDJDebugInfoResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Validate the return value = 0')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=EquadDJDebugInfo.REG_DEBUG_OFF,
                             obtained=int(Numeral(read_equad_d_j_debug_info_response.equad_dj_debug_info_reg)),
                             msg='The EquadDJDebugInfoReg parameter differs from the one expected')
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROT_1E00_0004")
    # end def test_ReadEQuadDJDebugInfoPadding
# end class ApplicationEquadDJDebugInfoTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
