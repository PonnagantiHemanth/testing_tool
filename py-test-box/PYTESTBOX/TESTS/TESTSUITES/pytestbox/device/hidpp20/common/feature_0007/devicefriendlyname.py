#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname
:brief: Validate HID++ 2.0 DeviceFriendlyName feature
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/10/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import warnings
from random import choices
from string import ascii_uppercase
from string import digits

from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameFactory
from pylibrary.tools.docutils import DocUtils
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceFriendlyNameTestCase(DeviceBaseTestCase):
    """
    Validates DeviceFriendlyName TestCases in Application mode
    """
    @DocUtils.copy_doc(DeviceBaseTestCase.setUp)
    def setUp(self):
        # Start with super setUp()
        super().setUp()

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get Feature 0x0007")
        # ----------------------------------------------------------------------------
        self.feature_0007_index, self.feature_0007, _, _ = DeviceFriendlyNameTestUtils.HIDppHelper.get_parameters(
            self,
            DeviceFriendlyName.FEATURE_ID,
            DeviceFriendlyNameFactory)

        # Size of name_chunk to read/write coming from 0x1807 properties if any, else from 0x0007 settings
        friendly_name_len = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(
            self, ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
        if friendly_name_len == 0:
            friendly_name_len = self.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME.F_NameMaxLength
        # end if
        payload_size = self.feature_0007.set_friendly_name_cls.LEN.NAME_CHUNK // 8
        if friendly_name_len > payload_size:
            warnings.warn("Tests scripts might not cover this case correctly yet. TODO: if this becomes necessary, "
                          "please check scripts and update.")
        # end if
        # Workaround to run tests only on names fitting in 1 request
        self.name_chunk_length = min(payload_size, friendly_name_len)
        self.test_name_chunk = ''.join(choices(ascii_uppercase + digits, k=self.name_chunk_length))
    # end def setUp

    def tearDown(self):
        """
        Handles post-requisites
        """
        if self.post_requisite_reload_nvs:
            # --------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Reload initial NVS")
            # --------------------------------------------------------------------------
            CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            self.post_requisite_reload_nvs = False
        # end if
        super().tearDown()
    # end def tearDown
# end class DeviceFriendlyNameTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
