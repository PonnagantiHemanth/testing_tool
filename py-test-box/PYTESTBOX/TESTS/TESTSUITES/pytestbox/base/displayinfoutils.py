#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.base.displayinfoutils
:brief: Help for Display Info of Contextual Keys feature 0x19A1
:author: Vinodh Selvaraj<vselvaraj2@logitech.com>
:date: 2023/11/09
"""
from pyhid.vlp.features.common.contextualdisplay import ButtonInfoPayload
from pyhid.vlp.features.common.contextualdisplay import DisplayInfoPayload
from pyhid.vlp.features.common.contextualdisplay import VisibleAreaInfoPayload
from pytestbox.base.configurationmanager import ConfigurationManager


# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

class DisplayInfoConfig:
    """
    Class representing Display Info from configuration
    """

    def __init__(self, index, display_index, shape, dimension, h_res, v_res, button_count, visible_area_count):
        """
        Constructor

        :param index: Index in the Display info table
        :type index: ``int``
        :param display_index: Display Index in the Display info table
        :type display_index: ``int``
        :param shape: Display Shape in the Display info table
        :type shape: ``int|HexList``
        :param dimension: Display Dimension in the Display info table
        :type dimension: ``int|HexList``
        :param h_res: Display Horizontal Resolution in the Display info table
        :type h_res: ``int|HexList``
        :param v_res: Display Vertical Resolution in the Display info table
        :type v_res: ``int|HexList``
        :param button_count: Display Button Count in the Display info table
        :type button_count: ``int|HexList``
        :param visible_area_count: Display Visible Area Count in the Display info table
        :type visible_area_count: ``int|HexList``
        """
        self.index = index
        self.display_index = display_index
        self.display_info_payload = DisplayInfoPayload(shape, dimension, h_res, v_res, button_count, visible_area_count)
    # end def __init__

    @classmethod
    def from_index(cls, features, index, config_manager=None):
        """
        Constructor from index in the Display info table in configuration.
        :param features: Context features
        :type features: ``context.features``
        :param index: Index in the CID info table
        :type index: ``int``
        :param config_manager: Configuration manager - OPTIONAL
        :type config_manager: ``ConfigurationManager``

        :return: Class instance
        :rtype: ``DisplayInfoConfig``
        """
        config_manager = ConfigurationManager(features) if config_manager is None else config_manager
        return cls(index,
                   config_manager.get_feature(ConfigurationManager.ID.DISPLAY_INFO_TABLE_INDEX)[index],
                   config_manager.get_feature(ConfigurationManager.ID.DISPLAY_INFO_TABLE_DISPLAY_SHAPE)[index],
                   config_manager.get_feature(ConfigurationManager.ID.DISPLAY_INFO_TABLE_DIMENSION)[index],
                   config_manager.get_feature(ConfigurationManager.ID.DISPLAY_INFO_TABLE_H_RES)[index],
                   config_manager.get_feature(ConfigurationManager.ID.DISPLAY_INFO_TABLE_V_RES)[index],
                   config_manager.get_feature(ConfigurationManager.ID.DISPLAY_INFO_TABLE_BUTTON_COUNT)[index],
                   config_manager.get_feature(ConfigurationManager.ID.DISPLAY_INFO_TABLE_VISIBLE_AREA_COUNT)[index])
    # end def from_index
# end class DisplayInfoConfig

class ButtonInfoConfig:
    """
    Class representing Button Info from configuration
    """

    def __init__(self, index, button_index, shape, loc_x, loc_y, loc_width, loc_height):
        """
        Constructor

        :param index: Index in the Button info table
        :type index: ``int``
        :param button_index: Button Index in the Button info table
        :type button_index: ``int``
        :param shape: Button Shape in the Button info table
        :type shape: ``int|HexList``
        :param loc_x: Button Location X in the Button info table
        :type loc_x: ``int|HexList``
        :param loc_y: Button Location Y in the Button info table
        :type loc_y: ``int|HexList``
        :param loc_width: Button Location Width in the Button info table
        :type loc_width: ``int|HexList``
        :param loc_height: Button Location Height in the Button info table
        :type loc_height: ``int|HexList``
        """
        self.index = index
        self.button_index = button_index
        self.button_info_payload = ButtonInfoPayload(shape, loc_x, loc_y, loc_width, loc_height)
    # end def __init__

    @classmethod
    def from_index(cls, features, index, config_manager=None):
        """
        Constructor from index in the Button info table in configuration.
        :param features: Context features
        :type features: ``context.features``
        :param index: Index in the CID info table
        :type index: ``int``
        :param config_manager: Configuration manager - OPTIONAL
        :type config_manager: ``ConfigurationManager``

        :return: Class instance
        :rtype: ``ButtonInfoConfig``
        """
        config_manager = ConfigurationManager(features) if config_manager is None else config_manager
        return cls(index,
                   config_manager.get_feature(ConfigurationManager.ID.BUTTON_TABLE_INDEX)[index],
                   config_manager.get_feature(ConfigurationManager.ID.BUTTON_TABLE_BUTTON_SHAPE)[index],
                   config_manager.get_feature(ConfigurationManager.ID.BUTTON_TABLE_LOC_X)[index],
                   config_manager.get_feature(ConfigurationManager.ID.BUTTON_TABLE_LOC_Y)[index],
                   config_manager.get_feature(ConfigurationManager.ID.BUTTON_TABLE_LOC_WIDTH)[index],
                   config_manager.get_feature(ConfigurationManager.ID.BUTTON_TABLE_LOC_HEIGHT)[index])
    # end def from_index
# end class ButtonInfoConfig

class VisibleAreaInfoConfig:
    """
    Class representing Visible Area Info from configuration
    """

    def __init__(self, index, visible_area_index, shape, loc_x, loc_y, loc_width, loc_height):
        """
        Constructor

        :param index: Index in the Visible Area info table
        :type index: ``int``
        :param visible_area_index: Visible Area Index in the Visible Area info table
        :type visible_area_index: ``int``
        :param shape: Visible Area Shape in the Visible Area info table
        :type shape: ``int|HexList``
        :param loc_x: Visible Area Location X in the Visible Area info table
        :type loc_x: ``int|HexList``
        :param loc_y: Visible Area Location Y in the Visible Area info table
        :type loc_y: ``int|HexList``
        :param loc_width: Visible Area Location Width in the Visible Area info table
        :type loc_width: ``int|HexList``
        :param loc_height: Visible Area Location Height in the Visible Area info table
        :type loc_height: ``int|HexList``
        """
        self.index = index
        self.visible_area_index = visible_area_index
        self.visible_area_info_payload = VisibleAreaInfoPayload(shape, loc_x, loc_y, loc_width, loc_height)
    # end def __init__

    @classmethod
    def from_index(cls, features, index, config_manager=None):
        """
        Constructor from index in the Visible Area info table in configuration.
        :param features: Context features
        :type features: ``context.features``
        :param index: Index in the CID info table
        :type index: ``int``
        :param config_manager: Configuration manager - OPTIONAL
        :type config_manager: ``ConfigurationManager``

        :return: Class instance
        :rtype: ``VisibleAreaInfoConfig``
        """
        config_manager = ConfigurationManager(features) if config_manager is None else config_manager
        return cls(index,
                   config_manager.get_feature(ConfigurationManager.ID.VISIBLE_AREA_TABLE_INDEX)[index],
                   config_manager.get_feature(ConfigurationManager.ID.VISIBLE_AREA_TABLE_AREA_SHAPE)[index],
                   config_manager.get_feature(ConfigurationManager.ID.VISIBLE_AREA_TABLE_LOC_X)[index],
                   config_manager.get_feature(ConfigurationManager.ID.VISIBLE_AREA_TABLE_LOC_Y)[index],
                   config_manager.get_feature(ConfigurationManager.ID.VISIBLE_AREA_TABLE_LOC_WIDTH)[index],
                   config_manager.get_feature(ConfigurationManager.ID.VISIBLE_AREA_TABLE_LOC_HEIGHT)[index])
    # end def from_index
# end class VisibleAreaInfoConfig
