#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.button.business
:brief: Hid mouse button business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/01/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.emulatorinterfaces import MAKE, BREAK, ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.mouse.button.button import ButtonTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ButtonBusinessTestCase(ButtonTestCase):
    """
    Validate Mouse button business TestCases
    """

    @features('Mice')
    @level('Business', 'SmokeTests')
    @services("RequiredKeys", (KEY_ID.LEFT_BUTTON,))
    @services('ButtonPressed')
    def test_left_click(self):
        """
        Verify various HID reports linked to the Left Click button
        """
        self.press_single_button(key_id=KEY_ID.LEFT_BUTTON)

        self.press_multiple_buttons(key_id=KEY_ID.LEFT_BUTTON)

        self.testCaseChecked("BUS_HID_MSE_BUT_0001")
    # end def test_left_click

    @features('Mice')
    @level('Business')
    @services("RequiredKeys", (KEY_ID.RIGHT_BUTTON,))
    @services('ButtonPressed')
    def test_right_click(self):
        """
        Verify various HID reports linked to the Right Click button
        """
        self.press_single_button(key_id=KEY_ID.RIGHT_BUTTON)

        self.press_multiple_buttons(key_id=KEY_ID.RIGHT_BUTTON)

        self.testCaseChecked("BUS_HID_MSE_BUT_0002")
    # end def test_right_click

    @features('Mice')
    @level('Business')
    @services("RequiredKeys", (KEY_ID.MIDDLE_BUTTON,))
    @services('ButtonPressed')
    def test_middle_click(self):
        """
        Verify various HID reports linked to the Middle Click button
        """
        self.press_single_button(key_id=KEY_ID.MIDDLE_BUTTON)

        self.press_multiple_buttons(key_id=KEY_ID.MIDDLE_BUTTON)

        self.testCaseChecked("BUS_HID_MSE_BUT_0003")
    # end def test_middle_click

    @features('Mice')
    @level('Business')
    @services("RequiredKeys", (KEY_ID.BACK_BUTTON,))
    @services('ButtonPressed')
    def test_back_button(self):
        """
        Verify various HID reports linked to the Backward button
        """
        self.press_single_button(key_id=KEY_ID.BACK_BUTTON)

        self.press_multiple_buttons(key_id=KEY_ID.BACK_BUTTON)

        self.testCaseChecked("BUS_HID_MSE_BUT_0004")
    # end def test_back_button

    @features('Mice')
    @level('Business')
    @services("RequiredKeys", (KEY_ID.FORWARD_BUTTON,))
    @services('ButtonPressed')
    def test_forward_button(self):
        """
        Verify various HID reports linked to the Forward button
        """
        self.press_single_button(key_id=KEY_ID.FORWARD_BUTTON)

        self.press_multiple_buttons(key_id=KEY_ID.FORWARD_BUTTON)

        self.testCaseChecked("BUS_HID_MSE_BUT_0005")
    # end def test_forward_button

    @features('Mice')
    @features('GamingDevice')
    @level('Business')
    @services("RequiredKeys", (KEY_ID.BUTTON_6,))
    @services('ButtonPressed')
    def test_button_6(self):
        """
        Verify various HID reports linked to the button number 6
        """
        self.press_single_button(key_id=KEY_ID.BUTTON_6)

        self.press_multiple_buttons(key_id=KEY_ID.BUTTON_6)

        self.testCaseChecked("BUS_HID_MSE_BUT_0006")
    # end def test_button_6

    @features('Mice')
    @features('GamingDevice')
    @level('Business')
    @services("RequiredKeys", (KEY_ID.BUTTON_7,))
    @services('ButtonPressed')
    def test_button_7(self):
        """
        Verify various HID reports linked to the button number 7
        """
        self.press_single_button(key_id=KEY_ID.BUTTON_7)

        self.press_multiple_buttons(key_id=KEY_ID.BUTTON_7)

        self.testCaseChecked("BUS_HID_MSE_BUT_0007")
    # end def test_button_7
# end class ButtonBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
