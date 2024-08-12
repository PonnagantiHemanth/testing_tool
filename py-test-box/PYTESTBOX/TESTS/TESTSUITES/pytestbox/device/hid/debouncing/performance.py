#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.debouncing.performance
:brief: Hid debouncing performance test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/11/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from enum import unique
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hid import HidKeyboard
from pyhid.hid import HidKeyboardBitmap
from pyhid.hid import HidMouse
from pyhid.hid import HidMouseNvidiaExtension
from pyhid.hiddata import HidData
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import ReportReferences
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.ble.gatt.hids.hids import GattHIDSApplicationTestCases
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DebounceConfiguration:
    """
    Debounce test configurations

    Test parameters in the debounce algorithm:
    https://spaces.logitech.com/display/ptb/Debounce+V1+Test
    https://spaces.logitech.com/display/ptb/Debounce+V2+Test
    """
    # Test step
    STEP_US = 100
    DEEP_SLEEP_STEP_US = 1000

    @unique
    class Mode(IntEnum):
        """
        Power mode
        """
        ACTIVE = auto()
        RUN = auto()
        SLEEP = auto()
        BACKLIGHT_OFF_SLEEP = auto()
        DEEP_SLEEP = auto()
        LIFT = auto()
    # end class Mode

    class Repetition:
        """
        Repetition times in different power mode
        """
        ACTIVE_MODE = 100
        RUN_MODE = 100
        SLEEP_MODE = 40
        BACKLIGHT_OFF_SLEEP_MODE = 20
        DEEP_SLEEP_MODE = 20
        LIFT_MODE = 20
    # end class Repetition

    class Gaming:
        """
        Gaming configurations in the debounce test
        """
        TOLERANCE_US = 100

        class Mouse:
            """
            Mouse configurations
            """

            class MechanicalSwitch:
                """
                Mechanical switch time range
                """
                MIN_TIME_ON_PRESS_US = 500
                MAX_TIME_ON_PRESS_US = 1000
                MIN_TIME_ON_RELEASE_US = 10000
                MAX_TIME_ON_RELEASE_US = 25000
                MIN_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 4000
                MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 30000
                MIN_TIME_ON_PRESS_AND_LIFT_US = 9000
                MAX_TIME_ON_PRESS_AND_LIFT_US = 10000
            # end class MechanicalSwitch

            class HybridSwitch:
                """
                Hybrid switch time range
                """
                MIN_TIME_ON_PRESS_US = 0
                MAX_TIME_ON_PRESS_US = 1000
                MIN_TIME_ON_RELEASE_US = 1000
                MAX_TIME_ON_RELEASE_US = 2000
                MIN_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 4000
                MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 30000
                MIN_TIME_ON_PRESS_AND_LIFT_US = 9000
                MAX_TIME_ON_PRESS_AND_LIFT_US = 10000
            # end class HybridSwitch
        # end class Mouse

        class Keyboard:
            """
            Keyboard configurations
            """

            class MechanicalSwitch:
                """
                Mechanical switch time range
                """
                MIN_TIME_ON_PRESS_US = 1000
                MAX_TIME_ON_PRESS_US = 2000
                MIN_TIME_ON_RELEASE_US = 1000
                MAX_TIME_ON_RELEASE_US = 2000
                MIN_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 4000
                MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 30000
                MIN_TIME_ON_PRESS_AND_BACKLIGHT_OFF_SLEEP_US = 4000
                MAX_TIME_ON_PRESS_AND_BACKLIGHT_OFF_SLEEP_US = 8000
            # end class MechanicalSwitch

            class OpticalSwitch:
                """
                Optical switch  time range
                """
                MIN_TIME_ON_PRESS_US = 0
                MAX_TIME_ON_PRESS_US = 1000
                MIN_TIME_ON_RELEASE_US = 1000
                MAX_TIME_ON_RELEASE_US = 2000
                MIN_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 4000
                MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 30000
                MIN_TIME_ON_PRESS_AND_BACKLIGHT_OFF_SLEEP_US = 4000
                MAX_TIME_ON_PRESS_AND_BACKLIGHT_OFF_SLEEP_US = 8000
            # end class OpticalSwitch
        # end class Keyboard
    # end class Gaming

    class PWS:
        """
        PWS configurations in the debounce test
        """
        TOLERANCE_US = 1000

        class Mouse:
            """
            Mouse configurations
            """
            MIN_TIME_ON_PRESS_US = 4000
            MAX_TIME_ON_PRESS_US = 8000
            MIN_TIME_ON_RELEASE_US = 4000
            MAX_TIME_ON_RELEASE_US = 8000
            MIN_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 8000
            MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 60000
        # end class Mouse

        class Keyboard:
            """
            Keyboard configurations
            """
            MIN_TIME_ON_PRESS_US = 4000
            MAX_TIME_ON_PRESS_US = 8000
            MIN_TIME_ON_RELEASE_US = 24000
            MAX_TIME_ON_RELEASE_US = 28000
            MIN_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 8000
            MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US = 60000
        # end class Keyboard
    # end class PWS

    @classmethod
    def get_debounce_config(cls, test_case):
        """
        Get the debounce configurations for the current test case

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The debounce factors for the current test case
        :rtype: ``tuple[DebounceConfiguration.Gaming | DebounceConfiguration.PWS, int]``

        :raise ``ValueError``: if F_MouseSwitchType or F_KeyboardType is unsupported
        """
        if test_case.f.PRODUCT.F_IsGaming:
            if test_case.f.PRODUCT.F_IsMice:
                if test_case.f.PRODUCT.DEVICE.F_MouseSwitchType == 'mechanical':
                    debounce_config = cls.Gaming.Mouse.MechanicalSwitch
                elif test_case.f.PRODUCT.DEVICE.F_MouseSwitchType == 'hybrid':
                    debounce_config = cls.Gaming.Mouse.HybridSwitch
                else:
                    raise ValueError(f'Invalid mouse switch type: {test_case.f.PRODUCT.DEVICE.F_MouseSwitchType}')
                # end if
            else:
                if test_case.f.PRODUCT.DEVICE.F_KeyboardType == 'mechanical':
                    debounce_config = cls.Gaming.Keyboard.MechanicalSwitch
                elif test_case.f.PRODUCT.DEVICE.F_KeyboardType == 'optical_switch_array':
                    debounce_config = cls.Gaming.Keyboard.OpticalSwitch
                else:
                    raise ValueError(f'Invalid keyboard type: {test_case.f.PRODUCT.DEVICE.F_KeyboardType}')
                # end if
            # end if
            tolerance = cls.Gaming.TOLERANCE_US
        else:
            debounce_config = cls.PWS.Mouse if test_case.f.PRODUCT.F_IsMice else cls.PWS.Keyboard
            tolerance = cls.PWS.TOLERANCE_US
        # end if
        return debounce_config, tolerance
    # end def get_debounce_config
