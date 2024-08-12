#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hidpp.managedeactivatablefeaturesauth.functionality
:brief: Manage deactivatable features (based on authentication) functionality test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from os.path import join

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.managedeactivatablefeaturesauth import \
    SharedManageDeactivatableFeaturesAuthTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SharedManageDeactivatableFeaturesAuthFunctionalityTestCase(SharedManageDeactivatableFeaturesAuthTestCase, ABC):
    """
    Validate Manage deactivatable features (based on authentication) functionality TestCases
    """
    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    @services("Debugger")
    def test_default_fw(self):
        """
        Check default activation state

        Gotthard is activated by default in the FW code.
        TDE commands are not activated by default in the FW
        Compliance commands are not activated by default in the FW
        """
        self.post_requisite_reload_nvs = True

        if self.current_channel.protocol == LogitechProtocol.USB and self.current_channel.is_open:
            ChannelUtils.close_channel(test_case=self)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reload default firmware')
        # --------------------------------------------------------------------------------------------------------------
        default_firmware = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)
        self.debugger.reload_file(firmware_hex_file=default_firmware, nvs_hex_file=default_firmware)

        if self.current_channel.protocol == LogitechProtocol.USB:
            DfuTestUtils.verify_communication_disconnection_then_reconnection(test_case=self)
        # end if

        if self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH.F_SupportGotthard:
            self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_enabled(
                self,
                device_index_on_gotthard=self.device_index_on_gotthard,
                gotthard_receiver_port_index=self.gotthard_receiver_port_index)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Read NVS and check Gotthard is disabled in NVS')
            # ----------------------------------------------------------------------------------------------------------
            expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap()
            self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)
        # end if

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0001")
    # end def test_default_fw

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    def test_enable_all_features(self):
        """
        Check all deactivatable features and Gotthard can be enabled using the "allBit"
        """
        self.post_requisite_reload_nvs = True

        config = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable features')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, enable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all supported features are enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=config.F_SupportManufacturing,
            compliance=config.F_SupportCompliance,
            gothard=config.F_SupportGotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        if config.F_SupportManufacturing:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check manufacturing features are enabled (send requests)')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_manufacturing_enabled(self)
        # end if

        if config.F_SupportCompliance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check compliance features are enabled (send requests)')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_compliance_enabled(self)
        # end if

        if config.F_SupportGotthard:
            self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_enabled(
                self,
                device_index_on_gotthard=self.device_index_on_gotthard,
                gotthard_receiver_port_index=self.gotthard_receiver_port_index)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check persistent features (i.e. Gotthard) are enabled in NVS')
        # --------------------------------------------------------------------------------------------------------------
        expected_nvs_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=config.F_PersistentActivationManufacturing,
            compliance=config.F_PersistentActivationCompliance,
            gothard=config.F_PersistentActivationGotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_nvs_state)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0004")
    # end def test_enable_all_features

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    def test_disable_manufacturing_features(self):
        """
        Check manufacturing features can be disabled
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable manufacturing features')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing is enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=True)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable manufacturing')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing is disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing features are disabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_manufacturing_disabled(self)
        self.post_requisite_reset_receiver = False

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0005")
    # end def test_disable_manufacturing_features

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    @bugtracker('Foster_DisableFeatures_Gotthard')
    def test_disable_all_features(self):
        """
        Check all deactivatable features and Gotthard can be disabled using the "allBit"
        """
        self.post_requisite_reload_nvs = True

        config = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, enable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check supported features are enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=config.F_SupportManufacturing,
            compliance=config.F_SupportCompliance,
            gothard=config.F_SupportGotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, disable_all=True)

        if config.F_SupportGotthard:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check all features are disabled (get info state). '
                                      'Gotthard should be disabled only after reset')
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False, compliance=False, gothard=True)
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check all features are disabled (get info state).')
            # ----------------------------------------------------------------------------------------------------------
            expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False, compliance=False)
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)
        # end if

        if config.F_SupportManufacturing:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check manufacturing features are disabled (send requests)')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_manufacturing_disabled(self)
            self.post_requisite_reset_receiver = False
        # end if

        if config.F_SupportCompliance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check compliance features are disabled (send requests)')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_compliance_disabled(self)
        # end if

        if config.F_SupportGotthard:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Reset')
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enable Hidden Features')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_hidden_features(self)

            self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_disabled(
                self,
                device_index_on_gotthard=self.device_index_on_gotthard,
                gotthard_receiver_port_index=self.gotthard_receiver_port_index)
        # end if

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0007")
    # end def test_disable_all_features

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    def test_persistent_activation(self):
        """
        Check reset does not disable deactivatable features or Gotthard if activation is persistent and disables
        deactivatable features or Gotthard if activation is volatile.
        """
        self.post_requisite_reload_nvs = True

        config = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all features')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(self, enable_all=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check supported features are enabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=config.F_SupportManufacturing,
            compliance=config.F_SupportCompliance,
            gothard=config.F_SupportGotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Activate Features')
        # --------------------------------------------------------------------------------------------------------------
        self.TestUtilsFacade.HIDppHelper.activate_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check deactivatable features are enabled only if activation is '
                                  'persistent (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(
            manufacturing=config.F_PersistentActivationManufacturing,
            compliance=config.F_PersistentActivationCompliance,
            gothard=config.F_PersistentActivationGotthard)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Read NVS and check deactivatable features are enabled only if '
                                  'activation is persistent (NVS state)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.check_state(self, expected_state)

        if config.F_SupportManufacturing:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check manufacturing features are disabled (send requests)')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_manufacturing_disabled(self)
        # end if

        if config.F_SupportCompliance:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check compliance features are disabled (send requests)')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_compliance_disabled(self)
        # end if

        if config.F_SupportGotthard:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Gotthard is enabled')
            # ----------------------------------------------------------------------------------------------------------
            self.ManageDeactivatableFeaturesAuthTestUtils.check_gotthard_enabled(
                self,
                device_index_on_gotthard=self.device_index_on_gotthard,
                gotthard_receiver_port_index=self.gotthard_receiver_port_index)
        # end if

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0008")
    # end def test_persistent_activation

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    def test_disable_manufacturing_does_not_enable(self):
        """
        Check disable manufacturing does not enable manufacturing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable manufacturing')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing is disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable manufacturing')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing is disabled (get info state)')
        # --------------------------------------------------------------------------------------------------------------
        expected_state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=False)
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self, expected_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check manufacturing features are disabled (send requests)')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_manufacturing_disabled(self)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0009")
    # end def test_disable_manufacturing_does_not_enable

    @features('ManageDeactivatableFeaturesAuth')
    @level('Functionality')
    def test_get_info_opened_manufacturing_session(self):
        """
        Check support and persist bit map do not change when sessions are opened
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Open session')
        # --------------------------------------------------------------------------------------------------------------
        self.PasswordAuthenticationTestUtils.HIDppHelper.start_session(
            test_case=self, account_name=self.PasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check get info state')
        # --------------------------------------------------------------------------------------------------------------
        self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.check_state(self)

        self.testCaseChecked("FUN_MAN_DEACT_FEAT_0018")
    # end def test_get_info_opened_manufacturing_session
# end class SharedManageDeactivatableFeaturesAuthFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
