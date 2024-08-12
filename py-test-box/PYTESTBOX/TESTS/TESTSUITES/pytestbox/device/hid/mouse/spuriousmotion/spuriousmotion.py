#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.spuriousmotion.spuriousmotion
:brief: Hid mouse spurious motion filtering algorithm test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/04/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from dataclasses import field

from math import floor

from pyraspi.services.kosmos.module.optemu_sensors import E7792Module
from pyraspi.services.kosmos.module.optemu_sensors import Paw3266Module
from pyraspi.services.kosmos.module.optemu_sensors import Pmw3816Module
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
@dataclass
class FwSensorParam:
    """
    Optical Sensor related settings in DUT firmware.
    TODO: Ideally, those constants should be defined outside of this class.
    """
    sensor_POLL_TIME_MS: float  # ms, sensor polling period
    sensor_REST_3_MODE_TIME_SEC: float  # s, sensor time to Rest3 mode

    sensor_SPURIOUS_MOTION_FLTR_PERIOD_MS: int = 32  # ms, time before filter reactivates
    sensor_SPURIOUS_MOTION_FLTR_MAX_CNT: int = field(init=False)  # sensor polling count before filter reactivates

    dbg_fw: bool = True
    dbg_sensor_REST_3_MODE_TIME_SEC: float = 30.  # 30 seconds by default

    def __post_init__(self):
        """
        Init derived settings.
        """
        self.sensor_SPURIOUS_MOTION_FLTR_MAX_CNT = \
            floor(self.sensor_SPURIOUS_MOTION_FLTR_PERIOD_MS / self.sensor_POLL_TIME_MS)
    # end def __post_init__

    @property
    def rest3_mode_time_sec(self):
        """
        Return Sensor Rest3 mode time, in seconds.
        For debug firmware (non-prod), the Rest3 time is shortened for faster validation tests.

        :return: Sensor Rest3 mode time
        :rtype: ``float``
        """
        return self.dbg_sensor_REST_3_MODE_TIME_SEC if self.dbg_fw else self.sensor_REST_3_MODE_TIME_SEC
    # end def rest3_mode_time_sec

    @property
    def poll_freq_hz(self):
        """
        Return Sensor polling frequency, in Hertz.

        :return: Sensor polling frequency
        :rtype: ``float``
        """
        return 1000/self.sensor_POLL_TIME_MS
    # end def poll_freq_hz

    @property
    def smf_max_count(self):
        """
        Return Spurious Motion Filter Algorithm polling count before filter reactivate itself.

        :return: Spurious Motion Filter Algorithm max polling count
        :rtype: ``int``
        """
        return self.sensor_SPURIOUS_MOTION_FLTR_MAX_CNT
    # end def smf_max_count
# end class FwSensorParam


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpuriousMotionTestCase(BaseTestCase):
    """
    Validate mouse spurious motion filtering algorithm requirements
    """
    post_requisite_unplug_usb_charging_cable: bool
    fw_sensor_param: FwSensorParam

    def setUp(self):
        """
        Set up module test class
        """
        super().setUp()
        self.post_requisite_unplug_usb_charging_cable = False

        # Workaround: define NPI-specific settings, based on the Optical Sensor Emulator type.
        # TODO: Ideally, those constants should be defined outside of this class.
        if isinstance(self.motion_emulator.module, E7792Module):
            self.fw_sensor_param = FwSensorParam(sensor_POLL_TIME_MS=4,
                                                 sensor_REST_3_MODE_TIME_SEC=610)  # Timings obtained from fw code
        elif isinstance(self.motion_emulator.module, Paw3266Module):
            self.fw_sensor_param = FwSensorParam(sensor_POLL_TIME_MS=8,
                                                 sensor_REST_3_MODE_TIME_SEC=310)  # Timings obtained from fw code
        elif isinstance(self.motion_emulator.module, Pmw3816Module):
            if self.getFeatures().PRODUCT.F_ProductReference in ['RBM22', 'RBM24']:
                self.skipTest("Spurious Motion Filter Algorithm is not implemented on Liza or Bardi mice "
                              "based on PMW3816 / PMW3826 optical sensors.")
            else:
                self.fw_sensor_param = FwSensorParam(sensor_POLL_TIME_MS=8,
                                                     sensor_REST_3_MODE_TIME_SEC=310)  # Timings obtained from fw code
            # end if
        else:
            raise NotImplementedError(self.motion_emulator.module)
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_unplug_usb_charging_cable:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Stop device charging")
                # ------------------------------------------------------------------------------------------------------
                if self.power_supply_emulator is not None:
                    self.power_supply_emulator.recharge(enable=False)
                # end if
                self.device.turn_off_usb_charging_cable()
                self.post_requisite_unplug_usb_charging_cable = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown
# end class SpuriousMotionTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
