#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.base.cidutils
    :brief: Help for CID Info
    :author: Martin Cryonnet
    :date: 2020/10/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import auto
from enum import IntEnum
from enum import unique
from sys import stdout

from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.controlidtable import CidTable
from pyhid.hidpp.features.common.specialkeysmsebuttons import CidInfoPayload
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.emulatorsmanager import EmulatorsManager


# ------------------------------------------------------------------------------
# Features implementation
# ------------------------------------------------------------------------------
class CidInfoFlags:
    # Additional flags
    RAW_XY_POS = 0
    RAW_XY_FLAG = (1 << RAW_XY_POS)
    FORCE_RAW_XY_POS = 1
    FORCE_RAW_XY_FLAG = (1 << FORCE_RAW_XY_POS)
    ANALYTICS_KEY_EVENTS_POS = 2
    ANALYTICS_KEY_EVENTS_FLAG = (1 << ANALYTICS_KEY_EVENTS_POS)
    RAW_WHEEL_POS = 3
    RAW_WHEEL_FLAG = (1 << RAW_WHEEL_POS)

    # Flags
    MOUSE_POS = 8
    MOUSE_FLAG = (1 << MOUSE_POS)
    F_KEY_POS = 9
    F_KEY_FLAG = (1 << F_KEY_POS)
    HOT_KEY_POS = 10
    HOT_KEY_FLAG = (1 << HOT_KEY_POS)
    FN_TOG_POS = 11
    FN_TOG_FLAG = (1 << FN_TOG_POS)
    REPROG_POS = 12
    REPROG_FLAG = (1 << REPROG_POS)
    DIVERT_POS = 13
    DIVERT_FLAG = (1 << DIVERT_POS)
    PERSIST_POS = 14
    PERSIST_FLAG = (1 << PERSIST_POS)
    VIRTUAL_POS = 15
    VIRTUAL_FLAG = (1 << VIRTUAL_POS)
# end class CidInfoFlags


@unique
class CidEmulation(IntEnum):
    """
    CID Emulation values
    """
    IGNORED = auto()
    LIMITED = auto()
    FULL = auto()
# end class CidEmulation


