#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_18b0.business
:brief: HID++ 2.0 ``StaticMonitorMode`` business test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import EnhancedKeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardModeEvent
from pyhid.hidpp.features.common.staticmonitormode import KeyboardWithLargerMatrixModeEvent
from pyhid.hidpp.features.common.staticmonitormode import MouseModeEvent
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorMode
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pyraspi.services.kosmos.config.buttonlayout import BUTTON_LAYOUT_BY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.staticmonitormodeutils import StaticMonitorModeTestUtils
from pytestbox.device.hidpp20.common.feature_18b0.staticmonitormode import StaticMonitorModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_CHECK_MONITOR_MODE_EVENT_GENERATED = "Check MonitorModeEvent is generated"
_CHECK_MONITOR_MODE_EVENT_NOT_GENERATED = "Check MonitorModeEvent is not generated"
_CHECK_MONITORMODE_RESPONSE = "Check SetMonitorModeResponse fields"
_END_TEST_LOOP = "End Test Loop"
_REBOOT_DUT = "Reboot DUT"
_SET_MONITOR_MODE_0 = "Send SetMonitorMode request with mode: 0 (OFF)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
@bugtracker.class_decorator('MonitorMode_BadRowColValues')
class StaticMonitorModeBusinessTestCase(StaticMonitorModeTestCase):
    """
    Validate ``StaticMonitorMode`` business test cases
    """

    @features("Feature18B0")
    @features("KeyboardMode")
    @level('Business', 'SmokeTests')
    @services("HardwareReset")
    def test_kbd_set_monitor_mode_1_and_reboot_using_hardware_reset(self):
        """
        Validate impact on device reboot (KBD)

        [0] setMonitorMode(mode)

        Require PowerSupply
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        mode_1 = StaticMonitorMode.KBD_ON
        row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 1")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code": (checker.check_row_col_code, row_col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
            }
        )
        checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code": (checker.check_row_col_code, row_col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
            }
        )
        checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0001", _AUTHOR)
    # end def test_kbd_set_monitor_mode_1_and_reboot_using_hardware_reset

    @features("Feature18B0")
    @features("KeyboardMode")
    @features("Feature1802")
    @level("Business")
    def test_kbd_set_monitor_mode_1_and_reboot_using_feature(self):
        """
        Validate impact on device reboot (KBD)

        [0] setMonitorMode(mode)

        Require 0x1802
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        mode_1 = StaticMonitorMode.KBD_ON
        key_row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 1")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code": (checker.check_row_col_code, key_row_col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
            }
        )
        checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
        check_map.update(
            {
                "row_col_code": (checker.check_row_col_code, key_row_col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
            }
        )
        checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        StaticMonitorModeTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean Battery Status Event and Wireless Device Status Broadcast Event")
        # --------------------------------------------------------------------------------------------------------------
        self.cleanup_battery_event_from_queue()
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent, timeout=.5, allow_no_message=True, check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0002", _AUTHOR)
    # end def test_kbd_set_monitor_mode_1_and_reboot_using_feature

    @features("Feature18B0")
    @features("Mice")
    @level("Business")
    @services("HardwareReset")
    @services("RequiredKeys", (KEY_ID.LEFT_BUTTON,))
    def test_mouse_set_monitor_mode_2_and_reboot_using_hardware_reset(self):
        """
        Validate impact on device reboot (mouse)

        [0] setMonitorMode(mode)

        Require PowerSupply
        """
        button = KEY_ID.LEFT_BUTTON
        mode_2 = StaticMonitorMode.MOUSE_ON
        switch = HexList("00" * (MouseModeEvent.LEN.SWITCHES // 8))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {button.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {button.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 2")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {button.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=button)
        switch = StaticMonitorModeTestUtils.update_switch(switch, button, set_bit=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.MouseModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"switches": (checker.check_switches, switch)})
        checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {button.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=button)
        switch = StaticMonitorModeTestUtils.update_switch(switch, button, clear_bit=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.MouseModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"switches": (checker.check_switches, switch)})
        checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {button.name} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {button.name} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0003", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_and_reboot_using_hardware_reset

    @features("Feature18B0")
    @features("Mice")
    @features("Feature1802")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.LEFT_BUTTON,))
    def test_mouse_set_monitor_mode_2_and_reboot_using_feature(self):
        """
        Validate impact on device reboot (mouse)

        [0] setMonitorMode(mode)

        Require 0x1802
        """
        button = KEY_ID.LEFT_BUTTON
        mode_2 = StaticMonitorMode.MOUSE_ON
        switch = HexList("00" * (MouseModeEvent.LEN.SWITCHES // 8))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {button.name} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {button.name} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 2")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {button.name} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=button)
        switch = StaticMonitorModeTestUtils.update_switch(switch, button, set_bit=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.MouseModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"switches": (checker.check_switches, switch)})
        checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {button.name} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=button)
        switch = StaticMonitorModeTestUtils.update_switch(switch, button, clear_bit=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.MouseModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"switches": (checker.check_switches, switch)})
        checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        StaticMonitorModeTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean Battery Status Event and Wireless Device Status Broadcast Event")
        # --------------------------------------------------------------------------------------------------------------
        self.cleanup_battery_event_from_queue()
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent, timeout=.5, allow_no_message=True,
            check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {button.name} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {button.name} button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=button)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0004", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_and_reboot_using_feature

    @features("Feature18B0")
    @features("EnhancedKeyboardMode")
    @level("Business")
    @services("HardwareReset")
    def test_kbd_set_monitor_mode_3_and_reboot_using_hardware_reset(self):
        """
        Validate impact on device reboot (Enhanced KBD)

        [0] setMonitorMode(mode)

        Require PowerSupply
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        mode_3 = StaticMonitorMode.ENHANCED_KBD_ON
        key_row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 3")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code_0": (checker.check_row_col_code_0, key_row_col_code)
            }
        )
        checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0005", _AUTHOR)
    # end def test_kbd_set_monitor_mode_3_and_reboot_using_hardware_reset

    @features("Feature18B0")
    @features("EnhancedKeyboardMode")
    @features("Feature1802")
    @level("Business")
    def test_kbd_set_monitor_mode_3_and_reboot_using_feature(self):
        """
        Validate impact on device reboot (Enhanced KBD)

        [0] setMonitorMode(mode)

        Require 0x1802
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        mode_3 = StaticMonitorMode.ENHANCED_KBD_ON
        key_row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 3")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_col_code_0": (checker.check_row_col_code_0, key_row_col_code)
            }
        )
        checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_keyboard_mode_event = EnhancedKeyboardModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardModeEventChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, enhanced_keyboard_mode_event, EnhancedKeyboardModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        StaticMonitorModeTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean Battery Status Event and Wireless Device Status Broadcast Event")
        # --------------------------------------------------------------------------------------------------------------
        self.cleanup_battery_event_from_queue()
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent, timeout=.5, allow_no_message=True,
            check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0006", _AUTHOR)
    # end def test_kbd_set_monitor_mode_3_and_reboot_using_feature

    @features("Feature18B0v1")
    @features("KeyboardWithLargerMatrixMode")
    @level("Business")
    @services("HardwareReset")
    def test_kbd_set_monitor_mode_4_and_reboot_using_hardware_reset(self):
        """
        Validate impact on device reboot (KBD with large matrix)

        [0] setMonitorMode(mode)

        Require PowerSupply
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        mode_4 = StaticMonitorMode.KBD_LARGER_MATRIX
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 4")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code": (checker.check_row_code, row_code),
                "col_code": (checker.check_col_code, col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
            }
        )
        checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code": (checker.check_row_code, row_code),
                "col_code": (checker.check_col_code, col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
            }
        )
        checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0007", _AUTHOR)
    # end def test_kbd_set_monitor_mode_4_and_reboot_using_hardware_reset

    @features("Feature18B0v1")
    @features("KeyboardWithLargerMatrixMode")
    @features("Feature1802")
    @level("Business")
    def test_kbd_set_monitor_mode_4_and_reboot_using_feature(self):
        """
        Validate impact on device reboot (KBD with large matrix)

        [0] setMonitorMode(mode)

        Require 0x1802
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        mode_4 = StaticMonitorMode.KBD_LARGER_MATRIX
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 4")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_4)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code": (checker.check_row_code, row_code),
                "col_code": (checker.check_col_code, col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
            }
        )
        checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        kbd_with_larger_matrix_mode_event = KeyboardWithLargerMatrixModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.KeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code": (checker.check_row_code, row_code),
                "col_code": (checker.check_col_code, col_code),
                "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
            }
        )
        checker.check_fields(self, kbd_with_larger_matrix_mode_event, KeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        StaticMonitorModeTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean Battery Status Event and Wireless Device Status Broadcast Event")
        # --------------------------------------------------------------------------------------------------------------
        self.cleanup_battery_event_from_queue()
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent, timeout=.5, allow_no_message=True,
            check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0008", _AUTHOR)
    # end def test_kbd_set_monitor_mode_4_and_reboot_using_feature

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @level("Business")
    @services("HardwareReset")
    def test_kbd_set_monitor_mode_5_and_reboot_using_hardware_reset(self):
        """
        Validate impact on device reboot (Enhanced KBD with large matrix)

        [0] setMonitorMode(mode)

        Require PowerSupply
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        mode_5 = StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 5")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code_0": (checker.check_row_code_0, row_code),
                "col_code_0": (checker.check_col_code_0, col_code)
            }
        )
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                             EnhancedKeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                             EnhancedKeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0009", _AUTHOR)
    # end def test_kbd_set_monitor_mode_5_and_reboot_using_hardware_reset

    @features("Feature18B0v1")
    @features("EnhancedKeyboardWithLargerMatrixMode")
    @features("Feature1802")
    @level("Business")
    def test_kbd_set_monitor_mode_5_and_reboot_using_feature(self):
        """
        Validate impact on device reboot (Enhanced KBD with large matrix)

        [0] setMonitorMode(mode)

        Require 0x1802
        """
        key = KeyMatrixTestUtils.get_key_list(test_case=self, group_count=1, group_size=1, random=True)[0][0]
        mode_5 = StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX
        row_code, col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(test_case=self, key_id=key, combined=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode 5")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "row_code_0": (checker.check_row_code_0, row_code),
                "col_code_0": (checker.check_col_code_0, col_code)
            }
        )
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                             EnhancedKeyboardWithLargerMatrixModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        enhanced_kbd_with_larger_matrix_mode_event = EnhancedKeyboardWithLargerMatrixModeEvent.fromHexList(
            HexList(event))
        checker = StaticMonitorModeTestUtils.EnhancedKeyboardWithLargerMatrixModeEventChecker
        checker.check_fields(self, enhanced_kbd_with_larger_matrix_mode_event,
                             EnhancedKeyboardWithLargerMatrixModeEvent)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _REBOOT_DUT)
        # --------------------------------------------------------------------------------------------------------------
        StaticMonitorModeTestUtils.ResetHelper.hidpp_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Clean Battery Status Event and Wireless Device Status Broadcast Event")
        # --------------------------------------------------------------------------------------------------------------
        self.cleanup_battery_event_from_queue()
        ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=WirelessDeviceStatusBroadcastEvent, timeout=.5, allow_no_message=True,
            check_first_message=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Press {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Release {key.name}")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITOR_MODE_EVENT_NOT_GENERATED)
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self,
                                       timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       class_type=self.feature_18b0.monitor_mode_broadcast_event_cls,
                                       queue_name=HIDDispatcher.QueueName.EVENT)

        self.testCaseChecked("BUS_18B0_0010", _AUTHOR)
    # end def test_kbd_set_monitor_mode_5_and_reboot_using_feature

    @features("Feature18B0")
    @features("Mice")
    @level("Business")
    @services("OpticalSensor")
    def test_mouse_set_monitor_mode_2_response_x_and_y(self):
        """
        Verify 'X' and 'Y' parameters are set correctly (Mouse)

        [0] setMonitorMode(mode)
        """
        raise NotImplementedError("To be implemented when @services('OpticalSensor') is available")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 2 (mouse)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some x values (few sample values between -32767 and 32767)")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "= 0x02 -> 0x04 -> 0x08 -> 0x10 -> 0x20 -> 0x40 -> 0x80 -> 0x100 -> 0x200 ->"
                                     "0x400 ... -> 0x7FF if 12 bits support else 0x7FFF")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set xy_motion(dx=x) using OpticalXyDisplacementInterface")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for input (x) = output (x)")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over some y values (few sample values between -32767 and 32767)")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "= 0x02 -> 0x04 -> 0x08 -> 0x10 -> 0x20 -> 0x40 -> 0x80 -> 0x100 -> 0x200 ->"
                                     "0x400 ... -> 0x7FF if 12 bits support else 0x7FFF")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set xy_motion(dy=y) using OpticalXyDisplacementInterface")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for input (y) = output (y)")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_18B0_0011", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_response_x_and_y

    @features("Feature18B0")
    @features("Mice")
    @level("Business")
    @services("RequiredKeys", (KEY_ID.FORWARD_BUTTON, KEY_ID.BACK_BUTTON))
    def test_mouse_set_monitor_mode_2_response_back_and_forward(self):
        """
        Verify 'Back' and 'Forward' parameters are set correctly (Mouse)

        [0] setMonitorMode(mode)
        """
        mode_2 = StaticMonitorMode.MOUSE_ON
        switch = HexList("00" * (MouseModeEvent.LEN.SWITCHES // 8))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 2 (mouse)")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Back button press")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.BACK_BUTTON)
        switch = StaticMonitorModeTestUtils.update_switch(switch, KEY_ID.BACK_BUTTON, set_bit=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the event for Back button")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.MouseModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"switches": (checker.check_switches, switch)})
        checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Forward button press")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(KEY_ID.FORWARD_BUTTON)
        switch = StaticMonitorModeTestUtils.update_switch(switch, KEY_ID.FORWARD_BUTTON, set_bit=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the event for Forward button")
        # --------------------------------------------------------------------------------------------------------------
        event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
        mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
        checker = StaticMonitorModeTestUtils.MouseModeEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"switches": (checker.check_switches, switch)})
        checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("BUS_18B0_0012", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_response_back_and_forward

    @features("Feature18B0")
    @features("Mice")
    @level("Business")
    @skip("MainWheel")
    def test_mouse_set_monitor_mode_2_response_roller(self):
        """
        Verify 'Roller' parameter is set correctly (Mouse)

        [0] setMonitorMode(mode)
        """
        raise NotImplementedError("To be implemented when @services('MainWheel') is available")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 2 (mouse)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Roller scroll up")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the event for Roller")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "UserAction: Roller scroll down")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the event for Roller")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_18B0_0013", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_response_roller

    @features("Feature18B0")
    @features("Mice")
    @level("Business")
    @skip("MainWheel")
    def test_mouse_set_monitor_mode_2_response_time_between_ratchets(self):
        """
        Verify 'Time between ratchets' parameter is set correctly (Mouse)

        [0] setMonitorMode(mode)
        """
        raise NotImplementedError("To be implemented when @services('MainWheel') is available")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 2 (mouse)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over ratchet interval values in [16ms, 8ms, 4ms, 1ms]")
        # --------------------------------------------------------------------------------------------------------------
        for _ in []:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "UserAction: Roller scroll up for a time interval")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for Roller")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "UserAction: Roller scroll down for a time interval")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for Roller")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_18B0_0014", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_response_time_between_ratchets

    @features("Feature18B0")
    @features("Mice")
    @level("Business")
    def test_mouse_set_monitor_mode_2_response_switches(self):
        """
        Verify 'Switches' parameter is set correctly (Mouse)

        [0] setMonitorMode(mode)
        """
        mode_2 = StaticMonitorMode.MOUSE_ON
        switch = HexList("00" * (MouseModeEvent.LEN.SWITCHES // 8))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 2 (mouse)")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, mode_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over switch values [left, middle, center, ...]")
        # --------------------------------------------------------------------------------------------------------------
        for button in BUTTON_LAYOUT_BY_ID[self.f.PRODUCT.F_ProductReference].KEYS.keys():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {button}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, set_bit=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for switch")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.MouseModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"switches": (checker.check_switches, switch)})
            checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {button}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(button)
            switch = StaticMonitorModeTestUtils.update_switch(switch, button, clear_bit=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for switch")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            mouse_mode_event = MouseModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.MouseModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"switches": (checker.check_switches, switch)})
            checker.check_fields(self, mouse_mode_event, MouseModeEvent, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("BUS_18B0_0015", _AUTHOR)
    # end def test_mouse_set_monitor_mode_2_response_switches

    @features("Feature18B0")
    @features("KeyboardMode")
    @level("Business")
    def test_kbd_set_monitor_mode_1_response_row_col_code(self):
        """
        Verify 'RowColCode' parameter is set correctly (KBD)

        [0] setMonitorMode(mode)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 1 (KBD)")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.KBD_ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over all keys in DUT")
        # --------------------------------------------------------------------------------------------------------------
        for key in self.button_stimuli_emulator.get_key_id_list():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for 'RowColCode'")
            # ----------------------------------------------------------------------------------------------------------
            key_row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_col_code": (checker.check_row_col_code, key_row_col_code),
                    "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
                }
            )
            checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for 'RowColCode'")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_col_code": (checker.check_row_col_code, key_row_col_code),
                    "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
                }
            )
            checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("BUS_18B0_0016", _AUTHOR)
    # end def test_kbd_set_monitor_mode_1_response_row_col_code

    @features("Feature18B0")
    @features("KeyboardMode")
    @level("Business")
    def test_kbd_set_monitor_mode_1_response_make_break(self):
        """
        Verify 'Break/Make' parameter is set correctly (KBD)

        [0] setMonitorMode(mode)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 1 (KBD)")
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.KBD_ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over all keys in DUT")
        # --------------------------------------------------------------------------------------------------------------
        for key in self.button_stimuli_emulator.get_key_id_list():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for 'Make'")
            # ----------------------------------------------------------------------------------------------------------
            key_row_col_code = StaticMonitorModeTestUtils.get_kbd_row_col_code(self, key)
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_col_code": (checker.check_row_col_code, key_row_col_code),
                    "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.MAKE)
                }
            )
            checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release {key.name}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Verify the event for 'Break'")
            # ----------------------------------------------------------------------------------------------------------
            event = StaticMonitorModeTestUtils.HIDppHelper.monitor_mode_broadcast_event(self, check_first_message=False)
            keyboard_mode_event = KeyboardModeEvent.fromHexList(HexList(event))
            checker = StaticMonitorModeTestUtils.KeyboardModeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "row_col_code": (checker.check_row_col_code, key_row_col_code),
                    "break_or_make_info": (checker.check_break_or_make_info, StaticMonitorMode.BREAK)
                }
            )
            checker.check_fields(self, keyboard_mode_event, KeyboardModeEvent, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_TEST_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SET_MONITOR_MODE_0)
        # --------------------------------------------------------------------------------------------------------------
        response = StaticMonitorModeTestUtils.HIDppHelper.set_monitor_mode(self, StaticMonitorMode.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CHECK_MONITORMODE_RESPONSE)
        # --------------------------------------------------------------------------------------------------------------
        checker = StaticMonitorModeTestUtils.SetMonitorModeResponseChecker
        checker.check_fields(self, response, self.feature_18b0.set_monitor_mode_response_cls)

        self.testCaseChecked("BUS_18B0_0017", _AUTHOR)
    # end def test_kbd_set_monitor_mode_1_response_make_break
# end class StaticMonitorModeBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
