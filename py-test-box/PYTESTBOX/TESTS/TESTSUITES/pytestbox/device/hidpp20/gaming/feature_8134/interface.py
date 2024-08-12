#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8134.interface
:brief: HID++ 2.0 ``BrakeForce`` interface test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brakeforceutils import BrakeForceTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.gaming.feature_8134.brakeforce import BrakeForceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrakeForceInterfaceTestCase(BrakeForceTestCase):
    """
    Validate ``BrakeForce`` interface test cases
    """

    @features("Feature8134")
    @level("Interface")
    def test_get_info_interface(self):
        """
        Validate ``GetInfo`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetInfo request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8134.get_info_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_8134_index)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.gaming_message_queue,
            response_class_type=self.feature_8134.get_info_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrakeForceTestUtils.GetInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_8134.get_info_response_cls, check_map)

        self.testCaseChecked("INT_8134_0001", _AUTHOR)
    # end def test_get_info_interface

    @features("Feature8134")
    @level("Interface")
    def test_get_max_load_point_interface(self):
        """
        Validate ``GetMaxLoadPoint`` interface
        """
        self.post_requisite_reload_nvs = True
        maximum_load_point = HexList("FFFF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8134.set_max_load_point_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_8134_index,
            maximum_load_point=maximum_load_point)
        self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.gaming_message_queue,
            response_class_type=self.feature_8134.set_max_load_point_response_cls)
        # Add delay to wait for previous commands to process and prevent them from generating events after clearing
        # queue
        sleep(.5)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clearing any existing Event messages of MaxLoad Point Changed type")
        # ----------------------------------------------------------------------------------------------------------
        self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                         class_type=self.feature_8134.max_load_point_changed_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8134.get_max_load_point_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_8134_index)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.gaming_message_queue,
            response_class_type=self.feature_8134.get_max_load_point_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetMaxLoadPointResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrakeForceTestUtils.GetMaxLoadPointResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "maximum_load_point": (checker.check_maximum_load_point, maximum_load_point),
        })
        checker.check_fields(self, response, self.feature_8134.get_max_load_point_response_cls, check_map)

        self.testCaseChecked("INT_8134_0002", _AUTHOR)
    # end def test_get_max_load_point_interface

    @features("Feature8134")
    @level("Interface")
    def test_set_max_load_point_interface(self):
        """
        Validate ``SetMaxLoadPoint`` interface
        """
        self.post_requisite_reload_nvs = True
        maximum_load_point = HexList("3FFF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8134.set_max_load_point_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_8134_index,
            maximum_load_point=maximum_load_point)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.gaming_message_queue,
            response_class_type=self.feature_8134.set_max_load_point_response_cls)
        # Add delay to wait for previous commands to process and prevent them from generating events after clearing
        # queue
        sleep(.5)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clearing any existing Event messages of MaxLoad Point Changed type")
        # ----------------------------------------------------------------------------------------------------------
        self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                         class_type=self.feature_8134.max_load_point_changed_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMaxLoadPointResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_8134.set_max_load_point_response_cls, check_map)

        self.testCaseChecked("INT_8134_0003", _AUTHOR)
    # end def test_set_max_load_point_interface
# end class BrakeForceInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
