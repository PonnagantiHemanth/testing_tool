#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
""" @package pytestbox.hid.emulator.buttonstimuliemulator

@brief  Validates Button Stimuli Emulator

@author Stanislas Cottard

@date   2019/07/03
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hiddata import HidData
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import BaseTestCase
from time import sleep
import unittest

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class ButtonStimuliEmulatorTestCase(BaseTestCase):
    """
    Validates XY displacement notifications TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super(ButtonStimuliEmulatorTestCase, self).setUp()
    # end def setUp

    @features('PeripheralEmulation')
    @level('Business')
    @services('ButtonPressed')
    def test_button_stimuli(self):
        """
        @tc_synopsis Validates all possible button stimuli
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over all CIDs possible on the device use to test the emulator')
        # ---------------------------------------------------------------------------
        for cid in self.button_stimuli_emulator.get_accessible_cid_list():
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send key press and release for CID = ' + str(hex(cid)))
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(cid)
            sleep(.1)
            self.button_stimuli_emulator.key_release(cid)
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Receive HID mouse key pressed and released one by one')
            # ---------------------------------------------------------------------------
            self.check_button_stimulus_response(cid=cid,
                                                make_or_break=True)
            self.check_button_stimulus_response(cid=cid,
                                                make_or_break=False)
            sleep(.5)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop end')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_BUTTON_STIMULI_0001")
    # end def test_button_stimuli

    @features('PeripheralEmulation')
    @level('Stress')
    @services('ButtonPressed')
    @unittest.skip("Very long")
    def test_stress_button_stimuli(self):
        """
        @tc_synopsis Stress test over button stimuli
        """
        # Stress test
        cid_list = self.button_stimuli_emulator.get_accessible_cid_list()
        number_of_stress_loops = 100
        success_rate = 0
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over a large number (' + str(number_of_stress_loops) + ') of complete button '
                       'stimuli tests')
        # ---------------------------------------------------------------------------
        for i in range(number_of_stress_loops):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop number ' + str(i) + ' over all CIDs possible on the device use to test the '
                           'emulator')
            # ---------------------------------------------------------------------------
            for cid in cid_list:
                # noinspection PyBroadException
                try:
                    # ---------------------------------------------------------------------------
                    self.logTitle2('Test Step 1: Send key press and release for CID = ' + str(hex(cid)))
                    # ---------------------------------------------------------------------------
                    self.button_stimuli_emulator.key_press(cid)
                    sleep(.1)
                    self.button_stimuli_emulator.key_release(cid)
                    # ---------------------------------------------------------------------------
                    self.logTitle2('Test Check 1: Receive HID mouse key pressed and released one by one')
                    # ---------------------------------------------------------------------------
                    make_success = self.check_button_stimulus_response(cid=cid,
                                                                       make_or_break=True,
                                                                       non_blocking=True)
                    break_success = self.check_button_stimulus_response(cid=cid,
                                                                        make_or_break=False,
                                                                        non_blocking=True)
                    sleep(.5)
                    success_rate += make_success & break_success
                except:
                    self.log_traceback_as_warning()
                # end try
            # end for
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Loop end')
            # ---------------------------------------------------------------------------
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop end')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=number_of_stress_loops*len(cid_list),
                         obtained=success_rate,
                         msg="Some stimuli failed")

        self.testCaseChecked("FNT_BUTTON_STIMULI_0002")
    # end def test_stress_button_stimuli

    def check_button_stimulus_response(self, cid, make_or_break, non_blocking=False):
        """
        Check the expected response for a button stimulus.

        @param  cid           [in] (int)  Button CID
        @param  make_or_break [in] (bool) If true check for a make, false check for a break
        @param  non_blocking  [in] (bool) Block or not when error or exception
        """
        if make_or_break:
            table_key = MAKE
        else:
            table_key = BREAK
        # end if

        key_id = CID_TO_KEY_ID_MAP[cid]
        # Button stimuli emulator uses first available variant
        variant = next(iter(HidData.KEY_ID_TO_HID_MAP[key_id]))
        responses_class = HidData.KEY_ID_TO_HID_MAP[key_id][variant][table_key]['Responses_class']
        fields_name = HidData.KEY_ID_TO_HID_MAP[key_id][variant][table_key]['Fields_name']
        fields_value = HidData.KEY_ID_TO_HID_MAP[key_id][variant][table_key]['Fields_value']

        success = True
        for i in range(len(responses_class)):
            # noinspection PyBroadException
            try:
                hid_packet = self.getMessage(queue=self.hidDispatcher.hid_message_queue,
                                             class_type=responses_class[i])
                self.logTrace('%s: %s\n' % (responses_class[i].__name__, str(hid_packet)))
                for j in range(len(fields_name[i])):
                    for field in hid_packet.FIELDS:
                        fid = field.getFid()
                        if field.name == fields_name[i][j]:
                            if isinstance(hid_packet.getValue(fid), HexList):
                                value_obtain = hid_packet.getValue(fid).toLong()
                            else:
                                value_obtain = hid_packet.getValue(fid)
                            if non_blocking:
                                if fields_value[i][j] != value_obtain:
                                    self.logTrace(msg=f"The {fields_name[i][j]} parameter differs from the expected "
                                                      f"one")
                                    success = False
                                # end if
                            else:
                                self.assertEquals(expected=fields_value[i][j],
                                                  obtained=value_obtain,
                                                  msg=f"The {fields_name[i][j]} parameter differs from the expected "
                                                      f"one")
                            # end if
            except:
                if non_blocking:
                    self.log_traceback_as_warning()
                    success = False
                else:
                    raise
                # end if
            # end try
        # end for
        return success
    # end def check_stimulus_response
# end class ButtonStimuliEmulatorTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
