#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.analogkeysprofileformat
:brief: Analog Keys profile format definitions
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from enum import IntEnum
from enum import unique
from random import choice

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hid.usbhidusagetable import ALL_KEYS
from pyhid.hid.usbhidusagetable import KEYBOARD_HID_USAGE
from pyhid.hid.usbhidusagetable import KEYBOARD_HID_USAGE_TO_KEY_ID_MAP
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hidpp.features.common.analogkeys import AnalogKeys
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.fkcprofileformat import KEY_ID_TO_MODIFIER_BITFIELD
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.device.base.controllistutils import ControlListTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeysGenericConfigurationTable:
    """
    Define Analog Keys Generic Configuration Table class

    https://docs.google.com/spreadsheets/d/1S3Fz3mccpNIoguVkO6hN5ggfgllsojhGkD2j5E9f2A0/view#gid=1017032508
    """

    def __init__(self, rows):
        """
        :param rows: A list of ActuationPointPerKey or SensitivityPerKey
        :type rows: ``list[ActuationPointPerKey] | list[SensitivityPerKey]``
        """
        self.table_id = None
        self.rows = rows
        self.first_sector_id_lsb = None
        self.crc_32 = None
    # end def __init__

    def get_trigger_cids(self):
        """
        Get trigger CIDs in the table

        :return: The list of trigger CIDs
        :rtype: ``list[int]``
        """
        return [row.trigger_cidx for row in self.rows]
    # end def get_trigger_cids

    def append(self, new_rows):
        """
        Append ActuationPointPerKey, SensitivityPerKey, list[ActuationPointPerKey] or list[SensitivityPerKey] into
        the table.

        :param new_rows: The list or element of ActuationPointPerKey or SensitivityPerKey
        :type new_rows: ``ActuationPointPerKey | list[ActuationPointPerKey]
                            | SensitivityPerKey | list[SensitivityPerKey]``

        :raise ``TypeError``: If the input data type is invalid
        """
        trigger_cids = self.get_trigger_cids()
        if isinstance(new_rows, (ActuationPointPerKey, SensitivityPerKey)):
            new_rows = [new_rows]
        # end if

        is_data_valid_for_table = [
            (isinstance(row, ActuationPointPerKey) and isinstance(self, ActuationConfigurationTable)) or
            (isinstance(row, SensitivityPerKey) and isinstance(self, RapidTriggerConfigurationTable))
            for row in new_rows]
        if not all(is_data_valid_for_table):
            raise TypeError(
                f'The {[type(row) for row, valid in zip(new_rows, is_data_valid_for_table) if not valid]} '
                f'data type(s) to be appended into the {self.__class__.__name__} class is(are) not supported')
        else:
            for row in new_rows:
                if row.trigger_cidx in trigger_cids:
                    trigger_cid_index = trigger_cids.index(row.trigger_cidx)
                    self.rows[trigger_cid_index] = row
                else:
                    self.rows.append(row)
                # end if
            # end for
        # end if
    # end def append

    @property
    def n_bytes(self):
        """
        The number of bytes in the table

        :return: The byte count of table
        :rtype: ``int``
        """
        return len(self.__hexlist__())
    # end def n_bytes

    def register(self, directory, file_type_id):
        """
        Register to ``DirectoryFile``

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param file_type_id: The file type id
        :type file_type_id: ``ProfileManagement.FileTypeId.X1B08 | int``

        :return: Resource assignment information after registration
        :rtype: ``tuple(int, int, int)``
        """
        return directory.register(
            feature_id=AnalogKeys.FEATURE_ID,
            file_type_id=file_type_id,
            table_object=self)
    # end def register

    def __hexlist__(self):
        """
        Convert ``ActuationConfigurationTable`` to its ``HexList`` representation

        :return: ActuationConfigurationTable data in ``HexList``
        :rtype: ``HexList``
        """
        actuation_data_in_hex_list = HexList(f'{Numeral(self.table_id, byteCount=1)}'
                                             f'{Numeral(len(self.rows), byteCount=(len(self.rows) // (2 ** 8)) + 1)}')
        for row in self.rows:
            actuation_data_in_hex_list += HexList(row)
        # end for
        return actuation_data_in_hex_list
    # end def __hexlist__

    def __str__(self):
        string_message = \
            f'\n{self.__class__.__name__}: {self.__hexlist__()}\n' \
            f'CRC 32: {self.crc_32}\nFIRST_SECTOR_ID_LSB: {self.first_sector_id_lsb}' + \
            f'\n - HEADER: \n  - Table ID: {self.table_id} \n  - Key Count: {len(self.rows)} \n - ' + \
            '\n - '.join([f'ROW#{index}: ' + str(row) for index, row in enumerate(self.rows)])
        return string_message
    # end def __str__
