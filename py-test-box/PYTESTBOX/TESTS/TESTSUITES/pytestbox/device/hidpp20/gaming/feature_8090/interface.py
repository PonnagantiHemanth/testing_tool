#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8090.interface
:brief: HID++ 2.0 ``ModeStatus`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils
from pytestbox.device.hidpp20.gaming.feature_8090.modestatus import ModeStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ModeStatusInterfaceTestCase(ModeStatusTestCase):
    """
    Validate ``ModeStatus`` interface test cases
    """

    @features("Feature8090")
    @level("Interface")
    def test_get_mode_status(self):
        """
        Validate ``GetModeStatus`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8090.get_mode_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8090_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8090.get_mode_status_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetModeStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ModeStatusTestUtils.GetModeStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.device_index),
            "featureIndex": (checker.check_feature_index, report.feature_index)
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        self.testCaseChecked("INT_8090_0001", _AUTHOR)
    # end def test_get_mode_status

    @features("Feature8090")
    @level("Interface")
    def test_set_mode_status(self):
        """
        Validate ``SetModeStatus`` interface
        """
        self.post_requisite_reload_nvs = True
        mode_status_0 = 0x00
        mode_status_1 = 0x00
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8090.set_mode_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8090_index,
            mode_status_0=mode_status_0,
            mode_status_1=mode_status_1,
            changed_mask_0=changed_mask_0,
            changed_mask_1=changed_mask_1)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8090.set_mode_status_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetModeStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.device_index),
            "featureIndex": (checker.check_feature_index, report.feature_index),
        }
        checker.check_fields(self, response, self.feature_8090.set_mode_status_response_cls, check_map)

        self.testCaseChecked("INT_8090_0002", _AUTHOR)
    # end def test_set_mode_status

    @features("Feature8090")
    @level("Interface")
    def test_get_dev_config(self):
        """
        Validate ``GetDevConfig`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDevConfig request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8090.get_dev_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8090_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8090.get_dev_config_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetDevConfigResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ModeStatusTestUtils.GetDevConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.device_index),
            "featureIndex": (checker.check_feature_index, report.feature_index)
        })
        checker.check_fields(self, response, self.feature_8090.get_dev_config_response_cls, check_map)

        self.testCaseChecked("INT_8090_0003", _AUTHOR)
    # end def test_get_dev_config
# end class ModeStatusInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
