#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1806.configurabledeviceproperties
:brief: Validate HID++ 2.0 Configurable Device Properties test case
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/04/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesFactory
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameFactory
from pyhid.hidpp.features.devicereset import DeviceReset
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ConfigurableDevicePropertiesTestCase(DeviceBaseTestCase):
    """
    Validates ConfigurableDeviceProperties TestCases in Application mode
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        # Start with super setUp()
        super().setUp()
        # ----------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ----------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)
        self.set_feature_1806()
        self.enable_hidden_feature()
    # end def setUp

    def tearDown(self):
        """
        Handles test post requisites.
        """
        if self.post_requisite_reload_nvs:
            # ------------------------------------------------------
            LogHelper.log_post_requisite(self, "Reload initial NVS")
            # ------------------------------------------------------
            CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            self.post_requisite_reload_nvs = False
        # end if
        super().tearDown()
    # end def tearDown

    def enable_hidden_feature(self):
        # ---------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # ---------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
    # end def enable_hidden_feature

    def set_feature_0007(self):
        """
        Feature 0007
        """
        # --------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x0007)")
        # --------------------------------------------------------------
        self.feature_0007_index = self.updateFeatureMapping(feature_id=DeviceFriendlyName.FEATURE_ID)
        self.feature_0007 = DeviceFriendlyNameFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME))
    # end def set_feature_0007

    def set_feature_1802(self):
        """
        Feature 1802
        """
        # --------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x1802)")
        # --------------------------------------------------------------
        self.feature_1802_index = self.updateFeatureMapping(feature_id=DeviceReset.FEATURE_ID)
    # end def set_feature_1802

    def set_feature_1806(self):
        """
        Feature 1806
        """
        # --------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x1806)")
        # --------------------------------------------------------------
        self.feature_1806_index = self.updateFeatureMapping(feature_id=ConfigurableDeviceProperties.FEATURE_ID)
        self.feature_1806 = ConfigurableDevicePropertiesFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_PROPERTIES))
    # end def set_feature_1806
# end class ConfigurableDevicePropertiesTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
