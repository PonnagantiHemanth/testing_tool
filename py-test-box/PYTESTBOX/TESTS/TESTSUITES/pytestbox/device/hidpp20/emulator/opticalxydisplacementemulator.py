#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
""" @package pytestbox.hid.emulator.opticalxydisplacementemulator

@brief  Validates Optical XY Displacement Emulator

@author Stanislas Cottard

@date   2019/07/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.basetest import BaseTestCase
from pyharness.selector import features
from pyharness.selector import services
from pyharness.extensions import level
from pyhid.hid.hidmouse import HidMouse

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class OpticalXyDisplacementEmulatorTestCase(BaseTestCase):
    """
    Validates Optical XY displacement emulator
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(OpticalXyDisplacementEmulatorTestCase, self).setUp()
    # end def setUp

    @features('PeripheralEmulation')
    @level('Business')
    @services('OpticalSensor')
    def test_xy_displacement(self):
        """
        @tc_synopsis Validates XY displacement
        """
        xy_displacements = [(5, 5), (5, -5), (-5, 5), (-5, -5)]
        for (dx, dy) in xy_displacements:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send XY displacement, dx = ' + str(dx) + ' and dy = ' + str(dy))
            # ---------------------------------------------------------------------------
            self.motion_emulator.xy_motion(dx=dx, dy=dy)
            self.motion_emulator.commit_actions()
            self.motion_emulator.prepare_sequence()

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Receive HID mouse XY displacement')
            # ---------------------------------------------------------------------------
            hid_packet = self.getMessage(queue=self.hidDispatcher.hid_message_queue,
                                         class_type=HidMouse)
            self.logTrace('HidMouse: %s\n' % str(hid_packet))
            for field in hid_packet.FIELDS:
                fid = field.getFid()
                if field.name == 'x':
                    self.assertEquals(expected=dx,
                                      obtained=hid_packet.get_absolute_value(fid),
                                      msg="The dx parameter differs from the one expected")
                elif field.name == 'y':
                    self.assertEquals(expected=dy,
                                      obtained=hid_packet.get_absolute_value(fid),
                                      msg="The dy parameter differs from the one expected")

        self.testCaseChecked("FNT_XY_DISPLACEMENT_0001")
    # end def test_xy_displacement
# end class OpticalXyDisplacementEmulatorTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
