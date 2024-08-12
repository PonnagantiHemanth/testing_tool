#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.managedeactivatablefeaturesauth.business
:brief: Manage deactivatable features (based on authentication) business test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.managedeactivatablefeaturesauth import \
    SharedManageDeactivatableFeaturesAuthTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedManageDeactivatableFeaturesAuthBusinessTestCase(SharedManageDeactivatableFeaturesAuthTestCase, ABC):
    """
    Validate Manage deactivatable features (based on authentication) business TestCases
    """
    @features('ManageDeactivatableFeaturesAuth')
    @level('Business')
    def test_enable_manufacturing_features(self):
        """
        For manufacturing, open a session, complete authentication and enable features. Features should be enabled.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all manufacturing features')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the manufacturing bit is set (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check manufacturing is not enabled permanently in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the DUT responds correctly to any manufacturing features requests')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_manufacturing_enabled(self)

        self.testCaseChecked("BUS_MAN_DEACT_FEAT_0001")
    # end def test_enable_manufacturing_features
# end class SharedManageDeactivatableFeaturesAuthBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
