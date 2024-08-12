#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.keymatrixutils
:brief:  Helpers for keyboard key matrix features
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from copy import deepcopy
from random import choice
from sys import stdout
from time import sleep

from pyhid.hid.hidconsumer import HidConsumer
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.usbhidusagetable import ALL_KEYS
from pyhid.hiddata import FIELDS_NAME
from pyhid.hiddata import FIELDS_VALUE
from pyhid.hiddata import HidData
from pyhid.hiddata import OS
from pyhid.hiddata import RESP_CLASS
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import KEYSTROKE
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import RemappedKey
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COL_COUNT
from pyraspi.services.kosmos.protocol.generated.messages import KBD_ROW_COUNT
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils

# ----------------------------------------------------------------------------
# constant
# ----------------------------------------------------------------------------
DEFAULT_EXCLUDED_KEYS = [KEY_ID.FN_KEY, KEY_ID.HOST_1, KEY_ID.HOST_2, KEY_ID.HOST_3,
                         KEY_ID.KEYBOARD_POWER, KEY_ID.CONNECT_BUTTON,
                         KEY_ID.LS2_BLE_CONNECTION_TOGGLE, KEY_ID.LS2_CONNECTION, KEY_ID.BLE_CONNECTION,
                         KEY_ID.GAME_MODE_KEY, KEY_ID.ONBOARD_PROFILE_1, KEY_ID.ONBOARD_PROFILE_2,
                         KEY_ID.ONBOARD_PROFILE_3, KEY_ID.SELECT_NEXT_ONBOARD_PROFILE,
                         KEY_ID.SELECT_PREV_ONBOARD_PROFILE, KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE,
                         KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE, KEY_ID.FKC_TOGGLE]

