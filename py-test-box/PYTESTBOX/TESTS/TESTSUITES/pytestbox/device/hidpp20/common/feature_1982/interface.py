#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1982.interface
:brief: HID++ 2.0 ``Backlight`` interface test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.backlight import Backlight
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.hidpp20.common.feature_1982.backlight import BacklightTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightInterfaceTestCase(BacklightTestCase):
    """
    Validate ``Backlight`` interface test cases
    """

    @features("Feature1982")
    @level("Interface")
    @services('Debugger')
    def test_get_backlight_config(self):
        """
        Validate ``GetBacklightConfig`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetBacklightConfig request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.get_backlight_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1982.get_backlight_config_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetBacklightConfigResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BacklightTestUtils.GetBacklightConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1982_index)),
        })
        checker.check_fields(self, response, self.feature_1982.get_backlight_config_response_cls, check_map)

        self.testCaseChecked("INT_1982_0001", _AUTHOR)
    # end def test_get_backlight_config

    @features("Feature1982")
    @level("Interface")
    def test_set_backlight_config(self):
        """
        Validate ``SetBacklightConfig`` interface
        """
        self.post_requisite_reload_nvs = True
        configuration = Backlight.Configuration.ENABLE
        default_options = BacklightTestUtils.get_default_options(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetBacklightConfig request")
        # --------------------------------------------------------------------------------------------------------------
        response = BacklightTestUtils.HIDppHelper.set_backlight_config(test_case=self,
                                                                       configuration=configuration,
                                                                       options=default_options)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetBacklightConfigResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1982_index)),
        }
        checker.check_fields(self, response, self.feature_1982.set_backlight_config_response_cls, check_map)

        self.testCaseChecked("INT_1982_0002", _AUTHOR)
    # end def test_set_backlight_config

    @features("Feature1982")
    @level("Interface")
    @services('Debugger')
    def test_get_backlight_info(self):
        """
        Validate ``GetBacklightInfo`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetBacklightInfo request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.get_backlight_info_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1982.get_backlight_info_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetBacklightInfoResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = BacklightTestUtils.GetBacklightInfoResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1982_index)),
        })
        checker.check_fields(self, response, self.feature_1982.get_backlight_info_response_cls, check_map)

        self.testCaseChecked("INT_1982_0003", _AUTHOR)
    # end def test_get_backlight_info

    @features("Feature1982v2+")
    @level("Interface")
    def test_set_backlight_effect(self):
        """
        Validate ``SetBacklightEffect`` interface
        """
        self.post_requisite_reload_nvs = True
        backlight_effect = HexList(Backlight.BacklightEffect.CURRENT_EFFECT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetBacklightEffect request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.set_backlight_effect_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index,
            backlight_effect=backlight_effect)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1982.set_backlight_effect_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetBacklightEffectResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "device_index": (checker.check_device_index, HexList(ChannelUtils.get_device_index(self))),
            "feature_index": (checker.check_feature_index, HexList(self.feature_1982_index)),
        }
        checker.check_fields(self, response, self.feature_1982.set_backlight_effect_response_cls, check_map)

        self.testCaseChecked("INT_1982_0004", _AUTHOR)
    # end def test_set_backlight_effect
# end class BacklightInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
