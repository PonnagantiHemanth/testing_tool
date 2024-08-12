#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1b04.interface
:brief: HID++ 2.0 Special Keys MSE Buttons interface test suite
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/05/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_1b04.specialkeysmsebuttons import SpecialKeysMSEButtonsTestCase
from pytestbox.shared.base.specialkeysmsebuttonsutils import SpecialKeysMseButtonsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpecialKeysMSEButtonsInterfaceTestCase(SpecialKeysMSEButtonsTestCase):
    """
    Validate the keyboard reprogrammable keys and mouse buttons interfaces.
    """
    @features('Feature1B04')
    @level('Interface')
    def test_get_count_api(self):
        """
        Validate the GetCount request API (Feature 0x1B04).

        v0
            ctrlIDCount = [0]GetCount()
        v1 ~ v5
            [0] getCount() -> count
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getCount request')
        # --------------------------------------------------------------------------------------------------------------
        get_count = self.special_keys_and_mouse_buttons_feature.get_count_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_id)
        get_count_response = ChannelUtils.send(
            test_case=self,
            report=get_count,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.special_keys_and_mouse_buttons_feature.get_count_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate getCount response format and CID count')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=get_count.deviceIndex,
                         obtained=get_count_response.deviceIndex,
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=get_count.featureIndex,
                         obtained=get_count_response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')
        f = self.getFeatures()
        self.assertEqual(expected=HexList(f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidCount),
                         obtained=get_count_response.count,
                         msg='The count parameter differs from the one expected')

        self.testCaseChecked("INT_1B04_0001")
    # end def test_get_count_api

    @features('Feature1B04')
    @level('Interface')
    def test_get_cid_info_api(self):
        """
        Validate the GetCidInfo request API (Feature 0x1B04).

        v0
            ctrlID, taskID, flags, fkeyPos =  [1]GetCtrlIDInfo(ctrlIDIndex)
        v1
            [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask
        v2 ~ v5
            [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask, additionalflags
        """
        # Get the supported version
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetCidInfo request with index = 0')
        # --------------------------------------------------------------------------------------------------------------
        get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id, ctrl_id_index=0)
        get_cid_info_response = ChannelUtils.send(
            test_case=self,
            report=get_cid_info,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=get_cid_info_response_class)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetCidInfo response format')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=get_cid_info.deviceIndex,
                         obtained=get_cid_info_response.deviceIndex,
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=get_cid_info.featureIndex,
                         obtained=get_cid_info_response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')

        get_cid_info_expected_response_hex = HexList(get_cid_info_response)[:4] + HexList(
            self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)[0])
        get_cid_info_expected_response_hex.addPadding(size=HidppMessage.LONG_MSG_SIZE,
                                                      fromLeft=False)
        get_cid_info_expected_response = get_cid_info_response_class.fromHexList(get_cid_info_expected_response_hex)

        obtained_field_ids = [field.fid for field in get_cid_info_response.FIELDS]
        expected_field_ids = [field.fid for field in get_cid_info_expected_response.FIELDS]

        error_message = ""
        if obtained_field_ids == expected_field_ids:
            error_message += "This parameters differ from the one expected:\n"
            for fid in obtained_field_ids:
                if get_cid_info_response.getValue(fid) != get_cid_info_expected_response.getValue(fid):
                    error_message += "\t- " + get_cid_info_response.getFieldDefinition(fid).name + "\n"
        else:
            error_message += "Field IDs are not matching"
        # end if

        self.assertEqual(expected=get_cid_info_expected_response,
                         obtained=get_cid_info_response,
                         msg=error_message)

        self.testCaseChecked("INT_1B04_0002")
    # end def test_get_cid_info_api

    @features('Feature1B04')
    @level('Interface')
    def test_get_cid_reporting_api(self):
        """
        Validate the GetCidReporting request API (Feature 0x1B04).

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
        # Get the supported version
        get_cid_info_response_class = self.get_cid_info_response_class()
        get_cid_reporting_response_class = self.get_cid_reporting_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetCidInfo request with index = 0 to get first CID value')
        # --------------------------------------------------------------------------------------------------------------
        get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id, ctrl_id_index=0)
        get_cid_info_response = ChannelUtils.send(
            test_case=self,
            report=get_cid_info,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=get_cid_info_response_class)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send GetCidReporting request with CID = '
                                 f'{get_cid_info_response.ctrl_id}')
        # --------------------------------------------------------------------------------------------------------------
        get_cid_reporting = self.special_keys_and_mouse_buttons_feature.get_cid_reporting_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
            ctrl_id=get_cid_info_response.ctrl_id)
        get_cid_reporting_response = ChannelUtils.send(
            test_case=self,
            report=get_cid_reporting,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=get_cid_reporting_response_class)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetCidReporting response format')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=get_cid_reporting.deviceIndex,
                         obtained=get_cid_reporting_response.deviceIndex,
                         msg='The deviceIndex parameter differs from the one expected')
        self.assertEqual(expected=get_cid_reporting.featureIndex,
                         obtained=get_cid_reporting_response.featureIndex,
                         msg='The featureIndex parameter differs from the one expected')
        self.assertEqual(expected=get_cid_reporting.ctrl_id,
                         obtained=get_cid_reporting_response.ctrl_id,
                         msg='The ctrl_id parameter differs from the one expected')

        """
        The field Remap is only present from version 1 to 5.
        This field should either be 0 or one of the CID in the table of this device.
        """
        if not self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_0:
            self.assertTrue(expr=(get_cid_reporting_response.remap == HexList("0000")) or
                                 (str(get_cid_reporting_response.remap) in
                                  [x[:4] for x in self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)]),
                            msg='The remap parameter is out of range')
        # end if

        self.testCaseChecked("INT_1B04_0003")
    # end def test_get_cid_reporting_api

    @features('Feature1B04')
    @level('Interface')
    def test_set_cid_reporting_api(self):
        """
        Validate the SetCidReporting request API (Feature 0x1B04).

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
        v1 ~ v5
            [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
        """

        # Get the supported version
        get_cid_info_response_class = self.get_cid_info_response_class()
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetCidInfo request with index = 0 to get first CID value')
        # --------------------------------------------------------------------------------------------------------------
        get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id, ctrl_id_index=0)
        get_cid_info_response = ChannelUtils.send(
            test_case=self,
            report=get_cid_info,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=get_cid_info_response_class)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetCidReporting request with CID = '
                                 f'{get_cid_info_response.ctrl_id} and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                    feature_index=self.feature_id,
                                                    ctrl_id=get_cid_info_response.ctrl_id)
        set_cid_reporting_response = ChannelUtils.send(
            test_case=self,
            report=set_cid_reporting,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=set_cid_reporting_response_class)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetCidReporting response format')
        # --------------------------------------------------------------------------------------------------------------
        SpecialKeysMseButtonsTestUtils.check_response_expected_field(
            self, set_cid_reporting, set_cid_reporting_response)

        self.testCaseChecked("INT_1B04_0004")
    # end def test_set_cid_reporting_api

    @features('Feature1B04V6+')
    @level('Interface')
    def test_get_capabilities_api(self):
        """
        Validate the getCapabilities request API (Feature 0x1B04).

        v6
            [4] getCapabilities() -> flags
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getCapabilities request')
        # --------------------------------------------------------------------------------------------------------------
        report = self.special_keys_and_mouse_buttons_feature.get_capabilities_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_id)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.special_keys_and_mouse_buttons_feature.get_capabilities_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate getCapabilities response format and flag')
        # --------------------------------------------------------------------------------------------------------------
        checker = SpecialKeysMseButtonsTestUtils.GetCapabilitiesV6ResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.special_keys_and_mouse_buttons_feature.get_capabilities_response_cls,
                             check_map)

        self.testCaseChecked("INT_1B04_0005")
    # end def test_get_capabilities_api

    @features('Feature1B04V6+')
    @features('Feature1B04resetAllCidReportSettings')
    @level('Interface')
    def test_reset_all_cid_report_settings_api(self):
        """
        Validate the resetAllCidReportSettings request API (Feature 0x1B04).

        v6
            [5] resetAllCidReportSettings()
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
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.special_keys_and_mouse_buttons_feature.reset_all_cid_report_settings_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate resetAllCidReportSettings response format')
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response,
                             self.special_keys_and_mouse_buttons_feature.reset_all_cid_report_settings_response_cls,
                             check_map)

        self.testCaseChecked("INT_1B04_0006")
    # end def test_reset_all_cid_report_settings_api
# end class SpecialKeysMSEButtonsInterfaceTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
