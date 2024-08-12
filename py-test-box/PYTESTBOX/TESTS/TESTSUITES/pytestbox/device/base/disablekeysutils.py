#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------------
# Python Test Box
# -------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.disablekeysutils
:brief: Helpers for DisableKeys feature
:author: YY Liu <yliu5@logitech.com>
:date: 2021/12/02
"""
# -------------------------------------------------------------------------------------------------------
# imports
# -------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeys
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeysFactory
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# -------------------------------------------------------------------------------------------------------
# implementation
# -------------------------------------------------------------------------------------------------------
class DisableKeysUtils(DeviceBaseTestUtils):
    """
    This class provides helpers for common checks on DisableKeys feature
    """

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help class to check GetCapabilities response
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
            return {
                "disableable_keys": (cls.check_disableable_keys,
                                     DisableKeysUtils.convert_all_disableable_keys_to_int(test_case)),
            }
        # end def get_default_check_map

        @staticmethod
        def check_disableable_keys(test_case, response, expected):
            """
            Check the capabilities fields

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=int(Numeral(response.disableable_keys)),
                                  expected=expected,
                                  msg='The disableableKeys differs from the one expected')
        # end def check_disableable_keys
    # end class GetCapabilitiesResponseChecker

    class DisabledKeysResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help class to check Set/Get DisabledKeys response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get map to check default parameters value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Mapping between fields and check method with expected value
            :rtype: ``dict``
            """
            return {
                "disabled_keys": (cls.check_disabled_keys, test_case.default_disabled_keys),
            }
        # end def get_default_check_map

        @classmethod
        def check_disabled_keys(cls, test_case, response, expected):
            """
            Check disabledKeys field

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: Set/Get DisabledKeys response to check
            :type response: ``GetDisabledKeysResponse`` or ``SetDisabledKeysResponse``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=int(Numeral(response.disabled_keys)),
                                  expected=expected,
                                  msg='The disabledKeys differs from the one expected')
        # end def check_disabled_keys
    # end class DisabledKeysResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None):
            """
            Get the presence of the keys which the SW allows the user to disable.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Get capabilities response
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_4521_index, feature_4521, device_index, port_index = cls.get_parameters(
                test_case, DisableKeys.FEATURE_ID, DisableKeysFactory, device_index, port_index)

            get_capabilities_request = feature_4521.get_capabilities_cls(device_index, feature_4521_index)

            get_capabilities_response = test_case.send_report_wait_response(
                report=get_capabilities_request,
                response_queue=test_case.hidDispatcher.keyboard_message_queue,
                response_class_type=feature_4521.get_capabilities_response_cls)

            return get_capabilities_response
        # end def get_capabilities

        @classmethod
        def get_disabled_keys(cls, test_case, device_index=None, port_index=None):
            """
            Get disabled keys

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Get disabled keys response
            :rtype: ``GetDisabledKeysResponse``
            """
            feature_4521_index, feature_4521, device_index, port_index = cls.get_parameters(
                test_case, DisableKeys.FEATURE_ID, DisableKeysFactory, device_index, port_index)

            get_disabled_keys_request = feature_4521.get_disabled_keys_cls(device_index, feature_4521_index)

            get_disabled_keys_response = test_case.send_report_wait_response(
                report=get_disabled_keys_request,
                response_queue=test_case.hidDispatcher.keyboard_message_queue,
                response_class_type=feature_4521.get_disabled_keys_response_cls)

            return get_disabled_keys_response
        # end def get_disabled_keys

        @classmethod
        def set_disabled_keys(cls, test_case, keys_to_disable=None, device_index=None, port_index=None):
            """
            Set keys to disable

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param keys_to_disable: Selected keys to disable - OPTIONAL
            :type keys_to_disable: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Set disabled keys response
            :rtype: ``SetDisabledKeysResponse``
            """
            feature_4521_index, feature_4521, device_index, port_index = cls.get_parameters(
                test_case, DisableKeys.FEATURE_ID, DisableKeysFactory, device_index, port_index)

            set_disabled_keys_request = feature_4521.set_disabled_keys_cls(device_index,
                                                                           feature_4521_index,
                                                                           keys_to_disable)

            set_disabled_keys_response = test_case.send_report_wait_response(
                report=set_disabled_keys_request,
                response_queue=test_case.hidDispatcher.keyboard_message_queue,
                response_class_type=feature_4521.set_disabled_keys_response_cls)

            return set_disabled_keys_response
        # end def set_disabled_keys
    # end class HIDppHelper

    @classmethod
    def update_disabled_keys_for_check_map(cls, test_case, keys_to_disable=None):
        """
        Update the value of disabled_keys in the check map

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param keys_to_disable: Selected keys to disable - OPTIONAL
        :type keys_to_disable: ``int`` or ``list[KEY_ID]``

        :return: Map of the fields to check
        :rtype: ``dict``

        :raise ``TypeError``: If input value type is invalid
        """
        if type(keys_to_disable) not in [int, list]:
            raise TypeError(f"{type(keys_to_disable)} is not an int or list")
        # end if

        if type(keys_to_disable) is list:
            if type(keys_to_disable[0]) not in [int, KEY_ID]:
                raise TypeError(f"{type(keys_to_disable[0])} is not an int or KEY_ID")
            else:
                keys_to_disable = cls.convert_keys_ids_to_int(test_case=test_case, key_ids=keys_to_disable)
            # end if
        # end if

        check_map = cls.DisabledKeysResponseChecker.get_default_check_map(test_case)
        check_map['disabled_keys'] = (cls.DisabledKeysResponseChecker.check_disabled_keys,
                                      keys_to_disable)

        return check_map
    # end def update_disabled_keys_for_check_map

    @classmethod
    def set_disabled_keys_by_key_id(cls, test_case, key_ids=None, device_index=None, port_index=None):
        """
        Set keys to disable

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param key_ids: List of key ids to disable - OPTIONAL
        :type key_ids: ``list[KEY_ID]``
        :param device_index: Device index - OPTIONAL
        :type device_index: ``int``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: Set disabled keys response
        :rtype: ``SetDisabledKeysResponse``
        """
        keys_to_disable = [] if key_ids is None else key_ids
        keys_to_disable_int = DisableKeysUtils.convert_keys_ids_to_int(test_case, keys_to_disable)

        set_disabled_keys_response = DisableKeysUtils.HIDppHelper.set_disabled_keys(test_case=test_case,
                                                                                    keys_to_disable=keys_to_disable_int,
                                                                                    device_index=device_index,
                                                                                    port_index=port_index)

        return set_disabled_keys_response
    # end def set_disabled_keys_by_key_id

    @classmethod
    def convert_disableable_keys_to_key_id(cls, test_case):
        """
        Convert disableable keys setting to a KEY_ID list

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :return: The KEY_ID list of disableable keys
        :rtype: ``list[KEY_ID]``
        """
        feature_config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS

        all_disableable_keys = {KEY_ID.KEYBOARD_CAPS_LOCK: feature_config.F_CapsLock,
                                KEY_ID.KEYBOARD_LOCKING_NUM_LOCK: feature_config.F_NumLock,
                                KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: feature_config.F_NumLock,
                                KEY_ID.KEYBOARD_SCROLL_LOCK: feature_config.F_ScrollLock,
                                KEY_ID.KEYBOARD_INSERT: feature_config.F_Insert,
                                KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: feature_config.F_Windows}

        key_ids = []

        for key in all_disableable_keys:
            if key not in test_case.button_stimuli_emulator.get_key_id_list() and key not in \
                    test_case.button_stimuli_emulator.get_fn_keys():
                continue
            elif all_disableable_keys[key]:
                key_ids.append(key)
            # end if
        # end for

        return key_ids
    # end def convert_disableable_keys_to_key_id

    @classmethod
    def convert_all_disableable_keys_to_int(cls, test_case):
        """
        Get the integer value of disableableKeys from feature configurations

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :return: key bitmap which the SW allows users to disable
        :rtype: ``int``
        """
        feature_config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS

        return feature_config.F_CapsLock * (2 ** 0) \
            + feature_config.F_NumLock * (2 ** 1) \
            + feature_config.F_ScrollLock * (2 ** 2) \
            + feature_config.F_Insert * (2 ** 3) \
            + feature_config.F_Windows * (2 ** 4)
    # end def convert_all_disableable_keys_to_int

    @classmethod
    def convert_keys_ids_to_int(cls, test_case, key_ids):
        """
        Convert key id list to disableable keys settings.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param key_ids: Selected keys to disable
        :type key_ids: ``list[KEY_ID]``

        :return: Bitmap of keys to disable
        :rtype: ``int``
        """
        feature_config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS
        disableable_keys = {0x00: 0,
                            KEY_ID.KEYBOARD_CAPS_LOCK: feature_config.F_CapsLock * (2 ** 0),
                            KEY_ID.KEYBOARD_LOCKING_NUM_LOCK: feature_config.F_NumLock * (2 ** 1),
                            KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: feature_config.F_NumLock * (2 ** 1),
                            KEY_ID.KEYBOARD_SCROLL_LOCK: feature_config.F_ScrollLock * (2 ** 2),
                            KEY_ID.KEYBOARD_INSERT: feature_config.F_Insert * (2 ** 3),
                            KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: feature_config.F_Windows * (2 ** 4)}

        keys_to_disabled_int = 0

        for key in key_ids:
            if key not in disableable_keys.keys():
                raise ValueError(f'Unsupported key: {str(key)} is not a key which the SW allows the user to disable')
            # end if

            keys_to_disabled_int += disableable_keys[key]
        # end for

        return keys_to_disabled_int
    # end def convert_keys_ids_to_int

    @classmethod
    def get_disabled_key_ids(cls, test_case, value):
        """
        Get the list of KEY_ID from the bitmap value

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param value: Value of disabled keys
        :type value: ``int``

        :return: list of  unique identifier of the key
        :rtype: ``list[KEY_ID]``

        :raise ``ValueError``: If value is out of valid range
        """
        if value > 0x1F or value < 0:
            raise ValueError(f'Unsupported value = {value}')
        # end if

        key_ids = []

        feature_config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS
        disableable_keys = {KEY_ID.KEYBOARD_CAPS_LOCK: feature_config.F_CapsLock * (2 ** 0),
                            KEY_ID.KEYBOARD_LOCKING_NUM_LOCK: feature_config.F_NumLock * (2 ** 1),
                            KEY_ID.KEYPAD_NUM_LOCK_AND_CLEAR: feature_config.F_NumLock * (2 ** 1),
                            KEY_ID.KEYBOARD_SCROLL_LOCK: feature_config.F_ScrollLock * (2 ** 2),
                            KEY_ID.KEYBOARD_INSERT: feature_config.F_Insert * (2 ** 3),
                            KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION: feature_config.F_Windows * (2 ** 4)}

        for key in disableable_keys.keys():
            if key not in test_case.button_stimuli_emulator.get_key_id_list() and key not in \
                    test_case.button_stimuli_emulator.get_fn_keys():
                continue
            elif disableable_keys[key] & value != 0:
                key_ids.append(key)
            # end if
        # end for

        return key_ids
    # end def get_disabled_key_ids

    @classmethod
    def check_keys_disableable_capability(cls, test_case, keys_to_disable):
        """
        Check input disabled keys are supported

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param keys_to_disable: Value of disableable keys
        :type keys_to_disable: ``int``

        :return: Flag indicating that the 'keys_to_disable' value is supported by the DisableKeys request
        :rtype: ``boolean``
        """
        key_ids = cls.get_disabled_key_ids(test_case=test_case, value=keys_to_disable)

        # Check if all targeted keys are supported on the device via bitmap check
        if bin(keys_to_disable).count('1') != len(key_ids):
            return False
        # end if

        for key in key_ids:
            if key not in cls.convert_disableable_keys_to_key_id(test_case):
                return False
            # end if
        # end for

        return True
    # end def check_keys_disableable_capability

    @classmethod
    def compute_unsupported_range(cls, test_case):
        """
        Compute unsupported disableable key range

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :return: unsupported keys range
        :rtype: ``list[int]``
        """
        unsupported_keys = []

        for keys in range(1, 0x20):
            if not cls.check_keys_disableable_capability(test_case=test_case, keys_to_disable=keys):
                unsupported_keys.append(keys)
            # end if
        # end for

        return unsupported_keys
    # end def compute_unsupported_range
# end class DisabledKeysUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
