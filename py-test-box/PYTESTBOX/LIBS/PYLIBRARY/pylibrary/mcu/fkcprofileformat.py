#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.fkcprofileformat
:brief: FKC profile format definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/3/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from binascii import a2b_hex
from binascii import crc32
from enum import IntEnum
from enum import unique
from math import ceil
from warnings import warn

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hid.usbhidusagetable import ConsumerHidUsage
from pyhid.hid.usbhidusagetable import KEYBOARD_HID_USAGE_TO_KEY_ID_MAP
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.keyid import ModifierKeys
from pylibrary.mcu.profileformat import AcPanCommand
from pylibrary.mcu.profileformat import ConsumerKeyCommand
from pylibrary.mcu.profileformat import KeyAction
from pylibrary.mcu.profileformat import MouseButtonCommand
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.mcu.profileformat import ProfileMacro
from pylibrary.mcu.profileformat import RollerCommand
from pylibrary.mcu.profileformat import StandardKeyCommand
from pylibrary.mcu.profileformat import XYCommand
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
NOT_REMAPPABLE_KEY_LIST = [KEY_ID.FN_KEY, KEY_ID.G_SHIFT, KEY_ID.HOST_1, KEY_ID.HOST_2, KEY_ID.HOST_3,
                           KEY_ID.BLE_CONNECTION, KEY_ID.LS2_BLE_CONNECTION_TOGGLE, KEY_ID.LS2_CONNECTION,
                           KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN, KEY_ID.DIMMING_KEY, KEY_ID.GAME_MODE_KEY,
                           KEY_ID.CYCLE_THROUGH_ANIMATION_EFFECTS, KEY_ID.CYCLE_THROUGH_COLOR_EFFECT_SUB_SETTINGS,
                           KEY_ID.KEYBOARD_POWER, KEY_ID.FKC_TOGGLE]

MODIFIER_KEY_LIST = ModifierKeys.FKC

MODIFIER_BITFIELD_TO_KEY_ID = {
    FullKeyCustomization.TriggerBitField.R_GUI:     KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,
    FullKeyCustomization.TriggerBitField.R_ALT:     KEY_ID.KEYBOARD_RIGHT_ALT,
    FullKeyCustomization.TriggerBitField.R_SHIFT:   KEY_ID.KEYBOARD_RIGHT_SHIFT,
    FullKeyCustomization.TriggerBitField.R_CTRL:    KEY_ID.KEYBOARD_RIGHT_CONTROL,
    FullKeyCustomization.TriggerBitField.L_GUI:     KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,
    FullKeyCustomization.TriggerBitField.L_ALT:     KEY_ID.KEYBOARD_LEFT_ALT,
    FullKeyCustomization.TriggerBitField.L_SHIFT:   KEY_ID.KEYBOARD_LEFT_SHIFT,
    FullKeyCustomization.TriggerBitField.L_CTRL:    KEY_ID.KEYBOARD_LEFT_CONTROL,
}

