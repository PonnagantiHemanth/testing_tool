#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hid.keyboard.analogkeys.functionality
:brief: ``AnalogKeys`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import warnings
from os.path import join
from random import choice
from time import sleep

# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import DfuStatusEvent
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.tools.dfufileparser import DfuFileParser
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.oobstateutils import OobStateTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hid.keyboard.analogkeys.analogkeys import AnalogKeysTestCase
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_50_MS_DELAY = 0.05         # This delay constant is used to wait between key combination press to be processed


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysFunctionalityTestCase(AnalogKeysTestCase):
    """
    Validate ``AnalogKeys`` functionality test cases
    """

    @features("Feature1B08")
    @level("Functionality")
    @services('DualKeyMatrix')
    def test_hidpp_request_in_analog_adjustment_mode(self):
        """
        Validate the users are able to send HID++ request and receive response when the device is in analog
        adjustment mode.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over mode in [Global Actuation Point mode, Global Rapid Trigger mode]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in ["Global Actuation Point mode", "Global Rapid Trigger mode"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enter {mode} (FN + {'F6' if mode == 'Global Actuation Point mode' else 'F7'})")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(_50_MS_DELAY)
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_F6 if mode == 'Global Actuation Point mode' else KEY_ID.KEYBOARD_F7)
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getDeviceNameCount request")
            # ----------------------------------------------------------------------------------------------------------
            response = DeviceTypeAndNameTestUtils.HIDppHelper.get_device_name_count(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the device name count is as expected from the response")
            # ----------------------------------------------------------------------------------------------------------
            marketing_name_count = len(self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME))
            self.assertEqual(expected=marketing_name_count, obtained=to_int(response.device_name_count),
                             msg=f"In {mode}, the device name count is not as expected")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Exit {mode} (ESC)")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_AKEY_0001", _AUTHOR)
    # end def test_hidpp_request_in_analog_adjustment_mode

    @features("Feature1B08")
    @level("Functionality")
    @services('PowerSupply')
    @services('DualKeyMatrix')
    def test_enter_deep_sleep_mode_in_analog_adjustment_mode(self):
        """
        Validate the device enters deep-sleep mode after power off timeout
        """
        power_off_timeout = self.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over mode in [Global Actuation Point mode, Global Rapid Trigger mode]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in ["Global Actuation Point mode", "Global Rapid Trigger mode"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enter {mode} (FN + {'F6' if mode == 'Global Actuation Point mode' else 'F7'})")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(_50_MS_DELAY)
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_F6 if mode == 'Global Actuation Point mode' else KEY_ID.KEYBOARD_F7)
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Wait {power_off_timeout} seconds to enter deep-sleep mode")
            # ----------------------------------------------------------------------------------------------------------
            sleep(power_off_timeout)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Measure the power consumption of the device")
            # ----------------------------------------------------------------------------------------------------------
            current = CommonBaseTestUtils.EmulatorHelper.get_current(
                self, delay=PowerModesTestUtils.CURRENT_MEASUREMENT_DELAY_TIME) * 1000

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the power consumption matches deep-sleep mode")
            # ----------------------------------------------------------------------------------------------------------
            expected_value = self.f.PRODUCT.FEATURES.COMMON.POWER_MODES.F_CurrentThresholdDeadMode
            self.assertLess(current, expected_value,
                            msg=f'The current value {current}uA shall be below {expected_value}uA')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Exit {mode} (ESC)")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_AKEY_0002", _AUTHOR)
    # end def test_enter_deep_sleep_mode_in_analog_adjustment_mode

    @features("Feature1B08")
    @features("Feature1830")
    @level("Functionality")
    @services('DualKeyMatrix')
    def test_exit_analog_adjustment_mode_after_deep_sleep(self):
        """
        Make the device enter analog adjustment mode, and validate the device backs to normal mode after the device
        was woken-up from deep-sleep mode
        """
        random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over mode in [Global Actuation Point mode, Global Rapid Trigger mode]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in ["Global Actuation Point mode", "Global Rapid Trigger mode"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enter {mode} (FN + {'F6' if mode == 'Global Actuation Point mode' else 'F7'})")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(_50_MS_DELAY)
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_F6 if mode == 'Global Actuation Point mode' else KEY_ID.KEYBOARD_F7)
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 0x1830.setPowerMode request to enter deep-sleep mode")
            # ----------------------------------------------------------------------------------------------------------
            PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform an user action to wake-up the device")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.user_action()
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on a random selected analog key: {random_selected_key!r}")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the corresponding HID reports are received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_AKEY_0003", _AUTHOR)
    # end def test_exit_analog_adjustment_mode_after_deep_sleep

    @features("Feature1B08")
    @level("Functionality")
    @services('DualKeyMatrix')
    def test_exit_analog_adjustment_mode_after_power_cycle(self):
        """
        Make the device enter analog adjustment mode, and validate the device backs to normal mode after a device
        power cycle
        """
        random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over mode in [Global Actuation Point mode, Global Rapid Trigger mode]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in ["Global Actuation Point mode", "Global Rapid Trigger mode"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enter {mode} (FN + {'F6' if mode == 'Global Actuation Point mode' else 'F7'})")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(_50_MS_DELAY)
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_F6 if mode == 'Global Actuation Point mode' else KEY_ID.KEYBOARD_F7)
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Power OFF -> ON the device")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on a random selected analog key: {random_selected_key}")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            self.button_stimuli_emulator.keystroke(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the corresponding HID reports are received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_AKEY_0004", _AUTHOR)
    # end def test_exit_analog_adjustment_mode_after_power_cycle

    @features("Feature1B08")
    @features("Feature00D0")
    @level("Functionality")
    @services('DualKeyMatrix')
    def test_exit_analog_adjustment_mode_after_dfu(self):
        """
        Make the device enter analog adjustment mode, and validate the device backs to normal mode after a device DFU
        """
        random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over mode in [Global Actuation Point mode, Global Rapid Trigger mode]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in ["Global Actuation Point mode", "Global Rapid Trigger mode"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enter {mode} (FN + {'F6' if mode == 'Global Actuation Point mode' else 'F7'})")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(_50_MS_DELAY)
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_F6 if mode == 'Global Actuation Point mode' else KEY_ID.KEYBOARD_F7)
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enter bootloader mode')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.jump_on_bootloader(test_case=self)
            self.post_requisite_program_mcu_initial_state = True

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform DFU")
            # ----------------------------------------------------------------------------------------------------------
            dfu_file = os.path.join(TESTS_PATH, "DFU_FILES",
                                    self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName)
            LogHelper.log_info(self, f'DFU file: {dfu_file}')
            self.post_requisite_reload_nvs = True
            self._perform_dfu()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text="Force target on application")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)
            DfuTestUtils.force_target_on_application(test_case=self, check_required=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on a random selected analog key: {random_selected_key}")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            self.button_stimuli_emulator.keystroke(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the corresponding HID reports are received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_AKEY_0005", _AUTHOR)
    # end def test_exit_analog_adjustment_mode_after_dfu

    @features("Feature1B08")
    @features("Feature1805")
    @level("Functionality")
    @services('DualKeyMatrix')
    def test_exit_analog_adjustment_mode_after_oob(self):
        """
        Make the device enter analog adjustment mode, and validate the device backs to normal mode after setting
        device OOB
        """
        random_selected_key = choice(list(self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over mode in [Global Actuation Point mode, Global Rapid Trigger mode]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in ["Global Actuation Point mode", "Global Rapid Trigger mode"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enter {mode} (FN + {'F6' if mode == 'Global Actuation Point mode' else 'F7'})")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(_50_MS_DELAY)
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_F6 if mode == 'Global Actuation Point mode' else KEY_ID.KEYBOARD_F7)
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set device OOB via 0x1805.setOob")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            try:
                OobStateTestUtils.HIDppHelper.set_oob_state(self)
            except AssertionError:
                warnings.warn("There is no set_oob_state response received from the device")
            # end try

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Perform a device hardware reset")
            # ----------------------------------------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Perform a keystroke on a random selected analog key: {random_selected_key}")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
            self.button_stimuli_emulator.keystroke(key_id=random_selected_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the corresponding HID reports are received from the device")
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(random_selected_key, BREAK))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_AKEY_0006", _AUTHOR)
    # end def test_exit_analog_adjustment_mode_after_oob

    @features("Feature1B08")
    @features("Feature8040")
    @level("Functionality")
    @services('DualKeyMatrix')
    def test_adjust_brightness_in_analog_adjustment_mode(self):
        """
        Make the device enter analog adjustment mode, and validate the brightness of the device is not able changed when
         pressing brightness keys
        """
        brightness_controls = BrightnessControlTestUtils.get_standard_physical_brightness_controls(test_case=self)
        fn_brightness_controls = \
            BrightnessControlTestUtils.get_functional_physical_brightness_controls(test_case=self)
        controls = fn_brightness_controls if len(fn_brightness_controls) > 0 else brightness_controls
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over mode in [Global Actuation Point mode, Global Rapid Trigger mode]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in ["Global Actuation Point mode", "Global Rapid Trigger mode"]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Enter {mode} (FN + {'F6' if mode == 'Global Actuation Point mode' else 'F7'})")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(_50_MS_DELAY)
            self.button_stimuli_emulator.keystroke(
                key_id=KEY_ID.KEYBOARD_F6 if mode == 'Global Actuation Point mode' else KEY_ID.KEYBOARD_F7)
            self.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Press a brightness control key")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=controls[0])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send 0x8040.getBrightness request to get the current brightness")
            # ----------------------------------------------------------------------------------------------------------
            response = BrightnessControlTestUtils.HIDppHelper.get_brightness(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the brightness remains default brightness from the response")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_DefaultBrightness,
                             obtained=to_int(response.brightness),
                             msg=f"The brightness is not expected to be changed in: {mode}")

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Exit {mode} (ESC)")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_ESCAPE)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_AKEY_0007", _AUTHOR)
    # end def test_adjust_brightness_in_analog_adjustment_mode

    def _wait_for_dfu_status(self, dfu_status_response, status, packet_number=None):
        """
        Wait for a DFU status (an optionally a packet number) either from the given response or from an event
        received later.

        :param dfu_status_response: Current response of the request
        :type dfu_status_response: ``DfuStatusResponse``
        :param status: Expected status (see in DfuStatusResponse.StatusValue)
        :type status: ``tuple`` or ``int``
        :param packet_number: Expected packet number - OPTIONAL
        :type packet_number: ``int`` or ``HexList``

        :raise ``AssertionError``: if the status differs from the expected one
        """
        while int(Numeral(dfu_status_response.status)) in DfuStatusResponse.StatusValue.WAIT_FOR_EVENT:
            message = ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, timeout=30)
            if isinstance(message, DfuStatusEvent):
                dfu_status_response = message
            # end if
        # end while

        self.assertTrue(expr=int(Numeral(dfu_status_response.status)) in status,
                        msg="The Dfu status differs from the expected one, received "
                            f"{int(Numeral(dfu_status_response.status))} and expected {status}")

        if packet_number is not None:
            self.assertEqual(expected=int(Numeral(packet_number)),
                             obtained=int(Numeral(dfu_status_response.pkt_nb)),
                             msg="The Dfu packet_number differs from the expected one")
        # end if
    # end def _wait_for_dfu_status

    def _perform_first_command_of_dfu(self):
        """
        Perform the first command of DFU: DfuStart. It will also create the DFU file parser objet

        :return: The DFU file parser object created
        :rtype: ``DfuFileParser``

        :raise ``AssertionError``: if the version is not specified in the product settings
        :raise ``ValueError``: if the target type is unknown
        """
        # Get the supported version
        if self.f.PRODUCT.FEATURES.COMMON.DFU.F_Version_0:
            dfu_feature_version = 0
        elif self.f.PRODUCT.FEATURES.COMMON.DFU.F_Version_1:
            dfu_feature_version = 1
        elif self.f.PRODUCT.FEATURES.COMMON.DFU.F_Version_2:
            dfu_feature_version = 2
        elif self.f.PRODUCT.FEATURES.COMMON.DFU.F_Version_3:
            dfu_feature_version = 3
        else:
            assert False, "Version not specified"
        # end if

        self.bootloader_dfu_feature_id = ChannelUtils.update_feature_mapping(test_case=self, feature_id=Dfu.FEATURE_ID)

        if self.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            dfu_file_name = self.f.PRODUCT.FEATURES.COMMON.DFU.F_ApplicationDfuFileName
        elif self.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            dfu_file_name = self.f.SHARED.DEVICES.F_DeviceApplicationDfuFileName
        else:
            raise ValueError(f"Unknown target type: {self.config_manager.current_target}")
        # end if

        dfu_file_parser = DfuFileParser.parse_dfu_file(
            dfu_file_path=join(TESTS_PATH, "DFU_FILES", dfu_file_name),
            device_index=ChannelUtils.get_device_index(test_case=self),
            dfu_feature_index=int(Numeral(self.bootloader_dfu_feature_id)),
            dfu_feature_version=dfu_feature_version)

        self.device_memory_manager.read_nvs()
        self.post_requisite_program_device_mcu_initial_state = True
        self.post_requisite_device_restart_in_main_application = False

        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.dfu_start_command,
            response_queue_name=HIDDispatcher.QueueName.COMMON, response_class_type=DfuStatusResponse)

        self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                  status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                  packet_number=0)

        return dfu_file_parser
    # end def _perform_first_command_of_dfu

    def _perform_dfu(self):
        """
        Perform a DFU, if log_step and log_check are <=0, there is no log message.
        """
        dfu_file_parser = self._perform_first_command_of_dfu()
        sequence_number = 1

        for (cmd_1, program_data_list) in dfu_file_parser.command_1:
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=cmd_1, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                      status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                      packet_number=sequence_number)

            sequence_number += 1

            for i in range(len(program_data_list)):
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=program_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                          status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                          packet_number=sequence_number)

                sequence_number += 1
            # end for
        # end for

        for (cmd_2, check_data_list) in dfu_file_parser.command_2:
            dfu_status_response = ChannelUtils.send(
                test_case=self, report=cmd_2, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=DfuStatusResponse)

            self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                      status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                      packet_number=sequence_number)

            sequence_number += 1

            for i in range(len(check_data_list)):
                dfu_status_response = ChannelUtils.send(
                    test_case=self, report=check_data_list[i], response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=DfuStatusResponse)

                self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                          status=DfuStatusResponse.StatusValue.PACKET_SUCCESS,
                                          packet_number=sequence_number)

                sequence_number += 1
            # end for
        # end for

        dfu_status_response = ChannelUtils.send(
            test_case=self, report=dfu_file_parser.command_3, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=DfuStatusResponse)

        self._wait_for_dfu_status(dfu_status_response=dfu_status_response,
                                  status=DfuStatusResponse.StatusValue.DFU_SUCCESS)

    # end def _perform_dfu
# end class AnalogKeysFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
