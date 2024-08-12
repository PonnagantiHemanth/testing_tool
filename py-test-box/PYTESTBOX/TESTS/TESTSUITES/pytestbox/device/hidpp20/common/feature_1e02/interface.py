#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1e02.interface
:brief: HID++ 2.0 Manage deactivatable features (based on authentication) interface test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1e02.managedeactivatablefeaturesauth import \
    DeviceManageDeactivatableFeaturesAuthTestCase
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.interface import \
    SharedManageDeactivatableFeaturesAuthInterfaceTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceManageDeactivatableFeaturesAuthInterfaceTestCase(DeviceManageDeactivatableFeaturesAuthTestCase,
                                                             SharedManageDeactivatableFeaturesAuthInterfaceTestCase):
    """
    Validate the 'manage deactivatable features' mechanism (based on password authentication) interface test cases
    with a device as a DUT
    """
    @features('ManageDeactivatableFeaturesAuth')
    @level('Interface')
    def test_get_react_info_api(self):
        """
        Validates getReactInfo API
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getReactInfo request')
        # --------------------------------------------------------------------------------------------------------------
        get_react_info_resp = self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_reactivation_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check response fields')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.GetReactInfoResponseChecker.check_fields(
            self,
            get_react_info_resp,
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_feature_interface(
                test_case=self).get_reactivation_info_response_cls)

        self.testCaseChecked("INT_MAN_DEACT_FEAT_0004")
    # end def test_get_react_info_api
# end class DeviceManageDeactivatableFeaturesAuthInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