# end class DebounceConfiguration


class DebouncePerformanceTestCase(BaseTestCase):
    """
    Validate Debouncing Performance TestCases

    Manual test cases:
    https://jira.logitech.io/secure/Tests.jspa#/testCase/PTB-T1
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        self.post_requisite_release_holding_key = False
        self.post_requisite_reset_motion_emulator = False
        self.post_requisite_turn_on_all_generic_usb_ports = False

        # Empty hid_message_queue
        channel_to_use = self.current_channel.receiver_channel \
            if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel
        ChannelUtils.clean_messages(
            test_case=self, channel=channel_to_use, queue_name=HIDDispatcher.QueueName.HID, class_type=HID_REPORTS)

        # For BLE HID notification validation
        self.last_make_report = None
        self.last_break_report = None
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_release_holding_key:
                holding_key = self._get_holding_key()
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, f'Release the holding key: {repr(holding_key)}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.multiple_keys_release(key_ids=[holding_key], delay=0.1)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reset_motion_emulator:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reset motion emulator')
                # ------------------------------------------------------------------------------------------------------
                self.motion_emulator.reset()
                self.post_requisite_reset_motion_emulator = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_turn_on_all_generic_usb_ports:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Turn on all generic USB ports (1, 2, 3, 4, 7)")
                # ------------------------------------------------------------------------------------------------------
                DeviceBaseTestUtils.UsbHubHelper.turn_on_all_generic_usb_ports(test_case=self)
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def _get_class_types(self):
        """
        Get the HID report class type for keyboard or mouse

        :return: HID report class types
        :rtype: ``tuple[HidMouse, HidMouseNvidiaExtension] | tuple[HidKeyboard, HidKeyboardBitmap]``
        """
        return (HidMouse, HidMouseNvidiaExtension) if self.f.PRODUCT.F_IsMice else (HidKeyboard, HidKeyboardBitmap)
    # end def _get_class_types

    def _get_holding_key(self):
        """
        Get the holding key to be tested

        :return: The holding key to be tested
        :rtype: ``KEY_ID``
        """
        return KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=2, random=False,
                                               excluded_keys=HidData.get_not_single_action_keys())[0][1]
    # end def _get_holding_key

    def _check_hid_report_by_key_id(
            self, key_id, action, ble_notification_queue=None):
        """
        Check if received HID reports are expected

        :param key_id: the target key id
        :type key_id: ``KEY_ID``
        :param action: MAKE or BREAK state
        :type action: ``str``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``

        :raise ``AssertionError``: If the action is not supported or the HID report is not as expected
        """
        assert action in [MAKE, BREAK], f'Unsupported action: {repr(action)}'
        if ble_notification_queue is None:
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id, action))
        else:
            report = ble_notification_queue.get(timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)
            if action == MAKE:
                if self.last_make_report is None:
                    self.last_make_report = report.data
                else:
                    # Check the report is the same as the last one
                    self.assertEqual(report.data, self.last_make_report, 'The MAKE report shall be the same')
                # end if
            else:
                if self.last_break_report is None:
                    self.last_break_report = report.data
                else:
                    # Check the report is the same as the last one
                    self.assertEqual(report.data, self.last_break_report, 'The BREAK report shall be the same')
                # end if
            # end if
        # end if
    # end def _check_hid_report_by_key_id

    def _check_queue_empty(self, channel_to_use, class_types, ble_notification_queue=None):
        """
        Check the queue is empty

        :param channel_to_use: the channel to use
        :type channel_to_use: ``BaseCommunicationChannel``
        :param class_types: The type of messages to be retrieved from the queue, cannot be ``None``
        :type class_types: ``type`` or ``tuple[type]`` or ``None``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``

        :raise ``AssertionError``: If the BLE HID notification queue is not empty
        """
        if ble_notification_queue is None:
            ChannelUtils.check_queue_empty(test_case=self, channel=channel_to_use,
                                           queue_name=HIDDispatcher.QueueName.HID, class_type=class_types)
        else:
            assert ble_notification_queue.empty(), 'The BLE HID notification queue shall be empty'
        # end if
    # end def _check_queue_empty

    def _clean_messages(self, channel_to_use, class_types, ble_notification_queue=None):
        """
        Clean messages in the queue

        :param channel_to_use: the channel to use
        :type channel_to_use: ``BaseCommunicationChannel``
        :param class_types: The type of messages to be retrieved from the queue, cannot be ``None``
        :type class_types: ``type`` or ``tuple[type]`` or ``None``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        if ble_notification_queue is None:
            ChannelUtils.clean_messages(test_case=self, channel=channel_to_use,
                                        queue_name=HIDDispatcher.QueueName.HID, class_type=class_types)
        else:
            while not ble_notification_queue.empty():
                ble_notification_queue.get()
            # end while
        # end if
    # end def _clean_messages

    def _0percent_make(self, mode, repetition, ble_notification_queue=None):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all.

        :param mode: The power mode to test
        :type mode: ``DebounceConfiguration.Mode``
        :param repetition: The number of loops to perform
        :type repetition: ``int``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``

        :raise ``ValueError``: If the mode provides an unsupported power option
        """
        (test_key,) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                      excluded_keys=HidData.get_not_single_action_keys())[0]
        debounce_config, tolerance = DebounceConfiguration.get_debounce_config(test_case=self)
        if mode in [DebounceConfiguration.Mode.ACTIVE,
                    DebounceConfiguration.Mode.RUN,
                    DebounceConfiguration.Mode.SLEEP]:
            make_detection_end = debounce_config.MAX_TIME_ON_PRESS_US
            test_step = DebounceConfiguration.STEP_US
        elif mode == DebounceConfiguration.Mode.DEEP_SLEEP:
            make_detection_end = debounce_config.MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US
            test_step = DebounceConfiguration.DEEP_SLEEP_STEP_US
        else:
            raise ValueError(f'Unsupported power mode: {repr(mode)}')
        # end if
        class_types = self._get_class_types()
        channel_to_use = self.current_channel.receiver_channel \
            if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Measure the 0% MAKE debounce time on the key id = {repr(test_key)} '
                                 f'from {make_detection_end}us to {test_step}us and loop {repetition} times.')
        # --------------------------------------------------------------------------------------------------------------
        done = False
        device_is_awake = True
        measuring_0_percent_make = make_detection_end
        for make_duration in reversed(range(test_step, make_detection_end, test_step)):
            for count in range(repetition):
                if mode == DebounceConfiguration.Mode.SLEEP and device_is_awake:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f'Wait {self.f.PRODUCT.DEVICE.F_MaxWaitSleep}s, let the device into sleep mode')
                    # --------------------------------------------------------------------------------------------------
                    sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep)
                    device_is_awake = False
                elif mode == DebounceConfiguration.Mode.DEEP_SLEEP and device_is_awake:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, 'Force the device into deep sleep mode thru the 0x1830 SetPowerMode request')
                    # --------------------------------------------------------------------------------------------------
                    PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
                    device_is_awake = False
                # end if

                self.button_stimuli_emulator.keystroke(key_id=test_key, duration=make_duration / 10 ** 6)

                try:
                    # noinspection PyTypeChecker
                    self._check_queue_empty(channel_to_use, class_types, ble_notification_queue)
                except (AssertionError, QueueEmpty):
                    measuring_0_percent_make = int(make_duration - test_step)
                    # noinspection PyTypeChecker
                    self._clean_messages(channel_to_use, class_types, ble_notification_queue)
                    device_is_awake = True
                    break
                # end try

                done = (count == repetition - 1)
            # end for
            if done:
                break
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_metrics(
            self, key=f'{repr(mode)}: the 0% MAKE debounce time', value=f'{measuring_0_percent_make}us')
        # --------------------------------------------------------------------------------------------------------------

        measured_0_percent_make_lower_bound = 0 if debounce_config.MIN_TIME_ON_PRESS_US == 0 else (
                debounce_config.MIN_TIME_ON_PRESS_US - tolerance)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the measured 0% MAKE debounce time {measuring_0_percent_make}us is greater '
                                  f'or equal to the expected time {measured_0_percent_make_lower_bound}us')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(a=measuring_0_percent_make, b=measured_0_percent_make_lower_bound,
                                msg='The measured 0% MAKE debounce time shall be greater or equal to the expected time '
                                    f'{measured_0_percent_make_lower_bound}us')
    # end def _0percent_make

    def _100percent_make(self, mode, repetition, ble_notification_queue=None):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make.

        :param mode: The power mode to test
        :type mode: ``DebounceConfiguration.Mode``
        :param repetition: The number of loops to perform
        :type repetition: ``int``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``

        :raise ``ValueError``: If the mode provides an unsupported power option
        """
        (test_key,) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                      excluded_keys=HidData.get_not_single_action_keys())[0]

        debounce_config, tolerance = DebounceConfiguration.get_debounce_config(test_case=self)
        if mode in [DebounceConfiguration.Mode.ACTIVE,
                    DebounceConfiguration.Mode.RUN,
                    DebounceConfiguration.Mode.SLEEP]:
            make_detection_start = debounce_config.MIN_TIME_ON_PRESS_US if debounce_config.MIN_TIME_ON_PRESS_US != 0 \
                else 100
            make_duration_end = debounce_config.MIN_TIME_ON_PRESS_US + debounce_config.MAX_TIME_ON_PRESS_US
            measured_100_percent_make_upper_bound = debounce_config.MAX_TIME_ON_PRESS_US + tolerance
            test_step = DebounceConfiguration.STEP_US
        elif mode == DebounceConfiguration.Mode.DEEP_SLEEP:
            make_detection_start = debounce_config.MIN_TIME_ON_PRESS_AND_DEEP_SLEEP_US
            make_duration_end = debounce_config.MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US + 1000
            measured_100_percent_make_upper_bound = debounce_config.MAX_TIME_ON_PRESS_AND_DEEP_SLEEP_US + tolerance
            test_step = DebounceConfiguration.DEEP_SLEEP_STEP_US
        elif mode == DebounceConfiguration.Mode.LIFT:
            make_detection_start = debounce_config.MIN_TIME_ON_PRESS_AND_LIFT_US
            make_duration_end = debounce_config.MAX_TIME_ON_PRESS_AND_LIFT_US + 1000
            measured_100_percent_make_upper_bound = debounce_config.MAX_TIME_ON_PRESS_AND_LIFT_US + tolerance
            test_step = DebounceConfiguration.STEP_US
        elif mode == DebounceConfiguration.Mode.BACKLIGHT_OFF_SLEEP:
            make_detection_start = debounce_config.MIN_TIME_ON_PRESS_AND_BACKLIGHT_OFF_SLEEP_US
            make_duration_end = debounce_config.MAX_TIME_ON_PRESS_AND_BACKLIGHT_OFF_SLEEP_US + 1000
            measured_100_percent_make_upper_bound = (debounce_config.MAX_TIME_ON_PRESS_AND_BACKLIGHT_OFF_SLEEP_US
                                                     + tolerance)
            test_step = DebounceConfiguration.DEEP_SLEEP_STEP_US
        else:
            raise ValueError(f'Unsupported power mode: {repr(mode)}')
        # end if
        class_types = self._get_class_types()
        channel_to_use = self.current_channel.receiver_channel \
            if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Measure the 100% MAKE debounce time on the key id = {repr(test_key)} from '
                                 f'{make_detection_start}us to {make_duration_end}us and loop {repetition} times.')
        # --------------------------------------------------------------------------------------------------------------
        done = False
        device_is_awake = True
        measuring_100_percent_make = make_detection_start
        for make_duration in range(make_detection_start, make_duration_end, test_step):
            for count in range(repetition):
                if (mode in [DebounceConfiguration.Mode.SLEEP, DebounceConfiguration.Mode.BACKLIGHT_OFF_SLEEP] and
                        device_is_awake):
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, f'Wait {self.f.PRODUCT.DEVICE.F_MaxWaitSleep}s, let the device into sleep mode')
                    # --------------------------------------------------------------------------------------------------
                    sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep)
                    device_is_awake = False
                elif mode == DebounceConfiguration.Mode.DEEP_SLEEP and device_is_awake:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        self, 'Force the device into deep sleep mode thru the 0x1830 SetPowerMode request')
                    # --------------------------------------------------------------------------------------------------
                    PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
                    device_is_awake = False
                # end if

                self.button_stimuli_emulator.keystroke(key_id=test_key, duration=make_duration / 10 ** 6)

                try:
                    if mode == DebounceConfiguration.Mode.DEEP_SLEEP and ble_notification_queue is not None:
                        BleProtocolTestUtils.connect_and_bond_device(test_case=self,
                                                                     ble_context_device=self.ble_context_device_used,
                                                                     log_gatt_table=False)
                        device_is_awake = True
                    # end if

                    self._check_hid_report_by_key_id(key_id=test_key, action=MAKE,
                                                     ble_notification_queue=ble_notification_queue)
                    self._check_hid_report_by_key_id(key_id=test_key, action=BREAK,
                                                     ble_notification_queue=ble_notification_queue)
                    device_is_awake = True
                except (AssertionError, QueueEmpty):
                    measuring_100_percent_make = make_duration + test_step
                    KeyMatrixTestUtils.KeyExpectedActions.reset()
                    # noinspection PyTypeChecker
                    self._clean_messages(channel_to_use=channel_to_use, class_types=class_types,
                                         ble_notification_queue=ble_notification_queue)
                    break
                # end try

                done = (count == repetition - 1)
            # end for
            if done:
                break
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_metrics(
            self, key=f'{repr(mode)}: the 100% MAKE debounce time', value=f'{measuring_100_percent_make}us')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the measured 100% MAKE debounce time {measuring_100_percent_make}us is less '
                                  f'or equal to the expected time {measured_100_percent_make_upper_bound}us')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLessEqual(a=measuring_100_percent_make, b=measured_100_percent_make_upper_bound,
                             msg='The measured 100% MAKE debounce time shall be less or equal to the expected time '
                                 f'{measured_100_percent_make_upper_bound}us')
    # end def _100percent_make

    def _0percent_break(self, mode, repetition, ble_notification_queue=None):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all.

        :param mode: The power mode to test
        :type mode: ``DebounceConfiguration.Mode``
        :param repetition: The number of loops to perform
        :type repetition: ``int``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        (test_key,) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                      excluded_keys=HidData.get_not_single_action_keys())[0]
        test_step = DebounceConfiguration.STEP_US
        class_types = self._get_class_types()
        debounce_config, tolerance = DebounceConfiguration.get_debounce_config(test_case=self)
        break_detection_end = debounce_config.MAX_TIME_ON_RELEASE_US
        channel_to_use = self.current_channel.receiver_channel \
            if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Measure the 0% BREAK debounce time on the key id = {repr(test_key)} '
                                 f'from {break_detection_end}us to {test_step}us and loop {repetition} times.')
        # --------------------------------------------------------------------------------------------------------------
        done = False
        measuring_0_percent_break = break_detection_end
        # Let the key in MAKE state before ding the test
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[test_key], delay=ButtonStimuliInterface.DEFAULT_DELAY)
        self._check_hid_report_by_key_id(key_id=test_key, action=MAKE, ble_notification_queue=ble_notification_queue)
        for break_duration in reversed(range(test_step, break_detection_end, test_step)):
            for count in range(repetition):
                self.kosmos.sequencer.offline_mode = True
                self.button_stimuli_emulator.multiple_keys_release(key_ids=[test_key], delay=break_duration / 10 ** 6)
                self.button_stimuli_emulator.multiple_keys_press(key_ids=[test_key])
                self.kosmos.sequencer.offline_mode = False
                self.kosmos.sequencer.play_sequence()
                sleep(.1)

                try:
                    # noinspection PyTypeChecker
                    self._check_queue_empty(channel_to_use=channel_to_use, class_types=class_types,
                                            ble_notification_queue=ble_notification_queue)
                except (AssertionError, QueueEmpty):
                    measuring_0_percent_break = break_duration - test_step
                    # noinspection PyTypeChecker
                    self._clean_messages(channel_to_use=channel_to_use, class_types=class_types,
                                         ble_notification_queue=ble_notification_queue)
                    break
                # end try

                done = (count == repetition - 1)
            # end for
            if done:
                break
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_metrics(
            self, key=f'{repr(mode)}: the 0% BREAK debounce time', value=f'{measuring_0_percent_break}us')
        # --------------------------------------------------------------------------------------------------------------

        measured_0_percent_break_lower_bound = debounce_config.MIN_TIME_ON_RELEASE_US - tolerance
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the measured 0% BREAK debounce time {measuring_0_percent_break}us is greater '
                                  f'or equal to the expected time {measured_0_percent_break_lower_bound}us')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreaterEqual(a=measuring_0_percent_break, b=measured_0_percent_break_lower_bound,
                                msg='The measured 0% BREAK debounce time shall be greater or equal to the expected '
                                    f'time {measured_0_percent_break_lower_bound}us')
    # end def _0percent_break

    def _100percent_break(self, mode, repetition, ble_notification_queue=None):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break.

        :param mode: The power mode to test
        :type mode: ``DebounceConfiguration.Mode``
        :param repetition: The number of loops to perform
        :type repetition: ``int``
        :param ble_notification_queue: the BLE HID notification queue to check - OPTIONAL
        :type ble_notification_queue: ``queue | None``
        """
        (test_key,) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                      excluded_keys=HidData.get_not_single_action_keys())[0]
        test_step = DebounceConfiguration.STEP_US
        class_types = self._get_class_types()
        debounce_config, tolerance = DebounceConfiguration.get_debounce_config(test_case=self)
        break_detection_start = debounce_config.MIN_TIME_ON_RELEASE_US
        break_duration_end = debounce_config.MIN_TIME_ON_RELEASE_US + debounce_config.MAX_TIME_ON_RELEASE_US
        channel_to_use = self.current_channel.receiver_channel \
            if isinstance(self.current_channel, ThroughReceiverChannel) else self.current_channel

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Measure the 100% BREAK debounce time on the key id = {repr(test_key)} from '
                                 f'{break_detection_start}us to {break_duration_end}us and loop {repetition} times.')
        # --------------------------------------------------------------------------------------------------------------
        done = False
        measuring_100_percent_break = break_detection_start
        # Let the key in MAKE state before ding the test
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[test_key], delay=.1)
        sleep(.1)
        self._check_hid_report_by_key_id(key_id=test_key, action=MAKE, ble_notification_queue=ble_notification_queue)
        for break_duration in range(break_detection_start, break_duration_end, test_step):
            for count in range(repetition):
                self.kosmos.sequencer.offline_mode = True
                self.button_stimuli_emulator.multiple_keys_release(key_ids=[test_key], delay=break_duration / 10 ** 6)
                self.button_stimuli_emulator.multiple_keys_press(key_ids=[test_key])
                self.kosmos.sequencer.offline_mode = False
                self.kosmos.sequencer.play_sequence()
                sleep(.1)

                try:
                    self._check_hid_report_by_key_id(key_id=test_key, action=BREAK,
                                                     ble_notification_queue=ble_notification_queue)
                    self._check_hid_report_by_key_id(key_id=test_key, action=MAKE,
                                                     ble_notification_queue=ble_notification_queue)
                except (AssertionError, QueueEmpty):
                    # Update the measure_100_percent_break value
                    measuring_100_percent_break = break_duration + test_step

                    # Release the key
                    self.button_stimuli_emulator.multiple_keys_release(key_ids=[test_key], delay=.1)

                    # noinspection PyTypeChecker
                    self._clean_messages(channel_to_use=channel_to_use, class_types=class_types,
                                         ble_notification_queue=ble_notification_queue)

                    # Let the key in MAKE state before doing the test again
                    self.button_stimuli_emulator.multiple_keys_press(key_ids=[test_key], delay=.1)
                    self._check_hid_report_by_key_id(key_id=test_key, action=MAKE,
                                                     ble_notification_queue=ble_notification_queue)
                    break
                # end try
                
                done = (count == repetition - 1)
            # end for
            if done:
                break
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_metrics(
            self, key=f'{repr(mode)}: the 100% BREAK debounce time', value=f'{measuring_100_percent_break}us')
        # --------------------------------------------------------------------------------------------------------------

        measured_100_percent_break_upper_bound = debounce_config.MAX_TIME_ON_RELEASE_US + tolerance
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check the measured 100% BREAK debounce time {measuring_100_percent_break}us is '
                                  f'less or equal to the expected time {measured_100_percent_break_upper_bound}us')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLessEqual(a=measuring_100_percent_break, b=measured_100_percent_break_upper_bound,
                             msg='The measured 1000% BREAK debounce time shall be less or equal to the expected time '
                                 f'{measured_100_percent_break_upper_bound}us')
    # end def _100percent_break
# end class DebouncePerformanceTestCase


class DebouncePerformanceLS2TestCase(DebouncePerformanceTestCase):
    """
    Test case for debounce measurement through the LS2 communication protocol
    """
    @features('Debounce')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_make_in_active_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        self._0percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                            repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_LS2_ACTIVE_0001")
    # end def test_0percent_make_in_active_mode

    @features('Debounce')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_make_in_active_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        self._100percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                              repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_LS2_ACTIVE_0002")
    # end def test_100percent_make_in_active_mode

    @features('Debounce')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_break_in_active_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        self._0percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                             repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_LS2_ACTIVE_0003")
    # end def test_0percent_break_in_active_mode

    @features('Debounce')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_break_in_active_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        self._100percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                               repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_LS2_ACTIVE_0004")
    # end def test_100percent_break_in_active_mode

    @features('Debounce')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_make_in_run_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._0percent_make(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_LS2_RUN_0001")
    # end def test_0percent_make_in_run_mode

    @features('Debounce')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_make_in_run_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._100percent_make(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_LS2_RUN_0002")
    # end def test_100percent_make_in_run_mode

    @features('Debounce')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_break_in_run_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._0percent_break(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_LS2_RUN_0003")
    # end def test_0percent_break_in_run_mode

    @features('Debounce')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_break_in_run_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._100percent_break(mode=DebounceConfiguration.Mode.RUN,
                               repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_LS2_RUN_0004")
    # end def test_100percent_break_in_run_mode

    @features('Debounce')
    @features('Unifying')
    @level('Time-consuming')
    @services('ButtonPressed')
    def test_100percent_make_in_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 40 repetitions)
        """
        self.assertGreaterEqual(a=self.f.PRODUCT.DEVICE.F_MaxWaitSleep, b=0)
        self._100percent_make(mode=DebounceConfiguration.Mode.SLEEP,
                              repetition=DebounceConfiguration.Repetition.SLEEP_MODE)
        self.testCaseChecked("PER_DEBC_LS2_SLEEP_0001")
    # end def test_100percent_make_in_sleep_mode

    @features('Debounce')
    @features("Feature8040")
    @features("Keyboard")
    @features('Unifying')
    @level('Time-consuming')
    @services('ButtonPressed')
    def test_100percent_make_while_backlight_off_in_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        self.assertGreaterEqual(a=self.f.PRODUCT.DEVICE.F_MaxWaitSleep, b=0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the backlight')
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=self, brightness=self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_MinBrightness)

        self._100percent_make(mode=DebounceConfiguration.Mode.BACKLIGHT_OFF_SLEEP,
                              repetition=DebounceConfiguration.Repetition.BACKLIGHT_OFF_SLEEP_MODE)
        self.testCaseChecked("PER_DEBC_LS2_SLEEP_0002")
    # end def test_100percent_make_while_backlight_off_in_sleep_mode

    @features('Debounce')
    @features('Unifying')
    @features('Feature1830powerMode', 3)
    @level('Time-consuming')
    @services('ButtonPressed')
    def test_100percent_make_in_deep_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self,
                           msg="Power off all generic usb ports except LS2 receiver port to make sure no "
                               "interferences from other receivers.")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.UsbHubHelper.turn_off_all_generic_usb_ports(
            test_case=self, ports_to_turn_on=(PortConfiguration.PRE_PAIRED_RECEIVER_PORT,))
        self.post_requisite_turn_on_all_generic_usb_ports = True

        self._100percent_make(mode=DebounceConfiguration.Mode.DEEP_SLEEP,
                              repetition=DebounceConfiguration.Repetition.DEEP_SLEEP_MODE)
        self.testCaseChecked("PER_DEBC_LS2_DEEP_SLEEP_0001")
    # end def test_100percent_make_in_deep_sleep_mode

    @features('Debounce')
    @features('GamingDevice')
    @features('Mice')
    @features('Unifying')
    @level('Performance')
    @services('ButtonPressed')
    @services('OpticalSensor')
    def test_100percent_make_in_lift_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Lift mouse')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_motion_emulator = True
        self.motion_emulator.xy_motion(dx=0, lift=True)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        self._100percent_make(mode=DebounceConfiguration.Mode.LIFT,
                              repetition=DebounceConfiguration.Repetition.LIFT_MODE)
        self.testCaseChecked("PER_DEBC_LS2_LIFT_0001")
    # end def test_100percent_make_in_lift_mode
