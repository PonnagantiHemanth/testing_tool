#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8134.robustness
:brief: HID++ 2.0 ``BrakeForce`` robustness test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.brakeforce import BrakeForce
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brakeforceutils import BrakeForceTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.gaming.feature_8134.brakeforce import BrakeForceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrakeForceRobustnessTestCase(BrakeForceTestCase):
    """
    Validate ``BrakeForce`` robustness test cases
    """

    @features("Feature8134")
    @level("Robustness")
    def test_get_info_software_id(self):
        """
        Validate ``GetInfo`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(BrakeForce.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8134.get_info_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8134_index)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_8134.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrakeForceTestUtils.GetInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                })
            checker.check_fields(self, response, self.feature_8134.get_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8134_0001", _AUTHOR)
    # end def test_get_info_software_id

    @features("Feature8134")
    @level("Robustness")
    def test_get_max_load_point_software_id(self):
        """
        Validate ``GetMaxLoadPoint`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        maximum_load_point = HexList("3FFF")

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # ----------------------------------------------------------------------------------------------------------
        report = self.feature_8134.set_max_load_point_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_8134_index,
            maximum_load_point=maximum_load_point)
        self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.gaming_message_queue,
            response_class_type=self.feature_8134.set_max_load_point_response_cls)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(BrakeForce.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetMaxLoadPoint request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8134.get_max_load_point_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8134_index)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_8134.get_max_load_point_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetMaxLoadPointResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrakeForceTestUtils.GetMaxLoadPointResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                "maximum_load_point": (checker.check_maximum_load_point, maximum_load_point),
            })
            checker.check_fields(self, response, self.feature_8134.get_max_load_point_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8134_0002", _AUTHOR)
    # end def test_get_max_load_point_software_id

    @features("Feature8134")
    @level("Robustness")
    def test_set_max_load_point_software_id(self):
        """
        Validate ``SetMaxLoadPoint`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.MaximumLoadPoint.0xPP

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        maximum_load_point = HexList("3FFF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(BrakeForce.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMaxLoadPoint request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8134.set_max_load_point_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8134_index,
                maximum_load_point=maximum_load_point)
            report.softwareId = software_id
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_8134.set_max_load_point_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Clearing any existing Event messages of MaxLoad Point Changed type")
            # ----------------------------------------------------------------------------------------------------------
            self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                             class_type=self.feature_8134.max_load_point_changed_event_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetMaxLoadPointResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            }
            checker.check_fields(self, response, self.feature_8134.set_max_load_point_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8134_0003", _AUTHOR)
    # end def test_set_max_load_point_software_id

    @features("Feature8134")
    @level("Robustness")
    def test_get_info_padding(self):
        """
        Validate ``GetInfo`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8134.get_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8134_index)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_8134.get_info_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrakeForceTestUtils.GetInfoResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                })
            checker.check_fields(self, response, self.feature_8134.get_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8134_0004", _AUTHOR)
    # end def test_get_info_padding

    @features("Feature8134")
    @level("Robustness")
    def test_get_max_load_point_padding(self):
        """
        Validate ``GetMaxLoadPoint`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        load_point_value_quarter = HexList("3FFF")
        maximum_load_point = load_point_value_quarter

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        BrakeForceTestUtils.HIDppHelper.set_max_load_point(self, maximum_load_point=load_point_value_quarter)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8134.get_max_load_point_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetMaxLoadPoint request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8134_index)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_8134.get_max_load_point_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetMaxLoadPointResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = BrakeForceTestUtils.GetMaxLoadPointResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
                "maximum_load_point": (checker.check_maximum_load_point, maximum_load_point),
            })
            checker.check_fields(self, response, self.feature_8134.get_max_load_point_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8134_0005", _AUTHOR)
    # end def test_get_max_load_point_padding

    @features("Feature8134")
    @level("Robustness")
    def test_set_max_load_point_padding(self):
        """
        Validate ``SetMaxLoadPoint`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.MaximumLoadPoint.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True
        load_point_value_half = HexList("7FFF")
        maximum_load_point = load_point_value_half

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8134.set_max_load_point_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMaxLoadPoint request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8134_index,
                maximum_load_point=maximum_load_point)
            report.padding = padding
            response = self.send_report_wait_response(
                report=report,
                response_queue=self.hidDispatcher.gaming_message_queue,
                response_class_type=self.feature_8134.set_max_load_point_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Clearing any existing Event messages of MaxLoad Point Changed type")
            # ----------------------------------------------------------------------------------------------------------
            self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                             class_type=self.feature_8134.max_load_point_changed_event_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetMaxLoadPointResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = DeviceTestUtils.MessageChecker
            check_map = {
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            }
            checker.check_fields(self, response, self.feature_8134.set_max_load_point_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8134_0006", _AUTHOR)
    # end def test_set_max_load_point_padding
# end class BrakeForceRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