class CidInfoConfig:
    """
    Class representing CID Info from configuration
    """
    def __init__(self, index, friendly_name, cid, task, flag_virtual, flag_persist, flag_divert, flag_reprog,
                 flag_fn_tog, flag_hot_key, flag_f_key, flag_mouse, pos, group, gmask, additional_flags_raw_wheel,
                 additional_flags_analytics_key_event, additional_flags_force_raw_xy, additional_flags_raw_xy):
        """
        Constructor

        :param index: Index in the CID info table
        :type index: ``int``
        :param friendly_name: Friendly name
        :type friendly_name: ``str``
        :param cid: Control Id
        :type cid: ``int`` or ``HexList``
        :param task: Task Id
        :type task: ``int`` or ``HexList``
        :param flag_virtual: Virtual flag
        :type flag_virtual: ``bool`` or ``int`` or ``HexList``
        :param flag_persist: Persist flag
        :type flag_persist: ``bool`` or ``int`` or ``HexList``
        :param flag_divert: Divert flag
        :type flag_divert: ``bool`` or ``int`` or ``HexList``
        :param flag_reprog: Reprog flag
        :type flag_reprog: ``bool`` or ``int`` or ``HexList``
        :param flag_fn_tog: FnTog flag
        :type flag_fn_tog: ``bool`` or ``int`` or ``HexList``
        :param flag_hot_key: HotKey flag
        :type flag_hot_key: ``bool`` or ``int`` or ``HexList``
        :param flag_f_key: FKey flag
        :type flag_f_key: ``bool`` or ``int`` or ``HexList``
        :param flag_mouse: Mouse flag
        :type flag_mouse: ``bool`` or ``int`` or ``HexList``
        :param pos: Pos
        :type pos: ``int`` or ``HexList``
        :param group: Group
        :type group: ``int`` or ``HexList``
        :param gmask: GMask
        :type gmask: ``int`` or ``HexList``
        :param additional_flags_raw_wheel: Raw Wheel flag
        :type additional_flags_raw_wheel: ``bool`` or ``int`` or ``HexList``
        :param additional_flags_analytics_key_event: Analytics Key Event flag
        :type additional_flags_analytics_key_event: ``bool`` or ``int`` or ``HexList``
        :param additional_flags_force_raw_xy: Force Raw XY flag
        :type additional_flags_force_raw_xy: ``bool`` or ``int`` or ``HexList``
        :param additional_flags_raw_xy: Raw XY flag
        :type additional_flags_raw_xy: ``bool`` or ``int`` or ``HexList``
        """
        self.index = index
        self.friendly_name = friendly_name
        self.cid_info_payload = CidInfoPayload.from_detailed_fields(
            cid, task, flag_virtual, flag_persist, flag_divert, flag_reprog, flag_fn_tog, flag_hot_key, flag_f_key,
            flag_mouse, pos, group, gmask, additional_flags_raw_wheel, additional_flags_analytics_key_event,
            additional_flags_force_raw_xy, additional_flags_raw_xy)
    # end def __init__

    @classmethod
    def from_index(cls, features, index, config_manager=None):
        """
        Constructor from index in the CID info table in configuration.

        :param features: Context features
        :type features: ``context.features``
        :param index: Index in the CID info table
        :type index: ``int``
        :param config_manager: Configuration manager - OPTIONAL
        :type config_manager: ``ConfigurationManager``

        :return: Class instance
        :rtype: ``CidInfoConfig``
        """
        config_manager = ConfigurationManager(features) if config_manager is None else config_manager
        return cls(index,
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FRIENDLY_NAME)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_TASK)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FLAG_VIRTUAL)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FLAG_PERSIST)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FLAG_DIVERT)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FLAG_REPROG)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FLAG_FNTOG)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FLAG_HOTKEY)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FLAG_FKEY)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FLAG_MOUSE)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_POS)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_GROUP)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_GMASK)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_ADDITIONAL_FLAGS_RAW_WHEEL)[index],
                   config_manager.get_feature(
                       ConfigurationManager.ID.CID_INFO_TABLE_ADDITIONAL_FLAGS_ANALYTICS_KEY_EVENTS)[index],
                   config_manager.get_feature(
                       ConfigurationManager.ID.CID_INFO_TABLE_ADDITIONAL_FLAGS_FORCE_RAW_XY)[index],
                   config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_ADDITIONAL_FLAGS_RAW_XY)[index])
    # end def from_index

    @classmethod
    def from_friendly_name(cls, features, friendly_name, config_manager):
        """
        Constructor from friendly name in the CID info table in configuration.

        :param features: Context features
        :type features: ``context.features``
        :param friendly_name: Friendly name in the CID info table
        :type friendly_name: ``str``
        :param config_manager: Configuration manager - OPTIONAL
        :type config_manager: ``ConfigurationManager``

        :return: Class instance
        :rtype: ``CidInfoConfig``
        """
        config_manager = ConfigurationManager(features) if config_manager is None else config_manager
        index = config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_FRIENDLY_NAME).index(friendly_name)
        return cls.from_index(features, index, config_manager)
    # end def from_friendly_name

    @classmethod
    def from_cid(cls, features, cid, config_manager):
        """
        Constructor from CID in the CID info table in configuration.

        :param features: Context features
        :type features: ``context.features``
        :param cid: Friendly name in the CID info table
        :type cid: ``int``
        :param config_manager: Configuration manager - OPTIONAL
        :type config_manager: ``ConfigurationManager``

        :return: Class instance
        :rtype: ``CidInfoConfig``
        """
        config_manager = ConfigurationManager(features) if config_manager is None else config_manager
        index = config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID).index(cid)
        return cls.from_index(features, index, config_manager)
    # end def from_cid
# end class CidInfoConfig


