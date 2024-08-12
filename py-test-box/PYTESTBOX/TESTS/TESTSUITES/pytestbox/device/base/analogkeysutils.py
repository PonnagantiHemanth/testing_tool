#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.analogkeysutils
:brief: Helpers for ``AnalogKeys`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/03/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import IntEnum
from enum import unique
from random import choice
from random import sample
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hid import HidConsumer
from pyhid.hid import HidKeyboardBitmap
from pyhid.hid import HidMouse
from pyhid.hid.usbhidusagetable import KEYBOARD_HID_USAGE_TO_KEY_ID_MAP
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.analogkeys import AnalogKeys
from pyhid.hidpp.features.common.analogkeys import AnalogKeysFactory
from pyhid.hidpp.features.common.analogkeys import GetCapabilitiesResponse
from pyhid.hidpp.features.common.analogkeys import GetRapidTriggerStateResponse
from pyhid.hidpp.features.common.analogkeys import KeyTravelChangeEvent
from pyhid.hidpp.features.common.analogkeys import SetKeyTravelEventStateResponse
from pyhid.hidpp.features.common.analogkeys import SetRapidTriggerStateResponse
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.analogkeysprofileformat import ActionAssignment
from pylibrary.mcu.analogkeysprofileformat import ActionGroup
from pylibrary.mcu.analogkeysprofileformat import ActuationConfigurationTable
from pylibrary.mcu.analogkeysprofileformat import ActuationPointPerKey
from pylibrary.mcu.analogkeysprofileformat import MultiActionConfigurationTable
from pylibrary.mcu.analogkeysprofileformat import RapidTriggerConfigurationTable
from pylibrary.mcu.analogkeysprofileformat import SensitivityPerKey
from pylibrary.mcu.fkcprofileformat import DirectoryFile
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_50_MS_DELAY = 0.05  # This delay constant is used to wait between key combination press to be processed


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``AnalogKeys`` feature
    """

    @unique
    class Status(IntEnum):
        """
        The state of either the key travel or rapid trigger options
        """
        DISABLE = 0
        ENABLE = 1
    # end class Status

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.ANALOG_KEYS
            return {
                "analog_key_config_file_ver": (cls.check_analog_key_config_file_ver, config.F_AnalogKeyConfigFileVer),
                "analog_key_config_file_maxsize": (cls.check_analog_key_config_file_maxsize,
                                                   config.F_AnalogKeyConfigFileMaxsize),
                "analog_key_level_resolution": (cls.check_analog_key_level_resolution,
                                                config.F_AnalogKeyLevelResolution),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_analog_key_config_file_ver(test_case, response, expected):
            """
            Check analog_key_config_file_ver field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert analog_key_config_file_ver that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The analog_key_config_file_ver shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.analog_key_config_file_ver),
                msg="The analog_key_config_file_ver parameter differs from the one expected")
        # end def check_analog_key_config_file_ver

        @staticmethod
        def check_analog_key_config_file_maxsize(test_case, response, expected):
            """
            Check analog_key_config_file_maxsize field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert analog_key_config_file_maxsize that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The analog_key_config_file_maxsize shall be (a) defined in the DUT settings (b) "
                    "passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.analog_key_config_file_maxsize),
                msg="The analog_key_config_file_maxsize parameter differs from the one expected")
        # end def check_analog_key_config_file_maxsize

        @staticmethod
        def check_analog_key_level_resolution(test_case, response, expected):
            """
            Check analog_key_level_resolution field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert analog_key_level_resolution that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The analog_key_level_resolution shall be (a) defined in the DUT settings (b) "
                    "passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.analog_key_level_resolution),
                msg="The analog_key_level_resolution parameter differs from the one expected")
        # end def check_analog_key_level_resolution

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class GetCapabilitiesResponseChecker

    class RapidTriggerSettingsChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``RapidTriggerSettings``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reserved": (cls.check_reserved, 0),
                "rapid_trigger_state": (cls.check_rapid_trigger_state,
                                        test_case.f.PRODUCT.FEATURES.COMMON.ANALOG_KEYS.F_RapidTriggerState)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: RapidTriggerSettings to check
            :type bitmap: ``AnalogKeys.RapidTriggerSettings``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_rapid_trigger_state(test_case, bitmap, expected):
            """
            Check rapid_trigger_state field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: RapidTriggerSettings to check
            :type bitmap: ``AnalogKeys.RapidTriggerSettings``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rapid_trigger_state that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rapid_trigger_state),
                msg="The rapid_trigger_state parameter differs from the one expected")
        # end def check_rapid_trigger_state
    # end class RapidTriggerSettingsChecker

    class GetRapidTriggerStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetRapidTriggerStateResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "rapid_trigger_settings": (
                    cls.check_rapid_trigger_settings,
                    AnalogKeysTestUtils.RapidTriggerSettingsChecker.get_default_check_map(test_case)),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rapid_trigger_settings(test_case, message, expected):
            """
            Check ``rapid_trigger_settings``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetRapidTriggerStateResponse to check
            :type message: ``GetRapidTriggerStateResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            AnalogKeysTestUtils.RapidTriggerSettingsChecker.check_fields(
                test_case, message.rapid_trigger_settings, AnalogKeys.RapidTriggerSettings, expected)
        # end def check_rapid_trigger_settings

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetRapidTriggerStateResponse to check
            :type response: ``GetRapidTriggerStateResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class GetRapidTriggerStateResponseChecker

    class SetRapidTriggerStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetRapidTriggerStateResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "rapid_trigger_settings": (
                    cls.check_rapid_trigger_settings,
                    AnalogKeysTestUtils.RapidTriggerSettingsChecker.get_default_check_map(test_case)),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_rapid_trigger_settings(test_case, message, expected):
            """
            Check ``rapid_trigger_settings``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: SetRapidTriggerStateResponse to check
            :type message: ``SetRapidTriggerStateResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            AnalogKeysTestUtils.RapidTriggerSettingsChecker.check_fields(
                test_case, message.rapid_trigger_settings, AnalogKeys.RapidTriggerSettings, expected)
        # end def check_rapid_trigger_settings

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetRapidTriggerStateResponse to check
            :type response: ``SetRapidTriggerStateResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class SetRapidTriggerStateResponseChecker

    class KeyTravelSettingsChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``KeyTravelSettings``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reserved": (cls.check_reserved, 0),
                "key_travel_event_state": (cls.check_key_travel_event_state, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTravelSettings to check
            :type bitmap: ``AnalogKeys.KeyTravelSettings``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_key_travel_event_state(test_case, bitmap, expected):
            """
            Check key_travel_event_state field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: KeyTravelSettings to check
            :type bitmap: ``AnalogKeys.KeyTravelSettings``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_travel_event_state that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.key_travel_event_state),
                msg="The key_travel_event_state parameter differs from the one expected")
        # end def check_key_travel_event_state
    # end class KeyTravelSettingsChecker

    class SetKeyTravelEventStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetKeyTravelEventStateResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "key_travel_settings": (cls.check_key_travel_settings,
                                        AnalogKeysTestUtils.KeyTravelSettingsChecker.get_default_check_map(test_case)),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_key_travel_settings(test_case, message, expected):
            """
            Check ``key_travel_settings``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: SetKeyTravelEventStateResponse to check
            :type message: ``SetKeyTravelEventStateResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            AnalogKeysTestUtils.KeyTravelSettingsChecker.check_fields(
                test_case, message.key_travel_settings, AnalogKeys.KeyTravelSettings, expected)
        # end def check_key_travel_settings

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetKeyTravelEventStateResponse to check
            :type response: ``SetKeyTravelEventStateResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class SetKeyTravelEventStateResponseChecker

    class KeyTravelChangeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``KeyTravelChangeEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "key_cidx": (cls.check_key_cidx, None),
                "key_travel": (cls.check_key_travel, None),
                "reserved": (cls.check_reserved, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_key_cidx(test_case, event, expected):
            """
            Check key_cidx field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyTravelChangeEvent to check
            :type event: ``KeyTravelChangeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_cidx that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The key_cidx shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_cidx),
                msg="The key_cidx parameter differs from the one expected")
        # end def check_key_cidx

        @staticmethod
        def check_key_travel(test_case, event, expected):
            """
            Check key_travel field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyTravelChangeEvent to check
            :type event: ``KeyTravelChangeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert key_travel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The key_travel shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.key_travel),
                msg="The key_travel parameter differs from the one expected")
        # end def check_key_travel

        @staticmethod
        def check_reserved(test_case, event, expected):
            """
            Check reserved field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyTravelChangeEvent to check
            :type event: ``KeyTravelChangeEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved
    # end class KeyTravelChangeEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=AnalogKeys.FEATURE_ID,
                           factory=AnalogKeysFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetCapabilitiesResponse (if not error)
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_1b08_index, feature_1b08, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b08.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_1b08_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1b08.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_capabilities_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1b08_index, feature_1b08, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b08.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_1b08_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def get_rapid_trigger_state(cls, test_case, device_index=None, port_index=None, software_id=None,
                                    padding=None):
            """
            Process ``GetRapidTriggerState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetRapidTriggerStateResponse (if not error)
            :rtype: ``GetRapidTriggerStateResponse``
            """
            feature_1b08_index, feature_1b08, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b08.get_rapid_trigger_state_cls(
                device_index=device_index,
                feature_index=feature_1b08_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1b08.get_rapid_trigger_state_response_cls)
        # end def get_rapid_trigger_state

        @classmethod
        def get_rapid_trigger_state_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetRapidTriggerState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1b08_index, feature_1b08, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b08.get_rapid_trigger_state_cls(
                device_index=device_index,
                feature_index=feature_1b08_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_rapid_trigger_state_and_check_error

        @classmethod
        def set_rapid_trigger_state(cls, test_case, rapid_trigger_state, device_index=None, port_index=None,
                                    software_id=None, reserved=None):
            """
            Process ``SetRapidTriggerState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param rapid_trigger_state: Rapid Trigger State
            :type rapid_trigger_state: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: SetRapidTriggerStateResponse (if not error)
            :rtype: ``SetRapidTriggerStateResponse``
            """
            feature_1b08_index, feature_1b08, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b08.set_rapid_trigger_state_cls(
                device_index=device_index,
                feature_index=feature_1b08_index,
                rapid_trigger_state=rapid_trigger_state)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if reserved is not None:
                report.reserved = reserved
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1b08.set_rapid_trigger_state_response_cls)
        # end def set_rapid_trigger_state

        @classmethod
        def set_rapid_trigger_state_and_check_error(
                cls, test_case, error_codes, rapid_trigger_state, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetRapidTriggerState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param rapid_trigger_state: Rapid Trigger State
            :type rapid_trigger_state: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1b08_index, feature_1b08, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b08.set_rapid_trigger_state_cls(
                device_index=device_index,
                feature_index=feature_1b08_index,
                rapid_trigger_state=rapid_trigger_state)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_rapid_trigger_state_and_check_error

        @classmethod
        def set_key_travel_event_state(cls, test_case, key_travel_event_state, device_index=None, port_index=None,
                                       software_id=None, reserved=None):
            """
            Process ``SetKeyTravelEventState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param key_travel_event_state: Key Travel Event State
            :type key_travel_event_state: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: SetKeyTravelEventStateResponse (if not error)
            :rtype: ``SetKeyTravelEventStateResponse``
            """
            feature_1b08_index, feature_1b08, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b08.set_key_travel_event_state_cls(
                device_index=device_index,
                feature_index=feature_1b08_index,
                key_travel_event_state=key_travel_event_state)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if reserved is not None:
                report.reserved = reserved
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1b08.set_key_travel_event_state_response_cls)
        # end def set_key_travel_event_state

        @classmethod
        def set_key_travel_event_state_and_check_error(
                cls, test_case, error_codes, key_travel_event_state, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetKeyTravelEventState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param key_travel_event_state: Key Travel Event State
            :type key_travel_event_state: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_1b08_index, feature_1b08, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b08.set_key_travel_event_state_cls(
                device_index=device_index,
                feature_index=feature_1b08_index,
                key_travel_event_state=key_travel_event_state)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_key_travel_event_state_and_check_error

        @classmethod
        def key_travel_change_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``KeyTravelChangeEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: KeyTravelChangeEvent
            :rtype: ``KeyTravelChangeEvent``
            """
            _, feature_1b08, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1b08.key_travel_change_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def key_travel_change_event
    # end class HIDppHelper

    class AnalogKeysHelper:
        """
        Helper for configuring Actuation, Rapid Trigger and Multi-Action tables

        Ref: https://docs.google.com/document/d/1yuMIIuF8-0v5ZQzZvzKoLQ1Y3GdEchM0E3pnrNDgUfo/view#heading=h.a9wxne5h3b7o
        """
        # Unit: 0.1 mm
        MAX_ACTUATION_POINT = 40            # 4.0 mm
        MIN_ACTUATION_POINT = 1             # 0.1 mm
        RESOLUTION_PER_STEP = 1             # 0.1 mm
        MAX_SENSITIVITY = 20                # 2.0 mm
        MIN_SENSITIVITY = 1                 # 0.1 mm
        RELEASE_POINT_DELTA = 3             # 0.3 mm
        MA_RELEASE_POINT_DELTA = 2          # 0.2 mm
        MA_MAX_FIRST_ACTUATION_POINT = 35   # 3.5 mm

        @classmethod
        def create_actuation_point_configuration_per_key(cls, test_case, keys_and_actuation_points):
            """
            Create actuation point configurations per the input KEY_ID and actuation point list.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param keys_and_actuation_points: A dictionary mapping the trigger keys and actuation points
            :type keys_and_actuation_points: ``dict``

            :return: A list of configurations of actuation point per key
            :rtype: ``list[ActuationPointPerKey]``

            :raise ``AssertionError``: If the input 'keys_and_actuation_points' is empty
            """
            assert len(keys_and_actuation_points) > 0, \
                "The input 'keys_and_actuation_points' should not be a empty list."

            actuation_point_per_keys = []
            for item in keys_and_actuation_points.items():
                actuation_point_per_keys.append(
                    ActuationPointPerKey(
                        trigger_cidx=ControlListTestUtils.key_id_to_cidx(test_case=test_case, key_id=item[0]),
                        actuation_point=item[1]))
            # end for

            return actuation_point_per_keys
        # end def create_actuation_point_configuration_per_key

        @classmethod
        def create_actuation_point_table(cls, test_case, directory, actuation_point_per_keys=None,
                                         number_of_key_to_be_random_generated=None):
            """
            Create an Actuation configuration table by the preset data or generate automatically and randomly

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param actuation_point_per_keys: Preset actuation point per keys - OPTIONAL
            :type actuation_point_per_keys: ``ActuationPointPerKey | list[ActuationPointPerKey] | None``
            :param number_of_key_to_be_random_generated: Number of keys to be automated generated randomly - OPTIONAL
            :type number_of_key_to_be_random_generated: ``int | None``

            :return: Actuation configuration table
            :rtype: ``ActuationConfigurationTable``
            """

            if actuation_point_per_keys:
                new_table = ActuationConfigurationTable(rows=actuation_point_per_keys)
            elif number_of_key_to_be_random_generated:
                actuation_point_per_keys = []
                valid_actuation_points = range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_ACTUATION_POINT,
                                               AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT)
                random_selected_keys = sample(list(
                    test_case.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()),
                    number_of_key_to_be_random_generated)
                for key in random_selected_keys:
                    actuation_point_per_keys.append(ActuationPointPerKey(
                        trigger_cidx=ControlListTestUtils.key_id_to_cidx(test_case=test_case, key_id=key),
                        actuation_point=choice(valid_actuation_points)))
                # end for
                new_table = ActuationConfigurationTable(rows=actuation_point_per_keys)
            else:
                new_table = ActuationConfigurationTable(rows=[])
            # end if

            new_table.register(directory=directory)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f"Actuation Point table: {new_table}")
            # ----------------------------------------------------------------------------------------------------------

            return new_table
        # end def create_actuation_point_table

        @classmethod
        def create_sensitivity_configuration_per_key(cls, test_case, keys_and_sensitivities):
            """
            Create rapid trigger sensitivity configurations given the KEY_ID and sensitivity list inputs.

            NB: The per key sensitivity is not available on version 0 of Analog Keys feature

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param keys_and_sensitivities: A dictionary mapping the trigger keys and sensitivities
            :type keys_and_sensitivities: ``dict``

            :return: A list of configurations of sensitivity per key
            :rtype: ``list[SensitivityPerKey]``

            :raise ``AssertionError``: If the input 'keys_and_sensitivities' is empty
            """
            assert len(keys_and_sensitivities) > 0, \
                "The input 'keys_and_sensitivities' should not be a empty list."

            sensitivity_per_keys = []
            for item in keys_and_sensitivities.items():
                sensitivity_per_keys.append(
                    SensitivityPerKey(
                        trigger_cidx=ControlListTestUtils.key_id_to_cidx(test_case=test_case, key_id=item[0]),
                        sensitivity=item[1]))
            # end for

            return sensitivity_per_keys
        # end def create_sensitivity_configuration_per_key

        @classmethod
        def create_rapid_trigger_table(cls, test_case, directory, sensitivity_per_keys=None,
                                       number_of_key_to_be_random_generated=None):
            """
            Create a Rapid Trigger configuration table by the preset data or generate automatically and randomly

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param sensitivity_per_keys: Preset sensitivity - OPTIONAL
            :type sensitivity_per_keys: ``SensitivityPerKey | list[SensitivityPerKey] | None``
            :param number_of_key_to_be_random_generated: Number of keys to be automated generated randomly - OPTIONAL
            :type number_of_key_to_be_random_generated: ``int | None``

            :return: Rapid trigger configuration table
            :rtype: ``RapidTriggerConfigurationTable``
            """

            if sensitivity_per_keys:
                new_table = RapidTriggerConfigurationTable(rows=sensitivity_per_keys)
            elif number_of_key_to_be_random_generated:
                sensitivity_per_keys = []
                valid_sensitivities = range(AnalogKeysTestUtils.AnalogKeysHelper.MIN_SENSITIVITY,
                                            AnalogKeysTestUtils.AnalogKeysHelper.MAX_SENSITIVITY)
                random_selected_keys = sample(list(
                    test_case.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()),
                    number_of_key_to_be_random_generated)
                for key in random_selected_keys:
                    sensitivity_per_keys.append(SensitivityPerKey(
                        trigger_cidx=ControlListTestUtils.key_id_to_cidx(test_case=test_case, key_id=key),
                        sensitivity=choice(valid_sensitivities)))
                # end for
                new_table = RapidTriggerConfigurationTable(rows=sensitivity_per_keys)
            else:
                new_table = RapidTriggerConfigurationTable(rows=[])
            # end if

            new_table.register(directory=directory)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f"Rapid Trigger table: {new_table}")
            # ----------------------------------------------------------------------------------------------------------

            return new_table
        # end def create_rapid_trigger_table

        @classmethod
        def create_multi_action_table(cls, test_case, directory, preset_groups=None,
                                      number_of_key_to_be_random_generated=None,
                                      global_actuation_point=None):
            """
            Create a Multi Action table by the preset data or generate automatically and randomly

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param directory: ``DirectoryFile`` instance
            :type directory: ``DirectoryFile``
            :param preset_groups: The preset action groups - OPTIONAL
            :type preset_groups: ``list[ActionGroup] | None``
            :param number_of_key_to_be_random_generated: Number of keys to be automated generated randomly - OPTIONAL
            :type number_of_key_to_be_random_generated: ``int | None``
            :param global_actuation_point: Global actuation point - OPTIONAL
            :type global_actuation_point: ``int | None``

            :return: ``MultiActionConfigurationTable`` instance
            :rtype: ``MultiActionConfigurationTable``

            :raise ``TypeError``: If the data type of preset assignment is invalid
            """
            if preset_groups:
                if isinstance(preset_groups, ActionGroup):
                    preset_groups = [preset_groups]
                # end if

                if not all(isinstance(preset_group, ActionGroup) for preset_group in preset_groups):
                    raise TypeError(
                        'Unsupported data type(s) to create Multi-Action table: '
                        f'{[type(item) for item in preset_groups if not isinstance(item, ActionGroup)]}')
                else:
                    for preset_group in preset_groups:
                        preset_group.sort()
                    # end for
                # end if

                table = MultiActionConfigurationTable(
                    groups=preset_groups,
                    cid_list=ControlListTestUtils.get_cid_list_from_device(test_case=test_case))
            elif number_of_key_to_be_random_generated:
                groups = []
                global_actuation_point = global_actuation_point if global_actuation_point else \
                    test_case.f.PRODUCT.FEATURES.COMMON.ANALOG_KEYS.F_DefaultActuationPoint
                random_selected_keys = sample(list(
                    test_case.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()),
                    number_of_key_to_be_random_generated)
                for key in random_selected_keys:
                    groups.append(ActionGroup(
                        trigger_key=key,
                        second_actuation_point=choice(
                            range(global_actuation_point + AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA,
                                  AnalogKeysTestUtils.AnalogKeysHelper.MAX_ACTUATION_POINT)),
                        random_assignments=True))
                # end for
                table = MultiActionConfigurationTable(
                    groups=groups, cid_list=ControlListTestUtils.get_cid_list_from_device(test_case=test_case))
            else:
                table = MultiActionConfigurationTable(
                    groups=[], cid_list=ControlListTestUtils.get_cid_list_from_device(test_case=test_case))
            # end if

            table.register(directory=directory)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f"Multi-Action table: {table}")
            # ----------------------------------------------------------------------------------------------------------

            return table
        # end def create_multi_action_table

        @classmethod
        def analog_keystroke(cls, test_case, key_id, actuation_point):
            """
            Perform a keystroke on the input analog key, and check there is no report received at AP - 1

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param key_id: Analog Key ID
            :type key_id: ``KEY_ID``
            :param actuation_point: Actuation Point
            :type actuation_point: ``int``
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case,
                "Perform a keystroke on the input analog key, and check there is no report received at AP - 1")
            # ----------------------------------------------------------------------------------------------------------
            # Perform a key press with displacement: AP - 1
            test_case.button_stimuli_emulator.key_displacement(key_id=key_id,
                                                               displacement=actuation_point - cls.RESOLUTION_PER_STEP)
            sleep(_50_MS_DELAY)
            test_case.button_stimuli_emulator.key_release(key_id=key_id)
            ChannelUtils.check_queue_empty(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)

            # Perform a key press with displacement: AP
            test_case.button_stimuli_emulator.key_displacement(key_id=key_id,
                                                               displacement=actuation_point)
            sleep(_50_MS_DELAY)
            test_case.button_stimuli_emulator.key_release(key_id=key_id)
        # end def analog_keystroke

        @classmethod
        def analog_key_rapid_trigger(cls, test_case, key_id, actuation_point, sensitivity, duration=0.02):
            """
            Perform rapid triggers on input analog key.

            NB: These method will generate 3 HID MAKE and BREAK reports.

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param key_id: Analog Key ID
            :type key_id: ``KEY_ID``
            :param actuation_point: Actuation Point
            :type actuation_point: ``int``
            :param sensitivity: Rapid trigger sensitivity
            :type sensitivity: ``int``
            :param duration: Wait time in second between each MAKE and BREAK - OPTIONAL
            :type duration: ``float``
            """
            _actuation_point = min(cls.MAX_ACTUATION_POINT, actuation_point + sensitivity)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, f"Perform rapid triggers on input analog key: {key_id!r} "
                           f"with AP: {_actuation_point}, sensitivity: {sensitivity}")
            # ----------------------------------------------------------------------------------------------------------
            test_case.button_stimuli_emulator.key_displacement(key_id=key_id, displacement=_actuation_point)
            sleep(duration)
            test_case.button_stimuli_emulator.key_displacement(key_id=key_id,
                                                               displacement=max(_actuation_point - sensitivity, 0))
            sleep(duration)
            test_case.button_stimuli_emulator.key_displacement(key_id=key_id,
                                                               displacement=_actuation_point)
            sleep(duration)
            test_case.button_stimuli_emulator.key_displacement(key_id=key_id,
                                                               displacement=cls.MIN_ACTUATION_POINT)
            sleep(duration)
            test_case.button_stimuli_emulator.key_displacement(key_id=key_id,
                                                               displacement=cls.MIN_ACTUATION_POINT + sensitivity)
            sleep(duration)
            test_case.button_stimuli_emulator.key_release(key_id=key_id)
        # end def analog_key_rapid_trigger

        @classmethod
        def select_standard_keys_randomly(cls, test_case, num_of_keys, excluded_keys=None):
            """
            Select standard keys randomly

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param num_of_keys: Number of keys to be picked
            :type num_of_keys: ``int``
            :param excluded_keys: Keys don't want to be picked into the returning list - OPTIONAL
            :type excluded_keys: ``list[KEY_ID] | None``

            :return: Random selected keys
            :rtype: ``list[KEY_ID]``
            """
            random_selected_keys = []
            while len(random_selected_keys) < num_of_keys:
                random_selected_key = choice(list(
                    test_case.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID.keys()))
                if random_selected_key in random_selected_keys:
                    continue
                elif excluded_keys is not None and random_selected_key in excluded_keys:
                    continue
                else:
                    random_selected_keys.append(random_selected_key)
                # end if
            # end while

            return random_selected_keys
        # end def select_standard_keys_randomly
    # end class AnalogKeysHelper

    class MultiActionChecker:
        """
        Class for checking methods of multi-action
        """

        @classmethod
        def check_event(cls, test_case, action_key, event):
            """
            Check HID reports of an assignment event

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param action_key: Action standard key
            :type action_key: ``KEY_ID``
            :param event: Assignment event
            :type event: ``MultiActionConfigurationTable.Event``
            """
            action_map = {
                'MAKE': MAKE,
                'BREAK': BREAK
            }
            actions = [action_map[action] for action in repr(event).split('.')[1].split(':')[0].split('_')]
            for action in actions:
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                              key=KeyMatrixTestUtils.Key(action_key, action))
            # end for
        # end def check_event

        @classmethod
        def check_assignment(cls, test_case, group, check_event_0=False, check_event_1=False,
                             check_event_2=False, check_event_3=False):
            """
            Check actions of assignment in a group

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param group: A group of multi-action
            :type group: ``ActionGroup``
            :param check_event_0: Flag indicating the event 0 shall be checked - OPTIONAL
            :type check_event_0: ``bool``
            :param check_event_1: Flag indicating the event 1 shall be checked - OPTIONAL
            :type check_event_1: ``bool``
            :param check_event_2: Flag indicating the event 2 shall be checked - OPTIONAL
            :type check_event_2: ``bool``
            :param check_event_3: Flag indicating the event 3 shall be checked - OPTIONAL
            :type check_event_3: ``bool``
            """
            events_to_be_checked = [check_event_0, check_event_1, check_event_2, check_event_3]
            for index, assignment in enumerate(group.rows):
                action_key_previous_assignment = None
                if to_int(assignment.opcode) == ActionAssignment.Opcode.NO_ACTION:
                    continue
                # end if

                action_key = KEYBOARD_HID_USAGE_TO_KEY_ID_MAP[assignment.params[1]]
                if action_key in group.action_keys[:index]:
                    sub_group_rows = group.rows[:index]
                    sub_group_rows.reverse()
                    action_key_previous_assignment = sub_group_rows[
                        group.action_keys[:index][::-1].index(action_key)]
                # end if
                for inner_index, event in enumerate(
                        [assignment.event_0, assignment.event_1, assignment.event_2, assignment.event_3]):
                    if events_to_be_checked[inner_index] and \
                            event not in [MultiActionConfigurationTable.Event.PRESSED,
                                          MultiActionConfigurationTable.Event.RELEASED]:
                        if (action_key_previous_assignment is None or
                                to_int(action_key_previous_assignment.opcode) == ActionAssignment.Opcode.NO_ACTION):
                            cls.check_event(test_case=test_case, action_key=action_key, event=event)
                        else:
                            action_key_previous_assignment_events = [
                                getattr(action_key_previous_assignment, f'event_{index}')
                                for index in range(ActionAssignment.NUM_OF_EVENTS)]
                            action_key_previous_state = None
                            for action_key_previous_assignment_event in \
                                    action_key_previous_assignment_events[:inner_index]:
                                # Ignore the first bit (RELEASED, PRESSED)
                                if action_key_previous_assignment_event >> 1:
                                    action_key_previous_state = MultiActionConfigurationTable.Event.MAKE if \
                                        action_key_previous_assignment_event in \
                                        [MultiActionConfigurationTable.Event.MAKE] \
                                        else MultiActionConfigurationTable.Event.BREAK
                                # end if
                            # end for
                            if event == action_key_previous_state:
                                pass
                            elif event == MultiActionConfigurationTable.Event.BREAK and \
                                    action_key_previous_state == MultiActionConfigurationTable.Event.MAKE:
                                pass
                            else:
                                cls.check_event(test_case=test_case, action_key=action_key, event=event)
                            # end if
                        # end if
                    # end if
                # end for
            # end for
        # end def check_assignment

        _key_id_1st_ap_mapping_table = {}     # {KEY_ID: bool}
        _key_id_2nd_ap_mapping_table = {}     # {KEY_ID: bool}

        @classmethod
        def clean_key_id_and_ap_mapping_table(cls):
            """
            Clean mapping tables
            """
            cls._key_id_1st_ap_mapping_table = {}
            cls._key_id_2nd_ap_mapping_table = {}
        # end def clean_key_id_and_ap_mapping_table

        @classmethod
        def check_multi_actions(cls, test_case, trigger_key, multi_action_table,
                                last_actuation_point=None, current_actuation_point=None,
                                global_actuation_point=None):
            """
            Check events of multi-action

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param trigger_key: Trigger key
            :type trigger_key: ``KEY_ID``
            :param multi_action_table: Multi-Action configuration table
            :type multi_action_table: ``MultiActionConfigurationTable``
            :param last_actuation_point:
                The actuation point before the current action (PRESS/RELEASE). Unit: 0.1mm - OPTIONAL
            :type last_actuation_point: ``int``
            :param current_actuation_point:
                The actuation point after the current action (PRESS/RELEASE). Unit: 0.1mm - OPTIONAL
            :type current_actuation_point: ``int``
            :param global_actuation_point: Global actuation point. Unit: 0.1mm - OPTIONAL
            :type global_actuation_point: ``int``
            """
            if trigger_key in multi_action_table.get_trigger_keys():
                # Get the group of the trigger key
                group_index = multi_action_table.get_trigger_keys().index(trigger_key)
                group = multi_action_table.groups[group_index]
                if last_actuation_point < current_actuation_point:  # Check the Press action
                    if last_actuation_point < global_actuation_point:
                        if current_actuation_point < global_actuation_point:
                            ChannelUtils.check_queue_empty(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)
                        elif current_actuation_point >= global_actuation_point:
                            if group.second_actuation_point not in [0, None] and \
                                    current_actuation_point >= group.second_actuation_point:
                                # Cross the 2nd actuation point when pressing
                                cls.check_assignment(test_case=test_case, group=group,
                                                     check_event_0=True, check_event_1=True)
                                cls._key_id_1st_ap_mapping_table[trigger_key] = True
                                cls._key_id_2nd_ap_mapping_table[trigger_key] = True
                            else:
                                # Cross the 1st actuation point when pressing (no 2nd actuation point or not reached)
                                cls.check_assignment(test_case=test_case, group=group, check_event_0=True)
                                cls._key_id_1st_ap_mapping_table[trigger_key] = True
                            # end if
                        # end if
                    elif last_actuation_point < group.second_actuation_point:
                        if group.second_actuation_point not in [0, None] and \
                                current_actuation_point >= group.second_actuation_point:
                            # Cross 2nd actuation point
                            cls.check_assignment(test_case=test_case, group=group, check_event_1=True)
                            cls._key_id_1st_ap_mapping_table[trigger_key] = True
                            cls._key_id_2nd_ap_mapping_table[trigger_key] = True
                        # end if
                    else:
                        ChannelUtils.check_queue_empty(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)
                    # end if
                elif last_actuation_point > current_actuation_point:  # Check the Release action
                    if group.second_actuation_point not in [0, None] and \
                            last_actuation_point >= group.second_actuation_point:
                        if current_actuation_point <= \
                                max(global_actuation_point -
                                    AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0):
                            cls.check_assignment(test_case=test_case, group=group,
                                                 check_event_2=True, check_event_3=True)
                            cls._key_id_1st_ap_mapping_table[trigger_key] = False
                            cls._key_id_2nd_ap_mapping_table[trigger_key] = False
                        elif current_actuation_point <= max(
                                group.second_actuation_point -
                                AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0):
                            cls.check_assignment(test_case=test_case, group=group, check_event_2=True)
                            cls._key_id_2nd_ap_mapping_table[trigger_key] = False
                        else:
                            # Check there is no report since the travel of key release didn't across 2nd and 1st AP
                            ChannelUtils.check_queue_empty(test_case=test_case,
                                                           queue_name=HIDDispatcher.QueueName.HID)
                        # end if
                    elif group.second_actuation_point not in [0, None] and \
                            last_actuation_point > (group.second_actuation_point -
                                                    AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA):
                        if current_actuation_point <= \
                                (max(global_actuation_point -
                                     AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0)):
                            cls.check_assignment(test_case=test_case, group=group,
                                                 check_event_2=True, check_event_3=True)
                            cls._key_id_1st_ap_mapping_table[trigger_key] = False
                            cls._key_id_2nd_ap_mapping_table[trigger_key] = False
                        elif cls._key_id_2nd_ap_mapping_table[trigger_key] and current_actuation_point <= \
                                (max(group.second_actuation_point -
                                     AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0)):
                            cls.check_assignment(test_case=test_case, group=group, check_event_2=True)
                            cls._key_id_2nd_ap_mapping_table[trigger_key] = False
                        else:
                            # Check there is no report since the travel of key release didn't across either 1st, 2nd AP
                            ChannelUtils.check_queue_empty(test_case=test_case,
                                                           queue_name=HIDDispatcher.QueueName.HID)
                        # end if
                    elif last_actuation_point >= global_actuation_point:
                        if current_actuation_point <= \
                                (max(global_actuation_point -
                                     AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0)):
                            cls.check_assignment(test_case=test_case, group=group, check_event_3=True)
                            cls._key_id_1st_ap_mapping_table[trigger_key] = False
                        else:
                            # Check there is no report since the travel of key release didn't across the 1st AP
                            ChannelUtils.check_queue_empty(test_case=test_case,
                                                           queue_name=HIDDispatcher.QueueName.HID)
                        # end if
                    elif last_actuation_point > max(global_actuation_point -
                                                    AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0):
                        if cls._key_id_1st_ap_mapping_table[trigger_key] and current_actuation_point <= \
                                (max(global_actuation_point -
                                     AnalogKeysTestUtils.AnalogKeysHelper.MA_RELEASE_POINT_DELTA, 0)):
                            cls.check_assignment(test_case=test_case, group=group, check_event_3=True)
                            cls._key_id_1st_ap_mapping_table[trigger_key] = False
                        else:
                            # Check there is no report since the travel of key release didn't across 1st AP
                            ChannelUtils.check_queue_empty(test_case=test_case,
                                                           queue_name=HIDDispatcher.QueueName.HID)
                        # end if
                    else:
                        # Check there is no report since the last actuation point already across the 1st AP
                        ChannelUtils.check_queue_empty(test_case=test_case,
                                                       queue_name=HIDDispatcher.QueueName.HID)
                    # end if
                else:   # Check there is no report since the current action is hold
                    ChannelUtils.check_queue_empty(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)
                # end if
            else:
                # There is no remapping in the multi-action table for the trigger key
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                              key=KeyMatrixTestUtils.Key(trigger_key, MAKE))
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                              key=KeyMatrixTestUtils.Key(trigger_key, BREAK))
            # end if
        # end def check_multi_actions
    # end class MultiActionChecker

    @classmethod
    def check_all_key_release_reports(cls, test_case):
        """
        Check all key release reports after configuring a profile, enabling FKC, etc.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :raise ``AssertionError``: Assert all key release reports that raise an exception
        """
        messages = ChannelUtils.clean_messages(test_case=test_case,
                                               queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=(HidMouse, HidConsumer, HidKeyboardBitmap))
        for message in messages:
            assert to_int(HexList(message)) == 0, \
                f"This all key release HID report: {message} is incorrect, receiving unexpected key MAKE!"
        # end for
    # end def check_all_key_release_reports

    @classmethod
    def enable_disable_multi_action_fkc(cls, test_case):
        """
        Enable or Disable Multi-Action and FKC via hotkey

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :raise ``ValueError``: If the key to switch to Base Profile is not found in the keyboard layout
        """
        if KEY_ID.FKC_TOGGLE in test_case.button_stimuli_emulator.keyboard_layout.KEYS.keys():
            key_to_enable_fkc = KEY_ID.FKC_TOGGLE
        elif KEY_ID.FKC_TOGGLE in test_case.button_stimuli_emulator.keyboard_layout.FN_KEYS.keys():
            key_to_enable_fkc = \
                test_case.button_stimuli_emulator.keyboard_layout.FN_KEYS[KEY_ID.FKC_TOGGLE]
        else:
            raise ValueError("The key to switch to Base Profile is not found in the keyboard layout")
        # end if

        ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)
        test_case.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
        sleep(_50_MS_DELAY)
        test_case.button_stimuli_emulator.keystroke(key_id=key_to_enable_fkc)
        test_case.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
        sleep(_50_MS_DELAY)
        cls.check_all_key_release_reports(test_case=test_case)
    # end def enable_disable_multi_action_fkc

    @classmethod
    def switch_to_base_profile(cls, test_case):
        """
        Switch to Base Profile via hotkey

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :raise ``ValueError``: If the key to switch to Base Profile is not found in the keyboard layout
        """
        if KEY_ID.ONBOARD_BASE_PROFILE in test_case.button_stimuli_emulator.keyboard_layout.KEYS.keys():
            key_to_switch_to_base_profile = KEY_ID.ONBOARD_BASE_PROFILE
        elif KEY_ID.ONBOARD_BASE_PROFILE in test_case.button_stimuli_emulator.keyboard_layout.FN_KEYS.keys():
            key_to_switch_to_base_profile = \
                test_case.button_stimuli_emulator.keyboard_layout.FN_KEYS[KEY_ID.ONBOARD_BASE_PROFILE]
        else:
            raise ValueError("The key to switch to Base Profile is not found in the keyboard layout")
        # end if

        ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)
        test_case.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
        sleep(_50_MS_DELAY)
        test_case.button_stimuli_emulator.keystroke(key_id=key_to_switch_to_base_profile)
        test_case.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
        sleep(_50_MS_DELAY)
        cls.check_all_key_release_reports(test_case=test_case)
    # end def switch_to_base_profile

    @classmethod
    def enter_exit_actuation_point_adjustment_mode(cls, test_case):
        """
        Make the device enter or exit actuation point adjustment mode via hotkey

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :raise ``ValueError``: If the key to enter Actuation Point Adjustment Mode is not found in the keyboard layout
        """
        if KEY_ID.ONBOARD_ACTUATION_MODE in test_case.button_stimuli_emulator.keyboard_layout.KEYS.keys():
            key_to_enter_onboard_actuation_mode = KEY_ID.ONBOARD_ACTUATION_MODE
        elif KEY_ID.ONBOARD_ACTUATION_MODE in test_case.button_stimuli_emulator.keyboard_layout.FN_KEYS.keys():
            key_to_enter_onboard_actuation_mode = \
                test_case.button_stimuli_emulator.keyboard_layout.FN_KEYS[KEY_ID.ONBOARD_ACTUATION_MODE]
        else:
            raise ValueError("The key to enter Actuation Point Adjustment Mode is not found in the keyboard layout")
        # end if

        ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)
        test_case.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
        sleep(_50_MS_DELAY)
        test_case.button_stimuli_emulator.keystroke(key_id=key_to_enter_onboard_actuation_mode)
        test_case.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
        sleep(_50_MS_DELAY)
        cls.check_all_key_release_reports(test_case=test_case)
    # end def enter_exit_actuation_point_adjustment_mode

    @classmethod
    def enter_exit_sensitivity_adjustment_mode(cls, test_case):
        """
        Make the device enter or exit sensitivity adjustment mode via hotkey

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :raise ``ValueError``: If the key to enter Sensitivity Adjustment Mode is not found in the keyboard layout
        """
        if KEY_ID.ONBOARD_RAPID_TRIGGER_MODE in test_case.button_stimuli_emulator.keyboard_layout.KEYS.keys():
            key_to_enter_onboard_rapid_trigger_mode = KEY_ID.ONBOARD_RAPID_TRIGGER_MODE
        elif KEY_ID.ONBOARD_RAPID_TRIGGER_MODE in test_case.button_stimuli_emulator.keyboard_layout.FN_KEYS.keys():
            key_to_enter_onboard_rapid_trigger_mode = \
                test_case.button_stimuli_emulator.keyboard_layout.FN_KEYS[KEY_ID.ONBOARD_RAPID_TRIGGER_MODE]
        else:
            raise ValueError("The key to enter Sensitivity Adjustment Mode is not found in the keyboard layout")
        # end if

        ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID)
        test_case.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
        sleep(_50_MS_DELAY)
        test_case.button_stimuli_emulator.keystroke(key_id=key_to_enter_onboard_rapid_trigger_mode)
        test_case.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
        sleep(_50_MS_DELAY)
        cls.check_all_key_release_reports(test_case=test_case)
    # end def enter_exit_sensitivity_adjustment_mode
# end class AnalogKeysTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
