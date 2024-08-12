#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80d0.functionality
:brief: HID++ 2.0 ``CombinedPedals`` functionality test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.combinedpedalsutils import CombinedPedalsTestUtils as Utils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.gaming.feature_80d0.combinedpedals import CombinedPedalsTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CombinedPedalsFunctionalityTestCase(CombinedPedalsTestCase):
    """
    Validates ``CombinedPedals`` functionality test cases
    """
    @features("Feature80D0")
    @level("Functionality")
    def test_set_get_combined_pedals(self):
        """
        Validate if value set by ``SetCombinedPedals`` is same as value read by ``GetCombinedPedals``
        """
        for enable_combined_pedals in [True, False]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCombinedPedals request with enable = {enable_combined_pedals}")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_combined_pedals(self, enable_combined_pedals=enable_combined_pedals)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCombinedPedals request")
            # ----------------------------------------------------------------------------------------------------------
            get_combined_pedals_response = Utils.HIDppHelper.get_combined_pedals(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, "Verify SetCombinedPedals.enable_combined_pedals == GetCombinedPedals.combined_pedals_enabled")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList(enable_combined_pedals),
                             obtained=HexList(get_combined_pedals_response.combined_pedals_enabled),
                             msg="combined pedals status different")
        # end for

        self.testCaseChecked("FUN_80D0_0001", _AUTHOR)
    # end def test_set_get_combined_pedals

    @features("Feature80D0")
    @level("Functionality")
    def test_combined_pedals_changed_event(self):
        """
        Validate ``CombinedPedalsChanged`` Event is generated if there is a change in CombinedPedals state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetCombinedPedals request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_combined_pedals(self, enable_combined_pedals=False)

        # Added delay to allow previous commands to process and prevent them from generating events after clearing queue
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Clear any existing Event messages of combined pedals changed type")
        # --------------------------------------------------------------------------------------------------------------
        self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                         class_type=self.feature_80d0.combined_pedals_changed_event_cls)

        for enable_combined_pedals in [True, False]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCombinedPedals request with enable = {enable_combined_pedals}")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_combined_pedals(self, enable_combined_pedals=enable_combined_pedals)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, "Verifying SetCombinedPedals with new status should generate event CombinedPedalsChanged")
            # ----------------------------------------------------------------------------------------------------------
            combined_pedals_changed_event_response = Utils.HIDppHelper.combined_pedals_changed_event(self)
            self.assertEqual(expected=HexList(enable_combined_pedals),
                             obtained=HexList(combined_pedals_changed_event_response.combined_pedals_enabled),
                             msg="combined pedals status is not affected")
        # end for

        self.testCaseChecked("FUN_80D0_0002", _AUTHOR)
    # end def test_combined_pedals_changed_event

    @features("Feature80D0")
    @level("Functionality")
    def test_combined_pedals_changed_event_no_event(self):
        """
        Validate ``CombinedPedalsChanged`` Event is not generated if there is no change in CombinedPedals state
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetCombinedPedals request")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_combined_pedals(self, enable_combined_pedals=False)

        # Added delay to allow previous commands to process and prevent them from generating events after clearing queue
        sleep(.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Clear any existing Event messages of combined pedals changed type")
        # --------------------------------------------------------------------------------------------------------------
        self.clean_message_type_in_queue(queue=self.hidDispatcher.event_message_queue,
                                         class_type=self.feature_80d0.combined_pedals_changed_event_cls)

        for enable_combined_pedals in [True, False]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCombinedPedals request with enable = {enable_combined_pedals}")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_combined_pedals(self, enable_combined_pedals=enable_combined_pedals)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, "Verifying SetCombinedPedals with new status should generate event CombinedPedalsChanged")
            # ----------------------------------------------------------------------------------------------------------
            combined_pedals_changed_event_response = Utils.HIDppHelper.combined_pedals_changed_event(self)
            self.assertEqual(expected=HexList(enable_combined_pedals),
                             obtained=HexList(combined_pedals_changed_event_response.combined_pedals_enabled),
                             msg="combined pedals status is not affected")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCombinedPedals request with enable = {enable_combined_pedals} again")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.set_combined_pedals(self, enable_combined_pedals=enable_combined_pedals)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, "Verifying SetCombinedPedals with same status should not generate event CombinedPedalsChanged")
            # ----------------------------------------------------------------------------------------------------------
            combined_pedals_changed_event_response = self.get_first_message_type_in_queue(
                queue=self.hidDispatcher.event_message_queue,
                class_type=self.feature_80d0.combined_pedals_changed_event_cls,
                skip_error_message=True)
            self.assertNone(
                obtained=combined_pedals_changed_event_response,
                msg="event_message_queue is not empty. Event is generated despite no change in CombinedPedals state")
        # end for

        self.testCaseChecked("FUN_80D0_0003", _AUTHOR)
    # end def test_combined_pedals_changed_event_no_event

    @features("Feature80D0")
    @features("Feature1802")
    @level("Functionality")
    def test_set_combined_pedals_after_reset(self):
        """
        Validate ``SetCombinedPedals`` functionality after device reset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetCombinedPedals request")
        # --------------------------------------------------------------------------------------------------------------
        response = Utils.HIDppHelper.get_combined_pedals(self)
        initial_pedal_status = response.combined_pedals_enabled
        new_pedal_status = not initial_pedal_status

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetCombinedPedals request with enable = {new_pedal_status}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.set_combined_pedals(self, enable_combined_pedals=new_pedal_status)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send ForceDeviceReset")
        # --------------------------------------------------------------------------------------------------------------
        feature_index_1802 = self.updateFeatureMapping(feature_id=ForceDeviceReset.FEATURE_ID)
        force_device_reset = ForceDeviceReset(deviceIndex=self.deviceIndex,
                                              featureId=feature_index_1802)
        self.send_report_to_device(report=force_device_reset)
        # Wait DUT to complete reset procedure
        sleep(5)
        self.set_receiver_wireless_notification_and_wait_notification()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable manufacturing features again")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetCombinedPedals request")
        # --------------------------------------------------------------------------------------------------------------
        response = Utils.HIDppHelper.get_combined_pedals(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verifying that CombinedPedals Status is back to original state after device reset")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HexList(initial_pedal_status),
                         obtained=HexList(response.combined_pedals_enabled),
                         msg="combined pedals status should not be affected by device reset")

        self.testCaseChecked("FUN_80D0_0004", _AUTHOR)
    # end def test_set_combined_pedals_after_reset
# end class CombinedPedalsFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
