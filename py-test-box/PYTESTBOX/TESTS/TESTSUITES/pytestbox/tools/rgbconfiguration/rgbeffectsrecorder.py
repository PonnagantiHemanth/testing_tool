#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.tools.rgbconfiguration.rgbeffectsrecorder
:brief: RGB effects recorder tool
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/07/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyraspi.services.kosmos.config.rgbconfiguration import GET_RGB_CONFIGURATION_BY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.hidpp20.gaming.feature_8071.functionality import SHUTDOWN_DURATION_MARGIN
from pytestbox.tools.rgbconfiguration.rgbconfiguration import RGBConfigurationTools


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RgbEffectsRecorder(RGBConfigurationTools):
    """
    RGB configuration tools to record OOB RGB effect (startup, shutdown, active and passive) with Kosmos RGB spy
    """
    @features("Feature8071")
    @level('Tools')
    @services("RGBMonitoring")
    def test_record_shutdown_effect(self):
        """
        Use to record the reference shutdown effect in order to detect the immersive lightning state machine
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_sw_control(
            self,
            get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
            sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set Disable effect and wait 1s to be sure no effect is played')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.set_disabled_effect(
            self,
            cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
            persistence=RGBEffectsTestUtils.Persistence.VOLATILE)
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait 5 seconds')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_off()
        sleep(5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Save shutdown RGB effect record')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.save_record(self, file_name='oob_rgb_shutdown', save_timestamp=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_on()
    # end def test_record_shutdown_effect

    @features("Feature8071")
    @level('Tools')
    @services("RGBMonitoring")
    def test_record_startup_effect(self):
        """
        Use to record the reference startup effect in order to detect the immersive lightning state machine
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]
        shutdown_duration = rgb_configuration.SHUTDOWN_DURATION

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off the DUT and wait the necessary duration to be sure no more effect is '
                                 'played')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_off()
        sleep(shutdown_duration + SHUTDOWN_DURATION_MARGIN)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on the DUT and wait 4 seconds')
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.power_on()
        sleep(4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Save startup RGB effect record')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.save_record(self, file_name='oob_rgb_start_up', save_timestamp=True)
    # end def _test_record_startup_effect

    @features("Feature8071")
    @level('Tools')
    @services("RGBMonitoring")
    def test_record_active_effect(self):
        """
        Use to record the reference active effect in order to detect the immersive lightning state machine
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_sw_control(
            self,
            get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
            sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set Disable effect and wait 1s to be sure no effect is played')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.set_disabled_effect(
            self,
            cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
            persistence=RGBEffectsTestUtils.Persistence.VOLATILE)
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set active effect on Multi-cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.set_rgb_cluster_effect_with_default_values(
            self,
            effect_id=rgb_configuration.ACTIVE_EFFECT_ID,
            cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
            persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 4 seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(4)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Save active RGB effect record')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.save_record(self, file_name='oob_rgb_active', save_timestamp=True)
    # end def test_record_active_effect

    @features("Feature8071")
    @level('Tools')
    @services("RGBMonitoring")
    def test_record_passive_effect(self):
        """
        Use to record the reference passive effect in order to detect the immersive lightning state machine
        """
        fw_id = self.f.PRODUCT.F_ProductReference
        rgb_configuration = GET_RGB_CONFIGURATION_BY_ID[fw_id]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable SW Control of RGB Cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_sw_control(
            self,
            get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
            sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set Disable effect and wait 1s to be sure no effect is played')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.set_disabled_effect(
            self,
            cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
            persistence=RGBEffectsTestUtils.Persistence.VOLATILE)
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set passive effect on Multi-cluster')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.set_rgb_cluster_effect_with_default_values(
            self,
            effect_id=rgb_configuration.PASSIVE_EFFECT_ID,
            cluster_index=RGBEffectsTestUtils.RGBClusterId.MULTI_CLUSTER,
            persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop RGB effect monitoring after 4 seconds')
        # --------------------------------------------------------------------------------------------------------------
        sleep(4)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Save passive RGB effect record')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.save_record(self, file_name='oob_rgb_passive', save_timestamp=True)
    # end def test_record_passive_effect
# end class RgbEffectsRecorder

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