class CidInfoCoverage:
    """
    Class to resolve CID Info coverage
    """
    def __init__(self):
        """
        Constructor
        """
        self.connected_cids = None
    # end def __init__

    def init_connected_cids(self, context):
        """
        Initialize connected CIDs

        :param context: Current context
        :type context: ``context``
        """
        context_features = context.getFeatures()
        config_manager = ConfigurationManager(context_features)
        cid_info_table = config_manager.get_feature(ConfigurationManager.ID.CID_TABLE)
        emulators_manager = EmulatorsManager.get_instance(context_features)
        emulators_manager.init(config_manager.current_device_type)
        connected_key_ids = emulators_manager.get_connected_key_ids()
        self.connected_cids = []
        for cid_info in cid_info_table:
            cid = int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).cid))
            if cid in CID_TO_KEY_ID_MAP and CID_TO_KEY_ID_MAP[cid] in connected_key_ids:
                self.connected_cids.append(cid)
            else:
                stdout.write(f'CID = {cid:#04x} is present in the test settings but not in the KEY_ID map or in the '
                             'connected key id list\n')
            # end if
        # end for
    # end def init_connected_cids

    def get_emulated(self, context, cid_info_table):
        """
        Get emulated CID from CID info table

        :param context: Current context
        :type context: ``context``
        :param cid_info_table: List of CID info
        :type cid_info_table: ``list``

        :return: Connected CIDs
        :rtype: ``list``
        """
        if self.connected_cids is None:
            self.init_connected_cids(context)
        # end if
        cid_info_list = [cid_info for cid_info in cid_info_table if (
                int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).cid)) in self.connected_cids and
                # CID = 0x50 on a touchpad (i.e Left button) is not emulated on the Platform DEV board yet
                not (context.getFeatures().PRODUCT.F_IsPlatform and
                     not CidInfoPayload.fromHexList(HexList(cid_info)).flags.mouse and
                     int(Numeral(CidInfoPayload.fromHexList(HexList(cid_info)).cid)) == CidTable.LEFT_CLICK))]
        return cid_info_list
    # end def get_emulated

    @staticmethod
    def cid_info_flags_selection(cid_info_table, flags, with_flag):
        """
        Select CID info based on flags

        :param cid_info_table: List of CID info
        :type cid_info_table: ``list``
        :param flags: Flags for CID selection
        :type flags: ``int``
        :param with_flag: Select CID info with or without the given flags
        :type with_flag: ``bool``

        :return: CID info matching the flags
        :rtype: ``list``
        """
        result = []
        additional_flags = flags & 0xFF
        flags = (flags >> 8) & 0xFF
        for cid_info in cid_info_table:
            str_min_len = (CidInfoPayload.LEN.CTRL_ID + CidInfoPayload.LEN.TASK_ID + CidInfoPayload.LEN.FLAGS) // 4
            str_add_flags_len = (CidInfoPayload.LEN.CTRL_ID + CidInfoPayload.LEN.TASK_ID + CidInfoPayload.LEN.FLAGS +
                                 CidInfoPayload.LEN.FKEY_POS + CidInfoPayload.LEN.GROUP + CidInfoPayload.LEN.GMASK +
                                 CidInfoPayload.LEN.ADDITIONAL_FLAGS) // 4
            if len(cid_info) < str_min_len or (len(cid_info) < str_add_flags_len and additional_flags != 0):
                raise AssertionError("Invalid CID Info format")
            # end if

            cid_info_config = CidInfoPayload.fromHexList(HexList(cid_info))
            cid_info_flags = int(Numeral(HexList(cid_info_config.flags)))
            cid_info_additional_flags = int(Numeral(HexList(cid_info_config.additional_flags)))

            if (cid_info_flags & (CidInfoFlags.VIRTUAL_FLAG >> 8)) != 0 and \
                    (additional_flags & CidInfoFlags.FORCE_RAW_XY_FLAG) == 0:
                # Virtual keys are ignored for now
                continue
            # end if

            if with_flag:
                expected_flags_mask_result = flags
                expected_additional_flags_mask_result = additional_flags
            else:
                expected_flags_mask_result = 0
                expected_additional_flags_mask_result = 0
            # end if

            if len(cid_info) < str_add_flags_len:
                if (cid_info_flags & flags) == expected_flags_mask_result:
                    result.append(cid_info)
                # end if
            else:
                if (cid_info_flags & flags) == expected_flags_mask_result and \
                        (cid_info_additional_flags & additional_flags) == expected_additional_flags_mask_result:
                    result.append(cid_info)
                # end if
            # end if
        # end for
        return result
    # end def cid_info_flags_selection

    def is_cid_info_table_emulated(self, context, emulation, cid_info_table, min_number):
        """
        Check emulation status for a given CID info table

        :param context: Current context
        :type context: ``context``
        :param emulation: CID Emulation required
        :type emulation: ``CidEmulation``
        :param cid_info_table: List of CID info
        :type cid_info_table: ``list``
        :param min_number: Minimum number of CID info matching
        :type min_number: ``int``
        :return: Emulation status
        :rtype: ``bool``
        """
        if emulation != CidEmulation.IGNORED:
            cid_info_table_emu = self.get_emulated(context, cid_info_table)
        else:
            cid_info_table_emu = cid_info_table
        # end if
        if len(cid_info_table_emu) >= min_number:
            result = (emulation == CidEmulation.FULL and (cid_info_table == cid_info_table_emu)) \
                     or (emulation == CidEmulation.LIMITED and (cid_info_table != cid_info_table_emu)) \
                     or (emulation == CidEmulation.IGNORED)
        else:
            result = False
        # end if
        return result
    # end def is_cid_info_table_emulated

    def cid_flags_coverage(self, context, flags=0x0000, with_flags=True, emulation=CidEmulation.IGNORED, min_number=1):
        """
        Get configuration CID Info table coverage, with respect to given flags

        Example:
        +------------+--------+------------+
        |   ctrl id    | divert | emulated |
        +============+========+============+
        |  80 = Left   |   0    |    1     |
        +--------------+--------+----------+
        |  81 = Right  |   0    |    1     |
        +--------------+--------+----------+
        | 82 = Middle  |   1    |    1     |
        +--------------+--------+----------+
        |  82 = Back   |   1    |    0     |
        +--------------+--------+----------+
        | 82 = Forward |   1    |    0     |
        +--------------+--------+----------+

        Can be run:
        @features('Feature1B04WithFlags', CidInfoFlags.DIVERT_FLAG)
        @features('Feature1B04WithFlags', CidInfoFlags.DIVERT_FLAG, 2)
        @features('Feature1B04WithoutFlags', CidInfoFlags.DIVERT_FLAG)
        @features('Feature1B04WithoutFlags', CidInfoFlags.DIVERT_FLAG, 2)
        @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED)
        @features('Feature1B04WithoutFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED)
        @features('Feature1B04WithoutFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL)
        @features('Feature1B04WithoutFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL, 2)

        Can not be run:
        @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL)
        @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED, 2)
        @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL, 2)

        :param context: Current context
        :type context: ``context``
        :param flags: Flags for CID selection
        :type flags: ``int``
        :param with_flags: Select CID info with or without the given flags
        :type with_flags: ``bool``
        :param emulation: CID Emulation required
        :type emulation: ``CidEmulation``
        :param min_number: Minimum number of CID info matching
        :type min_number: ``int``
        :return: Coverage status
        :rtype: ``bool``
        """
        assert min_number > 0, "Min number should be greater than 0"
        # Get configuration
        context_features = context.getFeatures()
        config_manager = ConfigurationManager(context_features)
        cid_info_table = config_manager.get_feature(ConfigurationManager.ID.CID_TABLE)

        cid_info_table = self.cid_info_flags_selection(cid_info_table, flags, with_flags)
        return self.is_cid_info_table_emulated(context, emulation, cid_info_table, min_number)
    # end def cid_flags_coverage

    def cid_groups_coverage(self, context, emulation=CidEmulation.IGNORED, min_number=1):
        """
        Get configuration CID Info table coverage, with respect to given groups

        :param context: Current context
        :type context: ``context``
        :param emulation: CID Emulation required
        :type emulation: ``CidEmulation``
        :param min_number: Minimum number of CID info matching
        :type min_number: ``int``
        :return: Coverage status
        :rtype: ``bool``
        """
        assert min_number > 0, "Min number should be greater than 0"
        # Get configuration
        context_features = context.getFeatures()
        config_manager = ConfigurationManager(context_features)
        cid_info_table = config_manager.get_feature(ConfigurationManager.ID.CID_TABLE)

        cid_table = self.cid_info_table_with_mappable_cids(cid_info_table)
        cid_info_table = [cid_info["raw_cid_info"] for cid_info in cid_table if len(cid_info["mappable"]) > 0]
        return self.is_cid_info_table_emulated(context, emulation, cid_info_table, min_number)
    # end def cid_groups_coverage

    @staticmethod
    def cid_info_table_with_mappable_cids(cid_info_table):
        """
        Get an extended CID info table with a list of CIDs where mapping is possible for each CID

        :param cid_info_table: CID info table (as a ``list`` of raw CID info)
        :type cid_info_table: ``list``

        :return: Extended CID info table (as a ``list[dict]`` with detailed info)
        :rtype: ``list[dict]``
        """
        cid_table = []
        for cid_info in cid_info_table:
            cid_info = CidInfoPayload.fromHexList(HexList(cid_info))
            cid = int(Numeral(cid_info.cid))
            group = int(Numeral(cid_info.group))
            gmask = int(Numeral(cid_info.gmask))
            if gmask != 0x00:
                cid_table.append({"raw_cid_info": cid_info, "cid": cid, "group": group, "gmask": gmask, "mappable": []})
            # end if
        # end for
        for cid_row in cid_table:
            cid_row["mappable"] = [
                cid_info["cid"] for cid_info in cid_table if (cid_info["group"] & cid_row["gmask"]) == cid_info["group"]
            ]
        # end for
        return cid_table
    # end def cid_info_table_with_mappable_cids

    def is_remappable(self, context, cid, emulation=False):
        """
        Check if a CID can be remapped to another control (called 'target' below)

        :param context: Current context
        :type context: ``context``
        :param cid: CID
        :type cid: ``int``
        :param emulation: Flag set to True if emulation of the 'target' is required
        :type emulation: ``bool``

        :return: CID remapping status (True if a remapping of this CID is possible)
        :rtype: ``bool``
        """
        # Get configuration
        context_features = context.getFeatures()
        config_manager = ConfigurationManager(context_features)
        cid_info_table = config_manager.get_feature(ConfigurationManager.ID.CID_TABLE)

        cid_table = self.cid_info_table_with_mappable_cids(cid_info_table)
        cid_mappable = []
        for elt in cid_table:
            if elt["cid"] == cid:
                cid_mappable = elt["mappable"]
                break
            # end if
        # end for
        cid_info_table = [cid_info["raw_cid_info"] for cid_info in cid_table
                          if cid_info["cid"] != cid and cid_info["cid"] in cid_mappable]

        if emulation:
            cid_info_table_emu = self.get_emulated(context, cid_info_table)
            return True if cid_info_table_emu else False
        else:
            return True if cid_info_table else False
        # end if
    # end def is_remappable

    def is_remap_target(self, context, cid_target, emulation=False):
        """
        Check if any (emulated if emulation is True) cid can be remapped on this cid target

        :param context: Current context
        :type context: ``context``
        :param cid_target: CID
        :type cid_target: ``int``
        :param emulation: Flag set to True if emulation is required
        :type emulation: ``bool``

        :return: CID remapping status (True if a remapping on this CID target is possible)
        :rtype: ``bool``
        """
        # Get configuration
        context_features = context.getFeatures()
        config_manager = ConfigurationManager(context_features)
        cid_info_table = config_manager.get_feature(ConfigurationManager.ID.CID_TABLE)

        extended_cid_table = self.cid_info_table_with_mappable_cids(cid_info_table)
        cid_info_table = [cid_info["raw_cid_info"] for cid_info in extended_cid_table
                          if cid_info["cid"] != cid_target and cid_target in cid_info["mappable"]]

        if emulation:
            cid_info_table_emu = self.get_emulated(context, cid_info_table)
            return True if cid_info_table_emu else False
        else:
            return True if cid_info_table else False
        # end if
    # end def is_remap_target
# end class CidInfoCoverage

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
