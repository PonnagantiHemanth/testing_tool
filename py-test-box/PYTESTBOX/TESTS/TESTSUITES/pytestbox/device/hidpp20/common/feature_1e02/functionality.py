#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1e02.functionality
:brief: HID++ 2.0 Manage deactivatable features (based on authentication) functionality test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.root import RootFactory
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.hidpp20.common.feature_1e02.managedeactivatablefeaturesauth import \
    DeviceManageDeactivatableFeaturesAuthTestCase
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.functionality import \
    SharedManageDeactivatableFeaturesAuthFunctionalityTestCase
from pytransport.usb.usbconstants import LogitechReceiverProductId


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class DeviceManageDeactivatableFeaturesAuthFunctionalityTestCase(
        DeviceManageDeactivatableFeaturesAuthTestCase, SharedManageDeactivatableFeaturesAuthFunctionalityTestCase):
    """
    Validate the 'manage deactivatable features' mechanism (based on password authentication) functionality test cases
    with a device as a DUT
    """
    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @level('Functionality')
    def test_enable_compliance_features(self):
        """
        Check compliance features can be enabled
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, compliance=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance is enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(compliance=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance features are enabled')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_enabled_features(self, self.compliance_features)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check compliance is not enabled in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(compliance=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0002")
    # end def test_enable_compliance_features

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    @services('Gotthard')
    def test_enable_gotthard_features(self):
        """
        Check Gotthard can be enabled
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Gotthard is enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check Gotthard is enabled in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)

        self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_enabled(
            self,
            device_index_on_gotthard=self.device_index_on_gotthard,
            gotthard_receiver_port_index=self.gotthard_receiver_port_index)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0003")
    # end def test_enable_gotthard_features

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @level('Functionality')
    def test_disable_compliance_features(self):
        """
        Check compliance features can be disabled
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable compliance features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, compliance=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance is enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(compliance=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable compliance')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, compliance=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance is disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(compliance=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance features are disabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_disabled_features(self,
                                                                                          self.compliance_features)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0006")
    # end def test_disable_compliance_features

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @level('Functionality')
    def test_disable_compliance_does_not_enable(self):
        """
        Check disable compliance does not enable compliance
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable compliance')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, compliance=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance is disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(compliance=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable compliance')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, compliance=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance is disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(compliance=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance features are disabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_disabled_features(self,
                                                                                          self.compliance_features)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0010")
    # end def test_disable_compliance_does_not_enable

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Functionality')
    def test_disable_gotthard_does_not_enable(self):
        """
        Check disable Gotthard does not enable Gotthard
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

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
            send_requests=False,
            device_index_on_gotthard=self.device_index_on_gotthard,
            gotthard_receiver_port_index=self.gotthard_receiver_port_index)

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

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0011")
    # end def test_disable_gotthard_does_not_enable

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    def test_enable_manufacturing_features_others_not_enabled(self):
        """
        Check enabling manufacturing does not enable the others
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all features are disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False, compliance=False, gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance and Gotthard are disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True, compliance=False, gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance features are disabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_disabled_features(self,
                                                                                          self.compliance_features)

        self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_disabled(
            self,
            get_info_state=False,
            device_index_on_gotthard=self.device_index_on_gotthard,
            gotthard_receiver_port_index=self.gotthard_receiver_port_index)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0012")
    # end def test_enable_manufacturing_features_others_not_enabled

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @level('Functionality')
    def test_enable_compliance_features_others_not_enabled(self):
        """
        Check enabling compliance does not enable the others
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all features are disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False, compliance=False, gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, compliance=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing and Gotthard are disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False, compliance=True, gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing features are disabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_disabled_features(self,
                                                                                          self.manufacturing_features)

        self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_disabled(
            self,
            get_info_state=False,
            device_index_on_gotthard=self.device_index_on_gotthard,
            gotthard_receiver_port_index=self.gotthard_receiver_port_index)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0013")
    # end def test_enable_compliance_features_others_not_enabled

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Functionality')
    def test_enable_gotthard_features_others_not_enabled(self):
        """
        Check enabling Gotthard does not enable the others
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all features are disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False, compliance=False, gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing and compliance are disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False, compliance=False, gothard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing features are disabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_disabled_features(self,
                                                                                          self.manufacturing_features)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance features are disabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_disabled_features(self,
                                                                                          self.compliance_features)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0014")
    # end def test_enable_gotthard_features_others_not_enabled

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    def test_disable_manufacturing_features_others_not_disabled(self):
        """
        Check disabling manufacturing does not disable the others
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, enable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all features are enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_compliance = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportCompliance
        expected_gotthard = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportGotthard
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=True, compliance=expected_compliance, gothard=expected_gotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance and Gotthard are enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=False, compliance=expected_compliance, gothard=expected_gotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance features are enabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        if expected_compliance:
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_enabled_features(self,
                                                                                             self.compliance_features)
        # end if

        if expected_gotthard:
            self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_enabled(
                self,
                get_info_state=False,
                device_index_on_gotthard=self.device_index_on_gotthard,
                gotthard_receiver_port_index=self.gotthard_receiver_port_index)
        # end if

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0015")
    # end def test_disable_manufacturing_features_others_not_disabled

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @level('Functionality')
    def test_disable_compliance_features_others_not_disabled(self):
        """
        Check disabling compliance does not disable the others
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, enable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all features enable state are as expected (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=self.config.F_SupportManufacturing,
            compliance=True,
            gothard=self.config.F_SupportGotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, compliance=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance is disabled and other features are as expected (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=self.config.F_SupportManufacturing,
            compliance=False,
            gothard=self.config.F_SupportGotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing features are enabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_enabled_features(self,
                                                                                         self.manufacturing_features)
        if self.config.F_SupportGotthard:
            self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_enabled(
                self,
                get_info_state=False,
                device_index_on_gotthard=self.device_index_on_gotthard,
                gotthard_receiver_port_index=self.gotthard_receiver_port_index)
        # end if

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0016")
    # end def test_disable_compliance_features_others_not_disabled

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Functionality')
    @bugtracker('Foster_DisableFeatures_Gotthard')
    def test_disable_gotthard_features_others_not_disabled(self):
        """
        Check disabling Gotthard does not disable the others
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, enable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all features are enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True, compliance=True, gothard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing and compliance are enabled (get info state). Gotthard should '
                                  'be still enabled (disabled only after re-init')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True, compliance=True, gotthard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing features are enabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_enabled_features(self,
                                                                                         self.manufacturing_features)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check compliance features are enabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_enabled_features(self,
                                                                                         self.compliance_features)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0017")
    # end def test_disable_gotthard_features_others_not_disabled

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportCompliance')
    @level('Functionality')
    def test_get_info_opened_compliance_session(self):
        """
        Check support and persist bit map do not change when sessions are opened
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Open session')
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
            test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.COMPLIANCE.value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check get info state')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0019")
    # end def test_get_info_opened_compliance_session

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Functionality')
    def test_get_info_opened_gotthard_session(self):
        """
        Check support and persist bit map do not change when sessions are opened
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Open session')
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
            test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.GOTHARD.value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check get info state')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0020")
    # end def test_get_info_opened_gotthard_session

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Functionality')
    @services('Gotthard')
    def test_disable_gotthard_with_gotthard(self):
        """
        Check Gotthard can be disabled with Gotthard
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Gotthard')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch to Gotthard receiver')
        # --------------------------------------------------------------------------------------------------------------
        if ChannelUtils.get_receiver_channel(
                self).get_transport_id() in LogitechReceiverProductId.unifying_pids():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Turn off current Unifying receiver on port {self.receiver_port_index}')
            # ----------------------------------------------------------------------------------------------------------
            self.device.disable_usb_port(self.receiver_port_index)
        # end if

        ReceiverTestUtils.switch_to_receiver(
            self,
            self.gotthard_receiver_port_index,
            task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
        ReceiverTestUtils.GotthardReceiver.init_connection(self)

        # -------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Features')
        # -------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(
            self, device_index=self.device_index_on_gotthard, port_index=self.gotthard_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable Gotthard')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(
            self, gotthard=True,
            device_index=self.device_index_on_gotthard, port_index=self.gotthard_receiver_port_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.device_debugger.reset(soft_reset=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check Gotthard is disabled in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Gotthard is disabled')
        # --------------------------------------------------------------------------------------------------------------
        root_feature = RootFactory.create(
                            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT))
        get_feature = root_feature.get_feature_cls(deviceIndex=self.device_index_on_gotthard, featureId=0x0000)
        self.assertRaises(AssertionError,
                          ChannelUtils.send,
                          test_case=self,
                          report=get_feature,
                          response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                          response_class_type=root_feature.get_feature_response_cls)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0021")
    # end def test_disable_gotthard_with_gotthard

    @features('ManageDeactivatableFeaturesAuth')
    @features('ManageDeactivatableFeaturesSupportGotthard')
    @level('Functionality')
    @services('Gotthard')
    @bugtracker('Foster_DisableFeatures_Gotthard')
    def test_gotthard_not_disable_before_reset(self):
        """
        Check Gotthard is not disabled before reset
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_switch_back_receiver = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Gotthard')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Gotthard is enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        gotthard_enabled = ManageDeactivatableFeaturesAuth.BitMap(gothard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state=gotthard_enabled)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check Gotthard is enabled in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_state=gotthard_enabled)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch back to initial receiver')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel, open_channel=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable Gotthard')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, gotthard=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Gotthard is not disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check Gotthard is disabled in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable Hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Gotthard is disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check Gotthard is disabled in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(gothard=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Switch to Gotthard receiver')
        # --------------------------------------------------------------------------------------------------------------
        if ChannelUtils.get_receiver_channel(
                self).get_transport_id() in LogitechReceiverProductId.unifying_pids():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Turn off current Unifying receiver on port {self.receiver_port_index}')
            # ----------------------------------------------------------------------------------------------------------
            self.device.disable_usb_port(self.receiver_port_index)
        # end if

        ReceiverTestUtils.switch_to_receiver(
            self,
            self.gotthard_receiver_port_index,
            task_enabler=ReceiverTestUtils.GotthardReceiver.GOTTHARD_TASK_ENABLER)
        ReceiverTestUtils.GotthardReceiver.init_connection(self, assert_connection=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Gotthard is disabled')
        # --------------------------------------------------------------------------------------------------------------
        root_feature = RootFactory.create(
                            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.IMPORTANT.ROOT))
        get_feature = root_feature.get_feature_cls(deviceIndex=self.device_index_on_gotthard, featureId=0x0000)
        self.assertRaises(AssertionError,
                          ChannelUtils.send,
                          test_case=self,
                          report=get_feature,
                          response_queue_name=HIDDispatcher.QueueName.IMPORTANT,
                          response_class_type=root_feature.get_feature_response_cls)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0022")
    # end def test_gotthard_not_disable_before_reset
# end class DeviceManageDeactivatableFeaturesAuthFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
