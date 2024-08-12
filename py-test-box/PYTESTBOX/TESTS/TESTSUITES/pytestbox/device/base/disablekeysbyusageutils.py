#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.disablekeysbyusageutils
:brief:  Helpers for Disable Keys By Usage feature
:author: YY Liu <yliu5@logitech.com>
:date: 2021/09/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from math import ceil

from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsage
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsageFactory
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysByUsageTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers for common checks on smart shift tunable feature
    """
    _game_mode_status = DisableKeysByUsage.GameMode.DISABLE

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help class to check getCapabilities response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get map to check default parameters values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Mapping between fields and check method with expected value
            :rtype: ``dict``
            """
            feature_config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS_BY_USAGE
            return {
                "max_disabled_usages": (cls.check_usage_count, feature_config.F_MaxDisabledUsages),
            }
        # end def get_default_check_map

        @staticmethod
        def check_usage_count(test_case, get_capabilities_response, expected):
            """
            Check the capabilities field reserved bits

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_capabilities_response: Response object
            :type get_capabilities_response: ``GetCapabilitiesResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=get_capabilities_response.max_disabled_usages,
                                  expected=expected,
                                  msg='The maxDisabledUsages parameter differs from the one expected')
        # end def check_usage_count
    # end class GetCapabilitiesResponseChecker

    class DisableKeysResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help class to check disableKeys response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get map to check default parameters values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Mapping between fields and check method with expected value
            :rtype: ``dict``
            """
            return {}
        # end def get_default_check_map

        @classmethod
        def check_disable_keys_responses(cls, test_case, messages, expected_cls, check_map=None):
            """
            Check fields of messages.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param messages: Messages to check
            :type messages: ``list[HidppMessage]``
            :param expected_cls: Expected class of the message
            :type expected_cls: ``DisableKeysResponse`` or ``tuple(DisableKeysResponse)``
            :param check_map: Map of the fields to check - OPTIONAL
            :type check_map: ``dict``

            :raise: ``TestException``: If check fails
            """
            for msg in messages:
                cls.check_fields(test_case=test_case,
                                 message=msg,
                                 expected_cls=expected_cls,
                                 check_map=check_map)
            # end for
        # end def check_disable_keys_responses
    # end class DisableKeysResponseChecker

    class EnableKeysResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help class to check enableKeys response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get map to check default parameters values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Mapping between fields and check method with expected value
            :rtype: ``dict``
            """
            return {}
        # end def get_default_check_map

        @classmethod
        def check_enable_keys_responses(cls, test_case, messages, expected_cls, check_map=None):
            """
            Check fields of messages.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param messages: Messages to check
            :type messages: ``list[HidppMessage]``
            :param expected_cls: Expected class of the message
            :type expected_cls: ``EnableKeysResponse`` or ``tuple(EnableKeysResponse)
            :param check_map: Map of the fields to check - OPTIONAL
            :type check_map: ``dict``

            :raise: ``TestException``: If check fails
            """
            for msg in messages:
                cls.check_fields(test_case=test_case,
                                 message=msg,
                                 expected_cls=expected_cls,
                                 check_map=check_map)
            # end for
        # end def check_enable_keys_responses
    # end class EnableKeysResponseChecker

    class EnableAllKeysResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help class to check enableAllKeys response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get map to check default parameters values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Mapping between fields and check method with expected value
            :rtype: ``dict``
            """
            return {}
        # end def get_default_check_map
    # end class EnableAllKeysResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None):
            """
            Get the capabilities of this feature.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Get Capabilities response
            :rtype: ``GetCapabilitiesResponseV0``
            """
            feature_4522_index, feature_4522, device_index, _ = cls.get_parameters(
                test_case, DisableKeysByUsage.FEATURE_ID, DisableKeysByUsageFactory, device_index, port_index)

            get_capabilities = feature_4522.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_4522_index)
            get_capabilities_response = test_case.send_report_wait_response(
                report=get_capabilities,
                response_queue=test_case.hidDispatcher.keyboard_message_queue,
                response_class_type=feature_4522.get_capabilities_response_cls)

            return get_capabilities_response
        # end def get_capabilities

        @classmethod
        def disable_keys(cls, test_case, keys, device_index=None, port_index=None):
            """
            Disable a list of 8-bit keyboard key usages. Multiple calls to 'disableKeys' will add to the set of disabled
            keys, not replace them. It will not return an error when keys already disable or disabling a key that does
            not exist on the keyboard.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param keys: keys to disable
            :type keys: ``list[int]``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: List of response to DisableKeys requests
            :rtype: ``list[DisableKeysResponseV0]``
            """
            feature_4522_index, feature_4522, device_index, _ = cls.get_parameters(
                test_case, DisableKeysByUsage.FEATURE_ID, DisableKeysByUsageFactory, device_index, port_index)

            max_key_hid_usages_per_request = 16
            i = 0
            responses = []

            for _ in range(ceil(len(keys)/max_key_hid_usages_per_request)):
                disable_keys = feature_4522.disable_keys_cls(
                    device_index=device_index,
                    feature_index=feature_4522_index,
                    keys_to_disable=keys[i:i+max_key_hid_usages_per_request])
                responses.append(test_case.send_report_wait_response(
                    report=disable_keys,
                    response_queue=test_case.hidDispatcher.keyboard_message_queue,
                    response_class_type=feature_4522.disable_keys_response_cls))
                i = i + max_key_hid_usages_per_request
            # end while

            return responses
        # end def disable_keys

        @classmethod
        def enable_keys(cls, test_case, keys, device_index=None, port_index=None):
            """
            Enable a list of 8-bit keyboard key usages. It does nothing and returns success when enabling a key that
            does not exist on the disable key list.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param keys: keys to enable
            :type keys: ``list[int]``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: List of response to EnableKeys requests
            :rtype: ``list[EnableKeysResponseV0]``
            """
            feature_4522_index, feature_4522, device_index, _ = cls.get_parameters(
                test_case, DisableKeysByUsage.FEATURE_ID, DisableKeysByUsageFactory, device_index, port_index)

            max_key_hid_usages_per_request = 16
            i = 0
            responses = []

            for _ in range(ceil(len(keys)/max_key_hid_usages_per_request)):
                enable_keys = feature_4522.enable_keys_cls(
                    device_index=device_index,
                    feature_index=feature_4522_index,
                    keys_to_enable=keys[i:i+max_key_hid_usages_per_request])
                responses.append(test_case.send_report_wait_response(
                    report=enable_keys,
                    response_queue=test_case.hidDispatcher.keyboard_message_queue,
                    response_class_type=feature_4522.enable_keys_response_cls))
                i = i + max_key_hid_usages_per_request
            # end while

            return responses
        # end def enable_keys

        @classmethod
        def enable_all_keys(cls, test_case, device_index=None, port_index=None):
            """
            Enable all keyboard key HID usages.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Response to EnableAllKeys requests
            :rtype: ``EnableAllKeysResponseV0``
            """
            feature_4522_index, feature_4522, device_index, port_index = cls.get_parameters(
                test_case, DisableKeysByUsage.FEATURE_ID, DisableKeysByUsageFactory, device_index, port_index)

            enable_all_keys = feature_4522.enable_all_keys_cls(
                device_index=device_index,
                feature_index=feature_4522_index)

            return test_case.send_report_wait_response(
                        report=enable_all_keys,
                        response_queue=test_case.hidDispatcher.keyboard_message_queue,
                        response_class_type=feature_4522.enable_all_keys_response_cls)
        # end def enable_all_keys
    # end class HIDppHelper

    @classmethod
    def enable_game_mode(cls, test_case):
        """
        Enable game mode HID usages.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        """
        if cls.game_mode_status != DisableKeysByUsage.GameMode.ENABLE:
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.GAME_MODE_KEY)
            cls.game_mode_status = DisableKeysByUsage.GameMode.ENABLE
        # end if

        test_case.clean_message_type_in_queue(queue=test_case.hidDispatcher.hid_message_queue,
                                              class_type=HidKeyboard)
    # end def enable_game_mode

    @classmethod
    def disable_game_mode(cls, test_case):
        """
        Disable game mode HID usages.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        """
        if cls.game_mode_status != DisableKeysByUsage.GameMode.DISABLE:
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.GAME_MODE_KEY)
            cls.game_mode_status = DisableKeysByUsage.GameMode.DISABLE
        # end if

        test_case.clean_message_type_in_queue(queue=test_case.hidDispatcher.hid_message_queue,
                                              class_type=HidKeyboard)
    # end def disable_game_mode

    @classmethod
    def get_keyboard_standard_key_id(cls, test_case, keyboard_layout):
        """
        Get keys from the intersection of standard keys and current keyboard layout.
        (The definition of standard keys could refer to the sheet which named Standard Keys in 0x4522 Disable Keys
        HID++ Feature Test Design Specification)

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param keyboard_layout: dict_keys of specific keyboard matrix layout
        :type keyboard_layout: ``dict_keys``

        :return: Identification of standard keys
        :rtype: ``list[KEY_ID]``
        """
        standard_keys_id = list(set(keyboard_layout).intersection(STANDARD_KEYS))

        for key in standard_keys_id:
            if str(key).split('.')[1] in \
                    test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS_BY_USAGE.F_DefaultDisableKeys:
                standard_keys_id.remove(key)
            # end if
        # end for

        return standard_keys_id
    # end def get_keyboard_standard_key_id

    @classmethod
    def disable_keys_by_key_id(cls, test_case, keys):
        """
        Disable a list of 8-bit keyboard key usages.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param keys: ID of keys to disable
        :type keys: ``list``

        :return: List of response to DisableKeys requests
        :rtype: ``list[DisableKeysResponseV0]``
        """
        return cls.HIDppHelper.disable_keys(
                        test_case=test_case,
                        keys=KeyMatrixTestUtils.get_keyboard_usage_index(keys=keys))
    # end def disable_keys_by_key_id

    @classmethod
    def enable_keys_by_key_id(cls, test_case, keys):
        """
        Enable a list of 8-bit keyboard key usages. It does nothing and returns success when enabling a key that
        does not exist on the disable key list.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param keys: ID of keys to enable
        :type keys: ``list``

        :return: List of response to EnableKeys requests
        :rtype: ``list[EnableKeysResponseV0]``
        """
        return cls.HIDppHelper.enable_keys(
                        test_case=test_case,
                        keys=KeyMatrixTestUtils.get_keyboard_usage_index(keys=keys))
    # end def enable_keys_by_key_id

    @classmethod
    def get_capabilities_with_specific_padding(cls, test_case, padding_byte):
        """
        Get capabilities with several value for padding. This could be used for ignoring padding byte test.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param padding_byte: specific value for padding
        :type padding_byte: ``HexList``

        :return: The message retrieved from the queue
        :rtype: ``GetCapabilitiesResponseV0``
        """
        get_capabilities = test_case.feature_4522.get_capabilities_cls(device_index=test_case.deviceIndex,
                                                                       feature_index=test_case.feature_4522_index)
        get_capabilities.padding = padding_byte

        return test_case.send_report_wait_response(
            report=get_capabilities,
            response_queue=test_case.hidDispatcher.keyboard_message_queue,
            response_class_type=test_case.feature_4522.get_capabilities_response_cls)
    # end def get_capabilities_with_specific_padding

    @classmethod
    def disable_key_with_function_id(cls, test_case, function_id, key_id, device_index=None, port_index=None):
        """
        Disable keys with specific function index. This could be used for disabling wrong function index test.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param function_id: ID of function
        :type function_id: ``int``
        :param key_id: ID of key to disable
        :type key_id: ``KEY_ID``
        :param device_index: Device index - OPTIONAL
        :type device_index: ``int``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: The error message retrieved from the queue
        :rtype: ``ErrorCodes``
        """
        feature_4522_index, feature_4522, device_index, port_index = cls.HIDppHelper.get_parameters(
            test_case, DisableKeysByUsage.FEATURE_ID, DisableKeysByUsageFactory, device_index, port_index)

        key_to_disable = KeyMatrixTestUtils.get_keyboard_usage_index(keys=[key_id])

        disable_keys = feature_4522.disable_keys_cls(
            device_index=device_index,
            feature_index=feature_4522_index,
            keys_to_disable=key_to_disable)

        disable_keys.functionIndex = function_id

        return test_case.send_report_wait_response(
            report=disable_keys,
            response_queue=test_case.hidDispatcher.error_message_queue,
            response_class_type=ErrorCodes)
    # end def disable_keys_with_function_id

    @classmethod
    def check_error_invalid_function_id(cls, test_case, response):
        """
        Check the error code of response message is INVALID_FUNCTION_ID

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param response: The error message retrieved from the queue
        :type response: ``ErrorCodes``

        :raise: ``TestException``: If check fails
        """
        if not isinstance(response, ErrorCodes):
            raise TypeError('Wrong response type: %s. Should be ErrorCodes' % (type(response).__name__,))
        # end if

        test_case.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                              obtained=response.errorCode,
                              msg='The errorCode parameter differs from the one expected')
    # end def check_error_invalid_function_id

    @classmethod
    def check_keys_disabled(cls, test_case, keys_reports):
        """
        Check host does not receive any key stroke report from the device.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param: keys_reports: HID message reports for keys
        :type keys_reports: ``list[tuple(KEY_ID, HexList(HIDMessage))]``

        :raise: ``TestException``: If the HID message queue is not empty
        """
        test_case.assertEqual(expected=[],
                              obtained=keys_reports,
                              msg='The host should not received any keys report from device after disabled'
                                  ' specific keys')
    # end def check_keys_disabled

    @classmethod
    def check_keys_enabled(cls, test_case, keys):
        """
        Check host can receive key stroke report from the device.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param keys: Identification of enabled keys
        :type keys: ``list[KEY_ID]``

        :raise: ``TestException``: If check fails
        """
        for key in keys:
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                          key=KeyMatrixTestUtils.Key(key, MAKE),
                                                          raise_exception=True)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                          key=KeyMatrixTestUtils.Key(key, BREAK),
                                                          raise_exception=True)
        # end for
    # end def check_keys_enabled

    @classmethod
    def check_all_standard_keys_enabled(cls, test_case, keyboard_layout):
        """
        Check host can receive the all standard key stroke report from device.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param keyboard_layout: dict_keys of specific keyboard matrix layout
        :type keyboard_layout: ``dict_keys``

        :raise: ``TestException``: If check fails
        """
        enabled_keys_id = DisableKeysByUsageTestUtils.get_keyboard_standard_key_id(
            test_case=test_case,
            keyboard_layout=keyboard_layout)
        DisableKeysByUsageTestUtils.check_keys_enabled(test_case=test_case,
                                                       keys=enabled_keys_id)
    # end def check_all_standard_keys_enabled

    @property
    def game_mode_status(self):
        """
        Get game_mode_status

        :return: The status of game mode
        :rtype: ``GameMode``
        """
        return self._game_mode_status
    # end def game_mode_status

    @game_mode_status.setter
    def game_mode_status(self, status):
        """
        Set game_mode_status

        :param status: Status of game mode
        :type status: ``GameMode``
        """
        if status in DisableKeysByUsage.GameMode:
            self._game_mode_status = status
        else:
            raise ValueError("Unknown status")
        # end if
    # end def game_mode_status

    @classmethod
    def get_key_list_from_standard_keys(cls, test_case, group_count, group_size):
        """
        Randomly selected specific number of keys.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param group_count: number of groups to create or ``None`` to test all keys
        :type group_count: ``int`` or ``None``
        :param group_size: number of keys per group (singleton, pair, triplet, ...) - OPTIONAL
        :type group_size: ``int``

        :return: Selected keys
        :rtype: ``list``
        """
        exclude_keys = set(STANDARD_KEYS) ^ test_case.button_stimuli_emulator._keyboard_layout.KEYS.keys()

        return list(KeyMatrixTestUtils.get_key_list(test_case=test_case,
                                                    group_count=group_count,
                                                    group_size=group_size,
                                                    excluded_keys=exclude_keys)[0])
    # end def get_key_list_from_standard_keys
# end class DisableKeysByUsageTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