KEY_ID_TO_MODIFIER_BITFIELD = {
    KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION:    FullKeyCustomization.TriggerBitField.R_GUI,
    KEY_ID.KEYBOARD_RIGHT_ALT:              FullKeyCustomization.TriggerBitField.R_ALT,
    KEY_ID.KEYBOARD_RIGHT_SHIFT:            FullKeyCustomization.TriggerBitField.R_SHIFT,
    KEY_ID.KEYBOARD_RIGHT_CONTROL:          FullKeyCustomization.TriggerBitField.R_CTRL,
    KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION:     FullKeyCustomization.TriggerBitField.L_GUI,
    KEY_ID.KEYBOARD_LEFT_ALT:               FullKeyCustomization.TriggerBitField.L_ALT,
    KEY_ID.KEYBOARD_LEFT_SHIFT:             FullKeyCustomization.TriggerBitField.L_SHIFT,
    KEY_ID.KEYBOARD_LEFT_CONTROL:           FullKeyCustomization.TriggerBitField.L_CTRL,
}


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FkcProfileButton(ProfileButton):
    """
    Profile Button definition class for FKC feature
    """

    @unique
    class ButtonRemapping(IntEnum):
        """
        Button remapping Opcode (i.e. Byte 1)
        """
        BUTTON_NOT_SENT = 0x00
        GENERIC_MOUSE_BUTTON = 0x01
        STANDARD_KEY = 0x02
        CONSUMER_KEY = 0x03
        VIRTUAL_MODIFIER = 0x04
    # end class ButtonRemapping

    @unique
    class FunctionExecution(IntEnum):
        """
        Function execution Opcode (i.e. Byte 1)
        """
        NO_ACTION = 0x00
        TILT_LEFT = 0x01
        TILT_RIGHT = 0x02
        SELECT_NEXT_DPI = 0x03
        SELECT_PREVIOUS_DPI = 0x04
        CYCLE_THROUGH_DPI = 0x05
        DEFAULT_DPI = 0x06
        DPI_SHIFT = 0x07
        SELECT_NEXT_PROFILE = 0x08
        SELECT_PREVIOUS_PROFILE = 0x09
        CYCLE_THROUGH_PROFILE = 0x0A
        BATTERY_LIFE_INDICATOR = 0x0C
        SWITCH_TO_SPECIFIC_PROFILE = 0x0D
    # end class FunctionExecution

    @classmethod
    def create_empty_button(cls):
        """
        Create an empty button with zeros HID usage

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        return cls.Button(param_1=0x80, param_2=0x00, param_3=0, param_4=0)
    # end def create_empty_button

    # noinspection PyMethodOverriding
    @classmethod
    def create_standard_key(cls, key_id):
        """
        Create standard key settings

        :param key_id: The key id
        :type key_id: ``KEY_ID``

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        return super().create_standard_key(key_id=key_id)
    # end def create_standard_key

    @classmethod
    def create_fn_key(cls):
        """
        Create Fn key settings

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        return cls.Button(param_1=cls.Category.BUTTON_REMAPPING, param_2=cls.ButtonRemapping.VIRTUAL_MODIFIER,
                          param_3=0, param_4=1)
    # end def create_fn_key

    @classmethod
    def create_gshift_key(cls):
        """
        Create GShift key settings

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``
        """
        return cls.Button(param_1=cls.Category.BUTTON_REMAPPING, param_2=cls.ButtonRemapping.VIRTUAL_MODIFIER,
                          param_3=0, param_4=2)
    # end def create_gshift_key

    # noinspection PyShadowingBuiltins
    @classmethod
    def create_function_button(cls, function_type, profile_number=None):
        """
        Create function execution button settings

        :param function_type: Function execution button
        :type function_type: ``ProfileButton.FunctionExecution``
        :param profile_number: The parameter be used for Enabled Profile specific number - OPTIONAL
        :type profile_number: ``int | None``

        :return: The settings of the profile button
        :rtype: ``ProfileButton.Button``

        :raise ``AssertionError``: If the function type is out of range
        """
        assert function_type in [function_execution.value for function_execution in FkcProfileButton.FunctionExecution]
        return super().create_function_button(function_type=function_type, profile_number=profile_number)
    # end def create_function_button
# end class FkcProfileButton


class FkcMainTable:
    """
    FKC Main Table definition class

    https://docs.google.com/spreadsheets/d/1-EmO2L0k_nDq4fASdaM3T6Ktn7V5P36NULwHgRpbVVg/view#gid=1017032508&range=A246

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Table Id                      8
    FkcGroupCnt                   8
    Group[n]                      (16 + 8 x 9) x n
    ============================  ==========
    """

    TABLE_ID = 0x00

    @unique
    class Layer(IntEnum):
        """
        The layers of FKC main table definition class
        """
        BASE = 0
        FN = 1
        GSHIFT = 2

        @classmethod
        def to_file_type_id(cls, layer):
            """
            Convert layer to file type id

            :param layer: The layer of Fkc main table
            :type layer: ``FkcMainTable.Layer | int``

            :return: The file type id
            :rtype: ``ProfileManagement.FileTypeId.X1B05``

            :raise ``ValueError``: If the input layer is unknown
            """
            if layer == cls.BASE:
                return ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE
            elif layer == cls.FN:
                return ProfileManagement.FileTypeId.X1B05.FN_LAYER_SETTINGS_FILE
            elif layer == cls.GSHIFT:
                return ProfileManagement.FileTypeId.X1B05.GSHIFT_LAYER_SETTINGS_FILE
            else:
                raise ValueError(f'Unknown layer: {layer}')
            # end if
        # end def to_file_type_id

        @classmethod
        def to_profile_tag(cls, layer):
            """
            Convert layer to the profile management tag

            :param layer: The layer of Fkc main table
            :type layer: ``FkcMainTable.Layer | int``

            :return: The profile management tag
            :rtype: ``ProfileManagement.Tag``

            :raise ``ValueError``: If the input layer is unknown
            """
            if layer == cls.BASE:
                return ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE
            elif layer == cls.FN:
                return ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_FN
            elif layer == cls.GSHIFT:
                return ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_GSHIFT
            else:
                raise ValueError(f'Unknown layer: {layer}')
            # end if
        # end def to_profile_tag
    # end class Layer

    class Group:
        """
        Group in the table represents one or more keypresses grouped according to the non-modifier trigger key

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        TriggerCidx                   8
        Num                           8
        Row[n]                        8 x 9 x n
        ============================  ==========
        """

        ROW_LENGTH = 9

        class Row(BitFieldContainerMixin):
            """
            The row definition of Modifier lookup table

            Note:
                The fkcIdx numbering is continuous across the entire table and not restarted with each group.
                The fkcIdx is used when reporting keypresses to SW. It uniquely identifies any row in the table.

            Format:
            ============================  ==========
            Name                          Bit count
            ============================  ==========
            FkcIdx                        8 (Be assigned in Group.__hexlist__())
            TriggerBitfield               16
            ActionBitfield                16
            ButtonSetting                 32
            ============================  ==========
            """

            class FID:
                """
                Field Identifiers
                """
                TRIGGER_BITFIELD = 0xFF
                ACTION_BITFIELD = TRIGGER_BITFIELD - 1
                BUTTON_SETTING = ACTION_BITFIELD - 1
            # end class FID

            class LEN:
                """
                Field Lengths in bits
                """
                TRIGGER_BITFIELD = 0x10
                ACTION_BITFIELD = 0x10
                BUTTON_SETTING = 0x20
            # end class LEN

            FIELDS = (
                BitField(
                    fid=FID.TRIGGER_BITFIELD,
                    length=LEN.TRIGGER_BITFIELD,
                    title='TriggerBitfield',
                    name='trigger_bitfield',
                    checks=(CheckHexList(LEN.TRIGGER_BITFIELD // 8), CheckInt(),), ),
                BitField(
                    fid=FID.ACTION_BITFIELD,
                    length=LEN.ACTION_BITFIELD,
                    title='ActionBitfield',
                    name='action_bitfield',
                    checks=(CheckHexList(LEN.ACTION_BITFIELD // 8), CheckInt(),), ),
                BitField(
                    fid=FID.BUTTON_SETTING,
                    length=LEN.BUTTON_SETTING,
                    title='ButtonSetting',
                    name='button_setting',
                    checks=(CheckHexList(LEN.BUTTON_SETTING // 8), CheckInt(),), ),
            )

            def __init__(self, trigger_bitfield, action_bitfield, button_setting, **kwargs):
                """
                :param trigger_bitfield: Bitmap of trigger modifiers
                :type trigger_bitfield: ``int | FullKeyCustomization.TriggerBitField``
                :param action_bitfield: Bitmap of target action modifiers
                :type action_bitfield: ``int | FullKeyCustomization.ActionBitField``
                :param button_setting: The key settings
                :type button_setting: ``ProfileButton.Button``
                :param **kwargs: Potential future parameters
                :type **kwargs: ``dict``
                """
                super().__init__(**kwargs)

                # Parameters initialization
                self.trigger_bitfield = trigger_bitfield
                self.action_bitfield = action_bitfield
                self.button_setting = button_setting
            # end def __init__

            @classmethod
            def fromHexList(cls, *args, **kwargs):
                """
                Parse from ``HexList`` instance

                :param args: List of arguments
                :type args: ``list``
                :param kwargs: Potential Future Parameters
                :type kwargs: ``dict``

                :return: Class instance
                :rtype: ``FkcMainTable.Group.Row``
                """
                inner_field_container_mixin = super().fromHexList(*args, **kwargs)
                inner_field_container_mixin.button_setting = ProfileButton.Button.fromHexList(
                    inner_field_container_mixin.button_setting)
                return inner_field_container_mixin
            # end def fromHexList
        # end class Row

        def __init__(self, trigger_cidx=None, rows=None, start_fkc_idx=None):
            """
            :param trigger_cidx: The CIDX of the trigger key - OPTIONAL
            :type trigger_cidx: ``int``
            :param rows: A particular trigger modifier-key combination - OPTIONAL
            :type rows: ``list[FkcMainTable.Group.Row]``
            :param start_fkc_idx: The fkc index in the first row of this group - OPTIONAL
            :type start_fkc_idx: ``int | None``
            """
            self.trigger_cidx = trigger_cidx
            self.rows = [] if rows is None else rows
            self.start_fkc_idx = start_fkc_idx  # Shall be updated while doing FkcMainTable.__hexlist__()
        # end def __init__

        def __hexlist__(self):
            """
            Convert ``FkcMainTable.Group`` to its ``HexList`` representation

            :return: ``FkcMainTable.Group`` data in ``HexList``
            :rtype: ``HexList``

            :raise ``AssertionError``: If start_fkc_idx is None
            """
            assert self.start_fkc_idx is not None
            group_hex_list = HexList(f'{Numeral(self.trigger_cidx, byteCount=1)}{Numeral(len(self.rows), byteCount=1)}')
            for index, row in enumerate(self.rows):
                group_hex_list += HexList(Numeral(self.start_fkc_idx + index, byteCount=1)) + HexList(row)
            # end for
            return group_hex_list
        # end def __hexlist__

        def init_from_hex_list(self, data):
            """
            Init ``FkcMainTable.Group`` from raw input

            :param data: The raw data of FkcMainTable Group
            :type data: ``HexList``

            :raise ``AssertionError``: If the start_fkc_idx is None or the fkc_idx is not consecutive
            """
            assert self.start_fkc_idx is not None
            self.trigger_cidx = to_int(data[0])
            num = to_int(data[1])
            start_pos = 2
            offset = self.ROW_LENGTH
            for idx in range(num):
                fkc_idx = data[start_pos]  # Ignore the fkc_idx but check it shall be consecutive
                assert self.start_fkc_idx + idx == fkc_idx, f'The fkc_idx shall be consecutive. data: {data}'
                row = self.Row.fromHexList(data[start_pos + 1: start_pos + offset])
                self.rows.append(row)
                start_pos += offset
            # end for
        # end def init_from_hex_list

        def append(self, new_rows):
            """
            Append ``FkcMainTable.Group.Row`` into the group

            :param new_rows: The list of ``FkcMainTable.Group.Row``
            :type new_rows: ``list[FkcMainTable.Group.Row]``
            """
            for row in new_rows:
                if to_int(row.trigger_bitfield) & FullKeyCustomization.TriggerBitField.SINGLE_KEY_MATCH == 0:
                    self.rows.insert(0, row)
                else:
                    # Put rows which enabled SingKeyMatch flag to the end of the row list
                    self.rows.append(row)
                # end if
            # end for
        # end def append

        def __str__(self):
            rows = ''
            for row in self.rows:
                rows += str(row) + '\n'
            # end for
            return f'TRIGGER_CIDX: {self.trigger_cidx}\nSTART_FKC_IDX: {self.start_fkc_idx}\n{rows}'
        # end def __str__

        def __repr__(self):
            return self.__str__()
        # end def __repr__
    # end class Group

    def __init__(self, groups):
        """
        :param groups: A list of FkcMainTable group
        :type groups: ``list[FkcMainTable.Group]``
        """
        self.groups = groups
        self.file_id_lsb = None
        self.first_sector_id_lsb = None
        self.crc_32 = None
    # end def __init__

    @property
    def n_bytes(self):
        """
        The number of bytes in the FKC main table

        :return: The byte count of FKC main table
        :rtype: ``int``
        """
        return len(self.__hexlist__())
    # end def n_bytes

    def is_empty(self):
        """
        Check the empty status of the FKC main table

        :return: The empty status of the FKC main table
        :rtype: ``bool``
        """
        return len(self.groups) == 0
    # end def is_empty

    def register(self, directory, file_type_id=ProfileManagement.FileTypeId.X1B05.BASE_LAYER_SETTINGS_FILE):
        """
        Register to ``DirectoryFile``

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param file_type_id: The file type id - OPTIONAL
        :type file_type_id: ``ProfileManagement.FileTypeId.X1B05 | int``
        """
        self.file_id_lsb, self.crc_32, self.first_sector_id_lsb = directory.register(
            feature_id=FullKeyCustomization.FEATURE_ID,
            file_type_id=file_type_id,
            table_object=self)
    # end def register

    def __hexlist__(self):
        """
        Convert ``FkcMainTable`` to its ``HexList`` representation

        :return: FkcMainTable data in ``HexList``
        :rtype: ``HexList``
        """
        hex_main_table = HexList(f'{Numeral(self.TABLE_ID, byteCount=1)}{Numeral(len(self.groups), byteCount=1)}')
        start_fkc_idx = 0
        for group in self.groups:
            group.start_fkc_idx = start_fkc_idx
            hex_main_table += HexList(group)
            start_fkc_idx += len(group.rows)
        # end for
        return hex_main_table
    # end def __hexlist__

    @classmethod
    def from_hex_list(cls, data):
        """
        Create ``FkcMainTable`` from raw input

        :param data: The raw data of FkcMainTable
        :type data: ``HexList``

        :return: The ``FkcMainTable`` instance
        :rtype: ``FkcMainTable``

        :raise ``AssertionError``: If the table_id is incorrect
        """
        table_id = to_int(data[0])
        fkc_group_cnt = to_int(data[1])
        assert table_id == cls.TABLE_ID
        groups = []
        start_pos = 2
        start_fkc_idx = 0
        for _ in range(fkc_group_cnt):
            num = to_int(data[start_pos + 1])
            offset = cls.Group.ROW_LENGTH * num + 2
            group = cls.Group(start_fkc_idx=start_fkc_idx)
            group.init_from_hex_list(data=data[start_pos: start_pos + offset])
            groups.append(group)
            start_pos += offset
            start_fkc_idx += num
        # end for
        return FkcMainTable(groups=groups)
    # end def from_hex_list

    def append(self, new_group):
        """
        Append a group into FkcMainTable

        Note: Recommend to append a row at a time to avoid to much failure returns.

        :param new_group: The new ``FkcMainTable.Group`` object
        :type new_group: ``FkcMainTable.Group``

        :return: Flag indicating if the new group has been added to the main table
        :rtype: ``bool``
        """
        merged = False
        for group in self.groups:
            if new_group.trigger_cidx == group.trigger_cidx:
                for row in group.rows:
                    # Check if one of the row's trigger_bitfield is a duplicate
                    if any([x.trigger_bitfield == row.trigger_bitfield for x in new_group.rows]):
                        return False
                    # end if
                # end for
                group.append(new_rows=new_group.rows)
                merged = True
                break
            # end if
        # end for

        if not merged:
            # Add this group which the CIDx is not yet registered
            self.groups.append(new_group)
        # end if

        return True
    # end def append

    def __str__(self):
        groups = ''
        for group in self.groups:
            groups += str(group) + '\n'
        # end for
        table_str = f'FkcMainTable: {self.__hexlist__()}\nCRC 32: {self.crc_32}\nFILE_ID_LSB: {self.file_id_lsb}\n' \
                    f'FIRST_SECTOR_ID_LSB: {self.first_sector_id_lsb}\n{groups}'
        return table_str
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__
# end class FkcMainTable


class RemappedKey:
    """
    FKC remapped key information class

    Usage
    1. Fixed FKC test data configuration
    2. KEY_ID container that be converted from FKC main table for key matrix emulator control and check results
    """

    @unique
    class ActionType(IntEnum):
        """
        Action Type definition class
        """
        KEYBOARD = 1
        MACRO = 2
        MOUSE = 3
        CONSUMER = 4
        FUNCTION = 5
        VIRTUAL_MODIFIER = 6
        RANDOM = 7  # Only available for preset remapped key.
        STOP_MACRO = 8
        STOP_ALL_MACRO = 9
    # end class ActionType

    @unique
    class RandomKey(IntEnum):
        """
        Random Key definition class
        Set unspecific key to trigger_key or action_key field. It will be turned into a specific KEY_ID by random key
        selection.

        Definition:
        STANDARD_KEY = NON_MODIFIER_KEY + MODIFIER_KEY
        """
        STANDARD_KEY = 1
        NON_MODIFIER_KEY = 2
        MODIFIER_KEY = 3
        ALL_REMAPPABLE_KEY = 4
        MOUSE_BUTTON = 5
        CONSUMER_KEY = 6
        RANDOM = 7  # Only available for preset remapped key.
    # end class RandomKey

    def __init__(self, layer=FkcMainTable.Layer.BASE, action_type=None, trigger_key=None, action_key=None,
                 trigger_modifier_keys=None, action_modifier_keys=None, macro_entry_index=None, state=None,
                 trigger_cidx=None, action_hid_usage=None, button_mask=None, macro_commands=None,
                 consumer_hid_usage=None, profile_number=None, fkc_idx=None):
        """
        :param layer: The layer of FKC main table - OPTIONAL
        :type layer: ``FkcMainTable.Layer``
        :param action_type: The action type of the remapped key - OPTIONAL
        :type action_type: ``RemappedKey.ActionType | int | None``
        :param trigger_key: Trigger key id - OPTIONAL
        :type trigger_key: ``KEY_ID | RemappedKey.RandomKey | None``
        :param action_key: Action key id - OPTIONAL
        :type action_key: ``KEY_ID | RemappedKey.RandomKey | None``
        :param trigger_modifier_keys: Trigger modifier key id list - OPTIONAL
        :type trigger_modifier_keys: ``list[KEY_ID | RemappedKey.RandomKey] | None``
        :param action_modifier_keys: Action modifier key id list - OPTIONAL
        :type action_modifier_keys: ``list[KEY_ID | RemappedKey.RandomKey] | None``
        :param macro_entry_index: The index of macro entry - OPTIONAL
        :type macro_entry_index: ``int | None``
        :param state: MAKE or BREAK state (for key press and check) - OPTIONAL
        :type state: ``str | None``
        :param trigger_cidx: Trigger Cid index (for debugging) - OPTIONAL
        :type trigger_cidx: ``int | None``
        :param action_hid_usage: Action Kbd HID Usage (for debugging) - OPTIONAL
        :type action_hid_usage: ``int | None``
        :param button_mask: Mouse button mask (for debugging) - OPTIONAL
        :type button_mask: ``ProfileButton.ButtonMask | int | None``
        :param macro_commands: The Macro commands list that be used for HID report validation - OPTIONAL
        :type macro_commands: ``StandardKeyCommand | MouseButtonCommand | ConsumerKeyCommand | XYMovementCommand |
                                RollerCommand | AcPanCommand | None``
        :param consumer_hid_usage: Consumer HID Usage - OPTIONAL
        :type consumer_hid_usage: ``ConsumerHidUsage | int | None``
        :param profile_number: Profile number be used in Function ENABLED_PROFILE_SPECIFIC_NUMBER - OPTIONAL
        :type profile_number: ``int | None``
        :param fkc_idx: FKC remapping index in the FKC main table - OPTIONAL
        :type fkc_idx: ``int | None``

        :raise ``AssertionError``: If required input is None
        """
        self.layer = layer
        self.action_type = action_type
        self.trigger_key = trigger_key
        self.trigger_modifier_keys = trigger_modifier_keys if trigger_modifier_keys else []
        self.action_modifier_keys = action_modifier_keys if action_modifier_keys else []
        self.action_key = action_key
        self.macro_entry_index = macro_entry_index
        self.profile_number = profile_number

        # Check availability
        if action_type:
            if action_type not in [self.ActionType.MACRO, self.ActionType.STOP_MACRO, self.ActionType.STOP_ALL_MACRO]:
                if action_type == self.ActionType.FUNCTION and \
                        action_key == ProfileButton.FunctionExecution.SWITCH_TO_SPECIFIC_PROFILE:
                    assert profile_number is not None
                # end if
            else:
                assert macro_entry_index is not None
            # end if
        # end if

        # MAKE or BREAK for button control
        self.state = state

        # Information for validation or debugging
        self.trigger_cidx = trigger_cidx
        self.action_hid_usage = action_hid_usage
        self.button_mask = button_mask
        self.macro_commands = macro_commands
        self.consumer_hid_usage = consumer_hid_usage
        self.fkc_idx = fkc_idx
    # end def __init__

    @classmethod
    def get_action_type(cls, button_settings):
        """
        Get the ``RemappedKey.ActionType``

        :param button_settings: Settings of ProfileButton.Button
        :type button_settings: ``ProfileButton.Button``

        :return: The action type of the remapped key
        :rtype: ``RemappedKey.ActionType``

        :raise ``ValueError``: If the opcode in button_settings is unknown
        """
        opcode_msb = to_int(button_settings.param_1)
        opcode_lsb = to_int(button_settings.param_2)
        if opcode_msb == FkcProfileButton.Category.EXECUTE_MACRO:
            action_type = cls.ActionType.MACRO
        elif opcode_msb == FkcProfileButton.Category.STOP_MACRO:
            action_type = cls.ActionType.STOP_MACRO
        elif opcode_msb == FkcProfileButton.Category.STOP_ALL_MACRO:
            action_type = cls.ActionType.STOP_ALL_MACRO
        elif opcode_msb == FkcProfileButton.Category.BUTTON_REMAPPING:
            if opcode_lsb in [FkcProfileButton.ButtonRemapping.BUTTON_NOT_SENT,
                              FkcProfileButton.ButtonRemapping.STANDARD_KEY]:
                action_type = cls.ActionType.KEYBOARD
            elif opcode_lsb == FkcProfileButton.ButtonRemapping.GENERIC_MOUSE_BUTTON:
                action_type = cls.ActionType.MOUSE
            elif opcode_lsb == FkcProfileButton.ButtonRemapping.CONSUMER_KEY:
                action_type = cls.ActionType.CONSUMER
            elif opcode_lsb == FkcProfileButton.ButtonRemapping.VIRTUAL_MODIFIER:
                action_type = cls.ActionType.VIRTUAL_MODIFIER
            else:
                raise ValueError(f'Unknown opcode: MSB={button_settings.param_1}, LSB={button_settings.param_2}')
            # end if
        elif opcode_msb == FkcProfileButton.Category.FUNCTION_EXECUTION:
            action_type = cls.ActionType.FUNCTION
        else:
            raise ValueError(f'Unknown opcode: MSB={button_settings.param_1}, LSB={button_settings.param_2}')
        # end if
        return action_type
    # end def get_action_type

    @staticmethod
    def sort(preset_remapped_keys):
        """
        Sort preset remapped keys as normal remapped keys + random remapped keys

        :param preset_remapped_keys: The preset remapped keys
        :type preset_remapped_keys: ``list[RemappedKey]``

        :return: The sorted remapped keys
        :rtype: ``list[RemappedKey]``
        """
        normal_keys = []
        random_keys = []
        for remapped_key in preset_remapped_keys:
            if remapped_key.trigger_key in [RemappedKey.RandomKey.NON_MODIFIER_KEY,
                                            RemappedKey.RandomKey.MODIFIER_KEY,
                                            RemappedKey.RandomKey.STANDARD_KEY,
                                            RemappedKey.RandomKey.MOUSE_BUTTON,
                                            RemappedKey.RandomKey.CONSUMER_KEY]:
                random_keys.append(remapped_key)
            else:
                normal_keys.append(remapped_key)
            # end if
        # end for
        return normal_keys + random_keys
    # end def sort

    def __str__(self):
        message = f'<RemappedKey> {self.layer!r}, {self.action_type!r}, ' \
                  f'Trigger Keys: {self.trigger_modifier_keys + [self.trigger_key]} ' \
                  f'(Trigger Cidx: {self.trigger_cidx}), FKC Index: {self.fkc_idx}, '
        if self.action_type == self.ActionType.KEYBOARD:
            return message + f'Action Keys: {self.action_modifier_keys + [self.action_key]} ' \
                             f'(Kdb HID Usage: 0x{self.action_hid_usage})\n'
        elif self.action_type == self.ActionType.MACRO:
            return message + f'Action Modifier Keys: {self.action_modifier_keys}, ' \
                             f'Macro Entry Index: {self.macro_entry_index}, Macro commands: {self.macro_commands}\n'
        elif self.action_type == self.ActionType.MOUSE:
            return message + f'Action Modifier Keys: {self.action_modifier_keys}, Mouse Button: {self.action_key!r} ' \
                             f'(Button Mask: {self.button_mask!r})\n'
        elif self.action_type == self.ActionType.CONSUMER:
            return message + f'Action Modifier Keys: {self.action_modifier_keys}, Consumer Key: {self.action_key!r} ' \
                             f'(Consumer HID Usage: {hex(self.consumer_hid_usage)})\n'
        elif self.action_type == self.ActionType.FUNCTION:
            if self.action_key == KEY_ID.SWITCH_TO_SPECIFIC_ONBOARD_PROFILE:
                return message + f'Action Modifier Keys: {self.action_modifier_keys}, ' \
                                 f'Function Key: {self.action_key!r}, Profile Number: {self.profile_number}\n'
            else:
                return message + \
                       f'Action Modifier Keys: {self.action_modifier_keys}, Function Key: {self.action_key!r}\n'
            # end if
        elif self.action_type in [self.ActionType.VIRTUAL_MODIFIER,
                                  self.ActionType.STOP_MACRO,
                                  self.ActionType.STOP_ALL_MACRO]:
            return message + f'Action Keys: {self.action_modifier_keys + [self.action_key]}\n'
        else:
            raise ValueError(f'Unsupported action type: {self.action_type!r}')
        # end if
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__
# end class RemappedKey


class DirectoryFile:
    """
    0x8101 Directory File definition

    https://docs.google.com/spreadsheets/d/1Py5a5bWBmDEK2voFczI4x0L5_dkbT9EGM-jmkCCJTao/view#gid=1017032508&range=B195

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Hash                          32
    nFiles                        8
    File[n]                       10 x n
    ============================  ==========
    """

    NO_FILE = 0xFF
    FILE_LENGTH = 10
    HEADER_LENGTH = 5
    EOF_LENGTH = 1

    class File(BitFieldContainerMixin):
        """
        The file entry in 0x8101 directory

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        FileIdLsb                     8
        FeatureId                     16
        FileTypeId                    2
        nBytes                        14
        Crc32                         32
        FirstSectorIdLsb              8
        ============================  ==========
        """

        class FID:
            """
            Field Identifiers
            """
            FILE_ID_LSB = 0xFF
            FEATURE_ID = FILE_ID_LSB - 1
            FILE_TYPE_ID = FEATURE_ID - 1
            N_BYTES = FILE_TYPE_ID - 1
            CRC_32 = N_BYTES - 1
            FIRST_SECTOR_ID_LSB = CRC_32 - 1
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            FILE_ID_LSB = 0x08
            FEATURE_ID = 0x10
            FILE_TYPE_ID = 0x02
            N_BYTES = 0x0E
            CRC_32 = 0x20
            FIRST_SECTOR_ID_LSB = 0x08
        # end class LEN

        FIELDS = (
            BitField(
                fid=FID.FILE_ID_LSB,
                length=LEN.FILE_ID_LSB,
                title='FileId LSB',
                name='file_id_lsb',
                checks=(CheckHexList(LEN.FILE_ID_LSB // 8), CheckByte(),), ),
            BitField(
                fid=FID.FEATURE_ID,
                length=LEN.FEATURE_ID,
                title='FeatureId',
                name='feature_id',
                checks=(CheckHexList(LEN.FEATURE_ID // 8), CheckInt(),), ),
            BitField(
                fid=FID.FILE_TYPE_ID,
                length=LEN.FILE_TYPE_ID,
                title='FileTypeId',
                name='file_type_id',
                checks=(CheckHexList(LEN.FILE_TYPE_ID // 8), CheckByte(),), ),
            BitField(
                fid=FID.N_BYTES,
                length=LEN.N_BYTES,
                title='nBytes',
                name='n_bytes',
                checks=(CheckHexList(LEN.N_BYTES // 8), CheckInt(),), ),
            BitField(
                fid=FID.CRC_32,
                length=LEN.CRC_32,
                title='Crc32',
                name='crc_32',
                checks=(CheckHexList(LEN.CRC_32 // 8), CheckInt(),), ),
            BitField(
                fid=FID.FIRST_SECTOR_ID_LSB,
                length=LEN.FIRST_SECTOR_ID_LSB,
                title='FirstSectorId LSB',
                name='first_sector_id_lsb',
                checks=(CheckHexList(LEN.FIRST_SECTOR_ID_LSB // 8), CheckByte(),), ),
        )
    # end class File

    class IDManager:
        """
        ID Manager class definition
        """

        def __init__(self, max_directory_sector_id, max_sector_id, sector_size, max_file_id):
            """
            :param max_directory_sector_id: The maximum usable sector_id for the directory.
            :type max_directory_sector_id: ``int``
            :param max_sector_id: The maximum usable sector_id (considering just LSB part).
            :type max_sector_id: ``init``
            :param sector_size: The maximum amount of data that can be written to a sector, in bytes.
            :type sector_size: ``init``
            :param max_file_id: The maximum usable file_id (considering just LSB part).
            :type max_file_id: ``int``
            """
            self.max_directory_sector_id = max_directory_sector_id
            self.next_sector_id = max_directory_sector_id + 1
            self.max_sector_id = max_sector_id
            self.sector_size = sector_size
            self.next_file_id = 1
            self.max_file_id = max_file_id
        # end def __init__

        def reset_sector_id(self):
            """
            Reset sector_id to initial value
            """
            self.next_sector_id = self.max_directory_sector_id + 1
        # end def reset_sector_id

        def get_next_file_id_lsb(self):
            """
            Get an unused file id LSB

            :return: The unused file id
            :rtype: ``int``
            """
            file_id = self.next_file_id
            self.next_file_id += 1
            if file_id > self.max_file_id:
                warn(f'The file_id: {file_id} > max file id: {self.max_file_id}')
            # end if
            return file_id
        # end def get_next_file_id_lsb

        def set_next_sector_id_lsb(self, byte_count):
            """
            Update the unused sector id LSB

            :param byte_count: The number of bytes to be saved in NVS
            :type byte_count: ``int``
            """
            sectors = max(ceil(byte_count / self.sector_size), 1)
            self.next_sector_id += sectors
            if self.next_sector_id > self.max_sector_id:
                warn(f'The next sector id: {self.next_sector_id} > max sector id: {self.max_sector_id}')
            # end if
        # end def set_next_sector_id_lsb

        def get_next_sector_id_lsb(self):
            """
            Get the unused sector id LSB

            :return: Unused sector id
            :rtype: ``int``
            """
            return self.next_sector_id
        # end def get_next_sector_id_lsb
    # end class IDManager

    def __init__(self, files=None, crc_32=None):
        """
        :param files: The file list in the ``DirectoryFile`` - OPTIONAL
        :type files: ``dict[int, DirectoryFile.File] | None``
        :param crc_32: The hash value of the ``DirectoryFile`` - OPTIONAL
        :type crc_32: ``HexList | None``
        """
        self.files = {} if files is None else files
        self.first_sector_id_lsb = 0x0000
        self.crc_32 = crc_32
        self.id_manager = None
        self.registered_tables = {}
    # end def __init__

    def init_id_manager(self, max_directory_sector_id, max_sector_id, sector_size, max_file_id):
        """
        Init ID Manager

        Note: Shall do init_id_manager() before doing register()

        :param max_directory_sector_id: The maximum usable sector_id for the directory.
        :type max_directory_sector_id: ``int``
        :param max_sector_id: The maximum usable sector_id (considering just LSB part).
        :type max_sector_id: ``init``
        :param sector_size: The maximum amount of data that can be written to a sector, in bytes.
        :type sector_size: ``init``
        :param max_file_id: The maximum usable file_id (considering just LSB part).
        :type max_file_id: ``int``
        """
        self.id_manager = self.IDManager(max_directory_sector_id=max_directory_sector_id,
                                         max_sector_id=max_sector_id, sector_size=sector_size, max_file_id=max_file_id)
    # end def init_id_manager

    def register(self, feature_id, file_type_id, table_object):
        """
        Register file in Directory File

        :param feature_id: The HID++ feature id
        :type feature_id: ``int``
        :param file_type_id: The file type id
        :type file_type_id: ``ProfileManagement.FileTypeId.X8101 | ProfileManagement.FileTypeId.X1B05 | int``
        :param table_object: The data be used to calculate crc32
        :type table_object: ``Macro | FkcMainTable | Profile``

        :return: Resource assignment information after registration
        :rtype: ``tuple(int, int, int)``

        :raise ``AssertionError``: If the ID manager is not initialized yet.
        """
        assert isinstance(self.id_manager, self.IDManager), 'Shall do init_id_manager() first!'
        file_id_lsb = self.id_manager.get_next_file_id_lsb()
        n_bytes = len(HexList(table_object))
        crc_32 = self.calculate_crc32(data=HexList(table_object))
        first_sector_id_lsb = self.id_manager.get_next_sector_id_lsb()
        file = self.File(file_id_lsb=file_id_lsb,
                         feature_id=feature_id,
                         file_type_id=file_type_id,
                         n_bytes=n_bytes,
                         crc_32=crc_32,
                         first_sector_id_lsb=first_sector_id_lsb)
        self.id_manager.set_next_sector_id_lsb(byte_count=n_bytes)
        self.files[file_id_lsb] = file

        # Update directory crc32
        self.crc_32 = self.calculate_crc32(data=self._get_hexlist_for_crc32_calculation())

        # Stored table_object
        self.registered_tables[file_id_lsb] = table_object
        return file_id_lsb, crc_32, first_sector_id_lsb
    # end def register

    def update_file(self, file_id_lsb, table_in_hexlist):
        """
        Update file

        :param file_id_lsb: The file ID to use as the source of the data.
        :type file_id_lsb: ``int``
        :param table_in_hexlist: The data be used to calculate crc32
        :type table_in_hexlist: ``HexList``

        :return: The crc32 value of the file (table_in_hexlist)
        :rtype: ``HexList``
        """
        # Update crc32 for directory file
        crc_32 = self.calculate_crc32(data=table_in_hexlist)
        self.files[file_id_lsb].crc_32 = crc_32
        self.files[file_id_lsb].n_bytes = len(table_in_hexlist)
        self.rearrange_sector_id()
        # Update directory crc32
        self.crc_32 = self.calculate_crc32(data=self._get_hexlist_for_crc32_calculation())
        return crc_32
    # end def update_file

    def rearrange_sector_id(self):
        """
        Re-arrange sector id
        """
        self.id_manager.reset_sector_id()
        for file_id_lsb in self.files:
            first_sector_id_lsb = self.id_manager.get_next_sector_id_lsb()
            self.files[file_id_lsb].first_sector_id_lsb = first_sector_id_lsb
            self.id_manager.set_next_sector_id_lsb(byte_count=self.files[file_id_lsb].n_bytes)
            # Update to registered table
            self.registered_tables[file_id_lsb].first_sector_id_lsb = first_sector_id_lsb
        # end for
    # end def rearrange_sector_id

    def _get_hexlist_for_crc32_calculation(self):
        """
        Get the ``DirectoryFile`` hex list for CRC32 calculation

        Note: Calculate CRC 32: it is computed over bytes 4:N-1 where N is the length of the directory file.
        cf: https://docs.google.com/spreadsheets/d/1Py5a5bWBmDEK2voFczI4x0L5_dkbT9EGM-jmkCCJTao/view#gid=1017032508&range=B165

        :return: DirectoryFile data in ``HexList``
        :rtype: ``HexList``
        """
        # Header Fields
        hex_directory = HexList()
        hex_directory += HexList(len(self.files))
        # File Entry Fields
        for file_id_lsb in self.files:
            hex_directory += HexList(self.files[file_id_lsb])
        # end for
        return hex_directory + HexList(self.NO_FILE)
    # end def _get_hexlist_for_crc32_calculation

    def __hexlist__(self):
        """
        Convert ``DirectoryFile`` to its ``HexList`` representation

        :return: DirectoryFile data in ``HexList``
        :rtype: ``HexList``
        """
        return self.crc_32 + self._get_hexlist_for_crc32_calculation()
    # end def __hexlist__

    @classmethod
    def fromHexList(cls, data):
        """
        Initialize ``DirectoryFile`` from the raw hex list

        :param data: The hex list of 0x8101 Profile Directory
        :type data: ``HexList``

        :return: The 0x8101 ``DirectoryFile`` object
        :rtype: ``DirectoryFile``
        """
        crc_32 = data[0:4]
        nb_files = data[4]
        start_pos = 5
        files = {}
        for _ in range(nb_files):
            file = cls.File.fromHexList(data[start_pos: start_pos + cls.FILE_LENGTH])
            files[to_int(file.file_id_lsb)] = file
            start_pos += cls.FILE_LENGTH
        # end for
        return DirectoryFile(files=files, crc_32=crc_32)
    # end def fromHexList

    @classmethod
    def calculate_crc32(cls, data):
        """
        Calculate CRC32 for input data

        :param data: Data
        :type data: ``HexList``

        :return: The CRC32 result of input data
        :rtype: ``HexList``
        """
        return HexList(Numeral(crc32(a2b_hex(str(data))), byteCount=4))
    # end def calculate_crc32

    def __str__(self):
        files = ''
        for file_id in self.files:
            files += str(self.files[file_id]) + '\n'
        # end for
        return f'DirectoryFile: {self.__hexlist__()}\nCRC_32: {self.crc_32}\n' \
               f'ID_Manager.Next_FILE_ID: {self.id_manager.next_file_id}\n' \
               f'ID_Manager.Next_SECTOR_ID: {self.id_manager.next_sector_id}\n{files}'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__
# end class DirectoryFile


class TagField_1_Byte(BitFieldContainerMixin):
    """
    0x8101 Tag with 1 byte data length
    """

    class FID:
        """
        Field Identifiers
        """
        DATA = 0xFF
    # end class FID

    class LEN:
        """
        Field Lengths in bits
        """
        DATA = 0x08
    # end class LEN

    FIELDS = (
        BitField(
            fid=FID.DATA,
            length=LEN.DATA,
            title='Data',
            name='data',
            checks=(CheckHexList(LEN.DATA // 8), CheckByte(),), ),
    )
# end class TagField_1_Byte


class TagField_2_Bytes(TagField_1_Byte):
    """
    0x8101 Tag with 2 bytes data length
    """

    class LEN(TagField_1_Byte.LEN):
        # See ``TagSize_1B.LEN``
        DATA = 0x10
    # end class LEN

    FIELDS = (
        BitField(
            fid=TagField_1_Byte.FID.DATA,
            length=LEN.DATA,
            title='Data',
            name='data',
            checks=(CheckHexList(LEN.DATA // 8), CheckInt(),), ),
    )
# end class TagField_2_Bytes


class TagField_11_Bytes(TagField_1_Byte):
    """
    0x8101 Tag with 11 bytes data length
    """

    class LEN(TagField_1_Byte.LEN):
        # See ``TagSize_1B.LEN``
        DATA = 0x58
    # end class LEN

    FIELDS = (
        BitField(
            fid=TagField_1_Byte.FID.DATA,
            length=LEN.DATA,
            title='Data',
            name='data',
            checks=(CheckHexList(LEN.DATA // 8), CheckInt(),), ),
    )
# end class TagField_11_Bytes


class TagField_16_Bytes(TagField_1_Byte):
    """
    0x8101 Tag with 16 bytes data length
    """

    class LEN(TagField_1_Byte.LEN):
        # See ``TagSize_1B.LEN``
        DATA = 0x80
    # end class LEN

    FIELDS = (
        BitField(
            fid=TagField_1_Byte.FID.DATA,
            length=LEN.DATA,
            title='Data',
            name='data',
            checks=(CheckHexList(LEN.DATA // 8), CheckInt(),), ),
    )
# end class TagField_16_Bytes


class TagField_24_Bytes(TagField_1_Byte):
    """
    0x8101 Tag with 24 bytes data length
    """

    class LEN(TagField_1_Byte.LEN):
        # See ``TagSize_1B.LEN``
        DATA = 0xC0
    # end class LEN

    FIELDS = (
        BitField(
            fid=TagField_1_Byte.FID.DATA,
            length=LEN.DATA,
            title='Data',
            name='data',
            checks=(CheckHexList(LEN.DATA // 8), CheckInt(),), ),
    )
# end class TagField_24_Bytes


class TagInfo:
    """
    Information class of 0x8101 Tag
    """

    def __init__(self, byte_count, class_type, name_in_settings=''):
        """
        :param byte_count: Byte count
        :type byte_count: ``int``
        :param class_type: Class types, ``TagField_1_Byte``, ``TagField_2_Byte`` and so on....
        :type class_type: ``type``
        :param name_in_settings: Name be defined in PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.OOB_PROFILES - OPTIONAL
        :type name_in_settings: ``str``
        """
        self.byte_count = byte_count
        self.class_type = class_type
        self.name_in_settings = name_in_settings
    # end def __init__
# end class TagInfo


PROFILE_TAG_INFO_MAP = {
    ProfileManagement.Tag.PROFILE_IDENTIFIER:
        TagInfo(byte_count=1, class_type=TagField_1_Byte, name_in_settings='ProfileIdentifier'),
    ProfileManagement.Tag.PROFILE_VERSION:
        TagInfo(byte_count=1, class_type=TagField_1_Byte, name_in_settings='ProfileVersion'),
    ProfileManagement.Tag.PROFILE_NAME:
        TagInfo(byte_count=24, class_type=TagField_24_Bytes, name_in_settings='ProfileName'),
    ProfileManagement.Tag.LIGHTING_FLAG:
        TagInfo(byte_count=1, class_type=TagField_1_Byte, name_in_settings='LightningFlag'),
    ProfileManagement.Tag.ACTIVE_CLUSTER_0_EFFECT:
        TagInfo(byte_count=11, class_type=TagField_11_Bytes, name_in_settings='ActiveCluster0Effect'),
    ProfileManagement.Tag.ACTIVE_CLUSTER_1_EFFECT:
        TagInfo(byte_count=11, class_type=TagField_11_Bytes, name_in_settings='ActiveCluster1Effect'),
    ProfileManagement.Tag.PASSIVE_CLUSTER_0_EFFECT:
        TagInfo(byte_count=11, class_type=TagField_11_Bytes, name_in_settings='PassiveCluster0Effect'),
    ProfileManagement.Tag.PASSIVE_CLUSTER_1_EFFECT:
        TagInfo(byte_count=11, class_type=TagField_11_Bytes, name_in_settings='PassiveCluster1Effect'),
    ProfileManagement.Tag.PS_TIMEOUT:
        TagInfo(byte_count=2, class_type=TagField_2_Bytes, name_in_settings='PSTimeout'),
    ProfileManagement.Tag.PO_TIMEOUT:
        TagInfo(byte_count=2, class_type=TagField_2_Bytes, name_in_settings='POTimeout'),
    ProfileManagement.Tag.X4523_CIDX_BITMAP:
        TagInfo(byte_count=16, class_type=TagField_16_Bytes, name_in_settings='X4523CidxBitmap'),
    ProfileManagement.Tag.ANALOG_GENERIC_SETTING:
        TagInfo(byte_count=2, class_type=TagField_2_Bytes, name_in_settings='AnalogGenericSetting'),
    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO: TagInfo(byte_count=2, class_type=TagField_2_Bytes),
    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE: TagInfo(byte_count=2, class_type=TagField_2_Bytes),
    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_FN: TagInfo(byte_count=2, class_type=TagField_2_Bytes),
    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_GSHIFT: TagInfo(byte_count=2, class_type=TagField_2_Bytes),
    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_ACTUATION: TagInfo(byte_count=2, class_type=TagField_2_Bytes),
    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER: TagInfo(byte_count=2, class_type=TagField_2_Bytes),
    ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_MULTI_ACTION: TagInfo(byte_count=2, class_type=TagField_2_Bytes),
}


class Profile:
    """
    0x8101 Profile definition

    https://docs.google.com/spreadsheets/d/1Py5a5bWBmDEK2voFczI4x0L5_dkbT9EGM-jmkCCJTao/view#gid=1072722811&range=A1
    """

    def __init__(self, tag_fields):
        """
        :param tag_fields: The dictionary of tag with its field
        :type tag_fields: ``dict[ProfileManagement.Tag, int | HexList]``
        """
        self.tag_fields = tag_fields
        self.file_id_lsb = None
        self.first_sector_id_lsb = None
        self.crc_32 = None
    # end def __init__

    def register(self, directory, file_type_id=ProfileManagement.FileTypeId.X8101.ONBOARD_MODE_PROFILE):
        """
        Register to ``DirectoryFile``

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param file_type_id: The file type id - OPTIONAL
        :type file_type_id: ``ProfileManagement.FileTypeId.X8101 | int``
        """
        self.file_id_lsb, self.crc_32, self.first_sector_id_lsb = directory.register(
            feature_id=ProfileManagement.FEATURE_ID,
            file_type_id=file_type_id,
            table_object=self)
    # end def register

    def update_tag_content(self, directory, tag_content_dict):
        """
        Update content for specific tags

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param tag_content_dict: The dictionary of ``ProfileManagement.Tag`` with its content
        :type tag_content_dict: ``dict[ProfileManagement.Tag, int | HexList]``
        """
        for tag in tag_content_dict:
            # noinspection PyUnresolvedReferences
            self.tag_fields[tag].setValue(
                fid=TagField_1_Byte.FID.DATA,
                value=HexList(Numeral(tag_content_dict[tag], byteCount=PROFILE_TAG_INFO_MAP[tag].byte_count)))
        # end for

        # Update CRC 32 hash code
        self.crc_32 = directory.update_file(file_id_lsb=self.file_id_lsb, table_in_hexlist=self.__hexlist__())
    # end def update_tag_content

    def __hexlist__(self):
        """
        Transform ``Profile`` to ``HexList``

        :return: Profile data in ``HexList``
        :rtype: ``HexList``
        """
        hex_profile = HexList()
        for tag in self.tag_fields:
            hex_profile += HexList(self.tag_fields[tag])
        # end for
        return hex_profile + HexList(ProfileManagement.Tag.EOF)
    # end def __hexlist__

    @classmethod
    def from_hex_list(cls, tag_list, data):
        """
        Initialize ``Profile`` from the raw hex list

        :param tag_list: Tag list
        :type tag_list: ``list[ProfileManagement.Tag]``
        :param data: The hex list of 0x8101 Profile
        :type data: ``HexList``

        :return: The ``Profile`` object
        :rtype: ``Profile``
        """
        tag_fields = {}
        start_pos = 0
        for tag in tag_list:
            if tag == ProfileManagement.Tag.EOF:
                break
            # end if
            tag_info = PROFILE_TAG_INFO_MAP[tag]
            # noinspection PyUnresolvedReferences
            tag_field = tag_info.class_type.fromHexList(data[start_pos: start_pos + tag_info.byte_count])
            tag_fields[tag] = tag_field
            start_pos += tag_info.byte_count
        # end for
        return Profile(tag_fields=tag_fields)
    # end def from_hex_list

    def __str__(self):
        tag_fields = ''
        for tag in self.tag_fields:
            # noinspection PyUnresolvedReferences
            tag_fields += f'{tag!r}: {self.tag_fields[tag].data}' + '\n'
        # end for
        return f'Profile: {self.__hexlist__()}\nCRC 32: {self.crc_32}\nFILE_ID_LSB: {self.file_id_lsb}\n' \
               f'FIRST_SECTOR_ID_LSB: {self.first_sector_id_lsb}\n{tag_fields}'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__
# end class Profile


class OobProfile(Profile):
    """
    0x8101 OOB Profile definition class

    https://drive.google.com/file/d/1qMP9MPajJe6xLZHHZtM4AG5uiVC2of7y/view
    """

    def __init__(self, tag_fields):
        """
        :param tag_fields: The dictionary of tag with its field
        :type tag_fields: ``dict[ProfileManagement.Tag, int]``
        """
        super().__init__(tag_fields=tag_fields)
    # end def __init__

    def __hexlist__(self):
        """
        Transform ``OobProfile`` to ``HexList``

        :return: OobProfile data in ``HexList``
        :rtype: ``HexList``
        """
        hex_profile = HexList()
        for tag in self.tag_fields:
            hex_profile += HexList(self.tag_fields[tag])
        # end for
        return hex_profile + HexList(ProfileManagement.Tag.EOF)
    # end def __hexlist__

    @classmethod
    def from_hex_list(cls, tag_list, data):
        """
        Initialize ``OobProfile`` from the raw hex list

        :param tag_list: Tag list
        :type tag_list: ``list[ProfileManagement.Tag]``
        :param data: The hex list of 0x8101 OOB Profile
        :type data: ``HexList``

        :return: The ``OobProfile`` object
        :rtype: ``OobProfile``
        """
        tag_fields = {}
        start_pos = 0
        for tag in tag_list:
            if tag == ProfileManagement.Tag.EOF:
                break
            elif tag in [ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_BASE,
                         ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_MACRO,
                         ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_FN,
                         ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B05_GSHIFT,
                         ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_ACTUATION,
                         ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER,
                         ProfileManagement.Tag.FEATURE_SETTINGS_FILE_1B08_MULTI_ACTION]:
                # Ignore feature setting in Oob profile
                continue
            # end if
            tag_info = PROFILE_TAG_INFO_MAP[tag]
            # noinspection PyUnresolvedReferences
            tag_field = tag_info.class_type.fromHexList(data[start_pos: start_pos + tag_info.byte_count])
            tag_fields[tag] = tag_field
            start_pos += tag_info.byte_count
        # end for

        return OobProfile(tag_fields=tag_fields)
    # end def from_hex_list
# end class OobProfile


class Macro(ProfileMacro):
    """
    0x8101 Macro definition class
    """

    class Entry:
        """
        Macro entry definition class
        """

        def __init__(self, commands, start_address):
            """
            :param commands: Macro command list
            :type commands: ``list[MacroCommand_0 | MacroCommand_1 | MacroCommand_2 | MacroCommand_4]``
            :param start_address: Start address in a macro
            :type start_address: ``int``
            """
            self.commands = commands
            self.start_address = start_address
        # end def __init__

        def __hexlist__(self):
            """
            Transform ``Entry`` to ``HexList``

            :return: Macro data in ``HexList``
            :rtype: ``HexList``
            """
            hex_commands = HexList()
            for command in self.commands:
                hex_commands += HexList(command)
            # end for
            return hex_commands
        # end def __hexlist__

        def __str__(self):
            commands = ''
            for command in self.commands:
                commands += f'{command}\n'
            # end for
            return f'Start_Address: {hex(self.start_address)}\n{commands}'
        # end def __str__

        def __repr__(self):
            return self.__str__()
        # end def __repr__
    # end class Entry

    def __init__(self, entries):
        """
        :param entries: Macro Entry list
        :type entries: ``list[Macro.Entry]``
        """
        self.entries = entries
        self.file_id_lsb = None
        self.first_sector_id_lsb = None
        self.crc_32 = None
    # end def __init__

    def register(self, directory):
        """
        Register to ``DirectoryFile``

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        """
        self.file_id_lsb, self.crc_32, self.first_sector_id_lsb = directory.register(
            feature_id=FullKeyCustomization.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B05.MACRO_DEFINITION_FILE,
            table_object=self)
    # end def register

    def append(self, directory, entries):
        """
        Append entries

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param entries: The macro entries
        :type entries: ``list[Macro.Entry]``
        """
        self.entries += entries
        self.crc_32 = directory.update_file(file_id_lsb=self.file_id_lsb, table_in_hexlist=self.__hexlist__())
    # end def append

    @property
    def n_bytes(self):
        """
        The number of bytes in the Macro

        :return: The byte count of Macro
        :rtype: ``int``
        """
        return len(self.__hexlist__())
    # end def n_bytes

    def __hexlist__(self):
        """
        Transform ``Macro`` to ``HexList``

        :return: Macro data in ``HexList``
        :rtype: ``HexList``
        """
        hex_entries = HexList()
        for entry in self.entries:
            hex_entries += HexList(entry)
        # end for
        return hex_entries
    # end def __hexlist__

    @classmethod
    def from_hex_list(cls, data):
        """
        Initialize ``Macro`` from the raw hex list

        :param data: The hex list of 0x8101 Macro
        :type data: ``HexList``

        :return: The ``Macro`` object
        :rtype: ``Macro``
        """
        entries = []
        commands = []

        start_address = 0
        offset = 0
        while offset < len(data):
            op_code = data[offset]
            command, param_count = ProfileMacro.get_data_class(op_code=op_code)
            if param_count >= 1:
                offset += 1
                command.p1 = data[offset]
            # end if
            if param_count >= 2:
                offset += 1
                command.p2 = data[offset]
            # end if
            if param_count == 4:
                offset += 1
                command.p3 = data[offset]
                offset += 1
                command.p4 = data[offset]
            # end if
            commands.append(command)

            offset += 1
            if op_code in [ProfileMacro.Opcode.MACRO_END, ProfileMacro.Opcode.WAIT_FOR_RELEASE,
                           ProfileMacro.Opcode.REPEAT_WHILE_PRESSED, ProfileMacro.Opcode.REPEAT_UNTIL_CANCEL]:
                # The end command
                entries.append(cls.Entry(commands=commands, start_address=start_address))
                commands = []
                start_address = offset
            # end if
        # end while
        return Macro(entries=entries)
    # end def from_hex_list

    @classmethod
    def convert_to_macro_commands(cls, macro, first_sector_id_lsb, start_address, os_variant):
        """
        Convert Macro entry to Preset Macro command list

        :param macro: Macro object
        :type macro: ``Macro``
        :param first_sector_id_lsb: The first sector id
        :type first_sector_id_lsb: ``int``
        :param start_address: The start address of Macro.Entry
        :type start_address: ``int``
        :param os_variant: OS variant
        :type os_variant: ``OS | str``

        :return: The preset macro command list
        :rtype: ``tuple[int, list[StandardKeyCommand | MouseButtonCommand | ConsumerKeyCommand | XYMovementCommand |
                                  RollerCommand | AcPanCommand]]``

        :raise ``AssertionError``: If the first_sector_id_lsb is not matched
        """
        assert macro.first_sector_id_lsb == first_sector_id_lsb
        command_list = []
        entry_index = None
        for index, entry in enumerate(macro.entries):
            if entry.start_address == start_address:
                for command in entry.commands:
                    op_code = to_int(command.op_code)
                    if op_code == ProfileMacro.Opcode.KEY_DOWN:
                        key_command = StandardKeyCommand(
                            key_id=KEYBOARD_HID_USAGE_TO_KEY_ID_MAP[to_int(command.p2)],
                            action=KeyAction.PRESS)
                        command_list.append(key_command)
                    elif op_code == ProfileMacro.Opcode.KEY_UP:
                        key_command = StandardKeyCommand(
                            key_id=KEYBOARD_HID_USAGE_TO_KEY_ID_MAP[to_int(command.p2)],
                            action=KeyAction.RELEASE)
                        command_list.append(key_command)
                    elif op_code == ProfileMacro.Opcode.BUTTON_DOWN:
                        button_mask = to_int(command.p1) << 8 | to_int(command.p2)
                        button_command = MouseButtonCommand(
                            key_id=ProfileButton.convert_button_mask_to_key_id(button_mask=button_mask),
                            action=KeyAction.PRESS)
                        command_list.append(button_command)
                    elif op_code == ProfileMacro.Opcode.BUTTON_UP:
                        button_mask = to_int(command.p1) << 8 | to_int(command.p2)
                        button_command = MouseButtonCommand(
                            key_id=ProfileButton.convert_button_mask_to_key_id(button_mask=button_mask),
                            action=KeyAction.RELEASE)
                        command_list.append(button_command)
                    elif op_code == ProfileMacro.Opcode.CONS_DOWN:
                        consumer_hid_usage = to_int(command.p1) << 8 | to_int(command.p2)
                        consumer_command = ConsumerKeyCommand(
                            key_id=ProfileButton.get_consumer_key_id(consumer_usage=consumer_hid_usage,
                                                                     os_variant=os_variant),
                            action=KeyAction.PRESS)
                        command_list.append(consumer_command)
                    elif op_code == ProfileMacro.Opcode.CONS_UP:
                        consumer_hid_usage = to_int(command.p1) << 8 | to_int(command.p2)
                        consumer_command = ConsumerKeyCommand(
                            key_id=ProfileButton.get_consumer_key_id(consumer_usage=consumer_hid_usage,
                                                                     os_variant=os_variant),
                            action=KeyAction.RELEASE)
                        command_list.append(consumer_command)
                    elif op_code == ProfileMacro.Opcode.XY:
                        x = to_int(command.p1) << 8 | to_int(command.p2)
                        y = to_int(command.p3) << 8 | to_int(command.p4)
                        xy_command = XYCommand(x=x, y=y)
                        command_list.append(xy_command)
                    elif op_code == ProfileMacro.Opcode.ROLLER:
                        wheel = to_int(command.p1)
                        roller_command = RollerCommand(wheel=wheel)
                        command_list.append(roller_command)
                    elif op_code == ProfileMacro.Opcode.AC_PAN:
                        ac_pan = to_int(command.p1)
                        ac_pan_command = AcPanCommand(ac_pan=ac_pan)
                        command_list.append(ac_pan_command)
                    # end if
                # end for
                entry_index = index
            # end if
        # end for
        return entry_index, command_list
    # end def convert_to_macro_commands

    def __str__(self):
        return f'Macro: {self.__hexlist__()}\nCRC 32: {self.crc_32}\nFILE_ID_LSB: {self.file_id_lsb}\n' \
               f'FIRST_SECTOR_ID_LSB: {self.first_sector_id_lsb}\n{self.entries}'
    # end def __str__

    def __repr__(self):
        return self.__str__()
    # end def __repr__
# end class Macro
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
