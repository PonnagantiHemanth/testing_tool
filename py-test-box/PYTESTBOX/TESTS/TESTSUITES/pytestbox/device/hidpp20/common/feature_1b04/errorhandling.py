#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1b04.errorhandling
:brief: HID++ 2.0 Special Keys MSE Buttons error handling test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.specialkeysmsebuttons import CidInfoPayload
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfo
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReporting
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetestutils import CommonBaseTestUtils as BaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.cidutils import CidInfoFlags
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1b04.specialkeysmsebuttons import SpecialKeysMSEButtonsTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpecialKeysMSEButtonsErrorHandlingTestCase(SpecialKeysMSEButtonsTestCase):
    """
    Validate the Keyboard reprogrammable Keys and Mouse buttons ErrorHandling TestCases.
    """
    @features('Feature1B04')
    @level('ErrorHandling')
    def test_get_cid_info_error_range(self):
        """
        Validate the getCidInfo with invalid range getCount()..0xFF.

        v0
            ctrlID, taskID, flags, fkeyPos =  [1]GetCtrlIDInfo(ctrlIDIndex)
        v1
            [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask
        v2 ~ v5
            [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask, additionalflags
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in invalid range (typical wrong values)')
        # --------------------------------------------------------------------------------------------------------------
        for invalid_index in compute_wrong_range(
                value=[x for x in range(self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidCount)],
                max_value=0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo request with index = {invalid_index}')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = GetCidInfo(device_index=ChannelUtils.get_device_index(test_case=self),
                                      feature_index=self.feature_id,
                                      ctrl_id_index=invalid_index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=get_cid_info_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0001")
    # end def test_GetCidInfoErrorRange

    @features('Feature1B04')
    @level('ErrorHandling')
    def test_get_cid_reporting_error_range(self):
        """
        Validate the getCidReporting with invalid Cid.

        Select several invalid CIDs in range 0x00FE..0xFFFF by compute_wrong_range.

        v0
            ctrlID, controlIDReporting = [2]GetCtrlIDReporting(ctrlID)
        v1
            [2] getCidReporting(cid) -> cid, divert, persist, remap
        v2
            [2] getCidReporting(cid) -> cid, divert, persist, rawXY, remap
        v3
            [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap
        v4
            [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap, analyticsKeyEvt
        v5
            [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap, analyticsKeyEvt, rawWheel
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in invalid range (typical wrong values)')
        # --------------------------------------------------------------------------------------------------------------
        for invalid_cid in compute_wrong_range(value=[x for x in range(0xFE)], max_value=0xFFFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidReprting request with CID = {invalid_cid} and set '
                                     f'other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_reporting = GetCidReporting(device_index=ChannelUtils.get_device_index(test_case=self),
                                                feature_index=self.feature_id,
                                                ctrl_id=invalid_cid)
            get_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=get_cid_reporting_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0002")
    # end def test_GetCidReportingErrorRange

    @features('Feature1B04')
    @level('ErrorHandling')
    def test_set_cid_reporting_error_range(self):
        """
        Validate the setCidReporting with CID not supported by the DUT.

        Select some CIDs that are not supported by the DUT.
        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.

        v0
            ctrlID, controlIDReporting =  [3]SetCtrlIDReporting(ctrlID, controlIDReporting)
            ctrlIDIndexPressedList   =  [0]ControlIDBroadcastEvent()
        v1
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, remap
        v2
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap
        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        """
        # Get the supported version
        (set_cid_reporting_class, _) = self.set_cid_reporting_classes()
        cid_list = self.config_manager.get_feature(self.config_manager.ID.CID_INFO_TABLE_CID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in not supported range (typical wrong values)')
        # --------------------------------------------------------------------------------------------------------------
        for invalid_cid in compute_wrong_range(value=cid_list, max_value=(int(max(CidTable)) + 1)):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send setCidReporting request with CID = {invalid_cid} and set other '
                           f'parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=invalid_cid)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=set_cid_reporting_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0003")
    # end def test_SetCidReportingErrorRange

    @features('Feature1B04')
    @features('Feature1B04WithoutFlags', CidInfoFlags.DIVERT_FLAG)
    @level('ErrorHandling')
    def test_set_cid_reporting_divert_error(self):
        """
        Validate the setCidReporting.divert=1 on CIDs which doesn't have divert capability.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.

        v0
            ctrlID, controlIDReporting =  [3]SetCtrlIDReporting(ctrlID, controlIDReporting)
            ctrlIDIndexPressedList   =  [0]ControlIDBroadcastEvent()
        v1
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, remap
        v2
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap
        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        """
        # Get the supported version
        (set_cid_reporting_class, _) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_list_no_d = [HexList(cid_info[:4]) for cid_info in
                         self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                         if (int(cid_info[8:10]+'00', 16) & CidInfoFlags.DIVERT_FLAG) == 0 and
                         (int(cid_info[8:10]+'00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with no divert capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_no_d in cid_list_no_d:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReprting request with CID = {cid_no_d} and set divert'
                                     f' = 1, dvalid = 1 and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            """
            The parameters used are common to every constructor's version.
            The other parameters default value in each constructors is 0.
            """
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_no_d,
                                                        divert_valid=True,
                                                        divert=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=set_cid_reporting_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0004")
    # end def test_SetCidReportingDivertError

    @features('Feature1B04')
    @features('Feature1B04WithoutFlags', CidInfoFlags.PERSIST_FLAG)
    @level('ErrorHandling')
    def test_set_cid_reporting_persist_error(self):
        """
        Validate the setCidReporting.persist on CIDs which doesn't have persist capability.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.

        v0
            ctrlID, controlIDReporting =  [3]SetCtrlIDReporting(ctrlID, controlIDReporting)
            ctrlIDIndexPressedList   =  [0]ControlIDBroadcastEvent()
        v1
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, remap
        v2
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap
        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        """
        # Get the supported version
        (set_cid_reporting_class, _) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_list_no_p = [HexList(cid_info[:4]) for cid_info in
                         self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                         if (int(cid_info[8:10]+'00', 16) & CidInfoFlags.PERSIST_FLAG) == 0 and
                         (int(cid_info[8:10]+'00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with no persist capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_no_p in cid_list_no_p:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReprting request with CID = {cid_no_p} and set '
                                     f'persist = 1, pvalid = 1 and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_no_p,
                                                        persist_valid=True,
                                                        persist=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=set_cid_reporting_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0005")
    # end def test_SetCidReportingPersistError

    @features('Feature1B04V2+')
    @features('Feature1B04WithoutFlags', CidInfoFlags.RAW_XY_FLAG)
    @level('ErrorHandling')
    def test_set_cid_reporting_raw_xy_error(self):
        """
        Validate the setCidReporting.rawXY on CIDs which doesn't have rawXY capability.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.

        v2
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap
        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        """
        # Get the supported version
        (set_cid_reporting_class, _) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_list_no_r = [HexList(cid_info[:4]) for cid_info in
                         self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                         if (int(cid_info[16:18], 16) & CidInfoFlags.RAW_XY_FLAG) == 0 and
                         (int(cid_info[8:10]+'00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with no rawXY capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_no_r in cid_list_no_r:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReprting request with CID = {cid_no_r} and set rawXY '
                                     f'= 1, rvalid = 1 and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_no_r,
                                                        raw_xy_valid=True,
                                                        raw_xy=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=set_cid_reporting_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0006")
    # end def test_SetCidReportingRawXyError

    @features('Feature1B04V3+')
    @features('Feature1B04WithoutFlags', CidInfoFlags.FORCE_RAW_XY_FLAG)
    @level('ErrorHandling')
    def test_set_cid_reporting_force_raw_xy_error(self):
        """
        Validate the setCidReporting.forceRawXY on CIDs which doesn't have forceRawXY capability.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.

        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        """
        # Get the supported version
        (set_cid_reporting_class, _) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_list_no_f = [HexList(cid_info[:4]) for cid_info in
                         self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                         if (int(cid_info[16:18], 16) & CidInfoFlags.FORCE_RAW_XY_FLAG) == 0 and
                         (int(cid_info[8:10]+'00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with no forceRawXY '
                                 'capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_no_f in cid_list_no_f:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReprting request with CID = {cid_no_f} and set '
                                     f'forceRawXY = 1, fvalid = 1 and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_no_f,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=set_cid_reporting_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0007")
    # end def test_SetCidReportingForceRawXyError

    @features('Feature1B04V4+')
    @features('Feature1B04WithoutFlags', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG)
    @level('ErrorHandling')
    def test_set_cid_reporting_analytics_key_events_error(self):
        """
        Validate the setCidReporting.analyticsKeyEvt on CIDs which doesn't have analyticsKeyEvt capability.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.

        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        """
        # Get the supported version
        (set_cid_reporting_class, _) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        if self.f.PRODUCT.F_IsPlatform:
            cid_list_no_a = [HexList(cid_info[:4]) for cid_info in self.config_manager.get_feature(
                self.config_manager.ID.CID_TABLE) if (
                    CidInfoPayload.fromHexList(HexList(cid_info)).additional_flags.analytics_key_events == 0 and
                    CidInfoPayload.fromHexList(HexList(cid_info)).flags.virtual == 0 and
                    CidInfoPayload.fromHexList(HexList(cid_info)).flags.mouse == 1)]
        else:
            cid_list_no_a = [HexList(cid_info[:4]) for cid_info in self.config_manager.get_feature(
                self.config_manager.ID.CID_TABLE) if (
                    CidInfoPayload.fromHexList(HexList(cid_info)).additional_flags.analytics_key_events == 0 and
                    CidInfoPayload.fromHexList(HexList(cid_info)).flags.virtual == 0)]
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with no analyticsKeyEvt '
                                 'capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_no_a in cid_list_no_a:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReprting request with CID = {cid_no_a} and set '
                                     f'analyticsKeyEvt = 1, avalid = 1 and other parameters to 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_no_a,
                                                        analytics_key_event_valid=True,
                                                        analytics_key_event=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidArgument (0x02) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(ErrorCodes.INVALID_ARGUMENT),
                             obtained=set_cid_reporting_response.errorCode,
                             msg='The errorCode parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0008")
    # end def test_SetCidReportingAnalyticsKeyEventsError

    @features('Feature1B04')
    @level('ErrorHandling')
    def test_wrong_function_index(self):
        """
        Validate the 0x1B04 robustness processing.

        Tests function index error range [4..0xF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over function index in invalid range (typical wrong values)')
        # --------------------------------------------------------------------------------------------------------------
        for invalid_function_index in compute_wrong_range(
                [x for x in range(self.special_keys_and_mouse_buttons_feature.get_max_function_index() + 1)],
                max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with a wrong function index = '
                                     f'{invalid_function_index}')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = GetCidInfo(device_index=ChannelUtils.get_device_index(test_case=self),
                                      feature_index=self.feature_id,
                                      ctrl_id_index=0)
            get_cid_info.functionIndex = int(invalid_function_index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidFunctionId (0x07) returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_cid_info.featureIndex,
                             obtained=get_cid_info_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_cid_info_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1B04_0009")
    # end def test_WrongFunctionIndex

    @features('Feature1B04V6+')
    @features('NoFeature1B04resetAllCidReportSettings')
    @level('ErrorHandling')
    def test_reset_all_cid_report_settings_not_supported_error(self):
        """
        resetAllCidReportSettings will return error if resetAllCidReportSettings bit is not supported on the DUT
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send resetAllCidReportSettings request')
        # --------------------------------------------------------------------------------------------------------------
        report = self.special_keys_and_mouse_buttons_feature.reset_all_cid_report_settings_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_id)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the 3rd bytes = 0xFF and the 5th bytes HIDPP 2.0 error code = '
                                  'NOT_ALLOWED(5) of resetAllCidReportSettings response')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=Hidpp2ErrorCodes.ERROR_TAG,
                         obtained=to_int(response.errorTag),
                         msg='The received error tag do not match the expected one !')
        BaseTestUtils.HIDppHelper.check_hidpp20_error_message(
            test_case=self,
            error_message=response,
            feature_index=report.featureIndex,
            function_index=report.functionIndex,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1B04_0010")
    # end def test_reset_all_cid_report_settings_not_supported_error
# end class SpecialKeysMSEButtonsErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# -----------------------------------------------------------------------------------------------------------------------