# end class AnalogKeysGenericConfigurationTable


class ActuationPointPerKey(BitFieldContainerMixin):
    """
    Define class for configuration of Actuation Point per key
    """

    class LEN(IntEnum):
        """
        FIELDS length
        """
        TRIGGER_CIDX = 0x08
        ACTUATION_POINT = 0x08
    # end class LEN

    class FID(IntEnum):
        """
        FIELDS identifier
        """
        TRIGGER_CIDX = 0xFF
        ACTUATION_POINT = TRIGGER_CIDX - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.TRIGGER_CIDX,
            length=LEN.TRIGGER_CIDX,
            title='Trigger Cidx',
            name='trigger_cidx',
            checks=(CheckHexList(LEN.TRIGGER_CIDX // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.TRIGGER_CIDX) - 1),)),
        BitField(
            fid=FID.ACTUATION_POINT,
            length=LEN.ACTUATION_POINT,
            title='Actuation Point',
            name='actuation_point',
            checks=(CheckHexList(LEN.ACTUATION_POINT // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.ACTUATION_POINT) - 1),)),
    )
# end class ActuationPointPerKey


class ActuationConfigurationTable(AnalogKeysGenericConfigurationTable):
    """
    Define Actuation Configuration Table class
    """

    def __init__(self, rows):
        """
        :param rows: An element of list of ActuationPointPerKey
        :type rows: ``ActuationPointPerKey | list[ActuationPointPerKey]``

        :raise ``TypeError``: If the input data type is invalid
        """
        if isinstance(rows, ActuationPointPerKey):
            rows = [rows]
        # end if

        if not all(isinstance(row, ActuationPointPerKey) for row in rows):
            raise TypeError('Unsupported data type(s) for ActuationConfigurationTable: '
                            f'{[type(row) for row in rows if not isinstance(row, ActuationPointPerKey)]}')
        # end if

        super().__init__(rows=rows)
    # end def __init__

    def register(self, directory, file_type_id=ProfileManagement.FileTypeId.X1B08.ACTUATION_CONFIGURATION_FILE):
        """
        Register to ``DirectoryFile``

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param file_type_id: The file type id - OPTIONAL
        :type file_type_id: ``ProfileManagement.FileTypeId.X1B08 | int``
        """
        self.table_id, _, self.first_sector_id_lsb = super().register(
            directory=directory,
            file_type_id=file_type_id)
        self.crc_32 = directory.update_file(file_id_lsb=self.table_id, table_in_hexlist=self.__hexlist__())
    # end def register
# end class ActuationConfigurationTable


class SensitivityPerKey(BitFieldContainerMixin):
    """
    Define class for configuration of sensitivity per key
    """

    class LEN(IntEnum):
        """
        FIELDS length
        """
        TRIGGER_CIDX = 0x08
        SENSITIVITY = 0x08
    # end class LEN

    class FID(IntEnum):
        """
        FIELDS identifier
        """
        TRIGGER_CIDX = 0xFF
        SENSITIVITY = TRIGGER_CIDX - 1
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.TRIGGER_CIDX,
            length=LEN.TRIGGER_CIDX,
            title='Trigger Cidx',
            name='trigger_cidx',
            checks=(CheckHexList(LEN.TRIGGER_CIDX // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.TRIGGER_CIDX) - 1),)),
        BitField(
            fid=FID.SENSITIVITY,
            length=LEN.SENSITIVITY,
            title='Sensitivity',
            name='sensitivity',
            checks=(CheckHexList(LEN.SENSITIVITY // 8),
                    CheckInt(min_value=0, max_value=pow(2, LEN.SENSITIVITY) - 1),)),
    )
# end class SensitivityPerKey


class RapidTriggerConfigurationTable(AnalogKeysGenericConfigurationTable):
    """
    Define Rapid Trigger Configuration Table class
    """

    def __init__(self, rows):
        """
        :param rows: A list of SensitivityPerKey
        :type rows: ``list[SensitivityPerKey]``
        """
        super().__init__(rows=rows)
    # end def __init__

    def register(self, directory, file_type_id=ProfileManagement.FileTypeId.X1B08.RAPID_TRIGGER_CONFIGURATION_FILE):
        """
        Register to ``DirectoryFile``

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        :param file_type_id: The file type id - OPTIONAL
        :type file_type_id: ``ProfileManagement.FileTypeId.X1B08 | int``
        """
        self.table_id, _, self.first_sector_id_lsb = super().register(
            directory=directory,
            file_type_id=file_type_id)
        self.crc_32 = directory.update_file(file_id_lsb=self.table_id, table_in_hexlist=self.__hexlist__())
    # end def register
# end class RapidTriggerConfigurationTable


class MultiActionConfigurationTable:
    """
    Define Multi Action Configuration Table class

    https://docs.google.com/spreadsheets/d/1S3Fz3mccpNIoguVkO6hN5ggfgllsojhGkD2j5E9f2A0/view#gid=1017032508
    """

    @unique
    class Event(IntEnum):
        """
        Enum for multi-action events
        """
        RELEASED = 0
        PRESSED = 1
        MAKE = 2
        BREAK = 3
        MAKE_BREAK = 4

        # Below events are not available in version 0
        # BREAK_MAKE = 5
        # BREAK_MAKE_BREAK = 6
    # end class Event

    def __init__(self, groups, cid_list=None):
        """
        :param groups: A list of MultiActionConfigurationTable group
        :type groups: ``list[ActionGroup]``
        :param cid_list: CID list of the device - OPTIONAL
        :type cid_list: ``list[CID] | None``
        """
        self.groups = groups
        self.table_id = None
        self.first_sector_id_lsb = None
        self.crc_32 = None
        self.cid_list = cid_list

        self.update_trigger_cidx_in_groups()
    # end def __init__

    def init_cid_list(self, cid_list):
        """
        Initialize the CID list and update the trigger CIDx in groups

        :param cid_list: CID list of the device
        :type cid_list: ``list[CID]``
        """
        self.cid_list = cid_list

        self.update_trigger_cidx_in_groups()
    # end def init_cid_list

    def update_trigger_cidx_in_groups(self):
        """
        Update trigger CIDx in groups

        :raise ``Exception``: If cid_list is None or can not find cid and cid_index
        """
        if self.cid_list is not None:
            for group in self.groups:
                cid = ControlListTestUtils.key_id_to_cid_by_provided_cid_list(cid_list=self.cid_list,
                                                                              key_id=group.trigger_key)
                if cid is None:
                    raise Exception(
                        f'The trigger key: {group.trigger_key!r} is not found in the CID list of the device.')
                # end if
                cid_index = ControlListTestUtils.get_cid_index_by_provided_cid_list(cid_list=self.cid_list, cid=cid)
                if cid_index is not None:
                    group.trigger_cidx = cid_index
                else:
                    raise Exception(f'The cid index of {cid!r} is not found in the CID list of the device.')
                # end if
            # end for
        else:
            raise Exception(
                f'Trigger CIDx of groups are not able to be updated, since the CID list is not initialized yet.')
        # end if
    # end def update_trigger_cidx_in_groups

    def get_trigger_cids(self):
        """
        Get trigger CIDs in the table

        :return: The list of trigger CIDs
        :rtype: ``list[int]``
        """
        if self.cid_list is None:
            warnings.warn("The CID list is not initialized yet.")
        # end if

        return [group.trigger_cidx for group in self.groups]
    # end def get_trigger_cids

    def get_trigger_keys(self):
        """
        Get trigger keys in the table

        :return: The list of trigger keys
        :rtype: ``list[int]``
        """
        return [group.trigger_key for group in self.groups]
    # end def get_trigger_keys

    def append(self, new_groups):
        """
        Append ``ActionGroup`` into the table

        :param new_groups: The list of ``ActionGroup``
        :type new_groups: ``list[ActionGroup] | ActionGroup``

        :raise ``TypeError``: If the input data type is invalid
        """
        trigger_keys = self.get_trigger_keys()
        if isinstance(new_groups, ActionGroup):
            new_groups = [new_groups]
        # end if

        if isinstance(new_groups, list):
            for group in new_groups:
                if group.trigger_key in trigger_keys:
                    trigger_key_index = trigger_keys.index(group.trigger_key)
                    self.groups[trigger_key_index] = group
                else:
                    self.groups.append(group)
                # end if
            # end for
        else:
            raise TypeError(
                f'Unsupported data type to be appended into the {self.__class__.__name__}: {type(new_groups)}')
        # end if
    # end def append

    def register(self, directory):
        """
        Register to ``DirectoryFile``

        :param directory: ``DirectoryFile`` instance
        :type directory: ``DirectoryFile``
        """
        self.table_id, _, self.first_sector_id_lsb = directory.register(
            feature_id=AnalogKeys.FEATURE_ID,
            file_type_id=ProfileManagement.FileTypeId.X1B08.MULTI_ACTION_CONFIGURATION_FILE,
            table_object=self)
        self.crc_32 = directory.update_file(file_id_lsb=self.table_id, table_in_hexlist=self.__hexlist__())
    # end def register

    @property
    def n_bytes(self):
        """
        The number of bytes in the Multi-Action configuration table

        :return: The byte count of  Multi-Action configuration table
        :rtype: ``int``
        """
        return len(self.__hexlist__())
    # end def n_bytes

    @property
    def key_count(self):
        """
        Number of trigger keys in the table

        :return: The number of trigger keys
        :rtype: ``int``
        """
        return len(self.groups)
    # end def key_count

    @property
    def supported_events(self):
        """
        Supported multi-action events

        :return: A list of supported multi-action events
        :rtype: ``list[MultiActionConfigurationTable.Event]``
        """
        return list(MultiActionConfigurationTable.Event.__members__.values())
    # end def supported_events

    def __hexlist__(self):
        """
        Convert ``MultiActionConfigurationTable`` to its ``HexList`` representation

        :return: MultiActionConfigurationTable data in ``HexList``
        :rtype: ``HexList``
        """
        multi_action_table_in_hex = HexList(f'{Numeral(self.table_id, byteCount=1)}'
                                            f'{Numeral(len(self.groups), byteCount=1)}')
        for group in self.groups:
            multi_action_table_in_hex += HexList(group)
        # end for
        return multi_action_table_in_hex
    # end def __hexlist__

    def __str__(self):
        table_str = f'MultiActionConfigurationTable: {self.__hexlist__()}\nCRC 32: {self.crc_32}\n' \
                    f'Table ID: {self.table_id}\nKey Count: {self.key_count}\n' \
                    f'FIRST_SECTOR_ID_LSB: {self.first_sector_id_lsb}\n* ' + \
                    f'\n* '.join([f'GROUP#{index}:\n' + str(group) for index, group in enumerate(self.groups)])
        return table_str
    # end def __str__
# end class MultiActionConfigurationTable


class ActionAssignment:
    """
    Multi-Action assignment information class
    """
    NUM_OF_EVENTS = 4

    @unique
    class Opcode(IntEnum):
        """
        Enum for multi-action remapping opcodes
        """
        REMAP_TO_STANDARD_KEY = 0x8002
        NO_ACTION = 0x9000
    # end class Opcode

    def __init__(self, action_key=None,
                 opcode=Opcode.REMAP_TO_STANDARD_KEY,
                 event_0=MultiActionConfigurationTable.Event.RELEASED,
                 event_1=MultiActionConfigurationTable.Event.RELEASED,
                 event_2=MultiActionConfigurationTable.Event.RELEASED,
                 event_3=MultiActionConfigurationTable.Event.RELEASED,
                 random_attributes=False):
        """
        :param action_key: Action key id - OPTIONAL
        :type action_key: ``KEY_ID | None``
        :param opcode: Opcode of the assignment - OPTIONAL
        :type opcode: ``Opcode``
        :param event_0: Event 0 of the assignment - OPTIONAL
        :type event_0: ``int | MultiActionConfigurationTable.Event``
        :param event_1: Event 1 of the assignment - OPTIONAL
        :type event_1: ``int | MultiActionConfigurationTable.Event``
        :param event_2: Event 2 of the assignment - OPTIONAL
        :type event_2: ``int | MultiActionConfigurationTable.Event``
        :param event_3: Event 3 of the assignment - OPTIONAL
        :type event_3: ``int | MultiActionConfigurationTable.Event``
        :param random_attributes: Flag indicating the value of attributes are assign randomly - OPTIONAL
        :type random_attributes: ``bool``

        :raise ``ValueError``: If the input action key is not valid
        """
        if not random_attributes:
            if action_key is not None and action_key not in \
                    (list(STANDARD_KEYS.keys()) + [KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION]):
                raise ValueError(f"Unsupported action key: {action_key!r}")
            # end if

            # params.p1 is reserved
            params = HexList(0,
                             Numeral(0 if action_key is None else ALL_KEYS[action_key], byteCount=1))
        else:
            event_types = list(MultiActionConfigurationTable.Event.__members__.values())
            # params.p1 is reserved
            params = HexList(0, Numeral(choice(list(STANDARD_KEYS.values())), byteCount=1))

            # FIXME: Removed this flag once the Multi-Action feature is fully implemented
            support_pre_defined_event_only = True
            # cf: Definition of pre-defined events
            # https://docs.google.com/spreadsheets/d/1S3Fz3mccpNIoguVkO6hN5ggfgllsojhGkD2j5E9f2A0/view#gid=2066641134

            if support_pre_defined_event_only:
                # FIXME: Removed this statement once the Multi-Action feature is fully implemented
                # NB: The events are ignored if the firmware is supporting pre-defined events only
                event_0 = 0
                event_1 = 0
                event_2 = 0
                event_3 = 0
            else:
                event_0 = choice(event_types)
                event_1 = choice(event_types)
                event_2 = choice(event_types)
                event_3 = choice(event_types)
            # end if
        # end if
        self.assignment = ActionGroup.AssignmentRow(
            opcode=opcode, params=params, event_0=event_0, event_1=event_1, event_2=event_2, event_3=event_3)
    # end def __init__

    @property
    def events(self):
        """
        Multi-Action events of the assignment

        :return: A list of multi-action events
        :rtype: ``list[MultiActionConfigurationTable.Event]``
        """
        return [self.assignment.event_0, self.assignment.event_1, self.assignment.event_2, self.assignment.event_3]
    # end def events

    def __str__(self):
        string_message = \
            f'\n{self.__class__.__name__}: {self.assignment}'
        return string_message
    # end def __str__
# end class ActionAssignment


class ActionGroup:
    """
    Group in the table represents one or more key presses grouped according to the trigger key

    Note:
        - Assignment row need to filled by order, so that device can know the priority while parsing.
        - When modifier and standard key assigned together, modifier must with the higher order

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    TriggerCidx                   8
    2ndActuationPoint             8
    NumAssignment                 8
    AssignmentRow[n]              8 x 6 x n
    ============================  ==========
    """

    ASSIGNMENT_ROW_LENGTH = 6
    MAX_NUM_ASSIGNMENT = 4

    class AssignmentRow(BitFieldContainerMixin):
        """
        The lookup table for assignment row definition

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        OpCode                        0x10
        Params                        0x10
        Event 0                       4
        Event 1                       4
        Event 2                       4
        Event 3                       4
        ============================  ==========
        """

        class FID:
            """
            Field Identifiers
            """
            OPCODE = 0xFF
            PARAMS = OPCODE - 1
            EVENT_1 = PARAMS - 1
            EVENT_0 = EVENT_1 - 1
            EVENT_3 = EVENT_0 - 1
            EVENT_2 = EVENT_3 - 1
        # end class FID

        class LEN:
            """
            Field Lengths in bits
            """
            OPCODE = 0x10
            PARAMS = 0x10
            EVENT_1 = 0x4
            EVENT_0 = 0x4
            EVENT_3 = 0x4
            EVENT_2 = 0x4
        # end class LEN

        FIELDS = (
            BitField(
                fid=FID.OPCODE,
                length=LEN.OPCODE,
                title='Opcode',
                name='opcode',
                checks=(CheckHexList(LEN.OPCODE // 8),
                        CheckInt(min_value=0, max_value=pow(2, LEN.OPCODE) - 1),)),
            BitField(
                fid=FID.PARAMS,
                length=LEN.PARAMS,
                title='Params',
                name='params',
                checks=(CheckHexList(LEN.PARAMS // 8),
                        CheckInt(min_value=0, max_value=pow(2, LEN.PARAMS) - 1),)),
            BitField(
                fid=FID.EVENT_1,
                length=LEN.EVENT_1,
                title='Event1',
                name='event_1',
                checks=(CheckInt(min_value=0, max_value=pow(2, LEN.EVENT_1) - 1),),
                default_value=0),
            BitField(
                fid=FID.EVENT_0,
                length=LEN.EVENT_0,
                title='Event0',
                name='event_0',
                checks=(CheckInt(min_value=0, max_value=pow(2, LEN.EVENT_0) - 1),),
                default_value=0),
            BitField(
                fid=FID.EVENT_3,
                length=LEN.EVENT_3,
                title='Event3',
                name='event_3',
                checks=(CheckInt(min_value=0, max_value=pow(2, LEN.EVENT_3) - 1),),
                default_value=0),
            BitField(
                fid=FID.EVENT_2,
                length=LEN.EVENT_2,
                title='Event2',
                name='event_2',
                checks=(CheckInt(min_value=0, max_value=pow(2, LEN.EVENT_2) - 1),),
                default_value=0),
        )
    # end class AssignmentRow

    def __init__(self, trigger_key=None, second_actuation_point=None, rows=None, random_assignments=False):
        """
        :param trigger_key: The trigger key - OPTIONAL
        :type trigger_key: ``int | KEY_ID``
        :param second_actuation_point: The 2nd actuation point of Multi-Action - OPTIONAL
        :type second_actuation_point: ``int``
        :param rows: A list of assignments of Multi-Action - OPTIONAL
        :type rows: ``list[ActionGroup.AssignmentRow] | list[ActionAssignment]``
        :param random_assignments: Flag indicating the assignments of the group are generate randomly - OPTIONAL
        :type random_assignments: ``bool``

        :raise ``AssertionError``: If the number of assignments is more than the maximum number of assignments
        """
        self.trigger_key = trigger_key
        self.trigger_cidx = None
        self.second_actuation_point = second_actuation_point

        if not random_assignments:
            self.rows = [] if rows is None else \
                ([row.assignment for row in rows] if isinstance(rows[0], ActionAssignment) else rows)

            assert len(self.rows) <= self.MAX_NUM_ASSIGNMENT, \
                f"The number of assignments ({len(rows)}) is not allowed to exceed {self.MAX_NUM_ASSIGNMENT}"
        else:
            # FIXME: Removed this flag once the Multi-Action feature is fully implemented
            support_pre_defined_event_only = True
            # cf: Definition of pre-defined events
            # https://docs.google.com/spreadsheets/d/1S3Fz3mccpNIoguVkO6hN5ggfgllsojhGkD2j5E9f2A0/view#gid=2066641134

            if support_pre_defined_event_only:
                # FIXME: Removed this statement once the Multi-Action feature is fully implemented
                # Assignment for 1st modifier
                valid_modifier_keys = list(KEY_ID_TO_MODIFIER_BITFIELD.keys())
                assignment_0 = ActionAssignment(opcode=choice([ActionAssignment.Opcode.NO_ACTION,
                                                               ActionAssignment.Opcode.REMAP_TO_STANDARD_KEY]),
                                                action_key=choice(valid_modifier_keys),
                                                event_0=MultiActionConfigurationTable.Event.MAKE,
                                                event_1=MultiActionConfigurationTable.Event.PRESSED,
                                                event_2=MultiActionConfigurationTable.Event.PRESSED,
                                                event_3=MultiActionConfigurationTable.Event.BREAK).assignment
                # Assignment for 1st standard key
                valid_action_keys = set(STANDARD_KEYS.keys())
                valid_action_keys.difference_update(set(KEY_ID_TO_MODIFIER_BITFIELD.keys()))
                assignment_1 = ActionAssignment(opcode=choice([ActionAssignment.Opcode.NO_ACTION,
                                                               ActionAssignment.Opcode.REMAP_TO_STANDARD_KEY]),
                                                action_key=choice(list(valid_action_keys)),
                                                event_0=MultiActionConfigurationTable.Event.MAKE,
                                                event_1=MultiActionConfigurationTable.Event.PRESSED,
                                                event_2=MultiActionConfigurationTable.Event.PRESSED,
                                                event_3=MultiActionConfigurationTable.Event.BREAK).assignment
                # Assignment for 2nd modifier
                assignment_2 = ActionAssignment(opcode=choice([ActionAssignment.Opcode.NO_ACTION,
                                                               ActionAssignment.Opcode.REMAP_TO_STANDARD_KEY]),
                                                action_key=choice(valid_modifier_keys),
                                                event_0=MultiActionConfigurationTable.Event.RELEASED,
                                                event_1=MultiActionConfigurationTable.Event.MAKE,
                                                event_2=MultiActionConfigurationTable.Event.BREAK,
                                                event_3=MultiActionConfigurationTable.Event.RELEASED).assignment
                # Assignment for 2nd standard key
                assignment_3 = ActionAssignment(opcode=choice([ActionAssignment.Opcode.NO_ACTION,
                                                               ActionAssignment.Opcode.REMAP_TO_STANDARD_KEY]),
                                                action_key=choice(list(valid_action_keys)),
                                                event_0=MultiActionConfigurationTable.Event.RELEASED,
                                                event_1=MultiActionConfigurationTable.Event.MAKE,
                                                event_2=MultiActionConfigurationTable.Event.BREAK,
                                                event_3=MultiActionConfigurationTable.Event.RELEASED).assignment
                self.rows = [assignment_0, assignment_1, assignment_2, assignment_3]
            else:
                self.rows = [ActionAssignment(random_attributes=True).assignment for _ in range(
                    choice(range(self.MAX_NUM_ASSIGNMENT)))]
                self.sort()
            # end if
        # end if
    # end def __init__

    @property
    def action_keys(self):
        """
        Return action keys of the group

        :return: Action keys of the group
        :rtype: ``list[KEY_ID]``
        """
        return [0 if assignment.params[1] == 0 else
                KEYBOARD_HID_USAGE_TO_KEY_ID_MAP[assignment.params[1]] for assignment in self.rows]
    # end def action_keys

    def sort(self):
        """
        Sort assignments in the group

        NB: When modifier and standard key assigned together, modifier must with the higher order

        :raise ``ValueError``: If the number of modifier keys or non-modifier keys is more than 2
        """
        # FIXME: Removed this flag once the Multi-Action feature is fully implemented
        support_pre_defined_event_only = True
        # cf: Definition of pre-defined events
        # https://docs.google.com/spreadsheets/d/1S3Fz3mccpNIoguVkO6hN5ggfgllsojhGkD2j5E9f2A0/view#gid=2066641134

        if support_pre_defined_event_only:
            modifier_sorted_index = 0
            non_modifier_sorted_index = 1
            for index, row in enumerate(self.rows):
                if (to_int(row.params) & 0xFF) in range(KEYBOARD_HID_USAGE.KEYBOARD_LEFT_CONTROL,
                                                        KEYBOARD_HID_USAGE.KEYBOARD_RIGHT_GUI + 1):
                    if modifier_sorted_index > 2:
                        raise ValueError(
                            'To many modifier keys, it is not a valid setting in current Multi-Action feature version')
                    # end if
                    self.rows.remove(row)
                    self.rows.insert(modifier_sorted_index, row)
                    modifier_sorted_index += 2
                else:
                    if non_modifier_sorted_index > 3:
                        raise ValueError('To many non modifier keys, it is not a valid setting in current Multi-Action '
                                         'feature version')
                    # end if
                    self.rows.remove(row)
                    self.rows.insert(non_modifier_sorted_index, row)
                    non_modifier_sorted_index += 2
                # end if
            # end for
        else:
            sorted_index = 0
            for row in self.rows:
                if (to_int(row.params) & 0xFF) in range(KEYBOARD_HID_USAGE.KEYBOARD_LEFT_CONTROL,
                                                        KEYBOARD_HID_USAGE.KEYBOARD_RIGHT_GUI + 1):
                    self.rows.remove(row)
                    self.rows.insert(sorted_index, row)
                    sorted_index += 1
                # end if
            # end for
        # end if
    # end def sort

    def __hexlist__(self):
        """
        Convert ``ActionGroup`` to its ``HexList`` representation

        :return: ``ActionGroup`` data in ``HexList``
        :rtype: ``HexList``
        """
        group_hex_list = HexList(f'{Numeral(self.trigger_cidx, byteCount=1)}'
                                 f'{Numeral(self.second_actuation_point, byteCount=1)}'
                                 f'{Numeral(len(self.rows), byteCount=1)}')
        for row in self.rows:
            group_hex_list += HexList(row)
        # end for
        return group_hex_list
    # end def __hexlist__

    def append(self, new_rows):
        """
        Append ``ActionGroup.AssignmentRow`` into the group

        :param new_rows: The list of ``ActionGroup.AssignmentRow``
        :type new_rows: ``ActionGroup.AssignmentRow | ActionAssignment``

        :raise ``TypeError``: If the input data type is invalid
        """
        if isinstance(new_rows, list):
            for row in new_rows:
                self.rows.append(row)
            # end for
        elif isinstance(new_rows, ActionGroup.AssignmentRow):
            self.rows.append(new_rows)
        elif isinstance(new_rows, ActionAssignment):
            self.rows.append(new_rows.assignment)
        else:
            raise TypeError(
                f'Unsupported data type to be appended into the {self.__class__.__name__}: {type(new_rows)}')
        # end if
    # end def append

    @property
    def num_of_assignments(self):
        """
        Get the number of assignments in the group

        :return: The number of assignments
        :rtype: ``int``
        """
        return len(self.rows)
    # end def num_of_assignments

    def __str__(self):
        return f'- TRIGGER_CIDX: {self.trigger_cidx}' \
               f'\n- TRIGGER_KEY_ID: {self.trigger_key!r}' \
               f'\n- SECOND_ACTUATION_POINT: {self.second_actuation_point}' \
               f'\n- NUM_ASSIGNMENTS: {self.num_of_assignments}\n- ' + \
            '\n- '.join(
                [f'ROW#{index}: ' +
                 f'\n  - ActionKey: {0 if to_int(row.params) == 0 else list(ALL_KEYS.keys())[list(ALL_KEYS.values()).index(to_int(row.params))]!r}' +
                 f'\n  - {str(row)}' for index, row in enumerate(self.rows)])
    # end def __str__
# end class ActionGroup
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
