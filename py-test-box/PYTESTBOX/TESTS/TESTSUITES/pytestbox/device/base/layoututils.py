#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.layoututils
:brief: Helpers for ``Layout`` feature
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/03/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.hidkeyboardbitmap import HidKeyboardBitmap
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pylibrary.mcu.kbdmasktablechunk import KbdMaskTableChunk
from pylibrary.tools.hexlist import HexList
from pyraspi.services.keyboardemulator import KeyboardMixin
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.opticalswitchesutils import OpticalSwitchesTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LayoutTestUtils(CommonBaseTestUtils):
    """
    Test utils class for layout feature.
    """
    @classmethod
    def select_layout(cls, test_case, layout=KeyboardInternationalLayouts.LAYOUT.UNKNOWN):
        """
        Change the keyboard international layout to match the device configuration in NVS

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param layout: keyboard international layout type
        :type layout: ``KeyboardInternationalLayouts.LAYOUT``
        """
        if layout in [KeyboardInternationalLayouts.LAYOUT.US_INTERNATIONAL_104_KEYS,
                      KeyboardInternationalLayouts.LAYOUT.RUSSIAN]:
            physical_layout = KeyboardMixin.LAYOUT.ISO_104_KEY
        elif layout == KeyboardInternationalLayouts.LAYOUT.JAPANESE:
            physical_layout = KeyboardMixin.LAYOUT.JIS_109_KEY
        elif layout == KeyboardInternationalLayouts.LAYOUT.PORTUGUESE_BRAZILIAN:
            physical_layout = KeyboardMixin.LAYOUT.ISO_107_KEY
        elif KeyboardInternationalLayouts.LAYOUT.US_INTERNATIONAL_105_KEYS <= layout <= \
                KeyboardInternationalLayouts.LAYOUT.PAN_NORDIC or \
                KeyboardInternationalLayouts.LAYOUT.SWISS <= layout <= KeyboardInternationalLayouts.LAYOUT.KAZAKH:
            physical_layout = KeyboardMixin.LAYOUT.ISO_105_KEY
        else:
            physical_layout = KeyboardMixin.LAYOUT.DEFAULT
        # end if

        if test_case.f.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES.F_Enabled:
            layout_string_name = KeyboardMixin.LAYOUT.get_string_name(physical_layout)
            if layout_string_name in test_case.f.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES.F_SupportedKeyLayout:
                kbd_mask_tables = test_case.config_manager.get_feature(
                    feature_id=ConfigurationManager.ID.OPTICAL_SWITCHES_KBD_MASK_TABLE)
                kbd_mask_table = KbdMaskTableChunk(
                    kbd_mask_tables[test_case.f.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES.F_SupportedKeyLayout.index(
                        layout_string_name)])
                OpticalSwitchesTestUtils.NvsHelper.add_kbd_mask_table(test_case=test_case,
                                                                      kbd_mask_table=HexList(kbd_mask_table))
            # end if
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=test_case,
                                   text=f"Map the Keyboard International Layout {layout} into physical layout "
                                        f"{physical_layout} and update the chunk in NVS")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.NvsHelper.write_property_id(
            test_case=test_case, property_id=ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT,
            data=HexList(layout))
        test_case.button_stimuli_emulator.select_layout(layout_type=physical_layout)

        # Workaround
        # Keep the keyboard in run mode to prevent lost the first pressed key after change key layout by debugger
        test_case.button_stimuli_emulator.user_action()
        for _ in range(2):
            ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                  class_type=(HidKeyboard, HidKeyboardBitmap))
        # end for
    # end def select_layout
# end class LayoutTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
