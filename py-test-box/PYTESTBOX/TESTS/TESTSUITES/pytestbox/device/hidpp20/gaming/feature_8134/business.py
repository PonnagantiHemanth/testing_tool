#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8134.business
:brief: HID++ 2.0 ``BrakeForce`` business test suite
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
from pytestbox.device.base.ads1231utils import Ads1231TestUtils
from pytestbox.device.base.brakeforceutils import BrakeForceTestUtils
from pytestbox.device.hidpp20.gaming.feature_8134.brakeforce import BrakeForceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrakeForceBusinessTestCase(BrakeForceTestCase):
    """
    Validate ``BrakeForce`` business test cases
    """

    @features("Feature8134")
    @level("Business")
    def test_set_max_load_point_verify(self):
        """
        Validate if value set by SetMaxLoadPoint is same as value read by GetMaxLoadPoint
        """
        self.post_requisite_reload_nvs = True
        maximum_load_point = HexList("7FFF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        BrakeForceTestUtils.HIDppHelper.set_max_load_point(self, maximum_load_point=maximum_load_point)

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

        self.testCaseChecked("BUS_8134_0001", _AUTHOR)
    # end def test_set_max_load_point_verify

    @features("Feature8134")
    @features("Feature9215")
    @level("Business")
    def test_get_info_business(self):
        """
       Validate if value set by WriteOtherNvsData is same as value read by GetInfo
       """
        self.post_requisite_reload_nvs = True

        # -------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Check value obtained from GetInfo is same as value set with WriteOtherNvsData")
        # -------------------------------------------------------------------------------------------------------------
        max_load_value = 55
        max_load_value = HexList(hex(max_load_value)[2:].ljust(30, '0'))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteOtherNvsData request")
        # --------------------------------------------------------------------------------------------------------------
        Ads1231TestUtils.HIDppHelper.write_other_nvs_data(self, data_field_id=0, data=max_load_value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadOtherNvsData request")
        # --------------------------------------------------------------------------------------------------------------
        read_other_nvs_data_response = Ads1231TestUtils.HIDppHelper. \
            read_other_nvs_data(self, data_field_id=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verifying data HIDppHelper.read from ReadOtherNvsData matches values "
                                  "set by WriteOtherNvsData")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=max_load_value,
                         obtained=read_other_nvs_data_response.data,
                         msg=f"The value of max load is not as expected")

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
            "maximum_kg_load": (checker.check_maximum_kg_load, max_load_value),
        })
        checker.check_fields(self, response, self.feature_8134.get_info_response_cls, check_map)

        self.testCaseChecked("BUS_8134_0002", _AUTHOR)
    # end def test_get_info_business
# end class BrakeForceBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
