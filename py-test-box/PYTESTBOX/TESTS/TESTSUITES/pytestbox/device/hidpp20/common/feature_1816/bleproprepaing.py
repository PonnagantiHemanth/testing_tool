#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1816.bleproprepairing
:brief: Validate HID++ 2.0 BLEPro pre-pairing feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairing
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingFactory
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Christophe Roquebert"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BleProPrePairingTestCase(DeviceBaseTestCase):
    """
    Validate ``BleProPrePairing`` TestCases in Application mode
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_program_nvs = False

        # Start with super setUp()
        super().setUp()

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x1816)")
        # ----------------------------------------------------------------------------
        self.feature_1816_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=BleProPrepairing.FEATURE_ID)

        # Get the feature under test
        self.feature_1816 = BleProPrepairingFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.BLE_PRO_PREPAIRING))

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable Manufacturing Feature")
        # ---------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_program_nvs and self.memory_manager is not None:
                # --------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # --------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
            # end if
        # end with

        super().tearDown()
    # end def tearDown
# end class BleProPrePairingTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
