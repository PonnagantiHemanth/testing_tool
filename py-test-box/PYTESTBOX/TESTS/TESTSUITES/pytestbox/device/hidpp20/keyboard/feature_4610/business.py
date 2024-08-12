#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4610.business
:brief: HID++ 2.0 ``MultiRoller`` business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HidMouse
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.multiroller import RollerMode
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.multirollerutils import MultiRollerTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4610.multiroller import MultiRollerTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRollerBusinessTestCase(MultiRollerTestCase):
    """
    Validate ``MultiRoller`` business test cases
    """

    @features("Feature4610")
    @level('Business', 'SmokeTests')
    @services('MainWheel')
    def test_scroll_roller_less_than_a_ratchet(self):
        """
        In divert mode, validate the RotationEvent is received if the user moves the roller less than a ratchet
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Scroll the roller with minimum movement (1 count increment)")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the RotationEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            rotation_event = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self)
            self.assertNotNone(
                obtained=rotation_event,
                msg='The RotationEvent is not received after moving the roller with minimum movement (1 count)')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_4610_0001", _AUTHOR)
    # end def test_scroll_roller_less_than_a_ratchet

    @features("Feature4610")
    @level("Business")
    @services('MainWheel')
    def test_scroll_roller_with_a_ratchet(self):
        """
        In divert mode, validate the RotationEvent is received if the user moves the roller with a ratchet
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Scroll the roller with a ratchet")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller emulator

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the RotationEvent is received")
            # ----------------------------------------------------------------------------------------------------------
            rotation_event = MultiRollerTestUtils.HIDppHelper.rotation_event(test_case=self)
            self.assertNotNone(
                obtained=rotation_event,
                msg='The RotationEvent is not received after moving the roller with a ratchet')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_4610_0002", _AUTHOR)
    # end def test_scroll_roller_with_a_ratchet

    @features("Feature4610")
    @level("Business")
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    @services('MainWheel')
    def test_scroll_diverted_roller_when_pressing_fn_key(self):
        """
        In divert mode, validate the FW should send reports as OOB when user is pressing FN and rolling roller
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press and hold the FN key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over roller in range({self.config.F_NumRollers}):")
        # --------------------------------------------------------------------------------------------------------------
        for roller_index in range(self.config.F_NumRollers):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send SetMode request with roller_id={roller_index}, mode={RollerMode.DIVERT!s}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode(test_case=self, roller_id=roller_index,
                                                      divert=RollerMode.DIVERT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Scroll the roller with random direction and movement")
            # ----------------------------------------------------------------------------------------------------------
            # TODO - Implement roller index

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the HID/VolumeUpDown/Dial report is received")
            # ----------------------------------------------------------------------------------------------------------
            response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                             class_type=HidMouse, allow_no_message=True)
            self.assertNotNone(
                obtained=response,
                msg=f'No HID report is received when the roller[{roller_index}] is scrolled in divert '
                    'and FN is pressed')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Release the FN key")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

        self.testCaseChecked("BUS_4610_0003", _AUTHOR)
    # end def test_scroll_diverted_roller_when_pressing_fn_key
# end class MultiRollerBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
