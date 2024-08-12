#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1e02.managedeactivatablefeaturesauth
:brief: Validate HID++ 2.0 Manage deactivatable features based on authentication mechanism
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthFactory
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.passwordauthenticationutils import DevicePasswordAuthenticationTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.hidpp.managedeactivatablefeaturesauth.managedeactivatablefeaturesauth import \
    SharedManageDeactivatableFeaturesAuthTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceManageDeactivatableFeaturesAuthTestCase(SharedManageDeactivatableFeaturesAuthTestCase, DeviceBaseTestCase):
    """
    Validate the 'manage deactivatable features' mechanism based on password authentication with a device as a DUT
    """
    ManageDeactivatableFeaturesAuthTestUtils = DeviceManageDeactivatableFeaturesAuthTestUtils
    PasswordAuthenticationTestUtils = DevicePasswordAuthenticationTestUtils
    TestUtilsFacade = DeviceTestUtils

    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_switch_back_receiver = False

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        gothard_enabling_chunks = self.memory_manager.get_chunks_by_name('NVS_X1E02_STATE_ID')
        if len(gothard_enabling_chunks) > 0 and HexList(gothard_enabling_chunks[-1]) != HexList(0x00):
            self.post_requisite_reload_nvs = True
            state = ManageDeactivatableFeaturesAuth.BitMap(manufacturing=0, compliance=0, gothard=0)
            self.ManageDeactivatableFeaturesAuthTestUtils.NvsHelper.force_state(self, state)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get receivers port index')
        # --------------------------------------------------------------------------------------------------------------
        self.receiver_port_index = ChannelUtils.get_port_index(test_case=self)
        self.gotthard_receiver_port_index = ReceiverTestUtils.get_receiver_port_index(
            self, ReceiverTestUtils.USB_PID_GOTTHARD)
        self.device_index_on_gotthard = 0x01

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature 0x1E02 index')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1e02_index = DeviceBaseTestUtils.HIDppHelper.get_feature_index(
            self, ManageDeactivatableFeaturesAuth.FEATURE_ID)
        self.feature_1e02 = ManageDeactivatableFeaturesAuthFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable Hidden Features')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Features sets setup')
        # --------------------------------------------------------------------------------------------------------------
        self.manufacturing_features, self.compliance_features, _ = \
            self.ManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_features(
                self, manufacturing=True, compliance=True, gotthard=True)

        self.config = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES_AUTH
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if not self.device.get_usb_ports_status()[self.receiver_port_index]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, f'Turn on the regular receiver on port {self.receiver_port_index}')
                # ------------------------------------------------------------------------------------------------------
                self.device.enable_usb_port(self.receiver_port_index)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs or self.post_requisite_switch_back_receiver:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_switch_back_receiver:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Switch back to initial receiver')
                # ------------------------------------------------------------------------------------------------------
                ReceiverTestUtils.switch_to_receiver(self, self.receiver_port_index)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.gotthard_receiver_port_index is not None:
                # Remove all channels related to the gotthard receiver
                DeviceManagerUtils.remove_channel_from_cache(
                    test_case=self, port_index=self.gotthard_receiver_port_index)
            # end if
        # end with

        super().tearDown()
    # end def tearDown
# end class DeviceManageDeactivatableFeaturesAuthTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
