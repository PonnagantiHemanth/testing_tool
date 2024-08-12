#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.layout.business
:brief: Hid Keyboard Layout business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/07/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.keyboardemulator import KeyboardMixin
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.layoututils import LayoutTestUtils as Utils
from pytestbox.device.hid.keyboard.layout.layout import LayoutTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class LayoutBusinessTestCase(LayoutTestCase):
    """
    Validate Keyboard Layout business TestCases
    """

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business', 'SmokeTests')
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_uk_layout_first_5_keys(self):
        """
        Check the first 5 keys starting from row 0 returned the correct key code when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_key_code(group_count=self.NUMBER_OF_KEYS)

        self.testCaseChecked("BUS_LAYT_0001")
    # end def test_uk_layout_first_5_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_KEY,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_fn_key(self):
        """
        Press on Fn-Key then check if the F-keys returned the correct key code when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_fn_key()

        self.testCaseChecked("BUS_LAYT_0002")
    # end def test_uk_layout_fn_key

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_LOCK,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_fn_lock_key(self):
        """
        Emulate a keystrocke on the Fn_lock key then check that F-Keys returned the correct key code
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_fn_lock_key()

        self.testCaseChecked("BUS_LAYT_0003")
    # end def test_uk_layout_fn_lock_key

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_jpn_layout_first_5_keys(self):
        """
        Check the first 5 keys starting from row 0 returned the correct key code when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_key_code(group_count=self.NUMBER_OF_KEYS)

        self.testCaseChecked("BUS_LAYT_0011")
    # end def test_jpn_layout_first_5_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_KEY,), KeyboardMixin.LAYOUT.JIS_109_KEY)
    @services('Debugger')
    def test_jpn_layout_fn_key(self):
        """
        Press on Fn-Key then check if the F-keys returned the correct key code when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_fn_key()

        self.testCaseChecked("BUS_LAYT_0012")
    # end def test_jpn_layout_fn_key

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_LOCK,), KeyboardMixin.LAYOUT.JIS_109_KEY)
    @services('Debugger')
    def test_jpn_layout_fn_lock_key(self):
        """
        Emulate a keystrocke on the Fn_lock key then check that F-Keys returned the correct key code
        when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_fn_lock_key()

        self.testCaseChecked("BUS_LAYT_0013")
    # end def test_jpn_layout_fn_lock_key

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_iso_104_layout_first_5_keys(self):
        """
        Check the first 5 keys starting from row 0 returned the correct key code when the ISO 104 layout is
        configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to ISO 104 keys")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.US_INTERNATIONAL_104_KEYS)

        self._test_key_code(group_count=self.NUMBER_OF_KEYS)

        self.testCaseChecked("BUS_LAYT_0021")
    # end def test_iso_104_layout_first_5_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_KEY,), KeyboardMixin.LAYOUT.ISO_104_KEY)
    @services('Debugger')
    def test_iso_104_layout_fn_key(self):
        """
        Press on Fn-Key then check if the F-keys returned the correct key code when the ISO 104 layout is
        configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to ISO 104 keys")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.US_INTERNATIONAL_104_KEYS)

        self._test_fn_key()

        self.testCaseChecked("BUS_LAYT_0022")
    # end def test_iso_104_layout_fn_key

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_iso_107_layout_first_5_keys(self):
        """
        Check the first 5 keys starting from row 0 returned the correct key code when the brazilian ISP 107 layout is
        configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to BRA")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.PORTUGUESE_BRAZILIAN)

        self._test_key_code(group_count=self.NUMBER_OF_KEYS)

        self.testCaseChecked("BUS_LAYT_0031")
    # end def test_iso_107_layout_first_5_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Business')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_KEY,), KeyboardMixin.LAYOUT.ISO_107_KEY)
    @services('Debugger')
    def test_iso_107_layout_fn_key(self):
        """
        Press on Fn-Key then check if the F-keys returned the correct key code when the brazilian ISP 107 layout is
        configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to BRA")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.PORTUGUESE_BRAZILIAN)

        self._test_fn_key()

        self.testCaseChecked("BUS_LAYT_0032")
    # end def test_iso_107_layout_fn_key

# end class LayoutBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
