#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.monitormode
:brief: HID++ 2.0 ``MonitorMode`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class StaticMonitorMode(HidppMessage):
    """
    This feature allows to send monitoring notifications
    """
    FEATURE_ID = 0x18B0
    MAX_FUNCTION_INDEX_V0 = 0
    MAX_FUNCTION_INDEX_V1 = 0

    # Monitor modes
    OFF = 0
    KBD_ON = 1
    MOUSE_ON = 2
    ENHANCED_KBD_ON = 3
    KBD_LARGER_MATRIX = 4
    ENHANCED_KBD_LARGER_MATRIX = 5

    # Make or break info
    MAKE = 1
    BREAK = 0

    # Keyboard matrix size
    ROW_UPPER_LIMIT = 18
    COL_UPPER_LIMIT = 15

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class StaticMonitorMode


# noinspection DuplicatedCode
class StaticMonitorModeModel(FeatureModel):
    """
    Define ``StaticMonitorMode`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        SET_MONITOR_MODE = 0

        # Event index
        MONITOR_MODE_BROADCAST = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``StaticMonitorMode`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.SET_MONITOR_MODE: {
                    "request": SetMonitorMode,
                    "response": SetMonitorModeResponse
                }
            },
            "events": {
                cls.INDEX.MONITOR_MODE_BROADCAST: {"report": MonitorModeBroadcastEvent}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.SET_MONITOR_MODE: {
                    "request": SetMonitorMode,
                    "response": SetMonitorModeResponse
                }
            },
            "events": {
                cls.INDEX.MONITOR_MODE_BROADCAST: {"report": MonitorModeBroadcastEvent},
            }
        }

        return {
            "feature_base": StaticMonitorMode,
            "versions": {
                StaticMonitorModeV0.VERSION: {
                    "main_cls": StaticMonitorModeV0,
                    "api": function_map_v0
                },
                StaticMonitorModeV1.VERSION: {
                    "main_cls": StaticMonitorModeV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class StaticMonitorModeModel


class StaticMonitorModeFactory(FeatureFactory):
    """
    Get ``StaticMonitorMode`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``StaticMonitorMode`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``StaticMonitorModeInterface``
        """
        return StaticMonitorModeModel.get_main_cls(version)()
    # end def create
# end class StaticMonitorModeFactory


class StaticMonitorModeInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``StaticMonitorMode``
    """

    def __init__(self):
        # Requests
        self.set_monitor_mode_cls = None

        # Responses
        self.set_monitor_mode_response_cls = None

        # Events
        self.monitor_mode_broadcast_event_cls = None
    # end def __init__
# end class StaticMonitorModeInterface


class StaticMonitorModeV0(StaticMonitorModeInterface):
    """
    Define ``StaticMonitorModeV0`` feature

    This feature provides model and unit specific information for version 0

    [0] SetMonitorMode(Mode) -> Mode

    [Event 0] MonitorModeBroadcastEvent -> ModeSpecificMonitorReport
    """
    VERSION = 0

    def __init__(self):
        # See ``StaticMonitorMode.__init__``
        super().__init__()
        index = StaticMonitorModeModel.INDEX

        # Requests
        self.set_monitor_mode_cls = StaticMonitorModeModel.get_request_cls(
            self.VERSION, index.SET_MONITOR_MODE)

        # Responses
        self.set_monitor_mode_response_cls = StaticMonitorModeModel.get_response_cls(
            self.VERSION, index.SET_MONITOR_MODE)

        # Events
        self.monitor_mode_broadcast_event_cls = StaticMonitorModeModel.get_report_cls(
            self.VERSION, index.MONITOR_MODE_BROADCAST)
    # end def __init__

    def get_max_function_index(self):
        # See ``StaticMonitorModeInterface.get_max_function_index``
        return StaticMonitorModeModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class StaticMonitorModeV0


class StaticMonitorModeV1(StaticMonitorModeV0):
    """
    Define ``StaticMonitorModeV1`` feature

    This feature provides model and unit specific information for version 1

    [0] SetMonitorMode(Mode) -> Mode

    [Event 0] MonitorModeBroadcastEvent -> ModeSpecificMonitorReport
    """
    VERSION = 1

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``StaticMonitorModeInterface.get_max_function_index``
        return StaticMonitorModeModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class StaticMonitorModeV1


class SetMonitorMode(StaticMonitorMode):
    """
    Define ``SetMonitorMode`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Mode                          8
    Padding                       16
    ============================  ==========
    """

    class FID(StaticMonitorMode.FID):
        # See ``StaticMonitorMode.FID``
        MODE = StaticMonitorMode.FID.SOFTWARE_ID - 1
        PADDING = MODE - 1
    # end class FID

    class LEN(StaticMonitorMode.LEN):
        # See ``StaticMonitorMode.LEN``
        MODE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = StaticMonitorMode.FIELDS + (
        BitField(fid=FID.MODE, length=LEN.MODE,
                 title="Mode", name="mode",
                 checks=(CheckHexList(LEN.MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=StaticMonitorMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param mode: Mode
        :type mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetMonitorModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.mode = mode
    # end def __init__
# end class SetMonitorMode


class SetMonitorModeResponse(StaticMonitorMode):
    """
    Define ``SetMonitorModeResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Mode                          8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetMonitorMode,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(StaticMonitorMode.FID):
        # See ``StaticMonitorMode.FID``
        MODE = StaticMonitorMode.FID.SOFTWARE_ID - 1
        PADDING = MODE - 1
    # end class FID

    class LEN(StaticMonitorMode.LEN):
        # See ``StaticMonitorMode.LEN``
        MODE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = StaticMonitorMode.FIELDS + (
        BitField(fid=FID.MODE, length=LEN.MODE,
                 title="Mode", name="mode",
                 checks=(CheckHexList(LEN.MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=StaticMonitorMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param mode: Mode
        :type mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mode = mode
    # end def __init__
# end class SetMonitorModeResponse


class MonitorModeBroadcastEvent(StaticMonitorMode):
    """
    Define ``MonitorModeBroadcastEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Mode Specific Monitor Report  128
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(StaticMonitorMode.FID):
        # See ``StaticMonitorMode.FID``
        MODE_SPECIFIC_MONITOR_REPORT = StaticMonitorMode.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(StaticMonitorMode.LEN):
        # See ``StaticMonitorMode.LEN``
        MODE_SPECIFIC_MONITOR_REPORT = 0x80
    # end class LEN

    FIELDS = StaticMonitorMode.FIELDS + (
        BitField(fid=FID.MODE_SPECIFIC_MONITOR_REPORT, length=LEN.MODE_SPECIFIC_MONITOR_REPORT,
                 title="ModeSpecificMonitorReport", name="mode_specific_monitor_report",
                 checks=(CheckHexList(LEN.MODE_SPECIFIC_MONITOR_REPORT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MODE_SPECIFIC_MONITOR_REPORT) - 1),)),
    )

    def __init__(self, device_index, feature_index, mode_specific_monitor_report, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param mode_specific_monitor_report: Mode Specific Monitor Report
        :type mode_specific_monitor_report: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.mode_specific_monitor_report = mode_specific_monitor_report
    # end def __init__
# end class MonitorModeBroadcastEvent


class KeyboardModeEvent(StaticMonitorMode):
    """
    Define ``KeyboardModeEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Row Col Code                  8
    Break Or Make Info            8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    class FID(MonitorModeBroadcastEvent.FID):
        # See ``StaticMonitorMode.FID``
        ROW_COL_CODE = MonitorModeBroadcastEvent.FID.SOFTWARE_ID - 1
        BREAK_OR_MAKE_INFO = ROW_COL_CODE - 1
        PADDING = BREAK_OR_MAKE_INFO - 1
    # end class FID

    class LEN(MonitorModeBroadcastEvent.LEN):
        # See ``StaticMonitorMode.LEN``
        ROW_COL_CODE = 0x8
        BREAK_OR_MAKE_INFO = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = StaticMonitorMode.FIELDS + (
        BitField(fid=FID.ROW_COL_CODE, length=LEN.ROW_COL_CODE,
                 title="RowColCode", name="row_col_code",
                 checks=(CheckHexList(LEN.ROW_COL_CODE // 8), CheckByte(),)),
        BitField(fid=FID.BREAK_OR_MAKE_INFO, length=LEN.BREAK_OR_MAKE_INFO,
                 title="BreakOrMakeInfo", name="break_or_make_info",
                 checks=(CheckHexList(LEN.BREAK_OR_MAKE_INFO // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=StaticMonitorMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, row_col_code, break_or_make_info, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param row_col_code: Row Col Code
        :type row_col_code: ``int | HexList``
        :param break_or_make_info: Break Or Make Info
        :type break_or_make_info: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.row_col_code = row_col_code
        self.break_or_make_info = break_or_make_info
    # end def __init__

    # Make or break info
    MAKE = 1
    BREAK = 0
# end class KeyboardModeEvent

class MouseModeEvent(StaticMonitorMode):
    """
    Define ``MouseModeEvent`` implementation class

    Format:
    ===============================  ==========
    Name                             Bit count
    ===============================  ==========
    X Value                          16
    Y Value                          16
    Tilt Left Or Right Analog Value  8
    Back And Forward Analog Values   8
    Roller Value                     8
    Time Between Ratchets            8
    Switches                         16
    Padding                          48
    ===============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 2

    class FID(MonitorModeBroadcastEvent.FID):
        # See ``StaticMonitorMode.FID``
        X_VALUE = StaticMonitorMode.FID.SOFTWARE_ID - 1
        Y_VALUE = X_VALUE - 1
        TILT_LEFT_OR_RIGHT_ANALOG_VALUE = Y_VALUE - 1
        BACK_AND_FORWARD_ANALOG_VALUES = TILT_LEFT_OR_RIGHT_ANALOG_VALUE - 1
        ROLLER_VALUE = BACK_AND_FORWARD_ANALOG_VALUES - 1
        TIME_BETWEEN_RATCHETS = ROLLER_VALUE - 1
        SWITCHES = TIME_BETWEEN_RATCHETS - 1
        PADDING = SWITCHES - 1
    # end class FID

    class LEN(MonitorModeBroadcastEvent.LEN):
        # See ``StaticMonitorMode.LEN``
        X_VALUE = 0x10
        Y_VALUE = 0x10
        TILT_LEFT_OR_RIGHT_ANALOG_VALUE = 0x8
        BACK_AND_FORWARD_ANALOG_VALUES = 0x8
        ROLLER_VALUE = 0x8
        TIME_BETWEEN_RATCHETS = 0x8
        SWITCHES = 0x10
        PADDING = 0x30
    # end class LEN

    FIELDS = StaticMonitorMode.FIELDS + (
        BitField(fid=FID.X_VALUE, length=LEN.X_VALUE,
                 title="XValue", name="x_value",
                 checks=(CheckHexList(LEN.X_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.X_VALUE) - 1),)),
        BitField(fid=FID.Y_VALUE, length=LEN.Y_VALUE,
                 title="YValue", name="y_value",
                 checks=(CheckHexList(LEN.Y_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.Y_VALUE) - 1),)),
        BitField(fid=FID.TILT_LEFT_OR_RIGHT_ANALOG_VALUE, length=LEN.TILT_LEFT_OR_RIGHT_ANALOG_VALUE,
                 title="TiltLeftOrRightAnalogValue", name="tilt_left_or_right_analog_value",
                 checks=(CheckHexList(LEN.TILT_LEFT_OR_RIGHT_ANALOG_VALUE // 8), CheckByte(),)),
        BitField(fid=FID.BACK_AND_FORWARD_ANALOG_VALUES, length=LEN.BACK_AND_FORWARD_ANALOG_VALUES,
                 title="BackAndForwardAnalogValues", name="back_and_forward_analog_values",
                 checks=(CheckHexList(LEN.BACK_AND_FORWARD_ANALOG_VALUES // 8), CheckByte(),)),
        BitField(fid=FID.ROLLER_VALUE, length=LEN.ROLLER_VALUE,
                 title="RollerValue", name="roller_value",
                 checks=(CheckHexList(LEN.ROLLER_VALUE // 8), CheckByte(),)),
        BitField(fid=FID.TIME_BETWEEN_RATCHETS, length=LEN.TIME_BETWEEN_RATCHETS,
                 title="TimeBetweenRatchets", name="time_between_ratchets",
                 checks=(CheckHexList(LEN.TIME_BETWEEN_RATCHETS // 8), CheckByte(),)),
        BitField(fid=FID.SWITCHES, length=LEN.SWITCHES,
                 title="Switches", name="switches",
                 checks=(CheckHexList(LEN.SWITCHES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SWITCHES) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=StaticMonitorMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, x_value, y_value, tilt_left_or_right_analog_value,
                 back_and_forward_analog_values, roller_value, time_between_ratchets, switches, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param x_value: X Value
        :type x_value: ``int | HexList``
        :param y_value: Y Value
        :type y_value: ``int | HexList``
        :param tilt_left_or_right_analog_value: Tilt Left Or Right Analog Value
        :type tilt_left_or_right_analog_value: ``int | HexList``
        :param back_and_forward_analog_values: Back And Forward Analog Values
        :type back_and_forward_analog_values: ``int | HexList``
        :param roller_value: Roller Value
        :type roller_value: ``int | HexList``
        :param time_between_ratchets: Time Between Ratchets
        :type time_between_ratchets: ``int | HexList``
        :param switches: Switches
        :type switches: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.x_value = x_value
        self.y_value = y_value
        self.tilt_left_or_right_analog_value = tilt_left_or_right_analog_value
        self.back_and_forward_analog_values = back_and_forward_analog_values
        self.roller_value = roller_value
        self.time_between_ratchets = time_between_ratchets
        self.switches = switches
    # end def __init__
# end class MouseModeEvent


class EnhancedKeyboardModeEvent(StaticMonitorMode):
    """
    Define ``EnhancedKeyboardModeEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Row Col Code 0                8
    Row Col Code 1                8
    Row Col Code 2                8
    Row Col Code 3                8
    Row Col Code 4                8
    Row Col Code 5                8
    Row Col Code 6                8
    Row Col Code 7                8
    Padding                       64
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 3

    class FID(MonitorModeBroadcastEvent.FID):
        # See ``StaticMonitorMode.FID``
        ROW_COL_CODE_0 = MonitorModeBroadcastEvent.FID.SOFTWARE_ID - 1
        ROW_COL_CODE_1 = ROW_COL_CODE_0 - 1
        ROW_COL_CODE_2 = ROW_COL_CODE_1 - 1
        ROW_COL_CODE_3 = ROW_COL_CODE_2 - 1
        ROW_COL_CODE_4 = ROW_COL_CODE_3 - 1
        ROW_COL_CODE_5 = ROW_COL_CODE_4 - 1
        ROW_COL_CODE_6 = ROW_COL_CODE_5 - 1
        ROW_COL_CODE_7 = ROW_COL_CODE_6 - 1
        PADDING = ROW_COL_CODE_7 - 1
    # end class FID

    class LEN(MonitorModeBroadcastEvent.LEN):
        # See ``StaticMonitorMode.LEN``
        ROW_COL_CODE_0 = 0x8
        ROW_COL_CODE_1 = 0x8
        ROW_COL_CODE_2 = 0x8
        ROW_COL_CODE_3 = 0x8
        ROW_COL_CODE_4 = 0x8
        ROW_COL_CODE_5 = 0x8
        ROW_COL_CODE_6 = 0x8
        ROW_COL_CODE_7 = 0x8
        PADDING = 0x40
    # end class LEN

    FIELDS = StaticMonitorMode.FIELDS + (
        BitField(fid=FID.ROW_COL_CODE_0, length=LEN.ROW_COL_CODE_0,
                 title="RowColCode0", name="row_col_code_0",
                 checks=(CheckHexList(LEN.ROW_COL_CODE_0 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_COL_CODE_1, length=LEN.ROW_COL_CODE_1,
                 title="RowColCode1", name="row_col_code_1",
                 checks=(CheckHexList(LEN.ROW_COL_CODE_1 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_COL_CODE_2, length=LEN.ROW_COL_CODE_2,
                 title="RowColCode2", name="row_col_code_2",
                 checks=(CheckHexList(LEN.ROW_COL_CODE_2 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_COL_CODE_3, length=LEN.ROW_COL_CODE_3,
                 title="RowColCode3", name="row_col_code_3",
                 checks=(CheckHexList(LEN.ROW_COL_CODE_3 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_COL_CODE_4, length=LEN.ROW_COL_CODE_4,
                 title="RowColCode4", name="row_col_code_4",
                 checks=(CheckHexList(LEN.ROW_COL_CODE_4 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_COL_CODE_5, length=LEN.ROW_COL_CODE_5,
                 title="RowColCode5", name="row_col_code_5",
                 checks=(CheckHexList(LEN.ROW_COL_CODE_5 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_COL_CODE_6, length=LEN.ROW_COL_CODE_6,
                 title="RowColCode6", name="row_col_code_6",
                 checks=(CheckHexList(LEN.ROW_COL_CODE_6 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_COL_CODE_7, length=LEN.ROW_COL_CODE_7,
                 title="RowColCode7", name="row_col_code_7",
                 checks=(CheckHexList(LEN.ROW_COL_CODE_7 // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=StaticMonitorMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, row_col_code_0, row_col_code_1, row_col_code_2, row_col_code_3,
                 row_col_code_4, row_col_code_5, row_col_code_6, row_col_code_7, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param row_col_code_0: Row Col Code 0
        :type row_col_code_0: ``int | HexList``
        :param row_col_code_1: Row Col Code 1
        :type row_col_code_1: ``int | HexList``
        :param row_col_code_2: Row Col Code 2
        :type row_col_code_2: ``int | HexList``
        :param row_col_code_3: Row Col Code 3
        :type row_col_code_3: ``int | HexList``
        :param row_col_code_4: Row Col Code 4
        :type row_col_code_4: ``int | HexList``
        :param row_col_code_5: Row Col Code 5
        :type row_col_code_5: ``int | HexList``
        :param row_col_code_6: Row Col Code 6
        :type row_col_code_6: ``int | HexList``
        :param row_col_code_7: Row Col Code 7
        :type row_col_code_7: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.row_col_code_0 = row_col_code_0
        self.row_col_code_1 = row_col_code_1
        self.row_col_code_2 = row_col_code_2
        self.row_col_code_3 = row_col_code_3
        self.row_col_code_4 = row_col_code_4
        self.row_col_code_5 = row_col_code_5
        self.row_col_code_6 = row_col_code_6
        self.row_col_code_7 = row_col_code_7
    # end def __init__
# end class EnhancedKeyboardModeEvent


class KeyboardWithLargerMatrixModeEvent(StaticMonitorMode):
    """
    Define ``KeyboardWithLargerMatrixModeEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Row Code                      8
    Col Code                      8
    Break Or Make Info            8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
    FUNCTION_INDEX = 4

    class FID(StaticMonitorMode.FID):
        # See ``StaticMonitorMode.FID``
        ROW_CODE = MonitorModeBroadcastEvent.FID.SOFTWARE_ID - 1
        COL_CODE = ROW_CODE - 1
        BREAK_OR_MAKE_INFO = COL_CODE - 1
        PADDING = BREAK_OR_MAKE_INFO - 1
    # end class FID

    class LEN(StaticMonitorMode.LEN):
        # See ``StaticMonitorMode.LEN``
        ROW_CODE = 0x8
        COL_CODE = 0x8
        BREAK_OR_MAKE_INFO = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = StaticMonitorMode.FIELDS + (
        BitField(fid=FID.ROW_CODE, length=LEN.ROW_CODE,
                 title="RowCode", name="row_code",
                 checks=(CheckHexList(LEN.ROW_CODE // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE, length=LEN.COL_CODE,
                 title="ColCode", name="col_code",
                 checks=(CheckHexList(LEN.COL_CODE // 8), CheckByte(),)),
        BitField(fid=FID.BREAK_OR_MAKE_INFO, length=LEN.BREAK_OR_MAKE_INFO,
                 title="BreakOrMakeInfo", name="break_or_make_info",
                 checks=(CheckHexList(LEN.BREAK_OR_MAKE_INFO // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=StaticMonitorMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, row_code, col_code, break_or_make_info, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param row_code: Row Code
        :type row_code: ``int | HexList``
        :param col_code: Col Code
        :type col_code: ``int | HexList``
        :param break_or_make_info: Break Or Make Info
        :type break_or_make_info: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.row_code = row_code
        self.col_code = col_code
        self.break_or_make_info = break_or_make_info
    # end def __init__
# end class KeyboardWithLargerMatrixModeEvent


class EnhancedKeyboardWithLargerMatrixModeEvent(StaticMonitorMode):
    """
    Define ``EnhancedKeyboardWithLargerMatrixModeEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Row Code 0                    8
    Col Code 0                    8
    Row Code 1                    8
    Col Code 1                    8
    Row Code 2                    8
    Col Code 2                    8
    Row Code 3                    8
    Col Code 3                    8
    Row Code 4                    8
    Col Code 4                    8
    Row Code 5                    8
    Col Code 5                    8
    Row Code 6                    8
    Col Code 6                    8
    Row Code 7                    8
    Col Code 7                    8
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
    FUNCTION_INDEX = 5

    class FID(StaticMonitorMode.FID):
        # See ``StaticMonitorMode.FID``
        ROW_CODE_0 = MonitorModeBroadcastEvent.FID.SOFTWARE_ID - 1
        COL_CODE_0 = ROW_CODE_0 - 1
        ROW_CODE_1 = COL_CODE_0 - 1
        COL_CODE_1 = ROW_CODE_1 - 1
        ROW_CODE_2 = COL_CODE_1 - 1
        COL_CODE_2 = ROW_CODE_2 - 1
        ROW_CODE_3 = COL_CODE_2 - 1
        COL_CODE_3 = ROW_CODE_3 - 1
        ROW_CODE_4 = COL_CODE_3 - 1
        COL_CODE_4 = ROW_CODE_4 - 1
        ROW_CODE_5 = COL_CODE_4 - 1
        COL_CODE_5 = ROW_CODE_5 - 1
        ROW_CODE_6 = COL_CODE_5 - 1
        COL_CODE_6 = ROW_CODE_6 - 1
        ROW_CODE_7 = COL_CODE_6 - 1
        COL_CODE_7 = ROW_CODE_7 - 1
    # end class FID

    class LEN(StaticMonitorMode.LEN):
        # See ``StaticMonitorMode.LEN``
        ROW_CODE_0 = 0x8
        COL_CODE_0 = 0x8
        ROW_CODE_1 = 0x8
        COL_CODE_1 = 0x8
        ROW_CODE_2 = 0x8
        COL_CODE_2 = 0x8
        ROW_CODE_3 = 0x8
        COL_CODE_3 = 0x8
        ROW_CODE_4 = 0x8
        COL_CODE_4 = 0x8
        ROW_CODE_5 = 0x8
        COL_CODE_5 = 0x8
        ROW_CODE_6 = 0x8
        COL_CODE_6 = 0x8
        ROW_CODE_7 = 0x8
        COL_CODE_7 = 0x8
    # end class LEN

    FIELDS = StaticMonitorMode.FIELDS + (
        BitField(fid=FID.ROW_CODE_0, length=LEN.ROW_CODE_0,
                 title="RowCode0", name="row_code_0",
                 checks=(CheckHexList(LEN.ROW_CODE_0 // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE_0, length=LEN.COL_CODE_0,
                 title="ColCode0", name="col_code_0",
                 checks=(CheckHexList(LEN.COL_CODE_0 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_CODE_1, length=LEN.ROW_CODE_1,
                 title="RowCode1", name="row_code_1",
                 checks=(CheckHexList(LEN.ROW_CODE_1 // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE_1, length=LEN.COL_CODE_1,
                 title="ColCode1", name="col_code_1",
                 checks=(CheckHexList(LEN.COL_CODE_1 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_CODE_2, length=LEN.ROW_CODE_2,
                 title="RowCode2", name="row_code_2",
                 checks=(CheckHexList(LEN.ROW_CODE_2 // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE_2, length=LEN.COL_CODE_2,
                 title="ColCode2", name="col_code_2",
                 checks=(CheckHexList(LEN.COL_CODE_2 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_CODE_3, length=LEN.ROW_CODE_3,
                 title="RowCode3", name="row_code_3",
                 checks=(CheckHexList(LEN.ROW_CODE_3 // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE_3, length=LEN.COL_CODE_3,
                 title="ColCode3", name="col_code_3",
                 checks=(CheckHexList(LEN.COL_CODE_3 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_CODE_4, length=LEN.ROW_CODE_4,
                 title="RowCode4", name="row_code_4",
                 checks=(CheckHexList(LEN.ROW_CODE_4 // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE_4, length=LEN.COL_CODE_4,
                 title="ColCode4", name="col_code_4",
                 checks=(CheckHexList(LEN.COL_CODE_4 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_CODE_5, length=LEN.ROW_CODE_5,
                 title="RowCode5", name="row_code_5",
                 checks=(CheckHexList(LEN.ROW_CODE_5 // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE_5, length=LEN.COL_CODE_5,
                 title="ColCode5", name="col_code_5",
                 checks=(CheckHexList(LEN.COL_CODE_5 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_CODE_6, length=LEN.ROW_CODE_6,
                 title="RowCode6", name="row_code_6",
                 checks=(CheckHexList(LEN.ROW_CODE_6 // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE_6, length=LEN.COL_CODE_6,
                 title="ColCode6", name="col_code_6",
                 checks=(CheckHexList(LEN.COL_CODE_6 // 8), CheckByte(),)),
        BitField(fid=FID.ROW_CODE_7, length=LEN.ROW_CODE_7,
                 title="RowCode7", name="row_code_7",
                 checks=(CheckHexList(LEN.ROW_CODE_7 // 8), CheckByte(),)),
        BitField(fid=FID.COL_CODE_7, length=LEN.COL_CODE_7,
                 title="ColCode7", name="col_code_7",
                 checks=(CheckHexList(LEN.COL_CODE_7 // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, row_code_0, col_code_0, row_code_1, col_code_1, row_code_2,
                 col_code_2, row_code_3, col_code_3, row_code_4, col_code_4, row_code_5, col_code_5, row_code_6,
                 col_code_6, row_code_7, col_code_7, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param row_code_0: Row Code 0
        :type row_code_0: ``int | HexList``
        :param col_code_0: Col Code 0
        :type col_code_0: ``int | HexList``
        :param row_code_1: Row Code 1
        :type row_code_1: ``int | HexList``
        :param col_code_1: Col Code 1
        :type col_code_1: ``int | HexList``
        :param row_code_2: Row Code 2
        :type row_code_2: ``int | HexList``
        :param col_code_2: Col Code 2
        :type col_code_2: ``int | HexList``
        :param row_code_3: Row Code 3
        :type row_code_3: ``int | HexList``
        :param col_code_3: Col Code 3
        :type col_code_3: ``int | HexList``
        :param row_code_4: Row Code 4
        :type row_code_4: ``int | HexList``
        :param col_code_4: Col Code 4
        :type col_code_4: ``int | HexList``
        :param row_code_5: Row Code 5
        :type row_code_5: ``int | HexList``
        :param col_code_5: Col Code 5
        :type col_code_5: ``int | HexList``
        :param row_code_6: Row Code 6
        :type row_code_6: ``int | HexList``
        :param col_code_6: Col Code 6
        :type col_code_6: ``int | HexList``
        :param row_code_7: Row Code 7
        :type row_code_7: ``int | HexList``
        :param col_code_7: Col Code 7
        :type col_code_7: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.row_code_0 = row_code_0
        self.col_code_0 = col_code_0
        self.row_code_1 = row_code_1
        self.col_code_1 = col_code_1
        self.row_code_2 = row_code_2
        self.col_code_2 = col_code_2
        self.row_code_3 = row_code_3
        self.col_code_3 = col_code_3
        self.row_code_4 = row_code_4
        self.col_code_4 = col_code_4
        self.row_code_5 = row_code_5
        self.col_code_5 = col_code_5
        self.row_code_6 = row_code_6
        self.col_code_6 = col_code_6
        self.row_code_7 = row_code_7
        self.col_code_7 = col_code_7
    # end def __init__
# end class EnhancedKeyboardWithLargerMatrixModeEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