# List of keys that can change their behavior in the case of a double press:
# cf https://docs.google.com/document/d/1Yebz9EikFP38I6lRIUav_JWwU4SgoWPzxfCzQGAj1SQ/edit#bookmark=id.c7ioidyhqlbh
DOUBLE_PRESS_KEYS = [KEY_ID.PLAY_PAUSE]


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class KeyMatrixTestUtils(HidReportTestUtils):
    """
    Test utils class for keyboard key matrix feature.
    """
    TEN_MS = .01

    class KEYSTATE:
        RELEASED = 0
        PRESSED = 1
        DIRECT_GHOST = 2
        INDIRECT_GHOST = 3
        DOUBLE_GHOST = 4
    # end class KEYSTATE

    class Key:
        """
        Key class implementation for multiple key press and hold tests
        """
        def __init__(self, key_id, state):
            """
            :param key_id: The key_id
            :type key_id: ``KEY_ID``
            :param state: MAKE or BREAK state
            :type state: ``str``
            """
            self.key_id = key_id
            self.state = state
        # end def __init__

        def __str__(self):
            return f'({str(self.key_id)}, state: {self.state})'
        # end def __str__

        def __repr__(self):
            return self.__str__()
        # end def __repr__
    # end class Key

    class KeyExpectedActions:
        """
        Merge expected actions for multiple key press and release
        """
        VERBOSE = False
        pressed_keys = []

        class SwitchKeys:
            """
            The function keys will be holding the modifiers for 1 sec after releasing it, it's to provide better UX.
            When modifiers is on hold, pressing any other key should trigger them being released first,
            otherwise an unexpected function could happen.

            cf Guidelines for Keyboards: implementation specification:
            https://docs.google.com/document/d/1L5hMnkgN0yU2sijrk0jW7mJ2iRFqbeNleYshjAd45C8/edit?usp=sharing

            Jira ticket: https://jira.logitech.io/browse/RBP-54
            """
            switch_keys = [
                KEY_ID.LANGUAGE_SWITCH, KEY_ID.APP_SWITCH_LAUNCHPAD
            ]

            pressed_switch_key = None

            @classmethod
            def check_and_insert_force_release_key(cls, key, expected_actions, variant):
                """
                Check whether the action key forces the release of a modifier key.
                If there is a modifier release key, it'll be inserted into the list of returned expected actions.

                :param key: The action key
                :type key: ``KeyMatrixTestUtils.Key``
                :param expected_actions: The expected actions for input keys
                :type expected_actions: ``list[list[], list[list[str]], list[list[int]]]``
                :param variant: OS detected by the firmware
                :type variant: ``str``
                """
                # Insert expected action for force release key
                if cls.pressed_switch_key:
                    if key.state == MAKE:
                        cls.debug(f'Force release switch key: {cls.pressed_switch_key}')
                        # Remove the SwitchKey from pressed_keys list
                        KeyMatrixTestUtils.KeyExpectedActions._remove_pressed_key(cls.pressed_switch_key)

                        temp_expected_actions = KeyMatrixTestUtils.KeyExpectedActions.get_unsealed_expected_actions(
                            cls.pressed_switch_key, variant)

                        # Insert expected actions of SwitchKey
                        if expected_actions[RESP_CLASS]:
                            for x in reversed(temp_expected_actions[RESP_CLASS]):
                                expected_actions[RESP_CLASS].insert(0, x)
                            # end for
                            for x in reversed(temp_expected_actions[FIELDS_NAME]):
                                expected_actions[FIELDS_NAME].insert(0, x)
                            # end for
                            for x in reversed(temp_expected_actions[FIELDS_VALUE]):
                                expected_actions[FIELDS_VALUE].insert(0, x)
                            # end for
                        else:
                            expected_actions[RESP_CLASS] = deepcopy(temp_expected_actions[RESP_CLASS])
                            expected_actions[FIELDS_NAME] = deepcopy(temp_expected_actions[FIELDS_NAME])
                            expected_actions[FIELDS_VALUE] = deepcopy(temp_expected_actions[FIELDS_VALUE])
                        # end if

                        cls.pressed_switch_key = None
                    else:
                        if key.key_id == cls.pressed_switch_key.key_id:
                            # Remove the SwitchKey if in BREAK state
                            cls.pressed_switch_key = None
                        # end if
                    # end if
                # end if

                # Check SwitchKey
                if key.key_id in cls.switch_keys:
                    if key.state == MAKE:
                        cls.pressed_switch_key = deepcopy(key)
                        cls.pressed_switch_key.state = BREAK
                    # end if
                # end if
            # end def check_and_insert_force_release_key

            @classmethod
            def reset(cls):
                """
                Reset ``SwitchKeys`` internal variables
                """
                cls.pressed_switch_key = None
            # end def reset

            @classmethod
            def debug(cls, message):
                """
                Print debug message

                :param message: The debug message
                :type message: ``str``
                """
                if KeyMatrixTestUtils.KeyExpectedActions.VERBOSE:
                    stdout.write(f"{message}\n")
                # end if
            # end def debug
        # end class SwitchKeys

        class ConsumerKeys:
            """
            Consumer key class to manage the available quota of consumer key
            """
            ignored_keys = []

            @classmethod
            def reset(cls):
                """
                Reset ``ConsumerKeys`` internal variables
                """
                cls.ignored_keys = []
            # end def reset

            @classmethod
            def is_key_ignored(cls, action_key, variant, pressed_keys):
                """
                To check if the given consumer key shall be ignored or not.

                Note:
                    If there are 2 consumer keys pressed and hold. The 3rd coming consumer key will be fully ignored.

                :param action_key: The action key
                :type action_key: ``KeyMatrixTestUtils.Key``
                :param variant: OS detected by the firmware
                :type variant: ``str``
                :param pressed_keys: The pressed key list
                :type pressed_keys: ``list[KeyMatrixTestUtils.Key]``

                return: Flag indicating if the consumer key shall be ignored or not
                rtype: ``bool``
                """
                ignore_the_key = False
                if action_key.state == MAKE:
                    if cls._is_consumer_report_overflowed(pressed_keys, hid_consumer_quota=2, variant=variant):
                        cls.ignored_keys.append(action_key.key_id)
                        ignore_the_key = True
                    # end if
                else:
                    for ignored_key in cls.ignored_keys:
                        if ignored_key == action_key.key_id:
                            cls.ignored_keys.remove(ignored_key)
                            ignore_the_key = True
                        # end if
                    # end for
                # end if
                return ignore_the_key
            # end def is_key_ignored

            @classmethod
            def _is_consumer_report_overflowed(cls, pressed_keys, hid_consumer_quota, variant):
                """
                Check whether the report capacity has been exceeded

                :param pressed_keys: The pressed key list
                :type pressed_keys: ``list[KeyMatrixTestUtils.Key]``
                :param hid_consumer_quota: The remaining quota of consumer key
                :type hid_consumer_quota: ``int``
                :param variant: OS detected by the firmware
                :type variant: ``str``

                return: To specify consumed quota or not
                rtype: ``bool``
                """
                run_out_of_quota = False
                for key in pressed_keys:
                    temp_responses_class, temp_fields_name, temp_fields_value = \
                        KeyMatrixTestUtils.get_expected_actions(key.key_id, key.state, variant)
                    if temp_responses_class and temp_responses_class[0] == HidConsumer:
                        hid_consumer_quota -= 1
                        if hid_consumer_quota == 0:
                            run_out_of_quota = True
                            break
                        # end if
                    # end if
                # end for
                return run_out_of_quota
            # end def _is_consumer_report_overflowed

            @classmethod
            def debug(cls, message):
                """
                Print debug message

                :param message: The debug message
                :type message: ``str``
                """
                if KeyMatrixTestUtils.KeyExpectedActions.VERBOSE:
                    stdout.write(f"{message}\n")
                # end if
            # end def debug
        # end class ConsumerKeys

        @classmethod
        def reset(cls):
            """
            Reset ``KeyExpectedActions``
            """
            cls.SwitchKeys.reset()
            cls.ConsumerKeys.reset()
            cls.pressed_keys = []
        # end def reset

        @classmethod
        def get_unsealed_expected_actions(cls, key, variant):
            """
            Get the unsealed expected actions for the key

            :param key: The key with its make or break state and key_id
            :type key: ``KeyMatrixTestUtils.Key``
            :param variant: OS detected by the firmware - OPTIONAL
            :type variant: ``str``

            :return: Expected actions
            :rtype: ``list[HIDReport]``, ``list[list[str]]``, ``list[list[int]]``
            """
            responses_class, fields_name, fields_value = KeyMatrixTestUtils.get_expected_actions(
                key.key_id, key.state, variant)
            return {RESP_CLASS: list(responses_class),
                    FIELDS_NAME: [list(a) for a in list(fields_name)],
                    FIELDS_VALUE: [list(a) for a in list(fields_value)]}
        # end def get_unsealed_expected_actions

        @classmethod
        def get(cls, key, variant):
            """
            Get the expected actions for input keys

            :param key: The action key with its make or break state
            :type key: ``KeyMatrixTestUtils.Key``
            :param variant: OS detected by the firmware - OPTIONAL
            :type variant: ``str``

            :return: Expected actions
            :rtype: ``list[HIDReport]``, ``list[list[str]]``, ``list[list[int]]``
            """
            cls.debug(f'action_key: {key}')
            expected_actions = cls.get_unsealed_expected_actions(key, variant)

            if expected_actions[RESP_CLASS] and expected_actions[RESP_CLASS][0] == HidConsumer:
                if cls.ConsumerKeys.is_key_ignored(key, variant, cls.pressed_keys):
                    cls.debug(f'---Ignore the consumer key: {key}---')
                    return [], [[], ], [[], ]
                else:
                    cls._update_pressed_keys(key)
                    return expected_actions[RESP_CLASS], expected_actions[FIELDS_NAME], expected_actions[FIELDS_VALUE]
                # end if
            else:
                # Check SwitchKey and insert force release key if needed
                cls.SwitchKeys.check_and_insert_force_release_key(key, expected_actions, variant)

                if not expected_actions[RESP_CLASS]:
                    cls.debug('---Skip the merging due to responses_class is empty---')
                    cls._update_pressed_keys(key)
                    return expected_actions[RESP_CLASS], expected_actions[FIELDS_NAME], expected_actions[FIELDS_VALUE]
                # end if

                if not cls.pressed_keys:
                    cls.debug('---Skip the merging due to no pressed key---')
                    cls._update_pressed_keys(key)
                    return expected_actions[RESP_CLASS], expected_actions[FIELDS_NAME], expected_actions[FIELDS_VALUE]
                # end if

                # Do nothing for the BREAK of SwitchKey
                pressed_keyid_list = [x.key_id for x in cls.pressed_keys]
                if key.state == BREAK and key.key_id not in pressed_keyid_list:
                    cls.debug('---Do nothing for the BREAK of SwitchKey---')
                    return [], [[], ], [[], ]
                # end if

                # Adjust fields name and value
                cls._adjust_name_value_fields(expected_actions)
                cls._update_pressed_keys(key)

                cls.debug(f'responses_class: {expected_actions[RESP_CLASS]}')
                cls.debug(f'fields_name: {expected_actions[FIELDS_NAME]}')
                cls.debug(f'fields_value: {expected_actions[FIELDS_VALUE]}')

                return expected_actions[RESP_CLASS], expected_actions[FIELDS_NAME], expected_actions[FIELDS_VALUE]
            # end if
        # end def get

        @classmethod
        def _adjust_name_value_fields(cls, expected_actions):
            """
            Adjust the item in the fields_name and fields_value

            :param expected_actions: The expected actions for input keys
            :type expected_actions: ``list[list[], list[list[str]], list[list[int]]]``
            """

            def get_value(item):
                """
                Get the value from the item

                :param item: The name_value item
                :type item: ``list[str, int]``

                :return: The value of the item
                :rtype: ``int``
                """
                return item[1]
            # end def get_value

            adjusted_name_list = []
            adjusted_value_list = []

            for index in range(len(expected_actions[FIELDS_NAME])):
                # Combine the name_list and value_list
                name_value_list = [list(a) for a in zip(expected_actions[FIELDS_NAME][index],
                                                        expected_actions[FIELDS_VALUE][index])]

                # Remove redundant fields which has the same key code for HID keyboard key_code and HID consumer key
                cls._remove_redundant_fields(name_value_list)

                # Sort list: increasing order
                name_value_list.sort(key=get_value)

                # Put the item to the end of list which has minus value
                cls._move_break_keys_to_the_list_end(name_value_list)

                # Correct name index of HID keyboard key_code and HID consumer key
                cls._adjust_order_for_name_fields(name_value_list)

                # Collect results
                unzip_name_value_list = list(zip(*name_value_list))
                adjusted_name_list.append(unzip_name_value_list[0])
                adjusted_value_list.append(unzip_name_value_list[1])
            # end for

            expected_actions[FIELDS_NAME] = adjusted_name_list
            expected_actions[FIELDS_VALUE] = adjusted_value_list
        # end def _adjust_name_value_fields

        @classmethod
        def _remove_redundant_fields(cls, name_value_list):
            """
            Remove redundant fields for name_value_list

            :param name_value_list: The fields_name list
            :type name_value_list: ``list[list[str, int]]``
            """
            offset = 0
            for idx in range(len(name_value_list)):
                # Remove redundant name_value item for MAKE key state
                if int(name_value_list[idx - offset][1]) >= 1:
                    matched_indices = [matched_index for (matched_index, name_value) in enumerate(name_value_list)
                                       if name_value[0] == name_value_list[idx - offset][0] and
                                       name_value[1] == name_value_list[idx - offset][1]]
                    # Remove redundant name_value item if found 2 more matched indices
                    if len(matched_indices) > 1:
                        for remove_index in range(1, len(matched_indices)):
                            name_value_list.pop(matched_indices[remove_index] - offset)
                            offset += 1
                        # end for
                    # end if
                # end if
            # end for
        # end def _remove_redundant_fields

        @classmethod
        def _move_break_keys_to_the_list_end(cls, name_value_list):
            """
            Move the items of break keys to the list end

            :param name_value_list: The fields_name list
            :type name_value_list: ``list[list[str, int]]``
            """
            # The name_value_list is increasing order
            # If the value of last item < 0, means the whole list is for key BREAK. Shall skip the operation
            if int(name_value_list[-1][1]) > 0:
                for _ in range(len(name_value_list)):
                    if int(name_value_list[0][1]) < 0:
                        # Move the item of break key to the list end
                        name_value_list.insert(len(name_value_list), name_value_list.pop(0))
                    else:
                        break
                    # end if
                # end for
            # end if
        # end def _move_break_keys_to_the_list_end

        @classmethod
        def _adjust_order_for_name_fields(cls, name_value_list):
            """
            Adjust order of fields_name for key_codeX and key_X

            :param name_value_list: The fields_name list
            :type name_value_list: ``list[list[str, int]]``
            """
            key_code_count = 1
            key_count = 1
            for idx in range(len(name_value_list)):
                if name_value_list[idx][0].find('key_code') != -1:
                    name_value_list[idx][0] = f'key_code{key_code_count}'
                    key_code_count += 1
                elif name_value_list[idx][0].find('key_') != -1:
                    name_value_list[idx][0] = f'key_{key_count}'
                    key_count += 1
                # end if
            # end for
        # end def _adjust_order_for_name_fields

        @classmethod
        def _update_pressed_keys(cls, key):
            """
            Insert or remove key from cls.pressed_keys by the key input state

            :param key: The key with its make or break state and key_id
            :type key: ``KeyMatrixTestUtils.Key``

            :raise ``ValueError``: if input key state is inconsistent with the pressed_keys list.
            """
            pressed_key_id = [x.key_id for x in cls.pressed_keys]
            if key.key_id not in pressed_key_id:
                if key.state == MAKE:
                    cls.pressed_keys.insert(0, key)
                else:
                    raise ValueError(f'Try to insert the key: {key} to pressed_keys list but the input state is BREAK!'
                                     f'cls.pressed_keys: {cls.pressed_keys}')
                # end if
            else:
                if key.state == BREAK:
                    cls.pressed_keys.pop(pressed_key_id.index(key.key_id))
                else:
                    raise ValueError(f'Try to remove the key: {key} from pressed_keys list but the input state is MAKE!'
                                     f'cls.pressed_keys: {cls.pressed_keys}')
                # end if
            # end if
        # end def _update_pressed_keys

        @classmethod
        def _remove_pressed_key(cls, key):
            """
            Remove key from cls.pressed_keys

            :param key: The key with its make or break state and key_id
            :type key: ``KeyMatrixTestUtils.Key``
            """
            cls._update_pressed_keys(key)
        # end def _remove_pressed_key

        @classmethod
        def debug(cls, message):
            """
            Print debug message

            :param message: The debug message
            :type message: ``str``
            """
            if cls.VERBOSE:
                stdout.write(f"{message}\n")
            # end if
        # end def debug
    # end class KeyExpectedActions

    @classmethod
    def get_key_list(cls, test_case, group_count, group_size=1, random=True, excluded_keys=None):
        """
        Generate a list of valid keys or grouped keys randomly chosen.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param group_count: number of groups to create or ``None`` to test all keys
        :type group_count: ``int`` or ``None``
        :param group_size: number of keys per group (singleton, pair, triplet, ...) - OPTIONAL
        :type group_size: ``int``
        :param random: Flag to enable the randomization of the selection (default is True) - OPTIONAL
        :type random: ``bool``
        :param excluded_keys: List of ``KEY_ID`` to remove from the random draw - OPTIONAL
        :type excluded_keys: ``list[KEY_ID]``

        :return: A list of valid keys or grouped keys
        :rtype: ``list[tuple]``
        """
        supported_key_id_list = test_case.button_stimuli_emulator.get_key_id_list()

        if not random:
            key_id_iterator = iter(supported_key_id_list)
        else:
            key_id_iterator = None
        # end if
        if group_count is None:
            internal_group_count = len(supported_key_id_list) // group_size
        else:
            internal_group_count = group_count
        # end if
        if excluded_keys is None:
            excluded_keys = DEFAULT_EXCLUDED_KEYS
        else:
            excluded_keys.extend(DEFAULT_EXCLUDED_KEYS)
        # end if

        if test_case.f.PRODUCT.FEATURES.KEYBOARD.F_PlayPauseDoublePress:
            # Exclude keys supporting the double press algorithm
            # Rationale: The firmware will delay by 500ms the HID report generation so that the next keystroke could
            # be processed and its report sent before this one.
            excluded_keys.extend(DOUBLE_PRESS_KEYS)
        # end if

        keys_list = []
        for group_count_index in range(internal_group_count):
            group = []
            key_id = None
            for group_size_index in range(group_size):
                # Exclude key ids which are not part of the translation table (i.e. KEY_ID_TO_HID_MAP)
                # Exclude key ids which are already included in the test group
                # Exclude some keys which could change the HID report generation (ex. FN Key by default)
                while (key_id is None or key_id not in HidData.KEY_ID_TO_HID_MAP or key_id in group or
                       key_id in excluded_keys):
                    if random:
                        key_id = choice(list(supported_key_id_list))
                    else:
                        try:
                            key_id = next(key_id_iterator)
                        except StopIteration:
                            # All supported keys were picked
                            if group_count is None:
                                # Case 1: select each key once at most
                                return keys_list
                            else:
                                # Case 2: fill in all the requested groups
                                key_id_iterator = iter(supported_key_id_list)
                                key_id = next(key_id_iterator)
                            # end if
                        # end try
                    # end if
                    if key_id not in HidData.KEY_ID_TO_HID_MAP:
                        test_case.log_warning(f"Warning: key {str(key_id)} not found in HID translation table",
                                              force_console_print=True)
                    # end if
                # end while
                group.append(key_id)
            # end for
            keys_list.append(tuple([x for x in group]))
        # end for
        return keys_list
    # end def get_key_list

    @classmethod
    def get_key_on_square(cls, test_case, row_indexes, column_indexes, key_count=4):
        """
        Generate a list of valid keys sharing raw and column indexes.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param row_indexes: list of raw indexes to match
        :type row_indexes: ``tuple[int]``
        :param column_indexes: list of raw indexes to match
        :type column_indexes: ``tuple[int]``
        :param key_count: number of keys to export in the list
        :type key_count: ``int``

        :return: A list of valid keys or ``None`` if the key count has not been reached
        :rtype: ``list`` or ``None``
        """
        supported_key_id_list = test_case.button_stimuli_emulator.get_key_id_list()

        # Exclude some special keys
        excluded_keys = [KEY_ID.FN_KEY, KEY_ID.HOST_1, KEY_ID.HOST_2, KEY_ID.HOST_3, KEY_ID.FN_LOCK]

        key_id_iterator = iter(supported_key_id_list)

        keys_list = []
        for _ in range(key_count):
            key_id = None
            # Exclude key ids which are not part of the translation table (i.e. KEY_ID_TO_HID_MAP)
            # Exclude some keys which could change the HID report generation (ex. FN Key by default)
            while key_id is None or key_id not in HidData.KEY_ID_TO_HID_MAP or key_id in excluded_keys:
                try:
                    key_id = next(key_id_iterator)
                except StopIteration:
                    # Select each key once at most
                    return None
                # end try
                row_index, col_index = test_case.button_stimuli_emulator.get_row_col_indexes(key_id=key_id)
                if not (row_index in row_indexes and col_index in column_indexes):
                    key_id = None
                # end if
            # end while
            if key_id is not None:
                keys_list.append(key_id)
            else:
                return None
            # end if
        # end for
        return keys_list
    # end def get_key_on_square

    @classmethod
    def get_first_supported_key_id(cls, test_case, key_ids):
        """
        Retrieve the first Key identifier from the given list which is supported by the DUT

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param key_ids: List of possible key identifiers
        :type key_ids: ``list[KEY_ID]|tuple[KEY_ID]``

        :return: First Key id from the given list which is supported by the DUT
        :rtype: ``KEY_ID`` or ``None``
        """
        if test_case.button_stimuli_emulator is not None:
            # Check keyboard supported keys
            keyboard = test_case.button_stimuli_emulator.keyboard_layout
            for key_id in key_ids:
                if key_id in keyboard.KEYS.keys() or key_id in keyboard.FN_KEYS.keys():
                    return key_id
                # end if
            # end for
        # end if
        return None
    # end def get_first_supported_key_id

    @classmethod
    def get_fn_key_list(cls, test_case, excluded_keys=None):
        """
        Get Fn key list

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param excluded_keys: Excluded key id list - OPTIONAL
        :type excluded_keys: ``list[KEY_ID] | None``

        :return: The map of Fn combination keys
        :rtype: ``dict[KEY_ID, KEY_ID]``
        """
        excluded_keys = DEFAULT_EXCLUDED_KEYS if excluded_keys is None else excluded_keys
        if test_case.f.PRODUCT.FEATURES.KEYBOARD.F_PlayPauseDoublePress:
            # Exclude keys supporting the double press algorithm
            # Rationale: The firmware will delay by 500ms the HID report generation so that the next keystroke could
            # be processed and its report sent before this one.
            excluded_keys.extend(DOUBLE_PRESS_KEYS)
        # end if

        fn_keys = {}
        for key, value in test_case.button_stimuli_emulator.get_fn_keys().items():
            if key not in excluded_keys:
                fn_keys[key] = value
            # end if
        # end for
        return fn_keys
    # end def get_fn_key_list

    @classmethod
    def send_keys_with_modifiers(cls, test_case, modifier_key_ids, group_size=1, delay=None):
        """
        Send groups of keys preceded by one or multiple modifiers.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param modifier_key_ids: List of modifiers to press before starting the keystroke sequence
        :type modifier_key_ids: ``list``
        :param group_size: number of keys per group (singleton, pair, triplet, ...) - OPTIONAL
        :type group_size: ``int``
        :param delay: delay before starting to fetch the report from the message queue
        :type delay: ``int``
        """
        test_case.kosmos.sequencer.offline_mode = True

        test_case.button_stimuli_emulator.multiple_keys_press(key_ids=modifier_key_ids, delay=1)

        # Exclude all special keys that could release one of the modifier keys.
        excluded_keys = modifier_key_ids + [KEY_ID.FN_KEY, KEY_ID.HOST_1, KEY_ID.HOST_2, KEY_ID.HOST_3, KEY_ID.FN_LOCK,
                                            KEY_ID.SHOW_DESKTOP, KEY_ID.MISSION_CTRL_TASK_VIEW,
                                            KEY_ID.APP_SWITCH_LAUNCHPAD, KEY_ID.SCREEN_CAPTURE, KEY_ID.LANGUAGE_SWITCH,
                                            KEY_ID.DICTATION, KEY_ID.EMOJI_PANEL, KEY_ID.SCREEN_LOCK, ]
        keys = KeyMatrixTestUtils.get_key_list(test_case, group_count=None, group_size=group_size, random=False,
                                               excluded_keys=excluded_keys)
        for key_group in keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_info(test_case, f'Emulate pressing a group of keys: {str(key_group)}')
            # ---------------------------------------------------------------------------
            test_case.button_stimuli_emulator.multiple_keys_press(key_ids=key_group,
                                                                  delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(test_case, f'Emulate releasing a group of keys: {str(key_group)}')
            # ---------------------------------------------------------------------------
            test_case.button_stimuli_emulator.multiple_keys_release(key_ids=key_group,
                                                                    delay=ButtonStimuliInterface.DEFAULT_DURATION)
        # end for

        test_case.button_stimuli_emulator.multiple_keys_release(key_ids=modifier_key_ids,
                                                                delay=ButtonStimuliInterface.DEFAULT_DURATION)

        test_case.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        test_case.kosmos.sequencer.play_sequence(block=False)
        if delay is not None:
            sleep(delay)
        # end if

        for modifier in modifier_key_ids:

            # ---------------------------------------------------------------------------
            LogHelper.log_info(test_case, f'Check Modifier bit in HID Keyboard report matches {str(modifier)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                          key=KeyMatrixTestUtils.Key(modifier, MAKE))
        # end for

        for key_group in keys:
            for key_id in iter(key_group):
                # ---------------------------------------------------------------------------
                LogHelper.log_info(test_case, f'Check HID Keyboard report on key {str(key_id)} press')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                              key=KeyMatrixTestUtils.Key(key_id, MAKE))
            # end for

            for key_id in iter(key_group):
                # ---------------------------------------------------------------------------
                LogHelper.log_info(test_case, f'Check HID Keyboard report on key {str(key_id)} release')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                              key=KeyMatrixTestUtils.Key(key_id, BREAK))
            # end for
        # end for

        for modifier in modifier_key_ids:
            # ---------------------------------------------------------------------------
            LogHelper.log_info(test_case, f'Check Modifier bit reset in HID Keyboard report matches {str(modifier)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=test_case,
                                                          key=KeyMatrixTestUtils.Key(modifier, BREAK))
        # end for
    # end def send_keys_with_modifiers

    @classmethod
    def get_key_id_dict(cls, test_case):
        """
        Get the mapping between Row/Column indexes and the KEY_ID

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The saved mapping with tuple (row_index, column_index) as key and key_id for value
        :rtype: ``dict``
        """
        if not hasattr(test_case, 'key_id_by_row_col'):
            test_case.key_id_by_row_col = {}
        # end if
        return test_case.key_id_by_row_col
    # end def get_key_id_dict

    @classmethod
    def get_ghost_keys_bitmaps(cls, test_case):
        """
        Check the HID report associated to a key pressed or released stimulus.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: An array of the size of the key membrane with unused position set to None, else set to 0.
        :rtype: ``list[list[None|int]]``
        """
        if not hasattr(test_case, 'key_matrix_states'):
            test_case.key_matrix_states = list([list([None for _ in range(KBD_COL_COUNT)]) for _ in range(
                KBD_ROW_COUNT)])
            for key_id in test_case.button_stimuli_emulator.get_key_id_list():
                row_index, col_index = test_case.button_stimuli_emulator.get_row_col_indexes(key_id=key_id)
                test_case.key_matrix_states[row_index][col_index] = 0
            # end for
        # end if
        return test_case.key_matrix_states
    # end def get_ghost_keys_bitmaps

    @classmethod
    def check_hid_report_by_key_id(cls, test_case, key, raise_exception=True, variant=None,
                                   get_expected_action_func=KeyExpectedActions.get):
        """
        Check the HID report associated to a key pressed or released stimulus.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key: The action key with its make or break state
        :type key: ``KeyMatrixTestUtils.Key | RemappedKey``
        :param raise_exception: Flag enabling to raise an exception when a failure occurs - OPTIONAL
        :type raise_exception: ``bool``
        :param variant: OS detected by the firmware - OPTIONAL
        :type variant: ``str`` or ``None``
        :param get_expected_action_func: Method called to extract the expected HID reports - OPTIONAL
        :type get_expected_action_func:
            ``KeyExpectedActions.get | FKCTestUtils.Remapping.get_custom_key_expected_actions``

        :return: Success status
        :rtype: ``bool``

        :raise ``NoMessageReceived``: Exception thrown by ``HidMessageQueue`` when the expected message hasn't been
        received.
        :raise ``TypeError``: If the input get_expected_action_func is not callable
        """
        if not callable(get_expected_action_func):
            raise TypeError("get_expected_action_func must be a callable")
        # end if

        success = True
        key_matrix_states = None
        row_index = None
        column_index = None
        immediate = None
        delayed = None

        # Default OS handling
        marketing_name = test_case.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        if variant is None:
            variant = OS.MAC if marketing_name.endswith('for Mac') else OS.IPAD if marketing_name.endswith('Apple') \
                else OS.WINDOWS
        # end if

        if test_case.f.PRODUCT.FEATURES.KEYBOARD.F_GhostKeyDetection:
            row_index, column_index = test_case.button_stimuli_emulator.get_row_col_indexes(key_id=key.key_id)
            key_matrix_states = KeyMatrixTestUtils.get_ghost_keys_bitmaps(test_case)
        # end if

        if key.state == MAKE:
            if test_case.f.PRODUCT.FEATURES.KEYBOARD.F_GhostKeyDetection:
                # Implement ghost key detection algorithm
                if KeyMatrixTestUtils.ghost_key_detection_on_key_press(test_case, key_matrix_states, row_index,
                                                                       column_index, key.key_id):
                    # Add delay here to prevent the next operations to trigger a timeout
                    sleep(ButtonStimuliInterface.DEFAULT_DURATION)
                    return success
                # end if
            # end if
        else:
            if test_case.f.PRODUCT.FEATURES.KEYBOARD.F_GhostKeyDetection:
                # Check if it's a ghosted key
                is_ghosted_key, immediate, delayed = KeyMatrixTestUtils.deghosting_key_on_key_release(
                    test_case, key_matrix_states, row_index, column_index)
                if is_ghosted_key:
                    # Releasing a ghosted key do not generate any HID report
                    # Add delay here to prevent the next operations to trigger a timeout
                    sleep(ButtonStimuliInterface.DEFAULT_DURATION)
                    return success
                # end if
            # end if
        # end if

        if test_case.f.PRODUCT.FEATURES.KEYBOARD.F_GhostKeyDetection and immediate is not None:
            # Extract the expected HID parameters for the make of the previously ghosted key
            responses_class, fields_name, fields_value = cls.KeyExpectedActions.get(
                key=KeyMatrixTestUtils.Key(immediate, MAKE), variant=variant)

            KeyMatrixTestUtils.check_actions(test_case, responses_class, fields_name, fields_value, raise_exception)
        # end if

        # Extract the expected HID parameters from table
        responses_class, fields_name, fields_value = get_expected_action_func(key, variant)

        # noinspection PyBroadException
        KeyMatrixTestUtils.check_actions(test_case, responses_class, fields_name, fields_value, raise_exception)

        if test_case.f.PRODUCT.FEATURES.KEYBOARD.F_GhostKeyDetection and delayed is not None:
            # Extract the expected HID parameters for the make of the previously ghosted key
            responses_class, fields_name, fields_value = cls.KeyExpectedActions.get(
                key=KeyMatrixTestUtils.Key(delayed, MAKE), variant=variant)
            KeyMatrixTestUtils.check_actions(test_case, responses_class, fields_name, fields_value, raise_exception)
        # end if
        return success
    # end def check_hid_report_by_key_id

    @staticmethod
    def get_expected_actions(key_id, action_type, variant):
        # Expected FW key codes could depend on the OS running on the host:
        # 'windowsOS' (default), 'macOS', 'iPadOS' or 'chromeOS'
        if variant not in iter(HidData.KEY_ID_TO_HID_MAP[key_id]):
            # If we have no information about the detected OS, we select the first available variant
            variant = next(iter(HidData.KEY_ID_TO_HID_MAP[key_id]))
        # end if
        # Extract the expected HID parameters from table
        responses_class = HidData.KEY_ID_TO_HID_MAP[key_id][variant][action_type]['Responses_class']
        fields_name = HidData.KEY_ID_TO_HID_MAP[key_id][variant][action_type]['Fields_name']
        fields_value = HidData.KEY_ID_TO_HID_MAP[key_id][variant][action_type]['Fields_value']
        return responses_class, fields_name, fields_value
    # end def get_expected_actions

    @staticmethod
    def check_actions(test_case, responses_class, fields_name, fields_value, raise_exception):
        """
        Check the HID report associated to a keystroke.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param responses_class: list of HID report messages
        :type responses_class: ``list[BitFieldContainerMixin]``
        :param fields_name: list of names related to the fields that are expected to change
        :type fields_name: ``list[str | tuple[str, str]]``
        :param fields_value: list of values related to the fields that are expected to change
        :type fields_value: ``list[int | tuple[int, int]]``
        :param raise_exception: Flag enabling to raise an exception when a failure occurs
        :type raise_exception: ``bool``
        """
        if len(responses_class) == 0:
            # Add timing here to prevent the next operations to trigger a timeout
            sleep(ButtonStimuliInterface.DEFAULT_DURATION)
        # end if
        for i in range(len(responses_class)):
            # Retrieve the previous HID report
            last_report = KeyMatrixTestUtils.get_last_report(test_case, responses_class[i])
            # Compute the next expected report
            for j in range(len(fields_name[i])):
                if responses_class[i] is HidConsumer:
                    KeyMatrixTestUtils._handle_consumer_report(last_report, value=fields_value[i][j])
                elif responses_class[i] is HidKeyboard and fields_name[i][j].lower().startswith('key_code'):
                    KeyMatrixTestUtils._handle_keyboard_report(last_report, value=fields_value[i][j])
                elif fields_value[i][j] >= 0:
                    last_report.setValue(last_report.getFidFromName(fields_name[i][j].lower()), fields_value[i][j])
                else:
                    last_report.setValue(last_report.getFidFromName(fields_name[i][j].lower()), 0)
                # end if
            # end for

            # Handle the case of a desynchronization with the DUT
            is_saved_report_matching = False
            saved_reports = KeyMatrixTestUtils.dut_mismached_reports(test_case)
            if len(saved_reports) > 0:
                for saved_report in saved_reports:
                    if HexList(last_report) == HexList(saved_report):
                        LogHelper.log_info(test_case, f'The expected report {HexList(last_report)} matches the '
                                                      f'missing {HexList(saved_report)}')
                        saved_reports.remove(saved_report)
                        is_saved_report_matching = True
                        break
                    # end if
                # end for
                if not is_saved_report_matching:
                    KeyMatrixTestUtils.get_missing_report_counter(test_case, increment=True)
                # end if
            else:
                # Retrieve the next HID report
                hid_packet = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                                   class_type=responses_class[i], check_first_message=False)

                test_case.logTrace(f'{responses_class[i].__name__}: {str(hid_packet)}\n')
                if not last_report == hid_packet:
                    KeyMatrixTestUtils.get_missing_report_counter(test_case, increment=True)
                    LogHelper.log_info(test_case, f'The expected report {HexList(last_report)} differs from the one '
                                                  f'received {HexList(hid_packet)}')
                    KeyMatrixTestUtils.dut_mismached_reports(test_case, report=HexList(hid_packet))
                    if raise_exception:
                        test_case.fail(f'Error on report verification {hid_packet} != {last_report}')
                    # end if
                # end if
            # end if
        # end for
    # end def check_actions

    @classmethod
    def _handle_consumer_report(cls, last_report, value):
        """
        Build the expected consumer HID report

        :param last_report: The last HID report returned to the host
        :type last_report: ``HidConsumer``
        :param value: new field value
        :type value: ``int``
        """
        if value >= 0:
            if not last_report.is_key_empty(2):
                # skip the handling of this key as the 2 slots of the HID report are already full
                return
            elif not last_report.is_key_empty(1):
                # Put the value in the second slot
                last_report.key_2 = HexList(Numeral(value, HidConsumer.LEN.KEY_2 // 8))
            else:
                # Put the value in the first slot
                last_report.key_1 = HexList(Numeral(value, HidConsumer.LEN.KEY_1 // 8))
            # end if
        else:
            if int(Numeral(last_report.key_2)) == -value:
                # Clean-up the value in the second slot
                last_report.key_2 = HidConsumer.DEFAULT.RELEASED
            elif int(Numeral(last_report.key_1)) == -value:
                if not last_report.is_key_empty(2):
                    # Move the value from the second slot to the first one
                    last_report.key_1 = last_report.key_2
                    last_report.key_2 = HidConsumer.DEFAULT.RELEASED
                else:
                    # Clean-up the value in the first slot
                    last_report.key_1 = HidConsumer.DEFAULT.RELEASED
                # end if
            else:
                # skip the clean-up of this key as it does not match any of the 2 slots
                return
            # end if
        # end if
    # end def _handle_consumer_report

    @classmethod
    def _handle_keyboard_report(cls, last_report, value):
        """
        Build the expected keyboard HID report

        :param last_report: The last HID report returned to the host
        :type last_report: ``HidKeyboard``
        :param value: new field value
        :type value: ``int``
        """
        if value >= 0:
            key_code_to_write = value
            for index in range(1, 7):
                key_code = to_int(last_report.getValue(last_report.getFidFromName(f'key_code{index}')))
                if key_code == 0:
                    last_report.setValue(last_report.getFidFromName(f'key_code{index}'), key_code_to_write)
                    break
                elif key_code == key_code_to_write:
                    # Duplicated key code
                    break
                elif key_code > key_code_to_write:
                    last_report.setValue(last_report.getFidFromName(f'key_code{index}'), key_code_to_write)
                    key_code_to_write = key_code
                # end if
            # end for
        else:
            move_left = False
            for index in range(1, 6):
                if to_int(last_report.getValue(last_report.getFidFromName(f'key_code{index}'))) == -value or move_left:
                    last_report.setValue(last_report.getFidFromName(f'key_code{index}'),
                                         last_report.getValue(last_report.getFidFromName(f'key_code{index + 1}')))
                    move_left = True
                # end if
            # end for
            last_report.setValue(last_report.getFidFromName(f'key_code6'), 0)
        # end if
    # end def _handle_keyboard_report

    @classmethod
    def ghost_key_detection_on_key_press(cls, test_case, key_matrix_states, row_index, column_index, key_id):
        """
        Check if we have a ghost key situation.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_matrix_states: An array representation of the key membrane with unused position set to None,
                                  else set to 0.
        :rtype: ``list[list]``
        :param row_index: Index of the targeted row
        :type row_index: ``int``
        :param column_index: Index of the targeted column
        :type column_index: ``int``
        :param key_id: key internal unique reference
        :type key_id: ``KEY_ID``

        :return: True if a ghost key has been detected, False otherwise
        :rtype: ``bool``
        """
        # cf https://drive.google.com/file/d/0Bz6TfM0EppwLSl9FbnM2cmEyMDA/view
        other_col_index = None
        other_row_index = None
        key_dict = KeyMatrixTestUtils.get_key_id_dict(test_case)

        # Check if the same row is already used by another key pressed
        key_pressed_on_row = [x for x in range(len(key_matrix_states[row_index])) if key_matrix_states[row_index][x]
                              == KeyMatrixTestUtils.KEYSTATE.PRESSED]
        if len(key_pressed_on_row) > 0:
            other_col_index = key_pressed_on_row[0]
        # end if
        # Check whether the same column is already used by another key pressed
        key_pressed_on_column = [x for x in range(len(key_matrix_states)) if key_matrix_states[x][column_index] is
                                 not None and key_matrix_states[x][column_index] == KeyMatrixTestUtils.KEYSTATE.PRESSED]
        if len(key_pressed_on_column) > 0:
            other_row_index = key_pressed_on_column[0]
        # end if

        # Check if the same row is already a ghosted key
        key_ghosted_on_row = [x for x in range(len(key_matrix_states[row_index])) if key_matrix_states[row_index][x]
                              in [KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST, KeyMatrixTestUtils.KEYSTATE.INDIRECT_GHOST]]
        if len(key_ghosted_on_row) > 0 and other_row_index is not None:
            key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST
            key_matrix_states[row_index][key_ghosted_on_row[0]] = KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST
            key_dict[(row_index, column_index)] = key_id
            return True
        # end if

        # Check if the same column is already a ghosted key
        key_ghosted_on_column = [x for x in range(len(key_matrix_states)) if key_matrix_states[x][column_index] in
                                 [KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST, KeyMatrixTestUtils.KEYSTATE.INDIRECT_GHOST]]
        if len(key_ghosted_on_column) > 0 and other_col_index is not None:
            key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST
            key_matrix_states[key_ghosted_on_column[0]][column_index] = KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST
            key_dict[(row_index, column_index)] = key_id
            return True
        # end if

        # Both row and column are already used
        if other_row_index is not None and other_col_index is not None:
            # Check if the fourth position is defined in the keyboard layout
            if key_matrix_states[other_row_index][other_col_index] is not None:
                LogHelper.log_info(
                    test_case, f'Direct ghost key detected on row_index={row_index} and column_index {column_index}')
                if key_matrix_states[other_row_index][other_col_index] == 0:
                    key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST
                elif key_matrix_states[other_row_index][other_col_index] in \
                        [KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST, KeyMatrixTestUtils.KEYSTATE.INDIRECT_GHOST]:
                    key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST
                    key_matrix_states[other_row_index][other_col_index] = KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST
                    LogHelper.log_info(test_case, f'Double ghost key detected on row_index={row_index} and '
                                                  f'column_index {column_index}')
                # end if
                key_dict[(row_index, column_index)] = key_id
                return True
            # end if
        elif not (other_row_index is None and other_col_index is None):
            # At least one of the two directions is already used
            # Check if the other column is already used by a third key pressed
            if other_col_index is not None and sum(
                    [key_matrix_states[x][other_col_index] for x in range(len(key_matrix_states))
                     if key_matrix_states[x][other_col_index] is not None]) > 1:
                other_row_index = ([x for x in range(len(key_matrix_states))
                                    if key_matrix_states[x][other_col_index] is not None and
                                    key_matrix_states[x][other_col_index] > KeyMatrixTestUtils.KEYSTATE.RELEASED and
                                    x != row_index][0])
                other_col_index = column_index
            # end if
            # Check whether the other row is already used by a third key pressed
            elif other_row_index is not None and \
                    sum([x for x in key_matrix_states[other_row_index] if x is not None]) > 1:
                other_col_index = ([x for x in range(len(key_matrix_states[other_row_index]))
                                    if key_matrix_states[other_row_index][x] is not None and
                                    key_matrix_states[other_row_index][x] > KeyMatrixTestUtils.KEYSTATE.RELEASED and
                                    x != column_index][0])
                other_row_index = row_index
            # end if
            if other_row_index is not None and other_col_index is not None:
                if key_matrix_states[other_row_index][other_col_index] is not None:
                    LogHelper.log_info(test_case, f'Indirect ghost key detected on row_index={row_index} and '
                                                  f'column_index {column_index}')
                    if key_matrix_states[other_row_index][other_col_index] in [KeyMatrixTestUtils.KEYSTATE.RELEASED,
                                                                               KeyMatrixTestUtils.KEYSTATE.PRESSED]:
                        key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.INDIRECT_GHOST
                    elif (key_matrix_states[other_row_index]
                          [other_col_index] in [KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST,
                                                KeyMatrixTestUtils.KEYSTATE.INDIRECT_GHOST]):
                        key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST
                        key_matrix_states[other_row_index][other_col_index] = KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST
                        LogHelper.log_info(test_case, f'Double ghost key detected on row_index={row_index} and '
                                                      f'column_index {column_index}')
                    # end if
                    key_dict[(row_index, column_index)] = key_id
                    return True
                # end if
            # end if
        # end if
        key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.PRESSED
        return False
    # end def ghost_key_detection_on_key_press

    @classmethod
    def deghosting_key_on_key_release(cls, test_case, key_matrix_states, row_index, column_index):
        """
        Check if the key release is unghosting another key.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_matrix_states: An array representation of the key membrane with unused position set to None,
                                  else set to 0.
        :rtype: ``list[list]``
        :param row_index: Index of the targeted row
        :type row_index: ``int``
        :param column_index: Index of the targeted column
        :type column_index: ``int``

        :return: True if a ghost key has been released, False otherwise
        :rtype: ``bool``
        """
        immediate = None
        delayed = None
        # Check if it's a ghosted key
        is_ghost_key, _, _ = KeyMatrixTestUtils.is_ghost_key(test_case, key_matrix_states, row_index=row_index,
                                                             column_index=column_index)
        if is_ghost_key:
            key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.RELEASED
            # Releasing a ghosted key do not generate any HID report
            return True, None, None
        elif key_matrix_states[row_index][column_index] == KeyMatrixTestUtils.KEYSTATE.PRESSED:
            key_matrix_states[row_index][column_index] = KeyMatrixTestUtils.KEYSTATE.RELEASED
            # Check if the same row has a pressed or a ghosted key
            is_ghost_key, row, col = KeyMatrixTestUtils.is_ghost_key(test_case, key_matrix_states, row_index=row_index)
            if not is_ghost_key:
                # Check if the same column has a pressed or a ghosted key
                is_ghost_key, row, col = KeyMatrixTestUtils.is_ghost_key(test_case, key_matrix_states,
                                                                         column_index=column_index)
            # end if
            if is_ghost_key:
                status = key_matrix_states[row][col]
                if status == KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST:
                    for (ghosted_key_row, ghosted_key_col) in KeyMatrixTestUtils.get_key_id_dict(test_case).keys():
                        key_matrix_states[ghosted_key_row][ghosted_key_col] = KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST
                    # end for
                else:
                    key_matrix_states[row][col] = KeyMatrixTestUtils.KEYSTATE.PRESSED
                    key_ref = KeyMatrixTestUtils.get_key_id_dict(test_case)
                    if status == KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST:
                        delayed = key_ref[(row, col)]
                    else:
                        immediate = key_ref[(row, col)]
                    # end if
                # end if
            # end if
        # end if
        return False, immediate, delayed
    # end def deghosting_key_on_key_release

    @classmethod
    def is_ghost_key(cls, test_case, key_matrix_states, row_index=None, column_index=None, excluded_row_index=None,
                     excluded_column_index=None):
        """
        Check if the key release is unghosting another key.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_matrix_states: An array representation of the key membrane with unused position set to None,
                                  else set to 0.
        :rtype: ``list[list]``
        :param row_index: Index of the targeted row
        :type row_index: ``int``
        :param column_index: Index of the targeted column
        :type column_index: ``int``
        :param excluded_row_index: Row index to be ignored
        :type excluded_row_index: ``int``
        :param excluded_column_index: Column index to be ignored
        :type excluded_column_index: ``int``

        :return: True if a ghost key has been released, False otherwise plus the row and column indexes
        :rtype: ``tuple[bool, int, int]``
        """
        if row_index is not None and column_index is not None:
            if key_matrix_states[row_index][column_index] in [KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST,
                                                              KeyMatrixTestUtils.KEYSTATE.INDIRECT_GHOST,
                                                              KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST]:
                return True, row_index, column_index
            # end if
        elif row_index is not None:
            row_values = key_matrix_states[row_index]
            for value in row_values:
                if value in [None, KeyMatrixTestUtils.KEYSTATE.RELEASED]:
                    continue
                # end if
                key_column_index = row_values.index(value)
                if excluded_column_index is not None and key_column_index == excluded_column_index:
                    continue
                # end if
                if value in [KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST, KeyMatrixTestUtils.KEYSTATE.INDIRECT_GHOST,
                             KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST]:
                    return True, row_index, key_column_index
                elif value == KeyMatrixTestUtils.KEYSTATE.PRESSED:
                    is_ghosted, row, col = KeyMatrixTestUtils.is_ghost_key(test_case, key_matrix_states,
                                                                           column_index=key_column_index,
                                                                           excluded_row_index=row_index)
                    if is_ghosted:
                        return True, row, col
                    # end if
                # end if
            # end for
        elif column_index is not None:
            column_values = [key_matrix_states[x][column_index] for x in range(len(key_matrix_states))]
            for value in column_values:
                if value in [None, KeyMatrixTestUtils.KEYSTATE.RELEASED]:
                    continue
                # end if
                key_row_index = column_values.index(value)
                if excluded_row_index is not None and key_row_index == excluded_row_index:
                    continue
                # end if
                if value in [KeyMatrixTestUtils.KEYSTATE.DIRECT_GHOST, KeyMatrixTestUtils.KEYSTATE.INDIRECT_GHOST,
                             KeyMatrixTestUtils.KEYSTATE.DOUBLE_GHOST]:
                    return True, key_row_index, column_index
                elif value == KeyMatrixTestUtils.KEYSTATE.PRESSED:
                    is_ghosted, row, col = KeyMatrixTestUtils.is_ghost_key(test_case, key_matrix_states,
                                                                           row_index=key_row_index,
                                                                           excluded_column_index=column_index)
                    if is_ghosted:
                        return True, row, col
                    # end if
                # end if
            # end for
        # end if
        return False, row_index, column_index
    # end def is_ghost_key

    @classmethod
    def switch_fn_lock_state(cls, test_case, enable=True):
        """
        Create the Key sequence to change the FN Lock state.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param enable: Flag indicating the targeted FN Lock state
        :type enable: ``bool``

        :return: Flag indicating that a Fn-Lock change occurred
        :rtype: ``bool``
        """
        if test_case.button_stimuli_emulator.fn_locked == enable:
            # If Fn Lock already matches the required mode, exit the processing here
            return False
        # end if
        # ---------------------------------------------------------------------------
        LogHelper.log_info(test_case, 'Switch Fn-Lock state')
        # ---------------------------------------------------------------------------
        if test_case.f.PRODUCT.F_IsGaming:
            # G: Activate Fn-Lock with the Fn Key only
            action_list = [(KEY_ID.FN_KEY, KEYSTROKE)]
        else:
            # C&P: Activate Fn-Lock with the Fn-ESC command
            action_list = [(KEY_ID.FN_KEY, MAKE), (KEY_ID.KEYBOARD_ESCAPE, KEYSTROKE), (KEY_ID.FN_KEY, BREAK)]
        # end if
        test_case.button_stimuli_emulator.perform_action_list(action_list=action_list, delay=.4)
        assert test_case.button_stimuli_emulator.fn_locked == enable, 'FN Lock key has not been correctly pressed !'

        return True
    # end def switch_fn_lock_state

    @classmethod
    def stroke_key_with_fn(cls, test_case, key_id):
        """
        Emulate a keystroke with non-function key or function key

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID``
        """
        test_case.kosmos.sequencer.offline_mode = True

        fn_keys = test_case.button_stimuli_emulator.get_fn_keys()

        if key_id in fn_keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Emulate a key press on Fn-Key')
            # ---------------------------------------------------------------------------
            test_case.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                                  delay=ButtonStimuliInterface.DEFAULT_DURATION)
            assert test_case.button_stimuli_emulator.fn_pressed, 'FN key has not been correctly pressed'

            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, f'Emulate a keystroke on the key {str(key_id)}')
            # ---------------------------------------------------------------------------
            test_case.button_stimuli_emulator.keystroke(key_id=fn_keys[key_id])

            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Emulate a key release on Fn-Key')
            # ---------------------------------------------------------------------------
            test_case.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                                    delay=ButtonStimuliInterface.DEFAULT_DURATION)
        else:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(test_case, f'Emulate a keystroke on the key {str(key_id)}')
            # ---------------------------------------------------------------------------
            test_case.button_stimuli_emulator.keystroke(key_id=key_id)
        # end if

        test_case.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        test_case.kosmos.sequencer.play_sequence()

    # end def stroke_key_with_fn

    @classmethod
    def stroke_keys_in_sequence(cls, test_case, keys, collect_hid_report=False):
        """
        Stroke keys.

        Note: Enable collect_hid_report will empty HID message queue

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param keys: Stroke specific keys
        :type keys: ``list[KEY_ID]``
        :param collect_hid_report: Flag enabling to collect HID message after stroked key - OPTIONAL
        :type collect_hid_report: ``bool``

        :return: keys_reports
        :rtype: ``list[tuple(KEY_ID, HexList(HIDMessage))]``
        """
        keys_reports = []

        for key in keys:
            test_case.button_stimuli_emulator.keystroke(key_id=key)

            if collect_hid_report:
                while not test_case.is_current_hid_dispatcher_queue_empty(
                        queue=test_case.hidDispatcher.hid_message_queue):
                    keys_reports.append((
                        key, HexList(test_case.getMessage(queue=test_case.hidDispatcher.hid_message_queue))))
                # end while
            # end if
        # end for

        return keys_reports
    # end def stroke_keys_in_sequence

    @classmethod
    def get_keyboard_usage_index(cls, keys):
        """
        Get keys index of keys from keyboard usage.

        :param keys: key ID
        :type keys: ``list``

        :return: keys index
        :rtype: ``list[int]``
        """
        return [i if i not in ALL_KEYS else ALL_KEYS[i] for i in keys]
    # end def get_keyboard_usage_index

    @classmethod
    def emulate_os_shortcut(cls, test_case, os_type=OS.WINDOWS, duration=ButtonStimuliInterface.LONG_PRESS_DURATION,
                            delay=None):
        """
        Emulate the shortcut to enter a specific os mode (long press on fn + ).

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param os_type: OS detected by the firmware - OPTIONAL
        :type os_type: ``str`` or ``None``
        :param duration: timing between the O key press and release
        :type duration: ``float``
        :param delay: delay after the Fn key release
        :type delay: ``float`` or ``None``
        """
        assert os_type in [OS.WINDOWS, OS.MAC, OS.IPAD, OS.CHROME, OS.INVERTED_MAC, OS.ANDROID], \
            f'wrong mode parameter: {os_type} received'

        test_case.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=cls.TEN_MS)
        if os_type == OS.WINDOWS:
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_P, duration=duration, delay=cls.TEN_MS)
        elif os_type == OS.MAC:
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_O, duration=duration, delay=cls.TEN_MS)
        elif os_type == OS.IPAD:
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_I, duration=duration, delay=cls.TEN_MS)
        elif os_type == OS.CHROME:
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_C, duration=duration, delay=cls.TEN_MS)
        elif os_type == OS.INVERTED_MAC:
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_U, duration=duration, delay=cls.TEN_MS)
        elif os_type == OS.ANDROID:
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.KEYBOARD_G, duration=duration, delay=cls.TEN_MS)
        # end if
        additional_delay = delay if delay is not None else cls.TEN_MS
        test_case.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY], delay=additional_delay)
    # end def emulate_os_shortcut

# end class KeyMatrixTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
