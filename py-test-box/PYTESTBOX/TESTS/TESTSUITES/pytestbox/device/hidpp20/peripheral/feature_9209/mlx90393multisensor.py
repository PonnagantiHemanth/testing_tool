#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------------------------------------
# Python Test Box
# -----------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_9209
:brief: Validate HID++ 2.0 MLX Multisensor test case
:author: Ganesh Thiraviam <gthiraviam@logitech.com>
:date: 2021/03/10
"""
# -----------------------------------------------------------------------------------------------------------
# imports
# -----------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MLX90393MultiSensor
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MLX90393MultiSensorFactory
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.basetest import DeviceBaseTestCase

# -----------------------------------------------------------------------------------------------------------
# constants
# -----------------------------------------------------------------------------------------------------------
LogHelper = CommonBaseTestUtils.LogHelper


# -----------------------------------------------------------------------------------------------------------
# implementation
# -----------------------------------------------------------------------------------------------------------
class Mlx90393MultiSensorTestCase(DeviceBaseTestCase):
    """
    Validates MLX 90393 MultiSensor TestCases
    """
    def __init__(self, method_name="runTest"):
        """
        Constructor
        :param method_name: name of the method
        :type method_name: ``str``
        """
        super().__init__(methodName=method_name)
        self.post_requisite_reload_nvs = False
        self.feature_9209_index = None
        self.feature_9209 = None
        self.product = None
    # end def __init__

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

        # --------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x9209)")
        # --------------------------------------------------------------
        self.feature_9209_index = self.updateFeatureMapping(feature_id=MLX90393MultiSensor.FEATURE_ID)

        # ---------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # ---------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # Get the feature under test
        self.feature_9209 = MLX90393MultiSensorFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.PERIPHERAL.MLX_90393_MULTI_SENSOR))

        self.product = self.f.PRODUCT.FEATURES.PERIPHERAL.MLX_90393_MULTI_SENSOR
    # end def setUp

    def tearDown(self):
        """
        Handles post requisites
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
# end class Mlx90393MultiSensorTestCase
