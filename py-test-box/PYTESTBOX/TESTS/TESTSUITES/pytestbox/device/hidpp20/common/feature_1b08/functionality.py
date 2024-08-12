#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b08.functionality
:brief: HID++ 2.0 ``AnalogKeys`` business test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choice
from random import sample
from time import sleep

from numpy import arange

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HidKeyboard
from pyhid.hid import HidKeyboardBitmap
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.module.kbdgtech import KBD_GTECH_EMU_MODE
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.analogkeysutils import AnalogKeysTestUtils
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.hidpp20.common.feature_1b08.analogkeys import AnalogKeysTestCase
from pytransport.usb.usbhub.usbhubconstants import UsbHubAction

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Fred Chen"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysFunctionalityTestCase(AnalogKeysTestCase):
    """
    Validate ``AnalogKeys`` functionality test cases
    """
    _WAIT_DEVICE_IN_THE_STEADY_STATE_S = 0.2

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Change KBD Functional Mode from Legacy to Analog")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.emu_gtech.kbd.func_mode_analog()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            self.button_stimuli_emulator.release_all()
            self.button_stimuli_emulator.emu_gtech.kbd.emu_mode_msg(KBD_GTECH_EMU_MODE.REAL)
        # end with

        super().tearDown()
    # end def tearDown

    @features("Feature1B08")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_enable_disable_rapid_trigger_by_sw(self):
        """
        Check be able to enable/disable RapidTrigger by setRapidTriggerState and received AllKeyRelease keyboard
        input report after changed RapidTrigger state.
        """
        ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                    class_type=(HidKeyboard, HidKeyboardBitmap))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over state in [Enable, Disable]')
        # --------------------------------------------------------------------------------------------------------------
        for state in [True, False]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set the RapidTrigger state by setRapidTriggerState(rapid_trigger_state={state})")
            # ----------------------------------------------------------------------------------------------------------
            resp = AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(test_case=self, rapid_trigger_state=state)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the RapidTrigger state has been changed")
            # ----------------------------------------------------------------------------------------------------------
            checker = AnalogKeysTestUtils.RapidTriggerSettingsChecker
            rapid_trigger_settings = {
                "reserved": (checker.check_reserved, 0),
                "rapid_trigger_state": (checker.check_rapid_trigger_state,
                                        resp.rapid_trigger_settings.rapid_trigger_state)
            }
            checker = AnalogKeysTestUtils.SetRapidTriggerStateResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rapid_trigger_settings": (checker.check_rapid_trigger_settings, rapid_trigger_settings)
            })
            checker.check_fields(self, resp, self.feature_1b08.set_rapid_trigger_state_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check received AllKeyRelease keyboard input report")
            # ----------------------------------------------------------------------------------------------------------
            hid_packet = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=(HidKeyboard, HidKeyboardBitmap), check_first_message=False)
            all_key_release = HexList([00] * 16)
            self.assertEqual(expected=all_key_release, obtained=HexList(hid_packet),
                             msg=f'Expect to receive all key release, but received {hid_packet}')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B08_0001", _AUTHOR)
    # end def test_enable_disable_rapid_trigger_by_sw

    @features("Feature1B08")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_enable_disable_key_travel_event_by_sw(self):
        """
        Check be able to enable/disable KeyTravelEvent by setKeyTravelEventState

        Note: Randomly select a test key from the standard key set

        :raise ``Exception``: Don't expect to receive KeyTravelEvent
        """
        test_key = (
            FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper.get_random_standard_key(test_case=self))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Randomly select a test key {test_key!r} from standard key')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable KeyTravelEvent by setKeyTravelEventState')
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(test_case=self, key_travel_event_state=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send a keystroke for the key {test_key!r}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=test_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device reports the KeyTravelEvent')
        # --------------------------------------------------------------------------------------------------------------
        key_cidx = ControlListTestUtils.key_id_to_cidx(test_case=self, key_id=test_key)
        for action in [MAKE, BREAK]:
            key_travel_change_event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            checker = AnalogKeysTestUtils.KeyTravelChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "key_cidx": (checker.check_key_cidx, key_cidx),
                "key_travel": (checker.check_key_travel,
                               AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT if action == MAKE else 0)
            })
            checker.check_fields(self, key_travel_change_event,
                                 self.feature_1b08.key_travel_change_event_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Disable the KeyTravelEvent by setKeyTravelEventState')
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(test_case=self, key_travel_event_state=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send a keystroke for the key {test_key!r}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=test_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device doesn\'t report the KeyTravelEvent')
        # --------------------------------------------------------------------------------------------------------------
        try:
            AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            raise Exception('Don\'t expect to receive KeyTravelEvent')
        except AssertionError:
            pass
        # end try

        self.testCaseChecked("FUN_1B08_0002", _AUTHOR)
    # end def test_enable_disable_key_travel_event_by_sw

    @features("Feature1B08")
    @features('Feature1830powerMode', 3)
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_no_key_travel_event_after_woke_up(self):
        """
        Check the KeyTravelEvent wouldn't been sent after woke up from deep sleep mode

        Note: Randomly select a test key from the standard key set

        :raise ``Exception``: Don't expect to receive KeyTravelEvent
        """
        test_key = (
            FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper.get_random_standard_key(test_case=self))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Randomly select a test key {test_key!r} from standard key')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable KeyTravelEvent by setKeyTravelEventState')
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(test_case=self, key_travel_event_state=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send a keystroke for the key {test_key!r}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=test_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device reports the KeyTravelEvent')
        # --------------------------------------------------------------------------------------------------------------
        key_cidx = ControlListTestUtils.key_id_to_cidx(test_case=self, key_id=test_key)
        for action in [MAKE, BREAK]:
            key_travel_change_event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            checker = AnalogKeysTestUtils.KeyTravelChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "key_cidx": (checker.check_key_cidx, key_cidx),
                "key_travel": (checker.check_key_travel,
                               AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT if action == MAKE else 0)
            })
            checker.check_fields(self, key_travel_change_event,
                                 self.feature_1b08.key_travel_change_event_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Let device enter deep sleep mode by 0x1830.setPowerMode(PowerModeNumber=3)')
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Do an user action to wake up device')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send a keystroke for the key {test_key!r}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=test_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device doesn\'t report the KeyTravelEvent')
        # --------------------------------------------------------------------------------------------------------------
        try:
            AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            raise Exception('Don\'t expect to receive KeyTravelEvent')
        except AssertionError:
            pass
        # end try

        self.testCaseChecked("FUN_1B08_0003", _AUTHOR)
    # end def test_no_key_travel_event_after_woke_up

    @features("Feature1B08")
    @features("Wireless")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_no_key_travel_event_after_reconnection(self):
        """
        Check the KeyTravelEvent wouldn't been sent after reconnection

        Note: Randomly select a test key from the standard key set

        :raise ``Exception``: Don't expect to receive KeyTravelEvent
        """
        test_key = (
            FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper.get_random_standard_key(test_case=self))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Randomly select a test key {test_key!r} from standard key')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable KeyTravelEvent by setKeyTravelEventState')
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(test_case=self, key_travel_event_state=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send a keystroke for the key {test_key!r}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=test_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device reports the KeyTravelEvent')
        # --------------------------------------------------------------------------------------------------------------
        key_cidx = ControlListTestUtils.key_id_to_cidx(test_case=self, key_id=test_key)
        for action in [MAKE, BREAK]:
            key_travel_change_event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            checker = AnalogKeysTestUtils.KeyTravelChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "key_cidx": (checker.check_key_cidx, key_cidx),
                "key_travel": (checker.check_key_travel,
                               AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT if action == MAKE else 0)
            })
            checker.check_fields(self, key_travel_change_event,
                                 self.feature_1b08.key_travel_change_event_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off receiver USB port')
        # --------------------------------------------------------------------------------------------------------------
        usb_port = ChannelUtils.get_port_index(test_case=self)
        self.device.set_usb_ports_status(port_index=usb_port, status=UsbHubAction.OFF)
        sleep(self._WAIT_DEVICE_IN_THE_STEADY_STATE_S)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power on receiver USB port')
        # --------------------------------------------------------------------------------------------------------------
        self.device.set_usb_ports_status(port_index=usb_port, status=UsbHubAction.ON)
        sleep(self._WAIT_DEVICE_IN_THE_STEADY_STATE_S)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send a keystroke for the key {test_key!r}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=test_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device doesn\'t report the KeyTravelEvent')
        # --------------------------------------------------------------------------------------------------------------
        try:
            AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            raise Exception('Don\'t expect to receive KeyTravelEvent')
        except AssertionError:
            pass
        # end try

        self.testCaseChecked("FUN_1B08_0004", _AUTHOR)
    # end def test_no_key_travel_event_after_reconnection

    @features("Feature1B08")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_no_key_travel_event_after_power_cycle(self):
        """
        Check the KeyTravelEvent wouldn't been sent after power cycle

        Note: Randomly select a test key from the standard key set

        :raise ``Exception``: Don't expect to receive KeyTravelEvent
        """
        test_key = (
            FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper.get_random_standard_key(test_case=self))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Randomly select a test key {test_key!r} from standard key')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable KeyTravelEvent by setKeyTravelEventState')
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(test_case=self, key_travel_event_state=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send a keystroke for the key {test_key!r}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=test_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device reports the KeyTravelEvent')
        # --------------------------------------------------------------------------------------------------------------
        key_cidx = ControlListTestUtils.key_id_to_cidx(test_case=self, key_id=test_key)
        for action in [MAKE, BREAK]:
            key_travel_change_event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            checker = AnalogKeysTestUtils.KeyTravelChangeEventChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "key_cidx": (checker.check_key_cidx, key_cidx),
                "key_travel": (checker.check_key_travel,
                               AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT if action == MAKE else 0)
            })
            checker.check_fields(self, key_travel_change_event,
                                 self.feature_1b08.key_travel_change_event_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power OFF -> ON device')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send a keystroke for the key {test_key!r}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=test_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check device doesn\'t report the KeyTravelEvent')
        # --------------------------------------------------------------------------------------------------------------
        try:
            AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            raise Exception('Don\'t expect to receive KeyTravelEvent')
        except AssertionError:
            pass
        # end try

        self.testCaseChecked("FUN_1B08_0005", _AUTHOR)
    # end def test_no_key_travel_event_after_power_cycle

    @features("Feature1B08")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_continuous_key_travel_event(self):
        """
        Check device continuous sends KeyTravelEvent while key_travel keeping changed

        Note: Randomly select a test key from the standard key set
        """
        test_key = (
            FullKeyCustomizationTestUtils.FkcTableHelper.RandomGenerationHelper.get_random_standard_key(test_case=self))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Randomly select a test key {test_key!r} from standard key')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable KeyTravelEvent by setKeyTravelEventState')
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(test_case=self, key_travel_event_state=True)

        num_of_keys = 20
        max_key_travel = AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT
        # noinspection PyTypeChecker
        key_travel_list = sample(arange(1, max_key_travel + 1, 1).tolist(), k=num_of_keys)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Randomly select {num_of_keys} key travels from [1..Full] to {key_travel_list}')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over key_travel in {key_travel_list}')
        # --------------------------------------------------------------------------------------------------------------
        for key_travel in key_travel_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press {test_key!r} with key travel = {key_travel}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=key_travel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check device reports the KeyTravelEvent and check the key travel')
            # ----------------------------------------------------------------------------------------------------------
            event = AnalogKeysTestUtils.HIDppHelper.key_travel_change_event(test_case=self)
            key_cidx = ControlListTestUtils.key_id_to_cidx(test_case=self, key_id=test_key)
            self.assertEqual(expected=key_cidx, obtained=to_int(event.key_cidx))
            self.assertEqual(expected=key_travel, obtained=to_int(event.key_travel))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B08_0006", _AUTHOR)
    # end def test_continuous_key_travel_event

    @features("Feature1B08")
    @features("Feature8101")
    @features("Feature1B10")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_actuation_point_for_some_keys(self):
        """
        Check be able to add different actuation point settings for some keys

        Note: Randomly select 30 test keys from the standard key set
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable KeyTravelEvent by setKeyTravelEventState')
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_key_travel_event_state(test_case=self, key_travel_event_state=True)

        num_of_keys = 30
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f'Create actuation point settings for {num_of_keys} keys (each key has difference settings)')
        # --------------------------------------------------------------------------------------------------------------
        actuation_table = self.create_actuation_table_in_ram(key_count=num_of_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over {key} in [test keys]')
        # --------------------------------------------------------------------------------------------------------------
        self.empty_hid_queue()
        for row in actuation_table.rows:
            test_key = ControlListTestUtils.cidx_to_key_id(test_case=self, cid_index=to_int(row.trigger_cidx))
            actuation_point = to_int(row.actuation_point)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press the key {test_key!r} with key travel = Full amount')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=test_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the key MAKE report')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id=test_key, state=MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Fully release the key {test_key!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=test_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the key BREAK report')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id=test_key, state=BREAK))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press the key {test_key!r} with key travel = actuation point {actuation_point}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the key MAKE report')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id=test_key, state=MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Fully release the key {test_key!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=test_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the key BREAK report')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id=test_key, state=BREAK))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press the key {test_key!r} with key travel = {actuation_point - 1}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=actuation_point - 1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no additional key reports are being received from device')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=2)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Fully release the key {test_key!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=test_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no additional key reports are being received from device')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=2)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B08_0007", _AUTHOR)
    # end def test_actuation_point_for_some_keys

    @features("Feature1B08")
    @features("Feature8101")
    @features("Feature1B10")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_sensitivity_for_some_keys(self):
        """
        Check be able to add different sensitivity settings of RapidTrigger for some keys

        Note: Randomly select 30 test keys from the standard key set
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set to host mode by 0x8101.getSetMode")
        # --------------------------------------------------------------------------------------------------------------
        ProfileManagementTestUtils.HIDppHelper.get_set_mode(test_case=self, set_onboard_mode=1,
                                                            onboard_mode=ProfileManagement.Mode.HOST_MODE)

        num_of_keys = 30
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f'Create rapid trigger settings for {num_of_keys} keys (each key has difference settings)')
        # --------------------------------------------------------------------------------------------------------------
        rapid_trigger_table = self.create_rapid_trigger_table_in_ram(key_count=num_of_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Rapid Trigger by setRapidTriggerState(rapid_trigger_state=Enable)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(test_case=self, rapid_trigger_state=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over {key} in [test keys]')
        # --------------------------------------------------------------------------------------------------------------
        self.empty_hid_queue()
        max_key_travel = AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT
        for row in rapid_trigger_table.rows:
            test_key = ControlListTestUtils.cidx_to_key_id(test_case=self, cid_index=to_int(row.trigger_cidx))
            sensitivity = to_int(row.sensitivity)
            if sensitivity == 1:
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press the key {test_key!r} with key travel = Full amount')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=test_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the key MAKE report')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id=test_key, state=MAKE))

            # noinspection PyTypeChecker
            amount = choice(arange(1, sensitivity).tolist())
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Selects a random {amount} from [1..{sensitivity - 1}](unit)')
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Faintly raise the key {test_key!r} with key travel = {sensitivity} - {amount}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key,
                                                          displacement=max_key_travel - sensitivity + amount)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no additional key reports are being received from device')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Release the key {test_key!r} with key travel = {amount}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key,
                                                          displacement=max_key_travel - sensitivity - 1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the BREAK key report')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id=test_key, state=BREAK))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Fully release the key {test_key!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=test_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no additional key reports are being received from device')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=1)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B08_0008", _AUTHOR)
    # end def test_sensitivity_for_some_keys

    @features("Feature1B08")
    @features("Feature8101")
    @features("Feature1B10")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_multi_action_for_some_keys(self):
        """
        Check be able to add different MultiAction settings (2nd actuation point and assignments) for some keys

        Note: Randomly select 30 test keys from the standard key set

        PS: Refer the event slots definition from the 0x1B08 specification:
        https://docs.google.com/spreadsheets/d/1S3Fz3mccpNIoguVkO6hN5ggfgllsojhGkD2j5E9f2A0
        """
        num_of_keys = 30
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Create multi-action settings for {num_of_keys} keys: with 1 ~ 4 assignments and '
                                 'valid 2nd actuation point setting')
        # --------------------------------------------------------------------------------------------------------------
        multi_action_table = self.create_multi_action_table_in_ram(number_of_key_to_be_random_generated=num_of_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable MultiAction by Assignment Toggle')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT)
        FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self, enable=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over {key} in [test keys]')
        # --------------------------------------------------------------------------------------------------------------
        self.empty_hid_queue()
        for action_group in multi_action_table.groups:
            test_key = action_group.trigger_key
            global_actuation_point = self.config.F_DefaultActuationPoint
            second_actuation_point = action_group.second_actuation_point
            max_key_travel = AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Press the key {test_key!r} with key travel = 1st actuation point {global_actuation_point}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=global_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive MAKE reports that defined on event 0 and 1')
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                test_case=self, trigger_key=test_key, multi_action_table=multi_action_table, last_actuation_point=0,
                current_actuation_point=global_actuation_point, global_actuation_point=global_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Press the key {test_key!r} with key travel = 2nd actuation point {second_actuation_point}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=second_actuation_point)

            if len(action_group.rows) > 2:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check we receive MAKE report(s) that defined on event 2 and 3')
                # ------------------------------------------------------------------------------------------------------
                AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                    test_case=self, trigger_key=test_key, multi_action_table=multi_action_table,
                    last_actuation_point=global_actuation_point, current_actuation_point=second_actuation_point,
                    global_actuation_point=global_actuation_point)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press the key {test_key!r} with key travel = Max key travel')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=max_key_travel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no additional key reports are being received from device')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Release the key {test_key!r} with key travel = 2nd actuation point {second_actuation_point}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=second_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we received BREAK report(s) that defined on event 3 and 2')
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                test_case=self, trigger_key=test_key, multi_action_table=multi_action_table,
                last_actuation_point=max_key_travel, current_actuation_point=second_actuation_point,
                global_actuation_point=global_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self,
                f'Release the key {test_key!r} with key travel = 1st actuation point {global_actuation_point}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=global_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive BREAK report(s) that defined on event 1 and 0')
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                test_case=self, trigger_key=test_key, multi_action_table=multi_action_table,
                last_actuation_point=second_actuation_point, current_actuation_point=global_actuation_point,
                global_actuation_point=global_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Release the key {test_key!r} with key with key travel = 0')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check all key released from device')
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                test_case=self, trigger_key=test_key, multi_action_table=multi_action_table,
                last_actuation_point=global_actuation_point, current_actuation_point=0,
                global_actuation_point=global_actuation_point)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B08_0009", _AUTHOR)
    # end def test_multi_action_for_some_keys

    @features("Feature1B08")
    @features("Feature8101")
    @features("Feature1B10")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_multi_action_with_special_key_travels(self):
        """
        Ensure that MultiAction shall work properly while release key travel exactly the same as the global sensitivity

        Note: Randomly select 20 test keys from the standard key set

        PS: Refer the event slots definition from the 0x1B08 specification:
        https://docs.google.com/spreadsheets/d/1S3Fz3mccpNIoguVkO6hN5ggfgllsojhGkD2j5E9f2A0
        """
        num_of_keys = 20
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Create MultiAction settings for {num_of_keys} keys (each key has difference '
                                 'settings and 2 assignments on event 1 and event 3)')
        # --------------------------------------------------------------------------------------------------------------
        multi_action_table = self.create_multi_action_table_in_ram(number_of_key_to_be_random_generated=num_of_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable MultiAction by Assignment Toggle')
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self, enable=True)

        self.empty_hid_queue()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over {key} in [test keys]')
        # --------------------------------------------------------------------------------------------------------------
        for action_group in multi_action_table.groups:
            test_key = action_group.trigger_key
            global_actuation_point = self.config.F_DefaultActuationPoint
            global_sensitivity = self.config.F_DefaultSensitivity
            max_key_travel = AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press the key {test_key!r} with key travel = Full amount')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=max_key_travel)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the MAKE report(s) defined for events 0 to 3')
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                test_case=self, trigger_key=test_key, multi_action_table=multi_action_table, last_actuation_point=0,
                current_actuation_point=max_key_travel, global_actuation_point=global_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Release the key {test_key!r} with key travel = Global Sensitivity {global_sensitivity}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key,
                                                          displacement=max_key_travel - global_sensitivity)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, 'Check no key report from device or we receive BREAK report(s) that defined on event 3')
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                test_case=self, trigger_key=test_key, multi_action_table=multi_action_table,
                last_actuation_point=max_key_travel, current_actuation_point=max_key_travel - global_sensitivity,
                global_actuation_point=global_actuation_point)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Release the key {test_key!r} with key travel = 0')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=test_key, displacement=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive BREAK report(s) that defined on event 3 ~ 0')
            # ----------------------------------------------------------------------------------------------------------
            AnalogKeysTestUtils.MultiActionChecker.check_multi_actions(
                test_case=self, trigger_key=test_key, multi_action_table=multi_action_table,
                last_actuation_point=max_key_travel - global_sensitivity, current_actuation_point=0,
                global_actuation_point=global_actuation_point)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B08_0010", _AUTHOR)
    # end def test_multi_action_with_special_key_travels

    @features("Feature1B08")
    @features("FullKeyCustomization")
    @level("Functionality")
    @services("DualKeyMatrix")
    def test_fkc_work_with_rapid_trigger(self):
        """
        Ensure that FKC be able to work with RapidTrigger

        Note: Randomly select 30 test keys from the standard key set
        """
        num_of_keys = 30
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Create FKC settings for {num_of_keys} keys (each key has difference settings)')
        # --------------------------------------------------------------------------------------------------------------
        random_parameters_cls = FullKeyCustomizationTestUtils.FkcTableHelper.RandomParameters
        remapped_keys = self.create_fkc_remapping_in_ram(random_parameters=random_parameters_cls(
            button=random_parameters_cls.Button(
                count=num_of_keys,
                trigger_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY,
                action_key_type=RemappedKey.RandomKey.NON_MODIFIER_KEY)))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable MultiAction by Assignment Toggle')
        # --------------------------------------------------------------------------------------------------------------
        FullKeyCustomizationTestUtils.set_fkc_state_by_toggle_key(test_case=self, enable=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable Rapid Trigger by setRapidTriggerState(rapid_trigger_state=Enable)")
        # --------------------------------------------------------------------------------------------------------------
        AnalogKeysTestUtils.HIDppHelper.set_rapid_trigger_state(test_case=self, rapid_trigger_state=True)
        self.empty_hid_queue()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over {key} in [test keys]')
        # --------------------------------------------------------------------------------------------------------------
        max_key_travel = AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT
        global_sensitivity = self.config.F_DefaultSensitivity
        for remapped_key in remapped_keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Press the key {remapped_key.trigger_key!r} with key travel = Full amount')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=remapped_key.trigger_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the key MAKE report')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id=remapped_key.action_key, state=MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Release the key {remapped_key!r} with key travel = Global sensitivity {global_sensitivity}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=remapped_key.trigger_key,
                                                          displacement=max_key_travel - global_sensitivity)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check we receive the key BREAK report')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id=remapped_key.action_key, state=BREAK))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Fully release the key {remapped_key!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_release(key_id=remapped_key.trigger_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check no additional key reports are being received from device')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=2)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B08_0011", _AUTHOR)
    # end def test_fkc_work_with_rapid_trigger
# end class AnalogKeysFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