# end class DebouncePerformanceLS2TestCase


class DebouncePerformanceBLEProTestCase(DebouncePerformanceTestCase):
    """
    Test case for latency measurement through the BLE Pro communication protocol
    """

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_make_in_active_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        self._0percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                            repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_ACTIVE_0001")
    # end def test_0percent_make_in_active_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_make_in_active_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        self._100percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                              repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_ACTIVE_0002")
    # end def test_100percent_make_in_active_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_break_in_active_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        self._0percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                             repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_ACTIVE_0003")
    # end def test_0percent_break_in_active_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_break_in_active_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        self._100percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                               repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_ACTIVE_0004")
    # end def test_100percent_break_in_active_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_make_in_run_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._0percent_make(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_RUN_0001")
    # end def test_0percent_make_in_run_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_make_in_run_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._100percent_make(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_RUN_0002")
    # end def test_100percent_make_in_run_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_break_in_run_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._0percent_break(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_RUN_0003")
    # end def test_0percent_break_in_run_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_break_in_run_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._100percent_break(mode=DebounceConfiguration.Mode.RUN,
                               repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_RUN_0004")
    # end def test_100percent_break_in_run_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @level('Time-consuming')
    @services('ButtonPressed')
    def test_100percent_make_in_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 40 repetitions)
        """
        self.assertGreaterEqual(a=self.f.PRODUCT.DEVICE.F_MaxWaitSleep, b=0)
        self._100percent_make(mode=DebounceConfiguration.Mode.SLEEP,
                              repetition=DebounceConfiguration.Repetition.SLEEP_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_SLEEP_0001")
    # end def test_100percent_make_in_sleep_mode

    @features('Debounce')
    @features("BLEProProtocol")
    @features('Feature1830powerMode', 3)
    @level('Time-consuming')
    @services('ButtonPressed')
    def test_100percent_make_in_deep_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        self._100percent_make(mode=DebounceConfiguration.Mode.DEEP_SLEEP,
                              repetition=DebounceConfiguration.Repetition.DEEP_SLEEP_MODE)
        self.testCaseChecked("PER_DEBC_BPRO_DEEP_SLEEP_0001")
    # end def test_100percent_make_in_deep_sleep_mode
# end class DebouncePerformanceBLEProTestCase


class DebouncePerformanceBLETestCase(GattHIDSApplicationTestCases, DebouncePerformanceTestCase):
    """
    Test case for debounce measurement through BLE Direct connection
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        if self.f.PRODUCT.F_IsGaming:
            if self.f.PRODUCT.F_IsMice:
                self.notification_queue = self.prerequisite_report_input_test(ReportReferences.MOUSE_16BITS_INPUT)
            else:
                self.notification_queue = self.prerequisite_report_input_test(ReportReferences.GAMING_KEYBOARD_INPUT)
            # end if
        else:
            if self.f.PRODUCT.F_IsMice:
                self.notification_queue = self.prerequisite_report_input_test(ReportReferences.MOUSE_INPUT)
            else:
                self.notification_queue = self.prerequisite_report_input_test(ReportReferences.KEYBOARD_INPUT)
            # end if
        # end if
    # end def setUp

    def prerequisite_report_input_test(self, report_reference):
        """
        Prerequisite for an input report test.
        Get the whole gatt table
        Subscribe to all reports
        get the report notification queue from the report reference

        :param report_reference: The report reference
        :type report_reference: ``HexList``

        :return: the notification queue
        :rtype: ``queue``
        """
        self._prerequisite_gatt_table()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Get the notification queue for report {report_reference}")
        # --------------------------------------------------------------------------------------------------------------
        characteristic = BleProtocolTestUtils.get_hid_report(
            self, self.gatt_table, self.current_ble_device, report_reference)
        self.assertNotNone(characteristic, msg="Report not present")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Get the notification queue for report {report_reference}")
        # --------------------------------------------------------------------------------------------------------------
        notification_queue = BleProtocolTestUtils.direct_subscribe_notification(self, self.current_ble_device,
                                                                                characteristic)
        self.assertNotNone(notification_queue, msg="Report not present")
        return notification_queue
    # end def prerequisite_report_input_test

    @features('Debounce')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_make_in_active_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        self._0percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                            repetition=DebounceConfiguration.Repetition.ACTIVE_MODE,
                            ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_ACTIVE_0001")
    # end def test_0percent_make_in_active_mode

    @features('Debounce')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_make_in_active_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        self._100percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                              repetition=DebounceConfiguration.Repetition.ACTIVE_MODE,
                              ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_ACTIVE_0002")
    # end def test_100percent_make_in_active_mode

    @features('Debounce')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_break_in_active_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        self._0percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                             repetition=DebounceConfiguration.Repetition.ACTIVE_MODE,
                             ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_ACTIVE_0003")
    # end def test_0percent_break_in_active_mode

    @features('Debounce')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_break_in_active_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        self._100percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                               repetition=DebounceConfiguration.Repetition.ACTIVE_MODE,
                               ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_ACTIVE_0004")
    # end def test_100percent_break_in_active_mode

    @features('Debounce')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_make_in_run_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        self.notification_queue.get(timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

        self._0percent_make(mode=DebounceConfiguration.Mode.RUN,
                            repetition=DebounceConfiguration.Repetition.RUN_MODE,
                            ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_RUN_0001")
    # end def test_0percent_make_in_run_mode

    @features('Debounce')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_make_in_run_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        self.notification_queue.get(timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

        self._100percent_make(mode=DebounceConfiguration.Mode.RUN,
                              repetition=DebounceConfiguration.Repetition.RUN_MODE,
                              ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_RUN_0002")
    # end def test_100percent_make_in_run_mode

    @features('Debounce')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_break_in_run_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        self.notification_queue.get(timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

        self._0percent_break(mode=DebounceConfiguration.Mode.RUN,
                             repetition=DebounceConfiguration.Repetition.RUN_MODE,
                             ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_RUN_0003")
    # end def test_0percent_break_in_run_mode

    @features('Debounce')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_break_in_run_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        self.notification_queue.get(timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

        self._100percent_break(mode=DebounceConfiguration.Mode.RUN,
                               repetition=DebounceConfiguration.Repetition.RUN_MODE,
                               ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_RUN_0004")
    # end def test_100percent_break_in_run_mode

    @features('Debounce')
    @features("BLEProtocol")
    @level('Time-consuming')
    @services('ButtonPressed')
    def test_100percent_make_in_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 40 repetitions)
        """
        self.assertGreaterEqual(a=self.f.PRODUCT.DEVICE.F_MaxWaitSleep, b=0)
        self._100percent_make(mode=DebounceConfiguration.Mode.SLEEP,
                              repetition=DebounceConfiguration.Repetition.SLEEP_MODE,
                              ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_SLEEP_0001")
    # end def test_100percent_make_in_sleep_mode

    @features('Debounce')
    @features("Feature8040")
    @features("Keyboard")
    @features("BLEProtocol")
    @level('Time-consuming')
    @services('ButtonPressed')
    def test_100percent_make_while_backlight_off_in_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        self.assertGreaterEqual(a=self.f.PRODUCT.DEVICE.F_MaxWaitSleep, b=0)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Turn off the backlight')
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=self, brightness=self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_MinBrightness)

        self._100percent_make(mode=DebounceConfiguration.Mode.BACKLIGHT_OFF_SLEEP,
                              repetition=DebounceConfiguration.Repetition.BACKLIGHT_OFF_SLEEP_MODE)
        self.testCaseChecked("PER_DEBC_BLE_SLEEP_0002")
    # end def test_100percent_make_while_backlight_off_in_sleep_mode

    @features('Debounce')
    @features("BLEProtocol")
    @features('Feature1830powerMode', 3)
    @level('Time-consuming')
    @services('ButtonPressed')
    def test_100percent_make_in_deep_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self,
                           msg="Power off all generic usb ports to make sure no interferences from LS2 receiver.")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.UsbHubHelper.turn_off_all_generic_usb_ports(test_case=self)
        self.post_requisite_turn_on_all_generic_usb_ports = True

        self._100percent_make(mode=DebounceConfiguration.Mode.DEEP_SLEEP,
                              repetition=DebounceConfiguration.Repetition.DEEP_SLEEP_MODE,
                              ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_DEEP_SLEEP_0001")
    # end def test_100percent_make_in_deep_sleep_mode

    @features('Debounce')
    @features('GamingDevice')
    @features('Mice')
    @features("BLEProtocol")
    @level('Performance')
    @services('ButtonPressed')
    @services('OpticalSensor')
    def test_100percent_make_in_lift_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Lift mouse')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_motion_emulator = True
        self.motion_emulator.xy_motion(dx=0, lift=True)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        self._100percent_make(mode=DebounceConfiguration.Mode.LIFT,
                              repetition=DebounceConfiguration.Repetition.LIFT_MODE,
                              ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_DEBC_BLE_LIFT_0001")
    # end def test_100percent_make_in_lift_mode
# end class DebouncePerformanceBLETestCase


class DebouncePerformanceCrushTestCase(DebouncePerformanceTestCase):
    """
    Test case for debounce measurement through Crush receiver
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.LS2_CA_CRC24_FOR_CRUSH

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_0percent_make_in_active_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        self._0percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                            repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_ACTIVE_0001")
    # end def test_0percent_make_in_active_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_100percent_make_in_active_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        self._100percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                              repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_ACTIVE_0002")
    # end def test_100percent_make_in_active_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_0percent_break_in_active_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        self._0percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                             repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_ACTIVE_0003")
    # end def test_0percent_break_in_active_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_100percent_break_in_active_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        self._100percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                               repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_ACTIVE_0004")
    # end def test_100percent_break_in_active_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_0percent_make_in_run_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._0percent_make(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_RUN_0001")
    # end def test_0percent_make_in_run_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_100percent_make_in_run_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._100percent_make(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_RUN_0002")
    # end def test_100percent_make_in_run_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_0percent_break_in_run_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._0percent_break(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_RUN_0003")
    # end def test_0percent_break_in_run_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_100percent_break_in_run_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._100percent_break(mode=DebounceConfiguration.Mode.RUN,
                               repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_RUN_0004")
    # end def test_100percent_break_in_run_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @level('Time-consuming')
    @services('Crush')
    @services('ButtonPressed')
    def test_100percent_make_in_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 40 repetitions)
        """
        self.assertGreaterEqual(a=self.f.PRODUCT.DEVICE.F_MaxWaitSleep, b=0)
        self._100percent_make(mode=DebounceConfiguration.Mode.SLEEP,
                              repetition=DebounceConfiguration.Repetition.SLEEP_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_SLEEP_0001")
    # end def test_100percent_make_in_sleep_mode

    @features('Debounce')
    @features('Feature1817CrushSlotSupported')
    @features('Feature1830powerMode', 3)
    @level('Time-consuming')
    @services('Crush')
    @services('ButtonPressed')
    def test_100percent_make_in_deep_sleep_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self,
                           msg="Power off all generic usb ports except LS2 receiver port to make sure no "
                               "interferences from other receivers.")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.UsbHubHelper.turn_off_all_generic_usb_ports(
            test_case=self, ports_to_turn_on=(PortConfiguration.PRE_PAIRED_RECEIVER_PORT,))
        self.post_requisite_turn_on_all_generic_usb_ports = True

        self._100percent_make(mode=DebounceConfiguration.Mode.DEEP_SLEEP,
                              repetition=DebounceConfiguration.Repetition.DEEP_SLEEP_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_DEEP_SLEEP_0001")
    # end def test_100percent_make_in_deep_sleep_mode

    @features('Debounce')
    @features('GamingDevice')
    @features('Mice')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    @services('OpticalSensor')
    def test_100percent_make_in_lift_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Lift mouse')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_motion_emulator = True
        self.motion_emulator.xy_motion(dx=0, lift=True)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        self._100percent_make(mode=DebounceConfiguration.Mode.LIFT,
                              repetition=DebounceConfiguration.Repetition.LIFT_MODE)
        self.testCaseChecked("PER_DEBC_CRUSH_LIFT_0001")
    # end def test_100percent_make_in_lift_mode
# end class DebouncePerformanceCrushTestCase


class DebouncePerformanceUSBTestCase(DebouncePerformanceTestCase):
    """
    Test case for debounce measurement through USB
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB

    @features('Debounce')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_make_in_active_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        self._0percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                            repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_USB_ACTIVE_0001")
    # end def test_0percent_make_in_active_mode

    @features('Debounce')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_make_in_active_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        self._100percent_make(mode=DebounceConfiguration.Mode.ACTIVE,
                              repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_USB_ACTIVE_0002")
    # end def test_100percent_make_in_active_mode

    @features('Debounce')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_break_in_active_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        self._0percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                             repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_USB_ACTIVE_0003")
    # end def test_0percent_break_in_active_mode

    @features('Debounce')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_break_in_active_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        self._100percent_break(mode=DebounceConfiguration.Mode.ACTIVE,
                               repetition=DebounceConfiguration.Repetition.ACTIVE_MODE)
        self.testCaseChecked("PER_DEBC_USB_ACTIVE_0004")
    # end def test_100percent_break_in_active_mode

    @features('Debounce')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_make_in_run_mode(self):
        """
        Measure the 0% Make timing by decreasing the Make duration from the 100% Make value to the point at which there
        is never any make at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._0percent_make(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_USB_RUN_0001")
    # end def test_0percent_make_in_run_mode

    @features('Debounce')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_make_in_run_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._100percent_make(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_USB_RUN_0002")
    # end def test_100percent_make_in_run_mode

    @features('Debounce')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    def test_0percent_break_in_run_mode(self):
        """
        Measure the 0% Break timing by decreasing the Break duration from the 100% Break value to the point at which
        there is never any break at all. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._0percent_break(mode=DebounceConfiguration.Mode.RUN, repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_USB_RUN_0003")
    # end def test_0percent_break_in_run_mode

    @features('Debounce')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    def test_100percent_break_in_run_mode(self):
        """
        Measure the 100% Break timing by increasing the Break duration from the 0% Break value to the point at which
        there is always a break. (Measured over 100 repetitions)
        """
        holding_key = self._get_holding_key()
        self.post_requisite_release_holding_key = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Pres and hold the key: {repr(holding_key)} to keep device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[holding_key], delay=1)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(holding_key, MAKE))

        self._100percent_break(mode=DebounceConfiguration.Mode.RUN,
                               repetition=DebounceConfiguration.Repetition.RUN_MODE)
        self.testCaseChecked("PER_DEBC_USB_RUN_0004")
    # end def test_100percent_break_in_run_mode

    @features('Debounce')
    @features('GamingDevice')
    @features('Mice')
    @features('USB')
    @level('Performance')
    @services('ButtonPressed')
    @services('OpticalSensor')
    def test_100percent_make_in_lift_mode(self):
        """
        Measure the 100% Make timing by increasing the Make duration from the 0% Make value to the point at which there
        is always a make. (Measured over 20 repetitions)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Lift mouse')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_motion_emulator = True
        self.motion_emulator.xy_motion(dx=0, lift=True)
        self.motion_emulator.commit_actions()
        self.motion_emulator.prepare_sequence()

        self._100percent_make(mode=DebounceConfiguration.Mode.LIFT,
                              repetition=DebounceConfiguration.Repetition.LIFT_MODE)
        self.testCaseChecked("PER_DEBC_USB_LIFT_0001")
    # end def test_100percent_make_in_lift_mode
# end class DebouncePerformanceUSBTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
