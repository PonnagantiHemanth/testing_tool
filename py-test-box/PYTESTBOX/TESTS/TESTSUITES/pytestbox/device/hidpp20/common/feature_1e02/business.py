#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1e02.business
:brief: HID++ 2.0 Manage deactivatable features (based on authentication) business test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.hidpp20.common.feature_1e02.managedeactivatablefeaturesauth import \
    DeviceManageDeactivatableFeaturesAuthTestCase
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.business import \
    SharedManageDeactivatableFeaturesAuthBusinessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceManageDeactivatableFeaturesAuthBusinessTestCase(DeviceManageDeactivatableFeaturesAuthTestCase,
                                                            SharedManageDeactivatableFeaturesAuthBusinessTestCase):
    """
    Validate the 'manage deactivatable features' mechanism (based on password authentication) business test cases
    with a device as a DUT
    """
    @features('ManageDeactivatableFeaturesAuth')
    @level('Business', 'SmokeTests')
    @services('Gotthard')
    def test_enable_manufacturing_and_gotthard_features(self):
        """
        For manufacturing and gotthard, open a session, complete authentication and enable features. Features should be
        enabled.
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(
            self, manufacturing=True, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing and Gotthard are enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True, gothard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check Gotthard is enabled in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing features are enabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_enabled_features(self,
                                                                                         self.manufacturing_features)

        self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_enabled(
            self,
            device_index_on_gotthard=self.device_index_on_gotthard,
            gotthard_receiver_port_index=self.gotthard_receiver_port_index)

        self.testCaseChecked("BUS_MAN_DEACT_FEAT_0002")
    # end def test_enable_manufacturing_and_gotthard_features

    @features('ManageDeactivatableFeaturesAuth')
    @level('Business')
    @services('Gotthard')
    def test_disable_gotthard_after_reset(self):
        """
        Check Gotthard can be disabled without authentication
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable Gotthard')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable Gotthard')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_disabled(
            self,
            device_index_on_gotthard=self.device_index_on_gotthard,
            gotthard_receiver_port_index=self.gotthard_receiver_port_index)

        self.testCaseChecked("BUS_MAN_DEACT_FEAT_0003")
    # end def test_disable_gotthard_after_reset
# end class ManageDeactivatableFeaturesAuthBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
