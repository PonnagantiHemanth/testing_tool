#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8134.functionality
:brief: HID++ 2.0 ``BrakeForce`` functionality test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pytransport.transportcontext import TransportContextException

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import choices
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.ads1231utils import Ads1231TestUtils
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
class BrakeForceFunctionalityTestCase(BrakeForceTestCase):
    """
    Validate ``BrakeForce`` functionality test cases
    """

    @features("Feature8134")
    @level("Functionality")
    def test_set_max_load_point_verify(self):
        """
        Validate if value set by ``SetMaxLoadPoint`` is same as value read by ``GetMaxLoadPoint``
        """
        self.post_requisite_reload_nvs = True
        valid_range = range(pow(2, 16))
        test_list = choices(valid_range, elem_nb=15)
        test_list.insert(0, 0)
        test_list.insert(-1, 0xFFFF)
        for load_point in test_list:
            load_point = HexList(hex(load_point)[2:].zfill(4))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetMaxLoadPoint request")
            # ----------------------------------------------------------------------------------------------------------
            BrakeForceTestUtils.HIDppHelper.set_max_load_point(self, maximum_load_point=load_point)

            # Add delay to wait for previous commands to process and prevent them from generating events after clearing
            # queue
            sleep(.5)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Clearing any existing Event messages of MaxLoad Point Changed type")
            # ----------------------------------------------------------------------------------------------------------
            self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                             class_type=self.feature_8134.max_load_point_changed_event_cls)

            # --------------------------------------------------------------------------------------------
            LogHelper.log_check(self,
                                "Check value obtained from GetMaxLoadPoint is same as value set with SetMaxLoadPoint")
            # --------------------------------------------------------------------------------------------
            report = self.feature_8134.get_max_load_point_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8134_index)
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
                "maximum_load_point": (checker.check_maximum_load_point, load_point),
            })
            checker.check_fields(self, response, self.feature_8134.get_max_load_point_response_cls, check_map)
        # end for
        self.testCaseChecked("FUN_8134_0001", _AUTHOR)
    # end def test_set_max_load_point_verify

    @features("Feature8134")
    @level("Functionality")
    def test_max_load_point_changed_verify(self):
        """
        Validate ``MaxLoadPointChanged`` Event is generated if there is a change in load point value
        """
        self.post_requisite_reload_nvs = True
        load_point_value_max = HexList("FFFF")
        load_point_value_quarter = HexList("3FFF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        BrakeForceTestUtils.HIDppHelper.set_max_load_point(self, maximum_load_point=load_point_value_max)
        # Add delay to wait for previous commands to process and prevent them from generating events after clearing
        # queue
        sleep(.5)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clearing any existing Event messages of MaxLoad Point Changed type")
        # ----------------------------------------------------------------------------------------------------------
        self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                         class_type=self.feature_8134.max_load_point_changed_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        BrakeForceTestUtils.HIDppHelper.set_max_load_point(self, maximum_load_point=load_point_value_quarter)

        # ---------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, "Changing load point value should generate event MaxLoadPointChanged with the correct value")
        # ---------------------------------------------------------------------------------------------------------
        max_load_point_changed = BrakeForceTestUtils.HIDppHelper.max_load_point_changed_event(self)
        checker = BrakeForceTestUtils.MaxLoadPointChangedEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "maximum_load_point": (checker.check_maximum_load_point, load_point_value_quarter),
        })
        checker.check_fields(self, max_load_point_changed, self.feature_8134.max_load_point_changed_event_cls,
                             check_map)

        self.testCaseChecked("FUN_8134_0002", _AUTHOR)
    # end def test_max_load_point_changed_verify

    @features("Feature8134")
    @level("Functionality")
    def test_max_load_point_changed_no_event_verify(self):
        """
        Validate ``MaxLoadPointChanged`` Event is not generated if there is no change in load point value
        """
        self.post_requisite_reload_nvs = True
        load_point_value_max = HexList("0FFF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        BrakeForceTestUtils.HIDppHelper.set_max_load_point(self, maximum_load_point=load_point_value_max)
        # Added delay to allow previous commands to process and prevent them from generating events after clearing queue
        sleep(.5)
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clearing any existing Event messages of MaxLoad Point Changed "
                                 "type")
        # -----------------------------------------------------------------------------------------------------------
        self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                         class_type=self.feature_8134.max_load_point_changed_event_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        BrakeForceTestUtils.HIDppHelper.set_max_load_point(self, maximum_load_point=load_point_value_max)
        max_load_point_changed_response = self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.event_message_queue,
            class_type=self.feature_8134.max_load_point_changed_event_cls,
            skip_error_message=True, allow_no_message=True)
        # -----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verifying that setting same value twice with SetMaxLoadPoint "
                                  "does not generate event MaxLoadPointChanged ")
        # -----------------------------------------------------------------------------------------------------------
        self.assertEqual(
            expected=None,
            obtained=max_load_point_changed_response,
            msg="event_message_queue is not empty, Event generated despite no change in BrakeForce state")
        self.testCaseChecked("FUN_8134_0003", _AUTHOR)
    # end def test_max_load_point_changed_no_event_verify

    @features("Feature8134")
    @features("Feature1802")
    @level("Functionality")
    def test_set_max_load_point_not_retained_verify(self):
        """
        Validate if value set by ``SetMaxLoadPoint`` is not retained after reset
        """
        self.post_requisite_reload_nvs = True
        load_point_value_quarter = HexList("3FFF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        BrakeForceTestUtils.HIDppHelper.set_max_load_point(self, maximum_load_point=load_point_value_quarter)
        self.feature_1802_index = self.updateFeatureMapping(feature_id=ForceDeviceReset.FEATURE_ID)
        force_device_reset = ForceDeviceReset(deviceIndex=self.deviceIndex, featureId=self.feature_1802_index)
        try:
            self.send_report_to_device(report=force_device_reset, timeout=.6)
        except TransportContextException as e:
            if e.get_cause() != TransportContextException.Cause.CONTEXT_ERROR_PIPE:
                raise
            # end if
        # end try
        # Wait DUT to complete reset procedure
        sleep(5)
        # Reset device connection
        self.reset(hardware_reset=False, recover_time_needed=True)
        sleep(2)
        # Enable Hidden Features
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetMaxLoadPoint request")
        # --------------------------------------------------------------------------------------------------------------
        get_max_load_point_response = BrakeForceTestUtils.HIDppHelper.get_max_load_point(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetMaxLoadPointResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        self.assertNotEquals(unexpected=load_point_value_quarter,
                             obtained=get_max_load_point_response.maximum_load_point,
                             msg=f"The obtained({get_max_load_point_response.maximum_load_point} "
                                 f"differs from the expected value")
        self.testCaseChecked("FUN_8134_0004", _AUTHOR)
    # end def test_set_max_load_point_not_retained_verify

    @features("Feature8134")
    @features("Feature9215")
    @level("Functionality")
    def test_get_info_verify(self):
        """
        Validate if value set by WriteOtherNvsData is same as value read by GetInfo
        """
        self.post_requisite_reload_nvs = True
        valid_range = range(pow(2, 8))
        test_list = choices(valid_range, elem_nb=15)
        data_field_id_zero = HexList("00")

        # -----------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Check value obtained from GetInfo is same as value set with WriteOtherNvsData")
        # -----------------------------------------------------------------------------------------------------------
        for max_load_value in test_list:
            max_load_value = HexList(hex(max_load_value)[2:].ljust(30, '0'))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send WriteOtherNvsData request")
            # ----------------------------------------------------------------------------------------------------------
            Ads1231TestUtils.HIDppHelper.write_other_nvs_data(self, data_field_id=data_field_id_zero,
                                                              data=max_load_value)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send ReadOtherNvsData request")
            # ----------------------------------------------------------------------------------------------------------
            read_other_nvs_data_response = Ads1231TestUtils.HIDppHelper.\
                read_other_nvs_data(self, data_field_id=data_field_id_zero)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verifying data HIDppHelper.read from ReadOtherNvsData matches values "
                                      "set by WriteOtherNvsData")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=max_load_value,
                             obtained=read_other_nvs_data_response.data,
                             msg=f"The value of max load is not as expected")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetInfo request")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8134.get_info_cls(
                device_index=self.deviceIndex,
                feature_index=self.feature_8134_index)
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
                "maximum_kg_load": (checker.check_maximum_kg_load, max_load_value),
            })
            checker.check_fields(self, response, self.feature_8134.get_info_response_cls, check_map)
        # end for
        self.testCaseChecked("FUN_8134_0005", _AUTHOR)
    # end def test_get_info_verify
# end class BrakeForceFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
